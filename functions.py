import cv2
from PIL import Image
from sklearn.cluster import KMeans 
import imutils 
import numpy as np
from colorthief import ColorThief
import extcolors

def colorPaletteByKmeans(image, clusterNumber):
    # a function to get the color palette of an image and return it as a list with the RGB values and the percentage of each color
    image = cv2.imread(image)
    image = imutils.resize(image, height=200)

    flat_img = np.reshape(image, (-1,3))

    kmeans = KMeans(n_clusters=clusterNumber, random_state=0)
    kmeans.fit(flat_img)

    dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint')

    percentages = (np.unique(kmeans.labels_, return_counts=True)[1])/flat_img.shape[0]
    p_and_c = zip(percentages, dominant_colors)
    p_and_c = sorted(p_and_c, reverse=True)

    for i in range(len(p_and_c)):
        p_and_c[i] = list(p_and_c[i])
        p_and_c[i][1] = p_and_c[i][1].tolist()

    return p_and_c

def colorPaletteByColorThief(image, number_of_colors):
    ct = ColorThief(image)
    palette = list(set(ct.get_palette(color_count=number_of_colors, quality=1)))
    dominant_color = ct.get_color(quality=1)

    palette.insert(0, dominant_color)

    return palette

def colorPaletteByExtColor(image, number_of_colors):
    colors, pixel_count = extcolors.extract_from_path(image, 25, number_of_colors)
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

def removeSpecificColor(filename, color):
    image = Image.open('static/images/one.jpg').convert('RGB')
    image_data = image.load()
    height, width = image.size

    rangePixel = 50

    if (len(color) == 3 and isinstance(color[0],int)):
        for i in range(len(color)):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    if r in range(int(color[0])-rangePixel, int(color[0])+rangePixel) and g in range(int(color[1])-rangePixel, int(color[1])+rangePixel) and b in range(int(color[2])-rangePixel, int(color[2])+rangePixel):
                        image_data[loop1, loop2] = 255, 255, 255

    if (color == 'red'):
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                image_data[loop1, loop2] = 0, g, b

    elif (color == 'green'):
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                image_data[loop1, loop2] = r, 0, b

    elif (color == 'blue'):
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                image_data[loop1, loop2] = r, g, 0

    image.save('static/images/response.jpg')
