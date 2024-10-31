from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from tkinter import ttk
import server

# Создаем главное окно
root = Tk()
root.title("IoT-Lab1")
root.geometry("750x400")

# Данные для графика
x_data = []
y_data = []

# Начальный уровень дыма
smoke_level = 50
update_interval = 5000
threshold_level = 80
fire_suppression_active = False  # Флаг, активен ли режим пожаротушения

# Настраиваем график
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data, color='red')
threshold_line = ax.axhline(y=threshold_level, color='blue', linestyle='--', label='Порог')
ax.set_xlabel('Время (с)')
ax.set_ylabel('Уровень дыма')
ax.set_ylim(0, 100)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(width=550, height=400, x=200, y=0)

# Функция для плавного изменения уровня дыма
def smooth_smoke_level(current_level):
    if current_level > 0:
        change = random.uniform(-5, 5)
    else:
        change = 0
    new_level = current_level + change
    return max(0, min(100, new_level))

def reduce_smoke_level(current_level):
    if current_level > 0:
        return max(0, current_level - 10)
    return current_level

def update_graph():
    global smoke_level, update_interval, fire_suppression_active

    # Если режим пожаротушения активен, уменьшаем уровень дыма
    if fire_suppression_active:
        smoke_level = reduce_smoke_level(smoke_level)
        if smoke_level == 0:  # Если уровень дыма достиг нуля, выключаем актуатор
            fire_suppression_active = False
    else:
        # Если уровень дыма выше порога, включаем пожаротушение
        if smoke_level > threshold_level:
            status_label.config(text="Пожар!\nВключена система тушения", fg="red")
            fire_suppression_active = True
        else:
            status_label.config(text="Система в норме", fg="green")
            if not manual_mode.get():  # Продолжаем генерировать случайные значения
                smoke_level = smooth_smoke_level(smoke_level)

    # Обновляем данные графика
    current_time = time.time()
    x_data.append(current_time)
    y_data.append(smoke_level)

    server.publish_sensor_data(smoke_level)

    if len(x_data) > 10:
        x_data.pop(0)
        y_data.pop(0)

    line.set_xdata([x - x_data[0] for x in x_data])
    line.set_ydata(y_data)
    ax.set_xlim(0, x_data[-1] - x_data[0] + 1)
    threshold_line.set_ydata([threshold_level])
    canvas.draw()

    root.after(update_interval, update_graph)

def update_interval_slider(val):
    global update_interval
    update_interval = int(val)

def update_smoke_level(val):
    global smoke_level
    smoke_level = float(val)

def toggle_manual_mode():
    if manual_mode.get():
        smoke_slider.config(state=NORMAL)
    else:
        smoke_slider.config(state=DISABLED)

def update_threshold_slider(val):
    global threshold_level
    threshold_level = float(val)

manual_frame = ttk.LabelFrame(root, text="Настройки руч. режима", padding=(10, 10))
manual_frame.place(x=10, y=50, width=180, height=200)

manual_mode = IntVar()
server.set_manual_mode(manual_mode)
manual_checkbox = Checkbutton(manual_frame, text="Ручной режим", variable=manual_mode, command=toggle_manual_mode)
manual_checkbox.pack(anchor='w')

Label(manual_frame, text="Уровень дыма").place(x=25, y=70)
smoke_slider = Scale(manual_frame, from_=0, to=100, orient=HORIZONTAL, command=update_smoke_level, state=DISABLED)
smoke_slider.set(smoke_level)
smoke_slider.place(x=22, y=30)

Label(root, text="Порог уровня дыма").place(x=30, y=220)
threshold_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=update_threshold_slider)
threshold_slider.set(threshold_level)
threshold_slider.place(x=45, y=180)

Label(root, text="Частота обновления \nграфика (мс)").place(x=30, y=360)
interval_slider = Scale(root, from_=500, to=10000, orient=HORIZONTAL, command=update_interval_slider, resolution=100)
interval_slider.set(update_interval)
interval_slider.place(x=38, y=320)

status_label = Label(root, text="Система в норме", font=("Arial", 14), fg="green")
status_label.place(x=5, y=10)

root.after(update_interval, update_graph)
root.mainloop()
