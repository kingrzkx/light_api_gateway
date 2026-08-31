import requests

url = "http://127.0.0.1:8000/api/demo"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIwMSIsImV4cCI6MTc4ODE5NTY0NX0.5FWLsnZHx2seDw4B78lQDjeVvTkjN76ZQN5AgHt-MH0"
}

resp = requests.get(url, headers=headers)
print(f"status={resp.status_code}")
print(resp.text)
