from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import model_users

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# ******************** DISPLAY ROUTES ********************

@app.route('/')
def register():
    return render_template('index.html')

# ******************** ACTION ROUTES ********************

@app.route('/user/process_login', methods=['POST'])
def index():
    user = model_users.User.get_one_email(email = request.form['user_input'])

    is_valid = True

    if not user:
        flash("Invalid Credentials", "user_input")
        is_valid = False

    if "password" in request.form and len(request.form['password']) < 8:
        flash("Must input a password", "password")
        is_valid = False

    if user:
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            is_valid = False
            flash('Invalid Credentials', "user_input")

    if not is_valid:
        return redirect('/')

    session['id'] = user.id
    return redirect('/dashboard')

@app.route('/user/create', methods=['POST'])
def create_user():
    is_valid = model_users.User.validate_users(request.form)
    if not is_valid:
        return redirect('/')
    password = bcrypt.generate_password_hash(request.form['password'])

    data = {
        **request.form,
        'password': password
    }

    user_id = model_users.User.create(data)
    session['id'] = user_id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect('/')