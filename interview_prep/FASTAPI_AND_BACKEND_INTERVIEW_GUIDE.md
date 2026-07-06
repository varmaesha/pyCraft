# FastAPI and Backend Interview Guide

This guide is for backend and API-related questions that often appear in interviews.

---

## 1. What is FastAPI?
**Answer**:
FastAPI is a Python web framework for building APIs quickly. It is known for speed, async support, and automatic validation using Pydantic.

---

## 2. What is `Depends` in FastAPI?
**Answer**:
`Depends` is used to inject reusable logic into routes, such as authentication, database sessions, or shared services.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

def get_db():
    db = "connection"
    try:
        yield db
    finally:
        print("closed")

@app.get("/users")
def read_users(db=Depends(get_db)):
    return {"db": db}
```

---

## 3. What is Pydantic?
**Answer**:
Pydantic is used for data validation and serialization in FastAPI. It ensures incoming data matches the expected structure.

---

## 4. What is the difference between synchronous and asynchronous endpoints?
**Answer**:
- Synchronous endpoints block the request until they finish.
- Asynchronous endpoints use `async` and are better for I/O-bound tasks.

---

## 5. What is an HTTP status code?
**Answer**:
It tells the client whether the request succeeded, failed, or needs something else.

Examples:
- `200` OK
- `201` Created
- `400` Bad Request
- `401` Unauthorized
- `404` Not Found
- `500` Internal Server Error

---

## 6. What is idempotency?
**Answer**:
An operation is idempotent if repeating it gives the same result and does not cause extra side effects.

Examples:
- `GET` is idempotent
- `PUT` is usually idempotent
- `POST` is usually not

---

## 7. What is authentication vs authorization?
**Answer**:
- Authentication checks who you are.
- Authorization checks what you are allowed to do.

---

## 8. What is middleware?
**Answer**:
Middleware runs before or after requests are handled. It is useful for logging, authentication, or request timing.

---

## 9. What is a webhook?
**Answer**:
A webhook is an HTTP callback triggered by an event in another system.

---

## 10. What is rate limiting?
**Answer**:
Rate limiting restricts how many requests a client can make in a given time period.

---

## 11. What is caching?
**Answer**:
Caching stores frequently used data in memory so later requests can be faster.

---

## 12. What is a REST API?
**Answer**:
A REST API uses standard HTTP methods like `GET`, `POST`, `PUT`, `PATCH`, and `DELETE` to interact with resources.

---

## 13. Why use async in backend development?
**Answer**:
It helps the server handle many requests efficiently when work involves waiting on I/O, such as databases or network calls.

---

## 14. What is the difference between `PUT` and `PATCH`?
**Answer**:
- `PUT` replaces the whole resource.
- `PATCH` updates part of it.

---

## 15. What are common API design best practices?
**Answer**:
- Use clear resource names
- Use proper status codes
- Keep endpoints consistent
- Validate input
- Handle errors clearly
- Use pagination for large results
