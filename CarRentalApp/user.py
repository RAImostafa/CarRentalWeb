import json
from collections import defaultdict
import os
from flask import session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

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

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @staticmethod
    def get_admin_user():
        users = User.get_list()
        return next((u for u in users if u['email'] == session['user_id'] and u.get('role') == 'admin'), None)
    
    @classmethod
    def sign_up(cls, form_data):
        first_name = form_data['first_name']
        last_name = form_data['last_name']
        email = form_data['email'].lower().strip()
        phone = form_data['phone']
        government = form_data['government']
        password = form_data['password']

        # Validation
        if not email.endswith('.com'):
            return "Email must end with '.com'", None
        if len(password) < 8 or ',' in password or not any(char.isalpha() for char in password):
            return "Password must be at least 8 characters long, contain letters, and not contain commas.", None

        users = cls.get_list()
        for user in users:
            if user["email"].lower().strip() == email:
                return "Email already exists", None

        # Create new user and save
        new_user = cls(first_name, last_name, email, phone, government, password)
        new_user.save_to_file()
        session['user_id'] = email
        return None, new_user

    @classmethod
    def sign_in(cls, form_data):
        email = form_data['email']
        password = form_data['password']
        users = cls.get_list()

        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user_id'] = email
                if user.get('role') == 'admin':
                    return None, "Admin", 'admin_page'
                else:
                    return None, user['first_name'], 'home'
        return "Invalid email or password", None, None
    
    @staticmethod
    def add_car(form_data, file):
        # Check if the file part exists and validate the file
        if file.filename == '':
            return "Error: No selected file or file not found."
    
        # Save the file if allowed
        if User.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join("static/images", filename)  # Save in 'static/images'
            file.save(file_path)
            image_path = f"images/{filename}"
        else:
            return "Error: File type not allowed. Only images are accepted."
    
        # Fetch other form data
        model = form_data['model']
        plate_number = form_data['plate_number']
        price = f"{form_data['price']} EGP"
    
        # Check for duplicate plate numbers
        with open('cars.txt', 'r') as file:
            existing_cars = file.readlines()
            for car in existing_cars:
                car_details = car.strip().split("|")
                if car_details[-1] == plate_number:
                    return "Error: Car with this plate number already exists."
    
        # Prepare car data for entry and save it
        car_data = {
            "image": image_path,
            "model": model,
            "type": form_data['car_type'],
            "capacity": form_data['seats'],
            "doors": form_data['doors'],
            "luggage": form_data['bags'],
            "transmission": form_data['transmission'],
            "location": form_data['location'],
            "price": price,
            "duration": form_data['duration'],
            "owner": form_data['renter_name'],
            "phone": form_data['renter_phone'],
            "plate_number": plate_number
        }
    
        car_entry = "|".join(car_data.values())
        with open('cars.txt', 'a') as file:
            file.write(car_entry + "\n")
    
        return None



    @staticmethod
    def remove_booking(car_model):
        with open('booked_cars.json', 'r') as file:
            bookings = json.load(file)
        bookings = [booking for booking in bookings if booking['car']['model'] != car_model]
        with open('booked_cars.json', 'w') as file:
            json.dump(bookings, file, indent=4)

    @staticmethod
    def delete_car(model_to_delete):
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

        # Remove from booked_cars.json if it exists
        if car_deleted:
            try:
                with open('booked_cars.json', 'r') as file:
                    booked_cars = json.load(file)
            except FileNotFoundError:
                booked_cars = []

            new_booked_cars = [car for car in booked_cars if car['car']['model'] != model_to_delete]
            with open('booked_cars.json', 'w') as file:
                json.dump(new_booked_cars, file, indent=4)

        return car_deleted

    @staticmethod
    def get_booked_cars():
        try:
            with open('booked_cars.json', 'r') as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []
        
        grouped_bookings = defaultdict(list)
        for booking in bookings:
            user = (booking['user']['first_name'], booking['user']['last_name'], booking['user']['email'])
            grouped_bookings[user].append(booking)
        return grouped_bookings