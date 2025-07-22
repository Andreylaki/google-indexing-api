from pathlib import Path
import os

# Сделать рабочей папкой ту, где лежит google_indexing.py
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)

# Теперь все пути можно указывать относительно этой папки:
urls_file = Path("urls/urls.txt")
service_account_file = Path("сюда вписать ключ.json")

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/indexing"]

# Читаем URLs из файла
with urls_file.open("r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]

credentials = service_account.Credentials.from_service_account_file(
    str(service_account_file), scopes=SCOPES)

service = build('indexing', 'v3', credentials=credentials)

sent = 0
for url in urls:
    body = {
        "url": url,
        "type": "URL_UPDATED"
    }
    try:
        response = service.urlNotifications().publish(body=body).execute()
        print(f"Отправлено: {url} — ответ: {response}")
        sent += 1
    except Exception as e:
        print(f"Ошибка при отправке {url}: {e}")

print(f"\nВсего отправлено на переиндексацию: {sent}")