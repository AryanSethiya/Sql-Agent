import requests

url = "http://localhost:8000/register"
data = {
    "username": "newuser1",
    "email": "newuser1@example.com",
    "password": "newpassword123"
}
response = requests.post(url, json=data)
print(response.status_code, response.text) 