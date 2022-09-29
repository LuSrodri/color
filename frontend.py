from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
import os
from functions import *
import numpy as np


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
        low_green = np.array([25, 52, 72])
        high_green = np.array([102, 255, 255])
        mask = creatingMask(os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename),low_green,high_green)

        image.save(os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], mask))

        print("mask = ",mask)
        return render_template("index.html", filename=filename, colors=colors,mask=mask)

    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/images/' + filename), code=301)


app.run()
