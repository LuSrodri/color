from http.client import BAD_REQUEST
from werkzeug.utils import secure_filename
from flask import Flask, Response, render_template, request, redirect, send_file
import os
from functions import *

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'static\images'

filename = 0
absolute_path = 0

@app.route('/', methods=["GET", "POST"])
def upload_image():
    return render_template('index.html')

@app.route('/getcolorpalettebyimage', methods=["GET", "POST"])
def get_color_palette_image():
    if request.method == "POST":
        image = request.files['file']

        if image.filename == '':
            Response("Image must have a file name", status=BAD_REQUEST)
        if image.content_type != 'image/jpeg' and image.content_type != 'image/png':
            Response("Image must be a jpeg or png", status=BAD_REQUEST)

        if image.content_type == 'image/jpeg':
            image.filename = 'one.jpg'
        if image.content_type == 'image/png':
            image.filename = 'one.png'

        global filename
        filename = secure_filename(image.filename)

        basedir = os.path.abspath(os.path.dirname(__file__))
        global absolute_path
        absolute_path = os.path.join(
            basedir, app.config["IMAGE_UPLOADS"], filename)

        image.save(absolute_path)

        numbers_of_colors_palette = 8

        colorsByKmeans = colorPaletteByKmeans(absolute_path, numbers_of_colors_palette)
        colorByColorThief = colorPaletteByColorThief(absolute_path, numbers_of_colors_palette)
        colorsByExtColor = colorPaletteByExtColor(image, numbers_of_colors_palette)

        return {"colorsByKmeans": colorsByKmeans, "colorByColorThief": colorByColorThief, "colorsByExtColor": colorsByExtColor}

    return redirect("/")

@app.route('/removeColor', methods=["GET", "POST"])
def removeColor():
    if request.method == "POST":
        request_data = request.get_json()
        colorReceived = request_data['colorsToSend']
        colorReceived = list(colorReceived)

        removeSpecificColor(colorReceived)

        return send_file('static/images/response.jpg', mimetype='image/*')
    
    return redirect('/')

@app.route('/removebg', methods=["GET", "POST"])
def removingBg():
    if request.method == "POST":
        
        removeBG()
        return send_file('static/images/response.png', mimetype='image/png')

    return redirect('/')