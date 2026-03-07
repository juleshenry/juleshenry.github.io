---
layout: post
title:  "The ML Smorgasbord Part 5: The Information Geometry of RAG"
date:   2026-04-11 10:00:00 -0000
categories: blog
mathjax: true
---

# Beyond Parametric Bottlenecks 🗄️

Welcome to Part 5! In Part 4, we showed how BERT-style Transformers learn to embed semantic information within their billions of weights $W \in \theta$. This is known as **parametric memory**. However, this memory is bounded by $O(|W|)$ and remains entirely static post-training, leading to catastrophic failure on factual temporal queries (hallucinations).

In 2021, Lewis et al. introduced **Retrieval-Augmented Generation (RAG)**, a hybrid model linking the continuous differentiable space of a sequence-to-sequence model with a massive **non-parametric** vector database. Let's dig into the math.

## 1. The Probabilistic Formulation of RAG

Standard language generation models the probability of generating token $y_i$ based solely on the input sequence $x$ and the preceding generated tokens $y_{<i}$:
$$ p_{\theta}(y_i | x, y_{<i}) $$

RAG modifies this by conditioning the generation on a latent variable $z$, which represents a retrieved document from an external corpus $\mathcal{Z}$. The system becomes a pipeline of two probabilistic components:
1. **The Retriever $p_\eta(z|x)$:** The probability of retrieving document $z$ given input $x$.
2. **The Generator $p_\theta(y_i|x, z, y_{<i})$:** The probability of generating token $y_i$ conditioned on both $x$ and $z$.

Lewis et al. proposed two mathematical formulations for marginalizing out the latent document $z$:

### RAG-Sequence
The model assumes the *entire sequence* $y$ is generated based on a single retrieved document $z$. We marginalize over the top-$k$ retrieved documents:
$$ p_{\text{sequence}}(y | x) = \sum_{z \in \text{top-}k} p_\eta(z | x) \prod_i^N p_\theta(y_i | x, z, y_{<i}) $$

### RAG-Token
The model assumes that the generation can pivot between different documents $z$ on a *per-token* basis, allowing it to synthesize facts from multiple distinct sources. We push the summation inside the product:
$$ p_{\text{token}}(y | x) = \prod_i^N \sum_{z \in \text{top-}k} p_\eta(z | x) p_\theta(y_i | x, z, y_{<i}) $$

## 2. Dense Passage Retrieval (DPR)

How do we actually define $p_\eta(z|x)$ over a corpus of 21 million Wikipedia passages? Sparse statistical methods like TF-IDF or BM25 struggle with lexical mismatch (e.g., "author" vs "writer").

We use **DPR**, a bi-encoder architecture. We instantiate two independent BERT networks: a Question Encoder $E_Q$ and a Document Encoder $E_D$. We map both strings into a shared $d$-dimensional continuous vector space:
$$ v_q = E_Q(x) \in \mathbb{R}^d, \quad v_z = E_D(z) \in \mathbb{R}^d $$

The relevance score between query $x$ and document $z$ is given by the inner product:
$$ \text{score}(x, z) = v_q^T v_z $$

We can then define the probability distribution $p_\eta(z|x)$ via a softmax over the entire corpus $\mathcal{Z}$:
$$ p_\eta(z|x) = \frac{\exp(v_q^T v_z)}{\sum_{z' \in \mathcal{Z}} \exp(v_q^T v_{z'})} $$

Since computing the denominator over 21 million documents at runtime is intractable, we pre-compute $v_z$ offline and use **Maximum Inner Product Search (MIPS)** algorithms (like FAISS HNSW) to approximate the top-$k$ documents in $O(\log |\mathcal{Z}|)$ time.

## 3. The RAG Pipeline Diagram

```mermaid
graph TD
    %% Query Encoding
    Q[Input Sequence: x] --> EQ[Encoder E_Q: R^d]
    EQ --> VQ[Query Vector: v_q]

    %% MIPS
    DB[(Offline Index E_D(Z))] --> MIPS{MIPS via FAISS}
    VQ --> MIPS

    %% Retrieval
    MIPS -->|argmax(v_q^T v_z)| Docs[Top-k Documents: z_1 ... z_k]

    %% Generation
    Q --> Concat((Concatenate String Contexts))
    Docs --> Concat
    
    Concat -->|x + z_k| Gen[Seq2Seq Generator: p_θ]
    Gen --> Y[Output Sequence: y]
```

## 4. Coding the MIPS Math in PyTorch

To truly grasp semantic search, let's write a bare-bones implementation of Maximum Inner Product Search natively in PyTorch using matrix multiplication.

```python
import torch
import torch.nn.functional as F

def get_top_k_documents(query_embedding, doc_embeddings, k=2):
    """
    query_embedding: Tensor of shape (1, d)
    doc_embeddings: Tensor of shape (N, d) representing N documents
    """
    # 1. Compute Inner Product (Dot Product)
    # R^(1 x d) @ R^(d x N) -> R^(1 x N)
    scores = torch.matmul(query_embedding, doc_embeddings.T) # Shape: (1, N)
    
    # 2. Get the top-k highest scoring indices
    # We use torch.topk to return the values and indices
    top_scores, top_indices = torch.topk(scores, k=k, dim=1)
    
    # 3. Compute Softmax probabilities over just the top-k (p_eta)
    probs = F.softmax(top_scores, dim=1)
    
    return top_indices.squeeze(), probs.squeeze()

# Define dimensions: N=1000 docs, d=768 embedding dim
N, d = 1000, 768

# Simulate our pre-computed offline document index
Z_index = F.normalize(torch.randn(N, d), p=2, dim=1) 

# Simulate a query embedding from E_Q
v_q = F.normalize(torch.randn(1, d), p=2, dim=1)

# Retrieve top 3 documents via MIPS
indices, probabilities = get_top_k_documents(v_q, Z_index, k=3)

print(f"Top 3 Document Indices in Database: {indices.tolist()}")
print(f"p_eta(z|x) probabilities: {probabilities.tolist()}")
```

In **Part 6**, our final post, we will look at how we can replace flat unstructured document retrieval with highly structured topological searches over **Knowledge Graphs**. See you then!
