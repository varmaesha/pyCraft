# Rate Limiter System Design

## Requirements

### Functional
- Limit requests per user/IP per time period
- Support multiple time windows (per second, minute, hour)
- Reject requests exceeding limit
- Return remaining quota
- Handle distributed systems

### Non-Functional
- Sub-millisecond latency
- Handle 1M+ requests/second
- Minimal memory overhead
- Support horizontal scaling

## Algorithms

### Algorithm 1: Token Bucket (Most Common)

**Concept**: Tokens refill at constant rate. Each request consumes 1 token.

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens/second
        self.last_refill = time.time()
        self.lock = threading.Lock()
    
    def allow_request(self):
        with self.lock:
            # Refill tokens
            now = time.time()
            elapsed = now - self.last_refill
            tokens_to_add = elapsed * self.refill_rate
            self.tokens = min(self.capacity, 
                            self.tokens + tokens_to_add)
            self.last_refill = now
            
            # Check if can consume
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False

# Usage: 10 requests per second
bucket = TokenBucket(capacity=10, refill_rate=10)

for i in range(15):
    if bucket.allow_request():
        print(f"Request {i}: allowed")
    else:
        print(f"Request {i}: rate limited")
```

### Algorithm 2: Sliding Window

**Concept**: Track timestamps of recent requests in a sliding window.

```python
class SlidingWindowLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []  # List of timestamps
        self.lock = threading.Lock()
    
    def allow_request(self):
        with self.lock:
            now = time.time()
            
            # Remove old requests outside window
            cutoff = now - self.window_seconds
            self.requests = [t for t in self.requests if t > cutoff]
            
            # Check limit
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            return False

# Usage: 100 requests per minute
limiter = SlidingWindowLimiter(max_requests=100, window_seconds=60)

for i in range(150):
    if limiter.allow_request():
        print(f"Request {i}: allowed")
    else:
        print(f"Request {i}: rate limited")
```

### Algorithm 3: Sliding Window with Buckets (Optimized)

```python
class SlidingWindowBucket:
    def __init__(self, max_requests, window_seconds, bucket_count=10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.bucket_count = bucket_count
        self.bucket_size = window_seconds / bucket_count
        self.buckets = [0] * bucket_count
        self.current_bucket = 0
        self.lock = threading.Lock()
    
    def allow_request(self):
        with self.lock:
            now = time.time()
            
            # Determine bucket
            bucket_index = int((now / self.bucket_size) % self.bucket_count)
            
            # Reset if moved to new bucket
            if bucket_index != self.current_bucket:
                self.buckets[bucket_index] = 0
                self.current_bucket = bucket_index
            
            # Check limit
            total_requests = sum(self.buckets)
            
            if total_requests < self.max_requests:
                self.buckets[bucket_index] += 1
                return True
            return False

# O(1) operation, memory efficient
```

### Algorithm 4: Leaky Bucket

```python
class LeakyBucket:
    def __init__(self, capacity, leak_rate):
        self.capacity = capacity
        self.water = 0
        self.leak_rate = leak_rate  # per second
        self.last_leak = time.time()
        self.lock = threading.Lock()
    
    def allow_request(self):
        with self.lock:
            now = time.time()
            
            # Leak water
            elapsed = now - self.last_leak
            self.water = max(0, self.water - elapsed * self.leak_rate)
            self.last_leak = now
            
            # Try to add water
            if self.water + 1 <= self.capacity:
                self.water += 1
                return True
            return False
```

## Distributed Rate Limiter

### Using Redis

```python
import redis

class DistributedRateLimiter:
    def __init__(self, redis_client, max_requests, window_seconds):
        self.redis = redis_client
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def allow_request(self, identifier):
        """Identifier: user_id, IP address, etc."""
        key = f"rate_limit:{identifier}"
        
        now = time.time()
        
        # Lua script for atomic operation
        script = """
        local key = KEYS[1]
        local now = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local max_requests = tonumber(ARGV[3])
        
        local cutoff = now - window
        
        -- Remove old entries
        redis.call('ZREMRANGEBYSCORE', key,'-inf', cutoff)
        
        -- Count current requests
        local count = redis.call('ZCARD', key)
        
        if count < max_requests then
            redis.call('ZADD', key, now, now)
            redis.call('EXPIRE', key, window)
            return 1
        end
        
        return 0
        """
        
        result = self.redis.eval(script, 1, key, now, 
                                 self.window_seconds, self.max_requests)
        
        return result == 1

# Usage
redis_client = redis.Redis()
limiter = DistributedRateLimiter(redis_client, 100, 60)

if limiter.allow_request("user_123"):
    print("Request allowed")
else:
    print("Rate limited")
```

### Multi-Tier Rate Limiter

```python
class MultiTierRateLimiter:
    def __init__(self):
        # Per-second limit
        self.per_second = TokenBucket(capacity=10, refill_rate=10)
        
        # Per-minute limit
        self.per_minute = TokenBucket(capacity=1000, refill_rate=1000/60)
        
        # Per-hour limit
        self.per_hour = TokenBucket(capacity=100000, refill_rate=100000/3600)
    
    def allow_request(self):
        # All limits must pass
        return (self.per_second.allow_request() and
                self.per_minute.allow_request() and
                self.per_hour.allow_request())

limiter = MultiTierRateLimiter()

# Request passes all limits
if limiter.allow_request():
    print("Allowed")
```

## API Response

```python
class RateLimitResponse:
    def __init__(self, allowed, remaining, retry_after=None):
        self.allowed = allowed
        self.remaining = remaining  # Tokens/quota remaining
        self.retry_after = retry_after  # Seconds until can retry
    
    def to_headers(self):
        return {
            "X-RateLimit-Remaining": str(self.remaining),
            "X-RateLimit-ResetAfter": str(self.retry_after) if self.retry_after else "N/A"
        }

# Usage in API
def get_user_data(request):
    user_id = request.user.id
    
    if not limiter.allow_request(user_id):
        response = RateLimitResponse(
            allowed=False,
            remaining=0,
            retry_after=60
        )
        
        return HttpResponse(
            "Rate limit exceeded",
            status_code=429,
            headers=response.to_headers()
        )
    
    # Process request
    return get_data(user_id)
```

## Algorithm Comparison

| Algorithm | Pros | Cons | Best For |
|-----------|------|------|----------|
| **Token Bucket** | Handles bursts | Memory per user | Most use cases |
| **Leaky Bucket** | Smooth traffic | No bursts allowed | Strict rate control |
| **Sliding Window** | Accurate | Memory intensive | Accurate counting |
| **Sliding Window Buckets** | Memory efficient | Less accurate | High scale |

## Real-World Examples

```python
# GitHub API: 60 requests/hour for unauthenticated
# Twitter: 450 requests/15 minutes per user

# DDoS Protection: 100 requests/second per IP

# API Gateway: 10K requests/second per tenant
```

## Design Decisions

| Decision | Reason |
|----------|--------|
| **Token Bucket** | Handles bursts, widely used, easy to understand |
| **Sliding Window Buckets** | Memory efficient for high scale |
| **Redis for Distribution** | Atomic operations, shared state across replicas |
| **Multi-tier limits** | Protect at multiple granularities |

## Key Interview Questions

1. **How to handle burst traffic?**
   - Token Bucket allows accumulation/burst

2. **Distributed rate limiting?**
   - Redis with Lua scripts for atomic operations

3. **Memory efficiency?**
   - Sliding window buckets instead of storing all timestamps

4. **What if user exceeds limit?**
   - Return 429, include retry-after header

5. **Different limits for different users?**
   - Use identifier (user_id, IP, API key) as key

## Important Points

- ✅ Token Bucket for most use cases
- ✅ Consider burst requirements
- ✅ Use Redis for distribution
- ✅ Multi-tier for defense in depth
- ✅ Return clear 429 responses
- ✅ Include retry-after headers
- ✅ Monitor and adjust limits
