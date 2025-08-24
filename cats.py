from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

def loade_image():
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        return ImageTk.photoImage(img)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None
        
window = Tk()
window.title("Cats")
window.geometry("600x480")

label = Label()
label.pack()

url = "https://cataas.com/cat"
img = loade_image(url)

if img:
    label.config(image=img)
    label.image = img

window.mainloop()