from flask import render_template, request, redirect, url_for, flash
from database import add_user

def handle_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        if add_user(username, password, email, phone):
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login_page'))
        else:
            flash('Registration failed. Username or email may already be taken.', 'danger')

    return render_template('register.html')
