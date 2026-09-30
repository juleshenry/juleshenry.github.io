---
layout: post
title: "Quantum Plankton Under Compression"
date: 2026-03-07
mathjax: true
---

*Revised September 30, 2026. The original version of this post reported that a quantum neural network beat a parameter-matched classical model on 20 of 25 plankton classification tasks. That result came from an undertrained baseline, and it does not survive a fair re-run. This version replaces it with the re-run, explains why the quantum model could never have had an advantage, and estimates what it would take for a model of this kind to match a CNN.*

In early 2026 I spent about a month teaching a simulated quantum computer to tell apart microscopic lake creatures. The images come from the Eawag zooplankton dataset behind *Deep Learning Classification of Lake Zooplankton* (Kyathanahally et al., 2021), where an ensemble of CNNs reaches 98% accuracy across 35 classes. My quantum model could not see what those CNNs see. Each image is resized to a 4×4 grayscale grid, and each of the 16 pixels is written into one qubit as a rotation angle, $R_y(\pi x_i)$. A seventeenth qubit collects the answer. The figure below shows what that costs. The top row is the microscope image, the middle row is the 28×28 input a small CNN receives, and the bottom row is everything the quantum circuit ever gets to look at.

<img src="/blog/assets/2026/quantum-plankton/what_the_models_see.png" alt="Eight plankton taxa shown as original images, as 28x28 CNN inputs, and as the 4x4 inputs encoded into the 16-qubit circuit" style="max-width:100%;">

The original experiment ran in seven phases: reproducing a published quantum MNIST notebook, building a binary plankton classifier, tuning it with nested cross-validation, comparing it against classical baselines on 25 pairs of species, scaling up to 16 classes, drawing saliency maps, and measuring the circuit's expressibility and entanglement. The whole pipeline ran in TensorFlow Quantum inside an x86 Docker container, emulated on an M1 laptop with deliberate sleeps between epochs to keep the machine from overheating. A full run took about twenty hours. The headline result was Phase 4: across 25 species pairs, the quantum network beat a 55-parameter classical network by 6.2 percentage points on average, winning 20 of 25 pairs, with a Wilcoxon p-value of 0.0007.

## Where the result came from

The number that should have stopped me was the classical baseline's accuracy. Averaged over the 25 pairs, the "fair" classical network scored 59.4%. Always guessing the more common species in each pair scores 58.8%. A network with 55 weights and 16 inputs should do much better than that on a binary task, so the baseline had barely learned anything. The reason is the training budget. Each fold trained on about 160 images for 20 epochs in batches of 32, which is at most 100 gradient steps at Adam's default learning rate of 0.001, with early stopping after three epochs without improvement. That is not enough for a small network starting from random weights. The quantum model was on the same schedule, but its accuracy was higher, and on 6 of the 25 pairs it was exactly the majority rate: it had learned to always answer with the larger class. A contest between a model that never learned and a model that learned to guess is not a comparison of anything.

The baseline was not parameter-matched either. The quantum circuit alternates three blocks of 16 $XX$ and 16 $ZZ$ couplings between each data qubit and the readout qubit with two blocks of 16 $R_x$ and 16 $R_y$ single-qubit rotations. That is $3 \times 32 + 2 \times 32 = 160$ trainable angles, about three times the classical network's 55.

The pattern is well documented. Bowles, Ahmed and Schuld ran a large benchmark of published quantum classifiers in 2024 and found that properly tuned classical models outperformed them nearly across the board, and that removing the entanglement from the quantum models often did not hurt them. A comparison where the quantum model wins against a weak baseline is the usual failure mode of this literature, and my experiment was an instance of it.

## The circuit is classically easy

There is a deeper problem, and it also explains why the original pipeline was so slow for no good reason. Every two-qubit gate in the circuit connects a data qubit to the same readout qubit $r$. Within one block, the gates $\exp(-i\tfrac{\pi s_i}{2} X_i X_r)$ therefore all commute, because they share the factor $X_r$ and act on different data qubits. Write $X_r = P_+ - P_-$, where $P_\pm$ project the readout onto the eigenstates of $X_r$. The whole block becomes

$$
U_{XX} \;=\; P_+ \otimes \bigotimes_{i=1}^{16} e^{-i\frac{\pi s_i}{2} X_i} \;+\; P_- \otimes \bigotimes_{i=1}^{16} e^{+i\frac{\pi s_i}{2} X_i},
$$

and the same holds for the $ZZ$ blocks with $Z_r$. Each branch is a product of single-qubit rotations. So a block turns one product state (a readout state times 16 independent qubit states) into a sum of two product states, and the rotation layers keep products as products. The encoded image starts as a product state, and the circuit has six entangling blocks, so the final 17-qubit state is always a sum of at most $2^6 = 64$ product states. The measured value is then

$$
\langle Z_r \rangle \;=\; \sum_{m,k=1}^{64} \langle \rho_m | Z | \rho_k \rangle \prod_{i=1}^{16} \langle \phi_{m,i} | \phi_{k,i} \rangle,
$$

which is $64^2$ products of 16 overlaps between two-dimensional vectors. The cost grows linearly with the number of qubits, not exponentially. I wrote this simulator in about a hundred lines of JAX and checked it against Google's cirq running the original circuit; they agree to within $10^{-4}$. It runs natively on the M1, needs no Docker and no thermal sleeps, and trains a model in seconds.

That is the end of any hope for quantum advantage from this architecture. A model a laptop can evaluate exactly in linear time cannot do anything a laptop cannot do. It is a particular family of functions of 16 numbers, and the only question is whether it is a good family. Recent theory makes the same point more generally: Cerezo and collaborators showed in 2025 that the circuits which avoid barren plateaus, the vanishing gradients that make large circuits untrainable, tend to be exactly the ones that are classically simulable.

## A fair re-run

With a fast simulator, a fair comparison is cheap. I re-ran Phase 4 with the same 25 pairs, the same 4×4 inputs, the same folds and seeds, and the same 200-image training cap, three times over with different shuffles. The quantum network and the small classical network were each trained twice: once under the original schedule, and once with an equal tuning budget of three learning rates, up to 150 epochs and more patient early stopping, choosing the learning rate on validation data only. Two standard classical models joined them, a logistic regression and a support vector machine with an RBF kernel, both tuned by cross-validation inside each training fold.

| Model (4×4 input unless noted) | Trainable parameters | Mean accuracy over 25 pairs |
| :--- | ---: | ---: |
| Always guess the larger class | 0 | 58.8% |
| Small classical network, original schedule | 55 | 59.7% |
| Quantum network, original schedule | 160 | 66.3% |
| Quantum network, tuned | 160 | 70.1% |
| Small classical network, tuned | 55 | 78.8% |
| Logistic regression | 17 | 79.9% |
| RBF support vector machine | n/a | 86.1% |
| CNN on 28×28 input (Phase 4) | 121,345 | 90.6% |

Under the original schedule, the old result reappears: the quantum network beats the undertrained classical network by 6.6 points and wins 21 of 25 pairs, almost exactly the original result. Give both the same tuning budget and the order reverses. Tuning adds 19 points to the classical network and 4 to the quantum one, and the tuned classical network wins on 24 of the 25 pairs, by 8.7 points on average (Wilcoxon $p = 4 \times 10^{-7}$). Logistic regression, with 17 parameters, beats the quantum network on 24 pairs and ties it on the 25th, where both sit exactly at the majority rate. The SVM beats it on all 25, by 15.9 points on average. Across the 375 test folds, the tuned quantum network answered every test image with the same class in 34% of them. The SVM never did. The quantum network's best showing was eudiaptomus against uroglena, where it reached 98.0%, ahead of the tuned classical network but still behind logistic regression and the SVM.

<img src="/blog/assets/2026/quantum-plankton/pair_accuracy.png" alt="Per-pair test accuracy of the tuned QNN, logistic regression and RBF SVM, with the majority-class rate marked for each of 25 plankton pairs" style="max-width:100%;">

One objection is that the tuning itself was noisy, because the learning rate was chosen on only about 40 validation images. On one pair, bosmina against brachionus, the untuned quantum network actually beat the tuned one. To rule this out I gave the quantum network an unfair advantage: for every fold, keep whichever of its two versions scored higher on the test set. Even this oracle loses to logistic regression by 9.1 points and to the SVM by 15.2 points on average, and it wins none of the 25 pairs against the SVM.

The same run explains two other results from the original post. The Phase 5 multi-class experiment, which used a properly swept classical baseline, already showed the classical network ahead at every class count from three up. And the Phase 7 expressibility measurement, which reported a KL divergence of exactly 0.0000 at every circuit depth, was an artifact. For 17 qubits, the fidelity between two random states is almost always close to $2^{-17} \approx 7.6 \times 10^{-6}$. With 75 histogram bins on $[0,1]$, both the circuit's distribution and the reference distribution land entirely in the first bin, so their divergence is zero whatever the circuit does.

## What would parity with a CNN take?

The 28×28 CNN from Phase 4 averaged 90.6% on these pairs. For a quantum model to match it, the first requirement is information, not quantum hardware. At 4×4 the best classical model I tried, the SVM, averages 86.1%, so no model of any kind reaches the CNN from 16 pixels. The resolution sweep below trains the same tuned logistic regression and SVM on larger images:

| Input | Pixels | Logistic regression | RBF SVM |
| :--- | ---: | ---: | ---: |
| 4×4 | 16 | 79.9% | 86.2% |
| 6×6 | 36 | 85.0% | 88.5% |
| 8×8 | 64 | 86.3% | 89.0% |
| 12×12 | 144 | 86.7% | 89.7% |
| 16×16 | 256 | 86.8% | 89.5% |
| 28×28 | 784 | 87.0% | 89.1% |

Accuracy climbs quickly up to 12×12 and then stops. The SVM comes within a point of the CNN at 144 pixels and never catches it, even with all 784. With 200 training images, a generic model runs out of improvement before the CNN does, because the CNN builds in an assumption that nearby pixels belong together, and that assumption is worth more than extra resolution. Parity therefore needs two things: roughly 150 pixels of input, which with one pixel per qubit means roughly 150 data qubits, and an architecture with the same kind of locality bias. The quantum architectures designed to have that bias, quantum convolutional networks, were shown in 2024 to be effectively classically simulable on the standard benchmarks (Bermejo et al.), which is not encouraging.

The second requirement is that the circuit be worth running on quantum hardware at all, which means it must be hard to simulate classically. The architecture here fails that test at any size, so it never reaches parity in any meaningful sense: scaled up, it becomes a fast classical model with an unusual structure. A circuit that is genuinely hard to simulate needs entangling gates between data qubits, and about 150 qubits with ten or so entangling layers, plus the swaps needed to route them on a real chip, comes to roughly 3,000 two-qubit gates. If each gate fails with probability $\varepsilon$, the useful signal survives with probability roughly $(1-\varepsilon)^G$ for $G$ gates, and the number of repetitions needed to read it grows as the inverse square of that. With $G \approx 3{,}000$ and IBM's best current error per layered gate of about $2 \times 10^{-3}$, the surviving signal is about $e^{-6}$, and an output that would need a thousand shots on a perfect machine needs over a hundred million. To keep half the signal, $\varepsilon$ has to fall to about $2 \times 10^{-4}$, which in practice means error-corrected logical qubits. IBM's roadmap puts its first machine of that kind, Starling, at about 200 logical qubits and 100 million gates in 2029, and Blue Jay at about 2,000 logical qubits after 2033.

The third requirement is training, and it is the hardest. A quantum circuit has no backpropagation. The standard way to get a gradient, the parameter-shift rule, runs the circuit twice per parameter, so one gradient for one image costs $2P$ circuit executions, each repeated for a thousand or more measurement shots. For a model with a few thousand parameters trained on a few thousand images for tens of epochs, that is on the order of $10^{13}$ shots. At IBM Nighthawk's advertised rate of about 100,000 circuits per second, that is years of machine time, and error-corrected machines will run their logical operations far more slowly than today's physical ones.

My prediction is therefore that a quantum classifier reaches CNN parity on these pairs no earlier than the early 2030s, needs on the order of 150 to 200 logical qubits and a convolution-like architecture to do it, and even then does so by being a large and expensive function approximator rather than by exploiting anything quantum. Parity is the best case. The images are ordinary classical data with no quantum structure for a quantum model to exploit, and the theory of learning from classical data (Huang et al., 2021) gives little reason to expect an advantage. A CNN that trains in a minute on a laptop will remain the practical choice.

## What the laptop was good for

In one sense, attempting quantum machine learning on a 16 GB laptop was foolhardy. A dense simulation of $n$ qubits stores $2^n$ complex amplitudes, and at 16 bytes each, 16 GB runs out at about 30 qubits. Twenty hours of emulated TensorFlow Quantum made the project feel like it was pushing against that limit. It was not. This circuit needed a few kilobytes, and the real limits were an emulation layer that should not have been there and a baseline that was never trained.

What the laptop is good for is building the method, and the method is what carries over to larger machines: an exact simulator validated against a reference implementation, classical baselines given the same tuning budget as the quantum model, the majority-class rate reported next to every accuracy, pairs rather than folds as the unit of statistical comparison, and a check of whether the circuit is classically simulable before any claim about it is made.

The obvious next step is to take a trained circuit to real hardware, and in 2026 that is easy to do. IBM's free Open Plan gives up to 10 minutes of processor time every 28 days on 156-qubit Heron and 120-qubit Nighthawk chips, with a one-time promotion of 180 more minutes this year. Amazon Braket charges 30 cents per task plus a per-shot fee that ranges from about 0.04 cents on Rigetti to 8 cents on IonQ Forte. Training on hardware is out of reach: with 160 parameters, one pass over 160 training images needs about 50,000 circuit executions, each repeated for hundreds of shots. Inference is not: train the circuit exactly on the laptop, then send the 200 or so test images of a pair to an IBM processor and measure how much accuracy hardware noise costs. There is an extra complication. Every data qubit talks to one readout qubit, and no real chip is wired as a star, so the compiler has to insert swap gates that add depth and noise. D-Wave's annealers are a different kind of machine that solves optimisation problems rather than running circuits, so this model cannot run there. The closest D-Wave experiment would train a support vector machine written as an optimisation problem, which Willsch and colleagues did in 2020.

None of that would change the conclusion above, because a hardware run of a classically simulable circuit can only add noise to an answer a laptop computes exactly. The experiment worth running on quantum hardware is a different one: a circuit that is provably hard to simulate, benchmarked against classical baselines tuned as carefully as the ones here. I no longer expect that experiment to favour the quantum model on images of plankton. But it is the right experiment, and the laptop is where to build the machinery for it.

The code, including the Phase 8 simulator, benchmark and figures, is on [GitHub](https://github.com/juleshenry/quantum-plankton-ml).

### References

- S. Kyathanahally et al., *Deep Learning Classification of Lake Zooplankton*, Frontiers in Microbiology (2021). [arXiv:2108.05258](https://arxiv.org/abs/2108.05258)
- E. Farhi and H. Neven, *Classification with Quantum Neural Networks on Near Term Processors* (2018). [arXiv:1802.06002](https://arxiv.org/abs/1802.06002)
- J. Bowles, S. Ahmed and M. Schuld, *Better than classical? The subtle art of benchmarking quantum machine learning models* (2024). [arXiv:2403.07059](https://arxiv.org/abs/2403.07059)
- M. Cerezo et al., *Does provable absence of barren plateaus imply classical simulability?*, Nature Communications (2025). [arXiv:2312.09121](https://arxiv.org/abs/2312.09121)
- P. Bermejo et al., *Quantum convolutional neural networks are (effectively) classically simulable* (2024). [arXiv:2408.12739](https://arxiv.org/abs/2408.12739)
- H.-Y. Huang et al., *Power of data in quantum machine learning*, Nature Communications (2021). [arXiv:2011.01938](https://arxiv.org/abs/2011.01938)
- D. Willsch et al., *Support vector machines on the D-Wave quantum annealer*, Computer Physics Communications (2020). [arXiv:1906.06283](https://arxiv.org/abs/1906.06283)
- IBM Quantum, [plans overview](https://quantum.cloud.ibm.com/docs/en/guides/plans-overview) and [Nighthawk r2](https://www.ibm.com/quantum/blog/nighthawk-r2).
