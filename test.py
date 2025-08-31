import asyncio
from g4f.client import AsyncClient
import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import requests
import threading
from g4f.client import AI2image

async def generate(prompt_user):
    client = AI2image()
    try:
        response = await client.images.generate(
            prompt=prompt_user,
            model="flux",
            response_format="url"
            # Add any other necessary parameters
        )
        return response.data[0].url
    except Exception as e:
        print(f"Ошибка обработки: {e}, по запросу: {prompt_user}")

async def load_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((300, 300))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")

def show_image(img, prompt_user):
    new_window = tk.Toplevel(window)
    new_window.title(f"Изображение по запросу: {prompt_user}")
    new_window.geometry("400x300")
    label = ttk.Label(new_window, image=img)
    label.image = img  # сохраняем ссылку
    label.pack(pady=20)

results = []

async def main(prompt_user):
    response = await generate(prompt_user)
    if response:
        img = await load_image(response)
        results.append((img, prompt_user))

def start_main():
    prompt_user = entry_input.get()
    entry_input.delete(0, 'end')  # очищаем сразу же при нажатии
    ttk.Label(window, text=f"Обрабатывается: {prompt_user}").pack()
    
    thread = threading.Thread(target=lambda: asyncio.run(main(prompt_user)))
    thread.start()
    
    check_results()

def check_results():
    if results:  # если есть результаты
        img, prompt = results.pop(0)
        show_image(img, prompt)
        #entry_input.delete(0, 'end')
    
    if results:  # если еще остались результаты - проверяем снова
        window.after(100, check_results)

window = tk.Tk()
window.title("Генератор изображений")
window.geometry("400x300")

label_input = ttk.Label(window, text="Введите текст для генерации изображения:")
label_input.pack(pady=10)
entry_input = ttk.Entry(window)
entry_input.pack(pady=10)
button_input = ttk.Button(window, text="Отправить", command=start_main)
button_input.pack(pady=10)

window.mainloop()