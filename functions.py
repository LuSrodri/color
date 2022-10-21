from os import remove
from PIL import Image
import extcolors
from rembg import remove


def colorPaletteByExtColor(image, number_of_colors):
    image = Image.open(image)
    colors, pixel_count = extcolors.extract_from_image(
        image, 25, number_of_colors)
    percentages = getPercentagesOfColorsByPixel(pixel_count, colors)

    p_and_c = zip(percentages, colors)
    p_and_c = sorted(p_and_c, reverse=True)

    for i in range(len(p_and_c)):
        p_and_c[i] = list(p_and_c[i])
        p_and_c[i][1] = list(p_and_c[i][1])

    return p_and_c


def getPercentagesOfColorsByPixel(pixel_count, colors):
    percentages = []
    for i in range(len(colors)):
        percentages.append(colors[i][1]/pixel_count*100)
    return percentages


def removeSpecificColor(color):
    image = Image.open('static/images/one.jpg').convert('RGB')
    image_data = image.load()
    height, width = image.size

    rangePixel = 80
    for c in range(len(color)):
        if (len(color[c]) == 3 and isinstance(color[c][0], int)):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    if r in range(int(color[c][0])-rangePixel, int(color[c][0])+rangePixel) and g in range(int(color[c][1])-rangePixel, int(color[c][1])+rangePixel) and b in range(int(color[c][2])-rangePixel, int(color[c][2])+rangePixel):
                        image_data[loop1, loop2] = 255, 255, 255

        elif (color[c] == 'red'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = 0, g, b

        elif (color[c] == 'green'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = r, 0, b

        elif (color[c] == 'blue'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = r, g, 0

    image.save('static/images/response.jpg')
