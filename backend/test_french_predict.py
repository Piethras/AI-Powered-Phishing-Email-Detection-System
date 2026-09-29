import requests

response = requests.post(
    "http://127.0.0.1:5000/api/predict",
    json={
        "sender": "securite@paypa1-secure.fr",
        "subject": "Alerte de compte",
        "body": "Veuillez vérifiez votre compte, cliquez ici immédiatement pour éviter la suspension.",
    },
)

print(response.status_code)
print(response.json())