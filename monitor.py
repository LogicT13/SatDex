import requests
import json
import os
import sys

# Configuracion desde variables de entorno (GitHub Secrets)
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

SATELLITES_TO_MONITOR = ['UTNH', 'USAT-1']
CACHE_FILE = 'sat_cache.json'

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Falta configurar los tokens de Telegram.")
        return
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message}
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()
        print("Mensaje de Telegram enviado!")
    except Exception as e:
        print(f"Error al enviar mensaje a Telegram: {e}")

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_cache(cache_data):
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache_data, f)

def check_satnogs():
    cache = load_cache()
    new_alerts = []
    
    # Esta URL usa la API publica de SatNOGS para buscar por nombre
    # y ver si el estado cambio a "Alive" o si hay telemetria reciente.
    for sat in SATELLITES_TO_MONITOR:
        url = f"https://db.satnogs.org/api/satellites/?search={sat}"
        headers = {'User-Agent': 'SatDex-Monitor/1.0'}
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            for s in data:
                sat_name = s.get('name', 'Unknown')
                sat_status = s.get('status', 'Unknown')
                norad_id = s.get('norad_cat_id', 'Unknown')
                
                # Checkeamos contra el cache
                prev_status = cache.get(sat_name, {}).get('status')
                
                if prev_status != sat_status:
                    if sat_status == 'alive':
                        new_alerts.append(f"🚀 ¡ALERTA SATDEX! 🚀\nEl satélite {sat_name} ahora figura como ACTIVO en la red global.\nNORAD ID: {norad_id}")
                    elif prev_status is None:
                        # La primera vez que corre, solo lo guardamos en cache
                        pass
                
                cache[sat_name] = {'status': sat_status, 'norad_id': norad_id}
                
        except Exception as e:
            print(f"Error revisando SatNOGS para {sat}: {e}")

    save_cache(cache)
    
    # Enviar las alertas
    for alert in new_alerts:
        send_telegram_message(alert)

if __name__ == '__main__':
    print("Iniciando revisión de satélites...")
    check_satnogs()
    print("Revisión completada.")
