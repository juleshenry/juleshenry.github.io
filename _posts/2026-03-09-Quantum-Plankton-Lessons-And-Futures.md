---
layout: post
title: "Quantum Plankton: Lessons Learned and What Comes Next"
date: 2026-03-09
mathjax: true
---

# [Quantum Plankton: Lessons Learned and What Comes Next](https://github.com/juleshenry/quantum-mnist)

I spent the better part of a month teaching a quantum computer to look at microscopic lake creatures that had been crushed down to 16 pixels and guess what they were. The [full technical writeup](/blog/2026/03/07/Quantum-Plankton-ML) covers the seven-phase investigation in detail. This post is about what I actually learned doing it, the things that surprised me, and where this whole direction might go.

---

## The Keyhole Problem

Everyone in quantum ML talks about qubit counts and circuit depth and entanglement entropy. Nobody talks about the fact that your entire input pipeline is a violence against information. We took plankton images -- beautiful, high-resolution micrographs of daphnia and cyclops and diaphanosoma -- and collapsed them to a $4 \times 4$ grayscale grid. Sixteen numbers. That is what the quantum circuit sees. Sixteen numbers that used to be an organism.

And here is the thing: this is not a limitation of the quantum model. This is a limitation of quantum *simulation*. The `4x4` encoding exists because simulating 17 qubits on a classical machine is already pushing it. You want `8x8`? That is 64 qubits. Good luck simulating that on your MacBook. Good luck simulating that on anyone's MacBook. The entire experimental regime was shaped by compute constraints that have nothing to do with the algorithm's theoretical capacity.

The bottleneck in quantum ML research is not the algorithm. It is the simulation. Until real quantum hardware with enough qubits, low enough noise, and fast enough gate times becomes accessible, we are studying quantum circuits through a classical keyhole. Everything I learned in this project is conditioned on that keyhole being `4x4`.

---

## 38.44%

Phase 2. First real experiment. Binary classification on plankton pairs. Mean accuracy: **38.44%**. Bootstrap 95% CI: $[35.49\%, 42.50\%]$. On a binary task. A coin flip would give you 50%.

My word.

I stared at those numbers for a while. The quantum model was performing *worse than random*. Not because the circuit was broken -- the simulation was numerically correct, the gradients were flowing, the loss was decreasing. But the default hyperparameters were wrong. The encoding was suboptimal. The learning rate was too aggressive. The batch size was arbitrary. It was a model assembled from reasonable defaults and deployed without tuning, and it performed like you would expect: badly.

Phase 3 fixed this. Nested cross-validation. Inner loop for hyperparameter selection, outer loop for unbiased evaluation. The tuned model exceeded 60% on several pairs and hit **95.3%** on diaphanosoma vs diatom_chain. Same circuit architecture. Same data. Different configuration. Bad results do not mean the approach is dead. They mean the approach has not been configured yet. This sounds obvious written down. It does not feel obvious when you are looking at sub-random accuracy from a circuit you spent three days building.

---

## Why Deeper Was Worse

This one genuinely surprised me. The hyperparameter search in Phase 3 converged on a single PQC layer as optimal. One layer. 32 trainable parameters. On a 17-qubit circuit.

I had assumed -- as most of the literature implicitly assumes -- that deeper circuits would capture more complex decision boundaries. More layers, more parameters, more expressiveness, better accuracy. The usual deep learning intuition. But the Phase 7 expressibility analysis told a different story. Yes, adding layers increased the Meyer-Wallach entanglement measure:

| Layers | Entanglement (95% CI) |
| --- | --- |
| 1 | 0.531 $[0.508, 0.553]$ |
| 2 | 0.750 $[0.733, 0.767]$ |
| 3 | 0.869 $[0.855, 0.881]$ |

More depth, more entanglement, bigger reachable state space. Beautiful. But on a `4x4` input with 16 features, there simply is not enough information to justify that expressiveness. The deeper circuits were over-parameterized. They were fitting noise. One layer was the right inductive bias for the amount of information actually present in the compressed representation.

In classical deep learning you have millions of pixels to justify millions of parameters. In a 16-feature quantum regime, one layer of 32 parameters is already generous. The circuit's capacity has to match the information content of the input, not your ambition.

---

## The Statistics Nearly Killed the Story

If I had to pick one thing that separates this project from most quantum ML demos I have seen, it is the statistical design. And I say that not to brag -- I say it because the statistics nearly killed the story.

Here is the problem: with 5-fold cross-validation, the minimum achievable p-value for a Wilcoxon signed-rank test is $2/2^5 = 0.0625$. You literally cannot reject the null hypothesis at $\alpha = 0.05$ with five paired observations, no matter how large the effect. The test does not have enough resolution. This is a mathematical fact, not a sample size issue you can fix by running more epochs.

So the per-pair comparisons in Phase 4? Most of them are marked "Not Significant." Only one pair (eudiaptomus vs uroglena, $p = 0.0002$) crossed the significance threshold. If you only looked at individual pairs, you would conclude the QNN is indistinguishable from the classical baseline.

But that is the wrong analysis. The right analysis treats the 25 pairs as replication units and asks: across all pairs, does the QNN systematically outperform? The answer is yes. Mean delta $+6.23\%$, Cohen's $d = 0.705$, Wilcoxon $p = 0.0007$, 20 wins out of 25. The power analysis showed that at the observed effect size ($d \approx 0.65$), 25 pairs yields 88% statistical power. That is a properly powered experiment with a defensible inferential claim.

The quantum ML literature is full of papers that report a single train/test split and declare quantum advantage. Papers that use cross-validation but never compute power. Papers that show impressive accuracy numbers without mentioning what a random baseline would achieve. Designing the statistics first -- the validation scheme, the test, the power analysis -- is not optional. It is the experiment.

---

## TensorFlow Quantum Does Not Install Cleanly Anywhere

This is a purely practical aside, but it cost me more hours than any of the scientific work.

TensorFlow Quantum requires `tensorflow==2.7.0`, `cirq==0.13.1`, `sympy==1.8`, and `numpy==1.21.6`. This combination does not install cleanly on a modern Python. It does not install cleanly on an M-series Mac. It does not install cleanly anywhere that is not the exact Docker environment it was designed for.

So everything runs in Docker. On Apple Silicon, that means AMD64 emulation via Rosetta 2. Which works. Slowly. Under thermal duress.

I added pacing controls to the experiment scripts -- `EPOCH_COOL`, `THERMAL_SLEEP`, `BREATHE_SLEEP` -- because without them, long Phase 4 runs (25 pairs $\times$ 5 folds $\times$ 3 models) would thermal-throttle the machine into submission. The estimated compute time for Phase 4 at full power is ~6.2 hours. Under emulation with thermal pacing, it is more like a full day. The Dockerfile pins every dependency version and runs the 82-test verification suite at build time. If the tests fail, the image does not build. This means that when I come back to this project in six months, it will still work. Exactly as it did. On any machine with Docker.

Reproducibility is not a README badge. It is a Dockerfile that runs your tests before it lets you touch the experiments.

---

## The Crossover

Phase 5 was the most revealing experiment. Same compressed input, same PCA-16 features, but now scale the number of classes from 2 to 16. Both the QNN and a parameter-matched classical model degrade as you add categories. But they degrade differently.

| K | QNN (PCA 16) | Classical (PCA 16) |
| --- | --- | --- |
| 2 | 71.0% | 68.8% |
| 3 | 54.5% | 55.6% |
| 4 | 46.1% | 47.8% |
| 5 | 37.8% | 40.5% |
| 8 | 30.2% | 31.8% |
| 16 | 18.3% | 21.7% |

At $k=2$, the QNN edges ahead. By $k=5$, the classical model pulls ahead. By $k=16$, the gap is 3.4 percentage points -- significant in a regime where random guessing gives you 6.25%.

The crossover happens around $k=3$. Below that, the QNN's entanglement-based feature interactions find structure that the classical learner misses. Above that, the classical learner's gradient dynamics handle the growing confusion matrix better. This is not evidence that quantum models are worse at multi-class tasks in general. It is evidence that *this* circuit, on *this* representation, under *this* parameter budget, loses its advantage as task complexity exceeds what the compressed input can support. The bottleneck is the 16 features, not the circuit.

Quantum models are not uniformly better or worse. They occupy a different region of the bias-variance tradeoff, and the crossover depends on the information regime. Understanding *where* that crossover happens -- and *why* -- is more scientifically valuable than any single headline accuracy number.

---

## Backpropagating Through a Quantum Circuit

Phase 6 was a sanity check that turned into one of the more interesting results. Can you compute gradient-based saliency maps through a quantum circuit? Yes. Because the TFQ simulation is fully differentiable. You backpropagate through the quantum layer exactly like you would through a classical layer, get a gradient with respect to the 16 PCA-compressed input features, invert the PCA transform, and land on a $28 \times 28$ saliency heatmap showing which spatial regions most influenced the decision.

Quantum circuits are not black boxes in the way people sometimes assume. If your simulation backend supports autodiff -- and TFQ does -- then saliency maps, gradient-weighted class activation maps, feature attribution, all of it is available out of the box. The quantum layer is just another differentiable layer in the computation graph.

The saliency maps showed the QNN attending to localized morphological features -- body edges, flagella, shell outlines -- rather than uniform background. The model is not solving the task through some artifact of the preprocessing pipeline. It is actually looking at plankton morphology. Even at `4x4` resolution. Quantum interpretability is not a future research direction. It is available now.

---

## Where This Goes

Alright. Lessons learned. Humility acquired. Now let me talk about why I think this direction is worth pursuing despite all the caveats.

### The Hardware Is Coming

IBM's 1000+ qubit systems, Google's Willow chip, Quantinuum's trapped-ion machines -- the qubit counts and gate fidelities are improving on a curve that is starting to look exponential rather than linear. The `4x4` bottleneck that shaped this entire project exists because simulating 17 qubits on a classical machine is expensive. On actual quantum hardware, 17 qubits is trivial. What happens when you can run 64, 128, or 256 qubits with low enough noise to get meaningful expectation values?

You encode `8x8`, `16x16`, or higher-resolution images directly. The information bottleneck disappears. The circuit sees real spatial structure instead of a 16-number summary. If the QNN's advantage at $k=2$ under compression holds up when the compression is relaxed, there might be a genuinely useful regime for quantum image classification. If it does not, at least we will know.

And then there is error correction. This project ran on a noiseless simulator -- every gate perfect, every measurement exact. Real quantum hardware has decoherence, gate errors, crosstalk, readout noise. Current error rates make it difficult to extract clean gradients from parameterized circuits. But Google's recent result showing below-threshold error rates on surface codes means that logical qubits with arbitrarily low error rates are theoretically achievable. When error-corrected quantum computers become available for variational workloads, the noise limitation vanishes and the algorithm's native behavior becomes directly observable. That is when the real benchmarks start.

### First Drafts of First Drafts

The circuit in this project was deliberately simple: angle encoding, a CZ entanglement layer, parameterized XX/ZZ interactions, readout on an ancilla. This is the quantum equivalent of a single-layer perceptron. The classical deep learning revolution did not happen with single-layer networks. It happened with ResNets, attention mechanisms, skip connections, normalization layers, and carefully designed inductive biases.

Quantum circuit design is still in its infancy. **Data re-uploading** -- encoding classical data multiple times at different circuit depths. **Quantum convolutional circuits** -- local entanglement patterns that respect spatial structure the way a classical kernel respects locality. **Quantum attention mechanisms** -- parameterized entanglement conditioned on input features. The design space for parameterized quantum circuits is enormous and almost entirely unexplored. The circuits I used in this project are not state-of-the-art. They are first drafts.

### Generative Quantum Models and the EAWAG Rematch

Everything in this project was discriminative -- given an input, produce a label. But some of the most exciting quantum ML work is generative. Quantum Born machines, quantum GANs, quantum Boltzmann machines -- they exploit the fact that quantum circuits naturally produce probability distributions over exponentially large state spaces. Sampling from these distributions is what quantum computers do natively. Classical generative models have to learn to approximate complex distributions from scratch. Quantum generative models start from a distribution that is already exponentially expressive. Imagine training a quantum generative model on plankton morphologies and using it to synthesize novel training examples for rare species. Data augmentation via quantum sampling. The theoretical framework exists and the hardware gap is closing.

And the EAWAG dataset deserves a rematch. Kyathanahally et al. achieved **98% accuracy** on 35-class plankton classification using ensembles of DenseNet, ResNet, and MobileNet at full resolution. Our quantum model hit 71% on 2 classes at `4x4` resolution. That is not a comparison. That is two experiments in different universes. A proper rematch would need higher resolution encoding, noise-aware training, multi-class quantum architectures with readout strategies better than one-qubit-per-class, hardware execution on a real quantum processor, and matched compute budgets. That is a multi-year research program, not a weekend project. But the scaffolding is here -- the validation framework, the statistical design, the baseline comparisons -- all of it transfers.

One direction I did not explore at all: using the quantum circuit not as the final classifier but as a feature extractor feeding a classical head. A quantum encoder producing a compact, entanglement-informed representation, classified by a gradient-boosted tree or a small MLP. Sidestep the multi-class scaling problem entirely. Let the classical head handle the softmax. This is the quantum equivalent of transfer learning: use the quantum circuit for what it is good at -- low-dimensional feature interactions in Hilbert space -- and offload what it is bad at to a classical model that has been solving that problem since 1958.

---

## Closing

I built an 82-test verification suite, a power analysis framework, a 7-phase experimental pipeline, and a Docker-based reproducibility stack to classify plankton at `4x4` resolution using quantum circuits. The QNN won 20 out of 25 binary comparisons against a matched classical baseline. It lost the multi-class scaling contest. It produced interpretable saliency maps. It ran on a noiseless simulator because real quantum hardware is not ready yet.

Is this quantum advantage? No. Not by any rigorous definition. The comparison is against a deliberately hobbled classical model under artificial compression constraints. A ResNet on full-resolution images would obliterate both.

Is it scientifically informative? I think so. It tells us something about how parameterized quantum circuits behave under extreme information bottlenecks, how their representational character changes with scale, and how to design experiments that separate signal from noise in a field that is drowning in hype.

The future of quantum ML is not going to arrive as a single paper showing quantum advantage on ImageNet. It is going to arrive as a slow accumulation of understanding -- circuit by circuit, dataset by dataset, carefully controlled comparison by carefully controlled comparison -- until one day the hardware catches up to the theory and we find out whether the mathematical promise of exponentially large state spaces translates into practical value.

I am betting it does. But I am also keeping my classical baselines close.

Meticulosity is for chumps, but sometimes you simulate 17 qubits to classify plankton and learn something real about the boundary between two computational paradigms.

Worth it.
