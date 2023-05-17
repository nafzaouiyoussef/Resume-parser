from flask import Flask, render_template, request
import docx2txt
import re

app = Flask(__name__)

# Define regex patterns for phone number and email address
name_regex = r'[A-Za-z]+ [A-Za-z]+'
phone_regex = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

# Define regex pattern for address
address_regex = r'\d+[^,]*,[^,]*'

# Define regex patterns for programming language skills
python_regex = r'\bpython\b|\bpython3\b'
java_regex = r'\bjava\b'
cpp_regex = r'\bc\+\+\b|\bcpp\b'
php_regex = r'\bc\+\+\b|\bphp\b'

# Define function to extract information
def extract_information(resume_text):
    # Extract name
    name = re.findall(name_regex, resume_text)
    if len(name) > 0:
        name = name[0]
    else:
        name = ''

    # Extract phone number
    phone_number = re.findall(phone_regex, resume_text)
    if len(phone_number) > 0:
        phone_number = phone_number[0]
    else:
        phone_number = ''
    
    # Extract email address
    email_address = re.findall(email_regex, resume_text)
    if len(email_address) > 0:
        email_address = email_address[0]
    else:
        email_address = ''
    
    # Extract address
    address = re.findall(address_regex, resume_text)
    if len(address) > 0:
        address = address[0]
    else:
        address = ''
    
    # Extract programming language skills
    programming_languages = []
    lang_regex_list = [(python_regex, 'Python'), (java_regex, 'Java'), (cpp_regex, 'C++'), (php_regex, 'php'),]
    for lang_regex, lang_name in lang_regex_list:
        if re.search(lang_regex, resume_text, re.IGNORECASE):
            programming_languages.append(lang_name)

    # Return a dictionary containing the extracted information
    return {'name': name, 'phone': phone_number, 'email': email_address, 'address': address, 'programming_languages': programming_languages}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    # Get the uploaded resume file
    resume_file = request.files['resume']
    
    # Check if a file was uploaded
    if resume_file:
        # Read the file contents
        resume_text = docx2txt.process(resume_file)
        
        # Extract the information from the resume text
        information = extract_information(resume_text)
        
        # Render the index.html template with the extracted information
        return render_template('index.html', information=information)
    
    # If no file was uploaded, render the index.html template without the extracted information
    return render_template('index.html')
