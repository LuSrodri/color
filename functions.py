from colorthief import ColorThief
import matplotlib.pyplot as plot
import cv2


def colorPallete(fileaddress):
    ct = ColorThief(fileaddress)
    total = 6
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
