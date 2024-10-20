Test Case Generator with Google Generative AI

**Project Overview**
This project is a Test Case Generator web application built using Flask, designed to interact with Google's Gemini Pro Model for generating test cases based on user-provided functionality. Users can login, register, generate test cases in JSON format, and download them as an Excel file.
Key Technologies Used:
•	Flask: Backend web framework
•	SQLite: Database to store user credentials
•	Google Generative AI (Gemini Model): To generate test cases
•	Xlsxwriter: Python module to create Excel files
•	HTML/CSS: Basic front-end templates
•	PythonAnywhere (Deployed)

**Project Structure**
GenAI/
│
├── app.py             # Main application file
├── database.py        # Database file (SQLite setup)
├── config.py          # API key configuration file for Google AI
├── templates/         # HTML templates
│   ├── index.html     # Home page
│   ├── login.html     # Login page
│   └── register.html  # Register page
├── auth/              # Authentication functions (login/register)
│   ├── login.py
│   └── register.py


**Folder and File Descriptions:**

1.	app.py:
o	Main Flask application.
o	Handles routing for home, login, register, and test case generation.
o	Contains Google Generative AI integration for generating test cases.
o	Manages Excel file creation and download.

2.	database.py:
o	Handles the initialization of SQLite database.
o	Creates a table users for storing username, password, email, and phone for authentication purposes.

3.	config.py:
o	Stores the API key for the Google Generative AI. The API key is required to use the Gemini Pro model.
o	Ensure that config.py is not included in version control (e.g., GitHub) for security reasons. Include it in .gitignore.

4.	auth/login.py & auth/register.py:
o	Contains the login and register functionality, handling form data, authentication, and registration.

5.	templates/:
o	This folder contains the HTML files that make up the front end of the application.
o	index.html: Home page
o	login.html: Login page
o	register.html: Registration page

**Features**
1. Authentication (Login/Register)
•	Login: Users can login using their registered email and password.
•	Register: New users can create an account by providing their username, email, phone, and password.
•	Logout: Logged-in users can log out of the session.
2. Test Case Generation
•	Users can enter a functionality name, and the application interacts with Google's Generative AI to generate unique test cases in JSON format.
•	The application provides an option to generate additional test cases if required.
3. Test Case Download
•	Users can download the generated test cases as an Excel file using the XlsxWriter Python library.

**Setup Instructions**
To set up and run this project locally or on any server, follow these steps:

Prerequisites:
•	Python 3.x
•	pip (Python package installer)
•	API Key for Google Generative AI (Gemini model)

1. Clone the Repository
git clone <repository-url>
cd GenAI

2. Create Virtual Environment 
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

3. Install Required Dependencies
pip install -r requirements.txt

4. Set Up the Database
Run the following Python command to initialize the SQLite database
python3 -c "import database; database.initialize_db()"
This will create the users table in an SQLite file to store user credentials.

5. Add Google Generative AI API Key
•	Create a config.py file.
•	Add the following code and replace 'YOUR_API_KEY' with your actual API key:
API_KEY = 'YOUR_API_KEY'

6. Run the Application
python app.py
Navigate to http://127.0.0.1:5000 in your browser to access the application.

