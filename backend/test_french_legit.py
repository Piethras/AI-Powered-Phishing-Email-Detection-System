import requests

response = requests.post(
    "http://127.0.0.1:5000/api/predict",
    json={
        "sender": "marie.dupont@entreprise.fr",
        "subject": "Réunion de lundi",
        "body": "Bonjour à tous, je vous rappelle que la réunion d'équipe aura lieu lundi à 10h dans la salle de conférence. Merci de préparer vos points d'avancement. Cordialement, Marie",
    },
)

print(response.status_code)
print(response.json())