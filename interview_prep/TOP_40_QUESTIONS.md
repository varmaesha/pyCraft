# Top 40 Interview Questions & Answers

## OOP & Design

### 1. What is the difference between classes and objects?
**Answer:** A class is a blueprint or template for creating objects. An object is an instance of a class with actual values. Multiple objects can be created from one class.

### 2. Explain the four pillars of OOP
**Answer:** 
- **Encapsulation**: Bundling data and methods, hiding internal details
- **Abstraction**: Showing only essential features, hiding complexity
- **Inheritance**: Deriving new classes from existing ones (IS-A)
- **Polymorphism**: Same interface, different implementations

### 3. What's the difference between composition and inheritance?
**Answer:** 
- **Inheritance (IS-A)**: Class extends another class, tightly coupled
- **Composition (HAS-A)**: Class contains instances of other classes, loosely coupled
- **Rule**: Prefer composition over inheritance for flexibility

### 4. What are SOLID principles?
**Answer:** 
- **S**: Single Responsibility - one reason to change
- **O**: Open/Closed - open for extension, closed for modification
- **L**: Liskov Substitution - subtypes interchangeable
- **I**: Interface Segregation - specific interfaces
- **D**: Dependency Inversion - depend on abstractions

### 5. What's a design pattern?
**Answer:** Reusable solution to common design problem. Provides template for writing better, maintainable code.

---

## Design Patterns

### 6. When would you use Singleton pattern?
**Answer:** When you need exactly one instance of a class:
- Database connections
- Logger
- Configuration manager
- Thread pools
- **Caution**: Makes testing difficult, hides dependencies

### 7. Difference between Factory and Builder patterns?
**Answer:** 
- **Factory**: One-step object creation, good for simple objects
- **Builder**: Step-by-step construction, good for complex objects with many options

### 8. When to use Strategy pattern?
**Answer:** When you have multiple algorithms for same task and want to:
- Select algorithm at runtime
- Switch algorithms easily
- Avoid if-else chains
**Example**: Payment methods (Credit Card, PayPal, Crypto)

### 9. What is Observer pattern?
**Answer:** One-to-many relationship where observers watch a subject. When subject changes, all observers are notified automatically.
**Example**: Stock price updates, button click handlers

### 10. How does Decorator pattern differ from Inheritance?
**Answer:** 
- **Inheritance**: Fixed at compile-time, creates class hierarchy
- **Decorator**: Runtime composition, adds behavior dynamically without modifying class

---

## Concurrency

### 11. What's a race condition?
**Answer:** When multiple threads access shared resource without synchronization, leading to unpredictable results because of non-deterministic execution order.

### 12. How do you prevent race conditions?
**Answer:** 
- Use **Locks/Mutex**: Ensure only one thread at a time
- **Atomic operations**: Indivisible operations
- **Immutable objects**: Cannot be modified
- **Thread pools**: Controlled threading

### 13. What causes deadlock?
**Answer:** Circular wait for resources:
- Thread A waits for lock held by Thread B
- Thread B waits for lock held by Thread A
- **Prevention**: Always acquire locks in same order

### 14. What's the difference between Lock and RLock?
**Answer:** 
- **Lock**: Single acquisition per thread
- **RLock** (Reentrant): Same thread can acquire multiple times

### 15. When should you use synchronized methods?
**Answer:** When multiple threads access shared mutable state. Keep synchronized blocks small for performance.

---

## System Design

### 16. What do you consider when designing a system?
**Answer:** 
1. **Requirements**: Functional and non-functional
2. **Components**: Identify major pieces
3. **Trade-offs**: Consistency vs Availability, latency vs throughput
4. **Scalability**: Handle growth
5. **Reliability**: Handle failures
6. **Maintainability**: Easy to change

### 17. How would you design an ATM?
**Answer:** 
1. **Components**: Card reader, PIN verification, account manager, cash manager
2. **State Machine**: IDLE → CARD_INSERTED → AUTHENTICATED → TRANSACTION
3. **Security**: PIN encryption, failed attempt limits
4. **Transactions**: Withdraw, deposit, balance check
5. **Patterns**: Singleton, Factory, State

### 18. How would you design a Parking Lot?
**Answer:** 
1. **Entities**: ParkingLot, Level, Spot, Vehicle, Ticket
2. **Spot Types**: Motorcycle, Compact, Regular, Large
3. **Features**: Availability tracking, fee calculation, spot search algorithm
4. **State**: Available, Occupied, Reserved
5. **Patterns**: Singleton, Factory, Strategy

### 19. How would you design a Library Management System?
**Answer:** 
1. **Entities**: Book, BookCopy, Member, Borrowing, reservation
2. **Features**: Search, borrow, return, track due dates, fine calculation
3. **Patterns**: Repository, Observer (notify of due dates), Strategy (fine calculation)

### 20. What are the pillars of a good system design?
**Answer**: **RASCAL**
- **Reliability**: Fault tolerance
- **Availability**: Uptime
- **Scalability**: Handle growth
- **Consistency**: Data correctness
- **Availability**: Access anytime
- **Latency**: Low response time

---

## Advanced Concepts

### 21. What's the difference between abstraction and encapsulation?
**Answer:** 
- **Abstraction**: WHAT - showing only essential features
- **Encapsulation**: HOW - hiding internal details and providing controlled access

### 22. Explain Liskov Substitution Principle
**Answer:** Derived classes should be substitutable for base classes without breaking functionality. If Penguin extends Bird but can't fly, it violates LSP.

### 23. What's idempotency and why is it important?
**Answer:** Operation producing same result regardless of how many times it's called. Important in:
- Payment systems (charge user only once)
- Distributed systems (retry-able operations)
- APIs (safe retries without side effects)

### 24. How do you handle concurrent updates to same resource?
**Answer:** Options:
- **Pessimistic Locking**: Lock before updating
- **Optimistic Locking**: Detect conflicts, retry if needed
- **MVCC**: Multiple versions, timestamp-based

### 25. What's shallow copy vs deep copy?
**Answer:** 
- **Shallow**: Copies object references, nested objects shared
- **Deep**: Copies recursively, complete independence
- **Use Deep Copy**: When you need complete independence (undo/redo, snapshots)

---

## Code & Implementation

### 26. How would you implement thread-safe Singleton?
**Answer:** Using double-checked locking:
```python
class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

### 27. How would you enforce immutability in Python?
**Answer:** 
- Use `@dataclass(frozen=True)`
- Override `__setattr__` to prevent modifications
- Use Tuple instead of List
- Use `namedtuple`

### 28. How to handle exceptions in distributed systems?
**Answer:** 
- **Timeout**: Fail fast
- **Retry**: Exponential backoff
- **Circuit Breaker**: Fail gracefully
- **Fallback**: Use cached/default value
- **Bulkhead**: Isolate failures

### 29. What's the most important design consideration?
**Answer:** **Separation of Concerns** - each component should have single responsibility, making code modular, testable, and maintainable.

### 30. How do you make code more testable?
**Answer:** 
- Dependency Injection
- Single Responsibility
- Loose Coupling
- Avoid Singletons
- Mock/Stub external dependencies

---

## Real-World Scenarios

### 31. Design an e-commerce checkout system
**Answer:** 
1. **Cart**: Items, quantities, prices
2. **Validation**: Check inventory, validate user
3. **Payment**: Strategy pattern for multiple methods
4. **Order**: Create order record
5. **Notification**: Observer pattern for order updates
6. **Consistency**: Database transactions, idempotency

### 32. How would you design a cache system?
**Answer:** 
- **Eviction Policy**: LRU, LFU, FIFO
- **Size Limit**: Max entries, max memory
- **Concurrency**: Thread-safe access
- **Invalidation**: TTL, manual invalidation
- **Patterns**: Singleton for cache instance

### 33. Design a notification system handling millions of users
**Answer:** 
- **Async Processing**: Queue notifications
- **Batching**: Group notifications
- **Channels**: Email, SMS, Push
- **Retry Logic**: Handle failures
- **Observer Pattern**: Decouple senders from notification handlers

### 34. How to handle rate limiting?
**Answer:** 
- **Token Bucket**: Allow burst traffic
- **Leaky Bucket**: Smooth traffic
- **Sliding Window**: Track recent requests
- **Distributed**: Use Redis for multi-server setup

### 35. Design a recommendation system
**Answer:** 
- **Data Collection**: User behavior tracking
- **Algorithms**: Collaborative filtering, content-based
- **Strategy Pattern**: Switch between algorithms
- **Performance**: Cache popular recommendations
- **A/B Testing**: Compare algorithm effectiveness

---

## Mistakes to Avoid

### 36. What's over-engineering?
**Answer:** Using complex solutions for simple problems. Use patterns only when needed, not for everything.

### 37. What's premature optimization?
**Answer:** Optimizing code before profiling. Focus on correctness first, optimize bottlenecks later.

### 38. What's wrong with tight coupling?
**Answer:** 
- Hard to test (can't mock)
- Hard to extend (must modify existing code)
- Ripple effects (change cascades)
- **Solution**: Depend on abstractions, use DI

### 39. Why avoid long inheritance chains?
**Answer:** 
- Fragile base class problem
- Hard to understand
- Difficult to modify
- **Solution**: Prefer composition

### 40. When is a design pattern unnecessary?
**Answer:** When the problem is too simple. Adding pattern introduces complexity without benefit. **Key**: Simplicity first, patterns when needed.

---

## Interview Tips

1. **Listen carefully** to requirements before jumping to solution
2. **Ask clarifications** about non-functional requirements
3. **Think out loud** so interviewer can follow your reasoning
4. **Draw diagrams** to visualize components and relationships
5. **Discuss trade-offs** - nothing is perfect
6. **Be ready to pivot** if interviewer suggests different approach
7. **Code quality matters** - clean, readable, maintainable code
8. **Test your code** - explain edge cases and error handling
