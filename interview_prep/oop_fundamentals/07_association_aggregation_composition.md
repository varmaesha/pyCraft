# Association, Aggregation, and Composition

## Definitions

### Association (HAS-A relationship)
Two objects have relationship but can exist independently. **Weakest** coupling.

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.courses = []  # Association - student HAS courses
    
    def enroll_course(self, course):
        self.courses.append(course)

class Course:
    def __init__(self, name):
        self.name = name

# Student and Course are independent
student = Student("Alice")
course = Course("Python 101")
student.enroll_course(course)

# If student is deleted, course still exists
del student
# course still exists!
```

### Aggregation (Weak HAS-A relationship)
Part-Whole relationship. **Weak** ownership. Parts can exist without whole.

```python
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []  # Aggregation - Department HAS employees
    
    def add_employee(self, employee):
        self.employees.append(employee)

class Employee:
    def __init__(self, name):
        self.name = name

# Employees exist before and after department
emp1 = Employee("John")
emp2 = Employee("Jane")

dept = Department("Engineering")
dept.add_employee(emp1)
dept.add_employee(emp2)

# If department is deleted, employees still exist
del dept
print(emp1.name)  # Still accessible!
```

### Composition (Strong HAS-A relationship)
Part-Whole relationship. **Strong** ownership. Parts **cannot** exist without whole.

```python
class House:
    def __init__(self):
        self.roof = Roof()        # House OWNS roof
        self.walls = [Wall(), Wall(), Wall()]  # House OWNS walls
        self.door = Door()        # House OWNS door

class Roof:
    pass

class Wall:
    pass

class Door:
    pass

# Roof, walls, door don't exist without house
house = House()

# If house is deleted, all parts are deleted
del house
# roof, walls, door are garbage collected
```

## Real-World Examples

### Example 1: University System
```python
# Association
class Student:
    def __init__(self, name):
        self.name = name
        self.professors = []  # Association - independent
    
    def take_course_from(self, professor):
        self.professors.append(professor)

class Professor:
    def __init__(self, name):
        self.name = name

# Aggregation
class Department:
    def __init__(self, name):
        self.name = name
        self.employees = []  # Aggregation - employees can exist without dept
    
    def hire_employee(self, employee):
        self.employees.append(employee)

employee1 = Employee("Dr. Smith")
employee2 = Employee("Dr. Jones")

dept = Department("Computer Science")
dept.hire_employee(employee1)
dept.hire_employee(employee2)

# Composition
class University:
    def __init__(self, name):
        self.name = name
        self.departments = [Department("CS"), Department("Physics")]  # Owned
        self.library = Library()  # Owned

class Library:
    def __init__(self):
        self.books = []

# When university is deleted, departments and library are deleted
```

### Example 2: Car System
```python
# Association
class Car:
    def __init__(self, model):
        self.model = model
        self.owners = []  # Association - owners are independent
    
    def add_owner(self, owner):
        self.owners.append(owner)

class Person:
    def __init__(self, name):
        self.name = name

# Aggregation
class Company:
    def __init__(self, name):
        self.name = name
        self.cars = []  # Aggregation - cars can be sold
    
    def buy_car(self, car):
        self.cars.append(car)

company = Company("Uber")
car1 = Car("Toyota")
car2 = Car("Honda")
company.buy_car(car1)
company.buy_car(car2)

# If company goes out of business, cars still exist
del company
print(car1.model)  # Still accessible

# Composition
class Engine:
    def start(self):
        return "Engine started"

class Tire:
    def __init__(self):
        self.pressure = 32

class Vehicle:
    def __init__(self):
        self.engine = Engine()  # OWNS - cannot exist without vehicle
        self.tires = [Tire() for _ in range(4)]  # OWNS

# Engine and Tires don't exist without vehicle
vehicle = Vehicle()
del vehicle
# engine and tires are deleted too
```

### Example 3: Company Structure
```python
# Composition - strict ownership
class Company:
    def __init__(self, name):
        self.name = name
        self.departments = {}  # Owns departments
        self.ceo = None

    def add_department(self, dept_name, manager):
        self.departments[dept_name] = Department(dept_name, manager)

class Department:
    def __init__(self, name, manager):
        self.name = name
        self.manager = manager
        self.teams = []  # Owns teams

    def add_team(self, team):
        self.teams.append(team)

class Team:
    def __init__(self, name):
        self.name = name
        self.members = []  # Aggregation - members can transfer

    def add_member(self, member):
        self.members.append(member)

class Employee:
    def __init__(self, name):
        self.name = name

# Setup hierarchy
company = Company("TechCorp")
engineer1 = Employee("Alice")
engineer2 = Employee("Bob")

dept = Department("Engineering", Employee("Carol"))
team = Team("Backend")
team.add_member(engineer1)
team.add_member(engineer2)
dept.add_team(team)
company.add_department("Engineering", dept)

# Aggregation: Employees can move to different teams
# Composition: Teams cannot exist without department
# Company owns everything
```

## Comparison Table

| Aspect | Association | Aggregation | Composition |
|--------|-------------|-------------|------------|
| **Relationship** | HAS-A (weak) | HAS-A (weak) | HAS-A (strong) |
| **Ownership** | None | Shared | Exclusive |
| **Lifetime** | Independent | Independent | Dependent |
| **Multiplicity** | One-to-Many | One-to-Many | One-to-Many |
| **Deletion** | Independent | Independent | Cascading |
| **Example** | Student-Course | Company-Car | House-Roof |

## UML Notation

```
Association: ─────────────  (line)
Aggregation: ◇─────────────  (hollow diamond)
Composition: ◆─────────────  (filled diamond)
```

## Key Interview Questions

1. **What's the difference between association and aggregation?**
   - Association: No ownership | Aggregation: Shared ownership

2. **When does composition differ from aggregation?**
   - Composition: Parts cannot exist without whole

3. **Example of each from real world?**
   - Association: Student-Professor
   - Aggregation: Company-Employee
   - Composition: Car-Engine

4. **Can aggregation have cycles?**
   - Yes, but composition cannot (would create circular dependency)

## Important Points

- ✅ Use association for independent relationships
- ✅ Use aggregation for shared ownership
- ✅ Use composition for exclusive ownership (most common in OOP)
- ✅ Composition is strongest relationship
- ✅ Consider lifetime of objects when designing
- ✅ Composition promotes cleaner code and better encapsulation
