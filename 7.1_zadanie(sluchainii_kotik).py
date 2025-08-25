from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Список доступных тегов
ALLOWED_TAGS = ['sleep', 'jump', 'smile', 'fight', 'black', 'white', 'red', 'siamese', 'bengal']

def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        img = Image.open(image_data)
        img.thumbnail((600, 480), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке изображения: {e}")
        return None

def teg_cate_url(): # отдельная ф-я - на каждую кнопку можно указать разные варианты (только рандом или с тегом и рандом)
    # открывается так же в новом окне через файл или кнопкой "Загрузить фото" рядом с combobox
    tag = tag_combobox.get()
    url = f"https://cataas.com/cat/{tag}" if tag else 'https://cataas.com/cat'
    open_new_window(url)

def random_cat_url(): # открывает кнопкой "Случайный котик" во вкладках основного окна
    tab = Frame(notebook)
    notebook.add(tab, text="Котик")
    close_button = Button(tab, text="✕", command=lambda: close_tab(tab))
    close_button.pack(anchor="ne")
    img = load_image("https://cataas.com/cat")
    if img:
        label = Label(tab, image=img)
        label.image = img
        label.pack()
    notebook.select(tab)
    def close_tab(tab):
        notebook.forget(tab)
    
def open_new_window(url):# открывает любой URL что в него загрузят
    img = load_image(url)
    if img:
        new_window = Toplevel()
        new_window.title("Cat Image")
        new_window.geometry("600x480")
        label = Label(new_window, image=img)
        label.image = img
        label.pack()
        
window = Tk()
window.title("Cats!")
window.geometry("600x520")

frame_1 = Frame(window)
frame_1.pack()
frame_2 = Frame(window)
frame_2.pack()

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Файл", menu=file_menu)
file_menu.add_command(label="Загрузить фото", command=teg_cate_url)
file_menu.add_separator()
file_menu.add_command(label="Выход", command=window.destroy)

tag_label = Label(frame_1, text="Выбери тег")
tag_label.grid(row=0, column=0)

tag_combobox = ttk.Combobox(frame_1, values=ALLOWED_TAGS)
tag_combobox.grid(row=1, column=0)

button_teg_cat = Button(frame_1, text="Загрузить фото", command=teg_cate_url)
button_teg_cat.grid(row=1, column=1)

button_random_cat = Button(frame_1, text="Cлучайный котик", command=random_cat_url)
button_random_cat.grid(row=1, column=2)

notebook = ttk.Notebook(window)
notebook.pack(fill=BOTH, expand=True)

window.mainloop()