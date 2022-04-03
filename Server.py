from flask import Flask, render_template, request
import os

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = './Upload/'

@app.route('/', methods=['GET', 'POST'])
def landing():
    return 'Welcome to landing page!'

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    print(f'************{request.method}')
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            return render_template("Upload.html", uploaded_image=image.filename)
    return render_template("Upload.html")


@app.route('/uploads/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)

if __name__ == '__main__':
    app.run(debug=False, host = '0.0.0.0', port = int(os.getenv('PORT', 6978)))