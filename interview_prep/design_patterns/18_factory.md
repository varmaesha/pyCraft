# Design Patterns - Factory

## Definition

**Factory Pattern** creates objects without specifying exact classes. It abstracts object creation.

## Types

1. **Simple Factory**: Single factory method
2. **Factory Method**: Each creator class has its own factory method
3. **Abstract Factory**: Family of related objects

## Real-World Examples

### Example 1: Payment Method Factory
```python
from abc import ABC, abstractmethod

# Product hierarchy
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CreditCard(PaymentMethod):
    def pay(self, amount):
        return f"Paying ${amount} with Credit Card"

class PayPal(PaymentMethod):
    def pay(self, amount):
        return f"Paying ${amount} with PayPal"

class Crypto(PaymentMethod):
    def pay(self, amount):
        return f"Paying ${amount} with Cryptocurrency"

# Simple Factory
class PaymentFactory:
    @staticmethod
    def create_payment(payment_type):
        if payment_type == "credit_card":
            return CreditCard()
        elif payment_type == "paypal":
            return PayPal()
        elif payment_type == "crypto":
            return Crypto()
        else:
            raise ValueError(f"Unknown payment type: {payment_type}")

# Usage
factory = PaymentFactory()
payment = factory.create_payment("credit_card")
print(payment.pay(99.99))

payment = factory.create_payment("paypal")
print(payment.pay(99.99))
```

### Example 2: Database Connection Factory
```python
class Database(ABC):
    @abstractmethod
    def execute(self, query):
        pass

class MySQLDatabase(Database):
    def execute(self, query):
        return f"MySQL: {query}"

class PostgreSQLDatabase(Database):
    def execute(self, query):
        return f"PostgreSQL: {query}"

class MongoDatabase(Database):
    def execute(self, query):
        return f"MongoDB: {query}"

class DatabaseFactory:
    @staticmethod
    def create_database(db_type):
        databases = {
            "mysql": MySQLDatabase,
            "postgresql": PostgreSQLDatabase,
            "mongodb": MongoDatabase
        }
        db_class = databases.get(db_type)
        if db_class:
            return db_class()
        raise ValueError(f"Unknown database: {db_type}")

# Usage
factory = DatabaseFactory()
mysql_db = factory.create_database("mysql")
print(mysql_db.execute("SELECT * FROM users"))

mongo_db = factory.create_database("mongodb")
print(mongo_db.execute("db.users.find()"))
```

### Example 3: Notification Factory
```python
class Notification(ABC):
    @abstractmethod
    def send(self, recipient, message):
        pass

class EmailNotification(Notification):
    def send(self, recipient, message):
        return f"Email sent to {recipient}: {message}"

class SMSNotification(Notification):
    def send(self, recipient, message):
        return f"SMS sent to {recipient}: {message}"

class PushNotification(Notification):
    def send(self, recipient, message):
        return f"Push notification sent to {recipient}: {message}"

class NotificationFactory:
    @staticmethod
    def create_notification(notification_type):
        notifications = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification
        }
        return notifications[notification_type]()

# Usage
def send_notification(notification_type, recipient, message):
    notification = NotificationFactory.create_notification(notification_type)
    return notification.send(recipient, message)

print(send_notification("email", "user@example.com", "Welcome!"))
print(send_notification("sms", "+1234567890", "Your code: 12345"))
print(send_notification("push", "user_id_123", "New message!"))
```

### Example 4: UI Component Factory
```python
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class WindowsButton(Button):
    def render(self):
        return "Rendering Windows button with native look"

class MacButton(Button):
    def render(self):
        return "Rendering Mac button with native look"

class LinuxButton(Button):
    def render(self):
        return "Rendering Linux button with native look"

class ButtonFactory:
    @staticmethod
    def create_button(os_type):
        buttons = {
            "windows": WindowsButton,
            "mac": MacButton,
            "linux": LinuxButton
        }
        return buttons[os_type]()

# Usage
import platform

current_os = platform.system().lower()
if current_os == "darwin":
    current_os = "mac"

button = ButtonFactory.create_button(current_os)
print(button.render())
```

### Example 5: Document Factory (Real-world E-commerce)
```python
class Document(ABC):
    @abstractmethod
    def save(self, filename):
        pass
    
    @abstractmethod
    def generate_report(self):
        pass

class PDFDocument(Document):
    def save(self, filename):
        return f"Saving as PDF: {filename}.pdf"
    
    def generate_report(self):
        return "PDF Report generated"

class ExcelDocument(Document):
    def save(self, filename):
        return f"Saving as Excel: {filename}.xlsx"
    
    def generate_report(self):
        return "Excel Report with charts generated"

class CSVDocument(Document):
    def save(self, filename):
        return f"Saving as CSV: {filename}.csv"
    
    def generate_report(self):
        return "CSV Report generated"

class DocumentFactory:
    @staticmethod
    def create_document(doc_type):
        documents = {
            "pdf": PDFDocument,
            "excel": ExcelDocument,
            "csv": CSVDocument
        }
        return documents[doc_type]()

# Usage - E-commerce order report system
def generate_sales_report(file_format):
    document = DocumentFactory.create_document(file_format)
    print(document.generate_report())
    print(document.save("sales_report_2024"))

generate_sales_report("pdf")
generate_sales_report("excel")
```

## Factory Method vs Simple Factory

### Factory Method (More Decoupled)
```python
class Creator(ABC):
    @abstractmethod
    def create_product(self):
        pass

class ConcreteCreatorA(Creator):
    def create_product(self):
        return ProductA()

class ConcreteCreatorB(Creator):
    def create_product(self):
        return ProductB()

# Usage
creator = ConcreteCreatorA()
product = creator.create_product()
```

## Benefits

- ✅ Decouples object creation from usage
- ✅ Easy to add new types
- ✅ Centralizes creation logic
- ✅ Follows Open-Closed Principle

## Key Interview Questions

1. **When should you use Factory Pattern?**
   - Multiple related subclasses, creation logic is complex

2. **Difference between Factory and Abstract Factory?**
   - Factory: single product | Abstract Factory: family of products

3. **Real-world example of Factory?**
   - Database connections, UI components, document types

## Important Points

- ✅ Use when object creation is complex
- ✅ Use when you have multiple similar classes
- ✅ Use when creation logic needs centralization
- ✅ Avoid over-engineering simple cases
