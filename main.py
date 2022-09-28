import cv2
import numpy as np
from tkinter import filedialog
from colorthief import ColorThief
import matplotlib.pyplot as plot
import sys
from tkinter import *
low_green = np.array([25, 52, 72])
high_green = np.array([102, 255, 255])

root = Tk()
root.filename = filedialog.askopenfilename(
    initialdir="/", title="Select file", filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
ct = ColorThief(root.filename)
dominant_color = (ct.get_color(quality=1))

plot.imshow([[dominant_color]])
# plot.show()

total = 6


palette = list(set(ct.get_palette(color_count=total)))
print(palette)


plot.imshow([[palette[i] for i in range(len(palette))]])
plot.show()

while True:
    img = cv2.imread(root.filename)
    img = cv2.resize(img, (900, 650), interpolation=cv2.INTER_CUBIC)

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, low_green, high_green)
    # inverse mask
    mask = 255-mask
    res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    cv2.imshow('res', res)
    cv2.waitKey(10)
