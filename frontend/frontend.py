from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
import os
from main import *

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'static\images'


@app.route('/home', methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":
        image = request.files['file']

        if image.filename == '':
            print("Image must have a file name")
            return redirect(request.url)

        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        image.save(os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename))
        colors = colorPallete(os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename))
        print(colors)
        return render_template("index.html", filename=filename)

    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/images/' + filename), code=301)


app.run()
