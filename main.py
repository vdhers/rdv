
from fastapi import FastAPI
import requests
import os

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
TENANT_ID = os.getenv("TENANT_ID")

@app.get("/graph")
def call_graph_api():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }

    token_response = requests.post(token_url, data=payload)
    token = token_response.json().get("access_token")

    if not token:
        return {"error": "Échec d'obtention du token"}

    headers = {"Authorization": f"Bearer {token}"}
    graph_url = "https://graph.microsoft.com/v1.0/users/vdhers@jbbernard.fr/calendar/events?$top=10"
    response = requests.get(graph_url, headers=headers)

    return response.json()
