---
layout: post
title: "Back-of-the-Envelope: Convolutional Neural Networks"
date: 2024-08-04
categories: machine-learning
---
# Terse notes on CNN's.

<ol>
    <li>Convolution</li>
    <li>Kernel</li>
    <li>Pooling</li>
    <li>Feed Forward Classification</li>
</ol>

# Convolution
A convolution combines information about local pixels such that pixels close to each other in an image are  ”summarized” by a smaller set of pixels.

A discrete convolution is defined like so:
![sshfs](/blog/assets/2024/cnn/discrete-convolution.png)

A continuous convolution is defined like so:
![sshfs](/blog/assets/2024/cnn/continuous-convolution.png)

Comparison
![sshfs](/blog/assets/2024/cnn/comparison.png)


# Kernel
In a CNN, the kernel refers to a filtered sampling window. For more insight, I like to refer to the Romance languages, which confer terms literally translating as nucleus (Spanish, Portuguese) or center (French). 

For example, a Gaussian blur can be achieved by iterating a 5x5 kernel over an image in which the weights are normally distributed from the center pixel going outwards. Therefore, the effect is that the central pixel is emphasized, while gaining marginal color from its neighbors, achieving a blur.

Kernels are leveraged to downsample from the data. Here are some examples

Comparison
![sshfs](/blog/assets/2024/cnn/kernel-examples.png)


# Pooling:
Pooling is another similar operation to convolutions done on an image. Sometimes, applying a convolution to an image doesn’t reduce an image enough, so we can further utilizing pooling operations. Pooling is a lot
more simple than applying a convolution in that we do not have a kernel full of elements. Instead, we have a filter that we slide across the image, and for every position of this filter, we simply take the minimum,
maximum, mean, or median, of the set of pixels inside the image that fall underneath this filter. It is most typical to use a max pool with a 2x2 filter and a 2x2 stride, such that there is no overlap between filters.
Using max pool has seemed to work better than the average pool.

Here is a concrete example of a pool:
![sshfs](/blog/assets/2024/cnn/maxpool.png)


# Microsoft Phi3 Lecture

**What is a Convolutional Neural Network?**

A Convolutional Neural Network (CNN) is a type of feedforward neural 
network that uses convolutional and pooling layers to extract features 
from images or other data with grid-like topology. The key characteristics
of a CNN are:

1. **Convolutional Layers**: These layers use small filters to scan the 
input data, performing a dot product at each position to generate a 
feature map.
2. **Pooling Layers**: These layers downsample the output of convolutional
layers, reducing the spatial dimensions and increasing the robustness to 
small translations.
3. **Activation Functions**: CNNs typically use ReLU (Rectified Linear 
Unit) or Sigmoid activation functions in hidden layers.

**Architecture**

A typical CNN architecture consists of:

1. **Input Layer**: The input layer receives the raw data, such as an 
image.
2. **Convolutional Layers**: One or more convolutional layers extract 
features from the input data.
3. **Pooling Layers**: One or more pooling layers downsample the output of
convolutional layers.
4. **Flatten Layer**: The flatten layer reshapes the output into a 1D 
array, which is then fed into fully connected (dense) layers.
5. **Dense Layers**: One or more dense layers perform classification or 
regression tasks.

![sshfs](/blog/assets/2024/cnn/general-cnn-architecture.png)


**How CNNs Work**

Here's a step-by-step explanation of how a CNN works:

1. **Data Input**: The input data (e.g., an image) is fed into the CNN.
2. **Convolutional Layer**: The convolutional layer applies filters to the
input data, generating a feature map.
3. **Activation Function**: The activation function (e.g., ReLU) is 
applied to the output of the convolutional layer.
4. **Pooling Layer**: The pooling layer downsamples the output of the 
convolutional layer.
5. **Repeat Steps 2-4**: This process is repeated multiple times, with 
each convolutional layer extracting more abstract features from the input 
data.
6. **Flatten Layer**: The output of the convolutional layers is flattened 
into a 1D array.
7. **Dense Layers**: One or more dense layers perform classification or 
regression tasks using the flattened output.

**Applications**

CNNs have numerous applications in computer vision, including:

1. **Image Classification**: CNNs are widely used for image classification
tasks, such as object recognition and scene understanding.
2. **Object Detection**: CNNs can detect objects within images, including 
people, animals, and vehicles.
3. **Segmentation**: CNNs can segment specific regions or objects from an 
image.
4. **Image Generation**: CNNs can generate new images based on patterns 
learned from a dataset.

**Key Advantages**

1. **Robustness to Small Translations**: CNNs are robust to small 
translations, thanks to the pooling layers.
2. **Ability to Extract Abstract Features**: CNNs can extract abstract 
features from input data, such as edges and textures.
3. **Flexibility in Architecture**: CNNs can be customized with different 
numbers of convolutional and pooling layers.

### Sources
* [Lecture on CNN, Washington University](https://courses.cs.washington.edu/courses/cse416/22su/lectures/10/lecture_10.pdf)

* [3 Brown 1 Blue](https://www.youtube.com/watch?v=KuXjwB4LzSA)

* [Microsoft Phi3](https://azure.microsoft.com/en-us/products/phi-3)