# Similar Article Search

## Outline

In this project I build a similarity search engine for scientific articles. It will use the representational learning to transform an article body into an embedding. It is using BERT pretraied embeddins to calculate cosine distance between them to find most similar papers to the one that is selected by user.

Papers are then ranked based on their similarity scores and five most similar papers are returned.

## ML Objective

To provide user with a similar article to one that they specify.

Input are the title, authors and an abstract of a paper.

Representation learning - to find embeddings of research paper, abstracts. These are ranked by calculating cosine similarity to the query text.

## Data Preparation

ArXiv Dataset containing 1.7 milion research papers are basis for the search. User click interactions should also be recorded.

### Feature engineering

Classical tokenization and creating input tensors based on abstracts. Another step can be to concatenate embeddings for authors, or some similarity based on coauthorships
as well as research category from arXiv to improve the search.

## Model

### Model selection

The BERT architecture is used to obtain embeddings because it provides bidirectional context and improves embeddings.

### Model training

We use a pretrained BERT basic model where we transfer learned embeddings onto our abstracts, since we dont have any information (human feedback) on similarity of abstracts. However, we provide a feature for a user to approve suggested articles.
This information can be used to further fine tune BERT's embeddings.

We could try to create an artificial abstracts (for example using chatgpt to create a rewritten versions, **self-supervision**)

### Loss function

There is no loss function since I am not performing any training. 

However, with user feedback data available wher we have similar/dissimilar measurments we could use MRR - average rank of the first relevant item in each output list produced by the model.
Recall@k
Precision@k

## Serving

### Prediction pipeline

#### Embedding Generation Service

Compute the embedding of the input query abstract. It preprocess the text and uses pre-trained BERT model to determine embedding.

#### Similarity Service

Uses cosine similarity to calculate similar articles in the embedding space. It can be cosine similarity or other similarity calculating algorithm, like for example k-nearest neighbors.

#### Re-ranking Service

It filters output.

### Indexing pipeline

#### Indexing Service

All abstracts on the platform are indexed by this service to improve search performance. It keeps indexing up to date, when new abstracts are added every week.

