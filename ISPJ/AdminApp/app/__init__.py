from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from prometheus_client import Counter, generate_latest
import os, csv
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Placeholder user database
users = {
    'admin': {'password': generate_password_hash('admin123'), 'role': 'admin'},
    'staff': {'password': generate_password_hash('staff123'), 'role': 'staff'},
    'patient': {'password': generate_password_hash('patient123'), 'role': 'patient'}
}

# Define counters for login attempts
login_attempts = Counter('admin_login_attempts_total', 'Total login attempts', ['status'])
admin_views = Counter('admin_views_total', 'Admin page views', ['page'])

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(username):
    if username not in users:
        return None
    user = User()
    user.id = username
    return user

@app.route('/')
def home():
    admin_views.labels(page='admin_home').inc()
    return render_template('admin_login.html')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    admin_username = "admin1"
    admin_password = "admin123"
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username:
            password == admin_password
            if password == admin_password:
                # Increment successful login counter
                login_attempts.labels(status='success').inc()
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password.', 'error')
                login_attempts.labels(status='password_failed').inc()
                return redirect(url_for('admin_login'))
        else:
            # Increment failed login counter
            login_attempts.labels(status='username_failed').inc()
            flash('Invalid username or password.', 'error')
    
    # Increment page view counter
    admin_views.labels(page='login').inc()
    return render_template('admin_login.html')

@app.route('/admin_dashboard')
def admin_dashboard():
    # # increment dash view counter

    # # Sample data for User Login Activity
    # login_dates = ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05']
    # login_counts = [50, 75, 60, 80, 90]

    # # Sample data for Failed Login Attempts
    # failed_login_periods = ['Week 1', 'Week 2', 'Week 3', 'Week 4']
    # failed_login_counts = [5, 7, 3, 9]
    
    # # Sample data for Document Uploads and Downloads
    # dates = ['2023-10-01', '2023-10-02', '2023-10-03', '2023-10-04', '2023-10-05']
    # uploads = [20, 30, 25, 35, 45]
    # downloads = [15, 25, 20, 30, 40]

    # # Create Plotly charts
    # login_activity_fig = go.Figure(data=[
    #     go.Scatter(x=login_dates, y=login_counts, mode='lines+markers', name='Logins', line=dict(color='blue'))
    # ])
    # login_activity_fig.update_layout(title='User Login Activity Over Time', xaxis_title='Date', yaxis_title='Number of Logins')

    # failed_logins_fig = go.Figure(data=[
    #     go.Bar(x=failed_login_periods, y=failed_login_counts, name='Failed Logins', marker=dict(color='red'))
    # ])
    # failed_logins_fig.update_layout(title='Failed Login Attempts by Week', xaxis_title='Week', yaxis_title='Number of Failed Attempts')

    # document_activity_fig = go.Figure(data=[
    #     go.Scatter(x=dates, y=uploads, fill='tozeroy', mode='none', name='Uploads', fillcolor='rgba(0, 128, 0, 0.5)'),
    #     go.Scatter(x=dates, y=downloads, fill='tonexty', mode='none', name='Downloads', fillcolor='rgba(0, 0, 255, 0.5)')
    # ])
    # document_activity_fig.update_layout(title='Document Uploads and Downloads Over Time', xaxis_title='Date', yaxis_title='Number of Documents')

    # # Convert charts to HTML
    # login_activity_html = pio.to_html(login_activity_fig, full_html=False)
    # failed_logins_html = pio.to_html(failed_logins_fig, full_html=False)
    # document_activity_html = pio.to_html(document_activity_fig, full_html=False)

    admin_views.labels(page='admin_dashboard').inc()
    return render_template('admin_dashboard.html')

@app.route('/admin_notif')
def admin_notif():
    notifications = []
    try:
        with open('log.csv', 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['levelname'] in ['ERROR', 'CRITICAL']:
                    notifications.append({
                        'datetime': row['asctime'],  # Assuming 'asctime' is the first column
                        'description': row['message'],  # Assuming 'message' is the second column
                        'level': row['levelname'],  # Assuming 'levelname' is the third column
                        'user_id': '12'  # Assuming 'user_id' is a field in the CSV
                    })
                print(notifications)
    except FileNotFoundError:
        flash('No logs found', 'warning')
        notifications = []
        
    admin_views.labels(page='admin_notification').inc()
    return render_template('admin_notif.html', notifications=notifications)

@app.route('/restrict_user/<int:user_id>', methods=['POST'])
def restrict_user(user_id):
    return "User restricted"


@app.route('/disable_user/<int:user_id>', methods=['POST'])
def disable_user(user_id):
    return "User disabled"


@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    return "User deleted"

@app.route('/metrics')
def metrics():
    return generate_latest()



# Import database session
from database import engine, Base, dbSession  # Ensure dbSession and engine are imported
from sqlalchemy.exc import SQLAlchemyError
from DBcreateTables import Message, CommentFailure  # Import models
from dotenv import load_dotenv
import base64  # 🔹 Fixes "name 'base64' is not defined"
import bleach  # 🔹 Fixes "name 'bleach' is not defined"
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from flask import send_from_directory


dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'AdminApp', 'app', '.env'))
load_dotenv(dotenv_path)
import logging
logging.basicConfig(level=logging.INFO)


# Define the correct uploads folder for screenshots
SCREENSHOT_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'ConsumerApp', 'app', 'static', 'uploads')
)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(SCREENSHOT_FOLDER, filename)


def mask_email(email):
    """Mask the email, showing only the first letter and domain."""
    if email:
        local, domain = email.split('@')
        return local[:1] + "****@" + domain  # Example: "j****@gmail.com"
    return email

@app.route('/unmask_email/<int:message_id>')
def unmask_email(message_id):
    """Fetches the decrypted full email for a specific message."""
    message = dbSession.query(Message).get(message_id)
    if not message:
        return jsonify({"error": "Message not found"}), 404

    decrypted_email = decrypt_kenzie(aes_key_kenzie, message.email)
    return jsonify({"email": decrypted_email})


# AES Encryption setup
key_hex_kenzie = os.getenv('AES_KEY_kenzie')
aes_key_kenzie = bytes.fromhex(key_hex_kenzie)


def decrypt_kenzie(key, encrypted_data):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        iv = encrypted_data[:AES.block_size]
        encrypted_data = encrypted_data[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = cipher.decrypt(encrypted_data)
        return unpad(padded_data, AES.block_size).decode('utf-8')
    except Exception as e:
        logging.error(f"Decryption error: {e}")
        return ''

# Ensure fresh database queries on every request
@app.before_request
def refresh_session():
    dbSession.expire_all()  # Force all objects to refresh on next query

@app.route('/retrieveMessages')
def retrieve_messages():
    """Fetch latest messages from the database with masked emails."""
    with app.app_context():
        dbSession.rollback()  # Undo uncommitted changes
        dbSession.expire_all()  # Force fresh queries

        messages_list = dbSession.query(
            Message.id,
            Message.name,
            Message.email,
            Message.message,
            Message.screenshot
        ).order_by(Message.date_added).all()

        sanitized_messages = [
            {
                'id': m.id,
                'name': bleach.clean(m.name, strip=True),
                'masked_email': bleach.clean(mask_email(decrypt_kenzie(aes_key_kenzie, m.email)) or '', strip=True),  # Masked email format
                'full_email': bleach.clean(decrypt_kenzie(aes_key_kenzie, m.email) or '', strip=True),  # Full email for unmasking
                'message': bleach.clean(decrypt_kenzie(aes_key_kenzie, m.message) or '', strip=True),
                'screenshot': m.screenshot
            } for m in messages_list
        ]

    return render_template('retrieveMessages.html', count=len(sanitized_messages), messages_list=sanitized_messages)




@app.route('/deleteMessages/<int:id>', methods=['POST'])
def delete_messages(id):
    """Deletes a message and removes the screenshot if it exists."""
    message = dbSession.query(Message).get(id)
    if not message:
        flash("Message not found.", "danger")
        return redirect(url_for('retrieve_messages'))

    # Delete associated screenshot
    if message.screenshot:
        file_path = os.path.join(SCREENSHOT_FOLDER, message.screenshot)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")

    try:
        dbSession.delete(message)
        dbSession.commit()
        flash("Message and screenshot deleted successfully.", "success")
    except SQLAlchemyError as e:
        dbSession.rollback()
        flash(f"Error deleting message: {e}", "danger")

    return redirect(url_for('retrieve_messages'))
    

@app.route('/view_errors')
def view_errors():
    """Retrieve latest error logs from database on every refresh."""
    with app.app_context():
        dbSession.rollback()  # Undo any uncommitted changes to prevent stale data
        dbSession.expire_all()  # Expire session AFTER fetching
        failures = dbSession.query(CommentFailure).order_by(CommentFailure.id.asc()).all()
    
    return render_template('view_errors.html', failures=failures)


if __name__ == '__main__':
    with app.app_context():
        Base.metadata.create_all(engine)  # Ensure tables exist at startup
    # if not os.path.exists(app.config['UPLOAD_FOLDER']):
    #     os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True, port=5001)