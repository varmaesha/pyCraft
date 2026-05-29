# Design Patterns - Observer

## Definition

**Observer Pattern** defines one-to-many relationship where multiple observers watch a subject. When subject changes, all observers are notified.

## Real-World Examples

### Example 1: Stock Price Monitoring
```python
from abc import ABC, abstractmethod

# Observer interface
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

# Subject
class Stock:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self.price = price
        self._observers = []
    
    def attach(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self):
        for observer in self._observers:
            observer.update(self)
    
    def set_price(self, new_price):
        if new_price != self.price:
            self.price = new_price
            print(f"{self.symbol}: Price changed to ${new_price}")
            self.notify()

# Concrete observers
class Investor(Observer):
    def __init__(self, name):
        self.name = name
    
    def update(self, subject: Stock):
        print(f"Investor {self.name}: {subject.symbol} is now ${subject.price}")

class Portfolio(Observer):
    def __init__(self, name):
        self.name = name
        self.stocks = {}
    
    def update(self, subject: Stock):
        self.stocks[subject.symbol] = subject.price
        print(f"Portfolio {self.name}: Updated {subject.symbol} to ${subject.price}")

# Usage
stock = Stock("AAPL", 150)

investor1 = Investor("John")
investor2 = Investor("Jane")
portfolio = Portfolio("Tech Fund")

stock.attach(investor1)
stock.attach(investor2)
stock.attach(portfolio)

# When price changes, all observers are notified
stock.set_price(155)  # All observers updated
stock.set_price(160)  # All observers updated
```

### Example 2: Event Notification System
```python
class Event:
    def __init__(self, event_type, data):
        self.event_type = event_type
        self.data = data

class EventPublisher:
    def __init__(self):
        self.subscribers = {}
    
    def subscribe(self, event_type, subscriber_callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(subscriber_callback)
    
    def unsubscribe(self, event_type, subscriber_callback):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(subscriber_callback)
    
    def publish(self, event):
        if event.event_type in self.subscribers:
            for callback in self.subscribers[event.event_type]:
                callback(event)

# Usage
publisher = EventPublisher()

def on_user_created(event):
    print(f"Email Service: Sending welcome email to {event.data['email']}")

def on_user_created_log(event):
    print(f"Logger: User {event.data['username']} created")

publisher.subscribe("user_created", on_user_created)
publisher.subscribe("user_created", on_user_created_log)

# When user is created, all subscribers are notified
event = Event("user_created", {"username": "alice", "email": "alice@example.com"})
publisher.publish(event)
```

### Example 3: MVC Pattern (Model-View-Controller)
```python
class Model:
    def __init__(self):
        self.data = None
        self.views = []
    
    def attach_view(self, view):
        self.views.append(view)
    
    def set_data(self, data):
        self.data = data
        self._notify_views()
    
    def _notify_views(self):
        for view in self.views:
            view.update(self.data)

class View:
    def __init__(self, name):
        self.name = name
    
    def update(self, data):
        print(f"View {self.name}: Display {data}")

# Usage
model = Model()
view1 = View("GraphicalView")
view2 = View("TableView")

model.attach_view(view1)
model.attach_view(view2)

model.set_data({"users": 100, "posts": 500})
# Both views updated automatically
```

### Example 4: UI Button Click Listeners
```python
class Button:
    def __init__(self, label):
        self.label = label
        self.click_listeners = []
    
    def add_click_listener(self, listener):
        self.click_listeners.append(listener)
    
    def click(self):
        print(f"Button '{self.label}' clicked")
        for listener in self.click_listeners:
            listener.on_click(self)

class ClickListener(ABC):
    @abstractmethod
    def on_click(self, button):
        pass

class SaveListener(ClickListener):
    def on_click(self, button):
        print(f"Saving data from '{button.label}' button click")

class ValidationListener(ClickListener):
    def on_click(self, button):
        print(f"Validating form for '{button.label}' button")

# Usage
button = Button("Submit")
button.add_click_listener(ValidationListener())
button.add_click_listener(SaveListener())

button.click()  # Both listeners notified
```

### Example 5: News Feed (Real-world)
```python
class NewsAgency:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
    
    def subscribe(self, channel):
        if channel not in self.subscribers:
            self.subscribers.append(channel)
            print(f"{channel.name} subscribed to {self.name}")
    
    def unsubscribe(self, channel):
        if channel in self.subscribers:
            self.subscribers.remove(channel)
            print(f"{channel.name} unsubscribed from {self.name}")
    
    def broadcast_news(self, news):
        print(f"\n{self.name} Broadcasting: {news}\n")
        for channel in self.subscribers:
            channel.receive_news(news)

class NewsChannel:
    def __init__(self, name):
        self.name = name
    
    def receive_news(self, news):
        print(f"{self.name} received: {news}")

# Usage
agency = NewsAgency("BBC News")

channel1 = NewsChannel("News Channel 1")
channel2 = NewsChannel("News Channel 2")
channel3 = NewsChannel("News Channel 3")

agency.subscribe(channel1)
agency.subscribe(channel2)
agency.subscribe(channel3)

agency.broadcast_news("Breaking News: Important event occurred!")

agency.unsubscribe(channel2)
agency.broadcast_news("Follow-up: More details released")
```

## Benefits

| Benefit | Example |
|---------|---------|
| **Loose Coupling** | Subject doesn't know observers |
| **Dynamic** | Add/remove observers at runtime |
| **Multiple Observers** | One subject, many observers |
| **Separation** | UI separate from business logic |

## Observer vs Pub/Sub

| Observer | Pub/Sub |
|----------|---------|
| Direct calls | Message broker |
| Tight coupling | Loose coupling |
| Synchronous | Usually async |
| Direct relationship | No direct relationship |

## Key Interview Questions

1. **When to use Observer Pattern?**
   - Event handling, MVC, real-time updates

2. **How is Observer different from Pub/Sub?**
   - Observer: direct notification | Pub/Sub: message broker intermediary

3. **Real-world example of Observer?**
   - Stock price updates, button click handlers, model-view patterns

4. **Potential issues with Observer?**
   - Memory leaks if observers not unsubscribed
   - Update order unpredictable

## Important Points

- ✅ Great for event-driven systems
- ✅ Enables loose coupling
- ✅ Multiple observers can react to single event
- ✅ Dynamic subscription/unsubscription
- ⚠️ Can lead to performance issues with many observers
- ⚠️ Update order is unpredictable
