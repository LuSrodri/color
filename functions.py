from colorthief import ColorThief
import matplotlib.pyplot as plot
import cv2
from PIL import Image


def colorPallete(fileaddress):
    ct = ColorThief(fileaddress)
    total = 2
    palette = list(set(ct.get_palette(color_count=total)))
    return palette


def creatingMask(filename, low, high):
    img = cv2.imread(filename)
    img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, low, high)
    mask = 255-mask

    cv2.imwrite('static/images/mask.jpg', mask)

    return mask


def responseImage(filename, mask):
    img = cv2.imread(filename)
    img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)
    res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imwrite('static/images/response.jpg', res)


def removeSpecificColor(filename, color):
    print(filename)
    print(color)
    image = Image.open(filename).convert('RGB')
    image_data = image.load()
    height, width = image.size

    if (len(color) == 3):
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                if r in range(int(color[0])-5, int(color[0])+5) and g in range(int(color[1])-5, int(color[1])+5) and b in range(int(color[2])-5, int(color[2])+5):
                    image_data[loop1, loop2] = 0, 0, 0

    elif (color[0] == 'red'):
        for loop1 in range(height):
            for loop2 in range(width):
                r, g, b = image_data[loop1, loop2]
                image_data[loop1, loop2] = 0, g, b
    image.save('static/images/response.jpg')
