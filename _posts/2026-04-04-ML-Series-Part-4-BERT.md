---
layout: post
title:  "The ML Smorgasbord Part 4: BERT and the Transformer Revolution"
date:   2026-04-04 10:00:00 -0000
categories: blog
mathjax: true
---

# Reading Everything Everywhere All At Once 📖

Welcome to Part 4! So far, we've talked about RNNs reading text left-to-right, one word at a time. But honestly? That's really slow. And if a sentence is really long, by the time the RNN gets to the end, it forgets what happened at the beginning.

In 2017, Google invented the **Transformer**, a completely new way to read text. Two years later, a model called **BERT** proved that Transformers were the undisputed kings of language.

## What makes BERT so special?

BERT stands for *Bidirectional Encoder Representations from Transformers*. 

Before BERT, AIs read like you and I do: word by word. BERT doesn't do that. BERT looks at the **entire paragraph at once**. It can look to the left of a word, and to the right of a word, simultaneously.

## How do you train a model that reads everything at once?

You give it a fill-in-the-blank test! This is called **Masked Language Modeling**.

Google took massive amounts of text from the internet and randomly replaced 15% of the words with the word `[MASK]`. 

> "The quick brown `[MASK]` jumps over the lazy dog."

BERT's job was to guess what word was under the mask. To guess "fox", it has to look at the words before the mask ("quick brown") AND the words after the mask ("jumps"). Because it was trained on billions of sentences this way, it developed an incredibly deep understanding of the English language.

```mermaid
graph TD
    Input[Input Tokens: `The [MASK] is barking`] --> Transformer
    Transformer -->|Reads everything at once| Output_Masked[Masked Token Representation]
    
    Output_Masked -->|Fill in the blank!| Guess(Guess: 'dog')
```

## The Secret Sauce: Attention

Instead of a "scratchpad" memory like an RNN, BERT uses **Self-Attention**. Every word in the sentence asks every other word in the sentence, "How relevant are you to me?" 

When BERT reads the word "barking", it pays a *ton* of attention to the word "dog". It's like drawing lines connecting related words in a sentence!

## Let's use BERT in 3 lines of code!

Thanks to an amazing library called Hugging Face, you can use BERT to fill in the blanks on your own laptop right now.

```python
# First, install the library: pip install transformers
from transformers import pipeline

# We download BERT and tell it we want to do the fill-in-the-blank task
unmasker = pipeline('fill-mask', model='bert-base-uncased')

# Let's give it a test!
text = "The college freshman was tired, so they drank a lot of [MASK]."

# Ask BERT to guess
guesses = unmasker(text)

# Print out what BERT thinks
print("BERT's top guesses:")
for guess in guesses:
    print(f"- {guess['token_str']} (Confidence: {guess['score']*100:.1f}%)")

# Output:
# - coffee (Confidence: 85.2%)
# - water (Confidence: 5.1%)
# - beer (Confidence: 2.3%)
```

BERT totally understands the life of a college freshman. 

In **Part 5**, we're going to talk about a huge problem with modern AIs like ChatGPT: they lie. How do we stop them from making things up? We give them an open-book test! See you next week for RAG!
