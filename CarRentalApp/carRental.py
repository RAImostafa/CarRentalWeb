from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import datetime
from user import User
from car import Car
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    message = ""
    if request.method == 'POST':
        form_data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'phone': request.form['phone'],
            'government': request.form['government'],
            'password': request.form['password']
        }
        message, user = User.sign_up(form_data)
        if user:
            return redirect(url_for('home'))
    return render_template('sign_up.html', message=message)





@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    message = ""
    if request.method == 'POST':
        form_data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        message, first_name, role = User.sign_in(form_data)
        if first_name:
            return f'''
            <script>
            localStorage.setItem('first_name', '{first_name}');
            window.location.href = "/{role}";
            </script>
            '''
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
                #welcome_message = f"Welcome back, {user['first_name']}!"
                welcome_message = f"Welcome back, {user.get('first_name', 'User')}!"

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
    booking_info, message = Car.book_car(user, car_model)

    if not booking_info:
        return jsonify({"message": message}), 404 if message == "Car not found" else 409

    return jsonify({"message": message}), 200



@app.route('/delete_booking', methods=['POST'])
def delete_booking():
    if 'user_id' not in session:
        return jsonify({"message": "User not logged in"}), 401

    email = session['user_id']
    car_model = request.json['car_model']

    message = Car.delete_booking(email, car_model)
    return jsonify({"message": message}), 200




# ************************************** ADMIN Funs *********************************
@app.route('/admin_page')
def admin_page():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    
    admin = User.get_admin_user()
    if admin:
        cars = Car.get_cars()
        booked_cars = User.get_booked_cars()
        return render_template('admin.html', cars=cars, booked_cars=booked_cars)
    else:
        return redirect(url_for('home'))


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    message = ""
    if request.method == 'POST':
        file = request.files['image_path']
        form_data = request.form
        message = User.add_car(form_data, file)
        if not message:
            return redirect(url_for('admin_page'))
    return render_template('add_car.html', message=message)

@app.route('/admin/remove_booking', methods=['POST'])
def remove_booking():
    car_model = request.form['model']
    User.remove_booking(car_model)
    return redirect(url_for('admin_page'))

@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()
    model_to_delete = data.get('model')
    car_deleted = User.delete_car(model_to_delete)
    if car_deleted:
        return jsonify({"success": True, "message": "Car and its booking removed successfully."})
    else:
        return jsonify({"success": False, "message": "Car not found."})

@app.route('/booked_cars')
def booked_cars():
    grouped_bookings = User.get_booked_cars()
    return render_template('booked_cars.html', grouped_bookings=grouped_bookings)


@app.route('/edit_car/<car_model>', methods=['GET', 'POST'])
def edit_car(car_model):
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    email = session['user_id']
    users = User.get_list()
    user = next((user for user in users if user['email'] == email), None)

    if user and user.get('role') == 'admin':
        cars = Car.get_cars()
        selected_car = next((car for car in cars if car.model == car_model), None)
        
        if request.method == 'POST':
            # Update car details from form data
            selected_car.image = request.form['image']
            selected_car.car_type = request.form['car_type']
            selected_car.capacity = request.form['capacity']
            selected_car.doors = request.form['doors']
            selected_car.luggage = request.form['luggage']
            selected_car.transmission = request.form['transmission']
            selected_car.location = request.form['location']
            selected_car.price = request.form['price']
            selected_car.duration = request.form['duration']
            selected_car.owner = request.form['owner']
            selected_car.phone = request.form['phone']
            selected_car.plate_number = request.form['plate_number']

            # Save updated car details back to cars.txt
            with open('cars.txt', 'w') as file:
                for car in cars:
                    file.write("|".join([car.image, car.model, car.car_type, str(car.capacity), str(car.doors), str(car.luggage), car.transmission, car.location, car.price, car.duration, car.owner, car.phone, car.plate_number]) + "\n")

            return redirect(url_for('admin_page'))

        return render_template('edit_car.html', car=selected_car)
    
    return redirect(url_for('home'))





if __name__ == '__main__':
    app.run(debug=True)
