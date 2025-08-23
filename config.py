import os
from dotenv import load_dotenv

# Загружаем переменные из .env (файл ищется в той же папке, где лежит config.py)
load_dotenv()

# Читаем настройки
API_ID      = int(os.getenv("API_ID", 0))
API_HASH    = os.getenv("API_HASH",  "").strip()
SESSION_NAME = os.getenv("SESSION_NAME", "session")
TARGET_PEER = os.getenv("TARGET_PEER_ID",  "").strip()

# Мониторинг бота
ADMIN_USERNAME = "@itsaliveor"  # Основной канал (обычные уведомления - без звука)
EMERGENCY_USERNAME = "@soooonsoooon"  # Экстренный канал (ошибки, критические события - со звуком)
HEARTBEAT_INTERVAL = 20  # Сообщение "я жив" каждые 10 минут (600 сек)
ENABLE_HEARTBEAT = True   # Включить/выключить heartbeat
