# SatDex Monitor 🛰️

![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)

SatDex Monitor es un script automatizado en Python diseñado para monitorear el estado de satélites específicos (como **UTNH** y **USAT-1**) a través de la red global de estaciones terrestres [SatNOGS](https://satnogs.org/).

El sistema revisa constantemente la API de SatNOGS para detectar si hay nueva telemetría o si el estado de los satélites cambia a "Activo" (alive). Cuando se detecta un cambio importante, envía inmediatamente una alerta a través de un bot de **Telegram**.

## 🚀 Características

- **Monitoreo Automático**: Utiliza GitHub Actions para ejecutarse automáticamente cada 10 minutos.
- **Alertas en Tiempo Real**: Notificaciones inmediatas a un chat de Telegram.
- **Gestión de Estado**: Mantiene un historial (caché) local para no enviar alertas duplicadas.
- **Fácilmente Extensible**: Puedes añadir más satélites a la lista de monitoreo fácilmente.

## 🛠️ Tecnologías

- [Python 3](https://www.python.org/)
- [Requests](https://pypi.org/project/requests/) (para peticiones a la API)
- [GitHub Actions](https://github.com/features/actions) (para ejecución periódica)
- [SatNOGS API](https://db.satnogs.org/api/)

## ⚙️ Configuración y Uso

Este proyecto está diseñado para funcionar de manera desatendida en GitHub Actions. Para configurarlo en tu propio repositorio (haciendo un fork o clonando):

### 1. Preparar Telegram
1. Crea un bot de Telegram hablando con [@BotFather](https://t.me/botfather) y obtén el **Token del Bot**.
2. Obtén tu **Chat ID** de Telegram (puedes usar bots como `@userinfobot` para averiguarlo) o el ID del grupo donde quieres recibir las notificaciones.

### 2. Configurar GitHub Secrets
Ve a la pestaña `Settings` > `Secrets and variables` > `Actions` de tu repositorio en GitHub y crea los siguientes secretos:
- `TELEGRAM_BOT_TOKEN`: El token de tu bot de Telegram.
- `TELEGRAM_CHAT_ID`: Tu ID de chat de Telegram.

### 3. Personalizar Satélites
Si deseas monitorear otros satélites, edita la variable `SATELLITES_TO_MONITOR` dentro del archivo `monitor.py`:
```python
SATELLITES_TO_MONITOR = ['UTNH', 'USAT-1']
```

## 💻 Ejecución Local

Si prefieres ejecutar el script manualmente en tu computadora:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/satdex-monitor.git
   cd satdex-monitor
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Exporta las variables de entorno necesarias:
   ```bash
   export TELEGRAM_BOT_TOKEN="tu_token_aqui"
   export TELEGRAM_CHAT_ID="tu_chat_id_aqui"
   ```

4. Ejecuta el script:
   ```bash
   python monitor.py
   ```

## 🔄 ¿Cómo funciona el caché?

El script guarda el estado actual de los satélites en un archivo llamado `sat_cache.json`. GitHub Actions hace un *commit* de este archivo automáticamente después de cada ejecución. Esto permite que en la siguiente ejecución el script sepa cuál era el estado anterior y pueda determinar si es necesario enviar una nueva alerta.
