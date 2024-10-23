import json
from collections import defaultdict
import os
from flask import session
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'avif' , 'webp'}

class User:
    def __init__(self, first_name, last_name, email, phone, government, password, role="user"):
        # Initialize User object with first name, last name, email, phone, government, password, and role (default is 'user')
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.government = government
        self.password = password
        self.role = role

    def save_to_file(self):
        # Save the user details to the 'signup_acc.json' file
        try:
            with open("signup_acc.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []

        # Append new user details to the list and save back to the file
        users.append({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "government": self.government,
            "password": self.password,
            "role": self.role
        })

        # Write the updated users list to the file
        with open("signup_acc.json", "w") as file:
            json.dump(users, file, indent=4)
    
     # Retrieve all users from 'signup_acc.json' file
    @staticmethod
    def get_list():
        try:
            with open("signup_acc.json", "r") as file:
                users = json.load(file)
        except FileNotFoundError:
            users = []
        return users


     # Check if the file extension is one of the allowed extensions for image uploads
    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    # Get the current user from the session and check if they are an admin
    @staticmethod
    def get_admin_user():
        users = User.get_list()
        return next((u for u in users if u['email'] == session['user_id'] and u.get('role') == 'admin'), None)
    


    # Validate and sign up a new user using form data
    @classmethod
    def sign_up(cls, form_data):
        first_name = form_data['first_name']
        last_name = form_data['last_name']
        email = form_data['email'].lower().strip()
        phone = form_data['phone']
        government = form_data['government']
        password = form_data['password']
        
        # Validate email format
        if '@' not in email or not email.endswith('.com'):
            return "Email must contain '@' and end with '.com'", None

        # Validate phone number format
        if not phone.isdigit() or len(phone) != 11 or not phone.startswith('0'):
            return "Phone number must be positive 11 digits, start with '0', and contain only numbers", None

        # Validate password
        if len(password) < 8 or ',' in password or not any(char.isalpha() for char in password):
            return "Password must be at least 8 characters and contain a letter", None

        # Check if the email already exists
        users = cls.get_list()
        for user in users:
            if user["email"].lower().strip() == email:
                return "Email already exists", None

        # Create new user and save
        new_user = cls(first_name, last_name, email, phone, government, password)
        new_user.save_to_file()
        session['user_id'] = email
        return None, new_user

     
     
    #Authenticate a user by email and password
    @classmethod
    def sign_in(cls, form_data):
        email = form_data['email']
        password = form_data['password']
        users = cls.get_list()

        # Check if the user exists and the credentials match
        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user_id'] = email
                if user.get('role') == 'admin':
                    return None, "Admin", 'admin_page'
                else:
                    return None, user['first_name'], 'home'
        return "Invalid email or password", None, None
    

    # Add a new car with its details and save the car image
    @staticmethod
    def add_car(form_data, file):
        if file.filename == '':
            return "Error: No selected file or file not found."

        # Validate and save the uploaded file
        if User.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join("static/images", filename)
            file.save(file_path)
            image_path = f"images/{filename}"
        else:
            return "Error: File type not allowed. Only images are accepted."

        # Ensure the plate number is numeric
        try:
            plate_number = int(form_data['plate_number'])
        except ValueError:
            return "Error: Plate number must be a number."

        # Ensure the price is a valid number
        try:
            price = float(form_data['price'])
        except ValueError:
            return "Error: Price must be a valid number."

        # Check for duplicate plate numbers in the cars file
        with open('cars.txt', 'r') as file:
            existing_cars = file.readlines()
            for car in existing_cars:
                car_details = car.strip().split("|")
                if car_details[-1] == str(plate_number):
                    return "Error: Car with this plate number already exists."

        # Save the new car entry in 'cars.txt'
        car_data = {
            "image": image_path,
            "model": form_data['model'],
            "type": form_data['car_type'],
            "capacity": form_data['seats'],
            "doors": form_data['doors'],
            "luggage": form_data['bags'],
            "transmission": form_data['transmission'],
            "location": form_data['location'],
            "price": str(price),
            "duration": form_data['duration'],
            "owner": form_data['renter_name'],
            "phone": form_data['renter_phone'],
            "plate_number": str(plate_number)
        }
        
        car_entry = "|".join(car_data.values())
        with open('cars.txt', 'a') as file:
            file.write(car_entry + "\n")
        
        return None
    
    # Remove a car booking based on the plate number from 'booked_cars.json'
    @staticmethod
    def remove_booking(car_plate):
        with open('booked_cars.json', 'r') as file:
            bookings = json.load(file)
        # Filter out the booking matching the plate number
        bookings = [booking for booking in bookings if booking['car']['plate_number'] != car_plate]
        # Save updated bookings
        with open('booked_cars.json', 'w') as file:
            json.dump(bookings, file, indent=4)


     # Delete a car by its plate number from both 'cars.txt' and 'booked_cars.json'
    @staticmethod
    def delete_car(plate_number_to_delete):
       
        car_deleted = False

        # Remove the car from 'cars.txt'
        with open('cars.txt', 'r') as file:
            cars = file.readlines()
        with open('cars.txt', 'w') as file:
            for car in cars:
                if plate_number_to_delete not in car:
                    file.write(car)
                else:
                    car_deleted = True
        
        # Remove the car from 'booked_cars.json' if it was booked
        if car_deleted:
            try:
                with open('booked_cars.json', 'r') as file:
                    booked_cars = json.load(file)
            except FileNotFoundError:
                booked_cars = []
            new_booked_cars = [car for car in booked_cars if car['car']['plate_number'] != plate_number_to_delete]
            with open('booked_cars.json', 'w') as file:
                json.dump(new_booked_cars, file, indent=4)

        return car_deleted


     # Retrieve all booked cars and group them by user
    @staticmethod
    def get_booked_cars():
        try:
            with open('booked_cars.json', 'r') as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []

        grouped_bookings = defaultdict(list)
        for booking in bookings:
            user = (booking['user']['first_name'], booking['user']['last_name'], booking['user']['email'], booking['user']['phone'])
            grouped_bookings[user].append(booking)
        return grouped_bookings
