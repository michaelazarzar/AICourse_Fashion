from flask import Flask, render_template, request
import os
import onnxruntime as ort
import numpy as np
from PIL import Image

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = './Upload/'
onnx_model = ort.InferenceSession('./models/model.onnx')
input_name = onnx_model.get_inputs()[0].name
output_name = onnx_model.get_outputs()[0].name

print(f'Model input name = {input_name}')
print(f'Model output name = {output_name}')

labels = {0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat', 5: 'Sandal', 6: 'Shirt',
          7: 'Sneaker', 8: 'Bag', 9: 'Ankle boo' } 

@app.route('/', methods=['GET', 'POST'])
def landing():
    return 'Welcome to landing page!<br>To redirect add to URL /upload'

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image_path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            image.save(image_path)
            prediction, probability = make_predict(image_path)
            return render_template("Upload.html", uploaded_image=image.filename, prediction_label = prediction, probability = probability)
    return render_template("Upload.html")

# Return label and probability
def make_predict(image_path):
    # Prepare the image to prediction.
    image = Image.open(image_path).convert('L')
    
    image = np.stack((image,)*1, axis=-1).astype(np.float32)
    image = np.stack((image,)*1, axis=0).astype(np.float32)
    
    hist = onnx_model.run([output_name], {input_name: image})
    max_val = np.argmax(hist)
    probability = np.max(hist) * 100
    return labels.get(max_val), probability
    


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = int(os.getenv('PORT', 6978)))