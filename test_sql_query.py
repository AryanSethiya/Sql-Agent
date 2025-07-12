import requests

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuZXd1c2VyMSIsImV4cCI6MTc1MjMwNzAzN30.mRIh7HQ_b6Mw3mgLysy9Nv-uik_vOWyj00g4r1XgtvE"
headers = {
    "Authorization": f"Bearer {token}"
}
url = "http://localhost:8000/sql/query"
data = {
    "query": "SELECT * FROM employees LIMIT 3",
    "description": "Test query"
}
response = requests.post(url, json=data, headers=headers)
print(response.status_code, response.text) 