# Interview Preparation Guide - Index

## Overview

This comprehensive interview preparation guide covers system design, OOP, design patterns, concurrency, and more with detailed explanations and real-world examples.

---

## 📚 OOP Fundamentals

### Core Concepts
1. **[OOP Basics](01_oop_basics.md)** - Classes, objects, and fundamentals
2. **[Encapsulation](02_encapsulation.md)** - Data hiding and access control
3. **[Abstraction](03_abstraction.md)** - Hiding complexity, showing interfaces
4. **[Inheritance](04_inheritance.md)** - Code reuse through IS-A relationships
5. **[Polymorphism](05_polymorphism.md)** - Same interface, different behaviors

### Advanced Concepts
6. **[Composition vs Inheritance](06_composition_vs_inheritance.md)** - When to use what
7. **[Association, Aggregation, Composition](07_association_aggregation_composition.md)** - Object relationships
8. **[Interface vs Abstract Class](08_interface_vs_abstract_class.md)** - Contracts vs shared code
9. **[Immutable Objects](09_immutable_objects.md)** - Thread-safe unchangeable objects
10. **[Deep Copy vs Shallow Copy](10_deepcopy_vs_shallowcopy.md)** - Object cloning strategies

---

## 🎨 Design Principles

11. **[SOLID Principles](design_principles/11_solid_principles.md)**
    - Single Responsibility
    - Open/Closed
    - Liskov Substitution
    - Interface Segregation
    - Dependency Inversion

12. **[Loose Coupling vs Tight Coupling](design_principles/12_loose_coupling_tight_coupling.md)**
13. **[Separation of Concerns](design_principles/13_separation_of_concerns.md)**
14. **[UML and Sequence Diagrams](design_principles/14_uml_sequence_diagrams.md)**
15. **[Designing for Extensibility](design_principles/15_designing_for_extensibility.md)**
16. **[Designing for Testability](design_principles/16_designing_for_testability.md)**

---

## 🏗️ Design Patterns

### Creational Patterns
17. **[Singleton](design_patterns/17_singleton.md)** - Single instance pattern
18. **[Factory](design_patterns/18_factory.md)** - Object creation abstractions
19. **[Builder](design_patterns/19_builder.md)** - Complex object construction

### Behavioral Patterns
20. **[Strategy](design_patterns/20_strategy.md)** - Algorithm families
21. **[Observer](design_patterns/21_observer.md)** - One-to-many notifications
22. **[Decorator](design_patterns/22_decorator.md)** - Adding behavior dynamically
23. **[Adapter](design_patterns/23_adapter.md)** - Interface compatibility
24. **[Proxy](design_patterns/24_proxy.md)** - Controlled access

---

## 🔗 Concurrency & Threading

25. **[Thread Safety](concurrency/25_thread_safety.md)** - Synchronization and locks
26. **[Race Conditions](concurrency/26_race_conditions.md)** - Issues with concurrent access
27. **[Synchronization](concurrency/27_synchronization.md)** - Locks, semaphores, monitors
28. **[Optimistic vs Pessimistic Locking](concurrency/28_optimistic_pessimistic_locking.md)**
29. **[Idempotency](concurrency/29_idempotency.md)** - Safe repeated operations
30. **[Multi-User/Concurrent Scenarios](concurrency/30_multi_user_concurrent_scenarios.md)**

---

## 🏢 System Design Problems

### Low-Level Design (LLD) - Object-Oriented Problems
1. **[ATM Machine](system_design_problems/01_atm_machine.md)**
   - Authentication, transactions, state management
   - Design Patterns: Singleton, Factory, State
   - Key Concepts: Encapsulation, error handling

2. **[Parking Lot](system_design_problems/02_parking_lot.md)**
   - Vehicle management, availability tracking, fees
   - Design Patterns: Singleton, Factory, Strategy
   - Key Concepts: Enum states, calculations

3. **[Library Management](system_design_problems/03_library_management.md)**
   - Book tracking, member management, due dates
   - Design Patterns: Observer, Repository
   - Key Concepts: One-to-many relationships, overdue handling

4. **[Chess Game](system_design_problems/04_chess_game.md)**
   - Turn-based game with valid moves, win detection
   - Design Patterns: State, Factory
   - Key Concepts: Game state, move validation

5. **[Elevator System](system_design_problems/05_elevator_system.md)**
   - Floor management, scheduling, movement
   - Design Patterns: State, Factory, Observer
   - Key Concepts: Priority queue, state transitions

6. **[Movie Ticket Booking](system_design_problems/06_movie_ticket_booking.md)**
   - Show scheduling, seat availability, concurrency
   - Design Patterns: Factory, Observer
   - Key Concepts: Transactions, race conditions

7. **[Hotel Booking](system_design_problems/07_hotel_booking.md)**
   - Room availability, reservations, pricing
   - Design Patterns: Strategy, Observer
   - Key Concepts: Date ranges, guest management

8. **[Food Delivery](system_design_problems/08_food_delivery.md)**
   - Order management, delivery tracking, notifications
   - Design Patterns: Observer, Factory
   - Key Concepts: Status tracking, ratings

9. **[Notification System](system_design_problems/09_notification_system.md)**
   - Multi-channel delivery (Email, SMS, Push)
   - Design Patterns: Factory, Observer, Strategy
   - Key Concepts: Abstraction, templates

10. **[Ride Sharing (Uber)](system_design_problems/10_ride_sharing.md)**
    - Driver-rider matching, routing, payments
    - Design Patterns: Observer, Factory
    - Key Concepts: Geolocation, surge pricing

### High-Level Design (HLD) - Distributed Systems
11. **[LRU Cache](system_design_problems/11_lru_cache.md)**
    - In-memory cache with least-recently-used eviction
    - Data Structures: HashMap + DoublyLinkedList
    - Key Concepts: O(1) operations, thread-safe implementation

12. **[Rate Limiter](system_design_problems/12_rate_limiter.md)**
    - Control request rates per user/IP
    - Algorithms: Token Bucket, Sliding Window, Leaky Bucket
    - Key Concepts: Distributed coordination, Redis integration

13. **[URL Shortener (TinyURL)](system_design_problems/13_url_shortener.md)**
    - Convert long URLs to short codes
    - Techniques: Base62 encoding, consistent hashing
    - Key Concepts: Redirect service, analytics, expiration

14. **[Real-Time Chat App (WhatsApp)](system_design_problems/14_realtime_chat_app.md)**
    - One-to-one and group messaging
    - Architecture: WebSocket, message queue, georeplication
    - Key Concepts: Delivery guarantees, presence, typing indicators

15. **[Distributed Key-Value Store (Redis/DynamoDB)](system_design_problems/15_distributed_kv_store.md)**
    - Scalable storage with replication
    - Techniques: Consistent hashing, replication, persistence
    - Key Concepts: CAP theorem, eventual consistency

### Specialized Systems
16. **[Tic Tac Toe Game](system_design_problems/16_tic_tac_toe.md)**
    - Game logic with AI player
    - Algorithms: Minimax, alpha-beta pruning
    - Key Concepts: Game state, optimal strategy, difficulty levels

17. **[Thread-Safe HashMap](system_design_problems/17_thread_safe_hashmap.md)**
    - Concurrent hash map with minimal locking
    - Techniques: Segment locking, copy-on-write
    - Key Concepts: Concurrency, lock contention, scalability

---

## 🎯 Interview Tips & Strategies

### Quick Checklist for Each Topic

#### OOP Fundamentals
- [ ] Understand real-world analogies
- [ ] Know when to apply each concept
- [ ] Practice code examples
- [ ] Explain tradeoffs

#### Design Patterns
- [ ] Know problem it solves
- [ ] Can draw UML diagram
- [ ] Real-world examples ready
- [ ] Pros and cons prepared

#### System Design
- [ ] Requirements clear
- [ ] Components identified
- [ ] Design patterns applied
- [ ] Scalability considered

---

## 📖 How to Use This Guide

### For Quick Review
- Read main section headers
- Review real-world examples
- Check comparison tables

### For Deep Dive
- Read full explanation
- Study all code examples
- Practice implementation
- Answer interview questions

### For Interview Preparation
1. Pick a topic
2. Read definition and examples
3. Code out examples yourself
4. Answer interview questions
5. Explain to a friend

---

## 🔑 Most Important Topics

**Must Know ♥️:**
- SOLID Principles
- Polymorphism
- Factory & Builder patterns
- Thread Safety
- System Design process
- LRU Cache, Rate Limiter, URL Shortener

**Very Important ⭐:**
- Abstraction & Encapsulation
- Inheritance & Composition
- Strategy & Observer patterns
- Race conditions
- ATM & Parking Lot systems
- Distributed systems (Chat, KV Store)
- Concurrency (Thread-Safe HashMap)

**Important 📌:**
- All OOP concepts
- All design patterns
- Concurrency basics
- Each system design problem
- Game design (Tic Tac Toe, Chess)

---

## 🚀 Study Plan (4 Weeks)

### Week 1: OOP Fundamentals
- Days 1-2: Basics, Encapsulation, Abstraction
- Days 3-4: Inheritance, Polymorphism, Composition
- Days 5-7: Deep dive with real-world examples

### Week 2: Design Principles & Patterns
- Days 1-3: SOLID principles
- Days 4-7: Creational patterns (Singleton, Factory, Builder)

### Week 3: More Patterns & Concurrency
- Days 1-3: Behavioral patterns (Strategy, Observer)
- Days 4-7: Thread safety, synchronization, race conditions

### Week 4: System Design (LLD)
- Days 1-2: ATM Machine, Parking Lot
- Days 3-4: Library Management, Tic Tac Toe
- Days 5-7: Elevator, Movie Ticket, Hotel, Food Delivery

### Week 5 (Optional): Advanced System Design (HLD)
- Days 1: LRU Cache, Thread-Safe HashMap
- Days 2: Rate Limiter, URL Shortener
- Days 3: Real-Time Chat App
- Days 4: Distributed Key-Value Store
- Days 5-7: Review and practice all problems

---

## 💡 Key Takeaways

1. **OOP is about relationships** - Understand IS-A vs HAS-A
2. **Design Patterns are tools** - Use right tool for right problem
3. **SOLID leads to maintainability** - Apply in every design
4. **Concurrency is hard** - Always think about thread safety
5. **System Design is holistic** - Consider scalability, reliability, maintainability
6. **Real-world examples matter** - Relate concepts to actual use cases

---

## 📞 Quick Reference

### Common Patterns by Problem

| Problem | Patterns |
|---------|----------|
| Creating objects | Factory, Builder, Singleton |
| Changing behavior | Strategy, State, Decorator |
| Notifications | Observer, Pub/Sub |
| Access control | Proxy, Facade |
| Relationships | Composition, Aggregation |

### Common Anti-patterns to Avoid

- ❌ Deep inheritance hierarchies (max 3 levels)
- ❌ God objects (too many responsibilities)
- ❌ Tight coupling (depends on concrete classes)
- ❌ Missing synchronization (concurrent access)
- ❌ Ignoring SOLID principles

---

## 🎓 Quality Over Quantity

Focus on understanding concepts deeply rather than memorizing. Be able to:

✅ **Explain** why each concept exists
✅ **Compare** similar concepts
✅ **Apply** patterns to new problems
✅ **Discuss** tradeoffs
✅ **Code** working examples

---

## 📝 Last Minute Checklist

Before interview:
- [ ] Review SOLID principles
- [ ] Practice 1-2 system design problems
- [ ] Understand common patterns
- [ ] Be ready with real-world examples
- [ ] Know design tradeoffs
- [ ] Practice explaining concepts clearly
