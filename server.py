from flask import Flask, request, send_from_directory, render_template, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import secrets  
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 * 1024 
UPLOAD_FOLDER = 'uploads'  
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'tar', 'gz', 'mp4', 'mkv', 'iso'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def index():
    return render_template('download.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)      
    file = request.files['file']   
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)      
    if not allowed_file(file.filename):
        flash('File type not allowed', 'error')
        return redirect(request.url)
    filename = secure_filename(file.filename)    
    try:
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        flash('File uploaded successfully', 'success')
    except Exception as e:
        flash(f'An error occurred while saving the file: {str(e)}', 'error')   
    return redirect(url_for('index'))
@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(UPLOAD_FOLDER, filename)
    except FileNotFoundError:
        flash('File not found', 'error')
        return redirect(url_for('list_files'))
@app.route('/files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER) 
    return render_template('file_list.html', files=files) 
if __name__ == '__main__':
    app.run(host='Your_ip', port=5000, debug=True)
