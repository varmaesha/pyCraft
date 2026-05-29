# Design Patterns - Builder

## Definition

**Builder Pattern** constructs complex objects step-by-step, separating construction from representation.

## Use Cases

1. Complex objects with many optional parameters
2. Immutable objects
3. Large configuration objects
4. Objects with fluent interface

## Real-World Examples

### Example 1: Pizza Builder (Classic Example)
```python
class Pizza:
    def __init__(self, builder):
        self.size = builder.size
        self.crust = builder.crust
        self.cheese = builder.cheese
        self.toppings = builder.toppings
        self.sauce = builder.sauce
    
    def __str__(self):
        return f"Pizza({self.size}, {self.crust}, {self.sauce}, {self.toppings})"

class PizzaBuilder:
    def __init__(self):
        self.size = None
        self.crust = None
        self.cheese = False
        self.toppings = []
        self.sauce = None
    
    def set_size(self, size):
        self.size = size
        return self
    
    def set_crust(self, crust):
        self.crust = crust
        return self
    
    def add_cheese(self):
        self.cheese = True
        return self
    
    def add_topping(self, topping):
        self.toppings.append(topping)
        return self
    
    def set_sauce(self, sauce):
        self.sauce = sauce
        return self
    
    def build(self):
        return Pizza(self)

# Usage - Fluent Interface
pizza = (PizzaBuilder()
    .set_size("Large")
    .set_crust("Thin")
    .add_cheese()
    .add_topping("Pepperoni")
    .add_topping("Mushrooms")
    .set_sauce("Tomato")
    .build())

print(pizza)
```

### Example 2: SQL Query Builder
```python
class SQLQuery:
    def __init__(self, builder):
        self.select = builder.select
        self.from_table = builder.from_table
        self.where = builder.where
        self.joins = builder.joins
        self.order_by = builder.order_by
    
    def __str__(self):
        query = f"SELECT {self.select} FROM {self.from_table}"
        if self.joins:
            query += " " + " ".join(self.joins)
        if self.where:
            query += f" WHERE {self.where}"
        if self.order_by:
            query += f" ORDER BY {self.order_by}"
        return query

class SQLQueryBuilder:
    def __init__(self):
        self.select = "*"
        self.from_table = None
        self.where = None
        self.joins = []
        self.order_by = None
    
    def select_columns(self, *columns):
        self.select = ", ".join(columns)
        return self
    
    def from_table(self, table):
        self.from_table = table
        return self
    
    def where(self, condition):
        self.where = condition
        return self
    
    def join(self, join_query):
        self.joins.append(join_query)
        return self
    
    def order_by(self, column):
        self.order_by = column
        return self
    
    def build(self):
        return SQLQuery(self)

# Usage
query = (SQLQueryBuilder()
    .select_columns("id", "name", "email")
    .from_table("users")
    .where("age > 18")
    .order_by("name")
    .build())

print(query)
# Output: SELECT id, name, email FROM users WHERE age > 18 ORDER BY name
```

### Example 3: HTTP Request Builder
```python
class HTTPRequest:
    def __init__(self, builder):
        self.method = builder.method
        self.url = builder.url
        self.headers = builder.headers
        self.body = builder.body
        self.params = builder.params
    
    def __str__(self):
        return f"{self.method} {self.url}"

class HTTPRequestBuilder:
    def __init__(self, url):
        self.url = url
        self.method = "GET"
        self.headers = {}
        self.body = None
        self.params = {}
    
    def set_method(self, method):
        self.method = method
        return self
    
    def add_header(self, key, value):
        self.headers[key] = value
        return self
    
    def set_body(self, body):
        self.body = body
        return self
    
    def add_param(self, key, value):
        self.params[key] = value
        return self
    
    def build(self):
        return HTTPRequest(self)

# Usage
request = (HTTPRequestBuilder("https://api.example.com/users")
    .set_method("POST")
    .add_header("Content-Type", "application/json")
    .add_header("Authorization", "Bearer token123")
    .set_body('{"name": "John"}')
    .build())

print(f"Method: {request.method}")
print(f"URL: {request.url}")
print(f"Headers: {request.headers}")
```

### Example 4: Configuration Builder
```python
class AppConfig:
    def __init__(self, builder):
        self.app_name = builder.app_name
        self.debug = builder.debug
        self.port = builder.port
        self.database_url = builder.database_url
        self.cache_enabled = builder.cache_enabled
        self.log_level = builder.log_level
    
    def __str__(self):
        return f"AppConfig(name={self.app_name}, debug={self.debug}, port={self.port})"

class AppConfigBuilder:
    def __init__(self, app_name):
        self.app_name = app_name
        self.debug = False
        self.port = 8000
        self.database_url = None
        self.cache_enabled = False
        self.log_level = "INFO"
    
    def set_debug(self, debug):
        self.debug = debug
        return self
    
    def set_port(self, port):
        self.port = port
        return self
    
    def set_database(self, db_url):
        self.database_url = db_url
        return self
    
    def enable_cache(self):
        self.cache_enabled = True
        return self
    
    def set_log_level(self, level):
        self.log_level = level
        return self
    
    def build(self):
        if not self.database_url:
            raise ValueError("Database URL is required")
        return AppConfig(self)

# Usage
config = (AppConfigBuilder("MyApp")
    .set_debug(True)
    .set_port(3000)
    .set_database("postgresql://localhost:5432/myapp")
    .enable_cache()
    .set_log_level("DEBUG")
    .build())

print(config)
```

### Example 5: Real-world: E-commerce Product
```python
class Product:
    def __init__(self, builder):
        self.id = builder.id
        self.name = builder.name
        self.price = builder.price
        self.description = builder.description
        self.images = builder.images
        self.tags = builder.tags
        self.variants = builder.variants

class ProductBuilder:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price
        self.description = ""
        self.images = []
        self.tags = []
        self.variants = []
    
    def set_description(self, description):
        self.description = description
        return self
    
    def add_image(self, url):
        self.images.append(url)
        return self
    
    def add_tag(self, tag):
        self.tags.append(tag)
        return self
    
    def add_variant(self, size, color, stock):
        self.variants.append({"size": size, "color": color, "stock": stock})
        return self
    
    def build(self):
        return Product(self)

# Usage
product = (ProductBuilder("P001", "T-Shirt", 29.99)
    .set_description("High-quality cotton t-shirt")
    .add_image("image1.jpg")
    .add_image("image2.jpg")
    .add_tag("clothing")
    .add_tag("summer")
    .add_variant("S", "Black", 10)
    .add_variant("M", "Black", 15)
    .add_variant("L", "White", 8)
    .build())

print(f"Product: {product.name}")
print(f"Price: ${product.price}")
print(f"Variants: {product.variants}")
```

## Benefits

| Benefit | Example |
|---------|---------|
| **Readability** | Fluent interface is clear |
| **Flexibility** | Optional parameters easy |
| **Immutability** | Final objects can be immutable |
| **Step-by-step** | Complex construction made simple |

## Key Interview Questions

1. **When to use Builder Pattern?**
   - Complex objects with many optional parameters

2. **What's Fluent Interface?**
   - Methods return `self` to enable method chaining

3. **Builder vs Factory?**
   - Builder: Step-by-step construction | Factory: One-step creation

## Important Points

- ✅ Great for complex objects
- ✅ Makes code readable and maintainable
- ✅ Enables fluent API
- ✅ Supports immlutability
- ❌ Overkill for simple objects
