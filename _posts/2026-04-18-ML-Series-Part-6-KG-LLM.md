---
layout: post
title:  "The ML Smorgasbord Part 6: Giving AI a Mind Map (Knowledge Graphs)"
date:   2026-04-18 10:00:00 -0000
categories: blog
mathjax: true
---

# Mind Maps for Computers 🗺️

Welcome to the grand finale of the ML Smorgasbord! 

In Part 5, we learned how RAG lets an AI search a library of documents to find facts. But what if our facts aren't in paragraphs? What if we have a massive web of data, like knowing who is friends with who on Facebook, or how every chemical in the human body interacts? 

Paragraphs are terrible for that. We need a **Knowledge Graph**. 

## What is a Knowledge Graph (KG)?

Think of a Knowledge Graph as a giant mind map. It’s made of two things:
1. **Nodes (Circles):** People, places, or things. 
2. **Edges (Arrows):** The relationship between those things.

Instead of writing "Albert Einstein was born in Germany," a KG just stores: 
`[Albert Einstein] --(Born_In)--> [Germany]`

A recent paper called "Unifying Large Language Models and Knowledge Graphs" explores how mixing these giant mind maps with smart AIs like ChatGPT creates a super-system. 

## The Dream Team: LLMs + KGs

LLMs are creative, fluent, and good at chatting. But they are bad at logic and hard facts.
KGs are perfectly logical and 100% factual. But they are rigid and can't talk to you.

When you put them together:
* **The AI reads the Mind Map:** You ask a complex question. The AI traverses the Knowledge Graph, gathers the exact logical facts, and translates them into a friendly sentence. 
* **The AI builds the Mind Map:** You feed the AI a 500-page biology textbook. The AI reads it, extracts all the relationships, and automatically draws the Knowledge Graph for you!

```mermaid
graph TD
    Text[Messy Textbook] --> LLM_Reader[AI reads the book]
    LLM_Reader -->|Extracts Facts| KG[(Knowledge Graph)]
    
    KG -->|Provides pure logic| LLM_Talker[AI answers your question]
    User[You: "What causes this disease?"] --> LLM_Talker
    LLM_Talker --> Answer[Perfectly accurate answer]
```

## Let's Build a Tiny Knowledge Graph in Python

We can use a cool library called `networkx` to literally draw a mini mind-map in Python, and see how we'd feed it to an AI.

```python
import networkx as nx

# 1. Create a blank mind map (a Directed Graph means the arrows point in one direction)
mind_map = nx.DiGraph()

# 2. Add our facts! (Subject, Object, and the Relationship)
mind_map.add_edge("Freshman", "Dorm", relation="lives_in")
mind_map.add_edge("Dorm", "Campus", relation="located_on")
mind_map.add_edge("Freshman", "Pizza", relation="eats_too_much")

# 3. Let's ask the mind map about the "Freshman"
person = "Freshman"
facts_we_found = []

# Follow all the arrows pointing away from "Freshman"
for connected_thing in mind_map.successors(person):
    # Find out what the arrow says
    relationship = mind_map.edges[person, connected_thing]['relation']
    
    # Translate it into English
    clean_relation = relationship.replace('_', ' ')
    facts_we_found.append(f"{person} {clean_relation} {connected_thing}.")

# 4. Give these facts to the AI
context = " ".join(facts_we_found)
question = "Where does the student live and what is their diet?"

prompt = f"""
Hey ChatGPT, please answer the question using ONLY these facts:
Facts: {context}

Question: {question}
"""

print(prompt)

# Output:
# Hey ChatGPT, please answer the question using ONLY these facts:
# Facts: Freshman lives in Dorm. Freshman eats too much Pizza.
#
# Question: Where does the student live and what is their diet?
```

## That's a wrap! 🎓

You've made it to the end! In this series, we've gone from the dawn of modern computer vision (AlexNet) to the cutting edge of AI fact-checking (RAG and Knowledge Graphs). 

Machine Learning isn't magic—it's just really clever math, a lot of data, and the simple desire to teach computers how to understand our messy, beautiful world. 

Thanks for reading, and keep exploring!
