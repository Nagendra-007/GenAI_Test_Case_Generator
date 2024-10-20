from flask import Blueprint, render_template, request, redirect, url_for
from database import authenticate_user

login = Blueprint('login', __name__)

@login.route('/login', methods=['GET', 'POST'])
def handle_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Authenticate user using the authenticate_user function from the database module
        if authenticate_user(username, password):
            return redirect(url_for('test'))  # Redirect to home page or dashboard on successful login
        else:
            error = "Incorrect login details"
    
    return render_template('login.html', error=error)

# Logout route definition
@login.route('/logout')
def logout():
    # Clear the session to log the user out
    #session.clear()

    # Flash message for successful logout
    #flash("You have been logged out successfully.", "info")
    
    # Redirect the user to the login page or home page after logging out
    return redirect(url_for('login'))
