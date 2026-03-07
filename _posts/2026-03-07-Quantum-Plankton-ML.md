---
layout: post
title: "Quantum Plankton ML"
date: 2026-03-07
---

# Quantum Plankton Machine Learning: Stress‑Testing Quantum Models Under Extreme Compression

Quantum machine learning is often presented through glossy benchmarks and sweeping claims, but many of those results lean on generous input resolutions, large parameter budgets, or forgiving evaluation protocols.[web:13][web:16][web:19] **Quantum Plankton Machine Learning** takes the opposite path: it asks how a carefully designed quantum model behaves when those advantages are deliberately taken away.

The repository proceeds in two stages. First, it reproduces an MNIST‑based quantum image‑classification demo. Second, it turns to lake zooplankton images derived from *Deep Learning Classification of Lake Zooplankton* by Kyathanahally et al. (Eawag, 2021), using them as a structured testbed for compressed quantum and classical models.[web:13][web:16][web:19] Throughout, the focus is on controlled comparisons, explicit statistics, and understanding the circuit itself—not on claiming an unconstrained “quantum advantage.”

---

## What the Study Actually Asks

The central question is narrow but meaningful: if you force both quantum and classical models to operate under the same brutal information bottleneck and similar parameter budgets, how do they behave?

Instead of feeding high‑resolution plankton imagery into a deep CNN, the project constrains everything to a `4x4` grayscale encoding. Sixteen pixels become sixteen data qubits, and all later experiments run in a 17‑qubit simulation regime (16 data + 1 readout). In that world, the most honest comparison is not against a full‑scale ResNet, but against classical baselines trained on exactly the same compressed signal.

The README is explicit about scope. The repository **does not** claim that current quantum models beat modern high‑resolution vision systems on the original zooplankton benchmark.[web:13][web:16][web:19] Any such statement would require much richer inputs, stronger classical architectures, and realistic quantum noise models. Instead, the study should be read as a careful investigation of compressed‑representation learning, statistical comparison, and circuit characterization in a tractable quantum‑simulation setting.

---

## From MNIST Reproduction to Plankton Classification

The repository is organized as a progression of phases, moving from reproduction to controlled comparison and then to interpretability and circuit‑level analysis.

### Phase 1 – MNIST Reproduction

Phase 1 recreates a published quantum MNIST notebook and checks that the original demonstration behaves as reported. This gives a baseline workflow before touching biological data and ensures that the quantum tooling and simulation stack are set up correctly.

### Phase 2 – Binary Quantum Classification

Phase 2 implements the first plankton‑focused model in `phase2/binary_quantum_classifier.py`. Grayscale plankton images are downsampled to a `4x4` representation, normalized, and flattened into a 16‑dimensional feature vector, which is then encoded into a parameterized quantum circuit.

Key elements include:

- **Angle encoding** of pixel intensities as \(Ry(\pi x_i)\) rotations, preserving grayscale information instead of thresholding it away.  
- A **hybrid classical–quantum pipeline** in which classical preprocessing feeds a TensorFlow Quantum model.  
- **5‑fold stratified cross‑validation**, deterministic fold seeding, and **bootstrap 95% confidence intervals**.  

The initial results (mean accuracy around 38% with a 95% CI of roughly \([35.49\%, 42.50\%]\)) highlight the difficulty of the setting and motivate more careful hyperparameter tuning.

### Phase 3 – Hyperparameter Optimization

Phase 3 introduces a nested cross‑validation scheme in `phase3/optimize_binary_classifier.py`. The outer loop provides an unbiased performance estimate, while the inner loop selects hyperparameters without touching held‑out test folds.

The tuned configuration arrives at:

- **Encoding**: Angle  
- **PQC layers**: 1 (deeper circuits showed signs of over‑parameterization on small `4x4` inputs)  
- **Learning rate**: 0.01  
- **Batch size**: 16  
- **Loss**: Hinge (compatible with \([-1, 1]\) expectation outputs)  

Under this setup, the binary QNN exceeds 60% accuracy on several biologically distinct plankton pairs, with some pairs (for example, diaphanosoma vs diatom_chain) reaching above 90%. These results show that even under severe compression, the quantum model can extract meaningful structure when the configuration is tuned appropriately.

### Phase 4 – Classical Comparison

Phase 4 is the scientific center of gravity. Rather than comparing against full‑resolution deep learning, it asks a narrower question: how does a binary QNN constrained to a `4x4` representation compare with a **parameter‑matched** classical model and with the compressed feature‑based baselines implied by the EAWAG study?[web:13][web:16][web:19]

The design uses:

- **25 binary plankton pairs** chosen from classes with at least 80 images, excluding ambiguous categories like `unknown`, `dirt`, `fish`, and `filament`.  
- Equalized sample budgets via the `Q_SAMPLES` parameter, applied uniformly across models.  
- QNN and classical accuracies per pair, alongside p‑values and a conservative “significant?” flag.  

Per‑pair tests are intentionally reported with caution: with only five folds per pair, individual pairwise tests are underpowered. The primary inference instead treats class pairs as replication units and analyzes the distribution of pairwise accuracy differences (QNN − Fair Classical).

The aggregate Phase 4 summary reports:

- **Mean delta (QNN − Fair)**: +6.23%  
- **Standard deviation of delta**: 8.83%  
- **Effect size (Cohen’s d)**: 0.705  
- **One‑sample t‑test p**: 0.0017  
- **Wilcoxon signed‑rank p**: 0.0007  
- **QNN wins**: 20 / 25 pairs  
- **Classical wins**: 5 / 25 pairs  

Under the severe `4x4` constraint, this suggests that the QNN can remain competitive and often slightly outperform a matched classical baseline across many binary tasks, even though it is not designed to beat high‑resolution CNNs on the original benchmark.

### Phase 5 – Multi‑Class Scaling

Phase 5 extends the experiments to \(k\)‑class classification with \(k \in \{2, 3, 4, 5, 8, 12, 16\}\). Both quantum and classical models operate on a shared **PCA‑compressed 16‑dimensional representation**, and the focus is on how performance degrades as the number of categories increases.

Representative scaling results:

| K (Categories) | QNN (PCA 16) | Fair Classical (PCA 16) |
| --- | --- | --- |
| 2 | 71.0% | 68.8% |
| 3 | 54.5% | 55.6% |
| 4 | 46.1% | 47.8% |
| 5 | 37.8% | 40.5% |
| 8 | 30.2% | 31.8% |
| 12 | 23.4% | 25.7% |
| 16 | 18.3% | 21.7% |

At low class counts, the QNN remains competitive, slightly edging out the classical baseline at \(k = 2\). As the number of categories increases, the classical learner generally becomes more favorable, which is exactly the regime where subtle class boundaries and limited information interact most strongly.

Again, the README emphasizes that these results are **scientifically** informative under compression but do not constitute a realistic proxy for production‑grade, high‑resolution plankton recognition.

### Phases 6 & 7 – Saliency, Expressibility, and Entanglement

The final phases add interpretability and circuit‑level analysis:

- **Phase 6 – Quantum saliency**  
  Introduces gradient‑based saliency maps for the quantum model, showing which `4x4` input regions most influence the decision function. The analysis suggests that the QNN often attends to localized morphological cues, and that the hybrid pipeline remains differentiable end‑to‑end, making saliency practical as a diagnostic.

- **Phase 7 – Expressibility and entanglement**  
  Studies the full **17‑qubit production PQC**, computing Meyer–Wallach entanglement and expressibility (KL divergence from a Haar reference) with bootstrap 95% confidence intervals. Increasing depth is observed to reduce the KL divergence and increase global entanglement, providing a circuit‑level rationale for how depth reshapes the reachable state space.

---

## How the Quantum Model Is Built

At the architectural level, the classifier is intentionally simple but scientifically motivated.

1. **Classical preprocessing**  
   - Start from `16x16` grayscale plankton images.  
   - Downsample to `4x4`.  
   - Apply min–max normalization.  
   - Flatten to a 16‑dimensional feature vector.

2. **Angle encoding and entanglement**  
   - Encode each normalized pixel intensity \(x_i\) as an \(Ry(\pi x_i)\) rotation on a corresponding data qubit.  
   - Use a linear chain of `CZ` gates to capture spatial correlations across the `4x4` grid.  
   - Add parameterized `XX`, `ZZ`, and `YY` interactions tying data qubits to a readout qubit.

3. **Readout and loss**  
   - Measure the ancilla/readout qubit in the \(Z\) basis and interpret the expectation value as a continuous score.  
   - Optimize with hinge loss, which matches the \([-1, 1]\) output range and works naturally with binary labels.

This structure is implemented in TensorFlow Quantum, running entirely on a classical simulator. The later expressibility and entanglement analyses directly reference this production circuit, so the performance numbers and circuit metrics are aligned.

---

## Statistical Design, Power, and Reproducibility

A standout feature of the repository is how seriously it treats experimental design and reproducibility.

### Cross‑Validation and Sampling

- **Phases 2, 4, 6** use stratified 5‑fold cross‑validation, reporting mean ± standard deviation and bootstrap 95% confidence intervals.  
- **Phases 3, 5** use nested cross‑validation (5 outer, 3 inner folds) so that hyperparameter selection and final evaluation remain cleanly separated.  
- The `Q_SAMPLES` parameter enforces equalized sample budgets across models, preventing data exposure from confounding the comparison.

Majority‑class and random baselines are reported so that model accuracies are always interpreted relative to meaningful null references.

### Statistical Testing and Power Analysis

Per‑pair statistical tests in Phase 4 are included for transparency but are explicitly labeled as underpowered at `n = 5` folds. The primary inference instead aggregates over the 25 class pairs.

A dedicated `utils/power_analysis.py` script explores how power scales with the number of pairs for a Wilcoxon signed‑rank test at an effect size near the pilot‑observed value (Cohen’s \(d \approx 0.65\)). The design with 25 pairs achieves around **88% power**, making the aggregate QNN versus classical comparison statistically robust.

### Reproducibility Infrastructure

Reproducibility is supported at multiple levels:

- Deterministic file ordering, with sorted directory listings.  
- Consistent seeding (`42 + fold_id`) across `numpy`, TensorFlow, and Python’s `random`.  
- Pinned package versions in the `Dockerfile`.  
- An 82‑test verification suite spanning Phases 2–7, plus smoke tests and rigor tests per phase.  
- JSON configuration dumps and structured CSV/JSON result artifacts in each `results` directory.

The README also documents practical concerns like AMD64 emulation on Apple Silicon, exposing pacing controls (`TF_THREADS`, `EPOCH_COOL`, `THERMAL_SLEEP`) so that long runs can be thermally safe without changing the scientific design.

---

## Running and Extending the Experiments

The repository is built around Docker to make the environment as close to “one‑command reproducible” as possible.

Typical workflows include:

- **Build the environment**  
  ```bash
  docker build --platform linux/amd64 -t quantum-plankton .

