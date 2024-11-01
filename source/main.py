from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
import time
from tkinter import ttk  # Для использования обводки


# Создаем главное окно
root = Tk()
root.title("IoT-Lab1")
root.geometry("750x400")

# Данные для графика
x_data = []
y_data = []

# Начальный уровень дыма
smoke_level = 50
update_interval = 1000  # Интервал обновления в миллисекундах
threshold_level = 80  # Пороговое значение по умолчанию

# Настраиваем график
fig, ax = plt.subplots()
line, = ax.plot(x_data, y_data, color='red')
threshold_line = ax.axhline(y=threshold_level, color='blue', linestyle='--', label='Порог')  # Линия порога
ax.set_xlabel('Время (с)')
ax.set_ylabel('Уровень дыма')
ax.set_ylim(0, 100)  # Диапазон значений для уровня дыма

# Встраиваем график в окно Tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().place(width=550, height=400, x=200, y=0)

# Функция для плавного изменения уровня дыма
def smooth_smoke_level(current_level):
    if current_level > 0:
        change = random.uniform(-5, 5)  # Плавное изменение от -5 до +5
    else:
        change = 0
    new_level = current_level + change
    new_level = max(0, min(100, new_level))  # Убедимся, что уровень дыма в пределах 0-100
    return new_level

# Функция для снижения уровня дыма при включении системы тушения
def reduce_smoke_level(current_level):
    if current_level > 0:
        return max(0, current_level - 10)  # Плавное снижение на 10
    return current_level

# Функция для обновления графика
def update_graph():
    global smoke_level, update_interval  # Используем глобальный уровень дыма и интервал обновления

    # Если уровень дыма превышает порог, включаем систему тушения
    if smoke_level > threshold_level:
        status_label.config(text="Пожар!\nВключена система тушения", fg="red")
        smoke_level = reduce_smoke_level(smoke_level)
    else:
        status_label.config(text="Система в норме", fg="green")

    # Обновляем данные уровня дыма плавно, если не в ручном режиме
    if not manual_mode.get() and smoke_level <= threshold_level:
        smoke_level = smooth_smoke_level(smoke_level)

    # Добавляем новые данные
    current_time = time.time()
    x_data.append(current_time)
    y_data.append(smoke_level)

    # Ограничиваем количество точек на графике
    if len(x_data) > 10:
        x_data.pop(0)
        y_data.pop(0)

    # Обновляем данные линии на графике
    line.set_xdata([x - x_data[0] for x in x_data])  # Смещаем время на графике
    line.set_ydata(y_data)

    # Обновляем лимиты оси X
    ax.set_xlim(0, x_data[-1] - x_data[0] + 1)

    # Обновляем пороговую линию
    threshold_line.set_ydata([threshold_level])

    # Перерисовываем график
    canvas.draw()

    # Вызываем функцию снова через время, указанное пользователем
    root.after(update_interval, update_graph)

# Функция для изменения интервала обновления через ползунок
def update_interval_slider(val):
    global update_interval
    update_interval = int(val)  # Преобразуем значение ползунка в целое число (мс)

# Функция для изменения уровня дыма вручную
def update_smoke_level(val):
    global smoke_level
    smoke_level = float(val)  # Устанавливаем новый уровень дыма, введенный пользователем

# Функция для обновления состояния ползунка уровня дыма
def toggle_manual_mode():
    if manual_mode.get():  # Если ручной режим включен
        smoke_slider.config(state=NORMAL)  # Сделать ползунок доступным
    else:
        smoke_slider.config(state=DISABLED)  # Сделать ползунок недоступным

# Функция для изменения порога
def update_threshold_slider(val):
    global threshold_level
    threshold_level = float(val)  # Устанавливаем новое пороговое значение

# Добавляем обводку для ручного режима и ползунка уровня дыма
manual_frame = ttk.LabelFrame(root, text="Настройки руч. режима", padding=(10, 10))
manual_frame.place(x=10, y=50, width=180, height=200)

# Флажок для включения ручного режима
manual_mode = IntVar()
manual_checkbox = Checkbutton(manual_frame, text="Ручной режим", variable=manual_mode, command=toggle_manual_mode)
manual_checkbox.pack(anchor='w')

# Ползунок для ручного изменения уровня дыма (изначально заблокирован)
Label(manual_frame, text="Уровень дыма").place(x=25, y=70)
smoke_slider = Scale(manual_frame, from_=0, to=100, orient=HORIZONTAL, command=update_smoke_level, state=DISABLED)
smoke_slider.set(smoke_level)
smoke_slider.place(x=22, y=30)
# Ползунок для изменения порога уровня дыма
Label(root, text="Порог уровня дыма").place(x=30, y=220)
threshold_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=update_threshold_slider)
threshold_slider.set(threshold_level)
threshold_slider.place(x=45, y=180)

# Ползунок для изменения частоты обновления графика
Label(root, text="Частота обновления \nграфика (мс)").place(x=30, y=360)
interval_slider = Scale(root, from_=500, to=10000, orient=HORIZONTAL, command=update_interval_slider, resolution=100)
interval_slider.set(update_interval)
interval_slider.place(x=38, y=320)

# Надпись для статуса системы тушения
status_label = Label(root, text="Система в норме", font=("Arial", 14), fg="green")
status_label.place(x=5, y=10)

# Запускаем обновление графика
root.after(update_interval, update_graph)

# Запускаем главный цикл
root.mainloop()
