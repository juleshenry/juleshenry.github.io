---
layout: post
title: "Hacker de Teclado"
date: 2026-04-27
---

# [Hacker de Teclado: Acoustic Keyboard Side-Channel Attack with Deep Learning](https://github.com/juleshenry/hacker-de-audio-de-teclado)

Every key on your keyboard makes a slightly different sound when pressed. The spacebar sounds different from the Enter key. The 'A' key sounds different from the 'S' key -- subtly, but measurably. If you record the audio of someone typing and feed it through a trained neural network, you can reconstruct what they typed.

This project is a from-scratch reimplementation of Harrison, Toreini, and Mehrnezhad's 2023 paper "A Practical Deep Learning-Based Acoustic Side Channel Attack on Keyboards" ([arXiv:2308.01074](https://arxiv.org/abs/2308.01074)). Written in Portuguese-flavored Python, built on PyTorch and librosa.

The project is on [GitHub](https://github.com/juleshenry/hacker-de-audio-de-teclado). MIT licensed.

## The Pipeline

```mermaid
graph TD
    A[Raw Audio Recording] -->|librosa onset detection| B[Individual Keystroke Chunks]
    B -->|Mel Spectrogram| C[64x64 Spectral Images]
    C -->|Time-Shift Augmentation| D[Augmented Dataset]
    D -->|SpecAugment Masking| E[Masked Spectrograms]
    E -->|CoAtNet| F[36-Class Prediction: a-z, 0-9]
```

Three stages: collect data, train a classifier, run the attack.

### Stage 1: Data Collection

The interactive recorder (`quickstart.py`) walks you through pressing each key on your keyboard. For each of the 36 alphanumeric keys (a-z, 0-9), it prompts you, records a short clip via your microphone using `sounddevice`, auto-detects the keystroke onset in the audio, and saves the isolated keystroke as a `.wav` file in a per-key directory.

For quick experimentation without a physical keyboard, a synthetic data generator (`gerar_exemplo_zorro.py` -- "generate fox example") creates fake keystroke audio using decaying sine waves at distinct frequencies. Each key gets a unique base frequency, so the spectrograms are distinguishable even though the sounds are artificial. The full pipeline (train, predict) works on synthetic data, letting you test end-to-end in under a minute.

The demo phrase is **"o zorro e gris"** -- Portuguese for "the fox is grey."

### Stage 2: Training

The training pipeline faithfully reproduces the paper's methodology.

**Onset Detection.** librosa detects keystroke onsets in the audio using energy-based peak detection with a 300ms minimum distance filter (to prevent detecting the same keypress twice).

**Mel Spectrogram Extraction.** Each keystroke chunk is converted into a 64-band Mel spectrogram with 1024-point FFT and 225 hop length, producing a 64x64 spectral image. This is the feature representation: a 2D image where the x-axis is time, the y-axis is frequency (mel-scaled), and pixel intensity represents energy at that time-frequency bin.

**Data Augmentation.** Two techniques from the paper:

1. **Time-shift augmentation** -- each keystroke is speed-distorted by +/- 40% using `librosa.effects.time_stretch`, producing 2 augmented copies per sample. This teaches the model to be invariant to typing speed.
2. **SpecAugment** -- at training time, random rectangular masks are applied to the spectrogram (2 frequency masks and 2 time masks, each spanning 10% of the axis width). This is the same augmentation technique used in speech recognition (Park et al. 2019), and it prevents the model from overfitting to specific time-frequency patterns.

**The Model: CoAtNet.** The classifier is a CoAtNet (Convolutional + Attention Network) -- a hybrid architecture that combines the local feature extraction of convolutions with the global context modeling of self-attention:

1. **Stem.** Conv2D (1 -> 32 channels, stride 2) with BatchNorm and GELU activation. Halves spatial dimensions.
2. **MBConv Phase.** Two Mobile Inverted Bottleneck Convolution blocks, expanding to 64 then 128 channels. These are depth-wise separable convolutions with squeeze-and-excitation -- the same building blocks used in EfficientNet. They capture local spectral patterns: the frequency distribution of a single keystroke.
3. **Transformer Phase.** Two Transformer Encoder layers with 4-head self-attention (d_model=128, feedforward dimension 512). These capture global dependencies across the entire spectrogram: the temporal shape of the keystroke's decay envelope, the relationship between the initial attack and the subsequent resonance.
4. **Classification Head.** Adaptive 2D Average Pooling -> Fully Connected Linear layer -> 36-class output.

The MBConv blocks say "what does this keystroke look like locally?" The Transformer blocks say "what does the overall shape tell us?" Together, they classify each 64x64 spectrogram as one of 36 alphanumeric characters.

**Training Hyperparameters.** Adam optimizer with max LR 5e-4 and linear annealing over 1100 epochs. Batch size 16. 80/20 train/val split. Early stopping with patience of 50 epochs. Best model checkpointed to `keystroke_model_best.pth`.

The model supports Apple MPS (Metal), CUDA, and CPU fallback. On an M-series Mac, training completes in minutes.

### Stage 3: The Attack

```bash
python hacker_de_teclado.py --prever recording.wav
```

Given a recording of someone typing, the system:
1. Detects each keystroke onset using the same librosa pipeline
2. Extracts the 64x64 Mel spectrogram for each detected keystroke
3. Runs each spectrogram through the trained CoAtNet
4. Outputs the predicted text: `o z o r r o e g r i s`

## Why This Works

It seems implausible that a microphone across the room could distinguish 'A' from 'S'. But the acoustic differences are real and arise from physical properties:

**Key position.** Keys in different positions on the keyboard produce different resonance patterns because the mechanical structure beneath them varies. A key near the edge of the keyboard plate has different vibrational modes than a key near the center.

**Finger angle.** Different keys are typically struck by different fingers at different angles. The ring finger hitting 'A' produces a different impact profile than the index finger hitting 'J'.

**Travel distance.** Adjacent keys have slightly different travel distances and spring tensions due to manufacturing tolerances, wear patterns, and the geometry of the underlying switch mechanism.

These differences are tiny -- inaudible to a human listener comparing two keystrokes -- but they are consistent and repeatable. A Mel spectrogram captures them as subtle variations in the frequency distribution of the keystroke's initial attack and subsequent decay. The CoAtNet learns to detect these patterns.

The Harrison et al. paper reports 95% accuracy on a MacBook Pro keyboard using a smartphone microphone placed nearby. The accuracy degrades with distance, ambient noise, and different keyboard models (the model trained on one keyboard does not transfer well to another, because the acoustic properties are hardware-specific).

## The Security Implications

This is a real attack vector. If someone can record the audio of your typing -- via a compromised microphone, a nearby phone, or even a video call where keyboard sounds leak through -- they can potentially reconstruct your keystrokes. Passwords, emails, code, messages.

Defenses include:
- **Acoustic noise injection** -- playing white noise near the keyboard to mask keystroke sounds
- **Silent keyboards** -- membrane keyboards produce weaker acoustic signatures than mechanical ones
- **Software-based keystroke randomization** -- introducing random delays between keystrokes to disrupt the temporal patterns
- **Awareness** -- muting your microphone during video calls when typing sensitive information

The project is educational. It demonstrates that the attack is accessible (PyTorch + librosa + a microphone), reproducible (the synthetic data generator lets anyone test the pipeline), and frighteningly effective on controlled setups. The paper it reimplements is publicly available. The code is MIT licensed. The fox is grey.
