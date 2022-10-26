from http.client import BAD_REQUEST
import json
from werkzeug.utils import secure_filename
from flask import Flask, Response, render_template, request, redirect, send_file
import os
from functions import *
from requests_toolbelt import MultipartEncoder

app = Flask(__name__)

app.config['IMAGE_UPLOADS'] = 'static\images'

filename = 0
absolute_path = 0


@app.route('/', methods=["GET", "POST"])
async def upload_image():
    await cleaningFiles()
    return render_template('index.html')


@app.route('/getcolorpalettebyimage', methods=["GET", "POST"])
async def get_color_palette_image():
    if request.method == "POST":
        image = getImageFromRequest(request, 'one')

        numbers_of_colors_palette = 8

        colorsByExtColor = await colorPaletteByExtColor(
            image, numbers_of_colors_palette)

        imageInfos = await getImageInfos('static/images/'+filename)

        return {"imageInfos": imageInfos, "colorsByExtColor": colorsByExtColor, "imagePath": str(filename)}

    return redirect("/")


@app.route('/removeColor', methods=["GET", "POST"])
async def removeColor():
    if request.method == "POST":
        request_data = request.get_json()

        colorReceived = request_data['colorsToSend']
        colorReceived = list(colorReceived)
        imagePath = request_data['imagePath']

        totalPixelsRemoved = await removeSpecificColor(colorReceived, imagePath)

        imageInfos = await getImageInfos('static/images/response.jpg')

        return {"imageInfos": imageInfos, "totalPixelsRemoved": totalPixelsRemoved, "imageResponsePath": "response.jpg"}

    return redirect('/')


@app.route('/getImage', methods=["POST"])
def getImage():
    request_data = request.get_json()
    imagePath = request_data['imagePath']
    return send_file(('static/images/' + imagePath), mimetype='image/jpg')


def getImageFromRequest(request, name):
    image = request.files['file']
    if image.filename == '':
        Response("Image must have a file name", status=BAD_REQUEST)
    if image.content_type != 'image/jpeg' and image.content_type != 'image/png':
        Response("Image must be a jpeg or png", status=BAD_REQUEST)

    if image.content_type == 'image/jpeg':
        image.filename = name + '.jpg'
    if image.content_type == 'image/png':
        image.filename = name + '.png'

    global filename
    filename = secure_filename(image.filename)

    basedir = os.path.abspath(os.path.dirname(__file__))
    global absolute_path
    absolute_path = os.path.join(
        basedir, app.config["IMAGE_UPLOADS"], filename)

    image.save(absolute_path)

    return image
