# Adapter Pattern

## Definition

**Adapter Pattern**: Convert interface of one class into interface expected by client.

**Purpose**: Make incompatible interfaces work together (like real-world adapters: USB-C to USB-A).

**Key Idea**: Wrapper that translates between incompatible interfaces.

## Real-World Examples

### Example 1: Payment Gateway Integration

#### ❌ WITHOUT ADAPTER
```python
# Different payment services have different interfaces
class StripePayment:
    def charge_card(self, card_token, amount_cents):
        print(f"Charging Stripe: {amount_cents} cents")
        return {"transaction_id": "tx_123"}

class PayPalPayment:
    def pay(self, user_id, dollars):
        print(f"Charging PayPal: {dollars} dollars")
        return {"payment_id": "pp_456"}

class SquarePayment:
    def process(self, nonce, amount_dollars):
        print(f"Charging Square: {amount_dollars} dollars")
        return {"charge": {"id": "sq_789"}}

# Client code has to know all interfaces
class CheckoutService:
    def checkout(self, payment_type, payment_data, amount):
        if payment_type == "stripe":
            return StripePayment().charge_card(payment_data, amount * 100)
        elif payment_type == "paypal":
            return PayPalPayment().pay(payment_data, amount)
        elif payment_type == "square":
            return SquarePayment().process(payment_data, amount)

# Problem: Client code gets complex
```

#### ✅ WITH ADAPTER
```python
# Define standard interface
class PaymentAdapter:
    def pay(self, amount_dollars):
        pass

# Adapt different services to standard interface
class StripeAdapter(PaymentAdapter):
    def __init__(self, card_token):
        self.stripe = StripePayment()
        self.card_token = card_token
    
    def pay(self, amount_dollars):
        # Adapt: convert dollars to cents, adapt method name
        result = self.stripe.charge_card(self.card_token, amount_dollars * 100)
        return {"success": True, "transaction_id": result["transaction_id"]}

class PayPalAdapter(PaymentAdapter):
    def __init__(self, user_id):
        self.paypal = PayPalPayment()
        self.user_id = user_id
    
    def pay(self, amount_dollars):
        # Adapt: method name, parameters
        result = self.paypal.pay(self.user_id, amount_dollars)
        return {"success": True, "transaction_id": result["payment_id"]}

class SquareAdapter(PaymentAdapter):
    def __init__(self, nonce):
        self.square = SquarePayment()
        self.nonce = nonce
    
    def pay(self, amount_dollars):
        # Adapt: method name, parameters
        result = self.square.process(self.nonce, amount_dollars)
        return {"success": True, "transaction_id": result["charge"]["id"]}

# Client code is clean
class CheckoutService:
    def checkout(self, payment_adapter: PaymentAdapter, amount):
        return payment_adapter.pay(amount)

# Usage
checkout = CheckoutService()
checkout.checkout(StripeAdapter("tok_123"), 99.99)
checkout.checkout(PayPalAdapter("user_456"), 99.99)
checkout.checkout(SquareAdapter("nonce_789"), 99.99)

# Easy to add new payment services
```

### Example 2: Logger Integration

#### ✅ WITH ADAPTER
```python
# Different logging libraries
class PythonLogger:
    def info(self, msg):
        print(f"[INFO] {msg}")
    
    def error(self, msg):
        print(f"[ERROR] {msg}")

class Log4J:
    def log_info(self, message):
        print(f"LOG4J_INFO: {message}")
    
    def log_error(self, message):
        print(f"LOG4J_ERROR: {message}")

class Loguru:
    def debug(self, text):
        print(f"DEBUG | {text}")
    
    def exception(self, text):
        print(f"EXCEPTION | {text}")

# Standard interface
class Logger:
    def info(self, message):
        pass
    
    def error(self, message):
        pass

# Adapters
class PythonLoggerAdapter(Logger):
    def __init__(self):
        self.logger = PythonLogger()
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message):
        self.logger.error(message)

class Log4JAdapter(Logger):
    def __init__(self):
        self.logger = Log4J()
    
    def info(self, message):
        self.logger.log_info(message)
    
    def error(self, message):
        self.logger.log_error(message)

class LlogeruAdapter(Logger):
    def __init__(self):
        self.logger = Loguru()
    
    def info(self, message):
        self.logger.debug(message)
    
    def error(self, message):
        self.logger.exception(message)

# Application uses standard interface
class Application:
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def run(self):
        self.logger.info("Starting application")
        try:
            self.logger.info("Processing")
        except Exception:
            self.logger.error("Error occurred")

# Easy to switch loggers
app1 = Application(PythonLoggerAdapter())
app1.run()

app2 = Application(Log4JAdapter())
app2.run()

app3 = Application(LlogeruAdapter())
app3.run()
```

### Example 3: Database Integration

#### ✅ WITH ADAPTER
```python
# Different database drivers
class MySQLDriver:
    def connect(self, host, user, password):
        return MySQLConnection(host, user, password)
    
    def execute_query(self, query):
        return self.connection.execute(query)

class PostgreSQLDriver:
    def db_connect(self, server, username, pwd):
        return PostgreSQLConnection(server, username, pwd)

class MongoDBDriver:
    def mongo_connect(self, url):
        return MongoDBConnection(url)

# Standard interface
class DatabaseAdapter:
    def connect(self, config):
        pass
    
    def execute(self, query):
        pass

# Adapters
class MySQLAdapter(DatabaseAdapter):
    def __init__(self):
        self.driver = MySQLDriver()
        self.connection = None
    
    def connect(self, config):
        self.connection = self.driver.connect(
            config["host"],
            config["user"],
            config["password"]
        )
    
    def execute(self, query):
        return self.driver.execute_query(query)

class PostgreSQLAdapter(DatabaseAdapter):
    def __init__(self):
        self.driver = PostgreSQLDriver()
        self.connection = None
    
    def connect(self, config):
        self.connection = self.driver.db_connect(
            config["host"],
            config["user"],
            config["password"]
        )
    
    def execute(self, query):
        return self.connection.execute(query)

class MongoAdapter(DatabaseAdapter):
    def __init__(self):
        self.driver = MongoDBDriver()
        self.connection = None
    
    def connect(self, config):
        self.connection = self.driver.mongo_connect(config["url"])
    
    def execute(self, query):
        return self.connection.find(query)

# Application
class DataStore:
    def __init__(self, db: DatabaseAdapter):
        self.db = db
    
    def save_user(self, user):
        self.db.execute(f"INSERT INTO users VALUES {user}")
    
    def find_user(self, user_id):
        return self.db.execute(f"SELECT * FROM users WHERE id={user_id}")

# Usage
config = {"host": "localhost", "user": "root", "password": "pass"}
store = DataStore(MySQLAdapter())
store.db.connect(config)
store.save_user(("John", "john@example.com"))

# Switch to PostgreSQL
store = DataStore(PostgreSQLAdapter())
store.db.connect(config)
store.save_user(("Jane", "jane@example.com"))
```

### Example 4: Format Conversion

#### ✅ WITH ADAPTER
```python
# Different data providers
class CSVReader:
    def read_csv(self, filename):
        return [["col1", "col2"], ["data1", "data2"]]

class JSONReader:
    def load_json(self, filename):
        return {"data": [{"col1": "data1", "col2": "data2"}]}

class XMLReader:
    def parse_xml(self, filename):
        return "<root><row><col1>data1</col1></row></root>"

# Standard interface
class DataAdapter:
    def read(self, source):
        pass

# Adapters
class CSVAdapter(DataAdapter):
    def __init__(self):
        self.reader = CSVReader()
    
    def read(self, source):
        return self.reader.read_csv(source)

class JSONAdapter(DataAdapter):
    def __init__(self):
        self.reader = JSONReader()
    
    def read(self, source):
        return self.reader.load_json(source)

class XMLAdapter(DataAdapter):
    def __init__(self):
        self.reader = XMLReader()
    
    def read(self, source):
        return self.reader.parse_xml(source)

# Application
class DataProcessor:
    def __init__(self, adapter: DataAdapter):
        self.adapter = adapter
    
    def process(self, source):
        data = self.adapter.read(source)
        return f"Processing: {data}"

# Easy to switch formats
processor = DataProcessor(CSVAdapter())
print(processor.process("data.csv"))

processor = DataProcessor(JSONAdapter())
print(processor.process("data.json"))

processor = DataProcessor(XMLAdapter())
print(processor.process("data.xml"))
```

## When to Use Adapter

- **Different interfaces**: Multiple libraries with different APIs
- **Legacy code**: Integrate old code with new
- **Third-party APIs**: Wrap external services
- **Testing**: Adapt real services to mock interfaces
- **Multiple implementations**: Support different backends

## Adapter vs Decorator

| Aspect | Adapter | Decorator |
|--------|---------|-----------|
| **Purpose** | Fix interface mismatch | Add behavior |
| **Use Case** | Incompatible interfaces | Same interface, new features |
| **Modifies** | Interface | Functionality |
| **Structure** | Wraps incompatible class | Wraps same interface |

## Key Interview Questions

1. **What problem does Adapter solve?**
   - Makes incompatible interfaces work together

2. **Real-world example?**
   - Payment gateways, logger libraries, database drivers

3. **Adapter vs Decorator?**
   - Adapter: Interface mismatch, Decorator: Add behavior

4. **Two types of adapters?**
   - Class Adapter (inheritance), Object Adapter (composition)

## Important Points

- ✅ Use to fix interface mismatches
- ✅ Wrap incompatible classes
- ✅ Keep client code clean
- ✅ Single Responsibility
- ✅ Test adapters thoroughly
- ⚠️ Don't overuse (indicates design problems)
- ✅ Useful for third-party integration
