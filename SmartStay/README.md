# SmartStay - Hotel Booking & Staff Management System

## Year 3 Software Engineering Project

A comprehensive hotel management system built with Flask, demonstrating Object-Oriented Programming principles and Agile development methodology.

## System Overview

SmartStay is a web-based hotel booking and staff management system designed to automate hotel operations including room booking, staff management, room availability tracking, and payment recording.

## Technology Stack

- **Backend**: Python 3.x with Flask Framework
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript with Bootstrap 5
- **Architecture**: Model-View-Controller (MVC)
- **Development Methodology**: Agile SDLC

## Features

### Core Functionality
- ✅ View available rooms
- ✅ Book and cancel rooms
- ✅ Track room availability
- ✅ Register and manage staff
- ✅ Record booking payments
- ✅ Role-based access control

### User Roles
1. **Administrator**: Full system access, user management, reports
2. **Receptionist**: Booking management, guest check-in/out
3. **Guest**: Room booking, booking history
4. **Staff**: Schedule viewing, profile management

## Project Structure

```
smartstay/
├── app.py                 # Main Flask application
├── models.py              # OOP classes and database models
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── rooms.html        # Room listing
│   ├── book_room.html    # Booking form
│   ├── my_bookings.html  # Guest bookings
│   ├── admin_dashboard.html
│   ├── manage_staff.html
│   ├── add_staff.html
│   ├── receptionist_dashboard.html
│   ├── guest_dashboard.html
│   ├── staff_dashboard.html
│   ├── all_bookings.html
│   └── demo_oop.html     # OOP principles demo
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles
    └── js/
        └── script.js      # Custom JavaScript
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd smartstay
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your web browser and navigate to: `http://localhost:5000`

## Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Administrator | admin | admin123 |
| Receptionist | reception | recep123 |
| Guest | john_guest | guest123 |
| Staff | housekeeping | staff123 |

## Object-Oriented Programming Implementation

### 1. Abstraction
The `User` abstract base class defines the common interface for all user types:

```python
from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def get_role(self) -> str:
        pass
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        pass
```

### 2. Inheritance
Four concrete classes inherit from the `User` base class:
- `Admin` - Full system access
- `Receptionist` - Booking management
- `Guest` - Room booking capabilities
- `Staff` - Limited access for operations

### 3. Encapsulation
Private attributes (prefixed with `_`) are protected with getter/setter methods:

```python
class Admin(User):
    def __init__(self, user_id, username, email, password):
        self._user_id = user_id  # Private attribute
        self._admin_level = "super_admin"
    
    def get_user_id(self) -> int:
        return self._user_id  # Controlled access
```

### 4. Polymorphism
Method overriding demonstrates polymorphic behavior:

```python
class User(ABC):
    def login(self) -> str:
        return f"{self._username} logged in successfully"

class Admin(User):
    def login(self) -> str:  # Method overriding
        return f"Administrator {self._username} accessed admin panel"
```

## Database Schema

### Users Table
- `user_id` (PK, INTEGER)
- `username` (TEXT, UNIQUE)
- `email` (TEXT, UNIQUE)
- `password` (TEXT)
- `role` (TEXT)
- `phone` (TEXT)
- `position` (TEXT)
- `salary` (REAL)
- `hire_date` (TEXT)
- `loyalty_points` (INTEGER)

### Rooms Table
- `room_id` (PK, INTEGER)
- `room_number` (TEXT, UNIQUE)
- `room_type` (TEXT)
- `price_per_night` (REAL)
- `capacity` (INTEGER)
- `is_available` (BOOLEAN)

### Bookings Table
- `booking_id` (PK, INTEGER)
- `room_id` (FK to rooms.room_id)
- `guest_id` (FK to users.user_id)
- `check_in_date` (TEXT)
- `check_out_date` (TEXT)
- `total_amount` (REAL)
- `status` (TEXT)
- `payment_status` (TEXT)

## Agile SDLC Implementation

### 1. Requirements Gathering
- User stories for each role
- Functional requirements specification
- Technical requirements analysis

### 2. Sprint Planning
- Sprint 1: Core OOP classes and database setup
- Sprint 2: Flask routes and basic functionality
- Sprint 3: UI templates and styling
- Sprint 4: Testing and documentation

### 3. Iterative Development
- Incremental feature implementation
- Continuous integration of components
- Regular testing and validation

### 4. Testing
- Unit testing for OOP classes
- Integration testing for Flask routes
- User acceptance testing

### 5. Review
- Code review and optimization
- Documentation updates
- Final system validation

## System Design Diagrams

### Data Flow Diagram (Level 0)
```
Guest/Staff/Receptionist/Admin → SmartStay System → Database
                                    ↓
                            Reports & Notifications
```

### Data Flow Diagram (Level 1)
```
Login Module → Authentication → Role-Based Dashboard
Booking Module → Room Availability → Payment Processing
Staff Module → User Management → Schedule Assignment
```

### Entity Relationship Diagram
```
Users (1) ←→ (N) Bookings (N) ←→ (1) Rooms
Users (1) ←→ (N) Staff_Roles
```

### Booking Process Flowchart
```
Start → Select Room → Choose Dates → Calculate Price → Confirm Booking → Update Room Status → End
```

## Testing Strategy

### Unit Testing
- Test OOP class methods
- Validate database operations
- Test business logic

### Integration Testing
- Test Flask routes
- Validate user authentication
- Test role-based access

### User Acceptance Testing
- End-to-end user workflows
- Cross-browser compatibility
- Mobile responsiveness

## API Endpoints

### Authentication
- `GET /` - Home page
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Room Management
- `GET /rooms` - View available rooms
- `GET/POST /book_room/<room_id>` - Book a room

### Booking Management
- `GET /my_bookings` - Guest bookings
- `GET /cancel_booking/<booking_id>` - Cancel booking
- `GET /all_bookings` - All bookings (Admin/Receptionist)
- `GET /process_payment/<booking_id>` - Process payment

### Staff Management
- `GET /admin_dashboard` - Admin dashboard
- `GET /manage_staff` - Staff management
- `GET/POST /add_staff` - Add new staff
- `GET /delete_staff/<user_id>` - Delete staff

### Dashboards
- `GET /receptionist_dashboard` - Receptionist dashboard
- `GET /guest_dashboard` - Guest dashboard
- `GET /staff_dashboard` - Staff dashboard

### Demo
- `GET /demo_oop` - OOP principles demonstration

## Security Features

- Session-based authentication
- Role-based access control
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## Future Enhancements

- Email notifications
- Advanced reporting
- Mobile app development
- Payment gateway integration
- Multi-language support
- Advanced room management
- Guest loyalty program
- Staff scheduling system

## Contributing

This project was developed as part of a Year 3 Software Engineering assignment. The codebase demonstrates:

1. **Object-Oriented Programming Principles**
2. **Agile Development Methodology**
3. **Software Architecture Design**
4. **Database Design and Management**
5. **Web Development Best Practices**

## License

This project is for educational purposes as part of a software engineering curriculum.

## Contact

For questions or feedback regarding this project, please refer to the academic submission guidelines.

---

**Note**: This system is designed for educational purposes and should not be used in a production environment without additional security measures and scalability considerations.
