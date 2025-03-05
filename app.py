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

@app.route('/directory', methods=['GET', 'POST'])
def list_directory():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    if request.method == 'POST':
        action = request.form.get('action')
        path = request.form.get('path')
        if action == 'delete':
            full_path = os.path.join(base_dir, path)
            try:
                if os.path.isfile(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    # For deleting directories, handle potential errors more robustly
                    import shutil
                    shutil.rmtree(full_path)
                return jsonify({'success': True, 'message': 'Item deleted successfully.'})
            except OSError as e:
                return jsonify({'success': False, 'message': f'Error deleting item: {e}'})
        elif action == 'download':
            full_path = os.path.join(base_dir, path)
            try:
                return send_from_directory(base_dir, path, as_attachment=True)
            except FileNotFoundError:
                return jsonify({'success': False, 'message': 'File not found.'})


    try:
      # Get the base directory of your app
      base_dir = os.path.dirname(os.path.abspath(__file__))

      # Function to recursively list files and directories
      def get_directory_structure(directory, parent_path=""):
          structure = []
          for item in os.listdir(directory):
              item_path = os.path.join(directory, item)
              full_path = os.path.join(parent_path,item) if parent_path else item
              if os.path.isdir(item_path):
                  structure.append({'name': item, 'type': 'directory', 'path': full_path, 'children': get_directory_structure(item_path, full_path)})
              else:
                  structure.append({'name': item, 'type': 'file', 'path': full_path})
          return structure

      directory_structure = get_directory_structure(base_dir)
      return render_template('directory.html', directory_structure=directory_structure)
    except OSError as e:
      return f"Error accessing directory: {e}"

@app.route('/messages', methods=['GET', 'POST'])
def display_messages():
    message_filepath = 'messages.txt'
    if request.method == 'POST':
        if request.form.get('delete_messages'):
            try:
                with open(message_filepath, 'w') as f: # Open in write mode to truncate
                    pass # This effectively clears the file
                return redirect(url_for('display_messages'))
            except FileNotFoundError:
                return "messages.txt not found."
            except OSError as e:
                return f"Error clearing messages.txt: {e}"

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
    app.run(debug=True, host='0.0.0.0', port=5000)
