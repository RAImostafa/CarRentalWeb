from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import datetime
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Define the User class
class User:
    def __init__(self, email, password, role="user", first_name=None, last_name=None, phone=None, government=None):
        self.email = email
        self.password = password
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.government = government

    # Save, load, and other methods remain unchanged

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
            "password": self.password
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


class Car:
    def __init__(self, image, model, type, capacity, doors, luggage, transmission, mileage, location, price, duration, owner, phone, plate_number):
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