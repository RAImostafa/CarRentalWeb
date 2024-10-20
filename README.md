CarRentalWeb
A website that helps users book cars from a variety of models and prices.

What does it do?
Users can book one or more cars, cancel reservations, and view car prices and owner information. An admin can add or remove cars, view the booked list, and cancel bookings.

New feature
A better user profile that displays the booked cars and ensures that deleting a car from the system also removes it from the user's booking list.

Prerequisites
Make sure you have the following installed:

Python: Install Python from the official website: python.org
<<<<<<< HEAD
Flask: You can install Flask using pip, Python's package installer. Run the following command:  pip install Flask
Jinja in Visual Studio Code: Ensure you have Visual Studio Code installed. Jinja is a templating engine used by Flask, and it should be integrated into Visual Studio Code by default when you have the Python extension installed.

## Project Checklist
-[✔️] It is available on GitHub. (https://github.com/RAImostafa/CarRentalWeb)
-[✔️] It uses the Flask web framework.
-[✔️] It uses at least one module from the Python Standard
Library other than the random module.
Module name: 1-datetime
               2-json
               3-OS
-[✔️] It contains at least one class written by you that has
both properties and methods. It uses `__init__()` to let the
class initialize the object's attributes (note that
`__init__()` doesn't count as a method). This includes
instantiating the class and using the methods in your app. 
                1- File name for the class definition: car.py and user.py
                2-For the User class in user.py:
                    Line number(s) for the class definition: Line 9 
                    Name of two properties: first_name, email
                    Name of two methods: sign_up(), sign_in()
                    File name and line numbers where the methods are used:
                    File name: carRental.py
                    Line numbers for sign_up(): Line 16 (inside the /sign_up route).
                    Line numbers for sign_in(): Line 33 (inside the /sign_in route).
                2-For the Car class in car.py:
                    File name for the class definition: car.py
                    Line number(s) for the class definition: Line 2
                    Name of two properties: model, car_type
                    Name of two methods: get_cars(), book_car()
                    File name and line numbers where the methods are used:
                    File name: carrental.py
                    Line numbers for get_cars(): Used in the /home route at line 95, /car/<car_model> route 114,/admin_page route at line 165 .
                    Line numbers for book_car(): Used in the /book_car route at line 134.

-[✔️] It makes use of JavaScript in the front end and uses the
localStorage of the web browser.
                1-"localStorage" is used in signup.js at line 3

-[✔️] It uses modern JavaScript (for example, let and const rather than var).
                1-const is used in "profile.js" at line 2,3 
                2-let is used in "home.js" at line 66 ,67
                3-Arrow function for DOMContentLoaded event listener in "add_car.js" at line 30

-[✔️] It makes use of the reading and writing to the same file feature.
                cars.txt
                1- in the admin can *add* a car by func add_car() at line 99 , in "user.py" 
                2- cars can be *read* through get_cars() at line 19 , in "car.py"
                3-admin can *delete* a car too by func delete_car(model_to_delete) at line 156 , in "user.py" 

-[✔️] It contains conditional statements.
                file name : carRental.py
                lines:

-[✔️] It contains loops. Please provide below the file name and the line number(s) of at least
                 one example of a loop in your code.
                 - File name:carRental.py
                 - Line number(s):58,66,115,129
                 - File name:user.py
                 - Line number(s):55,69,73,89,121,151,162,176,...
                 - File name:car.py
                 - Line number(s):22,23,29,40,63

-[✔️] It lets the user enter a value in a text box at some point This value is received and processed by your back end Python code.
                - used in Sign in and sign up fileds 
                -Adding car by admin
                -searching 

-[✔️] It doesn't generate any error message even if the user enters a wrong input.
                 -done through try and catch 

-[✔️] It is styled using your own CSS

- [✔️] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. In particular, the code should not use `print()` or
`console.log()` for any information the app user should see.
Instead, all user feedback needs to be visible in the
browser. 

-[✔️] All exercises have been completed as per the
requirements and pushed to the respective GitHub repository
=======
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
>>>>>>> 0e6798c954c858ffa05615122a1a0b8a4136a35d
