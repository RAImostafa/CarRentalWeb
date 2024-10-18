from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import datetime
from collections import defaultdict
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the User class
class User:
    def __init__(self, first_name, last_name, email, phone, government, password, role="user"):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.government = government
        self.password = password
        self.role = role

    def save_to_file(self):
        try:
           with open("signup_acc.json", "r") as file:
            users = json.load(file)
        except FileNotFoundError:
            users = []

        users.append({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "government": self.government,
            "password": self.password,
            "role": self.role
        })

        with open("signup_acc.json", "w") as file:
            json.dump(users, file, indent=4)

    @staticmethod
    def get_list():
        try:
            with open("signup_acc.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []
        return users
    
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    message = ""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        government = request.form['government']
        password = request.form['password']

        email = email.lower().strip()
        
        # Debugging: Print all received data
        print({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "government": government,
            "password": password
        })

        if not email.endswith('.com'):
            message = "Email must end with '.com'"
        elif len(password) < 8 or ',' in password or not any(char.isalpha() for char in password):
            message = "Password must be at least 8 characters long, contain letters, and not contain commas."
        else:
            users = User.get_list()
            for user in users:
                if user["email"].lower().strip() == email:
                    message = "Email already exists"
                    break
            else:
                new_user = User(first_name, last_name, email, phone, government, password, role="user")
                new_user.save_to_file()
                session['user_id'] = email
                print("User added successfully!")  # Debug statement
                return redirect(url_for('home'))
    return render_template('sign_up.html', message=message)

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    message = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.get_list()
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user_id'] = email
                
                # Check if the user has a role and it's 'admin'
                if user.get('role') == 'admin':
                    # Store a special message for the admin
                    first_name = "Admin"
                    role = 'admin_page'
                else:
                    # Otherwise, use the user's first name and normal role
                    first_name = user['first_name']
                    role = 'home'
                
                # Redirect with JavaScript and store first_name in localStorage
                return f'''
                <script>
                localStorage.setItem('first_name', '{first_name}');
                window.location.href = "/{role}";
                </script>
                '''
        
        message = "Invalid email or password"
    return render_template('sign_in.html', message=message)



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


@app.route('/sign_out', methods=['POST'])
def sign_out():
    session.pop('user_id', None)
    return redirect(url_for('index'))

# ************************************** CAR CLASS FUNS  *********************************
class Car:
    def __init__(self, image, model, type, capacity, doors, luggage, transmission, mileage, location, price, duration, owner, phone, plate_number, start_date, end_date):
        self.image = image
        self.model = model
        self.type = type
        self.capacity = capacity
        self.doors = doors
        self.luggage = luggage
        self.transmission = transmission
        self.mileage = mileage
        self.location = location
        self.price = price
        self.duration = duration
        self.owner = owner
        self.phone = phone
        self.plate_number = plate_number
        self.start_date = start_date
        self.end_date = end_date


    @staticmethod
    def get_cars():
        with open("cars.txt") as file:
            content = file.read()
        car_data = [tuple(line.split("|")) for line in content.strip().split("\n") if line]
        cars = [Car(*data) for data in car_data]
        return cars



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/home')
def home():
    welcome_message = ""
    if 'user_id' in session:
        email = session['user_id']
        users = User.get_list()
        for user in users:
            if user['email'] == email:
                welcome_message = f"Welcome back, {user['first_name']}!"
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cars = Car.get_cars()
    
    try:
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
            booked_models = {booking['car']['model']: booking['car'] for booking in bookings}
    except FileNotFoundError:
        booked_models = {}

    for car in cars:
        if car.model in booked_models:
            car.status = booked_models[car.model].get('status')

    return render_template('Home.html', welcome_message=welcome_message, current_datetime=current_datetime, cars=cars)


@app.route('/car/<car_model>')
def car(car_model):
    cars = Car.get_cars()
    selected_car = next((car for car in cars if car.model == car_model), None)
    if not selected_car:
        return "Car not found", 404

    return render_template('car_page.html', car=selected_car)



@app.route('/book_car', methods=['POST'])
def book_car():
    if 'user_id' not in session:
        return jsonify({"message": "User not logged in"}), 401

    email = session['user_id']
    users = User.get_list()
    user = next((u for u in users if u['email'] == email), None)
    if not user:
        return jsonify({"message": "User not found"}), 404

    car_model = request.json['car_model']
    cars = Car.get_cars()
    car = next((c for c in cars if c.model == car_model), None)
    if not car:
        return jsonify({"message": "Car not found"}), 404

    try:
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
    except FileNotFoundError:
        bookings = []

    # Check if the car is already booked
    if any(booking['car']['model'] == car_model for booking in bookings):
        return jsonify({"message": "Car is already booked"}), 409

    booking_info = {
        "user": user,
        "car": {**car.__dict__, "status": "booked"}
    }

    bookings.append(booking_info)

    with open("booked_cars.json", "w") as file:
        json.dump(bookings, file, indent=4)

    return jsonify({"message": "Car booked successfully"}), 200




@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if 'user_id' not in session:
        return jsonify({"message": "User not logged in"}), 401

    email = session['user_id']
    car_model = request.json['car_model']

    try:
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
    except FileNotFoundError:
        bookings = []

    bookings = [booking for booking in bookings if not (booking['car']['model'] == car_model and booking['user']['email'] == email)]

    with open("booked_cars.json", "w") as file:
        json.dump(bookings, file, indent=4)

    return jsonify({"message": "Booking cancelled successfully"}), 200



# ************************************** ADMIN PAGE *********************************
@app.route('/admin_page')
def admin_page():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    users = User.get_list()
    user = next((u for u in users if u['email'] == session['user_id']), None)
    
    if user and user.get('role') == 'admin':
        cars = Car.get_cars()
        with open("booked_cars.json", "r") as file:
            bookings = json.load(file)
        booked_cars = [booking['car'] for booking in bookings]
        return render_template('admin.html', cars=cars, booked_cars=booked_cars)
    else:
        return redirect(url_for('home'))
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    message = ""
    if request.method == 'POST':
        # Check if the file part exists in the request
        if 'image_path' not in request.files:
            message = "Error: No file part in the request."
            return render_template('add_car.html', message=message)
        
        file = request.files['image_path']
        
        # If the user does not select a file
        if file.filename == '':
            message = "Error: No selected file."
            return render_template('add_car.html', message=message)

        # Save the file if it is an allowed type
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_path = f"images/{filename}"
        else:
            message = "Error: File type not allowed. Only images are accepted."
            return render_template('add_car.html', message=message)
        
        # Fetch other form data
        model = request.form['model']
        plate_number = request.form['plate_number']

        # Append "EGP" to the price field
        price = f"{request.form['price']} EGP"

        # Check for duplicate plate numbers
        with open('cars.txt', 'r') as file:
            existing_cars = file.readlines()
            for car in existing_cars:
                car_details = car.strip().split("|")
                if car_details[-1] == plate_number:
                    message = "Error: Car with this plate number already exists."
                    return render_template('add_car.html', message=message)

        # Prepare car data for entry
        car_data = {
            "image": image_path,
            "model": model,
            "type": request.form['car_type'],
            "capacity": request.form['seats'],
            "doors": request.form['doors'],
            "luggage": request.form['bags'],
            "transmission": request.form['transmission'],
            "mileage": request.form['availability'],
            "location": request.form['location'],
            "price": price,
            "duration": request.form['duration'],
            "owner": request.form['renter_name'],
            "phone": request.form['renter_phone'],
            "plate_number": plate_number
        }
        
        # Convert car data to entry format and save it
        car_entry = "|".join(car_data.values())
        with open('cars.txt', 'a') as file:
            file.write(car_entry + "\n")
        
        return redirect(url_for('admin_page'))

    return render_template('add_car.html', message=message)
    




@app.route('/admin/remove_booking', methods=['POST'])
def remove_booking():
    car_model = request.form['model']
    with open('booked_cars.json', 'r') as file:
        bookings = json.load(file)
    bookings = [booking for booking in bookings if booking['car']['model'] != car_model]
    with open('booked_cars.json', 'w') as file:
        json.dump(bookings, file, indent=4)
    return redirect(url_for('admin_page'))



@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()
    model_to_delete = data.get('model')
    car_deleted = False

    # Remove from cars.txt
    with open('cars.txt', 'r') as file:
        cars = file.readlines()

    with open('cars.txt', 'w') as file:
        for car in cars:
            if model_to_delete not in car:
                file.write(car)
            else:
                car_deleted = True

    # Check if car was removed from cars.txt
    if car_deleted:
        # Remove from booked_cars.json if it exists
        try:
            with open('booked_cars.json', 'r') as file:
                booked_cars = json.load(file)
        except FileNotFoundError:
            booked_cars = []

        new_booked_cars = [car for car in booked_cars if car['car']['model'] != model_to_delete]
        
        if len(new_booked_cars) != len(booked_cars):
            with open('booked_cars.json', 'w') as file:
                json.dump(new_booked_cars, file, indent=4)
        
        return jsonify({"success": True, "message": "Car and its booking removed successfully."})
    else:
        return jsonify({"success": False, "message": "Car not found."})
    
@app.route('/booked_cars')
def booked_cars():
    try:
        with open('booked_cars.json', 'r') as file:
            bookings = json.load(file)
    except FileNotFoundError:
        bookings = []
    
    # Group bookings by user
    grouped_bookings = defaultdict(list)
    for booking in bookings:
        user = (booking['user']['first_name'], booking['user']['last_name'], booking['user']['email'], booking['user']['phone'])
        grouped_bookings[user].append(booking)
    
    return render_template('booked_cars.html', grouped_bookings=grouped_bookings)


if __name__ == '__main__':
    app.run(debug=True)
