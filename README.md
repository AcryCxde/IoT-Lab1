## Подключиться к MSQTT клиенту:
 

 - **Просмотр данных:** `mosquitto_sub -h test.mosquitto.org -t iot_lab1/smoke_level`
 
 - **Установка режима:**  
	 - **Ручной:** `mosquitto_pub -h test.mosquitto.org -t "iot_lab1/mode" -m "manual"`
	 - **Автоматический:** `mosquitto_pub -h test.mosquitto.org -t "iot_lab1/mode" -m "auto"`

 - **Активация акуатора (доступна только в ручном режиме):** `mosquitto_pub -h test.mosquitto.org -t "iot_lab1/actuator" -m "activate"`

## Запуск программы:
**Запустите исполняемый файл main.py**