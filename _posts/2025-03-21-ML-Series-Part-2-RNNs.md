---
layout: post
title:  "The ML Smörgåsbord Part 2: The Math of Recurrent Memory and LSTMs"
date:   2025-03-21 10:00:00 -0000
categories: blog
mathjax: true
---

# Stepping into the Time Dimension ⏳

Welcome back to Part 2! Last week we covered the spatial convolutions of AlexNet. Today, we shift from $x,y$ coordinates to the time axis $t$. We are going to explore how Recurrent Neural Networks (RNNs) and their upgraded cousins, Long Short-Term Memory networks (LSTMs), maintain continuous differentiable memory.

## 1. The Vanilla RNN Forward Pass

Let's rigorously define a vanilla RNN. At any timestep $t$, the network receives an input vector $x_t \in \mathbb{R}^d$ and the previous hidden state vector $h_{t-1} \in \mathbb{R}^h$. 

It computes the new hidden state via an affine transformation followed by a hyperbolic tangent non-linearity:

$$ h_t = \tanh(W_{hx} x_t + W_{hh} h_{t-1} + b_h) $$

Where:
* $W_{hx} \in \mathbb{R}^{h \times d}$ is the input-to-hidden weight matrix.
* $W_{hh} \in \mathbb{R}^{h \times h}$ is the hidden-to-hidden transition matrix.
* $b_h \in \mathbb{R}^h$ is the hidden bias vector.

To predict an output $\hat{y}_t \in \mathbb{R}^v$ (e.g., a probability distribution over a vocabulary of size $v$), we apply another affine projection and a softmax:

$$ \hat{y}_t = \text{softmax}(W_{yh} h_t + b_y) $$

### The Fundamental Flaw: Backpropagation Through Time (BPTT)

To train this, we must unroll the network through time and compute gradients. The gradient of the loss $\mathcal{L}_T$ at the final timestep with respect to the hidden state at timestep $k$ ($k < T$) involves the product of Jacobians:

$$ \frac{\partial \mathcal{L}_T}{\partial h_k} = \frac{\partial \mathcal{L}_T}{\partial h_T} \prod_{j=k+1}^T \frac{\partial h_j}{\partial h_{j-1}} $$

Since $h_j = \tanh(W_{hh} h_{j-1} + \dots)$, the Jacobian $\frac{\partial h_j}{\partial h_{j-1}} = \text{diag}(\tanh'(\dots)) W_{hh}$. 

If the largest singular value of $W_{hh}$ is less than 1, this product decays exponentially (Vanishing Gradients). If it's greater than 1, it grows exponentially (Exploding Gradients). Vanilla RNNs are fundamentally unstable for long sequences.

## 2. Enter the LSTM: An Additive Gradient Highway

In 1997, Hochreiter & Schmidhuber solved this with the LSTM. Instead of just a hidden state $h_t$, they introduced a **Cell State** $c_t$. 

The brilliant innovation of the Cell State is that information is updated *additively* rather than through matrix multiplication, acting as a "highway" where gradients can flow backward through time uninterrupted.

Here are the precise gated equations that govern an LSTM cell:

1. **Forget Gate:** Decides what to drop from the old cell state.
   $$ f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) $$
2. **Input Gate:** Decides what new information to add.
   $$ i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) $$
3. **Candidate Cell State:** Generates potential new values.
   $$ \tilde{c}_t = \tanh(W_c \cdot [h_{t-1}, x_t] + b_c) $$
4. **Cell State Update:** (The Additive Highway!)
   $$ c_t = f_t \odot c_{t-1} + i_t \odot \tilde{c}_t $$
5. **Output Gate & Hidden State:** Decides what part of the cell state becomes the hidden state.
   $$ o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) $$
   $$ h_t = o_t \odot \tanh(c_t) $$

*(Note: $\sigma$ is the sigmoid function, mapping values to $(0, 1)$ to act as a gate/valve. $\odot$ denotes element-wise Hadamard multiplication. $[h_{t-1}, x_t]$ denotes vector concatenation).*

## 3. Visualizing the LSTM Cell Architecture

Here is a detailed schematic of the internal flow of tensors inside a single LSTM cell at timestep $t$.

```mermaid
graph TD
    %% Inputs
    X_t[Input: x_t] --> Concat
    H_prev[Previous Hidden: h_{t-1}] --> Concat
    C_prev[Previous Cell State: c_{t-1}] --> Add_Op

    %% Concatenation
    Concat((Concatenate)) --> W_f[Linear + Sigmoid]
    Concat --> W_i[Linear + Sigmoid]
    Concat --> W_c[Linear + Tanh]
    Concat --> W_o[Linear + Sigmoid]

    %% Forget Gate logic
    W_f -->|Forget Vector: f_t| Mult_Forget(Element-wise X)
    C_prev --> Mult_Forget

    %% Input Gate logic
    W_i -->|Input Vector: i_t| Mult_Input(Element-wise X)
    W_c -->|Candidate Vector: c~_t| Mult_Input

    %% State Update
    Mult_Forget --> Add_Op(Element-wise +)
    Mult_Input --> Add_Op

    %% New Outputs
    Add_Op --> C_next[New Cell State: c_t]
    Add_Op --> Tanh_Op(Tanh)
    W_o -->|Output Gate: o_t| Mult_Output(Element-wise X)
    Tanh_Op --> Mult_Output
    Mult_Output --> H_next[New Hidden State: h_t]
```

## 4. Coding the LSTM Equations from Scratch

To truly understand it, let's implement the forward pass of a single LSTM cell strictly using PyTorch tensor operations, mirroring the equations above exactly.

```python
import torch
import torch.nn as nn

class RawLSTMCell(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # We concatenate h and x, so the weight matrix dimension is hidden_size + input_size
        concat_size = hidden_size + input_size
        
        # The 4 linear layers for our 4 gates: Forget, Input, Candidate, Output
        self.W_f = nn.Linear(concat_size, hidden_size)
        self.W_i = nn.Linear(concat_size, hidden_size)
        self.W_c = nn.Linear(concat_size, hidden_size)
        self.W_o = nn.Linear(concat_size, hidden_size)

    def forward(self, x_t, h_prev, c_prev):
        """
        x_t: Tensor of shape (batch_size, input_size)
        h_prev, c_prev: Tensors of shape (batch_size, hidden_size)
        """
        # 1. Concatenate h_{t-1} and x_t along the feature dimension
        combined = torch.cat((h_prev, x_t), dim=1)
        
        # 2. Compute the gates
        f_t = torch.sigmoid(self.W_f(combined))     # Forget gate: (0 to 1)
        i_t = torch.sigmoid(self.W_i(combined))     # Input gate: (0 to 1)
        c_tilde = torch.tanh(self.W_c(combined))    # Candidate cell: (-1 to 1)
        o_t = torch.sigmoid(self.W_o(combined))     # Output gate: (0 to 1)
        
        # 3. Update the Cell State (The Additive Highway)
        # Element-wise multiplication is done using '*' in PyTorch
        c_t = f_t * c_prev + i_t * c_tilde
        
        # 4. Compute the new Hidden State
        h_t = o_t * torch.tanh(c_t)
        
        return h_t, c_t

# Let's test the math!
batch_size, input_dim, hidden_dim = 1, 10, 20
lstm_cell = RawLSTMCell(input_size=input_dim, hidden_size=hidden_dim)

# Dummy inputs
x_t = torch.randn(batch_size, input_dim)
h_0 = torch.zeros(batch_size, hidden_dim)
c_0 = torch.zeros(batch_size, hidden_dim)

# Run one timestep
h_1, c_1 = lstm_cell(x_t, h_0, c_0)
print(f"New Hidden State shape: {h_1.shape}") # torch.Size([1, 20])
print(f"New Cell State shape: {c_1.shape}")   # torch.Size([1, 20])
```

In **Part 3**, we will merge Part 1 (CNNs) and Part 2 (LSTMs). We will introduce the mathematical formulation of *Spatial Attention*, allowing an LSTM to compute dynamic weight vectors over the spatial grid of a CNN feature map. See you then!
