import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk

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

# Function to open a file dialog and process the selected image
def open_image():
    input_image_path = filedialog.askopenfilename(title="Select an image")
    if input_image_path:
        result_image = circle_crop(input_image_path)
        result_image.thumbnail((400, 400))
        output_image_path = input_image_path.rsplit(".", 1)[0] + "-circle.png"
        result_image.save(output_image_path)
        display_image(result_image)

# Function to display the processed image in the UI
def display_image(image):
    image_tk = ImageTk.PhotoImage(image)
    image_label.config(image=image_tk)
    image_label.image = image_tk

# Create the main window
root = tk.Tk()
root.title("Circle Crop")

# Create the "Open Image" button
open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

# Create the image display label
image_label = tk.Label(root)
image_label.pack()

# Run the UI
root.mainloop()
