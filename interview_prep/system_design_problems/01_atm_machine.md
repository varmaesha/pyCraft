# Designing System: ATM Machine

## Requirements

### Functional Requirements
1. User authentication (PIN)
2. Check balance
3. Withdraw cash
4. Deposit cash
5. Change PIN
6. Transfer money
7. Print receipt

### Non-Functional Requirements
1. Security (encryption)
2. Availability (24/7)
3. Consistency (transactions)
4. Scalability
5. Low latency

## High-Level Architecture

```
ATM Terminal
    ↓
Transaction Manager
    ↓
┌───────────────┬──────────────┬─────────────┐
│   Account     │   Card       │   Cash      │
│   Manager     │   Manager    │   Manager   │
└───────────────┴──────────────┴─────────────┘
    ↓               ↓               ↓
┌────────────────────────────────────────────┐
│           Database Layer                   │
│   (Accounts, Transactions, Audit Log)      │
└────────────────────────────────────────────┘
```

## Detailed Design

### 1. Card and User Authentication
```python
class Card:
    def __init__(self, card_number, pin):
        self.card_number = card_number
        self.pin = self._hash_pin(pin)
        self.is_blocked = False
    
    def _hash_pin(self, pin):
        return f"hashed_{pin}"
    
    def verify_pin(self, pin):
        if self.is_blocked:
            raise Exception("Card is blocked")
        return self.pin == self._hash_pin(pin)

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.accounts = []
```

### 2. Account Management
```python
class Account:
    def __init__(self, account_id, owner, balance=0):
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.transaction_history = []
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise Exception("Insufficient funds")
        if amount <= 0:
            raise Exception("Invalid amount")
        self.balance -= amount
        self._record_transaction("WITHDRAW", amount)
        return self.balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise Exception("Invalid amount")
        self.balance += amount
        self._record_transaction("DEPOSIT", amount)
        return self.balance
    
    def _record_transaction(self, transaction_type, amount):
        self.transaction_history.append({
            "type": transaction_type,
            "amount": amount,
            "timestamp": self._get_timestamp(),
            "balance": self.balance
        })
    
    def get_balance(self):
        return self.balance
    
    def get_statement(self, num_transactions=10):
        return self.transaction_history[-num_transactions:]
    
    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now()
```

### 3. ATM Machine
```python
class ATM:
    def __init__(self, machine_id, location, cash_capacity=100000):
        self.machine_id = machine_id
        self.location = location
        self.cash = cash_capacity
        self.total_transactions = 0
    
    def check_cash_availability(self, amount):
        return self.cash >= amount
    
    def dispense_cash(self, amount):
        if not self.check_cash_availability(amount):
            raise Exception("ATM: Insufficient cash")
        self.cash -= amount
        return amount
    
    def accept_cash(self, amount):
        self.cash += amount
    
    def get_status(self):
        return {
            "machine_id": self.machine_id,
            "location": self.location,
            "cash_available": self.cash,
            "total_transactions": self.total_transactions
        }
```

### 4. Transaction Manager
```python
class TransactionManager:
    def __init__(self, db):
        self.db = db
    
    def process_withdrawal(self, account, amount, atm):
        try:
            # Check cash availability
            if not atm.check_cash_availability(amount):
                raise Exception("ATM: Insufficient cash")
            
            # Update account
            account.withdraw(amount)
            
            # Dispense cash
            atm.dispense_cash(amount)
            
            # Log transaction
            self.db.save_transaction({
                "type": "WITHDRAW",
                "account_id": account.account_id,
                "amount": amount,
                "atm_id": atm.machine_id,
                "status": "SUCCESS"
            })
            
            return {
                "status": "SUCCESS",
                "message": f"Withdrew ${amount}",
                "balance": account.balance
            }
        
        except Exception as e:
            self.db.save_transaction({
                "type": "WITHDRAW",
                "account_id": account.account_id,
                "amount": amount,
                "status": "FAILED",
                "error": str(e)
            })
            raise
    
    def process_deposit(self, account, amount, atm):
        try:
            account.deposit(amount)
            atm.accept_cash(amount)
            
            self.db.save_transaction({
                "type": "DEPOSIT",
                "account_id": account.account_id,
                "amount": amount,
                "atm_id": atm.machine_id,
                "status": "SUCCESS"
            })
            
            return {
                "status": "SUCCESS",
                "message": f"Deposited ${amount}",
                "balance": account.balance
            }
        
        except Exception as e:
            self.db.save_transaction({
                "type": "DEPOSIT",
                "account_id": account.account_id,
                "amount": amount,
                "status": "FAILED",
                "error": str(e)
            })
            raise
```

### 5. ATM Session/State Machine
```python
class ATMSession:
    def __init__(self, atm, card_reader, bank_service):
        self.atm = atm
        self.card_reader = card_reader
        self.bank_service = bank_service
        self.current_user = None
        self.current_account = None
        self.state = "IDLE"  # IDLE, CARD_INSERTED, AUTHENTICATED
    
    def insert_card(self, card):
        self.state = "CARD_INSERTED"
        self.card_reader.read_card(card)
    
    def authenticate(self, pin):
        try:
            card = self.card_reader.get_card()
            if card.verify_pin(pin):
                self.current_user = self.bank_service.get_user_by_card(card)
                self.current_account = self.current_user.accounts[0]  # Primary account
                self.state = "AUTHENTICATED"
                return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False
    
    def check_balance(self):
        if self.state != "AUTHENTICATED":
            raise Exception("Not authenticated")
        return self.current_account.get_balance()
    
    def withdraw(self, amount):
        if self.state != "AUTHENTICATED":
            raise Exception("Not authenticated")
        
        transaction_mgr = TransactionManager(self.bank_service.db)
        result = transaction_mgr.process_withdrawal(
            self.current_account,
            amount,
            self.atm
        )
        return result
    
    def deposit(self, amount):
        if self.state != "AUTHENTICATED":
            raise Exception("Not authenticated")
        
        transaction_mgr = TransactionManager(self.bank_service.db)
        result = transaction_mgr.process_deposit(
            self.current_account,
            amount,
            self.atm
        )
        return result
    
    def end_session(self):
        self.current_user = None
        self.current_account = None
        self.state = "IDLE"
```

## Usage Example

```python
# Setup
bank_service = BankService()
atm = ATM("ATM001", "Main Street")
session = ATMSession(atm, CardReader(), bank_service)

# User interaction
card = Card("4111111111111111", "1234")
session.insert_card(card)

if session.authenticate("1234"):
    print(f"Balance: ${session.check_balance()}")
    
    try:
        result = session.withdraw(100)
        print(result)  # Withdrew $100
    except Exception as e:
        print(f"Withdrawal failed: {e}")
    
    session.end_session()
```

## Key Design Patterns Used

1. **State Pattern**: ATM session states
2. **Singleton**: Bank service, database
3. **Factory**: Creating accounts, transactions
4. **Repository**: Database access

## Security Considerations

1. **Encryption**: PIN hashing, data encryption
2. **Rate limiting**: Failed attempts limit
3. **Audit logging**: All transactions logged
4. **Card blocking**: Auto-block after failed attempts
5. **Session timeout**: Automatic logout

## Potential Extensions

1. Transfer to other accounts
2. Change PIN
3. Card blocking/unblocking
4. Multi-currency support
5. Bill payment
