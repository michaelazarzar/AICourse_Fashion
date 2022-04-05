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

print(f'Model input name{input_name}')
print(f'Model output name{output_name}')

@app.route('/', methods=['GET', 'POST'])
def landing():
    return 'Welcome to landing page!'

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(f'image type ****{type(image)}')
            image_path = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            image.save(image_path)
            print(make_predict(image_path))
            return render_template("Upload.html", uploaded_image=image.filename)
    return render_template("Upload.html")


#TODO use this method to make the prediction when we ready with model.
def make_predict(image_path):
    #input_shape = np.zeros([None, 28, 28,1], np.int8)

    image = Image.open(image_path).convert('L')
    image = np.stack((image,)*3, axis=-1)
    return onnx_model.run([output_name], {'input1': image})
    




@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0', port = int(os.getenv('PORT', 6978)))