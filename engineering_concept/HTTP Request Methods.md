# HTTP Request Methods | GET, POST, PUT, DELETE

**Reference:** [YouTube Video](https://www.youtube.com/watch?v=tkfVQK6UxDI)

---

## What is HTTP?

**HTTP** (HyperText Transfer Protocol) is the de facto communication protocol used by web APIs.

### Key Characteristics
- **Client-Server Model**: Follows client server architecture - client sends requests and waits for response
- **Standardized Protocol**: Used universally for web communication
- **Stateless**: Each request is independent

### Request Methods
**HTTP Methods** are predefined values called **HTTP Verbs** that indicate the action to perform on a resource.

---

## CRUD Operations and HTTP Methods

There's a direct mapping between CRUD operations and HTTP methods:

| Operation | HTTP Method | Purpose | Idempotent | Safe |
|-----------|-------------|---------|-----------|------|
| **CREATE** | POST | Create new resource | ✗ No | ✗ No |
| **READ** | GET | Retrieve resource | ✓ Yes | ✓ Yes |
| **UPDATE** | PUT/PATCH | Modify existing resource | ✓ Yes (PUT) | ✗ No |
| **DELETE** | DELETE | Remove resource | ✓ Yes | ✗ No |

---

## HTTP Methods Details

### GET - READ ✓ Safe & Idempotent

```
GET /api/users/123
```

**Purpose:** Retrieve information/data from server

**Characteristics:**
- Should NOT modify data on server
- Safe operation (no side effects)
- Multiple requests produce same result (idempotent)
- Can be cached
- Parameters in URL (query string)
- No request body

**Example:**
```
GET /users → Get all users
GET /users/123 → Get user with ID 123
GET /users?role=admin → Get all admin users
```

**Response:**
```
200 OK
{
  "id": 123,
  "name": "John Doe",
  "email": "john@example.com"
}
```

---

### POST - CREATE ✓ Creates New Resource

```
POST /api/users
```

**Purpose:** Create new resource on server

**Characteristics:**
- **Will modify data** on server
- Creates new resource each time
- NOT idempotent (multiple calls create multiple resources)
- Response typically includes created resource
- Data in request body
- Usually returns 201 Created status

**Example:**
```
POST /users
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

**Response:**
```
201 Created
{
  "id": 124,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "created_at": "2024-01-18T10:00:00Z"
}
```

**⚠️ Warning - Multiple POSTs:**
```
POST /users (First call)  → Creates user 1
POST /users (Second call) → Creates user 2 ✗ Different result!
POST /users (Third call)  → Creates user 3  ✗ Different result!
```

---

### PUT - UPDATE ✓ Replace Entire Resource

```
PUT /api/users/123
```

**Purpose:** Modify/update existing resource (full replacement)

**Characteristics:**
- **Will modify data** on server
- Updates entire resource
- Idempotent (multiple calls produce same result)
- Requires full resource object
- Data in request body
- Can create if not exists (depends on API design)

**Example:**
```
PUT /users/123
{
  "name": "John Doe Updated",
  "email": "john.updated@example.com",
  "phone": "555-1234"
}
```

**Response:**
```
200 OK
{
  "id": 123,
  "name": "John Doe Updated",
  "email": "john.updated@example.com",
  "phone": "555-1234"
}
```

**Idempotent Behavior:**
```
PUT /users/123 with same data (First call)  → User updated
PUT /users/123 with same data (Second call) → Same state ✓ (idempotent)
PUT /users/123 with same data (Third call)  → Same state ✓ (idempotent)
```

---

### PATCH - UPDATE ✓ Partial Update

```
PATCH /api/users/123
```

**Purpose:** Partially modify/update resource (update only specified fields)

**Characteristics:**
- **Will modify data** on server
- Updates only specified fields
- Other fields remain unchanged
- Less bandwidth than PUT
- Idempotency depends on usage
- Data in request body

**Example:**
```
PATCH /users/123
{
  "email": "newemail@example.com"
}
```

**Response:**
```
200 OK
{
  "id": 123,
  "name": "John Doe",        ← Unchanged
  "email": "newemail@example.com",  ← Updated
  "phone": "555-1234"        ← Unchanged
}
```

---

### DELETE - DELETE ✓ Remove Resource

```
DELETE /api/users/123
```

**Purpose:** Remove/delete resource from server

**Characteristics:**
- **Will modify data** on server
- Removes resource permanently
- Idempotent (deleting deleted resource is same as deleting existing)
- Usually returns 204 No Content
- No request body

**Example:**
```
DELETE /users/123
```

**Response:**
```
204 No Content
(No body returned)
```

**Idempotent Behavior:**
```
DELETE /users/123 (First call)  → User deleted
DELETE /users/123 (Second call) → Already deleted, same end state ✓ (idempotent)
DELETE /users/123 (Third call)  → Already deleted, same end state ✓ (idempotent)
```

---

## Method Comparison

### Safe vs Unsafe
**Safe Methods** don't modify server state:
- GET ✓ Safe
- POST, PUT, PATCH, DELETE ✗ Unsafe

### Idempotent vs Non-Idempotent
**Idempotent Methods** produce same result with multiple calls:
- GET ✓ Idempotent
- PUT ✓ Idempotent
- DELETE ✓ Idempotent
- POST ✗ Non-idempotent
- PATCH ✓ Usually idempotent

---

## Real-World Examples

### Create User
```
POST /api/users
Content-Type: application/json

{
  "name": "Alice",
  "email": "alice@example.com"
}

Response: 201 Created
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### Get User
```
GET /api/users/1

Response: 200 OK
{
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

### Update User
```
PUT /api/users/1
Content-Type: application/json

{
  "name": "Alice Johnson",
  "email": "alice.j@example.com"
}

Response: 200 OK
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice.j@example.com"
}
```

### Delete User
```
DELETE /api/users/1

Response: 204 No Content
```

---

## Best Practices

1. **Use Correct Method for Action**
   - GET for retrieval only
   - POST for creation
   - PUT for full updates
   - PATCH for partial updates
   - DELETE for removal

2. **Return Appropriate Status Codes**
   - 201 Created for POST
   - 200 OK for successful updates
   - 204 No Content for deletion
   - 400 Bad Request for invalid input

3. **Make POST Idempotent When Needed**
   - Use idempotency keys for critical operations
   - Essential for payment/financial transactions

4. **Use Consistent Naming**
   - Singular or plural consistently
   - RESTful resource naming
   - Clear, descriptive paths

5. **Document Your API**
   - Show examples for each method
   - Specify parameters and request body
   - List possible response codes

