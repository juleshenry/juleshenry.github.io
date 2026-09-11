#!/usr/bin/env python3
"""Figures for Back-of-the-Envelope: Primitive Sets."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1] / "blog" / "assets" / "2025" / "primitivos"
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


def primes_upto(n):
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = False
    return np.nonzero(sieve)[0]


# --- constants number line --------------------------------------------------
fig, ax = plt.subplots(figsize=(9.6, 2.6), facecolor=BG)
ax.set_facecolor(BG)
ax.set_xlim(1.32, 1.90)
ax.set_ylim(-0.85, 1.15)
ax.axis("off")
ax.plot([1.34, 1.88], [0, 0], color="#444", lw=1.6, zorder=0)
for x, lab, color, va, dy in [
    (1.399, r"$e^{\gamma}\pi/4$" + "\n" + r"$1.399$" + "\n(large-element bound)", PINK, "bottom", 0.18),
    (1.60, r"$2$ missing" + "\n" + r"$1.60$", CYAN, "top", -0.22),
    (1.6366, r"$f(\mathcal{P})$" + "\n" + r"$1.6366$", WHITE, "bottom", 0.18),
    (1.781, r"$e^{\gamma}$" + "\n" + r"$1.781$" + "\n(1935 / 2019)", MUTED, "top", -0.22),
]:
    ax.plot([x], [0], "o", color=color, ms=9, zorder=3)
    ax.plot([x, x], [0, 0.08 if va == "bottom" else -0.08], color=color, lw=1.2)
    ax.text(x, dy, lab, ha="center", va=va, color=color, fontsize=9)
ax.text(1.61, 1.05, "Four numbers that run the whole argument",
        ha="center", color=TEXT, fontsize=13)
save(fig, "constants.png")


# --- Mertens product --------------------------------------------------------
N = 4000
ps = primes_upto(N)
prod = np.ones_like(ps, dtype=float)
running = 1.0
for i, p in enumerate(ps):
    running *= (1 - 1 / p)
    prod[i] = running
gamma = 0.5772156649015329
xs = np.linspace(3, N, 600)
approx = np.exp(-gamma) / np.log(xs)

fig, ax = plt.subplots(figsize=(8.4, 4.2), facecolor=BG)
style(ax, r"Mertens: sieving primes up to $x$ leaves about $e^{-\gamma}/\log x$")
ax.step(ps, prod, where="post", color=CYAN, lw=1.8, label=r"$\prod_{p\leq x}(1-1/p)$")
ax.plot(xs, approx, color=PINK, lw=2.0, label=r"$e^{-\gamma}/\log x$")
ax.set_xscale("log")
ax.set_xlim(2, N)
ax.set_ylim(0, 0.55)
ax.set_xlabel("x", color=MUTED)
ax.set_ylabel("proportion remaining", color=MUTED)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT, fontsize=9)
save(fig, "mertens.png")


# --- v tradeoff -------------------------------------------------------------
v = np.linspace(1e-4, 1, 500)
conv = 1 / (1 + v)
pack = np.sqrt(v)
integrand = 1 / (2 * np.sqrt(v) * (1 + v))

fig, ax = plt.subplots(figsize=(8.4, 4.4), facecolor=BG)
style(ax, r"Discount $1/(1+v)$, packing $\sqrt{v}$, extra room $1/(2\sqrt{v}(1+v))$")
ax.plot(v, conv, color=CYAN, lw=2.2, label=r"conversion $1/(1+v)$")
ax.plot(v, pack, color=PINK, lw=2.2, label=r"packing cap $\sqrt{v}$")
ax.plot(v, integrand, color=WHITE, lw=2.0, label=r"integrand $1/(2\sqrt{v}\,(1+v))$")
ax.set_xlim(0, 1)
ax.set_ylim(0, 2.05)
ax.set_xlabel("v", color=MUTED)
ax.legend(facecolor=AXBG, edgecolor="#333", labelcolor=TEXT, fontsize=9)
ax.text(0.62, 1.55, "the white curve blows up at 0\nbut is still integrable",
        color=MUTED, fontsize=8)
save(fig, "v-tradeoff.png")


# --- arctan / quarter-circle ------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.2), facecolor=BG)

u = np.linspace(0, 1, 400)
y = 1 / (1 + u ** 2)
style(axes[0], r"after $u=\sqrt{v}$: area $\int_0^1 du/(1+u^2)$")
axes[0].plot(u, y, color=CYAN, lw=2.2)
axes[0].fill_between(u, y, color=CYAN, alpha=0.22)
axes[0].set_xlim(0, 1)
axes[0].set_ylim(0, 1.15)
axes[0].set_xlabel("u", color=MUTED)
axes[0].text(0.52, 0.62, r"$\pi/4$", color=WHITE, fontsize=16, ha="center")

# unit-circle reading: the number π/4 is an *angle*, not a sector area
ax = axes[1]
style(ax, r"the same number is the $45^\circ$ angle  ($\tan=\mathrm{opp}/\mathrm{adj}=1$)")
ax.set_aspect("equal")
ax.set_xlim(-0.2, 1.45)
ax.set_ylim(-0.2, 1.45)
ax.plot([-0.05, 1.25], [0, 0], color="#444", lw=1)
ax.plot([0, 0], [-0.05, 1.25], color="#444", lw=1)
circ = plt.Circle((0, 0), 1, fill=False, edgecolor=MUTED, lw=1.4)
ax.add_patch(circ)
theta = np.linspace(0, np.pi / 4, 40)
ax.plot(np.cos(theta), np.sin(theta), color=PINK, lw=2.4)
ax.plot([0, 1], [0, 0], color=CYAN, lw=1.8)
ax.plot([0, np.cos(np.pi / 4)], [0, np.sin(np.pi / 4)], color=PINK, lw=1.8)
# isosceles right triangle on the unit circle
ax.plot([1, 1], [0, 1], color=MUTED, lw=1.0, ls="--")
ax.plot([0, 1], [0, 1], color=PINK, lw=1.2, ls=":")
ax.plot([1], [0], "o", color=CYAN, ms=6)
ax.plot([1], [1], "o", color=PINK, ms=6)
ax.text(1.06, -0.12, r"$(1,0)$", color=CYAN, fontsize=9)
ax.text(1.06, 1.04, r"$(1,1)$", color=PINK, fontsize=9)
ax.annotate(r"$\pi/4$", xy=(0.22, 0.08), color=WHITE, fontsize=13)
ax.set_xticks([])
ax.set_yticks([])
for s in ax.spines.values():
    s.set_visible(False)

fig.suptitle(r"The tradeoff integrates to a quarter-turn: $\arctan 1=\pi/4$",
             color=TEXT, fontsize=13, y=1.03)
save(fig, "arctan.png")

print("done")
