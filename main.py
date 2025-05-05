from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# Ces variables doivent être définies dans l'environnement Render
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
TENANT_ID = os.getenv("TENANT_ID")

def get_token():
    token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(token_url, data=payload)
    return response.json().get("access_token")

@app.get("/graph")
def call_graph_api():
    token = get_token()
    if not token:
        return {"error": "Échec d'obtention du token"}

    headers = {"Authorization": f"Bearer {token}"}
    graph_url = "https://graph.microsoft.com/v1.0/users/vdhers@jbbernard.fr/calendar/events?$top=10"
    response = requests.get(graph_url, headers=headers)
    return response.json()

@app.post("/graph/create")
async def create_event(req: Request):
    data = await req.json()
    token = get_token()
    if not token:
        return {"error": "Échec d'obtention du token"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    url = "https://graph.microsoft.com/v1.0/users/vdhers@jbbernard.fr/events"
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.get("/ping")
def ping():
    return {"status": "ok"}
