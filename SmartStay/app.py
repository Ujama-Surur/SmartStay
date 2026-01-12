from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, timedelta
import sqlite3
from models import DatabaseManager, Room, Booking, Admin, Receptionist, Guest, Staff, demonstrate_polymorphism

app = Flask(__name__)
app.secret_key = 'smartstay_secret_key_2024'

# Initialize database
db_manager = DatabaseManager()
db_manager.add_sample_data()

# Helper functions
def get_db_connection():
    return db_manager.get_connection()

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    conn.close()
    
    if user_data:
        user_dict = {
            'user_id': user_data[0],
            'username': user_data[1],
            'email': user_data[2],
            'password': user_data[3],
            'role': user_data[4],
            'phone': user_data[5],
            'position': user_data[6],
            'salary': user_data[7],
            'hire_date': user_data[8],
            'loyalty_points': user_data[9]
        }
        
        if user_data[4] == 'admin':
            return Admin(user_data[0], user_data[1], user_data[2], user_data[3])
        elif user_data[4] == 'receptionist':
            return Receptionist(user_data[0], user_data[1], user_data[2], user_data[3])
        elif user_data[4] == 'guest':
            return Guest(user_data[0], user_data[1], user_data[2], user_data[3], user_data[5])
        elif user_data[4] == 'staff':
            return Staff(user_data[0], user_data[1], user_data[2], user_data[3], user_data[6])
    return None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            session['user_id'] = user_data[0]
            session['username'] = user_data[1]
            session['role'] = user_data[4]
            
            if user_data[4] == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user_data[4] == 'receptionist':
                return redirect(url_for('receptionist_dashboard'))
            elif user_data[4] == 'guest':
                return redirect(url_for('guest_dashboard'))
            elif user_data[4] == 'staff':
                return redirect(url_for('staff_dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/rooms')
@login_required
def rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms ORDER BY room_number')
    rooms_data = cursor.fetchall()
    conn.close()
    
    rooms = []
    for room_data in rooms_data:
        room = Room(room_data[0], room_data[1], room_data[2], room_data[3], room_data[4])
        room.set_availability(bool(room_data[5]))
        rooms.append(room)
    
    return render_template('rooms.html', rooms=rooms)

@app.route('/book_room/<int:room_id>', methods=['GET', 'POST'])
@login_required
def book_room(room_id):
    if session.get('role') != 'guest':
        flash('Only guests can book rooms')
        return redirect(url_for('rooms'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms WHERE room_id = ?', (room_id,))
    room_data = cursor.fetchone()
    
    if not room_data or not room_data[5]:  # Room doesn't exist or not available
        flash('Room not available')
        return redirect(url_for('rooms'))
    
    if request.method == 'POST':
        check_in_date = request.form['check_in_date']
        check_out_date = request.form['check_out_date']
        
        # Calculate total amount
        check_in = datetime.strptime(check_in_date, '%Y-%m-%d')
        check_out = datetime.strptime(check_out_date, '%Y-%m-%d')
        nights = (check_out - check_in).days
        total_amount = nights * room_data[3]
        
        # Create booking
        cursor.execute('''
            INSERT INTO bookings (room_id, guest_id, check_in_date, check_out_date, total_amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (room_id, session['user_id'], check_in_date, check_out_date, total_amount))
        
        # Update room availability
        cursor.execute('UPDATE rooms SET is_available = 0 WHERE room_id = ?', (room_id,))
        
        conn.commit()
        conn.close()
        
        flash('Room booked successfully!')
        return redirect(url_for('my_bookings'))
    
    conn.close()
    room = Room(room_data[0], room_data[1], room_data[2], room_data[3], room_data[4])
    return render_template('book_room.html', room=room)

@app.route('/my_bookings')
@login_required
def my_bookings():
    if session.get('role') != 'guest':
        flash('Only guests can view their bookings')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, r.room_number, r.room_type 
        FROM bookings b
        JOIN rooms r ON b.room_id = r.room_id
        WHERE b.guest_id = ?
        ORDER BY b.booking_id DESC
    ''', (session['user_id'],))
    bookings_data = cursor.fetchall()
    conn.close()
    
    bookings = []
    for booking_data in bookings_data:
        booking = Booking(booking_data[0], booking_data[1], booking_data[2], 
                         booking_data[3], booking_data[4], booking_data[5])
        booking.set_status(booking_data[6])
        booking.set_payment_status(booking_data[7])
        bookings.append({
            'booking': booking,
            'room_number': booking_data[8],
            'room_type': booking_data[9]
        })
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/cancel_booking/<int:booking_id>')
@login_required
def cancel_booking(booking_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get booking details
    cursor.execute('SELECT * FROM bookings WHERE booking_id = ?', (booking_id,))
    booking_data = cursor.fetchone()
    
    if booking_data and booking_data[2] == session['user_id']:  # User owns this booking
        # Update booking status
        cursor.execute('UPDATE bookings SET status = ? WHERE booking_id = ?', 
                      ('cancelled', booking_id))
        
        # Make room available again
        cursor.execute('UPDATE rooms SET is_available = 1 WHERE room_id = ?', 
                      (booking_data[1],))
        
        conn.commit()
        flash('Booking cancelled successfully')
    
    conn.close()
    return redirect(url_for('my_bookings'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms')
    total_rooms = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE is_available = 1')
    available_rooms = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings')
    total_bookings = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings WHERE status = "confirmed"')
    active_bookings = cursor.fetchone()[0]
    
    conn.close()
    
    stats = {
        'total_users': total_users,
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings
    }
    
    return render_template('admin_dashboard.html', stats=stats)

@app.route('/manage_staff')
@login_required
def manage_staff():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE role IN ("staff", "receptionist")')
    staff_data = cursor.fetchall()
    conn.close()
    
    return render_template('manage_staff.html', staff=staff_data)

@app.route('/add_staff', methods=['GET', 'POST'])
@login_required
def add_staff():
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        position = request.form.get('position', '')
        salary = float(request.form.get('salary', 0))
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password, role, position, salary, hire_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (username, email, password, role, position, salary, datetime.now().strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        
        flash('Staff member added successfully')
        return redirect(url_for('manage_staff'))
    
    return render_template('add_staff.html')

@app.route('/delete_staff/<int:user_id>')
@login_required
def delete_staff(user_id):
    if session.get('role') != 'admin':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE user_id = ? AND role IN ("staff", "receptionist")', (user_id,))
    conn.commit()
    conn.close()
    
    flash('Staff member deleted successfully')
    return redirect(url_for('manage_staff'))

@app.route('/receptionist_dashboard')
@login_required
def receptionist_dashboard():
    if session.get('role') != 'receptionist':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get today's check-ins and check-outs
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('SELECT COUNT(*) FROM bookings WHERE check_in_date = ?', (today,))
    today_checkins = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM bookings WHERE check_out_date = ?', (today,))
    today_checkouts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE is_available = 1')
    available_rooms = cursor.fetchone()[0]
    
    conn.close()
    
    stats = {
        'today_checkins': today_checkins,
        'today_checkouts': today_checkouts,
        'available_rooms': available_rooms
    }
    
    return render_template('receptionist_dashboard.html', stats=stats)

@app.route('/guest_dashboard')
@login_required
def guest_dashboard():
    if session.get('role') != 'guest':
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user's loyalty points
    cursor.execute('SELECT loyalty_points FROM users WHERE user_id = ?', (session['user_id'],))
    loyalty_points = cursor.fetchone()[0]
    
    # Get user's active bookings
    cursor.execute('''
        SELECT COUNT(*) FROM bookings 
        WHERE guest_id = ? AND status = "confirmed"
    ''', (session['user_id'],))
    active_bookings = cursor.fetchone()[0]
    
    conn.close()
    
    stats = {
        'loyalty_points': loyalty_points,
        'active_bookings': active_bookings
    }
    
    return render_template('guest_dashboard.html', stats=stats)

@app.route('/staff_dashboard')
@login_required
def staff_dashboard():
    if session.get('role') != 'staff':
        return redirect(url_for('index'))
    
    user = get_user_by_id(session['user_id'])
    
    return render_template('staff_dashboard.html', user=user)

@app.route('/all_bookings')
@login_required
def all_bookings():
    if session.get('role') not in ['admin', 'receptionist']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT b.*, u.username, r.room_number, r.room_type 
        FROM bookings b
        JOIN users u ON b.guest_id = u.user_id
        JOIN rooms r ON b.room_id = r.room_id
        ORDER BY b.booking_id DESC
    ''')
    bookings_data = cursor.fetchall()
    conn.close()
    
    return render_template('all_bookings.html', bookings=bookings_data)

@app.route('/process_payment/<int:booking_id>')
@login_required
def process_payment(booking_id):
    if session.get('role') not in ['admin', 'receptionist']:
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE bookings SET payment_status = ? WHERE booking_id = ?', 
                  ('paid', booking_id))
    conn.commit()
    conn.close()
    
    flash('Payment processed successfully')
    return redirect(url_for('all_bookings'))

@app.route('/demo_oop')
def demo_oop():
    # Demonstrate OOP principles
    admin = Admin(1, "admin_user", "admin@hotel.com", "admin123")
    receptionist = Receptionist(2, "recep_user", "recep@hotel.com", "recep123")
    guest = Guest(3, "guest_user", "guest@hotel.com", "guest123", "+1234567890")
    staff = Staff(4, "staff_user", "staff@hotel.com", "staff123", "Housekeeping")
    
    users = [admin, receptionist, guest, staff]
    polymorphism_results = demonstrate_polymorphism(users)
    
    return render_template('demo_oop.html', results=polymorphism_results)

if __name__ == '__main__':
    app.run(debug=True)
