---
layout: post
title: "Back-of-the-Envelope: Black-Scholes-Merton"
date: 2024-07-24
categories: wealth
mathjax: true
---

Is it optional to know what an option is? No.

This note takes someone who can do calculus, differential equations, and a stats course, and builds the Black–Scholes–Merton formula in seven stages. No finance and no stochastic calculus are assumed; both are built. We take the stages in order.

<div class="note">
<p><strong>Roadmap</strong></p>
<ol>
<li><strong>What is an option?</strong> A rain check: the right to buy at a strike. Payoff at expiry is arithmetic. Today's premium is the question.</li>
<li><strong>Martingales, Wiener, stocks.</strong> A Wiener process (Brownian motion) is the noise. A martingale is a fair game. A stock is the ODE $dS=\mu S\,dt$ plus that noise, scaled by $S$ so the price stays positive.</li>
<li><strong>Lognormal properties.</strong> Multiplicative returns add in log space; the CLT makes $\ln S_T$ Gaussian. Density, Jacobian, median versus mean, $\mathbb{E}[e^{aZ}]=e^{a^2/2}$.</li>
<li><strong>A simple calculus argument.</strong> Given that lognormal, completing the square turns $\mathbb{E}[(S_T-K)^+]$ into two $\Phi$'s, in parameters $(m,s)$. Then each assumption is perturbed: what morphs the formula, and what breaks it.</li>
<li><strong>A detour to Japan.</strong> Ordinary calculus throws $(dW)^2$ away. Itô keeps it. Quadratic variation, Taylor in two variables, $d(W^2)=2W\,dW+dt$.</li>
<li><strong>Derive from stochastic calculus.</strong> Itô on $\ln S$ produces the lognormal with $m=\ln S+(\mu-\tfrac12\sigma^2)\tau$. Replication (a two-leaf tree) and Girsanov replace $\mu$ by $r$. Plug in: the rain check is $10.45$. The PDE is the same Gaussian, as heat.</li>
<li><strong>Change of numeraire.</strong> $\Phi(d_2)$ is exercise probability in dollars. $\Phi(d_1)$ is exercise probability in shares. One more Girsanov, tilt $-\sigma$.</li>
</ol>
</div>

- [1. What is an option?](#1-what-is-an-option)
- [2. Martingales, Wiener, stocks](#2-martingales-wiener-stocks)
- [3. Lognormal properties](#3-lognormal-properties)
- [4. A simple calculus argument](#4-a-simple-calculus-argument)
- [5. A detour to Japan](#5-a-detour-to-japan)
- [6. Derive from stochastic calculus](#6-derive-from-stochastic-calculus)
- [7. Change of numeraire](#7-change-of-numeraire)
- [Limitations](#limitations)
- [References](#references)

The change-of-numeraire calculation follows Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. The original host is gone. A copy is [here](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf); the [Wayback capture of 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf) is the provenance.

---

# 1. What is an option?
{: #1-what-is-an-option}

In ordinary English, optional means you do not have to. In finance that is almost the definition.

An **option** is a contract that gives its owner the *right*, and not the obligation, to buy or sell something at a pre-agreed price. The something is the **underlying** — a share of stock, a bushel of wheat. The pre-agreed price is the **strike**, written $K$. The deadline is **expiry**, written $T$. For that right you pay money up front, the **premium**. The rest of this note is the question: what must the premium be?

You already know the everyday version. A rain check that lets you buy a TV at today's price next month is a call option on the TV. If the store drops the price, you ignore the rain check and buy cheaper. If the store raises the price, you use the rain check. You will only exercise when it helps you. That one-sidedness is the whole point.

## Calls and puts

A **call** is the right to *buy* the underlying at the strike. It pays you when the underlying finishes *above* $K$. A **put** is the right to *sell* the underlying at the strike. It pays you when the underlying finishes *below* $K$.

Every contract has two sides. The **buyer** (the **holder**, **long** the option) pays the premium today and owns the right. The **seller** (the **writer**, **short** the option) *captures* that premium today and takes on the matching **obligation**. Whatever the buyer can choose to do, the writer can be forced to do. The buyer's profit is the writer's loss, dollar for dollar.

To see the cash move, fix a working premium of $10$. We do not yet know whether $10$ is the *right* price — that is the rest of the note — but we need a number to subtract. A stock trades at $100$ today. Strike $K=100$, expiry in one year.

### The call buyer

You pay $10$ today. One year later the stock is at $S_T$.

- If $S_T=130$, you **exercise**. The writer must sell you the share at $100$. You now hold something worth $130$ that you paid $100$ for, so the contract paid $30$. Subtract the $10$ you already spent: **net $+20$**. Or: buy at $100$ via the call, immediately sell in the open market at $130$.
- If $S_T=80$, exercising would mean paying $100$ for a share worth $80$. You are not required to be that foolish. You let the ticket expire. The $10$ is gone. **Net $-10$**.
- If $S_T=100$, exercising gains you nothing. You walk away. **Net $-10$**.

Unlimited upside (the stock can in principle go to the moon). Limited downside (the worst case is losing the premium). That is why people buy calls.

### The call writer

Someone took the other side. They received your $10$ today and promised: if you choose to buy at $100$, I *must* sell at $100$.

- If $S_T=80$ or $S_T=100$, the buyer walks away. You keep the $10$. **Net $+10$**. Collect premium, option expires worthless: the writer's dream.
- If $S_T=130$, the buyer knocks. You must sell a $130$ share for $100$.
  - If you already owned the share (**covered call**): you hand it over at $100$ instead of selling it in the market at $130$. You missed $30$ of upside, but you had pocketed $10$, so **net $-20$**.
  - If you did not own it (**naked call**): you buy at $130$, sell to the buyer at $100$, lose $30$, offset by the $10$. **Net $-20$**.

Limited upside (the premium is the most you can make). Unlimited downside (the stock can go to the moon, and you still have to sell at $100$). Writing naked calls is a dangerous way to “collect premium.” A covered call is the version to picture first: you already own the stock, you are willing to let it get called away, and the premium is extra income if it does not.

Break-even for both sides is $S_T=110$: the stock has to rally $10$ just to recoup the $10$ you paid (or, for the writer, that is where the obligation starts to eat the premium).

<table>
  <thead>
    <tr>
      <th>\(S_T\)</th>
      <th>Call buyer (paid 10)</th>
      <th>Call writer (captured 10)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>70</td><td>expires, −10</td><td>keeps premium, +10</td></tr>
    <tr><td>100</td><td>expires, −10</td><td>keeps premium, +10</td></tr>
    <tr><td>110</td><td>exercise, 10 − 10 = 0</td><td>obligation, 10 − 10 = 0</td></tr>
    <tr><td>130</td><td>buy at 100, sell at 130: +20</td><td>must sell at 100 a share worth 130: −20</td></tr>
    <tr><td>150</td><td>+40</td><td>−40</td></tr>
  </tbody>
</table>

Each row sums to zero. That is the bet.

### The put, briefly

A put is the other flavor. You have paid a premium (call it $8$ for this paragraph) for the right to *sell* the share at $100$. The clean cash picture: **buy the stock low in the open market, then sell it high to the put writer at the strike.**

- If $S_T=70$, you buy in the market for $70$, exercise the put, the writer is forced to buy at $100$. Pocket $30$, minus the $8$. **Net $+22$**.
- If $S_T=130$, nobody will let you sell a $130$ share to them at $100$. You throw the put away. **Net $-8$**.

A put is not a mystical “bet against.” It is a coupon that says: if this thing gets cheap, I may purchase it cheaply in the market and put it to you at the old high price.

<table>
  <thead>
    <tr>
      <th>\(S_T\)</th>
      <th>Put buyer (paid 8)</th>
      <th>Put writer (captured 8)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>70</td><td>buy at 70, put at 100: +22</td><td>must buy at 100 a share worth 70: −22</td></tr>
    <tr><td>100</td><td>expires, −8</td><td>keeps premium, +8</td></tr>
    <tr><td>130</td><td>expires, −8</td><td>keeps premium, +8</td></tr>
  </tbody>
</table>

The rest of this note prices the *call*. The put will fall out later from an accounting identity, not a second integral.

### Payoff versus profit

The **payoff** is what the contract hands you at expiry, *before* subtracting the premium. For the call buyer that is $\max(S_T-K,\,0)$; for the put buyer, $\max(K-S_T,\,0)$:

$$
(S_T - K)^+ \;=\; \max(S_T - K,\, 0).
$$

The **profit** is payoff minus premium for the buyer, and premium minus payoff for the writer.

<table>
  <thead>
    <tr>
      <th>Stock at expiry \(S_T\)</th>
      <th>Call payoff \(\max(S_T-100,\,0)\)</th>
      <th>Put payoff \(\max(100-S_T,\,0)\)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>70</td><td>0</td><td>30</td></tr>
    <tr><td>100</td><td>0</td><td>0</td></tr>
    <tr><td>120</td><td>20</td><td>0</td></tr>
    <tr><td>150</td><td>50</td><td>0</td></tr>
  </tbody>
</table>

When $S_T>K$ the call is **in the money** (the put is out). When $S_T<K$ the call is **out of the money** (the put is in). When $S_T=K$ both are **at the money**. Nicknames for the rows.

A **European** option may be exercised only at the single instant $T$. An **American** option may be exercised on any day up to and including $T$. For a call on a stock that pays no dividend, Merton's theorem says you should never exercise early, so the two prices agree. We price the European call.

At expiry the payoff is arithmetic. The hard question is *today's* premium. That depends on how $S$ wanders. Stage 2 is the language of that wander.

---

# 2. Martingales, Wiener, stocks
{: #2-martingales-wiener-stocks}

Three objects. A source of noise, a notion of a fair game, and a model of the stock built from both.

## Wiener process

A **Wiener process** — also called **Brownian motion**, written $W_t$ — is the model of pure noise used in this note. Picture a pollen grain on a water surface, or a walker who at every instant takes a tiny random step up or down. The walker's height at time $t$ is $W_t$.

It is *not* a stock price. It starts at $0$, it is as likely to be negative as positive, and its typical size at time $t$ is $\sqrt{t}$, not $t$.

**Coin-flip construction.** Fix a horizon $T$ and chop it into $n$ pieces of length $\Delta t=T/n$. Flip a fair coin at each tick. On heads walk up $\sqrt{\Delta t}$; on tails walk down $\sqrt{\Delta t}$. After time $t=k\,\Delta t$,

$$
W_t^{(n)} \;=\; \sqrt{\Delta t}\,(\xi_1+\cdots+\xi_k), \qquad \xi_i=\pm 1 \text{ with equal probability}.
$$

Each step has mean $0$ and variance $\Delta t$, so $k$ steps have mean $0$ and variance $t$. The CLT says that for large $n$ the position at a fixed $t$ is approximately $\mathcal{N}(0,t)$. Send $n\to\infty$ and the staircase becomes a continuous scribble. That scribble is $W_t$.

![A fair coin-flip walk becoming Brownian motion](/blog/assets/2024/bsm/random-walk-to-brownian.png)

**Four properties.** A standard Wiener process satisfies:

1. $W_0=0$.
2. **Independent increments.** For $t>s$, $W_t-W_s$ does not depend on the path before time $s$.
3. **Gaussian increments.** $W_t-W_s\sim\mathcal{N}(0,\,t-s)$. In particular $W_t\sim\mathcal{N}(0,t)$, so $\mathbb{E}[W_t]=0$ and $\mathrm{Var}(W_t)=t$. The typical size is $\sqrt{t}$. Over a short interval the typical move is $\sqrt{\Delta t}$, much larger than $\Delta t$ when $\Delta t$ is small.
4. **Continuous paths.** No jumps. A jagged scribble with no breaks.

![Standard Brownian motion: paths, the √t envelope, and the law of W_1](/blog/assets/2024/bsm/brownian-motion.png)

On the left, paths start at $0$ and wander equally above and below — several are *negative*, which a stock cannot be. The shaded trumpet is $\pm 2\sqrt{t}$. On the right, many runs stopped at $t=1$: the $\mathcal{N}(0,1)$ density.

Write $dW_t$ for an increment over an instant $dt$. Property 3 says $dW_t$ is about $\mathcal{N}(0,dt)$, so $(dW_t)^2$ is typically of size $dt$, not $(dt)^2$. Stage 5 is why that leftover must be kept. For now, the multiplication table, as a fact about this process:

$$
dt\cdot dt \to 0, \qquad dt\cdot dW_t \to 0, \qquad dW_t\cdot dW_t \to dt.
$$

## Martingales

A **stochastic process** is a family of random variables indexed by time — a random path. A process $M_t$ is a **martingale** if

$$
\mathbb{E}[M_T\mid \text{information up to time }t] \;=\; M_t.
$$

A martingale is a **fair game**. Given what you know now, you should not expect to win or to lose.

Wiener itself is a martingale: $\mathbb{E}[W_T\mid W_t]=W_t$, because the remaining increment has mean $0$ and is independent of the past. The physical stock will *not* be a martingale — it has a drift, which is why anyone bothers to own it. Pricing will live on a different assignment of probabilities, under which the *discounted* stock is a martingale. That assignment is stage 6. The definition is here so the word is not magic later.

## Stocks

$W_t$ is a bad model for a stock. It can be negative, and a $\$100$ stock and a $\$10$ stock should not make dollar moves of the same typical size.

You already know the ODE $dS=\mu S\,dt$, whose solution is $S_t=S_0 e^{\mu t}$. The model used here is that ODE plus noise, scaled by the current price so the *percentage* move is Wiener. That is **geometric Brownian motion**:

$$
dS_t \;=\; \mu S_t\,dt + \sigma S_t\,dW_t. \tag{2}
$$

Read it as a recipe for a short interval $dt$:

- a deterministic fraction $\mu\,dt$ (the **drift** $\mu$ is the expected rate of return);
- plus a random fraction $\sigma\,dW_t$ (the **volatility** $\sigma$ scales the Wiener increment).

Because the noise is multiplied by $S_t$, a $\$200$ stock wiggles twice as many dollars as a $\$100$ stock, and $S_t$ stays positive. The $d$ on the left is an increment, not a derivative.

The solution of $(2)$ is *not* $S_0 e^{\mu t}$ times a noise factor. Stage 5 will correct the exponent. Stage 3 is the distribution of $S_T$ that that solution will have: lognormal.

A dollar in the **money-market account** (riskless savings at a constant rate $r$) grows as $B_t=e^{rt}$. Continuous compounding: $e^{0.05}\approx 1.0513$ over a year.

![Geometric Brownian motion: stock paths, which stay positive](/blog/assets/2024/bsm/gbm-paths.png)

Each path is one draw of $W$, turned into a price by $(2)$. A European call with the dashed strike pays the excess over $100$ if the path ends above the line, and zero otherwise.

---

# 3. Lognormal properties
{: #3-lognormal-properties}

A stock is a product of returns, not a sum of dollars. Over a day the price multiplies by a gross return $1+R_i>0$. Over $N$ days

$$
S_T \;=\; S \prod_{i=1}^{N}(1+R_i), \qquad \ln S_T \;=\; \ln S + \sum_{i=1}^{N}\ln(1+R_i).
$$

The logs **add**. If the daily log-returns are independent with finite mean and variance, the CLT says their sum is approximately Gaussian. Therefore $\ln S_T\sim\mathcal{N}(m,s^2)$ for some $m,s$, and

$$
S_T \;=\; e^{Y}, \qquad Y\sim\mathcal{N}(m,s^2).
$$

A positive random variable whose logarithm is Gaussian is **lognormal**. Two objections to an additive Gaussian for the *price* are gone: $S_T>0$ always, and doubling $S$ doubles $S_T$.

![A Gaussian for the price spills below zero; a lognormal cannot](/blog/assets/2024/bsm/normal-vs-lognormal.png)

Write $Y=m+sZ$ with $Z\sim\mathcal{N}(0,1)$. The **median** of $S_T$ is $e^{m}$. The **mean** is not $e^{m}$: $x\mapsto e^{x}$ is convex, so Jensen gives $\mathbb{E}[e^Y]>e^{\mathbb{E}[Y]}$. The exact gap is the moment-generating function of a standard normal. Completing the square:

$$
\mathbb{E}[e^{aZ}]
\;=\;
\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\exp\Bigl(az-\frac{z^2}{2}\Bigr)\,dz
\;=\;
e^{a^2/2},
$$

because $az-z^2/2=-\tfrac12(z-a)^2+a^2/2$, and what remains is a normal density with mean $a$. Hence

$$
\mathbb{E}[S_T] \;=\; e^{m+s^2/2}.
$$

For $s=0.20$, $e^{0.02}\approx 1.0202$: a twenty-percent log-vol inflates the mean by about two percent relative to the median. Picture: $S=100$, $s=0.20$, $m=\ln 100+0.03$. Median $\approx 103.0$, mean $\approx 105.1$. The typical path ends near $103$; the average is pulled up by the right tail. That $e^{s^2/2}$ is Itô's correction, first as an MGF. Stage 5 recovers it from Taylor.

The density of $S_T$ follows from $y=\ln x$, $dy=dx/x$:

$$
f_{S_T}(x) \;=\; \frac{1}{s\, x\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{\ln x-m}{s}\Bigr)^2\Bigr), \qquad x>0.
$$

The extra $1/x$ is the Jacobian. The cdf is Gaussian in log-coordinates: $P(S_T\le K)=\Phi\bigl((\ln K-m)/s\bigr)$, where $\Phi(x)=P(Z\le x)$ for $Z\sim\mathcal{N}(0,1)$, and $\Phi(-x)=1-\Phi(x)$.

![Φ as area under the standard bell curve](/blog/assets/2024/bsm/phi-areas.png)

Stage 6 will identify $m=\ln S+(\mu-\tfrac12\sigma^2)\tau$ and $s=\sigma\sqrt{\tau}$ from the SDE $(2)$. For stage 4 we treat $(m,s)$ as given and compute the call by calculus.

---

# 4. A simple calculus argument
{: #4-a-simple-calculus-argument}

Assume $S_T$ is lognormal, $Y=\ln S_T\sim\mathcal{N}(m,s^2)$. Split the payoff on $\{S_T>K\}$:

$$
\mathbb{E}[(S_T-K)^+]
\;=\;
\mathbb{E}\bigl[S_T\,1_{\{S_T>K\}}\bigr] - K\,P(S_T>K).
$$

The second term is the Gaussian tail:

$$
P(S_T>K)
\;=\;
P(Y>\ln K)
\;=\;
\Phi\Bigl(\frac{-\ln K+m}{s}\Bigr).
$$

The first term is a **partial expectation**: the contribution of the upper tail, not divided by the tail probability. The $x$ in the integrand cancels the $1/x$ in the lognormal density:

$$
\mathbb{E}\bigl[S_T\,1_{\{S_T>K\}}\bigr]
\;=\;
\int_{\ln K}^{\infty}\frac{e^{y}}{s\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{y-m}{s}\Bigr)^2\Bigr)\,dy.
$$

The exponent is $y-(y-m)^2/(2s^2)$. Expand and complete the square, the same move as $\mathbb{E}[e^{aZ}]$:

\begin{align*}
y - \frac{(y-m)^2}{2s^2}
&= \frac{2s^2 y - (y^2-2my+m^2)}{2s^2}
= \frac{-y^2 + 2(m+s^2)y - m^2}{2s^2}.
\end{align*}

The identity $y^2-2(m+s^2)y=\bigl(y-(m+s^2)\bigr)^2-(m+s^2)^2$ turns the numerator into $-\bigl(y-(m+s^2)\bigr)^2+2ms^2+s^4$. Divide by $2s^2$:

$$
y - \frac{(y-m)^2}{2s^2}
\;=\;
-\frac{\bigl(y-(m+s^2)\bigr)^2}{2s^2} + m + \frac{s^2}{2}.
$$

The constant $m+s^2/2$ comes out. What remains is a normal density with mean $m+s^2$ and variance $s^2$, truncated at $\ln K$:

$$
\mathbb{E}\bigl[S_T\,1_{\{S_T>K\}}\bigr]
\;=\;
e^{m+s^2/2}\,\Phi\Bigl(\frac{-\ln K+m+s^2}{s}\Bigr). \tag{14}
$$

The cutoff turned the full MGF factor into that factor times a $\Phi$. The mean-shift $m\mapsto m+s^2$ is the gap between the two $\Phi$ arguments. Combining,

$$
\mathbb{E}[(S_T-K)^+]
\;=\;
e^{m+s^2/2}\,\Phi(d_{+}) - K\,\Phi(d_{-}),
\tag{15}
$$

$$
d_{+} \;=\; \frac{-\ln K+m+s^2}{s}, \qquad d_{-} \;=\; \frac{-\ln K+m}{s}.
$$

If the premium were the discounted expected payoff under this law, it would be $e^{-r\tau}$ times $(15)$. **That is the shape of Black–Scholes**: two $\Phi$'s, a share piece and a cash piece.

What we do not yet have is $(m,s)$, and we do not yet know that the *physical* pair $(m,s)$ is the one to use. Stage 5 produces $(m,s)$ from the SDE. Stage 6 replaces the physical drift in $m$ by $r$. Until then, this is a calculus problem with two free parameters.

## What each assumption is doing

The two-$\Phi$ shape is not a law of nature. It is a receipt for a short list of hypotheses. Perturb one and the formula either *morphs* (same skeleton, different inputs or an extra factor) or *breaks* (the completing-the-square step no longer lands on $\Phi$). That is the power the assumptions grant: they are what make a European call a pair of normal cdfs instead of a numerical integral, a PDE, or a tree.

**$Y=\ln S_T$ is Gaussian.** Completing the square turned $e^{y}$ times a normal density into another normal density. That is a property of $\exp(-\tfrac12 z^2)$, not of densities in general. If $\ln S_T$ is Student-$t$, the exponent is $\log(1+y^2/\nu)$ and there is no shift that produces another $t$ of the same family times a constant; you integrate numerically. If $S_T$ is a *mixture* of lognormals — stochastic volatility: $\sigma$ itself random, so $s$ is random and you mix over $s$ — then

$$
\mathbb{E}[(S_T-K)^+] \;=\; \mathbb{E}\bigl[e^{m+s^2/2}\Phi(d_{+}(s)) - K\Phi(d_{-}(s))\bigr],
$$

an average of Black–Scholes prices, not a single pair of $\Phi$'s. Heston lives here. If you add jumps, $Y$ is Gaussian plus a Poisson number of extra Gaussians: Merton's jump-diffusion is a **sum** of $\Phi$-pairs, one per jump-count. The skeleton morphs; the one-line formula $(15)$ breaks.

**A single pair $(m,s)$, not a family indexed by strike or path.** If volatility is a deterministic function of time, $s^2=\int_0^{\tau}\sigma(t)^2\,dt$ is still one number, and $(15)$ survives with that $s$. If $\sigma=\sigma(S,t)$ (local vol), $S_T$ is typically *not* lognormal, and there is no two-$\Phi$ of this shape — Dupire will still *quote* every strike in implied $\sigma(K)$, but that is the formula used backwards as a dictionary, not forwards as a model. If you let $s=s(K)$ depend on the strike you are pricing, you have already left the model: one lognormal cannot fit two smiles at once.

**The payoff is $(S_T-K)^+$, a function of the *terminal* price only.** The integral is over the law of $S_T$. It does not see the path. An **American** put can be exercised at any time, so the value depends on the whole path of opportunities; there is a free boundary, and no closed $\Phi$. A **barrier** option knocks out if $S$ touches a level before $T$; you need the joint law of $(S_T,\min S_t)$ or $(\,S_T,\max S_t)$. An **Asian** option pays on the average of $S$, which is not lognormal even when $S_T$ is. Cash-or-nothing — pay $1$ if $S_T>K$ — is not a break: it *is* the second term of the split, $e^{-r\tau}\Phi(d_{-})$. Asset-or-nothing is the first term. The call is those two claims glued together. Change the glue, and you are still in the family. Change the information the payoff sees, and you are not.

**The strike $K$ is a known constant.** It is the cutoff $\ln K$ in the integral. If the strike is itself random — average-strike Asian, or a quanto with a foreign asset in the strike — the cutoff is no longer a number, and $(14)$ does not apply. If you pay $(S_T-K)^+$ in a *different* currency, you have a second lognormal and a covariance; the formula morphs (still $\Phi$'s, extra $e^{q\tau}$ and a modified $s$).

**Discounting is $e^{-r\tau}$ with $r$ deterministic.** A constant $r$ factors out of the expectation. If $r_t$ is random and correlated with $S$, you must compute $\mathbb{E}\bigl[e^{-\int r}(S_T-K)^+\bigr]$; the discount no longer comes out, and you need a two-factor model (or a bond as numeraire — stage 7). If $r$ is deterministic but *time-dependent*, $e^{-r\tau}$ becomes $e^{-\int r}$, and $(15)$ survives with that factor. Deterministic $r$ is what lets a number sit in front of the two $\Phi$'s.

**The law of $S_T$ is the law you take the expectation under.** If you feed the *physical* $(m,s)$ — the one with $\mu$ in it — into $(15)$ and discount, you get a number. It is not the no-arbitrage price. The two-$\Phi$ *shape* is intact; the input $m$ is wrong. Stage 6 is the statement that the pricing law uses $r$ in place of $\mu$. Perturbing this assumption does not break the calculus. It prices a different lottery.

**$S_T>0$ and the Jacobian $1/x$.** That is the multiplicative hypothesis of stage 3. If you go back to an additive Gaussian, $S_T=S+\sigma\sqrt{\tau}\,Z$ (Bachelier), the integral is a $\Phi$ of $(S-K)/(\sigma\sqrt{\tau})$ with no logarithms, and prices can be negative. The formula *modulates* into a different closed form, used for rates after 2008 when yields could go through zero. The log in $d_{\pm}$ is not decoration. It is the Jacobian of stage 3, still visible in the answer.

**No dividend (or a continuous yield that can be absorbed into $m$).** If the stock pays a continuous yield $q$, the forward is $S e^{(r-q)\tau}$ instead of $S e^{r\tau}$, and $(15)$ morphs by $m\leftarrow m-q\tau$ and an extra $e^{-q\tau}$ on the share piece. The skeleton lives. A *discrete cash* dividend of size $D$ just before $T$ makes $S_T=S^*_T-D$ with $S^*$ lognormal; $S_T$ itself is not, and you integrate a shifted lognormal — doable, but not $(15)$ as written.

<table>
  <thead>
    <tr>
      <th>Assumption</th>
      <th>Perturb</th>
      <th>Two \(\Phi\)'s?</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>\(\ln S_T\) Gaussian</td><td>Student-\(t\); mixture (Heston); jumps (Merton)</td><td>breaks; average of \(\Phi\)'s; sum of \(\Phi\)'s</td></tr>
    <tr><td>one \((m,s)\)</td><td>\(\sigma(t)\) deterministic; \(\sigma(S,t)\); smile \(s(K)\)</td><td>survives as \(s^2=\int\sigma^2\); breaks; quoting machine</td></tr>
    <tr><td>payoff \((S_T-K)^+\)</td><td>American; barrier; Asian; cash-or-nothing</td><td>breaks; breaks; breaks; <em>is</em> the second \(\Phi\)</td></tr>
    <tr><td>fixed strike \(K\)</td><td>random strike; quanto</td><td>breaks; morphs (extra cov)</td></tr>
    <tr><td>\(e^{-r\tau}\), \(r\) deterministic</td><td>\(r(t)\) deterministic; random \(r_t\)</td><td>survives; breaks (two-factor)</td></tr>
    <tr><td>this law is the pricing law</td><td>physical \(\mu\) instead of \(r\)</td><td>shape lives, number is wrong</td></tr>
    <tr><td>multiplicative, \(S_T>0\)</td><td>additive Gaussian (Bachelier)</td><td>different \(\Phi\), no \(\ln\)</td></tr>
    <tr><td>no cash dividend</td><td>yield \(q\); discrete \(D\)</td><td>morphs (\(e^{-q\tau}\)); shifted integral</td></tr>
  </tbody>
</table>

The assumptions are doing a lot of work. They are also why a rain check on a stock has a two-line formula and a rain check on an average, or on a stock that can jump, does not. Stages 5–6 will *choose* $(m,s)$ inside this skeleton. They will not replace the skeleton. If you wanted a different skeleton, you would have had to perturb the list above.

---

# 5. A detour to Japan
{: #5-a-detour-to-japan}

Ordinary calculus throws $(dx)^2$ away because it is $o(dx)$. For Wiener that discard is illegal: $(dW)^2$ is the same size as $dt$. In 1942 Kiyosi Itô put the leftover back. That leftover *is* the $e^{s^2/2}$ of stage 3.

## Quadratic variation, by hand

Chop a year into four steps. Each step is $\pm\sqrt{1/4}=\pm 1/2$. Four heads ends at $+2$. Four tails ends at $-2$. Mixed paths end at $0$. The *ending* points disagree. The sum of the squared steps does not:

$$
\bigl(\tfrac12\bigr)^2+\bigl(\tfrac12\bigr)^2+\bigl(\tfrac12\bigr)^2+\bigl(\tfrac12\bigr)^2 \;=\; 1
$$

on **every** path.

![Four coin-flip paths; every one has quadratic variation 1](/blog/assets/2024/bsm/quadratic-variation.png)

In the limit this is a theorem. Chop $[0,t]$ into $n$ steps $\Delta t=t/n$. Each increment satisfies $\mathbb{E}[(\Delta W_i)^2]=\Delta t$ and, because $\Delta W_i\sim\mathcal{N}(0,\Delta t)$, $\mathrm{Var}((\Delta W_i)^2)=2(\Delta t)^2$. The sum of squares has mean $t$ and variance $2t^2/n\to 0$. Convergence in $L^2$ to the constant $t$: $(dW_t)^2=dt$. Keep them.

The paths have, with probability $1$, no tangent line anywhere. You cannot write $dW_t/dt$. You can only write $dW_t$.

## Itô on $W^2$

Taylor for $f(x)=x^2$ says $\Delta f=2x\,\Delta x+(\Delta x)^2$. Calculus 1 throws the second term away. On the four-step path of four heads, $W=0,0.5,1,1.5,2$, so $W^2$ ends at $4$. The Calculus-1 running sum $\sum 2W\,\Delta W$ is

$$
2\cdot 0\cdot\tfrac12 + 2\cdot\tfrac12\cdot\tfrac12 + 2\cdot 1\cdot\tfrac12 + 2\cdot\tfrac32\cdot\tfrac12 \;=\; 3.
$$

The leftover $\sum(\Delta W)^2=1$ makes up the difference: $3+1=4$.

![On HHHH, Calc 1 tracks W² with a gap of 1 — the quadratic variation](/blog/assets/2024/bsm/ito-square.png)

**Itô's lemma** is Taylor in two variables, with the multiplication table substituted in. Let $X$ satisfy $dX=a\,dt+b\,dW$, and let $f(t,x)$ be $C^{1,2}$. The second-order expansion is

$$
\Delta f
\;=\;
f_t\,\Delta t + f_x\,\Delta x + \tfrac12 f_{xx}(\Delta x)^2 + f_{tx}\,\Delta t\,\Delta x + \tfrac12 f_{tt}(\Delta t)^2 + o(\Delta t).
$$

Feed in $\Delta x=a\,\Delta t+b\,\Delta W$. The table kills $(\Delta t)^2$ and $\Delta t\,\Delta W$, and sends $(\Delta x)^2\to b^2\Delta t$. What remains is

$$
df(t,X_t) \;=\; \Bigl(f_t + a f_x + \tfrac12 b^2 f_{xx}\Bigr)dt + b f_x\,dW_t. \tag{3}
$$

The first two terms in the $dt$ coefficient are the ordinary chain rule. The third is the leftover on $W^2$. For $f(x)=x^2$ and $X=W$ ($a=0$, $b=1$, $f_{xx}=2$), the correction is $dt$, and $d(W^2)=2W\,dW+dt$. Integrate: $W_t^2=2\int W\,dW+t$. At $t=1$ the extra $+1$ is the gap in the figure.

Stage 6 applies the same lemma to $\ln S$.

---

# 6. Derive from stochastic calculus
{: #6-derive-from-stochastic-calculus}

Four jobs: solve the SDE, see why $\mu$ is not in the price, plug into stage 4, and match the PDE.

## Itô on $\ln S$

Apply $(3)$ to $f(s)=\ln s$ and to the stock $(2)$. Then $f_s=1/s$, $f_{ss}=-1/s^2$, and the leftover is $-\tfrac12\sigma^2\,dt$:

\begin{align*}
d\ln S_t
&= \frac{1}{S_t}\,dS_t + \tfrac12\Bigl(-\frac{1}{S_t^2}\Bigr)(\sigma S_t\,dW_t)^2 \\
&= \mu\,dt + \sigma\,dW_t - \tfrac12\sigma^2\,dt \\
&= \bigl(\mu - \tfrac12\sigma^2\bigr)dt + \sigma\,dW_t.
\end{align*}

Integrate from $t$ to $T$. Write $\tau=T-t$, and $W_T-W_t\stackrel{d}{=}\sqrt{\tau}\,Z$ with $Z\sim\mathcal{N}(0,1)$:

$$
S_T \;=\; S_t\exp\Bigl(\bigl(\mu-\tfrac12\sigma^2\bigr)\tau + \sigma\sqrt{\tau}\,Z\Bigr). \tag{4}
$$

This *is* the lognormal of stage 3, with

$$
m \;=\; \ln S_t + \bigl(\mu-\tfrac12\sigma^2\bigr)\tau, \qquad s^2 \;=\; \sigma^2\tau.
$$

The $\tfrac12\sigma^2$ that left the log-drift is the $e^{s^2/2}$ from the MGF. It returns in the mean of the stock: $\mathbb{E}[S_T\mid S_t]=S_t e^{\mu\tau}$. Nothing is lost. It is booked in a different ledger.

**Assumptions**, said once. The stock follows $(2)$ with $\mu,\sigma$ constant (one Brownian motion; no jumps). The rate $r$ is a known constant; you may borrow or lend any amount at $r$. No dividends. No arbitrage, continuous trading, a complete market: every payoff can be manufactured from the stock and the money-market account, because there is one source of noise and two traded assets. Fractional holdings and short sales are allowed; there are no transaction costs.

## Why not $\mu$: a two-leaf tree

The physical pair $(m,s)$ is not the one that prices the call. A cartoon is enough.

A stock trades at $100$. In one year it is either $200$ or $50$. No interest. A call struck at $100$ pays $100$ or $0$.

![One step, two outcomes, one manufactured call](/blog/assets/2024/bsm/one-step-tree.png)

Hold $\Delta$ shares and $B$ dollars in cash (negative $B$ means you borrowed). Match the call on both leaves:

$$
200\Delta + B \;=\; 100, \qquad 50\Delta + B \;=\; 0.
$$

Subtract: $\Delta=2/3$, then $B=-33.33$. Today the portfolio costs $\tfrac23\cdot 100-33.33=33.33$. If the call sold for anything else, you would buy the cheap side and sell the dear side:

<table>
  <thead>
    <tr>
      <th>Quote</th>
      <th>Today's cash</th>
      <th>At expiry</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>\(40\) (dear)</td><td>sell call, buy portfolio: \(+6.67\)</td><td>portfolio covers the call; keep \(6.67\)</td></tr>
    <tr><td>\(33.33\)</td><td>nothing to do</td><td>nothing to do</td></tr>
    <tr><td>\(20\) (cheap)</td><td>buy call, sell portfolio: \(+13.33\)</td><td>call covers the portfolio; keep \(13.33\)</td></tr>
  </tbody>
</table>

A free lunch if the quote is not $33.33$. The physical probability that the stock doubles never entered. Two linear equations.

The unique probability $p^*$ that makes the stock a fair game is $p^*=(1-1/2)/(2-1/2)=1/3$, and $C=p^*\cdot 100=33.33$ again. With interest, a dollar grows by a factor $R$ over the step, $p^*=(R-d)/(u-d)$, and the call is the discounted fair-game expectation. That $p^*$ is not the real-world chance of the up-move. It is the probability that makes the stock a martingale, in the sense of stage 2.

A tree calibrated to $r=5\%$, $\sigma=20\%$, one year, $S=K=100$, with Cox–Ross–Rubinstein $u=e^{\sigma\sqrt{\Delta t}}$, $d=1/u$, walks from $12.16$ ($n=1$) to $10.45$ ($n\to\infty$):

<table>
  <thead>
    <tr>
      <th>\(n\)</th><th>1</th><th>2</th><th>4</th><th>8</th><th>16</th><th>32</th><th>64</th><th>128</th><th>\(\infty\)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>call</td><td>12.16</td><td>9.54</td><td>9.97</td><td>10.21</td><td>10.33</td><td>10.39</td><td>10.42</td><td>10.43</td><td>10.45</td>
    </tr>
  </tbody>
</table>

![n-step Cox–Ross–Rubinstein tree walking to 10.45](/blog/assets/2024/bsm/crr-convergence.png)

The $n=2$ dip is a coarse histogram of a bell curve. From $n=4$ the walk is toward $10.45$. That is the number. The closed form is stage 4, with the *fair-game* $(m,s)$.

## Girsanov, from two Gaussians

On the tree, the likelihood ratio on one step is $p^*/p$ on up and $(1-p^*)/(1-p)$ on down. Then $\mathbb{E}^*[X]=\mathbb{E}[X\,\xi]$. Over $n$ steps, $\xi$ is the product of those ratios. That product *is* Girsanov, before the limit.

**One Gaussian.** Under $\mathbb{P}$, $W_t\sim\mathcal{N}(0,t)$. We want $\mathbb{Q}$ under which $W_t\sim\mathcal{N}(-\theta t,\,t)$, so that $W_t+\theta t$ is standard Wiener. The density ratio is

$$
\xi_t
\;=\;
\exp\bigl(-\theta W_t - \tfrac12\theta^2 t\bigr).
$$

For any test function, $\mathbb{E}^{\mathbb{Q}}[f(W_t)]=\mathbb{E}^{\mathbb{P}}[f(W_t)\,\xi_t]$. Independent increments multiply the same ratio across steps. That is **Girsanov's theorem**, from the Gaussian pdf.

**Which $\theta$.** Rewrite $(2)$ as

$$
dS \;=\; r S\,dt + \sigma S\Bigl(dW + \frac{\mu-r}{\sigma}\,dt\Bigr).
$$

The process in parentheses is Wiener plus a constant drift $\theta=(\mu-r)/\sigma$, the **market price of risk**. Girsanov with that $\theta$ makes $W^{\mathbb{Q}}_t=W_t+\theta t$ a Wiener process under $\mathbb{Q}$, and

$$
dS_t \;=\; r S_t\,dt + \sigma S_t\,dW_t^{\mathbb{Q}}. \tag{5}
$$

Under $\mathbb{Q}$, $(4)$ holds with $\mu$ replaced by $r$:

$$
S_T \;=\; S_t\exp\Bigl(\bigl(r-\tfrac12\sigma^2\bigr)\tau + \sigma\sqrt{\tau}\,Z\Bigr), \qquad Z\sim\mathcal{N}(0,1)\text{ under }\mathbb{Q}. \tag{7}
$$

The discounted stock $S_t e^{-rt}$ is a martingale under $\mathbb{Q}$. The call is the discounted fair-game expectation:

$$
C \;=\; e^{-r\tau}\,\mathbb{E}^{\mathbb{Q}}\bigl[(S_T-K)^+\bigr]. \tag{6}
$$

Two traders who disagree about $\mu$ still agree on $C$ if they agree on $\sigma$. $\Delta=2/3$ did not ask who thought the stock would double.

## Plug in

Under $\mathbb{Q}$,

$$
m \;=\; \ln S_t + \bigl(r-\tfrac12\sigma^2\bigr)\tau, \qquad s \;=\; \sigma\sqrt{\tau}.
$$

Feed into $(15)$. Then $e^{m+s^2/2}=S_t e^{r\tau}$, so the discounted share-piece is $S_t\Phi(d_1)$ and the discounted cash-piece is $K e^{-r\tau}\Phi(d_2)$, with

$$
C \;=\; S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2), \tag{1}
$$

$$
d_1 \;=\; \frac{\ln(S_t/K)+\bigl(r+\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}, \qquad d_2 \;=\; d_1 - \sigma\sqrt{\tau}.
$$

For the rain check: $S=K=100$, $\tau=1$, $r=0.05$, $\sigma=0.20$. Then $d_2=0.15$, $d_1=0.35$, $\Phi(0.15)\approx 0.560$, $\Phi(0.35)\approx 0.637$, and

$$
C \;=\; 100\cdot 0.637 - 100\cdot e^{-0.05}\cdot 0.560 \;\approx\; 63.68-53.23 \;=\; 10.45.
$$

We guessed a working premium of $10$. The formula charges $10.45$. Close, for a rain check. $\Phi(d_1)\approx 0.637$ is the **delta**: you manufacture this call by holding about two-thirds of a share, the $\Delta=2/3$ of the tree, smeared across spots. $\Phi(d_2)\approx 0.560$ is the risk-neutral chance of exercise.

![A European call: the kink at expiry, the smooth price today](/blog/assets/2024/bsm/call-payoff.png)

![Two evaluations of the same bell curve](/blog/assets/2024/bsm/phi-anatomy.png)

```python
from math import log, exp, sqrt, erf

def Phi(x):
    return 0.5 * (1 + erf(x / sqrt(2)))

S, K, r, sig, tau = 100, 100, 0.05, 0.20, 1.0
d1 = (log(S / K) + (r + 0.5 * sig**2) * tau) / (sig * sqrt(tau))
d2 = d1 - sig * sqrt(tau)
C = S * Phi(d1) - K * exp(-r * tau) * Phi(d2)
print(C)  # 10.450583572185565
```

Volatility is the only input you cannot read off a newspaper.

<table>
  <thead>
    <tr>
      <th>\(\sigma\)</th>
      <th>call</th>
      <th>what happened</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>\(0\)</td><td>\(4.88\)</td><td>no wander: just the forward \(S-Ke^{-r\tau}\)</td></tr>
    <tr><td>\(10\%\)</td><td>\(6.80\)</td><td></td></tr>
    <tr><td>\(20\%\)</td><td>\(10.45\)</td><td>the rain check</td></tr>
    <tr><td>\(40\%\)</td><td>\(18.02\)</td><td></td></tr>
    <tr><td>\(100\%\)</td><td>\(39.84\)</td><td>almost a coin-flip on the stock itself</td></tr>
  </tbody>
</table>

![ATM call price against volatility](/blog/assets/2024/bsm/call-vs-vol.png)

**Put-call parity.** A European call minus a European put, same strike and expiry, is a forward: you will buy the stock at $K$ at time $T$ whether $S_T$ is above or below. A forward on a non-dividend stock is worth $S_t-Ke^{-r\tau}$, so $C-P=S_t-Ke^{-r\tau}$ and

$$
P \;=\; K e^{-r\tau}\,\Phi(-d_2) - S_t\,\Phi(-d_1).
$$

For the rain-check numbers, $P\approx 5.57$, and $C-P=4.88$, the $\sigma=0$ row.

## The PDE, and the heat equation

Black and Scholes started from a portfolio $\Pi=-V+\Delta S$. Expand $dV$ with $(3)$, choose $\Delta=V_S$ so the $dW$ terms cancel (**delta-hedging**), and require the now-riskless $\Pi$ to earn $r$. The $dW$ cancellation eats $\mu$, just as $\Delta=2/3$ did. The Black–Scholes **PDE** is

$$
V_t + rS V_S + \tfrac12\sigma^2 S^2 V_{SS} - rV \;=\; 0, \tag{17}
$$

with $V(S,T)=(S-K)^+$. For the rain-check numbers, $\Delta=V_S=\Phi(d_1)\approx 0.637$.

This is a linear parabolic PDE. You have seen one: the heat equation. Let $\tau=T-t$, $x=\ln(S/K)$, $V(S,t)=U(x,\tau)$. Then $V_t=-U_\tau$, $V_S=U_x/S$, and $S^2 V_{SS}=U_{xx}-U_x$. Substitute:

$$
U_\tau \;=\; \tfrac12\sigma^2 U_{xx} + \bigl(r-\tfrac12\sigma^2\bigr)U_x - r U.
$$

Rescale $\tilde\tau=\sigma^2\tau/2$, set $k=2r/\sigma^2$, and kill lower-order terms with $U=e^{\alpha x+\beta\tilde\tau}W$, $\alpha=(1-k)/2$, $\beta=\alpha^2+(k-1)\alpha-k$. Then $W_{\tilde\tau}=W_{xx}$. (Rain-check numbers: $k=2.5$, $\alpha=-3/4$, $\beta=-49/16$.)

The heat kernel is $G(x,\tilde\tau)=(4\pi\tilde\tau)^{-1/2}\exp(-x^2/(4\tilde\tau))$, an expectation against $\mathcal{N}(0,2\tilde\tau)$. And $2\tilde\tau=\sigma^2\tau=\mathrm{Var}(\ln S_T)$ under $\mathbb{Q}$. The heat kernel *is* the lognormal. **Feynman–Kac**, here, is that kernel, run at variance $\sigma^2\tau$.

---

# 7. Change of numeraire
{: #7-change-of-numeraire}

Stage 4 split the call into a share-or-nothing and a cash-or-nothing. Under $\mathbb{Q}$, the cash-or-nothing's probability is $\Phi(d_2)$. The share-or-nothing's $\Phi(d_1)$ is the same event, measured in a different unit of account.

A **numeraire** is the unit you quote prices in. Dollars: the money-market account $B_t=e^{rt}$. Shares: the stock $S_t$. For each choice there is a measure that makes every asset, *divided by that numeraire*, a martingale.

<table>
  <thead>
    <tr>
      <th>Numeraire</th>
      <th>Measure</th>
      <th>Martingale</th>
      <th>exercise probability</th>
      <th>Role in (1)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>bond \(B_t=e^{rt}\)</td>
      <td>\(\mathbb{Q}\)</td>
      <td>\(S_t/B_t\)</td>
      <td>\(\Phi(d_2)\)</td>
      <td>multiplies the cash \(Ke^{-r\tau}\)</td>
    </tr>
    <tr>
      <td>stock \(S_t\)</td>
      <td>\(\mathbb{Q}^{S}\)</td>
      <td>\(B_t/S_t\)</td>
      <td>\(\Phi(d_1)\)</td>
      <td>multiplies the share \(S_t\)</td>
    </tr>
  </tbody>
</table>

The density ratio that changes $\mathbb{Q}$ into $\mathbb{Q}^{S}$ is the terminal value of the new numeraire, rebased:

$$
\frac{d\mathbb{Q}^{S}}{d\mathbb{Q}}
\;=\;
\frac{S_T}{S_t e^{r\tau}}.
$$

Under $\mathbb{Q}$, from $(7)$,

$$
\frac{S_T}{S_t e^{r\tau}}
\;=\;
\exp\bigl(-\tfrac12\sigma^2\tau + \sigma\sqrt{\tau}\,Z\bigr).
$$

That is the Girsanov density $\xi=\exp(-\theta W-\tfrac12\theta^2 t)$ of stage 6, with $\theta=-\sigma$ and $W_{\tau}=\sqrt{\tau}\,Z$. The tilt *adds* $\sigma\sqrt{\tau}$ to $Z$. The event $\{S_T>K\}$ is $\{Z>-d_2\}$ under $\mathbb{Q}$; after the tilt it is $\{Z+\sigma\sqrt{\tau}>-d_2\}=\{Z>-d_1\}$, so

$$
\mathbb{Q}^{S}(S_T>K) \;=\; \Phi(d_1).
$$

The share-or-nothing is therefore $S_t\,\Phi(d_1)$: today's share, times the exercise probability *in share units*. The cash-or-nothing is $Ke^{-r\tau}\,\Phi(d_2)$: discounted strike, times the exercise probability *in dollar units*. That is $(1)$, with both $\Phi$'s now ordinary probabilities, each belonging to the numeraire that multiplies it.

The same Itô computation on $f=1/S$ produces the SDE for the inverse stock, whose lognormal is the one $\mathbb{Q}^{S}$ sees. The density ratio above is enough: it is Girsanov with the opposite tilt.

---

# Limitations
{: #limitations}

**Dividends.** A continuous yield $q$ changes the risk-neutral drift of $S$ from $r$ to $r-q$. The same two integrals produce $C=S_t e^{-q\tau}\Phi(d_1)-K e^{-r\tau}\Phi(d_2)$, with $r$ replaced by $r-q$ inside $d_1,d_2$ as well. Index options ($q$ is the basket yield), FX ($q$ is the foreign rate), futures ($q=r$: Black 1976).

**The smile.** After 1987 the market stopped believing in a single $\sigma$. **Implied volatility** is the number you feed into $(1)$ to recover the quoted price. Plot it against strike and you get a smile, or in equities a smirk. Traders still quote in Black–Scholes implied vol. They do not believe the lognormal.

**Jumps, stochastic vol, Americans.** Merton added jumps. Heston let $\sigma_t$ wander. Dupire's local vol refits a whole implied surface. None of these has a two-$\Phi$ formula of the same shape. The American put has no closed form of this kind; a binomial tree is the honest computation.

What has been proved is a theorem about a complete market driven by one Wiener process: the unique no-arbitrage price of $(S_T-K)^+$ is $(1)$. Using that theorem as a price, as a quoting convention, or as the first term of an approximation is a separate decision.

Seven stages: the contract; the noise, the fair game, and the stock; the lognormal; a calculus integral; Itô; the SDE plus Girsanov; a change of unit. The rain check is $10.45$.

Cheers.

---

# References
{: #references}

- Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. [Local copy](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf). [Wayback, 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf).
- F. Black and M. Scholes, [The Pricing of Options and Corporate Liabilities](https://www.cs.princeton.edu/courses/archive/fall09/cos323/papers/black_scholes73.pdf), *JPE* 81 (1973).
- R. C. Merton, [Theory of Rational Option Pricing](https://www.jstor.org/stable/3003143), *Bell Journal* 4 (1973).
- J. C. Cox, S. A. Ross, and M. Rubinstein, [Option Pricing: A Simplified Approach](https://www.sciencedirect.com/science/article/pii/0304405X79900151), *J. Financial Economics* 7 (1979). The $n$-step tree.
- K. Itô, [On Stochastic Differential Equations](https://projecteuclid.org/euclid.memo/1183518816), *Mem. AMS* (1951).
- J. Hull, *Options, Futures, and Other Derivatives*.
- S. Shreve, *Stochastic Calculus for Finance II*.
- E. Derman and M. B. Miller, *The Volatility Smile*.
