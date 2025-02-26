---
layout: post
title: "Book Smarts, Remarks"
date: 2025-02-25
---

# What is a So-Called, Good-For-Nothing EDUCATION?

Is it the process by which woman learns the facts of this world, viz a viz a particular subdomain?

No, every caste defies global compatibility, few ye humans be police-doctor-plumber-scientist-poet-dancer.

Knowledge is so key to raising man's station; be it in markets, workforces, romantic relationships and war.

Twas' late 2022 when my research led me to these papers:

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

```math
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

## The Context Vector:
The attention weights αₜᵢ are normalized using softmax:

αₜᵢ = exp(eₜᵢ) / ∑ⱼ exp(eₜⱼ)

Then the context vector cₜ is computed as a weighted sum:

cₜ = ∑ᵢ αₜᵢhᵢ

## The Decoder Update:
The decoder hidden state is updated using:

sₜ = f(sₜ₋₁, yₜ₋₁, cₜ)

Where f is the RNN unit (GRU in the original paper), yₜ₋₁ is the previous output, and cₜ is the context vector.

## Output Probability:
The probability of the next target word is:

p(yₜ|y₁, ..., yₜ₋₁, x) = g(yₜ₋₁, sₜ, cₜ)

Where g is a feedforward neural network with softmax output.

These formulas together define the attention-based neural machine translation model, which was revolutionary because it allowed the model to focus on different parts of the input sentence when generating each word of the translation, rather than compressing the entire input into a fixed-length vector.
```

2211.10877 AI Interrogation
https://arxiv.org/pdf/2211.10877
```math 
Overall traditional multi-class text classification using the
latest transformer-based BERT model has shown the best performance in our experiments compared to the other approaches
for attributing fine-tuned models with their corresponding base
models. In our experiments, we performed ten-fold crossvalidation on the assembled training data set that did not
contain any miscellaneous records or responses generated from
additional third-party models provided by authorities other
than MLMAC [2]. We strongly think that the absence of such
miscellaneous records that don’t belong to any of the models
provided in the contest is the main reason behind the better
performance of traditional multi-class text classification over
the one-vs-all strategy using binary text classifiers. The vector
space models have shown a comparable performance and a
notable improvement over the translation evaluation metrics
```
* Sounded like a dead end tbh.

2004.05809 : Neural Machine Translation: Challenges, Progress and Future (2020)
https://arxiv.org/pdf/2004.05809
```sh
According to the comprehensive investigations conducted by [73], human translations are much preferred over
MT outputs if using better rating techniques, such as choosing professional translators as raters, evaluating documents
rather than individual sentences and utilizing original source
texts instead of source texts translated from target language.
Current NMT systems still suffer from serious translation errors of mistranslated words or named entities, omissions and
wrong word order. Obviously, there is much room for NMT
to improve and we suggest some potential research directions
in the next section.
```

* You should have hope, still, ye polyglots akimbo for there remains still hope for improvement.

2012.15515: Neural Machine Translation: A Review of Methods, Resources, and Tools (2020)
https://arxiv.org/pdf/2012.15515


```math
Despite the great success achieved by NMT, there are still
many problems to be explored. We list some important and
challenging problems for NMT as follows:

• Understanding NMT. Although there are many attempts
to analyze and interpret NMT, our understandings about
NMT are still limited. Understanding how and why NMT
produces its translation result is important to figure out the
bottleneck and weakness of NMT models.


• Designing better architectures. Designing a new architecture that better than Transformer is beneficial for both
NMT research and production. Furthermore, designing a
new architecture that balances translation performance and
computational complexity is also important.


• Making full use of monolingual data. Monolingual data
are valuable resources. Despite the remarkable progress,
we believe that there is still much room for NMT to make
use of abundant monolingual data.


• Integrating prior knowledge. Incorporating human
knowledge into NMT is also an important problem. Although there is some progress, the results are far from satisfactory. How to convert discrete and continuous representations into each other is a problem of NMT that needs further exploration
```
* This was a more a literature review and post-portem on Attention via Google. Really nice summary.

arxiv.org/pdf/2103.03206  `Perceiver: General Perception with Iterative Attention`
https://arxiv.org/pdf/2103.03206
```math
With great flexibility comes great overfitting, and many of
our design decisions were made to mitigate this. In future
work, we would like to pre-train our image classification
model on very large scale data (Dosovitskiy et al., 2021). 

We obtain strong results on the large AudioSet dataset, which
has 1.7M examples and where the Perceiver performed competitively with strong and recent state-of-the-art entries on audio, video and both combined. On ImageNet the model
performs on par with ResNet-50 and ViT. When comparing
these models across all different modalities and combinations considered in the paper, the Perceiver does best overall.
```
* This proposes a scalable solution to input handling in transformer architectures, so really cool for audio-visual applications. Could I take this and make a video-based, model to predict activity for security cameras?

1906.05909 : Stand-Alone Self-Attention in Vision Models
https://arxiv.org/pdf/1906.05909
```math
While this work primarily focuses on content-based interactions to establish their virtue for vision
tasks, in the future, we hope to unify convolution and self-attention to best combine their unique
advantages. Given the success of content-based interactions on core computer vision tasks, we expect
that future work may explore how attention could be applied to other vision tasks such as semantic
segmentation [63], instance segmentation [64], keypoint detection [65], human pose estimation
[66, 67] and other tasks currently addressed with convolutional neural networks.
```
* this wasn't so stimulating now, probably an paper inspired by Attention  '17

Utopia: Fast and Efficient Address Translation via Hybrid Restrictive & Flexible Virtual-to-Physical Address Mappings
https://arxiv.org/pdf/2211.12205
```math
• We quantitatively evaluate Utopia in single-core and multicore environments and compare it against three state-ofthe-art address translation mechanisms. Our experimental
results show that Utopia significantly reduces the overheads
associated with address translation at a modest low area and
power cost. We open-source Utopia at https://github.com/
CMU-SAFARI/Utopia.
```
* highly technical paper on virtual memory. I think I liked the name "Utopia" as I was living in hell working in a factory...

Learn RAG From Scratch – Python AI Tutorial from a LangChain Engineer - YouTube
* https://www.youtube.com/watch?v=sVcwVQRHIc8&ab_channel=freeCodeCamp.org
### todo: actually watch and take notes on this. will link in another post


What is RLHF? - Reinforcement Learning from Human Feedback Explained - AWS
* https://aws.amazon.com/what-is/reinforcement-learning-from-human-feedback/
```math
Building a separate reward model
The core of RLHF is training a separate AI reward model based on human feedback, and then using this model as a reward function to optimize policy through RL. Given a set of multiple responses from the model answering the same prompt, humans can indicate their preference regarding the quality of each response. You use these response-rating preferences to build the reward model that automatically estimates how high a human would score any given prompt response. 

Optimize the language model with the reward-based model
The language model then uses the reward model to automatically refine its policy before responding to prompts. Using the reward model, the language model internally evaluates a series of responses and then chooses the response that is most likely to result in the greatest reward. This means that it meets human preferences in a more optimized manner.

The following image shows an overview of the RLHF learning process.
```
* So, you get a high level definition of RLHF but no technical details... lmao!


### PSA: DeepSeek R2 seems to be the vector that burst the AI-Pre-Singularity Bubble. Oh, well.
### Tesla drops below $1 Trillion with the EV maker's sales falling 42% in Europe and Musk quagmired in  MAGA Mar-A-Lago
### That's why I blog, afterall, a `SYA` masquerading as a `CYA`.