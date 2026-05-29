# Deep Copy vs Shallow Copy

## Definitions

### Shallow Copy
Copies the object and references to its contents. **Nested objects** are not copied.

### Deep Copy
Recursively copies the object and all nested objects. **Complete independence**.

## Real-World Example

### Example 1: List Copying
```python
import copy

# Original list
original = [[1, 2], [3, 4], [5, 6]]

# Assignment - just creates reference
reference = original
reference[0][0] = 999
print(original)  # [[999, 2], [3, 4], [5, 6]] - MODIFIED!

# Shallow copy - copies list, but not nested lists
original = [[1, 2], [3, 4], [5, 6]]
shallow = copy.copy(original)
shallow[0][0] = 999
print(original)  # [[999, 2], [3, 4], [5, 6]] - MODIFIED!

# Deep copy - copies everything
original = [[1, 2], [3, 4], [5, 6]]
deep = copy.deepcopy(original)
deep[0][0] = 999
print(original)  # [[1, 2], [3, 4], [5, 6]] - SAFE!
```

### Example 2: Object with Nested Objects
```python
import copy

class Address:
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code
    
    def __repr__(self):
        return f"Address({self.city}, {self.zip_code})"

class Person:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def __repr__(self):
        return f"Person({self.name}, {self.address})"

# Create original
address = Address("New York", "10001")
person1 = Person("Alice", address)

# Shallow copy - address is shared!
person2 = copy.copy(person1)
person2.name = "Bob"
person2.address.city = "Boston"

print(person1)  # Person(Alice, Address(Boston, 10001)) - MODIFIED!
print(person2)  # Person(Bob, Address(Boston, 10001))

# Deep copy - completely independent
address = Address("New York", "10001")
person1 = Person("Alice", address)
person3 = copy.deepcopy(person1)
person3.name = "Charlie"
person3.address.city = "Chicago"

print(person1)  # Person(Alice, Address(New York, 10001)) - SAFE!
print(person3)  # Person(Charlie, Address(Chicago, 10001))
```

### Example 3: Database Record Copying
```python
# ❌ BAD - Using shallow copy for database records
class DatabaseRecord:
    def __init__(self, id, name, metadata):
        self.id = id
        self.name = name
        self.metadata = metadata  # Nested dict

record1 = DatabaseRecord(1, "User1", {"roles": ["admin"], "permissions": {}})
record2 = copy.copy(record1)  # Shallow copy

# Modifying nested metadata affects original!
record2.metadata["roles"].append("superadmin")
print(record1.metadata)  # {"roles": ["admin", "superadmin"]} - MODIFIED!

# ✅ GOOD - Use deep copy for independent database records
record1 = DatabaseRecord(1, "User1", {"roles": ["admin"], "permissions": {}})
record2 = copy.deepcopy(record1)  # Deep copy

record2.metadata["roles"].append("superadmin")
print(record1.metadata)  # {"roles": ["admin"]} - SAFE!
print(record2.metadata)  # {"roles": ["admin", "superadmin"]}
```

### Example 4: Game State Cloning
```python
import copy

class Item:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

class Player:
    def __init__(self, name, inventory):
        self.name = name
        self.inventory = inventory  # List of Item objects
    
    def save_checkpoint(self):
        # MUST use deep copy to preserve game state
        saved_state = copy.deepcopy(self)
        return saved_state
    
    def restore_checkpoint(self, checkpoint):
        self.inventory = copy.deepcopy(checkpoint.inventory)

# Gameplay
player = Player("Hero", [Item("sword", 1), Item("potion", 5)])

# Save checkpoint
checkpoint = player.save_checkpoint()

# Play and lose items
player.inventory[1].quantity = 0

# Restore from checkpoint
player.restore_checkpoint(checkpoint)
print(player.inventory[1].quantity)  # 5 - RESTORED!
```

### Example 5: Configuration Cloning
```python
import copy

class ConfigSection:
    def __init__(self, name, settings):
        self.name = name
        self.settings = settings

class AppConfig:
    def __init__(self):
        self.sections = {
            "database": ConfigSection("database", {"host": "localhost", "port": 5432}),
            "cache": ConfigSection("cache", {"ttl": 3600, "max_size": 1000})
        }
    
    # ❌ Shallow copy - sections are shared
    def get_config_shallow(self):
        return copy.copy(self)
    
    # ✅ Deep copy - completely independent
    def get_config_deep(self):
        return copy.deepcopy(self)

config1 = AppConfig()
config2 = copy.copy(config1)  # Shallow copy

# Sections are shared!
config2.sections["database"].settings["host"] = "remote-server"
print(config1.sections["database"].settings["host"])
# "remote-server" - MODIFIED!

# Solution: use deep copy
config1 = AppConfig()
config3 = copy.deepcopy(config1)

config3.sections["database"].settings["host"] = "remote-server"
print(config1.sections["database"].settings["host"])
# "localhost" - SAFE!
```

### Example 6: Undo/Redo System
```python
import copy

class Editor:
    def __init__(self):
        self.content = []
        self.history = []
    
    def add_line(self, line):
        self.content.append(line)
        # Save deep copy for undo
        self.history.append(copy.deepcopy(self.content))
    
    def undo(self):
        if self.history:
            self.content = copy.deepcopy(self.history.pop())
    
    def get_content(self):
        return self.content

# Usage
editor = Editor()
editor.add_line("Line 1")
editor.add_line("Line 2")
editor.add_line("Line 3")

print(editor.get_content())  # ["Line 1", "Line 2", "Line 3"]

editor.undo()
print(editor.get_content())  # ["Line 1", "Line 2"]

editor.undo()
print(editor.get_content())  # ["Line 1"]
```

## Comparison Table

| Aspect | Assignment | Shallow Copy | Deep Copy |
|--------|-----------|--------------|-----------|
| **Reference** | Same | Different | Different |
| **Nested Refs** | Shared | Shared | Independent |
| **Independence** | No | Partial | Complete |
| **Speed** | Fast | Moderate | Slow |
| **Memory** | Minimal | Moderate | Maximum |

## When to Use

### Use Assignment When:
- Want to reference same object
- Intended behavior

### Use Shallow Copy When:
- Only top-level changes
- Performance critical
- No nested modifications

### Use Deep Copy When:
- Complete independence needed
- Complex nested structures
- Undo/redo systems
- Database records
- Configuration snapshots

## Key Interview Questions

1. **What's the difference between shallow and deep copy?**
   - Shallow copies nested references; deep copies everything

2. **When would shallow copy fail?**
   - When modifying nested objects

3. **Cost of deep copy?**
   - Memory and performance overhead

4. **How to implement custom copy behavior?**
   - Override __copy__ and __deepcopy__ methods

## Important Points

- ✅ Use deep copy for complex objects with nesting
- ✅ Use shallow copy when performance matters and no nested mods
- ✅ Default assignment is just a reference
- ✅ Deep copy is safer but slower
- ✅ Use for system snapshots, undo/redo, database operations
