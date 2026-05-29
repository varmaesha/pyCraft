# Designing for Extensibility

## Definition

**Extensibility**: Ability to add new features/functionality without modifying existing code.

**Principle**: Open-Closed Principle (OCP) - Open for extension, closed for modification.

## Real-World Examples

### Example 1: Payment System

#### ❌ NOT EXTENSIBLE
```python
class PaymentProcessor:
    def process_payment(self, payment_type, amount):
        if payment_type == "credit_card":
            # Credit card logic
            print(f"Processing credit card: ${amount}")
        elif payment_type == "paypal":
            # PayPal logic
            print(f"Processing PayPal: ${amount}")
        elif payment_type == "stripe":
            # Stripe logic
            print(f"Processing Stripe: ${amount}")
        # Adding Bitcoin means modifying this function!

processor = PaymentProcessor()
processor.process_payment("credit_card", 100)

# Problem: Adding new payment method requires modifying PaymentProcessor
```

#### ✅ EXTENSIBLE
```python
from abc import ABC, abstractmethod

# Abstraction - allows extension
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Existing implementations
class CreditCardPayment(PaymentMethod):
    def pay(self, amount):
        return f"Credit Card: ${amount}"

class PayPalPayment(PaymentMethod):
    def pay(self, amount):
        return f"PayPal: ${amount}"

# NEW payment method - no modification to existing code!
class BitcoinPayment(PaymentMethod):
    def pay(self, amount):
        return f"Bitcoin: ${amount}"

class PaymentProcessor:
    def process_payment(self, payment_method: PaymentMethod, amount):
        return payment_method.pay(amount)

# Usage - works with any PaymentMethod
processor = PaymentProcessor()
print(processor.process_payment(CreditCardPayment(), 100))
print(processor.process_payment(PayPalPayment(), 100))
print(processor.process_payment(BitcoinPayment(), 100))  # New feature!

# No changes to PaymentProcessor or existing implementations!
```

### Example 2: Notification System

#### ❌ NOT EXTENSIBLE
```python
class NotificationSender:
    def send(self, notification_type, recipient, message):
        if notification_type == "email":
            # Email logic
            print(f"Email to {recipient}: {message}")
        elif notification_type == "sms":
            # SMS logic
            print(f"SMS to {recipient}: {message}")
        elif notification_type == "slack":
            # Slack logic
            print(f"Slack to {recipient}: {message}")
        # Adding WhatsApp requires modifying NotificationSender!

# Problem: Method grows with each new notification type
```

#### ✅ EXTENSIBLE
```python
class Notification(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass

# Implementations
class EmailNotification(Notification):
    def send(self, recipient, message):
        print(f"Email to {recipient}: {message}")

class SMSNotification(Notification):
    def send(self, recipient, message):
        print(f"SMS to {recipient}: {message}")

class SlackNotification(Notification):
    def send(self, recipient, message):
        print(f"Slack to {recipient}: {message}")

# NEW notification type - just add class
class WhatsAppNotification(Notification):
    def send(self, recipient, message):
        print(f"WhatsApp to {recipient}: {message}")

class NotificationSender:
    def send(self, notification: Notification, recipient, message):
        notification.send(recipient, message)

# Usage
sender = NotificationSender()
sender.send(EmailNotification(), "user@example.com", "Hi!")
sender.send(WhatsAppNotification(), "+1234567890", "Hi!")  # New!

# NotificationSender never changed!
```

### Example 3: Report Generation

#### ❌ NOT EXTENSIBLE
```python
class ReportFormatter:
    def format(self, data, format_type):
        if format_type == "pdf":
            # PDF formatting
            return f"PDF: {data}"
        elif format_type == "excel":
            # Excel formatting
            return f"EXCEL: {data}"
        elif format_type == "json":
            # JSON formatting
            return f"JSON: {data}"
        # Adding CSV requires modifying this method!

# Problem: Hard to extend, many if-else
```

#### ✅ EXTENSIBLE
```python
class ReportFormat(ABC):
    @abstractmethod
    def format(self, data):
        pass

# Existing formats
class PDFReport(ReportFormat):
    def format(self, data):
        return f"PDF: {data}"

class ExcelReport(ReportFormat):
    def format(self, data):
        return f"EXCEL: {data}"

# NEW format - just add class
class CSVReport(ReportFormat):
    def format(self, data):
        return f"CSV: {data}"

class ReportFormatter:
    def format(self, data, report_format: ReportFormat):
        return report_format.format(data)

# Usage
formatter = ReportFormatter()
formatter.format([1, 2, 3], PDFReport())
formatter.format([1, 2, 3], CSVReport())  # New format!

# ReportFormatter is stable, new formats added without modification
```

### Example 4: Discount Calculation

#### ❌ NOT EXTENSIBLE
```python
class PriceCalculator:
    def calculate_final_price(self, price, discount_type):
        if discount_type == "percentage":
            return price * 0.9
        elif discount_type == "fixed":
            return price - 10
        elif discount_type == "buy_one_get_one":
            return price / 2
        # Adding loyalty discount requires modification!

# Hard to extend without changing method
```

#### ✅ EXTENSIBLE
```python
class Discount(ABC):
    @abstractmethod
    def apply(self, price):
        pass

class PercentageDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent
    
    def apply(self, price):
        return price * (1 - self.percent / 100)

class FixedDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount
    
    def apply(self, price):
        return price - self.amount

# NEW discount type
class LoyaltyDiscount(Discount):
    def __init__(self, points):
        self.points = points
    
    def apply(self, price):
        return price * (1 - (self.points / 100))

class PriceCalculator:
    def calculate_final_price(self, price, discount: Discount):
        return discount.apply(price)

# Usage
calc = PriceCalculator()
print(calc.calculate_final_price(100, PercentageDiscount(10)))
print(calc.calculate_final_price(100, LoyaltyDiscount(20)))  # New!

# Easy to extend with new discount types
```

## Techniques for Extensibility

### 1. Use Abstractions (Interfaces/Abstract Classes)
```python
# Instead of concrete types
def process(payment: CreditCard):  # BAD

# Use abstractions
def process(payment: PaymentMethod):  # GOOD
    pass
```

### 2. Dependency Injection
```python
# Instead of creating dependencies
class Service:
    def __init__(self):
        self.logger = Logger()  # Hard-coded

# Accept dependencies
class Service:
    def __init__(self, logger):  # Easily swappable
        self.logger = logger
```

### 3. Strategy Pattern
```python
# Define family of algorithms
class Algorithm(ABC):
    @abstractmethod
    def execute(self, data):
        pass

# Easy to add new algorithms
```

### 4. Plugin Architecture
```python
# Register implementations dynamically
class PluginRegistry:
    def __init__(self):
        self.plugins = {}
    
    def register(self, name, plugin):
        self.plugins[name] = plugin
    
    def execute(self, name, data):
        return self.plugins[name].execute(data)
```

## Extensibility vs Complexity

**Balance**: Don't over-engineer for extensibility that won't happen.

```python
# ❌ OVER-ENGINEERED
class SinglePaymentProcessor:
    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy
    # Even though only one payment method exists

# ✅ APPROPRIATE
# Use simple approach until need extension
def process_credit_card(amount):
    return charge_card(amount)

# Then refactor to strategy when needed
```

## Key Interview Questions

1. **How do you design for extensibility?**
   - Use abstractions, avoid concrete dependencies, follow OCP

2. **When is extensibility needed?**
   - When you expect future changes or multiple implementations

3. **Cost of over-engineering for extensibility?**
   - Unnecessary complexity, harder to understand

4. **Example of extensible design?**
   - Payment processors using interface pattern

## Important Points

- ✅ Use abstractions for extensibility
- ✅ Follow Open-Closed Principle
- ✅ Identify extension points early
- ✅ New features = new classes, not modifications
- ⚠️ Don't over-engineer
- ✅ Balance extensibility with simplicity
