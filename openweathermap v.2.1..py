# Создать оконное приложение. Сделать так, чтобы с помощью API от openweathermap в окне выводилась
# информация о погоде в городе, название которого вводится в поле для ввода. Нужно сделать так,
# чтобы всё было на русском языке. Скомпилировать программу, exe файл вместе с исходным кодом загрузить на Github

from tkinter import *
import requests
from tkinter.messagebox import showerror
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageTk
import os, sys
import threading


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def save_image(url):
    response = requests.get(url)
    with open(resource_path("weather_icon.png"), "wb") as file:
        file.write(response.content)
    image = Image.open(resource_path("weather_icon.png"))
    return ImageTk.PhotoImage(image)


def show_weather():
    cityname = city.get()
    if not cityname:
        canvas.create_text(225, 350, text="", anchor="center")
        # picture.config(image="")
        showerror("Ошибка", "Строка не может быть пустой!")
    else:
        st_accept = "text/html"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        headers = {"Accept": st_accept, "User-Agent": user_agent}
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid=90154643e05772dfb09aa079236b068d&lang=ru", headers)
        if response.status_code != 404:
            response = response.json()
            img = save_image(f"https://openweathermap.org/img/wn/{response["weather"][0]["icon"]}@2x.png")
            canvas.create_window(225, 195, window=img, anchor="center")
            #
            # picture.config(image=img)
            #
            canvas.create_text(225, 350, font=("Times New Roman", 14),
                            text=f"{(response["weather"][0]["description"]).capitalize()}\n"
                            f"Температура: {round(response["main"]["temp"]-273.15, 1)} ℃\n"
                            f"Ощущается как: {round(response["main"]["feels_like"]-273.15, 1)} ℃\n"
                            f"Скорость ветра: {response["wind"]["speed"]} м/c\n"
                            f"Влажность: {response["main"]["humidity"]} %\n"
                            f"Давление: {response["main"]["pressure"]} мм.рт.ст.\n"
                            f"Восход солнца: {datetime.fromtimestamp(response["sys"]["sunrise"]).strftime("%H:%M")}\n"
                            f"Закат солнца: {datetime.fromtimestamp(response["sys"]["sunset"]).strftime("%H:%M")}", anchor="center")
        else:
            canvas.create_text(225, 350, text="", anchor="center")
            # picture.config(image="")
            showerror("Ошибка", "Указанный населенный пункт в OpenWeatherMap не найден!")


window = Tk()
window.title("Погода")
window.iconbitmap(resource_path("thermometer.ico"))
WIDTH = (window.winfo_screenwidth() // 2) - 250
HEIGHT = (window.winfo_screenheight() // 2) - 400
window.geometry(f"450x450+{WIDTH}+{HEIGHT}")
window.resizable(False, False)

canvas = Canvas(width=450, height=450)
python_image = PhotoImage(file="Skies.png")
canvas.create_image(200, 200, image=python_image)
canvas.pack(fill="both", expand=1)


canvas.create_text(225, 35, text="Укажите город", font=("Times New Roman", 18), anchor="center")

city = Entry(canvas)
canvas.create_window(225, 75, window=city, anchor="center")
city.focus()


def new_thread():
    thread = threading.Thread(target=show_weather)
    thread.start()


# Кнопка
button = Button(canvas, text="Узнать погоду", font=("Times New Roman", 12), command=new_thread)
canvas.create_window(225, 115, window=button, anchor="center")

# # Иконка с погодой
# picture = Label(canvas, bg="#B0E0E6")
# canvas.create_window(225, 195, window=picture, anchor="center")

window.mainloop()