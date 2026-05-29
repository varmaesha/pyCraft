# Inheritance

## Definition

**Inheritance** allows a class to inherit properties and methods from another class. It promotes code reusability and establishes IS-A relationships.

## Types of Inheritance

1. **Single**: Child inherits from one parent
2. **Multiple**: Child inherits from multiple parents
3. **Multilevel**: Grandparent → Parent → Child
4. **Hierarchical**: Multiple children from one parent

## Real-World Examples

### Example 1: Vehicle System (Single Inheritance)
```python
# Parent class
class Vehicle:
    def __init__(self, brand, color):
        self.brand = brand
        self.color = color
    
    def start(self):
        return f"{self.brand} vehicle started"
    
    def stop(self):
        return f"{self.brand} vehicle stopped"

# Child class - inherits from Vehicle
class Car(Vehicle):
    def __init__(self, brand, color, doors):
        super().__init__(brand, color)  # Call parent constructor
        self.doors = doors
    
    def open_trunk(self):
        return "Trunk opened"

class Bike(Vehicle):
    def start(self):  # Override parent method
        return f"{self.brand} bike started with kick start"

# Usage
car = Car("Toyota", "Red", 4)
print(car.start())          # Output: Toyota vehicle started
print(car.open_trunk())     # Output: Trunk opened

bike = Bike("Harley", "Black")
print(bike.start())         # Output: Harley bike started with kick start
```

### Example 2: Employee Hierarchy (Multilevel Inheritance)
```python
# Base class
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def get_info(self):
        return f"Name: {self.name}, Age: {self.age}"

# Middle class
class Employee(Person):
    def __init__(self, name, age, employee_id, salary):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.salary = salary
    
    def get_salary(self):
        return f"Salary: ${self.salary}"

# Final class
class Manager(Employee):
    def __init__(self, name, age, employee_id, salary, team_size):
        super().__init__(name, age, employee_id, salary)
        self.team_size = team_size
    
    def get_info(self):
        return f"{super().get_info()}, ID: {self.employee_id}, Team Size: {self.team_size}"

# Usage
manager = Manager("Alice", 40, "E001", 10000, 5)
print(manager.get_info())       # Name: Alice, Age: 40, ID: E001, Team Size: 5
print(manager.get_salary())     # Salary: $10000
```

### Example 3: Payment Systems (Hierarchical Inheritance)
```python
# Parent class
class PaymentMethod:
    def __init__(self, amount):
        self.amount = amount
    
    def validate(self):
        return True
    
    def process(self):
        pass

# Card payment
class CreditCard(PaymentMethod):
    def __init__(self, amount, card_number):
        super().__init__(amount)
        self.card_number = card_number
    
    def process(self):
        if self.validate():
            return f"Processed ${self.amount} via Credit Card (****{self.card_number[-4:]})"

# Wallet payment
class DigitalWallet(PaymentMethod):
    def __init__(self, amount, wallet_id):
        super().__init__(amount)
        self.wallet_id = wallet_id
    
    def process(self):
        if self.validate():
            return f"Processed ${self.amount} via Digital Wallet {self.wallet_id}"

# Bank transfer
class BankTransfer(PaymentMethod):
    def __init__(self, amount, account_number):
        super().__init__(amount)
        self.account_number = account_number
    
    def process(self):
        if self.validate():
            return f"Processed ${self.amount} via Bank Transfer to {self.account_number}"

# Usage
payments = [
    CreditCard(100, "4111111111111111"),
    DigitalWallet(50, "WALLET123"),
    BankTransfer(200, "123456789")
]

for payment in payments:
    print(payment.process())
```

### Example 4: Multiple Inheritance (Animal Example)
```python
# Parent classes
class Flyer:
    def fly(self):
        return "Flying..."

class Swimmer:
    def swim(self):
        return "Swimming..."

class Walker:
    def walk(self):
        return "Walking..."

# Single parent
class Bird(Flyer):
    pass

class Fish(Swimmer):
    pass

# Multiple parents
class Duck(Flyer, Swimmer):
    def quack(self):
        return "Quack!"

class Penguin(Swimmer, Walker):
    def waddle(self):
        return "Waddling..."

# Usage
duck = Duck()
print(duck.fly())       # Flying...
print(duck.swim())      # Swimming...
print(duck.quack())     # Quack!

penguin = Penguin()
print(penguin.swim())   # Swimming...
print(penguin.walk())   # Walking...
print(penguin.waddle()) # Waddling...
```

## Method Resolution Order (MRO)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):
    pass

d = D()
print(d.method())           # Output: B
print(D.__mro__)            # Shows inheritance order
# MRO: D -> B -> C -> A -> object
```

## Key Interview Questions

1. **What's the difference between method overriding and overloading?**
   - Overriding: Child changes parent's method (same signature)
   - Overloading: Multiple methods with same name (different signatures)

2. **When should you use inheritance?**
   - IS-A relationship (Car IS-A Vehicle)

3. **What's super() used for?**
   - Call parent class methods/constructor

4. **What are the pitfalls of inheritance?**
   - Tight coupling, fragile base class problem, multiple inheritance complexity

## Benefits

- ✅ Code Reusability
- ✅ Extensibility
- ✅ Relationship Modeling (IS-A)
- ✅ Polymorphism enablement

## Important Points

- ✅ Use inheritance for IS-A relationships
- ✅ Call parent constructor with `super().__init__()`
- ✅ Override methods when child needs different behavior
- ✅ Be careful with multiple inheritance (diamond problem)
- ✅ Prefer composition over inheritance in complex cases
