import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from ai_art_creation.api import chatgpt, dall_e
import threading

class App:
    def __init__(self, master):
        self.master = master
        self.master.title("AI Art Generator")
        self.master.geometry("800x600")

        # Import functions
        self.chatgpt = chatgpt
        self.dall_e = dall_e

        # Dropdown box for number of iterations
        self.tk_input = IntVar()
        self.tk_input.set(3)
        self.options = [i for i in range(1, 11)]
        self.dropdown = OptionMenu(self.master, self.tk_input, *self.options)
        self.dropdown.grid(row=0, column=0, padx=10, pady=10)

        # Generate button
        #self.generate_button = Button(self.master, text="Generate", command=self.generate_images)
        #self.generate_button.grid(row=0, column=1, padx=10, pady=10)
        self.generate_button = Button(self.master, text="Generate", command=self.start_generate_images)
        self.generate_button.grid(row=0, column=1, padx=10, pady=10)
                
        # Image preview window
        self.image_canvas = Canvas(self.master, width=256, height=256)
        self.image_canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Navigation buttons
        self.previous_button = Button(self.master, text="Previous", command=self.previous_image)
        self.previous_button.grid(row=2, column=0, padx=10, pady=10)

        self.next_button = Button(self.master, text="Next", command=self.next_image)
        self.next_button.grid(row=2, column=1, padx=10, pady=10)
        
            # Text box for system output
        self.output_text = Text(self.master, wrap=WORD, height=10, width=50)
        self.output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.image_dir = "C:\\Users\\trent\\OneDrive\\Documents\\GitHub\\ai_art_creation\\ai_art_creation\\image_processing\\images_raw"
        self.image_list = []
        self.current_image = None
        self.current_index = 0
        
    def show_image(self, image_path):
        self.current_image = Image.open(image_path)
        self.current_image.thumbnail((256, 256))
        self.tk_image = ImageTk.PhotoImage(self.current_image)
        self.image_canvas.create_image(128, 128, image=self.tk_image)

    def previous_image(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.image_list[self.current_index])

    def next_image(self):
        if self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.show_image(self.image_list[self.current_index])
            
    def start_generate_images(self):
        generate_thread = threading.Thread(target=self.generate_images)
        generate_thread.start()

    def generate_images(self):
        self.output_text.delete(1.0, END)
        tk_input = self.tk_input.get()
        for i in range(tk_input):
            # Generate prompts for DALL-E
            prompts = self.chatgpt.generate_prompts(how_many=3)
            self.output_text.insert(INSERT, f"Generated prompts: {prompts}\n")

            # Retrieve images from DALL-E API
            images = self.dall_e.generate_images(prompts)
            self.output_text.insert(INSERT, f"Generated images: {len(images)}\n")

            for img in images:
                img_path = os.path.join(self.image_dir, f"image_{i}.png")
                img.save(img_path)
                self.image_list.append(img_path)

            # Force the Tkinter window to update and redraw widgets
            self.master.update_idletasks()

        self.show_image(self.image_list[0])

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()

