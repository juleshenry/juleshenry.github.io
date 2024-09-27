---
layout: post
title: "Back of the Envelope: Grover's Search"
date: 2024-09-13
---

# Content
Herein we explain one of the most fascinating results in computer science, Grover's Search.

# Primer
You will need to know linear algebra and Big O notation to understand the signficance of this work.

# Intuition: the Lost Key-Ring Quandary


# Grover's Search

"An unsorted database contains N records, and the task is to identify the one record that satisfies a specific property. Classical algorithms, whether deterministic or probabilistic, would require O(N) steps on average to examine a significant portion of the records. However, quantum mechanical systems can perform multiple operations simultaneously due to their wave-like properties." -Lov K. Grover, 1996

Grover's Search is a quantum mechanical algorithm that can identify the record in O(√N) steps, and in the same paper proved it is within a constant factor of the fastest possible quantum mechanical algorithm.


## The Oracle


## The Procedure
1. Apply the Oracle
2. Apply the Hadamard transform
3. Perform a conditional phase shift on the computer, with every computational basis state except |0> receiving a phase shift of -1
4. Apply the Hadamard transform


### Sources

L. K. Grover. A fast quantum mechanical algorithm for database search. Nov. 19, 1996. arXiv: quant- ph/9605043.

M. A. Nielsen and I. L. Chuang. Quantum computation and quantum information. 10th anniversary ed. Cam- bridge ; New York: Cambridge University Press, 2010. 676 pp. ISBN: 978-1-107-00217-3.


