from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Define the User class
class User:
    def __init__(self, first_name, last_name, email, phone, government, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.government = government
        self.password = password

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


@app.route('/')
def index():
    return render_template('index.html')

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

        # Validate email and password
        email = email.lower().strip()
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
                new_user = User(first_name, last_name, email, phone, government, password)
                new_user.save_to_file()
                session['user_id'] = email
                return redirect(url_for('index'))

    return render_template('sign_up.html', validation_message=message)

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
                return redirect(url_for('index'))
        message = "Invalid email or password"
    return render_template('sign_in.html', message=message)




if __name__ == '__main__':
    app.run(debug=True)
