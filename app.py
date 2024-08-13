from flask import Flask, jsonify
import psutil
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)



load_dotenv()

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Umbral de uso de RAM y almacenamiento (90%)
RAM_THRESHOLD_PERCENT = 90
STORAGE_THRESHOLD_PERCENT = 90

def send_alert(message):
    # Enviar el mensaje al webhook de Google Chat
    payload = {'text': message}
    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code == 200:
        return 'Mensaje enviado al webhook de Google Chat'
    else:
        return f'Error al enviar mensaje al webhook de Google Chat. Código de estado: {response.status_code}'

def check_resource_usage():
    # Obtener el uso actual de RAM y almacenamiento
    ram_percent = psutil.virtual_memory().percent
    storage_percent = psutil.disk_usage('/').percent

    # Verificar si alguno de los recursos está por encima del umbral
    if ram_percent >= RAM_THRESHOLD_PERCENT or storage_percent >= STORAGE_THRESHOLD_PERCENT:
        message = f'Alerta: Uso elevado de recursos:\n'
        if ram_percent >= RAM_THRESHOLD_PERCENT:
            message += f'- Uso de RAM: {ram_percent}%\n'
        if storage_percent >= STORAGE_THRESHOLD_PERCENT:
            message += f'- Uso de almacenamiento: {storage_percent}%\n'

        # Enviar mensaje de alerta al webhook
        return send_alert(message)
    else:
        return 'Uso de recursos dentro del umbral normal'

@app.route('/')
def index():
    return 'Aplicación de monitoreo de recursos en funcionamiento.'

@app.route('/check_usage')
def check_usage():
    return check_resource_usage()

if __name__ == '__main__':
    app.run(debug=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
