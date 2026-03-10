---
layout: post
title: "✨ Quantum Plankton Under Compression"
date: 2026-03-07
mathjax: true
---

I spent the better part of a month teaching a quantum computer to classify microscopic lake creatures after crushing each image into a `4x4` grayscale grid. The full seven‑phase investigation shows how a compressed quantum model behaves, how it compares to a parameter‑matched classical baseline, and how circuit structure maps to learning dynamics. This post combines the core results with the lessons I learned along the way—what held up, what didn’t, and where this research might go next.

---

## The Keyhole Problem: Input Compression Shapes Everything

Quantum machine learning is often presented through glossy benchmarks and broad claims, but nearly all of those results ride on the same hidden assumption: you can feed the circuit enough information for it to learn something real.

In this project, you can’t. The `4x4` encoding exists because simulating 17 qubits on a classical machine is already expensive. The bottleneck is not theoretical capacity; it is simulation. A 16‑pixel input is a keyhole that narrows every inference you draw. That keyhole shapes the entire story.

The core question becomes: if you force both quantum and classical models into the same brutal information bottleneck, what happens?

---

## From MNIST Reproduction to Plankton Classification

The repository progresses in phases, moving from reproduction to controlled comparison and then to interpretability and circuit‑level analysis.

### Phase 1: MNIST Reproduction

Recreate a published quantum MNIST demo to validate the stack.

### Phase 2: Binary Quantum Classification

Plankton images are downsampled to `4x4`, flattened to 16 features, and angle‑encoded via \(Ry(\pi x_i)\) rotations. A TensorFlow Quantum pipeline trains a binary classifier on plankton pairs using 5‑fold stratified cross‑validation with bootstrap confidence intervals.

The initial result: **38.44% mean accuracy**, with a 95% CI of \([35.49\%, 42.50\%]\). On a binary task. That is worse than a coin flip.

That wasn’t a failure of quantum circuits; it was a failure of configuration. The defaults were wrong.

### Phase 3: Hyperparameter Optimization

Nested cross‑validation tuned the configuration. The best model used:

- **Angle encoding**
- **One PQC layer**
- **Learning rate 0.01**
- **Batch size 16**
- **Hinge loss**

Under this setup, the QNN surpassed **60%** on multiple pairs, and hit **95.3%** on diaphanosoma vs diatom_chain. Same architecture. Same data. Different choices. Bad results did not mean the approach was dead—only that it wasn’t tuned yet.

### Phase 4: Classical Comparison

This is the scientific center. Instead of comparing against modern CNNs (which would be absurd at `4x4`), the QNN is matched against a classical model with the same compressed inputs and similar parameter budgets. We tested 25 binary plankton pairs, equalized sample counts, and used per‑pair metrics plus aggregate inference.

Aggregate results across pairs:

- **Mean delta (QNN − classical): +6.23%**
- **Cohen’s d: 0.705**
- **Wilcoxon p: 0.0007**
- **QNN wins: 20 / 25**

Under the compression regime, the QNN was competitive and often slightly better.

### Phase 5: Multi‑Class Scaling

Both models degrade as the number of categories increases. The QNN edges ahead at \(k = 2\), but the classical model overtakes by \(k = 5\). The crossover happens around \(k = 3\). This is the most honest outcome: the circuit’s advantage appears only in narrow, low‑class regimes under severe compression.

### Phases 6–7: Saliency, Expressibility, Entanglement

- **Saliency maps** show the QNN attends to localized morphology even at `4x4`.
- **Expressibility and entanglement** increase with depth, but deeper circuits overfit the tiny input. One layer was the right inductive bias.

---

## A Calculus Student’s Guide to PQC (via Grover’s Search)

To understand how a "Quantum Neural Network" works, you first need to understand **Grover’s Search**.

### The Primer: Grover’s as Geometric Rotation

In calculus, you’re used to functions \(f(x)\) that map numbers to numbers. In quantum, we map **vectors to vectors**.

Imagine a 16-dimensional space (for our `4x4` grid). Every possible image is a unit vector in this space. Grover’s Algorithm is a **fixed sequence of rotations**. You start with a "uniform" vector (pointing equally toward all possibilities) and you apply a "Reflection" and a "Rotation."

- **The Oracle:** Flips the sign of the "correct" vector (Reflection).
- **The Diffusion:** Rotates the entire state toward that flipped vector.

After \(\approx \sqrt{N}\) steps, the vector points almost perfectly at the marked item. **Grover’s is a hard‑coded geometric search.** It’s like a compass that is pre‑programmed to find North.

### From Grover to PQC: The Learnable Compass

A **Parametric Quantum Circuit (PQC)** is Grover’s Search with adjustable rotation angles. Instead of a fixed compass, you have knobs \(\theta_1, \theta_2, \ldots, \theta_n\) that change the circuit’s behavior.

We define a function \(f(\theta)\) where the output is the **expectation value** after many measurements:

\[
f(\theta) = \langle \psi | U(\theta)^\dagger M U(\theta) | \psi \rangle
\]

For a calculus student, this is just a **composite multivariable function**:

1. **Input:** 16 pixel intensities (initial rotations).
2. **Layers:** A series of rotation matrices \(R(\theta_i)\).
3. **Output:** A scalar between \(-1\) and \(1\).

Our goal is to find the \(\theta\) that minimizes a loss function \(L(f(\theta))\). For that, we need the gradient \(\nabla f\).

### The Parameter‑Shift Rule: Quantum Calculus

You can’t directly inspect the middle of a quantum circuit without collapsing the state. Instead, you use the **parameter‑shift rule**. For many gates, the derivative of the expectation value is exactly:

\[
\frac{\partial f}{\partial \theta_i} = \frac{1}{2} \left( f\left(\theta_i + \frac{\pi}{2}\right) - f\left(\theta_i - \frac{\pi}{2}\right) \right)
\]

This looks like the difference quotient you learned in calculus, except it’s not an approximation. It’s exact. Run the circuit twice—shifted forward and backward—and you get the precise slope. That is how the QNN learns.

### Mapping the Math to the Source Code

If you look at `phase2/binary_quantum_classifier.py`, you can see exactly where the calculus meets the qubits.

1. **The Knobs (`sympy.Symbol`)**

```python
symbol = sympy.Symbol(prefix + "-" + str(i))
circuit.append(gate(qubit, self.readout) ** symbol)
```

These symbols are the \(\theta\) variables. They define the degrees of freedom that the optimizer twists to minimize error.

2. **The Geometric Transformation (`XX`, `ZZ`, `RX`, `RY`)**

The `create_quantum_model` function defines the structure of the circuit using entangling gates (`XX`, `ZZ`) and rotation gates (`RX`, `RY`). Together they form a trainable landscape the model walks through during optimization.

3. **The Readout Preparation (`X -> H`)**

```python
circuit.append(cirq.X(readout))
circuit.append(cirq.H(readout))
```

This prepares the readout qubit in a specific state. A final `H` at the end turns phase information into a measurable probability.

4. **The Bridge (`tfq.layers.PQC`)**

```python
tfq.layers.PQC(model_circuit, model_readout)
```

This layer implements the parameter‑shift rule under the hood. When the optimizer asks for gradients, TFQ runs shifted circuits, computes exact derivatives, and passes them back into the classical training loop.

---

## How the Quantum Model Is Built

At the architectural level, the classifier is intentionally simple but scientifically motivated.

1. **Classical preprocessing**
   - Start from `16x16` grayscale plankton images.
   - Downsample to `4x4`.
   - Apply min–max normalization.
   - Flatten to a 16‑dimensional feature vector.

2. **Angle encoding and entanglement**
   - Encode each normalized pixel intensity \(x_i\) as an \(Ry(\pi x_i)\) rotation.
   - Use a linear chain of `CZ` gates to capture spatial correlations.
   - Add parameterized `XX`, `ZZ`, and `YY` interactions tying data qubits to a readout qubit.

3. **Readout and loss**
   - Measure the readout qubit in the \(Z\) basis and interpret the expectation value as a continuous score.
   - Optimize with hinge loss, which matches the \([-1, 1]\) output range and works naturally with binary labels.

This structure runs on a classical simulator in TensorFlow Quantum. The later expressibility and entanglement analyses use the same production circuit so the performance numbers and circuit metrics align.

---

## Statistical Design, Power, and Reproducibility

The project treats experimental design as part of the experiment.

### Cross‑Validation and Sampling

- **Phases 2, 4, 6** use stratified 5‑fold cross‑validation with bootstrap 95% confidence intervals.
- **Phases 3, 5** use nested cross‑validation (5 outer, 3 inner folds).
- The `Q_SAMPLES` parameter enforces equalized sample budgets across models.

Majority‑class and random baselines are reported so every accuracy number has a meaningful reference.

### Statistical Testing and Power Analysis

Per‑pair tests are underpowered at \(n = 5\) folds, so the primary inference aggregates across the 25 class pairs. A dedicated `utils/power_analysis.py` script explores power for the Wilcoxon signed‑rank test at the observed effect size (\(d \approx 0.65\)), showing the design reaches about **88% power** with 25 pairs.

### Reproducibility Infrastructure

Reproducibility is supported by deterministic file ordering, consistent seeding, pinned dependencies in the `Dockerfile`, and an 82‑test verification suite that runs at build time.

---

## Why Deeper Was Worse

I expected deeper circuits to help. The expressibility analysis showed more depth increased entanglement and expanded the reachable state space. But on 16 features, that capacity was wasted; it fitted noise. One layer, 32 parameters, was already generous. The circuit should match the information content, not your ambition.

---

## The Statistics Nearly Killed the Story

Most quantum ML papers report a single split and claim advantage. This project did the opposite: validation, power analysis, baseline comparisons, and per‑pair statistical reporting.

The per‑pair Wilcoxon tests were underpowered with 5 folds; the minimum achievable p‑value is 0.0625. If you only looked at per‑pair stats, you would conclude no difference.

The correct inference treats pairs as replication units. That is where the signal appears. It’s a cautionary lesson: the design is the experiment.

---

## Practical Reality: TFQ Only Works in Docker

TensorFlow Quantum depends on a fragile constellation of pinned versions (`tensorflow==2.7.0`, `cirq==0.13.1`, `sympy==1.8`, `numpy==1.21.6`). It does not install cleanly on modern machines without Docker. On Apple Silicon it runs under AMD64 emulation and needs thermal pacing to survive long runs.

So reproducibility lives in the Dockerfile, not the README. The image runs an 82‑test suite at build time. If the tests fail, the image doesn’t build. That is the only reproducibility that matters.

---

## What the Project Actually Tells Us

This is **not** quantum advantage. The comparison is against a deliberately hobbled classical model under severe compression. A ResNet at full resolution would obliterate both.

What it *does* show is how parameterized quantum circuits behave under extreme information bottlenecks:

- They can extract structure when tuned carefully.
- They compete in low‑class regimes under compression.
- Their inductive bias changes with depth, and over‑capacity appears quickly.
- They are interpretable via standard gradient tools.

That is scientifically useful, even if it is not headline‑worthy.

---

## Where This Goes Next

### Hardware Changes the Game

On real quantum hardware, 17 qubits is trivial. With 64 or 128 qubits, you can encode real spatial structure. The keyhole widens. The central question becomes: does the QNN advantage at \(k=2\) persist when compression is relaxed?

### Better Circuit Design

The circuits here are first drafts. Quantum conv nets, data re‑uploading, attention‑like entanglement, and deeper inductive biases are all open directions. The design space is huge and barely explored.

### Generative Quantum Models

Discriminative classification is only one angle. Quantum generative models could synthesize new examples for rare species. That’s where quantum sampling could matter.

### Hybrid Pipelines

One promising path: use the quantum circuit as a feature extractor feeding a classical head. Let the quantum model do low‑dimensional feature interactions; let the classical model handle multi‑class scaling.

---

## Closing

I built a seven‑phase experimental pipeline, a power analysis framework, and a reproducible Docker stack to classify plankton at `4x4` resolution. The QNN won 20 of 25 binary comparisons. It lost the multi‑class scaling contest. It produced interpretable saliency maps. It ran on a noiseless simulator because hardware isn’t ready.

Is this quantum advantage? No.
Is it scientifically informative? Yes.

The future of quantum ML is not a single paper. It’s slow, careful accumulation—circuit by circuit, dataset by dataset—until the hardware catches up and we find out what the exponential promise actually buys.

I’m betting it buys something. But I’m keeping my classical baselines close.
