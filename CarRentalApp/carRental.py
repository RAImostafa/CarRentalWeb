from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import datetime
import os
from werkzeug.utils import secure_filename
from user import User
from car import Car
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ************************************** Authentication Routes *********************************

# Sign up route: Allows users to register with their details
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    message = ""
    if request.method == 'POST':
        form_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'government': request.form['government'],
            'password': request.form['password']
        }
        message, user = User.sign_up(form_data)
        if user:
            return redirect(url_for('home'))
    return render_template('sign_up.html', message=message)

# Sign in route: Handles user login by checking email and password
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    message = ""
    if request.method == 'POST':
        form_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        message, first_name, role = User.sign_in(form_data)
        if first_name:
            return f'''
            <script>
            localStorage.setItem('first_name', '{first_name}');
            window.location.href = "/{role}";
            </script>
            '''
    return render_template('sign_in.html', message=message)

# Sign out route: Logs the user out by clearing session data
@app.route('/sign_out', methods=['POST'])
def sign_out():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# ************************************** User Routes *********************************

# Home route: Displays welcome message and car listings
@app.route('/home')
def home():
    welcome_message = ""
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    if 'user_id' in session:
        email = session['user_id']
        users = User.get_list()
        for user in users:
            if user['email'] == email:
                welcome_message = f"Welcome back, {user.get('first_name', 'User')}!"

    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cars = Car.get_cars()

    try:
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
            booked_plate_numbers = {booking['car']['plate_number'] for booking in bookings}
    except FileNotFoundError:
        booked_plate_numbers = set()

    # Update each car's status based on the plate number
    for car in cars:
        if car.plate_number in booked_plate_numbers:
            car.status = 'booked'
        else:
            car.status = 'available'  # Set default status for unbooked cars

    return render_template('Home.html', welcome_message=welcome_message, current_datetime=current_datetime, cars=cars)

# Profile route: Displays user profile and their booked cars
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    email = session['user_id']
    users = User.get_list()
    user = next((user for user in users if user['email'] == email), None)

    try:
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
    except FileNotFoundError:
        bookings = []

    booked_cars = [booking['car'] for booking in bookings if booking['user']['email'] == email]

    return render_template('profile.html', user=user, booked_cars=booked_cars)

# Index route: The main landing page of the website
@app.route('/')
def index():
    return render_template('index.html')

# Car detail page: Displays details for a specific car by its plate number
@app.route('/car/<plate_number>')
def car(plate_number):
    cars = Car.get_cars()
    selected_car = next((car for car in cars if car.plate_number == plate_number), None)
    if not selected_car:
        return "Car not found", 404

    return render_template('car_page.html', car=selected_car)

# Book car route: Books a car for the current user
@app.route('/book_car', methods=['POST'])
def book_car():
    if 'user_id' not in session:
        return jsonify({"message": "User not logged in"}), 401

    email = session['user_id']
    users = User.get_list()
    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    plate_number = request.json['plate_number']
    booking_info, message = Car.book_car(user, plate_number)

    if not booking_info:
        return jsonify({"message": message}), 404 if message == "Car not found" else 409

    return jsonify({"message": message}), 200

# Delete booking route: Allows a user to cancel their booking
@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if 'user_id' not in session:
        return jsonify({"message": "User not logged in"}), 401

    email = session['user_id']
    plate_number = request.json['plate_number']

    message = Car.delete_booking(email, plate_number)
    return jsonify({"message": message}), 200

# ************************************** Admin Routes *********************************

# Admin page: Displays admin dashboard for managing cars and bookings
@app.route('/admin_page')
def admin_page():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    admin = User.get_admin_user()
    if admin:
        cars = Car.get_cars()
        booked_cars = User.get_booked_cars()
        return render_template('admin.html', cars=cars, booked_cars=booked_cars)
    else:
        return redirect(url_for('home'))

# Add car route: Allows admin to add new cars to the database
@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    message = ""
    if 'user_id' not in session:
         return redirect(url_for('sign_in'))
    if request.method == 'POST':
        file = request.files['image_path']
        form_data = request.form
        message = User.add_car(form_data, file)
        if not message:
            return redirect(url_for('admin_page'))
    return render_template('add_car.html', message=message)

# Remove booking route: Admin can remove a booking from the database
@app.route('/admin/remove_booking', methods=['POST'])
def remove_booking():
    car_plate = request.form['plate_number']
    User.remove_booking(car_plate)
    return redirect(url_for('admin_page'))

# Delete car route: Allows admin to delete a car from the database
@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()
    plate_number_to_delete = data.get('plate_number')

    # Check if the car is booked
    booked_cars = User.get_booked_cars()
    for bookings in booked_cars.values():
        for booking in bookings:
            if booking['car']['plate_number'] == plate_number_to_delete:
                return jsonify({"success": False, "message": "Cannot delete a booked car."})

    # Proceed to delete if not booked
    car_deleted = User.delete_car(plate_number_to_delete)
    if car_deleted:
        return jsonify({"success": True, "message": "Car removed successfully."})
    else:
        return jsonify({"success": False, "message": "Car not found."})

# List booked cars: Displays the list of booked cars in the admin view
@app.route('/booked_cars')
def booked_cars():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    grouped_bookings = User.get_booked_cars()
    return render_template('booked_cars.html', grouped_bookings=grouped_bookings)



# Edit car details route: Admin can edit a car's details if it is not booked
@app.route('/edit_car/<plate_number>', methods=['GET', 'POST'])
def edit_car(plate_number):
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    email = session['user_id']
    users = User.get_list()
    user = next((user for user in users if user['email'] == email), None)
    
    if user and user.get('role') == 'admin':
        cars = Car.get_cars()
        # Find the car by plate number instead of model
        selected_car = next((car for car in cars if car.plate_number == plate_number), None)
        
        booked_cars = User.get_booked_cars()
        for bookings in booked_cars.values():
            for booking in bookings:
                # Check if the car is booked by its plate number
                if booking['car']['plate_number'] == plate_number:
                    error_message = "Cannot edit a booked car."
                    return render_template('admin.html', error_message=error_message)
                   

        if request.method == 'POST':
            file = request.files['image_path']
            form_data = request.form

            # Save the file if allowed
            if file and User.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join("static/images", filename)  # Save in 'static/images'
                file.save(file_path)
                selected_car.image = f"images/{filename}"
            
            selected_car.car_type = form_data['car_type']
            selected_car.model = form_data['model']
            selected_car.capacity = form_data['capacity']
            selected_car.doors = form_data['doors']
            selected_car.luggage = form_data['luggage']
            selected_car.transmission = form_data['transmission']
            selected_car.location = form_data['location']
            selected_car.price = form_data['price']
            selected_car.duration = form_data['duration']
            selected_car.owner = form_data['owner']
            selected_car.phone = form_data['phone']
            selected_car.plate_number = form_data['plate_number']

            # Save updated car details back to cars.txt
            with open('cars.txt', 'w') as file:
                for car in cars:
                    file.write("|".join([car.image, car.model, car.car_type, str(car.capacity), str(car.doors),
                                         str(car.luggage), car.transmission, car.location, str(car.price), car.duration,
                                         car.owner, car.phone, car.plate_number]) + "\n")
            
            return redirect(url_for('admin_page'))
        
        return render_template('edit_car.html', car=selected_car)
    
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
