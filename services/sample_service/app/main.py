import json

import requests
import os

from fastapi import FastAPI

app = FastAPI(title="Sample Service")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000")

@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from AKS"}

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}

@app.get("/sample")
def sample() -> dict[str, str]:
    return {"message": "Hello from Sample Service"}

@app.get("/test-auth")
def test_auth() -> dict[str, str]:
    try:
        response = requests.get(f"{AUTH_SERVICE_URL}/health")
        response.raise_for_status()
        return {"message": "Auth service is reachable", "auth_service_status": json.dumps(response.json())}
    except requests.RequestException as e:
        return {"message": "Failed to reach auth service", "error": str(e)}