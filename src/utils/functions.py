import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../../.env'))

API_URL = os.environ['API_URL']
HF_TOKEN = os.environ['HF_TOKEN']


def generate_embedding(text: str) -> list[float]:

    response = requests.post(
        API_URL,
        headers={"Authorization": f"Bearer {HF_TOKEN}"},
        json={"inputs": text}
    )

    if response.status_code != 200:
        raise ValueError(f"Request failed with status code {response.status_code}: {response.text}")
    
    return response.json()