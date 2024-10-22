import json
class Car:
    def __init__(self, image, model, car_type, capacity, doors, luggage, transmission, location, price, duration, owner, phone, plate_number):
        self.image = image
        self.model = model
        self.car_type = car_type
        self.capacity = capacity
        self.doors = doors
        self.luggage = luggage
        self.transmission = transmission
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

    
    @staticmethod
    def book_car(user, plate_number):
        cars = Car.get_cars()
        car = next((c for c in cars if c.plate_number == plate_number), None)
        if not car:
            return None, "Car not found"
        
        try:
            with open("booked_cars.json", "r") as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []
        except json.JSONDecodeError:
            return None, "Error loading bookings. File may be corrupted."
    
        # Check if the car is already booked
        if any(booking['car']['plate_number'] == plate_number for booking in bookings):
            return None, "Car is already booked"
        
        # Prepare booking info
        booking_info = {
            "user": user,
            "car": {**car.__dict__, "status": "booked"}
        }
        
        bookings.append(booking_info)
        
        # Save the updated bookings
        try:
            with open("booked_cars.json", "w") as file:
                json.dump(bookings, file, indent=4)
        except Exception as e:
            return None, f"Error saving booking: {str(e)}"
    
        return booking_info, "Car booked successfully"
    
    
    @staticmethod
    def delete_booking(email, plate_number):  # Changed from car_model to plate_number
        try:
            with open("booked_cars.json", "r") as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []
    
        # Filter bookings based on plate_number instead of car_model
        bookings = [booking for booking in bookings if not (booking['car']['plate_number'] == plate_number and booking['user']['email'] == email)]
        
        with open("booked_cars.json", "w") as file:
            json.dump(bookings, file, indent=4)
            
        return "Booking cancelled successfully"



    
    
