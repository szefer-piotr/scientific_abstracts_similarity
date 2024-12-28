import requests
import time

query = {
    "query": "Markov Chain Monte Carlo",
}


# query = "Markov Chain Monte Carlo"

headers = {
    "Content-Type": "application/json",
}

url = "http://localhost:8080/similar_abstracts"
start = time.time()
response = requests.post(url=url, headers=headers, json=query)
end = time.time()
print(f"Time taken: {(end-start) * 1000:.8f} ms.")
print(f"Recieved status code {response.status_code}")
# print(f"Recieved {response.json()}")