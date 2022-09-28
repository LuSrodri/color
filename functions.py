from colorthief import ColorThief
import matplotlib.pyplot as plot


def colorPallete(fileaddress):
    print('filename = ', fileaddress)
    ct = ColorThief(fileaddress)
    total = 6
    palette = list(set(ct.get_palette(color_count=total)))
    return palette
