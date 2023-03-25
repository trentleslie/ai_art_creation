from PIL import Image, ImageDraw
import random

def fill_shape(image, polygon_coords, color=(255, 255, 254)):
    # Create a new image with transparency
    mask = Image.new('RGBA', image.size, (0, 0, 0, 0))

    # Draw the polygon on the mask image
    draw = ImageDraw.Draw(mask)
    draw.polygon(polygon_coords, fill=(255, 255, 255, 255))

    # Fill in any white pixels within the shape with the specified color
    pixels = mask.load()
    for x in range(mask.width):
        for y in range(mask.height):
            if pixels[x, y] == (255, 255, 255, 255):
                pixels[x, y] = color

    # Paste the mask onto the original image
    image.paste(mask, (0, 0), mask)

    # Return the modified image
    return image

def rounded_corners_img(image_path, radius_fraction=0.15):
    # Open the image file
    image = Image.open(image_path)

    # Calculate the size of the rounded corners
    size = min(image.size)
    radius = int(size * radius_fraction)

    # Create a new image with transparency
    mask = Image.new('RGBA', (size, size), (255, 255, 255, 0))

    # Draw the rounded corners on the mask image
    draw = ImageDraw.Draw(mask)
    draw.rectangle([(0, 0), (size, size)], fill=(255, 255, 255, 255), outline=None, width=0, joint=None)
    draw.rounded_rectangle([(0, 0), (size, size)], radius, fill=(0, 0, 0, 255), outline=None, width=0, joint=None)

    # Fill in any white pixels within the shape with black
    pixels = mask.load()
    for x in range(mask.width):
        for y in range(mask.height):
            if pixels[x, y] == (255, 255, 255, 255):
                pixels[x, y] = (254, 254, 254, 255)

    # Apply the transparency trick to the mask image
    pixels = mask.load()
    for x in range(mask.width):
        for y in range(mask.height):
            if pixels[x, y] == (255, 255, 255, 255):
                pixels[x, y] = (255, 255, 255, 0)

    # Paste the mask onto the original image
    image.paste(mask, (0, 0), mask)

    # Return the modified image
    return image

def circle_img(image_path):
    return rounded_corners_img(image_path, radius_fraction=0.5)

def symm_triangle_img(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Calculate the size of the triangle
    size = min(image.size)

    # Define the coordinates of the triangle
    x1, y1 = 0, size
    x2, y2 = size // 2, 0
    x3, y3 = size, size

    # Fill in the triangle with the specified color
    fill_shape(image, [(x1, y1), (x2, y2), (x3, y3)], color=(255, 255, 255))

    # Return the modified image
    return image

def random_triangle_img(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Calculate the size of the triangle
    size = min(image.size)

    # Define the coordinates of the triangle
    x1, y1 = random.randint(0, size // 2), random.randint(0, size // 2)
    x2, y2 = random.randint(size // 2, size), random.randint(0, size // 2)
    x3, y3 = random.randint(0, size // 2), random.randint(size // 2, size)

    # Fill in the triangle with the specified color
    fill_shape(image, [(x1, y1), (x2, y2), (x3, y3)], color=(255, 255, 255))

    # Return the modified image
    return image

def diamond_img(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Calculate the size of the diamond
    size = min(image.size)

    # Define the coordinates of the diamond
    x1, y1 = 0, size // 2
    x2, y2 = size // 2, 0
    x3, y3 = size, size // 2
    x4, y4 = size // 2, size

    # Fill in the diamond with the specified color
    fill_shape(image, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)], color=(255, 255, 255))

    # Return the modified image
    return image

def random_shape_img(image_path):
    # Open the image file
    image = Image.open(image_path)

    # Calculate the size of the square
    size = min(image.size)

    # Define the minimum and maximum number of sides for the polygon
    min_sides = 5
    max_sides = 99

    # Define the minimum area for the polygon
    min_area = size * size * 0.3

    # Generate a random number of sides for the polygon
    sides = random.randint(min_sides, max_sides)

    # Define the coordinates of the polygon
    vertices = []
    for i in range(sides):
        x = random.randint(0, size)
        y = random.randint(0, size)
        vertices.append((x, y))

    # Calculate the area of the polygon
    area = 0.5 * sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(vertices, vertices[1:] + [vertices[0]]))

    # If the area is too small, generate a new polygon
    while area < min_area:
        vertices = []
        for i in range(sides):
            x = random.randint(0, size)
            y = random.randint(0, size)
            vertices.append((x, y))
        area = 0.5 * sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(vertices, vertices[1:] + [vertices[0]]))

    # Fill in the polygon with the specified color
    fill_shape(image, vertices, color=(255, 255, 255))

    # Return the modified image
    return image
