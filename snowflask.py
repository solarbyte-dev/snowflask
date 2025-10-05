from flask import Flask, send_from_directory, render_template, url_for
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

@app.route('/')
def index():
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    return render_template('index.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    ip = get_local_ip()
    port = 6002
    print("\n======================================")
    print("❄️  snow.flask - Retro File Server")
    print("Serving files from:", BASE_DIR)
    print(f"Access the server on this device: http://localhost:6002")
    print(f"Access from other devices:     http://{ip}:6002")
    print("======================================\n")
    app.run(host='0.0.0.0', port=port)
