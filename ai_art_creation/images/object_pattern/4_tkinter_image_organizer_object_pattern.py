import os
import shutil
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

source_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\images\\object_pattern\\"
ready_to_scale_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\images\\object_pattern\\ready_to_scale\\"
selected_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\images\\object_pattern\\selected\\"
removed_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\images\\object_pattern\\rejected\\"

def get_png_files():
    return [file for file in os.listdir(source_dir) if file.endswith(".png")]

def refresh_image_list():
    listbox.delete(0, END)
    for file in get_png_files():
        listbox.insert(END, file)
    if listbox.size() > 0:
        listbox.selection_set(0)
        update_image_preview()

def process_image():
    selected_file = listbox.get(listbox.curselection())
    selected_path = os.path.join(source_dir, selected_file)
    base_filename, ext = os.path.splitext(selected_file)

    if var_standard.get():
        shutil.move(selected_path, os.path.join(selected_dir, f"{base_filename}{ext}"))
        shutil.move(os.path.join(source_dir, f"{base_filename}.txt"), os.path.join(selected_dir, f"{base_filename}.txt"))
    if var_shapes.get():
        for shape in ["-circle", "-diamond", "-star", "-triangle", "-randpoly", "-randpolycircle"]:
            shutil.move(selected_path, os.path.join(selected_dir, f"{base_filename}{shape}{ext}"))
            shutil.move(os.path.join(source_dir, f"{base_filename}.txt"), os.path.join(selected_dir, f"{base_filename}.txt"))
    if var_font.get():
        shutil.move(selected_path, os.path.join(selected_dir, f"{base_filename}-font{ext}"))
    
    refresh_image_list()

def remove_image():
    selected_file = listbox.get(listbox.curselection())
    selected_path = os.path.join(source_dir, selected_file)
    base_filename, ext = os.path.splitext(selected_file)
    shutil.move(selected_path, os.path.join(removed_dir, selected_file))
    shutil.move(os.path.join(source_dir, f"{base_filename}.txt"), os.path.join(removed_dir, selected_file))
    refresh_image_list()

def on_key_press(event):
    key = event.char
    if key == "j":
        var_standard.set(not var_standard.get())
    elif key == "k":
        var_shapes.set(not var_shapes.get())
    elif key == "l":
        var_font.set(not var_font.get())
    elif key == " ":
        process_image()
    elif key == "u":
        remove_image()

root = Tk()
root.title("Image Processing")
root.configure(padx=10, pady=10)  # Add padding around the edge of the entire window

label = Label(root)
label.grid(row=0, column=1)

def update_image_preview():
    selected_file = listbox.get(listbox.curselection())
    img = Image.open(os.path.join(source_dir, selected_file))
    #img.thumbnail((600, 600))
    img.thumbnail((1200, 1200))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

def on_listbox_select(evt):
    update_image_preview()

listbox = Listbox(root, height=40, width=40)  # Make the image list box twice as wide
listbox.grid(row=0, column=0, rowspan=4, padx=(0, 10))
listbox.bind('<<ListboxSelect>>', on_listbox_select)
listbox.bind_all('<KeyPress>', on_key_press)
refresh_image_list()

var_standard = BooleanVar()
check_standard = Checkbutton(root, text="Standard", variable=var_standard)
check_standard.grid(row=1, column=1)

var_shapes = BooleanVar()
check_shapes = Checkbutton(root, text="Shapes", variable=var_shapes)
check_shapes.grid(row=2, column=1)

var_font = BooleanVar()
check_font = Checkbutton(root, text="Font", variable=var_font)
check_font.grid(row=3, column=1)

btn_process_image = Button(root, text="Process Image", command=process_image)
btn_process_image.grid(row=4, column=1) #, sticky=W, padx=(200, 0))  # Add padding to center the button

btn_remove_image = Button(root, text="Remove", command=remove_image)
btn_remove_image.grid(row=5, column=1) #, padx=(350, 0), sticky=W)  # Move the "Remove" button to the right of the "Process Image" button with padding in between

if listbox.size() > 0:
    listbox.selection_set(0)
    img = Image.open(os.path.join(source_dir, listbox.get(0)))
    img.thumbnail((600, 600))
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

root.mainloop()

