import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# import our OCR function
from ocr_core import ocr_core

# define a folder to store and later serve the images
UPLOAD_FOLDER = '/static/uploads/'

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpeg', 'jpg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to hangle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.dirname(os.path.realpath(__file__))+os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.dirname(os.path.realpath(__file__))+os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                msg='Successfully processed',
                extracted_text=extracted_text,
                img_src=UPLOAD_FOLDER + filename)
    elif request.method == 'GET':
        return render_template('upload.html')

if __name__ == '__main__':
    app.run()