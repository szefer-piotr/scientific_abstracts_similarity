# Similar Article Search

## Outline

In this project I build a similarity search engine for scientific articles. It will use the representational learning to transform an article body into an embedding. It is using BERT pretraied embeddins to calculate cosine distance between them to find most similar papers to the one that is selected by user.

Papers are then ranked based on their similarity scores and five most similar papers are returned.

## Model

The BERT architecture is used to obtain embeddings.
