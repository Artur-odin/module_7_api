import asyncio
from g4f.client import AsyncClient
import tkinter as tk
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
import requests
import threading

requests_list = [] # очередь отправки запросов

def request_user(): #сохраняем запрос из поля ввода и очищаем поле ввода
    prompt = entry_input.get().strip()
    entry_input.delete(0, 'end')
    return prompt

async def response_AI(prompt_user): # обработка запроса ИИ асинхронно
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

async def load_image(url): # загрузка данных и преобразование в изображения тоже может занять время, тоже асинхронно
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

def show_image(img, prompt_user): # создание и зугрузка изображения в новое окно
    new_window = tk.Toplevel(window)
    new_window.title(f"Изображение по запросу: {prompt_user}")
    new_window.geometry("400x300")
    label = ttk.Label(new_window, image=img)
    label.image = img  # сохраняем ссылку
    label.pack(pady=20)

async def new_window(url, prompt_user): # два процесса: создание картинги и загрузка в новое окно
    img = await load_image(url)
    if img:
        show_image(img, prompt_user)

async def main(prompt_user): # основная ф-я запускает два процесса: обработку и вывод запроса, загрузку и вывод изображения
    requests_list.append(prompt_user) # отправляем запрос в очередь
    while requests_list.index(prompt_user) > 0: # если запрос не обработан ждем секнду
        await asyncio.sleep(5)
    result = await response_AI(prompt_user)
    requests_list.pop(0)
    if result is None:
        print("Прерываем выполнение - нет URL")
        return
    if result:
        await new_window(*result)

def start_main(): # сохраняем и освобождаем поле ввода и запускаем основную ф-ю в одельном процессе
    prompt_user = request_user()
    if not prompt_user:
        return print("Пустой запрос")
    # пытался избежать использования данной ф-ии, но удалить данные из поля ввода для нового ввода оказалось невозможным из-за блокировки GUI
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