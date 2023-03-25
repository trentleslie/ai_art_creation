import os
from PIL import Image

def make_white_transparent(image_path):
    image = Image.open(image_path)
    image = image.convert("RGBA")
    
    width, height = image.size
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel[0] == 255 and pixel[1] == 255 and pixel[2] == 255:
                image.putpixel((x, y), (255, 255, 255, 0))

    image.save(image_path)

directory = './ai_art_creation/image_processing/images_processed'
for filename in os.listdir(directory):
    if filename.endswith('.png'):
        image_path = os.path.join(directory, filename)
        make_white_transparent(image_path)
