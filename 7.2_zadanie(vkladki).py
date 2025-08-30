import requests
from tkinter import Tk, Toplevel, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')  
        response.raise_for_status()
        data = response.json()
        return data["message"]
    except requests.RequestException as e:
        messagebox.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None

def show_image():
    status_label.config(text="Загрузка...")
    image_url = get_random_dog_image()

    if image_url:
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)
            img = ImageTk.PhotoImage(img)

            tab = ttk.Frame(notebook)
            notebook.add(tab, text=f"Изображение {notebook.index('end') + 1}")
            label = ttk.Label(tab, image=img)
            label.image = img
            label.pack(padx=10, pady=10)

            status_label.config(text="")
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

def start_progress():
    progress['value'] = 0
    progress.start(30)
    window.after(3000, lambda: [progress.stop(), show_image()])

def del_tabs():# ф-я удаления всех вкладок
    for tab in notebook.tabs():
        notebook.forget(tab)# можно индекс 0 указать, эффект тот-же.

window = Tk()
window.title("Случайное изображение")
frame = ttk.Frame(window, padding=10)
frame.pack(pady=10)

status_label = ttk.Label(window, text="")
status_label.pack(padx=10, pady=(5, 5))

button_1 = ttk.Button(frame, text="Загрузить изображение", command=start_progress)
button_1.grid(row=0, column=1)
button_2 = ttk.Button(frame, text="Очистить вкладки", command=del_tabs)# кнопка для удаления всех вкладок
button_2.grid(row=0, column=2)

progress = ttk.Progressbar(window, mode='determinate', length=300)
progress.pack(padx=10, pady=(0, 5))

width_label = ttk.Label(window, text="Ширина:")
width_label.pack(side='left', padx=(10, 0), pady=(0, 5))
width_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side='left', padx=(0, 10), pady=(0, 5))
width_spinbox.set(300)

height_label = ttk.Label(window, text="Высота:")
height_label.pack(side='left', padx=(10, 0), pady=(0, 5))
height_spinbox = ttk.Spinbox(window, from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side='left', padx=(0, 10), pady=(0, 5))
height_spinbox.set(300)

# Создаем отдельное окно для Notebook
top_level_window = Toplevel(window)
top_level_window.title("Изображения пёсиков")

notebook = ttk.Notebook(top_level_window)
notebook.pack(expand=True, fill='both', padx=10, pady=10)

window.mainloop()