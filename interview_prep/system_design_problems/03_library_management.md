# Designing System: Library Management

## Requirements

### Functional Requirements
1. Add/remove books and members
2. Check book availability
3. Borrow books (max 5 books per member)
4. Return books
5. Track due dates and fines
6. Search books by title/author/ISBN
7. View member history
8. Manage book reservations

### Non-Functional Requirements
1. Real-time availability
2. Quick book search
3. Member authentication
4. Data persistence
5. Handle concurrent operations

## System Design

### 1. Book Management
```python
from enum import Enum
from datetime import datetime, timedelta

class BookStatus(Enum):
    AVAILABLE = 1
    BORROWED = 2
    RESERVED = 3

class Book:
    def __init__(self, isbn, title, author, publisher, quantity=1):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.total_quantity = quantity
        self.available_quantity = quantity
        self.copies = {}  # copy_id -> BookCopy
        self._create_copies()
    
    def _create_copies(self):
        for i in range(1, self.total_quantity + 1):
            copy_id = f"{self.isbn}-{i}"
            self.copies[copy_id] = BookCopy(copy_id, BookStatus.AVAILABLE)
    
    def get_available_count(self):
        return sum(1 for copy in self.copies.values() 
                   if copy.status == BookStatus.AVAILABLE)
    
    def is_available(self):
        return self.get_available_count() > 0
    
    def get_available_copy(self):
        for copy in self.copies.values():
            if copy.status == BookStatus.AVAILABLE:
                return copy
        return None
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

class BookCopy:
    def __init__(self, copy_id, status):
        self.copy_id = copy_id
        self.status = status
        self.borrowed_by = None
        self.borrow_date = None
    
    def mark_borrowed(self, member_id):
        self.status = BookStatus.BORROWED
        self.borrowed_by = member_id
        self.borrow_date = datetime.now()
    
    def mark_returned(self):
        self.status = BookStatus.AVAILABLE
        self.borrowed_by = None
        self.borrow_date = None
```

### 2. Member Management
```python
class Member:
    def __init__(self, member_id, name, email, phone):
        self.member_id = member_id
        self.name = name
        self.email = email
        self.phone = phone
        self.borrowed_books = []  # List of Borrowing records
        self.fines = 0.0
        self.max_borrow = 5
        self.registration_date = datetime.now()
    
    def can_borrow(self):
        return len(self.borrowed_books) < self.max_borrow
    
    def borrow_book(self, book_copy):
        if not self.can_borrow():
            raise Exception("Maximum borrow limit reached")
        
        borrowing = Borrowing(self.member_id, book_copy.copy_id, book_copy)
        self.borrowed_books.append(borrowing)
        book_copy.mark_borrowed(self.member_id)
        return borrowing
    
    def return_book(self, copy_id):
        for i, borrowing in enumerate(self.borrowed_books):
            if borrowing.copy_id == copy_id:
                book_copy = borrowing.book_copy
                days_overdue = borrowing.calculate_overdue_days()
                
                if days_overdue > 0:
                    fine = days_overdue * 1.0  # $1 per day
                    self.fines += fine
                    borrowing.set_fine(fine)
                
                borrowing.return_date = datetime.now()
                book_copy.mark_returned()
                self.borrowed_books.pop(i)
                return borrowing
        
        raise Exception(f"Book copy {copy_id} not borrowed by this member")
    
    def pay_fine(self, amount):
        if amount > self.fines:
            raise Exception("Amount exceeds total fines")
        self.fines -= amount
    
    def get_borrowed_books(self):
        return self.borrowed_books
    
    def __str__(self):
        return f"Member({self.name}, ID: {self.member_id})"

class Borrowing:
    def __init__(self, member_id, copy_id, book_copy):
        self.member_id = member_id
        self.copy_id = copy_id
        self.book_copy = book_copy
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=14)  # 2 weeks
        self.return_date = None
        self.fine = 0.0
    
    def is_overdue(self):
        return datetime.now() > self.due_date and not self.return_date
    
    def calculate_overdue_days(self):
        if self.return_date:
            end_date = self.return_date
        else:
            end_date = datetime.now()
        
        if end_date <= self.due_date:
            return 0
        
        return (end_date - self.due_date).days
    
    def set_fine(self, amount):
        self.fine = amount
    
    def get_days_remaining(self):
        days = (self.due_date - datetime.now()).days
        return max(0, days)
```

### 3. Library Management System
```python
class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}  # isbn -> Book
        self.members = {}  # member_id -> Member
        self.reservations = []  # List of reservations
    
    def add_book(self, isbn, title, author, publisher, quantity=1):
        if isbn in self.books:
            self.books[isbn].total_quantity += quantity
            for i in range(quantity):
                copy_id = f"{isbn}-{self.books[isbn].total_quantity - quantity + i + 1}"
                self.books[isbn].copies[copy_id] = BookCopy(copy_id, BookStatus.AVAILABLE)
        else:
            self.books[isbn] = Book(isbn, title, author, publisher, quantity)
        return self.books[isbn]
    
    def remove_book(self, isbn):
        if isbn in self.books:
            del self.books[isbn]
    
    def register_member(self, name, email, phone):
        member_id = f"MEM{len(self.members) + 1:04d}"
        member = Member(member_id, name, email, phone)
        self.members[member_id] = member
        return member
    
    def search_books_by_title(self, title):
        return [book for book in self.books.values() 
                if title.lower() in book.title.lower()]
    
    def search_books_by_author(self, author):
        return [book for book in self.books.values() 
                if author.lower() in book.author.lower()]
    
    def borrow_book(self, member_id, isbn):
        if member_id not in self.members:
            raise Exception("Invalid member ID")
        if isbn not in self.books:
            raise Exception("Book not found")
        
        member = self.members[member_id]
        book = self.books[isbn]
        
        if not book.is_available():
            raise Exception(f"{book.title} is not available")
        
        copy = book.get_available_copy()
        borrowing = member.borrow_book(copy)
        return borrowing
    
    def return_book(self, member_id, copy_id):
        if member_id not in self.members:
            raise Exception("Invalid member ID")
        
        member = self.members[member_id]
        borrowing = member.return_book(copy_id)
        return borrowing
    
    def get_overdue_books(self):
        overdue = []
        for member in self.members.values():
            for borrowing in member.borrowed_books:
                if borrowing.is_overdue():
                    overdue.append({
                        "member": member.name,
                        "book": borrowing.book_copy.copy_id,
                        "days_overdue": borrowing.calculate_overdue_days()
                    })
        return overdue
    
    def get_member_summary(self, member_id):
        if member_id not in self.members:
            raise Exception("Invalid member ID")
        
        member = self.members[member_id]
        return {
            "name": member.name,
            "books_borrowed": len(member.borrowed_books),
            "outstanding_fines": member.fines,
            "borrowed_books": [
                {
                    "title": b.book_copy.copy_id,
                    "due_date": b.due_date.date(),
                    "days_remaining": b.get_days_remaining()
                }
                for b in member.borrowed_books
            ]
        }
    
    def reserve_book(self, member_id, isbn):
        if isbn not in self.books:
            raise Exception("Book not found")
        
        book = self.books[isbn]
        if book.is_available():
            raise Exception("Book is available, no need to reserve")
        
        reservation = Reservation(member_id, isbn)
        self.reservations.append(reservation)
        return reservation
    
    def get_library_status(self):
        return {
            "total_members": len(self.members),
            "total_books": sum(b.total_quantity for b in self.books.values()),
            "available_books": sum(b.get_available_count() for b in self.books.values()),
            "borrowed_books": sum(len(m.borrowed_books) for m in self.members.values())
        }

class Reservation:
    def __init__(self, member_id, isbn):
        self.member_id = member_id
        self.isbn = isbn
        self.reservation_date = datetime.now()
```

## Usage Example

```python
# Setup library
library = Library("Central Library")

# Add books
library.add_book("978-0134685991", "Effective Java", "Joshua Bloch", "Addison-Wesley", 3)
library.add_book("978-0201633610", "Design Patterns", "Gang of Four", "Addison-Wesley", 2)
library.add_book("978-0132350884", "Clean Code", "Robert Martin", "Prentice Hall", 2)

# Register members
alice = library.register_member("Alice", "alice@example.com", "555-0001")
bob = library.register_member("Bob", "bob@example.com", "555-0002")

# Borrow books
print("=== BORROWING ===")
borrow1 = library.borrow_book(alice.member_id, "978-0134685991")
print(f"Alice borrowed {borrow1.book_copy.copy_id}, due: {borrow1.due_date.date()}")

borrow2 = library.borrow_book(bob.member_id, "978-0201633610")
print(f"Bob borrowed {borrow2.book_copy.copy_id}, due: {borrow2.due_date.date()}")

# Search books
print("\n=== SEARCH ===")
design_books = library.search_books_by_title("Design")
print(f"Found {len(design_books)} books about Design")

# Member summary
print("\n=== MEMBER SUMMARY ===")
print(library.get_member_summary(alice.member_id))

# Library status
print("\n=== LIBRARY STATUS ===")
print(library.get_library_status())

# Return books
print("\n=== RETURN BOOKS ===")
return1 = library.return_book(alice.member_id, borrow1.copy_id)
print(f"Alice returned book, fine: ${return1.fine}")

# Overdue books
print("\n=== OVERDUE BOOKS ===")
overdue = library.get_overdue_books()
print(f"Overdue books: {overdue}")
```

## Key Design Patterns Used

1. **Singleton**: Library instance
2. **Factory**: Creating books, members
3. **Repository**: Book and member storage
4. **State**: Book status (AVAILABLE, BORROWED, RESERVED)

## Scalability Considerations

1. **Database**: Store books, members, borrowings, reservations
2. **Indexing**: Fast search by title, author, ISBN
3. **Caching**: Cache available books count
4. **Notifications**: Email reminders for due dates
5. **Transaction Log**: Audit trail of all operations
