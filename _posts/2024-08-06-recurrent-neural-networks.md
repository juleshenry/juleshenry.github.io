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
    <li>Seminal Papers</li>
    <li>Python Code Vanilla Example</li>
</ol>

# Applications
RNN's are especially adept at sequence data.


# Math in a Vanilla Recurrent Neural Network
1. Vanilla Forward Pass
2. Vanilla Backward Pass
3. Vanilla Bidirectional Pass
4. Training of Vanilla RNN
5. Vanishing and exploding gradient problem

![back-propagation](/blog/assets/2024/back-propagation.png)
![feed-forward-lstm](/blog/assets/2024/feed-forward-lstm.png)
![bidirectional-rnn](/blog/assets/2024/bidirectional-rnn.png)
![formulae](/blog/assets/2024/formulae.png)
![computation-graph](/blog/assets/2024/computation-graph.png)
![lstm-cell](/blog/assets/2024/lstm-cell.svg)
![example](/blog/assets/2024/example.png)
![lstm](/blog/assets/2024/lstm.png)
![example2](/blog/assets/2024/example2.png)
![rnn-notation](/blog/assets/2024/rnn-notation.png)
![example3](/blog/assets/2024/example3.png)
![unrolled-rnn](/blog/assets/2024/unrolled-rnn.png)
![feed-backward-lstm](/blog/assets/2024/feed-backward-lstm.png)
![vanilla-forward-pass](/blog/assets/2024/vanilla-forward-pass.png)


# LSTM
The LSTM architecture consists of a set of recurrentlyconnectedsubnets, known as memory blocks. These blocks canbe thoughtofas a differentiable version of the memory chips in a digital
computer. Each block contains one or more self-connectedmemorycells and three multiplicative units that provide continuousanalogues of write, read and reset operations for the cells
* The input, output and forget gates.


# Python Code Vanilla Example
https://gist.github.com/karpathy/d4dee566867f8291f086

# Microsoft Phi3 Lecture

## Example 1: Basic Recurrent Neural Network**

Let's consider an example where we have three inputs x_t (time t), and 
corresponding hidden states h_t. Our task is to find y_t, our output at 
time step 't'. Here are the calculations for each of these steps using 
simple RNN:

1) **Calculating Hidden State**

The hidden state `h_t` is calculated as follows:

```math
    h_t = f(W_{hh}*h_(t-1) + W_{xh}*x_t)
```

Let's suppose our inputs x_t and previous hidden states are [0.5, 0.6] and
[0.4] respectively. Also, let the weight matrices be as follows:

```math
    W_{hh} = [[0.1, -0.2],
              [-0e-1, 0.3]]
    W_{xh} = [[0.3, -0.5],
              [0.4, -0.7]]
```

Then we can calculate `h_t` as follows:

```math
    h_t = f(W_{hh}*[0.4, 0] + W_{xh} * [0.5, 0.6])
        = f([0.03, -0.02] + [0.15,-0.38])
        = f([0.18, -0.39])
```

Assuming the activation function `f(x)` is a sigmoid function (used 
commonly in RNNs), we can calculate its output:

```math
    h_t = 1/(1+exp(-[0.18, -0.39]))
       ≈ [0.54, 0.67]
```

2) **Calculating Output**:

The output `y_t` is calculated as follows:

```math
    y_t = g(W_{hy}*h_t)
        ≈ g([0.1 * 0.54 + (-0.2) * 0.67], [0.3 * 0.54 + (-0.5) * 0.67])
        ≈ [-0.09, -0.18]
```

## Example 2: LSTM Cell

In case of Long Short-Term Memory (LSTM), the cell state and hidden states
are computed through a series of gates. Let's illustrate this with an 
example involving only one gate for simplicity – let’s call it forget gate
'f'. The calculations will be much more complex in real applications but 
I'll simplify here:

Let's consider we have input x_t = [0.7], a previous hidden state h_(t-1)  = [0.3] and weight matrices W_{hi} = [[0.2, -0.4]], f_gate matrix = 
[[0.5], [-0.6]]

The forget gate calculation:

```math
    i_t = σ(W_{hi}*h_(t-1) + b_i) 
        ≈ [0.2 * 0.3 - 0.4] * [0.5]
       ≈ [-0.06]
```

The output gate calculation:

```math
    o_t = σ(W_{ho}*h_(t-1) + b_o)
        ≈ (0.2 * 0.3 - 0.4) * [0.5]
       ≈ [-0.06]
```

The new cell state:

```math
    c_t = f_t * c_(t-1) + i_t * tanh(W_{xc}*x_t + b_c)
        ≈ (-0.06)*c_(t-1) + (0.27)*tanh([0.7])
       ≈ c_(t-1) - 0.06, assuming the previous cell state was [0.5]
```

These examples should give you a better understanding of how RNNs work on 
a mathematical level. In real applications, this process would be repeated
for each time step in your input sequence!