---
layout: post
title: "Back-of-the-Envelope: Retrieval Augmented Generation (RAG)"
date: 2024-08-24
---

# What is RAG?

Retrieval augmented generation forces LLM's to cite their sources.

# How it's achieved

From a high level, a RAG architecture concatenates relevant documents to a query and gives back the most likely sequnce given a query modulo the documents.
![architecture](/blog/assets/2024/rag/rag-arch.png)

Firstly, we have the encoding. While the paper discusses both RAG-Sequence and RAG-Token, the former is simpler to understand.
![rag-sequence](/blog/assets/2024/rag/rag-sequence.png)

Next, we have the seq-2-seq model generator ingest.
![generator](/blog/assets/2024/rag/generator.png)

In addition, there is a decoding process.
![decode](/blog/assets/2024/rag/decode.png)

Finally, a retriever produces the relevant sequence.
![retriever-dpr](/blog/assets/2024/rag/retriever-dpr.png)


## Further Reading

* [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/pdf/2005.11401)

