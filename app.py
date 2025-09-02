from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import json  # New import

load_dotenv()

app = Flask(__name__)

# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# Initialize Flask-Mail
mail = Mail(app)

# This is the root route. It serves the HTML file for your frontend.
@app.route('/')
def home():
    """Renders the frontend HTML page."""
    # Load the Firebase config from the .env file
    firebase_config_str = os.environ.get('FIREBASE_CONFIG')
    firebase_config = json.loads(firebase_config_str) if firebase_config_str else {}
    
    # Pass the config to the HTML template
    return render_template('frontend.html', firebase_config=json.dumps(firebase_config))

@app.route('/send_email', methods=['POST'])
def send_email():
    """
    Handles the contact form submission and sends an email.
    """
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        service = data.get('service')
        message_content = data.get('message')

        msg_body = (
            f"You have a new inquiry from Ingwenyakazi.\n"
            f"----------------------------------------\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Service of Interest: {service}\n"
            f"Message: {message_content}\n"
            f"----------------------------------------\n"
        )
        
        msg = Message(
            subject=f"New Inquiry from {name} - {service}",
            recipients=[app.config['MAIL_DEFAULT_SENDER']],
            body=msg_body
        )

        mail.send(msg)
        
        print("Received a new inquiry and sent email:")
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Service: {service}")
        print(f"Message: {message_content}")
        print("-" * 20)
        
        return jsonify({"success": True, "message": "Inquiry received successfully."})

    except Exception as e:
        print(f"Error processing form submission: {e}")
        return jsonify({"success": False, "message": "An internal error occurred."}), 500

if __name__ == '__main__':
    # You must have a .env file with MAIL_PASSWORD and MAIL_USERNAME
    # to run this application.
    app.run(debug=True)