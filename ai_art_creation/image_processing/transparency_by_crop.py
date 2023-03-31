from PIL import Image, ImageDraw
import os
import random as rand
import math
import numpy as np

def rounded_corners_crop(image_path, radius_percentage=0.2):
    # Open the image and convert it to RGBA mode (if it's not already)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    if width != height:
        raise ValueError("The input image should be square.")

    # Calculate the corner radius based on the percentage of image width
    corner_radius = int(width * radius_percentage)

    # Create a new image with the same size and RGBA mode
    mask = Image.new("RGBA", (width, height))

    # Draw a rounded rectangle on the mask image
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, width, height), radius=corner_radius, fill=(255, 255, 255, 255))

    # Apply the mask to the original image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(image, mask=mask)

    return result

def circle_crop(image_path):
    # Open the image and convert it to RGBA mode (if it's not already)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    if width != height:
        raise ValueError("The input image should be square.")

    # Create a new image with the same size and RGBA mode
    mask = Image.new("RGBA", (width, height))

    # Draw a filled white circle on the mask image
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=(255, 255, 255, 255))

    # Apply the mask to the original image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(image, mask=mask)

    return result

def triangle_crop(image_path):
    # Open the image and convert it to RGBA mode (if it's not already)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    if width != height:
        raise ValueError("The input image should be square.")

    # Create a new image with the same size and RGBA mode
    mask = Image.new("RGBA", (width, height))

    # Draw a filled white triangle on the mask image
    draw = ImageDraw.Draw(mask)
    triangle_points = [(0, height), (width, height), (width // 2, 0)]
    draw.polygon(triangle_points, fill=(255, 255, 255, 255))

    # Apply the mask to the original image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(image, mask=mask)

    return result

def diamond_crop(image_path):
    # Open the image and convert it to RGBA mode (if it's not already)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    if width != height:
        raise ValueError("The input image should be square.")

    # Create a new image with the same size and RGBA mode
    mask = Image.new("RGBA", (width, height))

    # Draw a filled white diamond on the mask image
    draw = ImageDraw.Draw(mask)
    diamond_points = [(width // 2, 0), (width, height // 2), (width // 2, height), (0, height // 2)]
    draw.polygon(diamond_points, fill=(255, 255, 255, 255))

    # Apply the mask to the original image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(image, mask=mask)

    return result

def random_triangle_crop(image_path):
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    # Open the image file
    img = Image.open(image_path)

    # Check if the image is square
    if img.width != img.height:
        raise ValueError("Image must be square")

    # Get the size of the image
    size = img.width

    # Calculate minimum area for the triangle
    min_area = 0.25 * size * size
    
    # Create a list of integers
    sides = [1, 2, 3, 4]

    # Shuffle the list randomly
    rand.shuffle(sides)

    # Take the first three elements from the shuffled list
    sides = sides[:3]

    # Generate triangle points that cover at least 25% of the image
    while True:
        if 1 not in sides:
            p1 = (rand.randint(0, size), 0)
            p2 = (0, rand.randint(0, size))
            p3 = (rand.randint(0, size), size)
        if 2 not in sides:
            p1 = (size, rand.randint(0, size))
            p2 = (0, rand.randint(0, size))
            p3 = (rand.randint(0, size), size)
        if 3 not in sides:
            p1 = (rand.randint(0, size), 0)
            p2 = (size, rand.randint(0, size))
            p3 = (rand.randint(0, size), size)
        if 4 not in sides:
            p1 = (rand.randint(0, size), 0)
            p2 = (0, rand.randint(0, size))
            p3 = (size, rand.randint(0, size))

        # Calculate the area of the generated triangle using the Shoelace formula
        area = 0.5 * abs(p1[0]*p2[1] + p2[0]*p3[1] + p3[0]*p1[1] - p2[0]*p1[1] - p3[0]*p2[1] - p1[0]*p3[1])
        
        if area >= min_area:
            break

    # Create a new image with the same size and mode as the input image
    output_image = Image.new(img.mode, (size, size), (0, 0, 0, 0))

    # Create a draw object to draw the triangle on the new image
    draw = ImageDraw.Draw(output_image, "RGBA")

    # Draw the triangle with a fully opaque color
    draw.polygon([p1, p2, p3], fill=(255, 255, 255, 255))

    # Create a mask from the triangle image
    mask = Image.new("L", (size, size), 0)
    mask.paste(output_image.split()[-1])

    # Apply the mask to the input image
    img.putalpha(mask)

    # Return the modified image
    return img

def random_polygon_crop(image_path):
    num_sides = rand.randint(5, 99)

    # Open the image and convert it to RGBA mode (if it's not already)
    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    if width != height:
        raise ValueError("The input image should be square.")

    # Create a new image with the same size and RGBA mode
    mask = Image.new("RGBA", (width, height))

    # Draw a filled white polygon on the mask image
    draw = ImageDraw.Draw(mask)
    polygon_points = [
        (
            random.randint(0, width),
            random.randint(0, height)
        )
        for i in range(num_sides)
    ]
    draw.polygon(polygon_points, fill=(255, 255, 255, 255))

    # Apply the mask to the original image
    result = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    result.paste(image, mask=mask)

    return result

def random_polygon_crop_circle(image_path):
    # Load the image
    image = Image.open(image_path).convert("RGBA")

    # Check if the image is square
    if image.width != image.height:
        raise ValueError("The input image must be square")

    size = image.width
    radius = size / 2

    # Generate a random number of points between 5 and 99
    n_points = rand.randint(250, 1000)

    # Generate random points within the circle
    points = []
    while len(points) < n_points:
        x = rand.uniform(0, size)
        y = rand.uniform(0, size)
        if (x - radius) ** 2 + (y - radius) ** 2 <= radius ** 2:
            points.append((x, y))

    # Create a new transparent image with the same size
    mask = Image.new("RGBA", (size, size), 0)
    draw = ImageDraw.Draw(mask)

    # Draw the polygon on the mask
    draw.polygon(points, fill=(255, 255, 255, 255))

    # Convert mask to RGBA
    mask = mask.convert("RGBA")

    # Apply the mask to the original image
    #result = Image.composite(image, Image.new("RGBA", image.size, (0, 0, 0, 0)), mask)

    # Apply the mask to the original image
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(image, mask=mask)


    # Save the result to a new file
    #output_path = "output_" + image_path
    #result.save(output_path, "PNG")

    return result
