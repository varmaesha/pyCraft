# Design Patterns - Strategy

## Definition

**Strategy Pattern** defines a family of algorithms, encapsulates each, and makes them interchangeable.

## Key Idea

The algorithm varies independent of clients that use it. Encapsulate each algorithm separately.

## Real-World Examples

### Example 1: Payment Processing Strategies
```python
from abc import ABC, abstractmethod

# Strategy interface
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

# Concrete strategies
class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number, cvv):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount):
        return f"Charged ${amount} to card {self.card_number[-4:]}"

class PayPalStrategy(PaymentStrategy):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        return f"Charged ${amount} via PayPal ({self.email})"

class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def pay(self, amount):
        return f"Transferred {amount} crypto to {self.wallet_address}"

# Context
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.strategy = None
    
    def add_item(self, item, price):
        self.items.append({"item": item, "price": price})
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.strategy = strategy
    
    def checkout(self):
        total = sum(item["price"] for item in self.items)
        if self.strategy:
            return self.strategy.pay(total)
        return "No payment method selected"

# Usage
cart = ShoppingCart()
cart.add_item("Laptop", 1200)
cart.add_item("Mouse", 50)

# User chooses payment strategy
cart.set_payment_strategy(CreditCardStrategy("4111111111111111", "123"))
print(cart.checkout())  # Charged $1250 to card 1111

cart.set_payment_strategy(PayPalStrategy("user@example.com"))
print(cart.checkout())  # Charged $1250 via PayPal (user@example.com)

cart.set_payment_strategy(CryptoStrategy("0x123..."))
print(cart.checkout())  # Transferred 1250 crypto to 0x123...
```

### Example 2: Sorting Strategies
```python
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class BubbleSortStrategy(SortStrategy):
    def sort(self, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        # Simplified quick sort
        if len(data) <= 1:
            return data
        pivot = data[0]
        less = [x for x in data[1:] if x <= pivot]
        greater = [x for x in data[1:] if x > pivot]
        return self.sort(less) + [pivot] + self.sort(greater)

class MergeSortStrategy(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class DataSorter:
    def __init__(self):
        self.strategy = None
    
    def set_strategy(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def execute(self, data):
        if self.strategy:
            return self.strategy.sort(data.copy())
        return data

# Usage
data = [64, 34, 25, 12, 22, 11, 90]

sorter = DataSorter()

sorter.set_strategy(BubbleSortStrategy())
print("Bubble Sort:", sorter.execute(data))

sorter.set_strategy(QuickSortStrategy())
print("Quick Sort:", sorter.execute(data))

sorter.set_strategy(MergeSortStrategy())
print("Merge Sort:", sorter.execute(data))
```

### Example 3: Compression Strategies
```python
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, file_data):
        pass
    
    @abstractmethod
    def decompress(self, compressed_data):
        pass

class ZipCompressionStrategy(CompressionStrategy):
    def compress(self, file_data):
        return f"[ZIP] {file_data}"
    
    def decompress(self, compressed_data):
        return compressed_data.replace("[ZIP] ", "")

class RarCompressionStrategy(CompressionStrategy):
    def compress(self, file_data):
        return f"[RAR] {file_data}"
    
    def decompress(self, compressed_data):
        return compressed_data.replace("[RAR] ", "")

class GzipCompressionStrategy(CompressionStrategy):
    def compress(self, file_data):
        return f"[GZIP] {file_data}"
    
    def decompress(self, compressed_data):
        return compressed_data.replace("[GZIP] ", "")

class FileArchiver:
    def __init__(self, strategy: CompressionStrategy):
        self.strategy = strategy
    
    def compress_file(self, file_data):
        return self.strategy.compress(file_data)
    
    def decompress_file(self, compressed_data):
        return self.strategy.decompress(compressed_data)

# Usage
file_data = "This is a large file content"

archiver = FileArchiver(ZipCompressionStrategy())
compressed = archiver.compress_file(file_data)
print(f"Compressed: {compressed}")
print(f"Decompressed: {archiver.decompress_file(compressed)}")

archiver = FileArchiver(GzipCompressionStrategy())
compressed = archiver.compress_file(file_data)
print(f"Compressed: {compressed}")
```

### Example 4: Notification Strategies (Real-world)
```python
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailStrategy(NotificationStrategy):
    def __init__(self, email):
        self.email = email
    
    def send(self, message):
        return f"Email sent to {self.email}: {message}"

class SMSStrategy(NotificationStrategy):
    def __init__(self, phone):
        self.phone = phone
    
    def send(self, message):
        return f"SMS sent to {self.phone}: {message}"

class PushStrategy(NotificationStrategy):
    def __init__(self, device_id):
        self.device_id = device_id
    
    def send(self, message):
        return f"Push notification to {self.device_id}: {message}"

class User:
    def __init__(self, name):
        self.name = name
        self.notification_strategy = None
    
    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_strategy = strategy
    
    def notify(self, message):
        if self.notification_strategy:
            return self.notification_strategy.send(message)
        return "No notification method set"

# Usage
user = User("John")

user.set_notification_strategy(EmailStrategy("john@example.com"))
print(user.notify("Order confirmed"))

user.set_notification_strategy(SMSStrategy("+1234567890"))
print(user.notify("Order shipped"))

user.set_notification_strategy(PushStrategy("device_123"))
print(user.notify("Order delivered"))
```

## Benefits

| Benefit | Example |
|---------|---------|
| **Flexibility** | Change algorithms at runtime |
| **Encapsulation** | Each algorithm in separate class |
| **Open-Closed** | Add new strategies without modifying context |
| **Testing** | Easy to test each strategy independently |

## Strategy vs Decorator

| Strategy | Decorator |
|----------|-----------|
| Change behavior | Add behavior |
| Runtime selection | Chain behaviors |
| One strategy at a time | Multiple decorators |

## Key Interview Questions

1. **When to use Strategy?**
   - Multiple algorithms for same task, runtime selection needed

2. **Example from your experience?**
   - Payment methods, sorting algorithms, compression formats

3. **How does Strategy differ from State?**
   - Strategy: client chooses | State: object's state determines behavior

## Important Points

- ✅ Excellent for algorithm families
- ✅ Promotes Open-Closed Principle
- ✅ Easy to add new strategies
- ✅ Runtime behavior switching
- ❌ Overkill for single algorithm
