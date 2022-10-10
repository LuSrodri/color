from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for
import os
from functions import *
import numpy as np
import colorsys


app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'static\images'

filename = 0
absolute_path = 0


@app.route('/', methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        image = request.files['file']

        if image.filename == '':
            print("Image must have a file name")
            return redirect(request.url)
        global filename
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        global absolute_path
        absolute_path = os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename)

        # salvando imagem principal
        image.save(absolute_path)

        # coletando paleta de cores
        colors = colorPallete(absolute_path)

        low_green = np.array([25, 52, 72])
        high_green = np.array([102, 255, 255])

        return render_template("colorPallete.html", filename=filename, colors=colors)

    return render_template('index.html')


@app.route('/color', methods=["GET", "POST"])
def get_colors():
    if request.method == "POST":
        image = request.files['file']

        # coletando paleta de cores
        colors = colorPallete(absolute_path)

        return render_template("colorPallete.html", filename=filename, colors=colors)

    return render_template('index.html')


@app.route('/result', methods=["GET", "POST"])
def results():
    if request.method == "POST":
        color = request.form.get('color').split(',')
        # hsvColor = colorsys.rgb_to_hsv(
        #     int(color[0]), int(color[1]), int(color[2]))
        # print(hsvColor)
        # print(hsvColor[0])
        # print(hsvColor[1])
        # print(hsvColor[2])
        low = np.array(
            [0, 0, 0])
        high = np.array([int(color[0]), int(color[1]), int(color[2])])
        low_green = np.array([25, 52, 72])
        high_green = np.array([102, 255, 255])
        print()
        print("low = ", low)
        print("high = ", high)
        print("low_green = ", low_green)
        print("high_green = ", high_green)

        # criando mascara
        mask = creatingMask(absolute_path, low, high)

        # aplicando mascara e salvando a imagem de resposta
        responseImage(absolute_path, mask)

        return render_template("result.html", filename=filename, mask='mask.jpg', response='response.jpg')

    return render_template('index.html')


@app.route('/removeColor', methods=["GET", "POST"])
def removeColor():
    if request.method == "POST":
        color = request.form.get('color').split(',')
        removeSpecificColor(absolute_path, color)
        return render_template("result.html", filename=filename, mask='mask.jpg', response='response.jpg')

    return render_template('index.html')


@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='/images/' + filename), code=301)
