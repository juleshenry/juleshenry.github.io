---
layout: post
title: "BookSmarktks"
date: 2025-02-25
---

# What is education?

Is it the process by which woman learns the facts of this world, viz a viz a particular subdomain?

No, every caste defies global compatibility, few ye humans be police-doctor-plumber-scientist-poet-dancer.

Knowledge is so key to raising man's station; be it in markets, workforces, romantic relationships and war.

Twas' 2022 when my research led me to these papers:

2211.12781 (StrokeNet application of parsing Chinese characters via stroke romantization)
https://arxiv.org/pdf/2211.12781

```sh
"This work was supported in part by the National Natural Science Foundation of China (Grant No.62206076) and Shenzhen College Stability Support Plan (Grant No. GXWD20220811173340003 and GXWD20220817123150002)."
```
* I found it most curious to try to replicate the results of this paper, and I would love to do so in my free time.


KAN: Kolmogorov–Arnold Networks
https://arxiv.org/html/2404.19756v1

```sh
Figure 3.1: Compare KANs to MLPs on five toy examples. KANs can almost saturate the fastest scaling law predicted by our theory  (α = 4), while MLPs scales slowly and plateau quickly.
```
* I found it most curious to implement the KAN and try TOY examples 

1409.0473
https://arxiv.org/pdf/1409.0473

```sh
I'll explain the key formulas that support the attention mechanism introduced in the Bahdanau et al. paper. Here are the most important mathematical foundations:

The Encoder RNN:
The bidirectional RNN encoder produces annotations for each word in the source sentence. For each word xᵢ, it creates:
hᵢ = [h⃗ᵢ; h⃖ᵢ]
Where h⃗ᵢ is the forward hidden state and h⃖ᵢ is the backward hidden state.
The Attention Mechanism (core innovation):
The alignment model (attention) computes a score between the previous decoder hidden state sₜ₋₁ and each encoder annotation hᵢ:
eₜᵢ = a(sₜ₋₁, hᵢ)
This is typically computed as:
eₜᵢ = vₐᵀ tanh(Wₐsₜ₋₁ + Uₐhᵢ)
Where vₐ, Wₐ, and Uₐ are learned weight matrices.
The Context Vector:
The attention weights αₜᵢ are normalized using softmax:
αₜᵢ = exp(eₜᵢ) / ∑ⱼ exp(eₜⱼ)
Then the context vector cₜ is computed as a weighted sum:
cₜ = ∑ᵢ αₜᵢhᵢ
The Decoder Update:
The decoder hidden state is updated using:
sₜ = f(sₜ₋₁, yₜ₋₁, cₜ)
Where f is the RNN unit (GRU in the original paper), yₜ₋₁ is the previous output, and cₜ is the context vector.
Output Probability:
The probability of the next target word is:
p(yₜ|y₁, ..., yₜ₋₁, x) = g(yₜ₋₁, sₜ, cₜ)
Where g is a feedforward neural network with softmax output.

These formulas together define the attention-based neural machine translation model, which was revolutionary because it allowed the model to focus on different parts of the input sentence when generating each word of the translation, rather than compressing the entire input into a fixed-length vector.
```

2211.10877
https://arxiv.org/pdf/2211.10877

2004.05809
https://arxiv.org/pdf/2004.05809

Neural Machine Translation: A Review of Methods, Resources, and Tools
https://arxiv.org/pdf/2012.15515

arxiv.org/pdf/2103.03206
https://arxiv.org/pdf/2103.03206

1906.05909
https://arxiv.org/pdf/1906.05909

Utopia: Fast and Efficient Address Translation via Hybrid Restrictive & Flexible Virtual-to-Physical Address Mappings
https://arxiv.org/pdf/2211.12205


Learn RAG From Scratch – Python AI Tutorial from a LangChain Engineer - YouTube
https://www.youtube.com/watch?v=sVcwVQRHIc8&ab_channel=freeCodeCamp.org

What is RLHF? - Reinforcement Learning from Human Feedback Explained - AWS
https://aws.amazon.com/what-is/reinforcement-learning-from-human-feedback/










