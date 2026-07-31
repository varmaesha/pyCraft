# Interview Cheat Sheet - Quick Reference

## OOP Quick Reference

| Concept | Definition | When to Use |
|---------|-----------|------------|
| **Encapsulation** | Hide data, control access | Always - protects internal state |
| **Abstraction** | Show interface, hide complexity | Define contracts, reduce coupling |
| **Inheritance** | IS-A relationship, code reuse | True hierarchies (Employee < Person) |
| **Polymorphism** | Same method, different behavior | Enable flexibility and extensibility |
| **Composition** | HAS-A relationship, ownership | Default choice - most flexible |
| **Aggregation** | HAS-A relationship, no ownership | Shared resources |

## SOLID Quick Recap

```
S - Single Responsibility: One reason to change
O - Open/Closed: Open for extension, closed for modification
L - Liskov Substitution: Subtypes interchangeable
I - Interface Segregation: Specific interfaces, not fat ones
D - Dependency Inversion: Depend on abstractions, not concretions
```

**Golden Rule**: "Depend on interfaces, not implementations"

## Design Patterns Quick Reference

| Pattern | Purpose | Example | When NOT to Use |
|---------|---------|---------|-----------------|
| **Singleton** | Single instance, global access | Logger, Database | Makes testing hard, hides deps |
| **Factory** | Create objects without specifying classes | Payment processors | Overkill for simple creation |
| **Builder** | Construct complex objects step-by-step | Configuration, Query builder | Not for simple objects |
| **Strategy** | Algorithm families, runtime selection | Payment methods, sorting | Only one algorithm |
| **Observer** | One-to-many notifications | Event listeners, MVC | Tight coupling concerns |
| **Decorator** | Add behavior dynamically | Beverage with toppings | When you need inheritance |
| **Adapter** | Make incompatible interfaces work | Convert XML to JSON | Over-coupling different systems |
| **Proxy** | Controlled access to real object | Cache proxy, security proxy | Add unnecessary indirection |

## Concurrency Toolkit

| Issue | Solution |
|-------|----------|
| **Race Condition** | Use Lock/Mutex for shared resources |
| **Deadlock** | Always acquire locks in same order |
| **Thread Efficiency** | Use ThreadPool, avoid creating many threads |
| **Data Consistency** | Atomic operations or Immutable objects |
| **Producer-Consumer** | Use Queue or Condition variables |
| **Distributed System** | Use Idempotency, Retry with backoff |

## System Design Checklist

### Requirements Phase
- [ ] Clarify functional requirements
- [ ] Ask about non-functional requirements (scale, latency, availability)
- [ ] Define constraints and scope

### Architecture Phase
- [ ] Identify key components
- [ ] Define data models
- [ ] Choose appropriate patterns
- [ ] Consider CAP theorem

### Implementation Considerations
- [ ] Scalability: horizontal/vertical scaling
- [ ] Reliability: fault tolerance, replication
- [ ] Consistency: eventual vs strong
- [ ] Performance: caching, indexing, async

## Common Anti-patterns (Avoid These)

❌ **God Object**: Does too many things
❌ **Deep Inheritance**: More than 3 levels
❌ **Tight Coupling**: Hard-coded dependencies
❌ **Over-engineering**: Complex solution for simple problem
❌ **Missing Error Handling**: Unhandled exceptions
❌ **No Synchronization**: Concurrent access without locks
❌ **Resource Leaks**: Not releasing resources
❌ **Magic Numbers**: Unexplained constants

## Quick Problem-Solving Approach

```
1. UNDERSTAND
   - Read problem carefully
   - Ask clarifying questions
   - Identify constraints

2. ANALYZE
   - List requirements (functional + non-functional)
   - Identify key components
   - Think about trade-offs

3. DESIGN
   - Sketch high-level architecture
   - Identify patterns to use
   - Define interfaces

4. IMPLEMENT
   - Write clean, readable code
   - Apply design patterns
   - Handle edge cases

5. OPTIMIZE
   - Identify bottlenecks
   - Add caching if needed
   - Consider scaling
```

## Design Pattern Selection Tree

```
Need object creation?
├─ Simple creation → Factory
├─ Complex with many options → Builder
└─ Ensure single instance → Singleton

Need to vary algorithm?
├─ Runtime selection → Strategy
└─ Different data representations → State

Need to extend behavior?
├─ Add dynamically → Decorator
├─ Adapt interface → Adapter
└─ Control access → Proxy

Need communication?
├─ One-to-many notifications → Observer
└─ Request handling chain → Chain of Responsibility
```

## Interview Language

✅ **Use These Phrases:**
- "Let me clarify..."
- "This trade-off..."
- "This pattern would help because..."
- "Another approach would be..."
- "In this scenario..."

❌ **Avoid:**
- "I know this already" (be humble)
- "That's wrong" (discuss alternatives)
- "It's obvious" (explain anyway)
- Absolute statements without nuance

## Real-World Examples (One-Liners)

- **Encapsulation**: Bank account - can't directly change balance
- **Polymorphism**: Different payment methods with same checkout flow
- **Strategy Pattern**: Netflix choosing video codec based on device
- **Observer Pattern**: Email notification when order ships
- **Singleton**: Application logger used everywhere
- **Factory**: Creating different database connections
- **Builder**: Constructing complex SQL queries
- **Decorator**: Adding toppings to coffee without changing class
- **Thread Safety**: Multiple users withdrawing from same account
- **Idempotency**: Payment API - safe to retry without double-charging

## Estimation Quick Reference

| Scale | Transactions/sec | Latency |
|-------|-----------------|---------|
| Small | <1,000 | <100ms |
| Medium | 1K-10K | 100-500ms |
| Large | 10K-100K | <500ms critical |
| Huge | 100K+ | <50ms critical |

## Distributed System Patterns

| Pattern | Use Case | Trade-off |
|---------|----------|-----------|
| **Replication** | High availability | Consistency overhead |
| **Sharding** | Scalability | Complexity, joins harder |
| **Caching** | Performance | Stale data |
| **Event-driven** | Decoupling | Eventual consistency |
| **Circuit Breaker** | Fault tolerance | More components |

## Before Interview: Do This

- [ ] Review SOLID principles
- [ ] Practice 1-2 system designs
- [ ] Prepare real-world examples
- [ ] Know when to apply patterns (not every pattern to every problem)
- [ ] Practice explaining clearly
- [ ] Understand trade-offs
- [ ] Have questions ready for interviewer
- [ ] Code sample solutions (don't just talk)

## During Interview: Remember This

1. **Slow down** - Take time to think
2. **Communicate** - Think out loud
3. **Clarify** - Ask questions about ambiguous requirements
4. **Draw** - Use whiteboard effectively
5. **Trade-offs** - Discuss pros and cons
6. **Examples** - Use real-world scenarios
7. **Code carefully** - Quality over speed
8. **Test** - Mention edge cases and error handling

## System Design Problems Quick Summary

### Low-Level Design (LLD) - Object-Oriented

| Problem | Key Patterns | Key Concepts | Complexity |
|---------|--------------|--------------|-----------|
| **ATM Machine** | Singleton, Factory, State | Transaction states, authentication | Medium |
| **Parking Lot** | Singleton, Strategy | Space allocation, pricing | Medium |
| **Library** | Observer, Repository | Tracking, notifications | Medium |
| **Chess/Tic Tac Toe** | State, Factory | Win detection, game flow | Medium-Hard |
| **Elevator** | State, Observer, Factory | Scheduling, movement logic | Hard |
| **Movie Booking** | Factory, Observer | Availability, concurrency locks | Hard |
| **Hotel Booking** | Strategy, Repository | Date ranges, pricing | Medium-Hard |
| **Food Delivery** | Observer, Factory | Order tracking, status updates | Hard |
| **Notification System** | Factory, Observer, Strategy | Multi-channel delivery, templates | Medium-Hard |
| **Ride Sharing** | Observer, Factory, Observer | Matching, routing, payments | Very Hard |

### High-Level Design (HLD) - Distributed Systems

| Problem | Key Concepts | Algorithm/Tech | Interview Appeal |
|---------|--------------|-----------------|-----------------|
| **LRU Cache** | HashMap + LinkedList, O(1) ops | Eviction policy | High - fundamental |
| **Rate Limiter** | Token Bucket, Sliding Window | Distributed coordination | High - practical |
| **URL Shortener** | Base62 encoding, consistency hashing | DB sharding, analytics | High - real product |
| **Real-Time Chat** | WebSocket, message queue | Georeplication, delivery guarantees | Very High - complex |
| **Distributed KV Store** | Consistent hashing, CAP theorem | Replication, persistence | Very High - advanced |
| **Thread-Safe HashMap** | Segment locking, copy-on-write | Concurrent access patterns | High - concurrency |

## System Design Keywords

### Data Structures
- **HashMap/Hashtable**: Fast lookup O(1)
- **DoublyLinkedList**: Ordered, O(1) insertion/removal
- **PriorityQueue**: Ordered by priority
- **Graph**: Relationships, routing
- **Trie**: Prefix matching, autocomplete

### Techniques
- **Consistent Hashing**: Distributed partitioning
- **Sharding**: Horizontal scalability
- **Replication**: High availability
- **Caching**: Performance
- **Load Balancing**: Traffic distribution
- **Message Queue**: Async processing
- **Database Migration**: Zero-downtime updates

### Algorithms
- **Minimax**: Game AI decisions
- **Token Bucket**: Rate limiting
- **Chord/DHT**: Distributed lookup
- **Raft/Paxos**: Consensus
- **MapReduce**: Large-scale processing

### Infrastructure
- **CAP Theorem**: Consistency, Availability, Partition tolerance
- **ACID**: Database properties
- **BASE**: Alternative to ACID
- **DNS**: Domain resolution
- **CDN**: Content delivery
- **Load Balancer**: Traffic routing
- **Database**: SQL vs NoSQL choice

## Most Important Insights

1. **Context matters** - No one-size-fits-all solution
2. **Simplicity first** - Don't overcomplicate
3. **Separation of concerns** - Each component does one thing
4. **Extensibility over perfection** - Easy to add features
5. **Testability is critical** - Write testable code
6. **Real-world thinking** - Consider deployment, operations
7. **Communication > Perfection** - Explain your thinking
8. **Humble and curious** - Learn from feedback

---

**Remember**: The goal is not perfect solution, but demonstrating strong fundamentals, clear thinking, and good communication.
