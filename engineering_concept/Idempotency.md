# Idempotency: What it is and How to Implement it

**Reference:** [YouTube Video](https://www.youtube.com/watch?v=XAccGbtl3Z8)

---

## Definition

**Idempotency** means the **intended effect on the server is the same no matter how many times a request is made**.

Making the same request 1 time or 100 times produces identical results.

---

## HTTP Methods and Idempotency

### Idempotent Methods ✓

**GET**
- Retrieves data without modification
- Safe to call multiple times
- Returns same data each time
- No side effects

**PUT**
- Updates entire resource
- Same data sent = same final state
- Multiple requests result in same state
- Idempotent operation

**DELETE**
- Removes resource
- First call: Resource deleted
- Second call: Resource already gone (same end state)
- Technically idempotent (deleted or already deleted)

### Non-Idempotent Methods ✗

**POST**
- Creates new resource
- **Problem: Multiple requests = Multiple resources created**

Example: Creating a user
```
POST /users
{
  "name": "John",
  "email": "john@example.com"
}

Request 1: User created with ID 1
Request 2: User created with ID 2  ← Different result!
Request 3: User created with ID 3  ← Different result!
```

**Payment Example (Critical):**
```
POST /payments
{
  "amount": 100,
  "currency": "USD",
  "card_number": "1234-5678-9012-3456",
  "cvv": "123",
  "expiry_date": "12/25"
}

Request 1: Charge $100 ✓
Request 2: Charge $100 ✓ ← Customer charged again!
Request 3: Charge $100 ✓ ← Customer charged AGAIN!

Result: Customer charged 3 times for 1 purchase
Problem: Nothing to identify requests as the same
```

**PATCH**
- Partially updates resource
- Idempotency depends on implementation
- Can be idempotent or non-idempotent

Example:
```
PATCH /users/123
{ "email": "newemail@example.com" }
Request 1: Email updated
Request 2: Email updated to same value ✓ (Idempotent)

vs.

PATCH /users/123
{ "increment_balance": 50 }
Request 1: Balance increases by 50
Request 2: Balance increases by 50 again ✗ (NOT idempotent)
```

---

## Making POST Idempotent

POST is inherently non-idempotent, but we can make it safe by adding unique request identifiers.

### Solution: Unique Request Identifier

**Idempotency Key**
```
POST /payments
{
  "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
  "amount": 100,
  "currency": "USD",
  "card_number": "1234-5678-9012-3456"
}
```

### Implementation Strategy

1. **Client sends unique key with request**
   - UUID (Universally Unique Identifier)
   - Format: `123e4567-e89b-12d3-a456-426614174000`

2. **Server stores key and response**
   - Create mapping: `idempotency_key → response`
   - Use hash of request body combined with key for more security

3. **Duplicate request handling**
   - Check if key exists in database
   - If key exists: Retrieve and return previous response
   - If key doesn't exist: Process request, store response with key

4. **Expiration**
   - Expire keys after certain time to save storage
   - Typical TTL: 24 or 48 hours
   - After expiration: Treat as new request

### Benefits
- Prevents duplicate processing
- Handles network failures gracefully
- Supports client retries without side effects
- Essential for financial transactions

---

## Implementation Details

### Storage Strategy

**In-Memory Store (Fast)**
- Use Redis or similar for temporary storage
- Fast access and lookups
- TTL support for automatic expiration
- Good for high-traffic scenarios

**Persistent Store**
- Use database for permanent record
- Can retrieve responses after server restart
- Better for critical operations

### Key Expiration

```
Idempotency Key: "abc123"
Stored at: 2024-01-18 10:00:00
TTL: 24 hours
Expires at: 2024-01-19 10:00:00

After expiration:
- Key removed automatically
- Same request treated as new transaction
```

### Data Structure Example

```json
{
  "idempotency_key": "123e4567-e89b-12d3-a456-426614174000",
  "user_id": "user_456",
  "request_body": "hash_of_request",
  "response": {
    "status": 201,
    "data": { "transaction_id": "txn_789" }
  },
  "created_at": "2024-01-18T10:00:00Z",
  "expires_at": "2024-01-20T10:00:00Z"
}
```

---

## Real-World Scenarios

### Payment Processing
```
Customer clicks "Pay Now" button
Network lag causes timeout
User clicks again → Same idempotency key
Server detects duplicate → Returns previous result
Outcome: Only charged once ✓
```

### Order Creation
```
POST /orders
idempotency_key: "order_789"

Attempt 1: Order created, confirmation sent
Network fails before response reaches client
Client retries with same key
Attempt 2: Key found, previous response returned
Result: Order created once, no duplicate ✓
```

### Account Transfer
```
POST /transfers
idempotency_key: "transfer_123"

Attempt 1: $500 transferred
Attempt 2: Same key → Return previous result
Attempt 3: Same key → Return previous result
Result: Money transferred once ✓
```

---

## Best Practices

1. **Always Use for Modifying Operations**
   - Required for POST, PUT, PATCH operations
   - Critical for financial transactions
   - Important for any state-changing operations

2. **Generate Unique Keys**
   - Use UUIDs (UUID v4 recommended)
   - Make client responsible for generation
   - Allow server to validate uniqueness

3. **Clear TTL Policy**
   - Document key expiration time
   - Provide guidance (24-48 hours typical)
   - Balance storage vs safety

4. **Communicate to Clients**
   - Document idempotency requirements
   - Provide examples
   - Show response headers for key validation

5. **Monitor and Log**
   - Track idempotency key usage
   - Monitor duplicate request patterns
   - Alert on suspicious activity

---

## Idempotency Key Headers

### Standard Format
```
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000
```

### Response Headers
```
Idempotency-Key: 123e4567-e89b-12d3-a456-426614174000
Idempotency-Key-Status: used  (or "created")
```

---

## Summary

| Aspect | Non-Idempotent | Idempotent |
|--------|----------------|-----------|
| **Multiple Requests** | Different outcomes | Same outcome |
| **Side Effects** | Multiple charges/duplicates | Single effect |
| **Risk Level** | High | Low |
| **HTTP Methods** | POST, PATCH | GET, PUT, DELETE |
| **Protection** | Idempotency key | Built-in |
| **Use Case** | Financial ops | Data retrieval |


