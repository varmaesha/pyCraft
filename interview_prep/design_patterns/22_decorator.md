# Decorator Pattern

## Definition

**Decorator Pattern**: Add new functionality to objects dynamically without altering their structure.

**Purpose**: Provide flexible alternative to subclassing for extending functionality.

**Key Idea**: Wrap object with decorator that has same interface but adds behavior.

## Real-World Examples

### Example 1: Coffee Shop (Classic)

#### ❌ WITHOUT DECORATOR (Bad Approach)
```python
# Explosion of classes for combinations
class SimpleCoffee:
    def cost(self):
        return 2

class CoffeeWithMilk(SimpleCoffee):
    def cost(self):
        return super().cost() + 0.5

class CoffeeWithMilkAndSugar(CoffeeWithMilk):
    def cost(self):
        return super().cost() + 0.25

class CoffeeWithMilkSugarWhip(CoffeeWithMilkAndSugar):
    def cost(self):
        return super().cost() + 1.0

# And many more combinations...
# Class explosion!
```

#### ✅ WITH DECORATOR (Good Approach)
```python
class Coffee:
    def cost(self):
        pass
    
    def description(self):
        pass

class SimpleCoffee(Coffee):
    def cost(self):
        return 2
    
    def description(self):
        return "Simple Coffee"

# Decorators wrap Coffee and add functionality
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self.coffee = coffee
    
    def cost(self):
        return self.coffee.cost()
    
    def description(self):
        return self.coffee.description()

class MilkDecorator(CoffeeDecorator):
    def cost(self):
        return self.coffee.cost() + 0.5
    
    def description(self):
        return self.coffee.description() + ", Milk"

class SugarDecorator(CoffeeDecorator):
    def cost(self):
        return self.coffee.cost() + 0.25
    
    def description(self):
        return self.coffee.description() + ", Sugar"

class WhipDecorator(CoffeeDecorator):
    def cost(self):
        return self.coffee.cost() + 1.0
    
    def description(self):
        return self.coffee.description() + ", Whip"

# Easy composition!
coffee = SimpleCoffee()
coffee = MilkDecorator(coffee)
coffee = SugarDecorator(coffee)
coffee = WhipDecorator(coffee)

print(coffee.description())  # Simple Coffee, Milk, Sugar, Whip
print(f"${coffee.cost()}")   # $3.75

# Different combination without new classes
coffee2 = SimpleCoffee()
coffee2 = SugarDecorator(coffee2)
print(coffee2.description())  # Simple Coffee, Sugar
print(f"${coffee2.cost()}")   # $2.25
```

### Example 2: File Compression/Encryption

#### ❌ WITHOUT DECORATOR
```python
class DataWriter:
    def write(self, data):
        # Write plain data
        with open("file.txt", "w") as f:
            f.write(data)

class CompressedDataWriter:
    def write(self, data):
        # Compress then write
        compressed = compress(data)
        with open("file.txt", "w") as f:
            f.write(compressed)

class EncryptedDataWriter:
    def write(self, data):
        # Encrypt then write
        encrypted = encrypt(data)
        with open("file.txt", "w") as f:
            f.write(encrypted)

class CompressedEncryptedDataWriter:
    def write(self, data):
        # Compress and encrypt then write
        compressed = compress(data)
        encrypted = encrypt(compressed)
        with open("file.txt", "w") as f:
            f.write(encrypted)

# Need more combinations? More classes!
```

#### ✅ WITH DECORATOR
```python
class Writer:
    def write(self, data):
        pass

class FileWriter(Writer):
    def write(self, data):
        with open("file.txt", "w") as f:
            f.write(data)

class WriterDecorator(Writer):
    def __init__(self, writer: Writer):
        self.writer = writer
    
    def write(self, data):
        self.writer.write(data)

class CompressDecorator(WriterDecorator):
    def write(self, data):
        compressed = self._compress(data)
        self.writer.write(compressed)
    
    def _compress(self, data):
        import gzip
        return gzip.compress(data.encode())

class EncryptDecorator(WriterDecorator):
    def write(self, data):
        encrypted = self._encrypt(data)
        self.writer.write(encrypted)
    
    def _encrypt(self, data):
        # Simple XOR encryption for demo
        return ''.join(chr(ord(c) ^ 42) for c in data)

# Compose dynamically!
writer = FileWriter()
writer = CompressDecorator(writer)
writer = EncryptDecorator(writer)

writer.write("Sensitive data")

# Just compress?
writer2 = FileWriter()
writer2 = CompressDecorator(writer2)
writer2.write("Not sensitive data")

# Just encrypt?
writer3 = FileWriter()
writer3 = EncryptDecorator(writer3)
writer3.write("Encrypted data")
```

### Example 3: UI Components

#### ❌ WITHOUT DECORATOR
```python
class Window:
    def draw(self):
        print("Drawing window")

class WindowWithBorder(Window):
    def draw(self):
        super().draw()
        print("Drawing border")

class WindowWithBorderAndScroll(WindowWithBorder):
    def draw(self):
        super().draw()
        print("Drawing scrollbar")

class WindowWithBorderScrollAndTitle(WindowWithBorderAndScroll):
    def draw(self):
        super().draw()
        print("Drawing title")

# Multiple inheritance complexity!
```

#### ✅ WITH DECORATOR
```python
class Component:
    def draw(self):
        pass

class Window(Component):
    def draw(self):
        print("Drawing window")

class ComponentDecorator(Component):
    def __init__(self, component: Component):
        self.component = component
    
    def draw(self):
        self.component.draw()

class BorderDecorator(ComponentDecorator):
    def draw(self):
        self.component.draw()
        print("Drawing border")

class ScrollDecorator(ComponentDecorator):
    def draw(self):
        self.component.draw()
        print("Drawing scrollbar")

class TitleDecorator(ComponentDecorator):
    def draw(self):
        self.component.draw()
        print("Drawing title")

# Build UI dynamically
window = Window()
window = BorderDecorator(window)
window = ScrollDecorator(window)
window = TitleDecorator(window)
window.draw()

# Different UI without new classes
window2 = Window()
window2 = BorderDecorator(window2)
window2.draw()
```

### Example 4: Stream Processing

#### ✅ GOOD EXAMPLE (Decorator)
```python
class DataStream:
    def read(self):
        pass

class FileStream(DataStream):
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()

class StreamDecorator(DataStream):
    def __init__(self, stream: DataStream):
        self.stream = stream
    
    def read(self):
        return self.stream.read()

class DecompressionDecorator(StreamDecorator):
    def read(self):
        data = self.stream.read()
        import zlib
        return zlib.decompress(data)

class DecryptionDecorator(StreamDecorator):
    def read(self):
        data = self.stream.read()
        return ''.join(chr(ord(c) ^ 42) for c in data)

class TranslationDecorator(StreamDecorator):
    def read(self):
        data = self.stream.read()
        # Some translation/transformation
        return data.upper()

# Compose decorators
stream = FileStream("data.bin")
stream = DecompressionDecorator(stream)
stream = DecryptionDecorator(stream)
stream = TranslationDecorator(stream)

content = stream.read()
```

## Decorator vs Inheritance vs Composition

| Approach | Use Case | Pros | Cons |
|----------|----------|------|------|
| **Inheritance** | Fixed behavior hierarchy | Simple for static | Class explosion, tight coupling |
| **Composition** | Dynamic behavior | Flexible, reusable | More code |
| **Decorator** | Dynamic behavior stacking | Clean, flexible | Complexity with many decorators |

## Decorator Chain

```python
# Decorators wrap each other
Original
   ↓
Decorator1(Original)
   ↓
Decorator2(Decorator1(Original))
   ↓
Decorator3(Decorator2(Decorator1(Original)))

# When calling method:
Decorator3.method()
  → Decorator2.method()
    → Decorator1.method()
      → Original.method()
```

## Comparison Table

| Factor | Inheritance | Decorator |
|--------|-------------|-----------|
| Flexibility | Low | High |
| Runtime changes | No | Yes |
| Multiple features | Class explosion | Clean composition |
| Performance | Better | Slight overhead |
| Code reuse | Good | Excellent |

## Key Interview Questions

1. **When to use Decorator pattern?**
   - When need flexible, dynamic behavior addition

2. **Decorator vs Inheritance?**
   - Decorator: Runtime, flexible, multiple combinations
   - Inheritance: Compile-time, fixed, class hierarchy

3. **Real-world example?**
   - Coffee shop, UI components, file compression, streams

4. **Problem with many decorators?**
   - Complex chain, hard to debug, performance overhead

## Important Points

- ✅ Use for dynamic behavior addition
- ✅ Wrap objects with same interface
- ✅ Avoid class explosion
- ✅ Clean composition
- ✅ Runtime flexibility
- ⚠️ Can create complex chains
- ✅ Follow Single Responsibility
