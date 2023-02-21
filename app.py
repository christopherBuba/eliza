import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
CORS(app)

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

# Initialize Firebase app and credentials
cred = credentials.Certificate('./elizafashions-1679-firebase-adminsdk-hhr9d-0eeb6fe5b7.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'elizafashions-1679.appspot.com'
})
bucket = storage.bucket()

# Route that fetches image and reads hidden code
@app.route('/')
def get_hidden_code():
    blob = bucket.blob('sisyphus.jpeg')
    content = blob.download_as_bytes()
    offset = content.index(bytes.fromhex('FFD9'))
    code = content[offset + 2:].decode('utf-8')
    response = {'hidden_code': code}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
