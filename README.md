CarRentalWeb
A website that helps users book cars from a variety of models and prices.

What does it do?
Users can book one or more cars, cancel reservations, and view car prices and owner information. An admin can add or remove cars, view the booked list, and cancel bookings.

New feature
A better user profile that displays the booked cars and ensures that deleting a car from the system also removes it from the user's booking list.

Prerequisites
Make sure you have the following installed:

Python: Install Python from the official website: python.org
Flask: Install Flask using pip by running this command:
bash
Copy code
pip install Flask
Jinja in Visual Studio Code: Ensure you have Visual Studio Code installed. Jinja is integrated into Visual Studio Code by default with the Python extension.
Project Checklist
[✔️] It is available on GitHub: https://github.com/RAImostafa/CarRentalWeb
[✔️] It uses the Flask web framework.
[✔️] It uses at least one module from the Python Standard Library (other than the random module).
Modules used:
datetime
json
os
[✔️] It contains at least one custom class with both properties and methods, and uses __init__() to initialize attributes:
User class in user.py:
Line number for class definition: 9
Properties: first_name, email
Methods: sign_up(), sign_in()
Methods used in:
sign_up() in app.py at line 16
sign_in() in app.py at line 33
Car class in car.py:
Line number for class definition: 2
Properties: model, car_type
Methods: get_cars(), book_car()
Methods used in:
get_cars() in app.py at line 95, line 114, and line 165
book_car() in app.py at line 134
[✔️] It uses JavaScript in the frontend and localStorage:
localStorage is used in signup.js at line 3
[✔️] It uses modern JavaScript (let/const instead of var):
const in profile.js at lines 2, 3
let in home.js at lines 66, 67
Arrow functions in add_car.js at line 30
[✔️] It makes use of reading and writing to the same file:
cars.txt:
Adding a car: add_car() in user.py at line 99
Reading cars: get_cars() in car.py at line 19
Deleting a car: delete_car() in user.py at line 156
[✔️] It contains conditional statements.
File name: app.py
Lines: 13, 25, 33, 39, 51, 65, 79, 82, 102, 114, 126, 130, 134, 148, 158, 162, 175, 178, 192
[✔️] It contains loops.
File name: app.py
Lines: 58, 66, 115, 129
File name: user.py
Lines: 55, 69, 73, 89, 121, 151, 162, 176
File name: car.py
Lines: 22, 23, 29, 40, 63
[✔️] It allows users to enter values in text boxes, which are processed in the backend:
Sign in, sign up fields
Admin adding a car
Searching functionality
[✔️] It handles incorrect inputs gracefully using try/except blocks.
[✔️] It is styled using custom CSS.
[✔️] The code follows the course's style and documentation conventions. It is fully documented and does not contain unused code.
