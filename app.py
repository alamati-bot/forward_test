from flask import Flask, request, render_template, send_from_directory, url_for,redirect
import os
import time
import unzip_files

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    return f'File uploaded successfully! <br><a href="/files">Download files</a>'

@app.route('/files', methods=['GET', 'POST'])
def list_files():
    if request.method == 'POST':
        file_to_delete = request.form.get('delete')
        if file_to_delete:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file_to_delete)
            try:
                os.remove(filepath)
                redirect(url_for('list_files'))
            except OSError as e:
                return f'Error deleting file: {e}'

    files_data = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(filepath)))
        files_data.append({'filename': filename, 'modified_time': modified_time, 'url': url_for('download_file', filename=filename)})

    return render_template('files.html', files=files_data)

@app.route('/messages')
def display_messages():
    message_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'messages.txt')
    try:
        with open(message_filepath, 'r') as f:
            messages = f.read()
            return render_template('messages.html', messages=messages)
    except FileNotFoundError:
        return "messages.txt not found."
    except OSError as e:
        return f"Error reading messages.txt: {e}"

@app.route('/extractor', methods=['GET', 'POST'])
def extractor():
    if request.method == 'POST':
        zip_file_to_extract = request.form.get('extract')
        if zip_file_to_extract:
            zip_filepath = os.path.join(app.config['UPLOAD_FOLDER'], zip_file_to_extract)
            unzip_files.extractor(zip_filepath,"adab")


    zip_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.endswith('.zip')]
    return render_template('extractor.html', zip_files=zip_files)

@app.route('/files/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



if __name__ == '__main__':
    app.run(debug=True)
