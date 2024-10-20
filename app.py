from flask import Flask, render_template, redirect, url_for
from auth import login, register
import database


app = Flask(__name__)
app.secret_key = 'Ngk@0625'  # Required for session management

# Home Page
@app.route('/')
def home_page():
    return render_template('Home.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    return login.handle_login()

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    return register.handle_register()

# Logout route definition
@app.route('/logout')
def logout():
    return login.logout()





import os
import config
from flask import request, jsonify, send_file
import google.generativeai as genai
import json
import xlsxwriter
import io


# Initialize Google Generative AI with the API key
genai.configure(api_key=config.API_KEY)

# Create a Gemini Pro model instance
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# In-memory storage for test cases to track existing ones and ensure uniqueness
all_test_cases = []
test_case_counter = 0  # Tracks the total number of generated test cases

@app.route('/test')
def test():
    return render_template('Test_cases.html')

def generate_prompt(functionality, start_case_number=1):
    prompt = f"""
    Generate a list of 10 unique test cases for the functionality: "{functionality}" in strict JSON format. Each test case must have a unique Name, description, and input/output format. Number the test cases starting from {start_case_number}. Ensure the format is valid JSON, and no test case should repeat any previous ones. Follow this structure:
    [
      {{
        "Name": "Test Case {start_case_number}",
        "description": "Short description",
        "input": {{
          "username": "example_username",
          "password": "example_password"
        }},
        "output": "Expected output."
      }},
      {{
        "Name": "Test Case {start_case_number+1}",
        "description": "Short description",
        "input": {{
          "username": "example_username",
          "password": "example_password"
        }},
        "output": "Expected output."
      }}
    ]
    """
    return prompt

@app.route('/generate_test_cases', methods=['POST'])
def generate_test_cases():
    global all_test_cases, test_case_counter

    functionality = request.form.get('functionality')

    if not functionality:
        return jsonify({"error": "Functionality is required."}), 400

    # Reset the counter and test case storage for new functionality
    all_test_cases = []
    test_case_counter = 0

    prompt = generate_prompt(functionality, start_case_number=1)

    try:
        response = model.generate_content(prompt)
        generated_text = response.text

        try:
            test_cases = json.loads(generated_text)
        except json.JSONDecodeError:
            return jsonify({
                "error": "Failed to parse test cases. Check the response format.",
                "response": generated_text
            }), 500

        test_case_counter += len(test_cases)
        all_test_cases.extend(test_cases)

        return jsonify({"test_cases": test_cases})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate_more_test_cases', methods=['POST'])
def generate_more_test_cases():
    global all_test_cases, test_case_counter

    functionality = request.form.get('functionality')

    if not functionality:
        return jsonify({"error": "Functionality is required."}), 400

    prompt = generate_prompt(functionality, start_case_number=test_case_counter + 1)

    try:
        response = model.generate_content(prompt)
        generated_text = response.text

        try:
            new_test_cases = json.loads(generated_text)
        except json.JSONDecodeError:
            return jsonify({
                "error": "Failed to parse new test cases. Check the response format.",
                "response": generated_text
            }), 500

        # Ensure uniqueness by comparing new test cases to existing ones
        unique_test_cases = [case for case in new_test_cases if case not in all_test_cases]

        test_case_counter += len(unique_test_cases)
        all_test_cases.extend(unique_test_cases)

        return jsonify({"new_test_cases": unique_test_cases})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Download all test cases as an Excel file
@app.route('/download_test_cases', methods=['GET'])
def download_test_cases():
    if not all_test_cases:
        return jsonify({"error": "No test cases available to download."}), 400

    # Create an in-memory output file to send the Excel file
    output = io.BytesIO()

    # Create a new Excel file using XlsxWriter
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    # Write headers
    worksheet.write(0, 0, 'Test Case Name')
    worksheet.write(0, 1, 'Description')
    worksheet.write(0, 2, 'Input')
    worksheet.write(0, 3, 'Expected Output')

    # Write test cases to the Excel file (update 'Name' to match your JSON key structure)
    for row_num, test_case in enumerate(all_test_cases, 1):
        worksheet.write(row_num, 0, test_case['Name'])  # 'Name' with a capital "N"
        worksheet.write(row_num, 1, test_case['description'])
        worksheet.write(row_num, 2, str(test_case['input']))
        worksheet.write(row_num, 3, test_case['output'])

    workbook.close()

    # Rewind the buffer to the beginning so Flask can send the file
    output.seek(0)
    return send_file(output, download_name='test_cases.xlsx', as_attachment=True)


    #return send_file(output, attachment_filename='test_cases.xlsx', as_attachment=True)




if __name__ == '__main__':
    database.initialize_db()
    app.run(debug=True)
