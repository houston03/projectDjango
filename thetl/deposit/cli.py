import requests
import json

url = 'http://127.0.0.1:8000/calculate/'
data = {
    "date": "31.01.2021",
    "periods": 4,
    "amount": 10000,
    "rate": 8
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()

    print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Ошибка при отправке запроса: {e}")
except json.JSONDecodeError as e:
    print(f"Ошибка декодирования ответа: {e}")