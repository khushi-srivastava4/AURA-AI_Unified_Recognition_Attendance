import requests
import streamlit as st

BASE_URL = st.secrets.get(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

def api_get(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def api_post(endpoint, data=None, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.post(
        f"{BASE_URL}{endpoint}",
        json=data,
        headers=headers
    )

    response.raise_for_status()

    return response.json()


def api_delete(endpoint, token=None):
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.delete(
        f"{BASE_URL}{endpoint}",
        headers=headers
    )

    response.raise_for_status()

    return response.json()