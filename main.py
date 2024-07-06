from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)  # Enable CORS if necessary

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/img', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No image selected for uploading'}), 400
    
    if image and allowed_file(image.filename):
        try:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'message': 'Image uploaded successfully'})
        except Exception as e:
            print(str(e))  # Log the actual exception
            return jsonify({'error': 'Error saving the image'}), 500
    else:
        return jsonify({'error': 'Invalid file type. Allowed types: png, jpg, jpeg, gif'}), 400

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True, port=8080)
