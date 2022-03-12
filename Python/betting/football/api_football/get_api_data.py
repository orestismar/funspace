import requests

url = "https://api-football-v1.p.rapidapi.com/v3/timezone"

headers = {
    'x-rapidapi-key': "640e75bfa1msh1fe61fb1c1a2310p18e96ejsn56372184e24b",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers)

print(response.text)

