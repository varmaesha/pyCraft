# System Design and Architecture Interview Guide

This file is for common system design questions asked in interviews.

---

## 1. What is the difference between monolithic and microservices architecture?
**Answer**:
- A monolith is one large application deployed as a single unit.
- Microservices split the system into smaller services that can scale and deploy independently.

**When to use which**:
- Monolith for simpler products
- Microservices for large, growing systems with many teams

---

## 2. What is load balancing?
**Answer**:
Load balancing distributes traffic across multiple servers so no single server gets overloaded.

---

## 3. What is scalability?
**Answer**:
Scalability is the ability of a system to handle more traffic or more data without breaking down.

---

## 4. What is horizontal scaling?
**Answer**:
Horizontal scaling means adding more machines to share the load.

---

## 5. What is vertical scaling?
**Answer**:
Vertical scaling means increasing the power of a single machine, such as more CPU or RAM.

---

## 6. What is caching?
**Answer**:
Caching stores data temporarily so future requests can be served faster.

---

## 7. What is a database index?
**Answer**:
An index helps the database find rows faster, especially for frequent queries.

---

## 8. What is a message queue?
**Answer**:
A message queue lets different services communicate asynchronously.

**Example**:
- A payment service sends an event to a queue.
- Another service processes it later.

---

## 9. What is eventual consistency?
**Answer**:
Eventual consistency means different parts of a system may temporarily have different data, but they will converge over time.

---

## 10. What is CAP theorem?
**Answer**:
The CAP theorem says distributed systems often need to trade off between consistency, availability, and partition tolerance.

---

## 11. What is rate limiting?
**Answer**:
Rate limiting controls how many requests a user or service can make in a certain time window.

---

## 12. What is API versioning?
**Answer**:
API versioning lets you introduce changes without breaking old clients.

Examples:
- `/api/v1/users`
- `/api/v2/users`

---

## 13. What is a CDN?
**Answer**:
A CDN distributes static content like images and videos across servers closer to users to improve delivery speed.

---

## 14. What are common reliability patterns?
**Answer**:
- Retries
- Timeouts
- Circuit breakers
- Health checks
- Backoff strategies

---

## 15. What is a circuit breaker?
**Answer**:
A circuit breaker prevents a system from repeatedly calling a failing service and helps it recover gracefully.
