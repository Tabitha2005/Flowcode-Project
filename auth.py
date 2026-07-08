import requests
from config import AUTH_URL, CLIENT_ID, CLIENT_SECRET


def get_bearer_token():
    response = requests.post(
        AUTH_URL,
        headers={"accept": "application/json", "content-type": "application/json"},
        json={"clientId": CLIENT_ID, "secret": CLIENT_SECRET},
    )
    response.raise_for_status()
    data = response.json()
    return data["accessToken"], data["refreshToken"]


def refresh_bearer_token(current_token, refresh_token):
    refresh_url = "https://authn.flowcode.com/identity/resources/auth/v2/api-token/token/refresh"
    response = requests.post(
        refresh_url,
        headers={
            "Authorization": f"Bearer {current_token}",
            "Content-Type": "application/json",
        },
        json={"refreshToken": refresh_token},
    )
    response.raise_for_status()
    data = response.json()
    return data["accessToken"], data["refreshToken"]


# Demo mode mock
def get_demo_token():
    return "DEMO_TOKEN", "DEMO_REFRESH_TOKEN"
