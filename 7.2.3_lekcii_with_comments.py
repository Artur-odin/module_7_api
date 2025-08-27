import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

def get_random_dog_image():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        response.raise_for_status()
        data = response.json()
        return data['message']
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при запросе к API: {e}")
        return None

def show_image():
    image_url = get_random_dog_image()
    if image_url:
        try:
            # 📡 Загружаем изображение по URL потоково (экономим память)
            response = requests.get(image_url, stream=True)
            # ⚠️ Проверяем успешность запроса (вызовет исключение при ошибке)
            response.raise_for_status()
            # 🔄 Конвертируем байты в файлоподобный объект для PIL
            img_data = BytesIO(response.content)
            # 🖼️ Открываем изображение из байтов (создаем PIL Image объект)
            img = Image.open(img_data)
            # 📏 Уменьшаем размер до 300x300 пикселей (сохраняя пропорции)
            img.thumbnail((300, 300))
            # 🔄 Конвертируем PIL Image в формат понятный tkinter
            img = ImageTk.PhotoImage(img)
            # 📺 Устанавливаем изображение в Label виджет
            label.config(image=img)
            # 🔗 Сохраняем ссылку чтобы изображение не удалилось из памяти
            label.image = img
        except requests.RequestException as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

window = Tk()
window.title("Картинки с собачками")
window.geometry("360x420")
label = Label()
label.pack(padx=10, pady=10)

button = Button(text="Загрузить изображение", command=show_image)
button.pack(padx=10, pady=10)
window.mainloop()