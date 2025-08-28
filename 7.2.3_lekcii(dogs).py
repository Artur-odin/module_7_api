import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
from PIL import Image, ImageTk
from io import BytesIO
from tkinter import Toplevel

def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        mb.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None

def show_image():
    image_url = get_random_dog_image()
    if image_url:
        try:
            
            response = requests.get(image_url, stream=True)# 📡 Загружаем изображение по URL потоково (экономим память)
            response.raise_for_status() # ⚠️ Проверяем успешность запроса (вызовет исключение при ошибке)
            img_data = BytesIO(response.content)# 🔄 Конвертируем байты в файлоподобный объект для PIL
            img = Image.open(img_data)# 🖼️ Открываем изображение из байтов (создаем PIL Image объект)
            img_size = (int(width_spinbox.get()), int(height_spinbox.get()))
            img.thumbnail(img_size)# 📏 Уменьшаем размер до 300x300 пикселей (сохраняя пропорции)
            img = ImageTk.PhotoImage(img)# 🔄 Конвертируем PIL Image в формат понятный tkinter
            new_window = Toplevel(window)# 🌟 Создаем новое окно для отображения изображения
            new_window.title("Случайное изображение")# 📝 Устанавливаем заголовок окна
            lb = ttk.label(new_window, image=img)# 🖼️ Создаем Label с изображением)
            lb.pack()
            lb.image = img# 🔗 Сохраняем ссылку на изображение чтобы не удалилось из памяти
            #label.config(image=img)# 📺 Устанавливаем изображение в Label виджет
            #label.image = img# 🔗 Сохраняем ссылку чтобы изображение не удалилось из памяти
        except requests.RequestException as e:
            mb.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")
    progress.stop()

def prog():
    progress["value"] = 0
    progress.start(30)
    window.after(3000, show_image)

window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")
label = ttk.Label()
label.pack(padx=10, pady=10)

button = ttk.Button(text="Загрузить изображение", command=prog)
button.pack(padx=10, pady=10)
progress = ttk.Progressbar(mode="indeterminate", length=300)
progress.pack(pady=10)

width_label = ttk.Label(text="Ширина:")
width_label.pack(side=LEFT, padx=(10, 0))
width_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
width_spinbox.pack(side=LEFT, padx=(0, 10))

height_label = ttk.Label(text="Высота:")
height_label.pack(side=LEFT, padx=(10, 0))
height_spinbox = ttk.Spinbox(from_=200, to=500, increment=50, width=5)
height_spinbox.pack(side=LEFT, padx=(0, 10))


window.mainloop()