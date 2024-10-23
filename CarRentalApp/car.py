import json
 # Initialize the Car object with various attributes such as image, model, car type, etc.
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
    
    # Reads car details from 'cars.txt', processes each line, and returns a list of Car objects
    @staticmethod
    def get_cars():
        with open("cars.txt") as file:
            content = file.read()
        car_data = [tuple(line.split("|")) for line in content.strip().split("\n") if line]
        cars = [Car(*data) for data in car_data]
        return cars

     # Books a car by plate number if available and stores the booking in 'booked_cars.json'
    @staticmethod
    def book_car(user, plate_number):
        # Retrieve all cars
        cars = Car.get_cars()
        # Search for the car with the specified plate number
        car = next((c for c in cars if c.plate_number == plate_number), None)
        if not car:
            return None, "Car not found"
        
        # Load existing bookings from the JSON file
        try:
            with open("booked_cars.json", "r") as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []  # If file not found, assume no bookings
        except json.JSONDecodeError:
            return None, "Error loading bookings. File may be corrupted."
    
        # Check if the car is already booked
        if any(booking['car']['plate_number'] == plate_number for booking in bookings):
            return None, "Car is already booked"
        
        # Prepare booking information with user and car details
        booking_info = {
            "user": user,
            "car": {**car.__dict__, "status": "booked"}
        }
        
        # Add new booking to the list
        bookings.append(booking_info)
        
        # Save the updated bookings list back to the JSON file
        try:
            with open("booked_cars.json", "w") as file:
                json.dump(bookings, file, indent=4)
        except Exception as e:
            return None, f"Error saving booking: {str(e)}"
    
        return booking_info, "Car booked successfully"
    
    
    # Cancels a car booking based on the user's email and car's plate number
    @staticmethod
    def delete_booking(email, plate_number):
        # Load existing bookings from the JSON file
        try:
            with open("booked_cars.json", "r") as file:
                bookings = json.load(file)
        except FileNotFoundError:
            bookings = []  # If file not found, assume no bookings
    
        # Filter bookings to remove the one with the matching email and plate number
        bookings = [booking for booking in bookings if not (booking['car']['plate_number'] == plate_number and booking['user']['email'] == email)]
        
        # Save the updated bookings list back to the JSON file
        with open("booked_cars.json", "w") as file:
            json.dump(bookings, file, indent=4)
            
        return "Booking cancelled successfully"
