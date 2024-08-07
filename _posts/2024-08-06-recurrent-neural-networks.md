---
layout: post
title: "Back-of-the-Envelope: Recurrent Neural Networks"
date: 2024-08-06
categories: machine-learning
---
# Purpose

Terse notes on RNN's.

<ol>
    <li>Applications</li>
    <li>RNN Model</li>
    <li>Illustration : Character-Level Language Model</li>
    <li>Long Short-Term Memory</li>
    <li>Python Code Vanilla Example</li>
    <li>Further Reading</li>
</ol>

# Applications
RNN's are especially adept at sequence data. They hold context in weights and can reference all elements of a sequence for ingestion and memory.


# Math in a Vanilla Recurrent Neural Network
1. Vanilla Forward Pass
![vanilla-forward-pass](/blog/assets/2024/vanilla-forward-pass.png)
2. Vanilla Backward Pass
![back-propagation](/blog/assets/2024/back-propagation.png)
3. Vanilla Bidirectional Pass
![bidirectional-rnn](/blog/assets/2024/bidirectional-rnn.png)
4. Training of Vanilla RNN
5. Vanishing and exploding gradient problem




![formulae](/blog/assets/2024/formulae.png)
![rnn-notation](/blog/assets/2024/rnn-notation.png)
![unrolled-rnn](/blog/assets/2024/unrolled-rnn.png)
![computation-graph](/blog/assets/2024/computation-graph.png)

# Illustration : Character-Level Language Model
![example](/blog/assets/2024/example.png)
![example2](/blog/assets/2024/example2.png)
![example3](/blog/assets/2024/example3.png)



# LSTM
The LSTM architecture consists of a set of recurrentlyconnectedsubnets, known as memory blocks. These blocks canbe thoughtofas a differentiable version of the memory chips in a digital
computer. Each block contains one or more self-connectedmemorycells and three multiplicative units that provide continuousanalogues of write, read and reset operations for the cells: namely, the input, output and forget gates.

### formulae
![lstm](/blog/assets/2024/lstm.png)
![lstm-cell](/blog/assets/2024/lstm-cell.svg)

Feed-Forward LSTM equations
![feed-forward-lstm](/blog/assets/2024/feed-forward-lstm.png)

Feed-Backward LSTM equations
![feed-backward-lstm](/blog/assets/2024/feed-backward-lstm.png)


# Python Code Vanilla Example (Karpathy)
Note, lines 48-58 are where backpropagation occurs and where the vanishing/exponential gradient issue arises in plain RNN.

### Gist
https://gist.github.com/karpathy/d4dee566867f8291f086
### Commentary Blog
https://towardsdatascience.com/recurrent-neural-networks-rnns-3f06d7653a85

## Further Reading

* [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper_files/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)

* [VISUALIZING AND UNDERSTANDING RECURRENT NETWORKS](https://arxiv.org/pdf/1506.02078)

* [Visual7W Grounded Question Answering in Images](https://arxiv.org/pdf/1511.03416)


