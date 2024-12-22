import requests

data = {
    "query1": "Markov Chain Monte Carlo",
    "query2": "Markov Chain Monte Carlo",
}

headers = {
    "Content-Type": "application/json",
}

url = "http://localhost:8080/find_similar_abstracts"
response = requests.post(url=url, headers=headers, json=data)
print(f"Recieved status code {response.status_code}")
print(f"Recieved {response.json()}")