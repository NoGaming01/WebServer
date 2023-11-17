from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'a20a90eb88d6db187d558a3c'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configure Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Mock user database (replace with a proper database in a real application)
users = {'user1': {'username': 'user1', 'password': 'password1'},
         'user2': {'username': 'user2', 'password': 'password2'}}

@login_manager.user_loader
def load_user(user_id):
    user_data = users.get(user_id)
    if user_data:
        user = User(user_data['username'])
        return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = users.get(username)
        if user_data and password == user_data['password']:
            user = User(username)
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        flash('Invalid username or password', 'error')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    folders = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', folders=folders)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        file.save(f'uploads/{file.filename}')
        return 'File uploaded successfully'

def secure_filename(filename):
    # This function ensures that the filename is safe to use on Windows
    # You can replace this function with a more comprehensive one if needed
    return ''.join(c if c.isalnum() or c in ('.', '_') else '_' for c in filename)

@app.route('/download/<filename>')
def download_file(filename):
    # Replace spaces with underscores in the filename
    sanitized_filename = secure_filename(filename)
    
    # Rename the file by replacing spaces with underscores
    original_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    new_path = os.path.join(app.config['UPLOAD_FOLDER'], sanitized_filename)
    
    os.rename(original_path, new_path)
    
    # Send the renamed file for download
    return send_from_directory(app.config['UPLOAD_FOLDER'], sanitized_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
