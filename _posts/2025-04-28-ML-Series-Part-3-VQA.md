---
layout: post
title:  "ML Smörgåsbord 3: Spatial Attention"
date:   2025-03-28 10:00:00 -0000
categories: blog
mathjax: true
---

# Grounding Language in Vision 📸✍️

Welcome back to Part 3! In Part 1, we defined the convolutional operations that extract spatial feature maps $V \in \mathbb{R}^{C \times H \times W}$ from images. In Part 2, we formalized the LSTM sequence modeling that compresses a variable-length text sequence into a fixed-length dense vector $h_Q \in \mathbb{R}^{d_q}$. 

Today, we unite these two spaces. How can a network conditionally route visual information based on a textual query? The answer lies in the mathematics of **Spatial Attention**. 

## 1. The Formulation of Visual7W

In Zhu et al. (2016), the objective of Visual Question Answering (VQA) is framed as a mapping function:
$$ f: (I, Q) \rightarrow A $$
Where $I$ is an image, $Q$ is a sequence of word embeddings $[q_1, \dots, q_T]$, and $A$ is the answer (either a discrete class or a localized bounding box).

If we simply concatenate the flattened global image features $v_{global}$ with the final question hidden state $h_Q$, the network struggles to isolate small spatial details relevant to specific questions (e.g., "What color is the *tie*?").

Instead, we treat the final convolutional feature map $V \in \mathbb{R}^{C \times H \times W}$ as a set of $N = H \times W$ distinct spatial vectors:
$$ V = \{v_1, v_2, \dots, v_N\} \text{ where } v_i \in \mathbb{R}^C $$

## 2. Deriving the Attention Mechanism

We want to compute a scalar weight $\alpha_i \in [0, 1]$ for every spatial region $v_i$, conditioned on the question vector $h_Q$. We require that $\sum_{i=1}^N \alpha_i = 1$.

We do this via a Multi-Layer Perceptron (MLP) alignment model. First, we project both the visual vector $v_i$ and the question vector $h_Q$ into a shared joint-embedding space of dimension $k$:

$$ z_i = \tanh(W_v v_i + W_q h_Q + b_z) $$
Where $W_v \in \mathbb{R}^{k \times C}$ and $W_q \in \mathbb{R}^{k \times d_q}$.

Next, we project this joint representation to a scalar logit using a weight vector $w_a \in \mathbb{R}^k$:
$$ e_i = w_a^T z_i + b_a $$

Finally, we apply the softmax function over the $N$ regions to yield a normalized probability distribution (the attention map):
$$ \alpha_i = \frac{\exp(e_i)}{\sum_{j=1}^N \exp(e_j)} $$

The resulting **context vector** $\hat{v}$ is the $\alpha$-weighted sum of the original spatial features:
$$ \hat{v} = \sum_{i=1}^N \alpha_i v_i $$
This vector $\hat{v} \in \mathbb{R}^C$ now represents the *exact visual information required to answer the question*, filtering out irrelevant background noise.

## 3. Visualizing the Tensor Operations

Let's look at the flow of tensor dimensions during the attention calculation. Assume a batch size of $B$.

```mermaid
graph TD
    %% Tensors
    V[Visual Map: B x N x C] -->|Linear(C -> K)| V_proj[Projected V: B x N x K]
    Q[Question Vector: B x d_q] -->|Linear(d_q -> K)| Q_proj[Projected Q: B x K]
    
    %% Broadcasting
    Q_proj -->|Unsqueeze & Expand| Q_exp[Expanded Q: B x N x K]
    
    %% Addition and Tanh
    V_proj --> Add_Op(Element-wise +)
    Q_exp --> Add_Op
    Add_Op --> Tanh_Op(Tanh)
    
    %% Scoring
    Tanh_Op -->|Linear(K -> 1)| Z[Logits e_i: B x N x 1]
    Z -->|Squeeze| Z_sq[Logits: B x N]
    
    %% Softmax
    Z_sq -->|Softmax(dim=1)| Alpha[Attention Weights α: B x N]
    
    %% Weighted Sum (Batch Matrix Multiplication)
    Alpha -->|Unsqueeze| Alpha_uns[α: B x 1 x N]
    V --> BMM(Batch Matrix Multiply: BMM)
    Alpha_uns --> BMM
    BMM --> V_hat[Context Vector v_hat: B x 1 x C]
```

## 4. PyTorch Implementation of the MLP Attention Layer

Notice in the graph above, the most efficient way to compute $\sum \alpha_i v_i$ for a batch of images is using Batch Matrix Multiplication (`torch.bmm`). 

Let's implement this layer mathematically identically to the equations above.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SpatialAttention(nn.Module):
    def __init__(self, c_dim=512, q_dim=256, k_dim=128):
        super(SpatialAttention, self).__init__()
        # W_v projection: R^C -> R^k
        self.W_v = nn.Linear(c_dim, k_dim, bias=False)
        # W_q projection: R^d_q -> R^k
        self.W_q = nn.Linear(q_dim, k_dim, bias=True) # Bias b_z goes here
        # w_a scoring vector: R^k -> R^1
        self.w_a = nn.Linear(k_dim, 1, bias=True)     # Bias b_a goes here

    def forward(self, V, h_Q):
        """
        V: (Batch, N, C) - The flattened spatial feature map
        h_Q: (Batch, d_q) - The question hidden state
        """
        B, N, C = V.size()
        
        # 1. Project Visual Features
        v_proj = self.W_v(V) # Shape: (B, N, k_dim)
        
        # 2. Project Question Vector and broadcast to match N spatial regions
        q_proj = self.W_q(h_Q) # Shape: (B, k_dim)
        q_exp = q_proj.unsqueeze(1).expand(-1, N, -1) # Shape: (B, N, k_dim)
        
        # 3. Compute joint embedding with Tanh
        z = torch.tanh(v_proj + q_exp) # Shape: (B, N, k_dim)
        
        # 4. Compute unnormalized logits e_i
        e = self.w_a(z).squeeze(2) # Shape: (B, N)
        
        # 5. Softmax to get attention weights \alpha
        alpha = F.softmax(e, dim=1) # Shape: (B, N)
        
        # 6. Compute context vector \hat{v} via Batch Matrix Multiplication
        # alpha.unsqueeze(1) is (B, 1, N)
        # V is (B, N, C)
        # BMM( (B, 1, N), (B, N, C) ) -> (B, 1, C)
        v_hat = torch.bmm(alpha.unsqueeze(1), V).squeeze(1) # Shape: (B, C)
        
        return v_hat, alpha

# Let's verify the dimensions
B, N, C, d_q = 32, 49, 512, 256
V_tensor = torch.randn(B, N, C)
h_Q_tensor = torch.randn(B, d_q)

attention_module = SpatialAttention(c_dim=C, q_dim=d_q, k_dim=128)
context_vector, attention_map = attention_module(V_tensor, h_Q_tensor)

print(f"Context Vector shape: {context_vector.shape}") # torch.Size([32, 512])
print(f"Attention Map shape: {attention_map.shape}")   # torch.Size([32, 49])
```

In **Part 4**, we will discard the sequential nature of LSTMs entirely. We will dive into the purely parallel matrix operations of the **Transformer Architecture** and derive the mathematical powerhouse known as *Scaled Dot-Product Self-Attention*, the core engine of BERT!
