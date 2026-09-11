#!/usr/bin/env python3
"""Figures for the deepened Back-of-the-Envelope ML notes."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1] / "blog" / "assets" / "2024"
BG, AXBG, TEXT, MUTED = "#0a0a0a", "#121212", "#e0e0e0", "#a0a0a0"
PINK, CYAN, WHITE = "#FFA7CC", "#00FFFF", "#ffffff"

cmap = LinearSegmentedColormap.from_list(
    "bote", ["#0a0a0a", "#1a3a4a", CYAN, PINK, WHITE]
)
pink_cyan = LinearSegmentedColormap.from_list("pc", ["#0a0a0a", PINK, WHITE])


def style(ax, title=None):
    ax.set_facecolor(AXBG)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ax.spines.values():
        s.set_color("#333")
    if title:
        ax.set_title(title, color=TEXT, fontsize=13, pad=10)


def save(fig, rel):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=160, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# --- CNN: 2d6 convolution ---------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(11.2, 3.6), facecolor=BG)
die = np.full(6, 1 / 6)
two = np.convolve(die, die)
for ax, ys, title, color in [
    (axes[0], die, r"one die  $P_X$", CYAN),
    (axes[1], die, r"one die  $P_Y$", PINK),
    (axes[2], two, r"$P_X * P_Y$  (two dice)", WHITE),
]:
    style(ax, title)
    xs = np.arange(1, 1 + len(ys))
    ax.bar(xs, ys, color=color, edgecolor="#000", width=0.84, alpha=0.92)
    ax.set_xticks(xs)
    ax.set_ylim(0, 0.22)
    ax.set_xlabel("face / sum", color=MUTED, fontsize=9)
axes[2].set_xticks(range(2, 13))
fig.suptitle("Convolution is how independent random variables add",
             color=TEXT, fontsize=14, y=1.04)
save(fig, "cnn/dice-convolution.png")


# --- CNN: square + edge kernel ----------------------------------------------
img = np.zeros((8, 8))
img[2:6, 2:6] = 1.0
K = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], dtype=float)
out = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        out[i, j] = np.sum(img[i:i + 3, j:j + 3] * K)

fig, axes = plt.subplots(1, 3, figsize=(10.4, 3.5), facecolor=BG)
for ax, M, title, cm in [
    (axes[0], img, "a handmade square", "gray"),
    (axes[1], K, r"edge kernel  (sums to 0)", cmap),
    (axes[2], out, "response: only the boundary fires", cmap),
]:
    style(ax, title)
    im = ax.imshow(M, cmap=cm, interpolation="nearest")
    ax.set_xticks(range(M.shape[1]))
    ax.set_yticks(range(M.shape[0]))
    for (r, c), val in np.ndenumerate(M):
        ax.text(c, r, f"{val:.0f}", ha="center", va="center",
                color="#111" if abs(val) > 3 else TEXT, fontsize=8)
fig.suptitle("A kernel is a question in nine numbers",
             color=TEXT, fontsize=14, y=1.03)
save(fig, "cnn/square-edge.png")


# --- CNN: receptive field ---------------------------------------------------
fig, ax = plt.subplots(figsize=(10.6, 3.8), facecolor=BG)
ax.set_xlim(0, 16)
ax.set_ylim(0, 5)
ax.set_axis_off()
ax.set_facecolor(BG)
stages = [
    (0.4, "input pixel", 1, CYAN),
    (4.0, "after 3×3 conv\nRF = 3", 3, PINK),
    (8.0, "after 2×2 pool\nRF = 4", 4, CYAN),
    (12.2, "after 3×3 conv\nRF = 8", 8, PINK),
]
ax.text(8, 4.6, "Receptive field: how much input one cell can see",
        ha="center", color=TEXT, fontsize=13)
for x, label, rf, color in stages:
    size = 0.28 * rf
    ax.add_patch(Rectangle((x, 1.6), size, size, fill=True,
                           facecolor=color, alpha=0.35, edgecolor=color, lw=1.6))
    ax.plot([x + size / 2], [1.6 + size / 2], "o", color=color, ms=5)
    ax.text(x + size / 2, 0.55, label, ha="center", va="top",
            color=TEXT, fontsize=9)
    if x < 12:
        ax.annotate("", xy=(x + size + 0.45, 2.4),
                    xytext=(x + size + 0.05, 2.4),
                    arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4))
save(fig, "cnn/receptive-field.png")


# --- RNN: vanishing vs LSTM highway -----------------------------------------
T = np.arange(0, 41)
vanilla = (0.5 * 0.9) ** T
lstm_leaky = (0.9) ** T
lstm_copy = np.ones_like(T, dtype=float)
fig, ax = plt.subplots(figsize=(8.6, 4.2), facecolor=BG)
style(ax, "How much of step 0 is still alive at step t")
ax.plot(T, vanilla, color=PINK, lw=2.4, label=r"vanilla  $(0.5 \times 0.9)^t$")
ax.plot(T, lstm_leaky, color=CYAN, lw=2.4, label=r"LSTM forget $f=0.9$   $0.9^t$")
ax.plot(T, lstm_copy, color=WHITE, lw=1.8, ls="--", label=r"LSTM forget $f=1$   copy")
ax.set_yscale("log")
ax.set_xlabel("t", color=MUTED)
ax.set_ylabel("surviving gradient", color=MUTED)
ax.set_xlim(0, 40)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT, fontsize=9)
ax.axhline(1e-3, color="#333", lw=0.8)
save(fig, "rnn/vanish-vs-highway.png")


# --- RNN: tanh and its derivative -------------------------------------------
z = np.linspace(-4, 4, 400)
th = np.tanh(z)
thp = 1 - th ** 2
fig, ax = plt.subplots(figsize=(7.4, 4.0), facecolor=BG)
style(ax, r"$\tanh$ saturates; its derivative never exceeds 1")
ax.plot(z, th, color=CYAN, lw=2.3, label=r"$\tanh z$")
ax.plot(z, thp, color=PINK, lw=2.3, label=r"$1-\tanh^2 z$")
ax.axhline(1, color=MUTED, lw=0.7, ls=":")
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT)
ax.set_xlabel("z", color=MUTED)
save(fig, "rnn/tanh-derivative.png")


# --- RAG: sequence vs token on two answers ----------------------------------
labels = ["faithful\n'born Hawaii'", "Frankenstein\n'Chicago Hawaii'"]
seq = [0.516, 0.065]
tok = [0.449, 0.090]
x = np.arange(len(labels))
w = 0.36
fig, ax = plt.subplots(figsize=(7.6, 4.2), facecolor=BG)
style(ax, "RAG-Sequence commits; RAG-Token will stitch")
ax.bar(x - w / 2, seq, w, color=CYAN, label="RAG-Sequence", edgecolor="#000")
ax.bar(x + w / 2, tok, w, color=PINK, label="RAG-Token", edgecolor="#000")
ax.set_xticks(x)
ax.set_xticklabels(labels, color=TEXT)
ax.set_ylabel(r"$p(y \mid x)$", color=MUTED)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT)
for i, (s, t) in enumerate(zip(seq, tok)):
    ax.text(i - w / 2, s + 0.012, f"{s:.3f}", ha="center", color=CYAN, fontsize=9)
    ax.text(i + w / 2, t + 0.012, f"{t:.3f}", ha="center", color=PINK, fontsize=9)
ax.set_ylim(0, 0.62)
save(fig, "rag/seq-vs-token.png")


# --- RAG: prior vs posterior over documents ---------------------------------
fig, ax = plt.subplots(figsize=(7.2, 4.0), facecolor=BG)
style(ax, r"An answer updates the document posterior  $p(z\mid x,y)$")
docs = ["Hawaii passage", "Chicago passage"]
prior = [0.70, 0.30]
post = [0.63 / 0.69, 0.06 / 0.69]
x = np.arange(2)
w = 0.36
ax.bar(x - w / 2, prior, w, color=CYAN, label=r"$p(z\mid x)$  retriever", edgecolor="#000")
ax.bar(x + w / 2, post, w, color=PINK, label=r"$p(z\mid x,y{=}\mathrm{Hawaii})$", edgecolor="#000")
ax.set_xticks(x)
ax.set_xticklabels(docs, color=TEXT)
ax.set_ylim(0, 1.05)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT, fontsize=9)
ax.set_ylabel("probability", color=MUTED)
save(fig, "rag/prior-posterior.png")


# --- Attention: "not good" heatmap ------------------------------------------
# Causal self-attention on ["not","good"] constructed so "good" looks at "not".
Q = np.array([[0.0, 1.0],
              [1.0, 0.0]])
K = np.array([[1.0, 0.0],
              [0.0, 1.0]])
V = np.array([[-2.0, 0.0],   # "not" contributes a negation
              [0.0, 2.0]])   # "good" contributes positive
scores = Q @ K.T / np.sqrt(2)
mask = np.triu(np.ones((2, 2), dtype=bool), k=1)
scores_masked = scores.copy()
scores_masked[mask] = -1e9

def sm(x):
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)

A = sm(scores_masked)
out = A @ V
print("ATTN scores\n", scores)
print("ATTN A\n", A)
print("ATTN out\n", out)

def cell_text_color(val, vmin, vmax):
    t = (val - vmin) / (vmax - vmin + 1e-9)
    return "#111" if t > 0.62 else WHITE


fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.6), facecolor=BG)
tok = ["not", "good"]
panels = [
    (axes[0], scores, r"scores  $QK^\top/\sqrt{d_k}$", -0.2, 0.8, "key", True),
    (axes[1], A, "causal attention weights", 0, 1, "key", True),
    (axes[2], out, "mixed values  (negation, polarity)", -2.2, 2.2, "dim", False),
]
for ax, M, title, vmin, vmax, xlab, use_tok_x in panels:
    style(ax, title)
    ax.imshow(M, cmap=cmap, vmin=vmin, vmax=vmax)
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    ax.set_xticklabels(tok if use_tok_x else ["neg", "pos"], color=TEXT)
    ax.set_yticklabels(tok, color=TEXT)
    ax.set_xlabel(xlab, color=MUTED, fontsize=9)
    ax.set_ylabel("query", color=MUTED, fontsize=9)
    for (r, c), val in np.ndenumerate(M):
        ax.text(c, r, f"{val:.2f}", ha="center", va="center",
                color=cell_text_color(val, vmin, vmax), fontsize=10)
fig.suptitle('"good" is allowed to look at "not". That is the whole joke.',
             color=TEXT, fontsize=13, y=1.04)
save(fig, "attention/not-good.png")


# --- Attention: causal mask -------------------------------------------------
n = 8
tri = np.tril(np.ones((n, n)))
fig, ax = plt.subplots(figsize=(4.8, 4.6), facecolor=BG)
style(ax, "Causal mask: the future is −∞")
ax.imshow(tri, cmap=LinearSegmentedColormap.from_list("m", ["#1a1a1a", CYAN]))
ax.set_xlabel("key  →  (later)", color=MUTED)
ax.set_ylabel("query  →  (later)", color=MUTED)
ax.set_xticks(range(n)); ax.set_yticks(range(n))
save(fig, "attention/causal-mask.png")


# --- Attention: positional sinusoids ----------------------------------------
d, npos = 32, 48
pos = np.arange(npos)[:, None]
i = np.arange(d // 2)[None, :]
div = 10000 ** (2 * i / d)
PE = np.zeros((npos, d))
PE[:, 0::2] = np.sin(pos / div)
PE[:, 1::2] = np.cos(pos / div)
fig, ax = plt.subplots(figsize=(8.8, 4.4), facecolor=BG)
style(ax, "Sinusoidal positional encodings  (32 dimensions)")
im = ax.imshow(PE.T, aspect="auto", cmap=cmap, interpolation="nearest")
ax.set_xlabel("position t", color=MUTED)
ax.set_ylabel("dimension", color=MUTED)
cb = fig.colorbar(im, ax=ax, fraction=0.03)
cb.ax.yaxis.set_tick_params(color=MUTED)
plt.setp(cb.ax.yaxis.get_ticklabels(), color=MUTED)
save(fig, "attention/positional-sines.png")


# --- Attention: why we scale ------------------------------------------------
rng = np.random.default_rng(0)

def max_softmax_hist(d_k, n=4000):
    # q,k ~ N(0,1)^{d_k}, score = q·k / scale
    q = rng.normal(size=(n, d_k))
    k = rng.normal(size=(n, d_k))
    raw = np.sum(q * k, axis=1)
    scaled = raw / np.sqrt(d_k)
    # softmax over a fake row of 8 keys, one of them is this score, rest N(0, var)
    # simpler: look at |score| distribution
    return raw, scaled

raw64, sc64 = max_softmax_hist(64)
raw4, sc4 = max_softmax_hist(4)
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8), facecolor=BG)
style(axes[0], r"unscaled $q^\top k$   ($d_k=64$)")
style(axes[1], r"scaled $q^\top k / \sqrt{d_k}$")
axes[0].hist(raw64, bins=40, color=PINK, edgecolor="#000", density=True)
axes[1].hist(sc64, bins=40, color=CYAN, edgecolor="#000", density=True)
axes[0].set_xlim(-40, 40)
axes[1].set_xlim(-40, 40)
for ax in axes:
    ax.set_xlabel("score", color=MUTED)
    ax.set_ylabel("density", color=MUTED)
fig.suptitle("Without the scale, softmax sees a one-hot and dies",
             color=TEXT, fontsize=13, y=1.03)
save(fig, "attention/why-scale.png")


print("\n--- numbers for the posts ---")
print("2d6:", {k: round(v, 4) for k, v in zip(range(2, 13), two)})
print("edge out max", out.max(), "min", out.min())

# RNN 1-unit walk
wx, wh = 1.0, 0.5
xs = [1.0, 0.0, 1.0]
h = 0.0
hs = []
for t, x in enumerate(xs, 1):
    h = np.tanh(wx * x + wh * h)
    hs.append(float(h))
    print(f"h_{t} = tanh({wx}*{x} + {wh}*h) = {h:.4f}")

# RAG numbers already printed conceptually
print("posterior Hawaii", 0.63 / 0.69, 0.06 / 0.69)
