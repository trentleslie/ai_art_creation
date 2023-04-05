import os
import shutil
from tkinter import messagebox
from PIL import Image, ImageTk
import tkinter as tk

root = tk.Tk()
root.title('Image Processing')

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

raw_images_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\image_processing\\images_raw"
special_images_dir = os.path.join(raw_images_dir, "ready_to_scale")
font_images_dir = os.path.join(raw_images_dir, "ready_to_scale")

def update_image_list():
    image_list.delete(0, tk.END)
    png_files = [f for f in os.listdir(raw_images_dir) if f.endswith('.png')]
    for f in png_files:
        image_list.insert(tk.END, f)

def select_image(event):
    selected_image = image_list.get(image_list.curselection())
    file_path = os.path.join(raw_images_dir, selected_image)
    
    img = Image.open(file_path)
    img.thumbnail((600, 600))
    img = ImageTk.PhotoImage(img)

    label.config(image=img)
    label.image = img

def process_image():
    selected_image = image_list.get(image_list.curselection())
    file_path = os.path.join(raw_images_dir, selected_image)
    filename, file_extension = os.path.splitext(selected_image)

    if standard_var.get():
        new_filename = filename + '-rounded' + file_extension
        shutil.copy(file_path, os.path.join(raw_images_dir, new_filename))
        
    if special_var.get():
        shapes = ['-circle', '-diamond', '-triangle', '-randpoly', '-randpolycircle']
        for shape in shapes:
            new_filename = filename + shape + file_extension
            shutil.copy(file_path, os.path.join(special_images_dir, new_filename))
            
    if font_var.get():
        new_filename = filename + '-font' + file_extension
        shutil.copy(file_path, os.path.join(font_images_dir, new_filename))

    update_image_list()
    messagebox.showinfo("Success", "Image processed successfully")

image_list = tk.Listbox(frame, width=40, height=10)
image_list.grid(row=0, column=0, padx=(0, 10))
image_list.bind("<<ListboxSelect>>", select_image)
update_image_list()

scrollbar = tk.Scrollbar(frame, orient="vertical", command=image_list.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
image_list.config(yscrollcommand=scrollbar.set)

label = tk.Label(frame)
label.grid(row=0, column=2, padx=(10, 0))

standard_var = tk.BooleanVar()
special_var = tk.BooleanVar()
font_var = tk.BooleanVar()

standard_cb = tk.Checkbutton(frame, text="Standard", variable=standard_var)
standard_cb.grid(row=1, column=0, sticky="w")

special_cb = tk.Checkbutton(frame, text="Special", variable=special_var)
special_cb.grid(row=2, column=0, sticky="w")

font_cb = tk.Checkbutton(frame, text="Font", variable=font_var)
font_cb.grid(row=3, column=0, sticky="w")

process_button = tk.Button(frame, text="Process Image", command=process_image)
process_button.grid(row=4, column=0, pady=(10, 0))

root.mainloop()
