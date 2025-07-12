import requests

url = "http://localhost:8000/token"
data = {
    "username": "newuser1",
    "password": "newpassword123"
}
response = requests.post(url, data=data)
print(response.status_code, response.text) 