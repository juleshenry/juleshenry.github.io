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


# The Mathematics of a Vanilla Recurrent Neural Network
1. Vanilla Forward Pass
![vanilla-forward-pass](/blog/assets/2024/rnn/vanilla-forward-pass.png)
2. Vanilla Backward Pass
![back-propagation](/blog/assets/2024/rnn/back-propagation.png)
3. Vanilla Bidirectional Pass
![bidirectional-rnn](/blog/assets/2024/rnn/bidirectional-rnn.png)
4. Training of Vanilla RNN

5. Vanishing and exploding gradient problem
> While training using BPTT the gradients have to travel from the last cell all the way to the first cell. The product of these gradients can go to zero or increase exponentially. The exploding gradients problem refers to the large increase in the norm of the gradient during training. The vanishing gradients problem refers to the opposite behavior, when long term components go exponentially fast to norm 0, making it impossible for the model to learn correlation between temporally distant events.

![unrolled-rnn](/blog/assets/2024/rnn/unrolled-rnn.png)
![computation-graph](/blog/assets/2024/rnn/computation-graph.png)

# Illustration : Character-Level Language Model
![example](/blog/assets/2024/rnn/example.png)
![example2](/blog/assets/2024/rnn/example2.png)
![example3](/blog/assets/2024/rnn/example3.png)



# LSTM
The LSTM architecture consists of a set of recurrentlyconnectedsubnets, known as memory blocks. These blocks canbe thoughtofas a differentiable version of the memory chips in a digital computer. Each block contains one or more self-connectedmemorycells and three multiplicative units that provide continuousanalogues of write, read and reset operations for the cells: namely, the input, output and forget gates.

### formulae
![lstm](/blog/assets/2024/rnn/lstm.png)
![lstm-cell](/blog/assets/2024/rnn/lstm-cell.svg)

Feed-Forward LSTM equations
![feed-forward-lstm](/blog/assets/2024/rnn/feed-forward-lstm.png)

Feed-Backward LSTM equations
![feed-backward-lstm](/blog/assets/2024/rnn/feed-backward-lstm.png)


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

