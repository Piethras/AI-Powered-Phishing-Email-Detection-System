import requests

with open("test_email.eml", "rb") as f:
    response = requests.post(
        "http://127.0.0.1:5000/api/upload",
        files={"file": f}
    )

print(response.status_code)
print(response.json())
