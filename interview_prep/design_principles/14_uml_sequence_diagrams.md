# UML Sequence Diagrams

## Definition

**UML Sequence Diagram**: Visual representation of how objects interact over time with message flow.

**Purpose**: Show order of operations, interactions, and timing in a system.

## Diagram Components

```
Actor/Object | Object | Object
    |          |         |
    |          |         |
    |---msg1---->        |
    |          |         |
    |          |---msg2---->
    |          |         |
    |          |<--msg3--|
    |----------result----|
    |          |         |
```

- **Actors**: External users/systems
- **Objects**: System components
- **Messages**: Communication (calls, returns)
- **Lifeline**: Vertical dashed line (lifetime)
- **Activation Box**: Bar showing active execution

## Real-World Examples

### Example 1: User Login Flow

```
User          | System        | Database      | EmailService
 |             |              |               |
 |--login----->|              |               |
 |             |--query user--|               |
 |             |<--user data--|               |
 |             |--validate----|               |
 |             |              |               |
 |             |--send email--|--->|           |
 |             |<--sent ok----|<---|
 |<--success---|              |
 |             |              |
```

**Sequence**:
1. User sends login credentials
2. System queries database for user
3. Database returns user data
4. System validates credentials
5. System requests email service send confirmation
6. Email service confirms sent
7. System returns success to user

### Example 2: Online Shopping - Order Processing

```
Customer      | WebServer     | Payment       | Inventory     | Notification
  |            |               |               |               |
  |--order---->|               |               |               |
  |            |--verify----->|               |               |
  |            |<--valid------|               |               |
  |            |               |--charge----->|               |
  |            |               |<--success----|               |
  |            |                               |--reduce---->|
  |            |                               |<--reduced---|
  |            |                                               |
  |            |--------send order confirmed---------------->|
  |<--confirm--|<--notification sent--------------------------|
  |            |               |               |               |
```

**Sequence**:
1. Customer places order
2. WebServer verifies payment details
3. Payment gateway charges credit card
4. Inventory service reduces stock
5. Notification service sends confirmation email
6. Customer receives confirmation

### Example 3: ATM Withdrawal

```
User          | ATM           | Bank          | Database
 |             |               |               |
 |--insert---->|               |               |
 |             |               |               |
 |--PIN------->|               |               |
 |             |--verify------>|               |
 |             |<--valid-------|               |
 |             |               |               |
 |--amount---->|               |               |
 |             |--check balance|               |
 |             |               |--query (acc)--|
 |             |               |<--balance----|
 |             |<--sufficient--|               |
 |             |               |               |
 |             |--debit-------->-|
 |             |               |--update db---|
 |             |               |<--updated---|
 |             |               |               |
 |             |--dispense----->              |
 |<--cash------|               |               |
 |--eject card-|               |               |
```

**Sequence**:
1. User inserts ATM card
2. User enters PIN
3. ATM verifies PIN with Bank
4. User enters withdrawal amount
5. ATM checks balance with Database
6. If sufficient, Bank debits account
7. Database updated
8. ATM dispenses cash
9. Card ejected

### Example 4: Email Sending with Retry Logic

```
Application   | EmailQueue    | EmailService  | SMTPServer
  |            |               |               |
  |--send----->|               |               |
  |            |--process----->|               |
  |            |               |--connect---->|
  |            |               |<--ACK--------|
  |            |               |--send----->|
  |            |               |<--TIMEOUT--|
  |            |<--error-------|               |
  |            |               |               |
  |            |--retry (delay)--|            |
  |            |--process----->|               |
  |            |               |--connect---->|
  |            |<--success-----|<--OK--------|
  |<--confirmed|               |               |
  |            |               |               |
```

**Sequence**:
1. Application queues email
2. EmailQueue processes
3. EmailService connects to SMTP
4. SMTP times out (failure)
5. Queue logs error and retries after delay
6. Retries connection
7. SMTP returns success
8. Application notified

### Example 5: Movie Ticket Booking

```
Customer      | WebApp        | PaymentGW     | Ticketing     | Notification
  |            |               |               |               |
  |--search--->|               |               |               |
  |            |               |               |               |
  |--select--->|               |               |               |
  |            |               |               |               |
  |--book----->|               |               |               |
  |            |--verify seats-|               |               |
  |            |               |--reserve---->|               |
  |            |               |<--reserved---|               |
  |            |--charge----->|               |               |
  |            |<--success----|               |               |
  |            |               |               |               |
  |            |--------issue ticket--------->|               |
  |            |               |               |               |
  |            |-----send confirmation-------------------------------->|
  |<--confirm--|               |               |               |
  |            |               |               |               |
```

**Sequence**:
1. Customer searches for movies/shows
2. Customer selects show and seats
3. WebApp verifies seat availability
4. Ticketing system reserves seats
5. Payment gateway processes payment
6. Ticketing system issues ticket
7. Notification service sends confirmation

## Creating Sequence Diagrams

### Format (Text-based - ASCII)

```
Object1       Object2       Object3
  |             |             |
  |--msg1------->             |
  |             |             |
  |             |--msg2------->
  |             |             |
  |             |<--response--|
  |<----return--|             |
  |             |             |
  |--msg3------->             |
  |             |             |
  |<----data----|             |
```

### In Code (Using sequence diagram libraries)

**Python Example with mermaid-js**:
```python
# Using sequence in documentation
sequence_diagram = """
sequenceDiagram
    User->>System: login(email, password)
    System->>Database: query_user(email)
    Database-->>System: user_data
    System->>System: validate_password()
    System-->>User: success
"""
```

## Types of Messages

| Message Type | Symbol | Meaning |
|--------------|--------|---------|
| Synchronous Call | -> | Waits for response |
| Asynchronous | ->> | Doesn't wait |
| Return | <-- | Response message |
| Self Call | -> Self | Object calls itself |
| Callback | <- | Callback/response |

## Interactions

### Synchronous (Blocking)
```
Client   | Server
  |       |
  |---call--->  <- Client waits
  |       |
  |       | Processing
  |       |
  |<--return--  <- Client resumes
  |       |
```

### Asynchronous (Non-blocking)
```
Client   | Server
  |       |
  |===>   | <- Client doesn't wait
  |       |
  |       | Processing
  |       |
  |       | Event notification sent later
  |<--event-  <- Separate callback
```

## Common Patterns in Sequence Diagrams

### Pattern 1: Request-Response
```
Client   | Server
  |       |
  |--req-->
  |       | Process
  |<--res--
  |       |
```

### Pattern 2: Publish-Subscribe
```
Publisher | Subscriber1 | Subscriber2
   |       |             |
   |--publish-->         |
   |       |             |
   |-------publish------->
   |       |             |
```

### Pattern 3: Chain of Calls
```
A | B | C | D
 | |  |  |
 |--call--->
 |   |  |
 |   |--call--->
 |   |   |  |
 |   |   |--call--->
 |   |   |   |
 |<-----|<--|  Return
 |
```

### Pattern 4: Decision/Loop
```
Actor | System | Database
  |    |        |
  |--login----->
  |    | [if valid]
  |    |--query---->
  |    |<--data---
  |    | [loop: check attempts]
  |<--login ok--
  |    |        |
```

## Interview Tips

1. **Ask clarifying questions**: What's the actor? What's the interaction?
2. **Start simple**: Identify main objects and sequence
3. **Add error cases**: What happens if things fail?
4. **Show timing**: Which operations are synchronous vs async?
5. **Use standard notation**: Make it understandable

## Key Interview Questions

1. **What's in a sequence diagram?**
   - Actors, objects, messages, timing, interactions

2. **How to show error handling?**
   - Alternative paths, exception messages

3. **Synchronous vs async in diagrams?**
   - Arrow types indicate call styles

4. **When to use sequence diagrams?**
   - Complex interactions, API design, system behavior

## Important Points

- ✅ Show interaction flow clearly
- ✅ Use proper message notation
- ✅ Include error scenarios
- ✅ Show timing and sequencing
- ✅ Name objects and messages clearly
- ✅ Include return values
- ✅ Make diagrams simple and readable
