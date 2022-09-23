from colorthief import ColorThief
import matplotlib.pyplot as plot
import sys

ct = ColorThief("imagemteste.jpeg")
dominant_color = (ct.get_color(quality=1))

plot.imshow([[dominant_color]])
# plot.show()

total = 6

palette = ct.get_palette(color_count=total)
palette1 = set(ct.get_palette(color_count=total))
palette1 = list(palette1)
print(palette)
print("-----------------------------------------")
print(palette1)

plot.imshow([[palette[i] for i in range(len(palette)) ]])
plot.show()
plot.imshow([[palette1[i] for i in range(len(palette1)) ]])
plot.show()