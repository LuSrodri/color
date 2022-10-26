import os
from PIL import Image
import extcolors


async def colorPaletteByExtColor(image, number_of_colors):
    await cleaningResponseFile()
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


async def removeSpecificColor(color, imagePath):
    await cleaningResponseFile()
    image = Image.open('static/images/'+imagePath).convert('RGB')
    image_data = image.load()
    height, width = image.size
    totalPixelsRemoved = 0

    rangePixel = 80
    for c in range(len(color)):
        if (len(color[c]) == 3 and isinstance(color[c][0], int)):
            # totalPixelsRemoved = removeStrictPercentageColors(imagePath,
            #                                                   c, totalPixelsRemoved, image_data, color, height, width)
            totalPixelsRemoved = removeColorsWithRangeError(c, totalPixelsRemoved,
                                                            image_data, color, height, width, rangePixel)

        elif (color[c] == 'red'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = 0, g, b
                    totalPixelsRemoved += 1

        elif (color[c] == 'green'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = r, 0, b
                    totalPixelsRemoved += 1

        elif (color[c] == 'blue'):
            for loop1 in range(height):
                for loop2 in range(width):
                    r, g, b = image_data[loop1, loop2]
                    image_data[loop1, loop2] = r, g, 0
                    totalPixelsRemoved += 1

    image.save('static/images/response.jpg')
    return totalPixelsRemoved


async def getImageInfos(imagePath):
    image = Image.open(imagePath)
    width, height = image.size

    totalBytes = os.path.getsize(imagePath)

    imageInfos = {"totalPixel": width*height, "totalBytes": totalBytes}
    return imageInfos


async def cleaningFiles():
    extensions = ['.jpg', '.png']
    mainFile = "static/images/one"
    response = 'static/images/response'

    for ext in extensions:
        if os.path.isfile(mainFile+ext):
            os.remove(mainFile+ext)
        if os.path.isfile(response+ext):
            os.remove(response+ext)


async def cleaningResponseFile():
    extensions = ['.jpg', '.png']
    response = 'static/images/response'

    for ext in extensions:
        if os.path.isfile(response+ext):
            os.remove(response+ext)


def removeColorsWithRangeError(c, totalPixelsRemoved, image_data, color, height, width, rangePixel=80):
    total = totalPixelsRemoved
    for loop1 in range(height):
        for loop2 in range(width):
            r, g, b = image_data[loop1, loop2]
            if r in range(int(color[c][0])-rangePixel, int(color[c][0])+rangePixel) and g in range(int(color[c][1])-rangePixel, int(color[c][1])+rangePixel) and b in range(int(color[c][2])-rangePixel, int(color[c][2])+rangePixel):
                image_data[loop1, loop2] = 255, 255, 255
                total += 1

    return total


def removeStrictPercentageColors(imagePath, c, totalPixelsRemoved, image_data, color, height, width):

    dicionary = getTotalColors(imagePath)
    total = totalPixelsRemoved
    originalColor = '('+str(color[c][0])+', ' + \
        str(color[c][1])+', '+str(color[c][2])+')'
    for loop1 in range(height):
        for loop2 in range(width):
            r, g, b = image_data[loop1, loop2]
            aux = '('+str(r)+', '+str(g)+', '+str(b)+')'
            if aux in dicionary[originalColor]:
                image_data[loop1, loop2] = 255, 255, 255
                total += 1

    return total


def getTotalColors(imagePath):
    image = Image.open('static/images/'+imagePath)
    pixels = list(image.convert("RGBA").getdata())
    pixel_count = len(pixels)
    pixels = [p for p in pixels if p[3] > 0]
    pixels = [(p[0], p[1], p[2]) for p in pixels]
    colors = extcolors._count_colors(pixels)
    totalColors = {}
    colors.sort(reverse=True)

    i = 0
    while i < len(colors):
        larger = colors[i]
        if not larger.compressed:
            if totalColors.get(larger) is None:
                conteudo = 0
                totalColors[str(larger.rgb)] = []
            j = i + 1
            while j < len(colors):
                smaller = colors[j]
                if not smaller.compressed and extcolors.difference.cie76(
                        larger.lab, smaller.lab) < 25:
                    totalColors[str(larger.rgb)].append(str(smaller.rgb))
                    conteudo += 1
                    larger.count += smaller.count
                    smaller.compressed = True

                j += 1
        i += 1

    return totalColors
