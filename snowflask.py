from flask import Flask, send_from_directory, render_template, abort
from werkzeug.utils import safe_join
import os
import socket

app = Flask(__name__)
BASE_DIR = os.path.join(os.path.dirname(__file__), 'Uploads')

# Get local IP automatically
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "localhost"

def get_directory_structure(root_dir):
    """
    Recursively builds nested folder structure starting at root_dir.
    Each folder is a dict: {name, files, subfolders}
    """
    folder_name = os.path.relpath(root_dir, BASE_DIR)
    if folder_name == '.':
        folder_name = 'Uploads'  # Show root as 'Uploads'

    structure = {
        'name': folder_name,
        'files': [],
        'subfolders': []
    }

    try:
        with os.scandir(root_dir) as it:
            for entry in it:
                if entry.is_file():
                    structure['files'].append(entry.name)
                elif entry.is_dir():
                    subfolder_structure = get_directory_structure(entry.path)
                    structure['subfolders'].append(subfolder_structure)
    except PermissionError:
        pass  # Skip folders we can't access

    return structure

@app.route('/')
def index():
    directory_structure = get_directory_structure(BASE_DIR)
    # Pass as list so template can iterate easily
    return render_template('index.html', structure=[directory_structure], os=os)

@app.route('/download/<path:filename>')
def download_file(filename):
    # Sanitize the path to prevent directory traversal
    safe_path = safe_join(BASE_DIR, filename)
    if not safe_path or not os.path.isfile(safe_path):
        abort(404)
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    ip = get_local_ip()
    port = 6002
    print("\n======================================")
    print("❄️  snow.flask - Retro File Server")
    print("Serving files from:", BASE_DIR)
    print(f"Access the server on this device: http://localhost:{port}")
    print(f"Access from other devices:     http://{ip}:{port}")
    print("======================================\n")
    app.run(host='0.0.0.0', port=port)
