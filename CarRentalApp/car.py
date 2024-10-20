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
