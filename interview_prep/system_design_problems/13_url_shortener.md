# URL Shortener (TinyURL) System Design

## Requirements

### Functional
- Convert long URL to short URL
- Redirect short URL to original
- Custom short URLs
- Analytics (click tracking)
- Expiration support
- QR code generation

### Non-Functional
- Handles 1,000 short links created/second
- Redirect latency < 100ms
- 99.9% availability
- URL accessible for years
- URL length optimized (6-8 characters)

## System Architecture

```
User Input     Encode Service     Database          Analytics
Long URL -----> Generate Code -----> Store URL ----> Track Clicks
                                       |
           Read Service <----- Redirect Service <---- Get URL
             Short URL <------ Lookup
```

## Core Design

### URL Encoding

#### Base62 Encoding (Alphanumeric)
```python
import string

class URLShortener:
    BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase
    BASE = len(BASE62_CHARS)  # 62
    
    def __init__(self):
        self.url_map = {}  # {short_code: long_url}
        self.counter = 0
        self.lock = threading.Lock()
    
    def encode(self, num):
        """Convert number to base62"""
        if num == 0:
            return self.BASE62_CHARS[0]
        
        encoded = []
        while num > 0:
            encoded.append(self.BASE62_CHARS[num % self.BASE])
            num //= self.BASE
        
        return ''.join(reversed(encoded))
    
    def decode(self, code):
        """Convert base62 to number"""
        num = 0
        for char in code:
            num = num * self.BASE + self.BASE62_CHARS.index(char)
        return num
    
    def shorten(self, long_url):
        """Create short URL"""
        with self.lock:
            short_code = self.encode(self.counter)
            self.counter += 1
            
            self.url_map[short_code] = {
                "long_url": long_url,
                "created_at": datetime.now(),
                "clicks": 0
            }
            
            return f"https://tinyurl.com/{short_code}"
    
    def expand(self, short_code):
        """Get long URL from short code"""
        if short_code in self.url_map:
            entry = self.url_map[short_code]
            entry["clicks"] += 1  # Track click
            return entry["long_url"]
        
        return None

# Test
shortener = URLShortener()
short = shortener.shorten("https://www.example.com/very/long/url")
print(short)  # https://tinyurl.com/a
expanded = shortener.expand("a")
print(expanded)  # https://www.example.com/very/long/url
```

#### MD5 Hash Approach
```python
import hashlib

class MD5URLShortener:
    def __init__(self):
        self.url_map = {}
        self.counter = 0
    
    def shorten(self, long_url):
        """Create short URL using MD5"""
        # Generate hash
        hash_digest = hashlib.md5(long_url.encode()).hexdigest()
        
        # Take first 6 characters
        short_code = hash_digest[:6]
        
        # Handle collision (unlikely with MD5)
        if short_code in self.url_map:
            # Use more characters or add counter
            short_code = hash_digest[:8]
        
        self.url_map[short_code] = long_url
        return f"https://tinyurl.com/{short_code}"
    
    def expand(self, short_code):
        return self.url_map.get(short_code)
```

## Database Schema

```sql
CREATE TABLE urls (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    short_code VARCHAR(8) UNIQUE NOT NULL,
    long_url VARCHAR(2048) NOT NULL,
    user_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_short_code (short_code),
    INDEX idx_user_id (user_id)
);

CREATE TABLE analytics (
    id BIGINT PRIMARY KEY,
    short_code VARCHAR(8),
    user_agent VARCHAR(500),
    ip_address VARCHAR(45),
    referer VARCHAR(2048),
    clicked_at TIMESTAMP,
    FOREIGN KEY (short_code) REFERENCES urls(short_code),
    INDEX idx_short_code (short_code),
    INDEX idx_clicked_at (clicked_at)
);
```

## Full Implementation

```python
class URLShortenerService:
    def __init__(self, db):
        self.db = db
        self.cache = {}  # Redis in production
        self.lock = threading.RLock()
    
    def create_short_url(self, user_id, long_url, custom_code=None, expires_in_days=None):
        """Create short URL"""
        with self.lock:
            # Validate URL
            if not self._is_valid_url(long_url):
                return None, "Invalid URL"
            
            # Check if URL already shortened
            existing = self.db.get_by_long_url(long_url, user_id)
            if existing:
                return existing["short_code"], "Already shortened"
            
            # Generate or use custom code
            if custom_code:
                if self.db.is_code_taken(custom_code):
                    return None, "Custom code taken"
                short_code = custom_code
            else:
                short_code = self._generate_unique_code()
            
            # Calculate expiration
            expires_at = None
            if expires_in_days:
                expires_at = datetime.now() + timedelta(days=expires_in_days)
            
            # Store in database
            url_entry = {
                "short_code": short_code,
                "long_url": long_url,
                "user_id": user_id,
                "expires_at": expires_at,
                "clicks": 0,
                "created_at": datetime.now()
            }
            
            self.db.save_url(url_entry)
            self.cache[short_code] = url_entry
            
            return short_code, "Success"
    
    def get_long_url(self, short_code):
        """Get original URL and track click"""
        # Try cache first
        if short_code in self.cache:
            entry = self.cache[short_code]
        else:
            entry = self.db.get_url(short_code)
            if entry:
                self.cache[short_code] = entry
        
        if not entry:
            return None
        
        # Check expiration
        if entry.get("expires_at") and datetime.now() > entry["expires_at"]:
            self.db.mark_inactive(short_code)
            return None
        
        # Track click asynchronously
        self._track_click_async(short_code)
        
        return entry["long_url"]
    
    def get_analytics(self, short_code, user_id):
        """Get analytics for URL"""
        # Verify ownership
        url = self.db.get_url(short_code)
        if not url or url["user_id"] != user_id:
            return None
        
        # Get click data
        analytics = self.db.get_analytics(short_code)
        
        return {
            "total_clicks": len(analytics),
            "created_at": url["created_at"],
            "last_click": max([a["clicked_at"] for a in analytics]) if analytics else None,
            "top_referrers": self._get_top_referrers(analytics),
            "browsers": self._get_browser_stats(analytics)
        }
    
    def _track_click_async(self, short_code):
        """Track click in background"""
        def track():
            # Get request context (would be pass in real app)
            analytics_data = {
                "short_code": short_code,
                "user_agent": request.user_agent,
                "ip_address": request.remote_addr,
                "referer": request.referer,
                "clicked_at": datetime.now()
            }
            
            self.db.save_analytics(analytics_data)
        
        thread = threading.Thread(target=track, daemon=True)
        thread.start()
    
    def _generate_unique_code(self):
        """Generate unique 6-character code"""
        import random
        chars = string.digits + string.ascii_lowercase + string.ascii_uppercase
        
        while True:
            code = ''.join(random.choice(chars) for _ in range(6))
            if not self.db.is_code_taken(code):
                return code
    
    def _is_valid_url(self, url):
        """Validate URL format"""
        import re
        pattern = re.compile(
            r'^https?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return pattern.match(url) is not None
    
    def _get_top_referrers(self, analytics):
        from collections import Counter
        referrers = [a.get("referer") for a in analytics if a.get("referer")]
        return Counter(referrers).most_common(5)
    
    def _get_browser_stats(self, analytics):
        from collections import Counter
        browsers = []
        for a in analytics:
            ua = a.get("user_agent", "Unknown")
            if "Chrome" in ua:
                browsers.append("Chrome")
            elif "Firefox" in ua:
                browsers.append("Firefox")
            else:
                browsers.append("Other")
        return dict(Counter(browsers))
```

## API Endpoints

```python
# POST /api/shorten
# Body: {"long_url": "...", "custom_code": "...", "expires_in_days": 365}
# Response: {"short_code": "abc123", "short_url": "https://tinyurl.com/abc123"}

# GET /{short_code}
# Response: 301 redirect to long URL

# GET /api/{short_code}/analytics
# Response: {"clicks": 1000, "referrers": [...], "browsers": {...}}
```

## Scalability Considerations

### Database Sharding
```python
# Shard by short_code first character
def get_shard(short_code):
    char = short_code[0]
    shard_id = ord(char) % 62  # 0-61
    return f"db_shard_{shard_id}"
```

### Caching Strategy
```python
# Cache short_code -> long_url with TTL
redis.set(f"url:{short_code}", long_url, ex=86400)  # 24 hour TTL

# Cache also recently shortened URLs
redis.setex(f"new_urls:{user_id}", 3600, json.dumps(urls))
```

### Analytics Optimization
```python
# Use separate analytics database
# Write to queue, process in batch
# Real-time analytics via stream processing (Kafka)
```

## Key Interview Questions

1. **How to generate unique short codes?**
   - Counter with base62 encoding (simpler)
   - Or MD5 hash with collision handling

2. **What if URL already exists?**
   - Return existing short code (dedupe)

3. **Handle custom short codes?**
   - Check if taken before assignment

4. **Expire old URLs?**
   - Background job to mark inactive after expiration

5. **Track analytics at scale?**
   - Queue-based async processing, batch writes

## Important Points

- ✅ Use base62 encoding for compact codes
- ✅ Cache all reads (hot shorten traffic)
- ✅ Track analytics asynchronously
- ✅ Handle expiration with background jobs
- ✅ Shard database by short_code for scale
- ✅ Use 301 redirects (permanent) or 302 (temporary)
- ✅ URL validation important for security
