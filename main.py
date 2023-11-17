from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'a20a90eb88d6db187d558a3c'

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
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
