from tkinter import filedialog, messagebox
from tkinter import *
from PIL import Image, ImageTk
import os


class WatermarkApp:
    def __init__(self):
        self.photo_path = StringVar()  # class variable for string text
        self.watermark_path = StringVar()
        self.photo_image = None
        self.image = None
        self.saved_image_path = StringVar()

    def load_photo(self):
        self.photo_path.set(filedialog.askopenfilename())  # opens dialog window and save selected file path

    def load_watermark(self):
        self.watermark_path.set(filedialog.askopenfilename())
        if self.photo_path.get() and self.watermark_path.get():  # if file paths not empty
            self.image = Image.open(self.photo_path.get())  # open image file path and assign image to object

            watermark = Image.open(self.watermark_path.get())

            # Make the image as transparent as needed
            watermark = watermark.convert("RGBA")
            datas = watermark.getdata()
            new_data = []
            for item in datas:
                # change all white (also shades of whites) pixels to transparent
                if item[0] > 200 and item[1] > 200 and item[2] > 200:
                    new_data.append((255, 255, 255, 0))
                else:
                    # pixels are left unchanged.
                    new_data.append(item)

            # Update watermark image
            watermark.putdata(new_data)

            # Calculate the watermark size as a fraction of the image size
            watermark_width = int(self.image.size[0] * 0.2)
            watermark_height = int(watermark_width * (watermark.size[1] / watermark.size[0]))

            # Resize the watermark
            watermark = watermark.resize((watermark_width, watermark_height), Image.LANCZOS)

            # Calculate the position to place the watermark
            position = (self.image.size[0] - watermark_width + 30, self.image.size[1] - watermark_height + 90)

            # Paste watermark on image
            self.image.paste(watermark, position, watermark)

            # Resize the image for display
            canvas_image = self.resize_image(self.image, 40)
            # Convert the PIL Image object to a PhotoImage object
            self.photo_image = ImageTk.PhotoImage(canvas_image)

            # Canvas for the display
            canvas = Canvas(root, width=canvas_image.width, height=canvas_image.height)
            canvas.grid(row=2, column=0, columnspan=3)
            canvas.delete("all")
            canvas.create_image(0, 0, anchor=NW, image=self.photo_image)
            Button(root, text='Save Image', command=self.save_image).grid(row=3, column=1, padx=5, pady=5)

    def resize_image(self, image, percent):
        width, height = image.size
        new_width = int(width * percent / 100)
        new_height = int(height * percent / 100)
        return image.resize((new_width, new_height), Image.LANCZOS)

    def save_image(self):
        if messagebox.askyesno('Save Image', 'Do you want to save the image?'):
            head, tail = os.path.split(self.photo_path.get())
            filename, ext = os.path.splitext(tail)
            saved_image_path = os.path.join(head, f'{filename}_watermarked{ext}')
            self.image.save(saved_image_path)
            self.saved_image_path.set('Saved Image Path: ' + saved_image_path)
            Label(root, textvariable=self.saved_image_path).grid(row=4, column=0, columnspan=3, padx=5, pady=5)
            img = Image.open(saved_image_path)
            img.show()


root = Tk()
root.title("Watermark App")
app = WatermarkApp()

# Image selection button and entry
Label(root, text='Image Path').grid(row=0, column=0, padx=5, pady=5)
Entry(root, textvariable=app.photo_path, width=50).grid(row=0, column=1, padx=5, pady=5)
Button(root, text='Upload Image', command=app.load_photo).grid(row=0, column=2, padx=5, pady=5)

# Watermark selection button and entry
Label(root, text='Watermark Path').grid(row=1, column=0, padx=5, pady=5)
Entry(root, textvariable=app.watermark_path, width=50).grid(row=1, column=1, padx=5, pady=5)
Button(root, text='Upload Watermark', command=app.load_watermark).grid(row=1, column=2, padx=5, pady=5)

root.mainloop()
