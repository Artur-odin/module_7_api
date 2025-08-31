import asyncio
from g4f.client import AsyncClient
import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import requests
import threading
#from g4f.Provider import (DeepInfra, OpenaiChat, HuggingChat, You, Gemini, Groq, OpenRouter)

def request_user():
    prompt = entry_input.get()
    entry_input.delete(0, 'end')
    return prompt

async def response_AI(prompt_user):
    client = AsyncClient()
    try:
        response = await client.images.generate(
            prompt=prompt_user,
            model="flux",
            response_format="url"
            # Add any other necessary parameters
        )
        return (response.data[0].url, prompt_user)
    except Exception as e:
        print(f"Ошибка обработки: {e}, по запросу: {prompt_user}")

#async def reg_res(): # ф-я 1
#    prompt_user = request_user()
#    url_and_promt = await response_AI(prompt_user)
#    return url_and_promt

async def load_image(url): # ф-я 2
    try:
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img.thumbnail((300, 300))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")
        return None

def show_image(img, prompt_user):
    new_window = tk.Toplevel(window)
    new_window.title(f"Изображение по запросу: {prompt_user}")
    new_window.geometry("400x300")
    label = ttk.Label(new_window, image=img)
    label.image = img  # сохраняем ссылку
    label.pack(pady=20)

async def new_window(url, prompt_user):
    img = await load_image(url)
    if img:
        show_image(img, prompt_user)

async def main(prompt_user):
    result = await response_AI(prompt_user)
    if result is None:
        print("Прерываем выполнение - нет URL")
        return
    if result:
        await new_window(*result)

def start_main():
    prompt_user = request_user()
    thread = threading.Thread(target=lambda: asyncio.run(main(prompt_user)))
    thread.start()
        
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