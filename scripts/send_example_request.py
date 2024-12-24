import requests

query = {
    "query": "Markov Chain Monte Carlo",
}


# query = "Markov Chain Monte Carlo"

headers = {
    "Content-Type": "application/json",
}

url = "http://localhost:8080/similar_abstracts"
response = requests.post(url=url, headers=headers, json=query)
print(f"Recieved status code {response.status_code}")
print(f"Recieved {response.json()}")