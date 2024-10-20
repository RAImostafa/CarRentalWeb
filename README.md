# CarRentalWeb
it's a website that helps you to book the cars with a huge variety of models and prices 

- What does it do?
you can book a car or more and cancel the reservation ,it also shows their perices
and all the car and the owner info
with an admin that car add a new car or remove a car , watch the booked list and cancel booking.

- What is the "new feature" which you have implemented that
we haven't seen before?
better user profile that contains the car he booked , also deleteing car from the system
removes it from the booked list in the user's profile 

## Prerequisites
make sure you got this :
Python: Install Python from the official website: python.org
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