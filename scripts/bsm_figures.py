#!/usr/bin/env python3
"""Extra figures for the Black–Scholes–Merton note."""
from pathlib import Path
from math import log, exp, sqrt, erf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

ROOT = Path(__file__).resolve().parents[1] / "blog" / "assets" / "2024" / "bsm"
BG, AXBG, TEXT, MUTED = "#0a0a0a", "#121212", "#e0e0e0", "#a0a0a0"
PINK, CYAN, WHITE = "#FFA7CC", "#00FFFF", "#ffffff"


def style(ax, title=None):
    ax.set_facecolor(AXBG)
    ax.tick_params(colors=MUTED, labelsize=9)
    for s in ax.spines.values():
        s.set_color("#333")
    if title:
        ax.set_title(title, color=TEXT, fontsize=13, pad=10)


def save(fig, name):
    ROOT.mkdir(parents=True, exist_ok=True)
    path = ROOT / name
    fig.savefig(path, dpi=160, facecolor=BG, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path)


# --- one-step tree ----------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.8, 4.8), facecolor=BG)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.2)
ax.set_axis_off()
ax.set_facecolor(BG)
ax.text(5, 5.85, "One step, two outcomes, one manufactured call",
        ha="center", color=TEXT, fontsize=14)


def node(x, y, lines, color):
    ax.add_patch(FancyBboxPatch((x - 1.35, y - 0.72), 2.7, 1.44,
                                boxstyle="round,pad=0.08,rounding_size=0.2",
                                facecolor=AXBG, edgecolor=color, lw=1.6))
    for i, line in enumerate(lines):
        ax.text(x, y + 0.38 - 0.38 * i, line, ha="center", va="center",
                color=TEXT, fontsize=10, fontfamily="monospace")


node(1.7, 3.0, ["S = 100", "C = 33.33", "Δ = 2/3 share"], CYAN)
node(7.8, 4.7, ["S = 200", "payoff = 100"], PINK)
node(7.8, 1.3, ["S = 50", "payoff = 0"], PINK)
ax.annotate("", xy=(6.35, 4.45), xytext=(3.15, 3.35),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))
ax.annotate("", xy=(6.35, 1.55), xytext=(3.15, 2.65),
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.5))
ax.text(4.7, 4.25, "×2", color=PINK, fontsize=11)
ax.text(4.7, 1.75, "×½", color=CYAN, fontsize=11)
ax.text(5, 0.35, r"$r=0$. Replicate: long $2/3$ of a share, borrow $33.33$. Drift never enters.",
        ha="center", color=MUTED, fontsize=10)
save(fig, "one-step-tree.png")


# --- quadratic variation, 4 steps ------------------------------------------
rng_steps = [
    [+1, +1, +1, +1],
    [+1, -1, +1, -1],
    [+1, +1, -1, -1],
    [-1, -1, -1, -1],
]
labels = ["HHHH  ends at +2", "HTHT  ends at  0", "HHTT  ends at  0", "TTTT  ends at −2"]
fig, axes = plt.subplots(2, 2, figsize=(9.2, 6.6), facecolor=BG)
dt = 0.25
step = 0.5
for ax, signs, lab in zip(axes.ravel(), rng_steps, labels):
    style(ax, lab)
    t = np.arange(5) * dt
    w = np.concatenate([[0], np.cumsum(np.array(signs) * step)])
    ax.plot(t, w, color=CYAN, lw=2.0, marker="o", ms=5)
    ax.set_ylim(-2.4, 2.4)
    ax.set_xlim(0, 1)
    qv = 4 * (step ** 2)
    ax.text(0.98, -2.15, rf"$\sum (\Delta W)^2 = {qv:.0f}$",
            ha="right", color=PINK, fontsize=10)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
fig.suptitle(r"Four coin-flip paths, $\Delta t=1/4$. Every one has quadratic variation 1.",
             color=TEXT, fontsize=13)
fig.tight_layout(rect=(0, 0, 1, 0.95))
save(fig, "quadratic-variation.png")


# --- call vs vol ------------------------------------------------------------
def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))


def bsm_call(S, K, r, sig, tau):
    if sig < 1e-12:
        return max(S - K * exp(-r * tau), 0.0)
    d1 = (log(S / K) + (r + 0.5 * sig ** 2) * tau) / (sig * sqrt(tau))
    d2 = d1 - sig * sqrt(tau)
    return S * Phi(d1) - K * exp(-r * tau) * Phi(d2)


sigs = np.linspace(0.0, 1.0, 201)
Cs = [bsm_call(100, 100, 0.05, s, 1.0) for s in sigs]
fig, ax = plt.subplots(figsize=(8.2, 4.4), facecolor=BG)
style(ax, r"ATM call vs volatility  ($S=K=100$, $r=5\%$, one year)")
ax.plot(sigs * 100, Cs, color=PINK, lw=2.4)
ax.axhline(4.877, color=MUTED, lw=0.9, ls="--")
ax.plot([20], [10.45], "o", color=CYAN, ms=8, zorder=5)
ax.annotate(r"the rain check: $\sigma=20\%$, $C\approx 10.45$",
            xy=(20, 10.45), xytext=(38, 8),
            color=CYAN, fontsize=10,
            arrowprops=dict(arrowstyle="->", color=CYAN, lw=1.1))
ax.text(55, 6.1, r"$\sigma=0$: just the forward, $4.88$",
        color=MUTED, fontsize=10)
ax.set_xlabel(r"volatility $\sigma$ (%)", color=MUTED)
ax.set_ylabel("call price", color=MUTED)
ax.set_xlim(0, 100)
ax.set_ylim(0, 45)
save(fig, "call-vs-vol.png")


# --- CRR n-step → BSM -------------------------------------------------------
from math import comb


def crr_call(S, K, r, sig, T, n):
    dt = T / n
    u = exp(sig * sqrt(dt))
    dwn = 1 / u
    p = (exp(r * dt) - dwn) / (u - dwn)
    disc = exp(-r * T)
    tot = 0.0
    for k in range(n + 1):
        ST = S * (u ** k) * (dwn ** (n - k))
        tot += comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) * max(ST - K, 0.0)
    return disc * tot


ns = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])
Cs = [crr_call(100, 100, 0.05, 0.20, 1.0, int(n)) for n in ns]
fig, ax = plt.subplots(figsize=(8.4, 4.4), facecolor=BG)
style(ax, r"Cox–Ross–Rubinstein tree $\to$ $10.45$")
ax.plot(ns, Cs, color=CYAN, lw=2.2, marker="o", ms=6, label="n-step tree")
ax.axhline(10.4506, color=PINK, lw=1.4, ls="--", label=r"BSM  $10.45$")
ax.set_xscale("log", base=2)
ax.set_xticks(ns)
ax.set_xticklabels([str(int(n)) for n in ns])
ax.set_xlabel("steps n", color=MUTED)
ax.set_ylabel("call price", color=MUTED)
ax.set_ylim(8.8, 12.6)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT)
ax.annotate(r"$n=1$:  $12.16$", xy=(1, 12.16), xytext=(3.2, 12.05),
            color=MUTED, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.9))
save(fig, "crr-convergence.png")


# --- Itô leftover on W^2, path HHHH -----------------------------------------
step = 0.5
dws = [step, step, step, step]
W = 0.0
rows_W = [0.0]
rows_2 = [0.0]
rows_ito = [0.0]
rows_qv = [0.0]
acc_ito = 0.0
acc_qv = 0.0
for dw in dws:
    acc_ito += 2 * W * dw
    acc_qv += dw * dw
    W += dw
    rows_W.append(W)
    rows_2.append(W * W)
    rows_ito.append(acc_ito)
    rows_qv.append(acc_qv)

t = np.arange(5) * 0.25
fig, ax = plt.subplots(figsize=(8.4, 4.4), facecolor=BG)
style(ax, r"Path HHHH:  $W^2$ vs  $\sum 2W\,\Delta W$")
ax.plot(t, rows_2, color=PINK, lw=2.3, marker="o", ms=6, label=r"$W_t^2$  (truth)")
ax.plot(t, rows_ito, color=CYAN, lw=2.3, marker="s", ms=5,
        label=r"$\sum 2W\,\Delta W$  (Calc 1)")
ax.fill_between(t, rows_ito, rows_2, color=PINK, alpha=0.18)
ax.text(0.38, 2.55, r"the gap is $\sum(\Delta W)^2 = 1$",
        color=PINK, fontsize=11)
ax.set_xlabel("t", color=MUTED)
ax.set_ylabel("dollars of $W^2$", color=MUTED)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT, loc="upper left")
ax.set_xlim(0, 1)
ax.set_ylim(-0.2, 4.4)
save(fig, "ito-square.png")


# --- Φ as area --------------------------------------------------------------
from math import pi
xs = np.linspace(-3.2, 3.2, 400)
dens = np.exp(-0.5 * xs ** 2) / np.sqrt(2 * pi)
fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.8), facecolor=BG)
for ax, cut, title, color in [
    (axes[0], 0.15, r"$\Phi(0.15)\approx 0.560$  =  $P(Z\leq 0.15)$", CYAN),
    (axes[1], 0.35, r"$\Phi(0.35)\approx 0.637$  =  $P(Z\leq 0.35)$", PINK),
]:
    style(ax, title)
    ax.plot(xs, dens, color=WHITE, lw=1.6)
    ax.fill_between(xs, dens, where=(xs <= cut), color=color, alpha=0.45)
    ax.axvline(cut, color=color, lw=1.2)
    ax.set_xlim(-3.2, 3.2)
    ax.set_ylim(0, 0.45)
    ax.set_xlabel("z", color=MUTED)
    ax.set_yticks([])
save(fig, "phi-areas.png")


# --- normal vs lognormal ----------------------------------------------------
from math import pi
xs = np.linspace(-20, 220, 600)
# N(100, 25^2) — a naive additive model
mu_n, sd_n = 100.0, 25.0
dens_n = np.exp(-0.5 * ((xs - mu_n) / sd_n) ** 2) / (sd_n * np.sqrt(2 * pi))
# Lognormal with median 100, s=0.25 so typical 25% log-vol
s_ln = 0.25
m_ln = np.log(100.0)
ys = np.linspace(0.1, 220, 600)
dens_ln = np.exp(-0.5 * ((np.log(ys) - m_ln) / s_ln) ** 2) / (ys * s_ln * np.sqrt(2 * pi))
fig, axes = plt.subplots(1, 2, figsize=(9.8, 3.8), facecolor=BG)
style(axes[0], r"additive:  $\mathcal{N}(100,25^2)$  goes negative")
axes[0].plot(xs, dens_n, color=WHITE, lw=1.7)
axes[0].fill_between(xs, dens_n, where=(xs < 0), color=PINK, alpha=0.55)
axes[0].axvline(0, color=PINK, lw=1.1, ls="--")
axes[0].set_xlim(-20, 220)
axes[0].set_ylim(0, 0.02)
axes[0].set_xlabel(r"$S_T$", color=MUTED)
axes[0].set_yticks([])
style(axes[1], r"multiplicative: lognormal,  $S_T>0$")
axes[1].plot(ys, dens_ln, color=CYAN, lw=1.7)
axes[1].fill_between(ys, dens_ln, color=CYAN, alpha=0.25)
axes[1].axvline(100, color=MUTED, lw=0.9, ls=":")
axes[1].set_xlim(0, 220)
axes[1].set_ylim(0, 0.02)
axes[1].set_xlabel(r"$S_T$", color=MUTED)
axes[1].set_yticks([])
fig.suptitle("A stock is a product of returns, not a sum of dollars",
             color=TEXT, fontsize=13, y=1.04)
save(fig, "normal-vs-lognormal.png")
