from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
import sqlite3

# ABSTRACTION: Abstract base class User
class User(ABC):
    def __init__(self, user_id: int, username: str, email: str, password: str):
        self._user_id = user_id  # ENCAPSULATION: Private attribute
        self._username = username
        self._email = email
        self._password = password
    
    # ABSTRACTION: Abstract methods
    @abstractmethod
    def get_role(self) -> str:
        pass
    
    @abstractmethod
    def get_permissions(self) -> List[str]:
        pass
    
    # ENCAPSULATION: Getters and setters
    def get_user_id(self) -> int:
        return self._user_id
    
    def set_user_id(self, user_id: int):
        self._user_id = user_id
    
    def get_username(self) -> str:
        return self._username
    
    def set_username(self, username: str):
        self._username = username
    
    def get_email(self) -> str:
        return self._email
    
    def set_email(self, email: str):
        self._email = email
    
    def login(self) -> str:
        return f"{self._username} logged in successfully"
    
    def logout(self) -> str:
        return f"{self._username} logged out successfully"

# INHERITANCE: Admin class inherits from User
class Admin(User):
    def __init__(self, user_id: int, username: str, email: str, password: str):
        super().__init__(user_id, username, email, password)
        self._admin_level = "super_admin"
    
    def get_role(self) -> str:
        return "Administrator"
    
    def get_permissions(self) -> List[str]:
        return ["manage_users", "manage_rooms", "manage_bookings", "manage_staff", "view_reports"]
    
    def get_admin_level(self) -> str:
        return self._admin_level
    
    def set_admin_level(self, level: str):
        self._admin_level = level
    
    # POLYMORPHISM: Method overriding
    def login(self) -> str:
        return f"Administrator {self._username} accessed admin panel"

# INHERITANCE: Receptionist class inherits from User
class Receptionist(User):
    def __init__(self, user_id: int, username: str, email: str, password: str):
        super().__init__(user_id, username, email, password)
        self._department = "front_desk"
    
    def get_role(self) -> str:
        return "Receptionist"
    
    def get_permissions(self) -> List[str]:
        return ["manage_bookings", "view_rooms", "check_in_guest", "check_out_guest"]
    
    def get_department(self) -> str:
        return self._department
    
    def set_department(self, department: str):
        self._department = department
    
    # POLYMORPHISM: Method overriding
    def login(self) -> str:
        return f"Receptionist {self._username} accessed reception system"

# INHERITANCE: Guest class inherits from User
class Guest(User):
    def __init__(self, user_id: int, username: str, email: str, password: str, phone: str = ""):
        super().__init__(user_id, username, email, password)
        self._phone = phone
        self._loyalty_points = 0
    
    def get_role(self) -> str:
        return "Guest"
    
    def get_permissions(self) -> List[str]:
        return ["view_rooms", "book_room", "cancel_booking", "view_own_bookings"]
    
    def get_phone(self) -> str:
        return self._phone
    
    def set_phone(self, phone: str):
        self._phone = phone
    
    def get_loyalty_points(self) -> int:
        return self._loyalty_points
    
    def add_loyalty_points(self, points: int):
        self._loyalty_points += points
    
    # POLYMORPHISM: Method overriding
    def login(self) -> str:
        return f"Guest {self._username} welcomed to SmartStay Hotel"

# INHERITANCE: Staff class inherits from User
class Staff(User):
    def __init__(self, user_id: int, username: str, email: str, password: str, position: str = ""):
        super().__init__(user_id, username, email, password)
        self._position = position
        self._salary = 0.0
        self._hire_date = datetime.now().strftime("%Y-%m-%d")
    
    def get_role(self) -> str:
        return "Staff"
    
    def get_permissions(self) -> List[str]:
        return ["view_schedule", "update_profile", "view_assigned_tasks"]
    
    def get_position(self) -> str:
        return self._position
    
    def set_position(self, position: str):
        self._position = position
    
    def get_salary(self) -> float:
        return self._salary
    
    def set_salary(self, salary: float):
        self._salary = salary
    
    def get_hire_date(self) -> str:
        return self._hire_date
    
    # POLYMORPHISM: Method overriding
    def login(self) -> str:
        return f"Staff {self._username} ({self._position}) clocked in"

# Room class
class Room:
    def __init__(self, room_id: int, room_number: str, room_type: str, price_per_night: float, capacity: int):
        self._room_id = room_id
        self._room_number = room_number
        self._room_type = room_type
        self._price_per_night = price_per_night
        self._capacity = capacity
        self._is_available = True
    
    def get_room_id(self) -> int:
        return self._room_id
    
    def get_room_number(self) -> str:
        return self._room_number
    
    def get_room_type(self) -> str:
        return self._room_type
    
    def get_price_per_night(self) -> float:
        return self._price_per_night
    
    def get_capacity(self) -> int:
        return self._capacity
    
    def is_available(self) -> bool:
        return self._is_available
    
    def set_availability(self, available: bool):
        self._is_available = available
    
    def to_dict(self) -> dict:
        return {
            'room_id': self._room_id,
            'room_number': self._room_number,
            'room_type': self._room_type,
            'price_per_night': self._price_per_night,
            'capacity': self._capacity,
            'is_available': self._is_available
        }

# Booking class
class Booking:
    def __init__(self, booking_id: int, room_id: int, guest_id: int, check_in_date: str, check_out_date: str, total_amount: float):
        self._booking_id = booking_id
        self._room_id = room_id
        self._guest_id = guest_id
        self._check_in_date = check_in_date
        self._check_out_date = check_out_date
        self._total_amount = total_amount
        self._status = "confirmed"
        self._payment_status = "pending"
    
    def get_booking_id(self) -> int:
        return self._booking_id
    
    def get_room_id(self) -> int:
        return self._room_id
    
    def get_guest_id(self) -> int:
        return self._guest_id
    
    def get_check_in_date(self) -> str:
        return self._check_in_date
    
    def get_check_out_date(self) -> str:
        return self._check_out_date
    
    def get_total_amount(self) -> float:
        return self._total_amount
    
    def get_status(self) -> str:
        return self._status
    
    def set_status(self, status: str):
        self._status = status
    
    def get_payment_status(self) -> str:
        return self._payment_status
    
    def set_payment_status(self, status: str):
        self._payment_status = status
    
    def to_dict(self) -> dict:
        return {
            'booking_id': self._booking_id,
            'room_id': self._room_id,
            'guest_id': self._guest_id,
            'check_in_date': self._check_in_date,
            'check_out_date': self._check_out_date,
            'total_amount': self._total_amount,
            'status': self._status,
            'payment_status': self._payment_status
        }

# Database Manager class
class DatabaseManager:
    def __init__(self, db_path: str = "smartstay/database/database.db"):
        import os
        # Ensure database directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                phone TEXT,
                position TEXT,
                salary REAL,
                hire_date TEXT,
                loyalty_points INTEGER DEFAULT 0
            )
        ''')
        
        # Create rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                room_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_number TEXT UNIQUE NOT NULL,
                room_type TEXT NOT NULL,
                price_per_night REAL NOT NULL,
                capacity INTEGER NOT NULL,
                is_available BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
                room_id INTEGER NOT NULL,
                guest_id INTEGER NOT NULL,
                check_in_date TEXT NOT NULL,
                check_out_date TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'confirmed',
                payment_status TEXT DEFAULT 'pending',
                FOREIGN KEY (room_id) REFERENCES rooms (room_id),
                FOREIGN KEY (guest_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def add_sample_data(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Add sample rooms
        rooms = [
            ('101', 'Single', 50000.0, 1),
            ('102', 'Single', 50000.0, 1),
            ('201', 'Double', 80000.0, 2),
            ('202', 'Double', 80000.0, 2),
            ('301', 'Suite', 150000.0, 4),
            ('302', 'Suite', 150000.0, 4)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO rooms (room_number, room_type, price_per_night, capacity, is_available)
            VALUES (?, ?, ?, ?, 1)
        ''', rooms)
        
        # Add sample users
        users = [
            ('admin', 'admin@smartstay.com', 'admin123', 'admin', '', '', 0.0, '', 0),
            ('reception', 'reception@smartstay.com', 'recep123', 'receptionist', '', 'Receptionist', 2500000.0, '2024-01-01', 0),
            ('housekeeping', 'housekeeping@smartstay.com', 'staff123', 'staff', '', 'Housekeeping', 1800000.0, '2024-01-01', 0),
            ('john_guest', 'john@email.com', 'guest123', 'guest', '+1234567890', '', 0.0, '', 0)
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO users (username, email, password, role, phone, position, salary, hire_date, loyalty_points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', users)
        
        conn.commit()
        conn.close()

# POLYMORPHISM: Function demonstrating polymorphic behavior
def demonstrate_polymorphism(users: List[User]) -> List[str]:
    results = []
    for user in users:
        results.append(user.login())  # Different behavior based on object type
        results.append(f"Role: {user.get_role()}")
        results.append(f"Permissions: {', '.join(user.get_permissions())}")
        results.append("---")
    return results
