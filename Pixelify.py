from PIL import Image
from math import sqrt
import subprocess

maxHeight = 36
maxWidth = 36
colorThreshold = 10000

inputPath = "src/absolutelybarbaric.jpeg"
usingAlias = True

def compressImage(image, height, width):
	h = 0
	w = 0
	ratio = 0

	heightBound = image.height > image.width

	if (heightBound):
		ratio = image.height / image.width
		h = min(maxHeight, image.height)
		w = round(h / ratio)
	else:
		ratio = image.width / image.height
		w = min(maxWidth, image.width)
		h = round(w / ratio)

	image = image.resize((w,h))
	return image

def clamp(x):
	return max(0, min(x, 255))

def RGBToHex(rgb):
	if (type(rgb) is tuple):
		return "{0:02x}{1:02x}{2:02x}".format(clamp(rgb[0]), clamp(rgb[1]), clamp(rgb[2]))
	else:
		return "0"

def hex_to_rgb(value):
    value = value.rstrip('\n')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def closest_color(rgb, COLORS):
    r, g, b, a = rgb
    color_diffs = []
    for color in COLORS:
        cr, cg, cb = color
        color_diff = sqrt((r - cr)**2 + (g - cg)**2 + (b - cb)**2)
        color_diffs.append((color_diff, color))
    return min(color_diffs)[1]

def run():
	img = Image.open(inputPath)
	with open("colorList.txt") as file:
		lines = list(file)

	length = len(lines)
	for i in range(length):
		#pre = lines[i][:6]
		#lines[i] = int(lines[i], 16)
		lines[i] = hex_to_rgb(lines[i])
		#post = hex(lines[i])[2:].zfill(6)
		#print(f":pixel-color-{pre}: | :pixel-color-{post}:")

	if (img.height > maxHeight or img.width > maxWidth):
		img = compressImage(img, maxHeight, maxWidth)

	img = img.convert("RGBA")

	img.save("out/outputTest.png")

	f = open("slackOutput.txt", "w")
	output = ""
	for y in range(img.height):
		for x in range (img.width):
			#print(img.getpixel((x,y)))
			closestClr = closest_color(img.getpixel((x,y)), lines)
			#print(closestClr)
			closestHEX = RGBToHex(closestClr)
			#print("difference", diff)
			if (usingAlias):
				output += str(f':{closestHEX}:')
			else:
				output += str(f':pixel-color-{closestHEX}:')
		output += str('\n')
	f.write(output)
	f.close()

	subprocess.run("pbcopy", universal_newlines=True, input=output)




if __name__ == "__main__":
	run()

