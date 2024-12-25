import json

JSON_FILE_PATH = '/home/piotr/projects/articles_similarity/scientific_abstracts_similarity/data/arxiv_papers/arxiv-metadata-oai-snapshot.json'
JSON_SAVE_FILE = '/home/piotr/projects/articles_similarity/scientific_abstracts_similarity/data/arxiv_papers/arxiv-metadata-10000.json'
# print('Open the file')

# with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
#     ll = [json.loads(line.strip()) for line in f.readlines()]
#     print(len(ll))
#     size_of_the_split = 2000
#     total = len(ll) // size_of_the_split
#     print(total+1)
#     for i in range(total+1):
#         json.dump(ll[i*size_of_the_split:(i+1)*size_of_the_split], 
#                   open(
#                       '/home/piotr/projects/articles_similarity/scientific_abstracts_similarity/data/arxiv_papers/' + str(i+1) + ".json", "w", encoding='utf8'
#                   ), ensure_ascii=False, indent=True)

TEXT_LIM = 10000

# # Get some data
texts = []
with open(JSON_FILE_PATH, 'r') as f:
    for line in f:
        data = json.loads(line)
        texts.append(data)
        if len(texts) > TEXT_LIM:
            break


with open(JSON_SAVE_FILE, "w") as final:
	json.dump(texts, final)