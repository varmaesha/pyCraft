# Authentication Explained: When to Use Basic, Bearer, OAuth2, JWT & SSO

**References:**
- [Authentication Explained: When to Use Basic, Bearer, OAuth2, JWT & SSO](https://www.youtube.com/watch?v=9JPnN1Z_iSY)
- [Difference between Authentication and Authorization in Hindi](https://www.youtube.com/watch?v=B76BhEq1FN8)

---

## Core Concepts

### Authentication vs Authorization

**Authentication** ← Who are you?
- Process of verifying user identity
- Confirming user is who they claim to be
- Checking credentials (username, password, token, etc.)
- Answer: "User is verified"

**Authorization** ← What can you do?
- Process of verifying user permissions
- Checking if authenticated user has access to resource
- Based on user roles and permissions
- Answer: "User has access to this resource"

---

## Basic Authentication

### Definition
Username and password sent with every request

### How It Works
```
User Credentials:
  username: "john@example.com"
  password: "securepassword123"

Encoded: base64[username+password]
  base64("john@example.com:securepassword123") = "am9obkBleGFtcGxlLmNvbTpzZWN1cmVwYXNzd29yZDEyMw=="

Request Header:
  Authorization: Basic am9obkBleGFtcGxlLmNvbTpzZWN1cmVwYXNzd29yZDEyMw==
```

![Authentication](assets/image-7.png)

### Characteristics
- Simple to implement
- Credentials sent with each request
- Base64 encoding (NOT encryption)
- Must use HTTPS (credentials visible without HTTPS)

### Advantages
- Simple, straightforward approach
- No additional setup needed

### Disadvantages ✗
- Credentials sent with every request
- If intercepted, attacker gets password
- Base64 is easy to decode
- Not scalable
- Hard to revoke access quickly

### When to Use
- Internal APIs only
- Development/testing
- Simple authentication needs
- Always use with HTTPS

---

## Bearer Tokens

### Definition
Access token sent with each request for authentication

### How It Works
```
1. Client logs in
2. Server generates access token
3. Client includes token in Authorization header:
   Authorization: Bearer eyJhbGc...

4. Server verifies and processes request
5. API verifies token and processes request
```

![Bearer Token](assets/image-3.png)

### Characteristics
- Fast and stateless
- Token generated server-side
- No password sent with each request
- Enables scalability

### Advantages ✓
- Fast and efficient
- Stateless (no server session storage)
- Scalable to large number of users
- Can be revoked

### Disadvantages ✗
- Token storage on client side
- Token could be stolen
- Need token refresh mechanism
- Doesn't provide information about user

### When to Use
- Simple API authentication
- Mobile applications
- When statelessness is desired
- Short-lived tokens

---

## OAuth2 + JWT

### OAuth2 Overview

**Definition:** Authorization framework allowing user to authenticate with external identity provider

### How OAuth2 Works
```
1. User clicks "Login with Google"
2. Redirects to Google login page
3. User authenticates with Google
4. Google redirects back with authorization code
5. Your app exchanges code for access token
6. User authenticated and logged in
```

![OAuth2](assets/image-4.png)

### Benefits
- User authenticates with trusted provider
- Your app doesn't store password
- User can revoke access anytime
- Stateless architecture

### Characteristics
- User authenticated with other authenticators (Google, GitHub, Facebook, etc.)
- Stateless
- No need to store password on your server
- Each request treated independently

---

### JWT (JSON Web Tokens)

**Definition:** Self-contained token containing user information and claims

### JWT Structure
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

Header.Payload.Signature
```

**Header:** Algorithm and token type
**Payload:** User data and claims
**Signature:** Server signature for verification

### JWT Characteristics
- Self-contained (includes user info)
- Signed, not encrypted
- Stateless verification
- Can expire (exp claim)

### Advantages ✓
- Stateless (no server session needed)
- Self-contained (includes user info)
- Scalable
- Works well with microservices
- Can include custom claims

### Disadvantages ✗
- Cannot revoke immediately (until expiry)
- Size larger than session ID
- Signature verification required
- Exposed to XSS attacks if stored in localStorage

---

## Access Token vs Refresh Token

### Access Token
- **Short-lived** token for API requests
- Expires quickly (minutes to hours)
- Contains user permissions and claims
- Stored client-side
- Sent with each API request

### Refresh Token
- **Long-lived** token for getting new access tokens
- Expires slowly (days to months)
- Stored server-side
- Used only to request new access token
- More secure (not sent with every request)

![Access Refresh Tokens](assets/image-5.png)

### Flow
```
Login
    ↓
Server issues: Access Token (5 min) + Refresh Token (7 days)
    ↓
Client stores both locally
    ↓
Make API request with Access Token
    ├─ Token valid → Request succeeds
    └─ Token expired → Use Refresh Token to get new Access Token
        ↓
        Server validates Refresh Token
        ├─ Valid → Issue new Access Token
        └─ Invalid → Login required
```

### Benefits
- Access token expires quickly (security)
- Refresh token allows seamless user experience
- No need to re-login when access token expires
- Refresh tokens can be revoked immediately

---

## SSO + Identity Protocols

### SSO (Single Sign-On)

**Definition:** One login with access to multiple resources/applications

### How SSO Works
```
User logs into Zoom Account
    ↓
Access all linked apps:
  ✓ Gmail
  ✓ Google Drive
  ✓ YouTube
  ✓ Google Photos
    
All with single login
```

![SSO](assets/image-6.png)

### Benefit
- Seamless experience across multiple apps
- User logs in once, accesses everything
- Improves security (centralized authentication)

### Protocols Used

**SAML (Security Assertion Markup Language)**
- Older protocol, XML-based
- Primarily used in enterprise tools
- Complex setup
- Good for corporate environments
- Examples: Okta, Active Directory

**OAuth 2.0**
- Modern protocol, JSON-based
- Used in background by many apps
- Lighter weight than SAML
- Good for modern web/mobile apps
- Examples: Google, GitHub, Facebook

### SAML vs OAuth2

| Aspect | SAML | OAuth 2.0 |
|--------|------|----------|
| **Format** | XML | JSON |
| **Age** | Older | Modern |
| **Use Case** | Enterprise | Web/Mobile |
| **Complexity** | High | Moderate |
| **Setup** | Complex | Simpler |
| **Primary Use** | Authentication | Authorization |

---

## Authentication Methods Comparison

| Method | Security | Scalability | Complexity | Use Case |
|--------|----------|-------------|-----------|----------|
| **Basic Auth** | Low ⚠️ | Poor | Simple | Dev/Testing only |
| **Bearer Token** | Medium | Good | Moderate | Simple APIs |
| **OAuth2** | High | Excellent | Complex | Enterprise/3rd party |
| **JWT** | High | Excellent | Moderate | Modern APIs |
| **SSO** | High | Excellent | Complex | Enterprise multi-app |

---

## Best Practices

1. **Always Use HTTPS**
   - Prevents token/credential interception
   - Non-negotiable for production

2. **Use Short-Lived Access Tokens**
   - 5-15 minutes is typical
   - Limits damage if token is stolen

3. **Store Tokens Securely**
   - Use HttpOnly cookies for web
   - Use secure storage for mobile
   - Never hardcode tokens

4. **Implement Token Refresh**
   - Use refresh tokens for new access tokens
   - Refresh before expiry
   - Revoke on logout

5. **Choose Right Authentication Method**
   - Internal APIs: JWT
   - Public APIs: OAuth2
   - SSO: SAML or OAuth2
   - Simple: Bearer tokens
   - Legacy systems: Basic Auth (HTTPS only)

6. **Monitor and Audit**
   - Log authentication attempts
   - Alert on suspicious activity
   - Track token usage
   - Revoke compromised tokens immediately

7. **Regular Security Updates**
   - Update authentication libraries
   - Patch vulnerabilities quickly
   - Rotate secrets regularly

