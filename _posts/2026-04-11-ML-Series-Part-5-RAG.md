---
layout: post
title:  "The ML Smorgasbord Part 5: Giving AI an Open-Book Test (RAG)"
date:   2026-04-11 10:00:00 -0000
categories: blog
mathjax: true
---

# Stopping the AI from Hallucinating 🛑🤖

Welcome to Part 5! By now, we all know that large language models (like ChatGPT) are incredibly smart. They've read the whole internet (thanks to architectures like BERT from Part 4). 

But they have a huge flaw: **they confidently make things up**. In the AI world, we call this "hallucinating." It happens because the AI's memory is fixed. If you ask it about a news event that happened yesterday, it doesn't know about it, so it just guesses.

How do we fix this? We use **RAG: Retrieval-Augmented Generation**. 

## What is RAG?

Imagine taking a final exam. 
* A standard LLM is taking a **closed-book test**. It has to rely purely on what it memorized while studying.
* RAG gives the LLM an **open-book test**. 

Before the AI answers your question, it is allowed to "Google" the answer in a trusted database (like Wikipedia or your company's private documents), read the results, and *then* answer you.

## How it works (The 2 Steps)

1. **The Retriever (The Librarian):** You ask a question. The Retriever takes your question and searches a massive library of documents to find the top 3 most relevant paragraphs.
2. **The Generator (The Writer):** The AI takes your question, *glues the 3 paragraphs to it*, and writes a perfect, factual answer based *only* on those paragraphs.

```mermaid
graph LR
    User[You: "Who won the game last night?"] --> Retriever[The Librarian]
    
    DB[(ESPN Articles)] --> Retriever
    
    Retriever -->|Finds article about the game| Context[Relevant Paragraph]
    
    Context --> Generator[The Writer: LLM]
    User --> Generator
    
    Generator --> Answer["Based on the article, the Lakers won."]
```

## A Simple Python Example

We use a special kind of math called "Embeddings" to turn text into lists of numbers, which makes searching incredibly fast.

```python
# Think of sentence_transformers as our Librarian
from sentence_transformers import SentenceTransformer
import numpy as np

# Download a tiny model to turn text into numbers
librarian = SentenceTransformer('all-MiniLM-L6-v2')

# Here is our "database" (a list of facts)
database = [
    "The dining hall serves pizza on Tuesdays.",
    "The library closes at midnight.",
    "Professor Smith's office hours are on Wednesdays."
]

# 1. The librarian reads the database and turns every sentence into a list of numbers
doc_numbers = librarian.encode(database)

# 2. You ask a question
question = "When can I get help from my professor?"
question_numbers = librarian.encode([question])

# 3. We compare the question numbers to the database numbers to find the closest match!
# (We are just finding the smallest mathematical distance between them)
distances = np.linalg.norm(doc_numbers - question_numbers, axis=1)

# The index of the smallest distance is our winning fact!
best_match_index = np.argmin(distances)
winning_fact = database[best_match_index]

print(f"Question: {question}")
print(f"Librarian found: {winning_fact}")

# Next, we would send the Question + the Winning Fact to ChatGPT to write a polite response!
```

RAG is how every major company uses AI today. They don't train custom models from scratch; they just use RAG to let a smart model read their private documents securely!

In **Part 6**, our grand finale, we'll look at the ultimate way to store facts: Knowledge Graphs! See you then!
