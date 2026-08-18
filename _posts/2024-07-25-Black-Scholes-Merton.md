---
layout: post
title: "Back-of-the-Envelope: Black-Scholes-Merton"
date: 2024-07-24
categories: wealth
mathjax: true
---

Is it optional to know what an option is? No.

This note prices a European call. We will not write the famous formula until we have the tools to read it. First: what the contract *is*. Then a detour to Japan, where Kiyosi Itô repaired the chain rule for paths that jitter like a stock. Then, and only then, the price.

If you have Calc 1–2, a first course in probability (bell curves, means, the substitution $y=\ln x$), and have never seen a derivative in the Wall Street sense, you are the intended reader. Every term is defined when it appears.

- [What is an option?](#what-is-an-option)
- [How do we price one of these things?](#how-do-we-price-one-of-these-things)
- [A detour to Japan](#a-detour-to-japan)
- [Brownian motion](#brownian-motion)
- [The stock: geometric Brownian motion](#the-stock-geometric-brownian-motion)
- [Martingales](#martingales)
- [Itô's lemma](#itos-lemma)
- [Assumptions](#assumptions)
- [The Black–Scholes–Merton formula](#the-blackscholesmerton-formula)
- [Risk-neutral pricing](#risk-neutral-pricing)
- [Toolkit: the lognormal](#toolkit-the-lognormal)
- [Route I: two lognormal integrals](#route-i-two-lognormal-integrals)
- [Route II: change of numeraire](#route-ii-change-of-numeraire)
- [The PDE, briefly](#the-pde-briefly)
- [Limitations](#limitations)
- [References](#references)

The change-of-numeraire calculation follows Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. The original host is gone. A copy is [here](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf); the [Wayback capture of 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf) is the provenance.

---

# What is an option?
{: #what-is-an-option}

In ordinary English, optional means you do not have to. In finance that is almost the definition.

An **option** is a contract that gives its owner the *right*, and not the obligation, to buy or sell something at a pre-agreed price. The something is the **underlying** — a share of stock, a bushel of wheat. The pre-agreed price is the **strike**, written $K$. The deadline is **expiry**, written $T$. For that right you pay money up front, the **premium**. The rest of this note is the question: what must the premium be?

You already know the everyday version. A rain check that lets you buy a TV at today's price next month is a call option on the TV. If the store drops the price, you ignore the rain check and buy cheaper. If the store raises the price, you use the rain check. You will only exercise when it helps you. That one-sidedness is the whole point.

## Calls and puts: bets in favor and bets against

Options come in two flavors.

A **call** is the right to *buy* the underlying at the strike. It is a bet the underlying will finish *above* $K$. A **put** is the right to *sell* the underlying at the strike. It is a bet the underlying will finish *below* $K$.

Walk through a call with numbers, before any symbols. A stock trades at 100 dollars today. You buy a call with strike $K = 100$, expiring in one year. You have paid some premium $C$ — we do not yet know what $C$ should be. One year later the stock is at $S_T$, and you look at the contract:

- If $S_T = 130$, you exercise: buy at 100 a share that is worth 130, and pocket 30. Your net profit is $30 - C$.
- If $S_T = 80$, exercising would mean paying 100 for something worth 80. You are not required to be that foolish. You throw the contract away. Your net profit is $-C$ (you already paid the premium).
- If $S_T = 100$, exercising gains you nothing. You are indifferent. Payoff of the contract itself is 0.

The **payoff** of the contract — what it hands you at expiry, ignoring the premium you already paid — is therefore

$$
(S_T - K)^+ \;=\; \max(S_T - K,\, 0).
$$

The little plus means “take this if it is positive, otherwise take zero.” A put’s payoff is $(K - S_T)^+$.

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

When $S_T > K$ people say the call is **in the money**. When $S_T < K$ it is **out of the money**. When $S_T = K$ it is **at the money**. Those are just nicknames for the three rows.

## Europeans and Americans

Two nationalities, and this is the only distinction that matters here.

- A **European** option may be exercised only at the single instant $T$. You wait until expiry, then decide.
- An **American** option may be exercised on any day up to and including $T$.

The American extra right sounds valuable, and for a *put* it is. For a *call* on a stock that pays no dividend, it is a theorem of Merton’s that you should never exercise early — so the American call and the European call have the same price. We price the European call. The European put will fall out of an accounting identity later, not a second integral.

---

# How do we price one of these things?
{: #how-do-we-price-one-of-these-things}

At expiry the payoff is arithmetic: count on your fingers. The hard question is *today’s* premium. What should you pay *now* for a lottery that, one year from now, pays $\max(S_T - 100,\, 0)$?

The honest answer depends on how $S$ is going to wander between now and $T$. If the stock is almost surely going to sit at 100, the lottery is almost surely worth nothing and you should pay almost nothing. If the stock is liable to be at 200 or at 20, the lottery is juicy — you capture the 200 and walk away from the 20 — and you should pay more.

So we need a model of the wander. Stock prices are not smooth curves. They jitter. The chain rule you learned in Calculus 1 assumes a tangent line; a stock path does not offer one. In 1942 the Japanese mathematician Kiyosi Itô found the corrected chain rule for this kind of path. We cannot write down a price until we have that correction. Detour.

---

# A detour to Japan
{: #a-detour-to-japan}

Itô’s observation, in one sentence: if the input to a function is a Brownian scribble, the $\tfrac12 f''(x)\,(dx)^2$ term in Taylor’s formula is the *same size* as the $f'(x)\,dx$ term, and you cannot throw it away. That leftover is the entire difference between a world you can hedge and a world you cannot.

We need four things from his world, in order.

1. **Brownian motion** $W_t$ — a stand-in for the market’s noise. (Also called a **Wiener process**. Same object, two names.)
2. **Geometric Brownian motion** — the stock, built from $W_t$ so the price stays positive.
3. A **martingale** — a fair game. This is how we will mean “no free lunch.”
4. **Itô’s lemma** — the corrected chain rule.

Then we can write the formula.

# Brownian motion
{: #brownian-motion}

A **Brownian motion** — also called a **Wiener process**, written $W_t$ — is the model of pure noise used in this note. Picture a pollen grain on a water surface, or a walker who at every instant takes a tiny random step up or down. The walker's height at time $t$ is $W_t$.

It is *not* a stock price. It starts at $0$, it is as likely to be negative as positive, and its typical size at time $t$ is $\sqrt{t}$, not $t$. The stock will be built from it in the next section.

## A coin-flip construction

Fix a time horizon $T$ and chop it into $n$ equal pieces of length $\Delta t = T/n$. Flip a fair coin at each tick. On heads walk up $\sqrt{\Delta t}$; on tails walk down $\sqrt{\Delta t}$. After time $t = k\,\Delta t$ the position is

$$
W_t^{(n)} = \sqrt{\Delta t}\,(\xi_1 + \cdots + \xi_k), \qquad \xi_i = \pm 1 \text{ with equal probability}.
$$

Each step has mean $0$ and variance $\Delta t$, so the sum of $k$ steps has mean $0$ and variance $k\,\Delta t = t$. The central limit theorem — a sum of many small independent kicks becomes a bell curve — says that for large $n$ the position at a fixed $t$ is approximately $\mathcal{N}(0,t)$. Send $n\to\infty$ and the staircase becomes a continuous scribble. That scribble is Brownian motion.

![A fair coin-flip walk becoming Brownian motion](/blog/assets/2024/bsm/random-walk-to-brownian.png)

The three panels are the *same* sequence of coin flips, grouped into fewer, larger steps on the left and drawn almost continuously on the right. Brownian motion is the right-hand picture, taken as a mathematical limit.

## The four properties, in symbols

A **standard Brownian motion** is a random function $t\mapsto W_t$ satisfying:

1. **Starts at zero.** $W_0 = 0$.
2. **Independent increments.** For $t>s$, the future step $W_t-W_s$ does not depend on the path before time $s$. The next wiggle does not remember how it got here.
3. **Gaussian increments.** $W_t - W_s \sim \mathcal{N}(0,\, t-s)$. In words: over an interval of length $\Delta t$ the step is drawn from a bell curve with mean $0$ and variance $\Delta t$. In particular the position itself is
   $$
   W_t \sim \mathcal{N}(0,t), \qquad \mathbb{E}[W_t] = 0, \qquad \mathrm{Var}(W_t) = t.
   $$
   The **typical size** of $W_t$ is therefore the standard deviation $\sqrt{t}$, not $t$. Over a short interval the typical move is $\sqrt{\Delta t}$, which is much larger than $\Delta t$ itself when $\Delta t$ is small.
4. **Continuous paths.** The graph of $t\mapsto W_t$ has no jumps. It is a jagged scribble with no breaks.

**Normal reminder.** We write $Z\sim\mathcal{N}(m,s^2)$ to mean that $Z$ has the bell-curve (**Gaussian**, **normal**) density

$$
f(z) = \frac{1}{s\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{z-m}{s}\Bigr)^2\Bigr).
$$

The number $m$ is the mean, $s^2$ is the variance. The **standard normal** is the special case $\mathcal{N}(0,1)$. Later we will need the **cumulative distribution function** (cdf) of this law: the area under the bell curve to the left of a point $x$, written

$$
\Phi(x) = P(Z\le x) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x} e^{-u^2/2}\,du, \qquad Z\sim\mathcal{N}(0,1).
$$

If that integral looks unfriendly, just remember: $\Phi(0)=1/2$ (half the bell is to the left of zero), $\Phi$ increases from $0$ to $1$, and $\Phi(-x)=1-\Phi(x)$. We will only ever *evaluate* $\Phi$, never compute the integral by hand.

![Standard Brownian motion: paths, the $\sqrt{t}$ envelope, and the law of $W_1$](/blog/assets/2024/bsm/brownian-motion.png)

On the left, every path starts at $0$ and wanders equally above and below the axis — several paths are *negative*, which a stock price cannot be. The shaded trumpet is the band $\pm 2\sqrt{t}$; at each fixed $t$ about 95% of paths sit inside it, because a normal random variable is within two standard deviations of its mean about 95% of the time. On the right, many independent runs are stopped at $t=1$ and histogrammed. The histogram is the $\mathcal{N}(0,1)$ density, which is property 3 at $t=1$.

## The increment $dW_t$, and why ordinary calculus fails

Write $dW_t$ for the increment of $W$ over an instant of length $dt$. Property 3 says $dW_t$ is approximately $\mathcal{N}(0,dt)$, so $(dW_t)^2$ is typically of size $dt$, not $(dt)^2$. That is the multiplication table we will use:

$$
dt\cdot dt \to 0, \qquad dt\cdot dW_t \to 0, \qquad dW_t\cdot dW_t \to dt.
$$

The third rule has a name, **quadratic variation**. Chop $[0,t]$ into $n$ steps of length $\Delta t=t/n$. Each increment $\Delta W_i$ satisfies $\mathbb{E}[(\Delta W_i)^2]=\Delta t$, so the sum of the squares has expectation $t$. The variance of that sum shrinks like $1/n$ and vanishes as $n\to\infty$. The sum of squared wiggles converges to $t$: in the infinitesimal shorthand, $(dW_t)^2=dt$. Ordinary calculus throws $(dx)^2$ away. Here it is the same size as $dt$, so it must be kept. That is why, when we later differentiate functions of $S_t$, we will need Itô's lemma rather than the chain rule from Calculus 1.

The paths are so jagged that, with probability $1$, they have no tangent line anywhere. You cannot write $dW_t/dt$. You can only write $dW_t$.

---

# The stock: geometric Brownian motion
{: #the-stock-geometric-brownian-motion}

$W_t$ is a bad model for a stock. It can be negative, and a \$100 stock and a \$10 stock should not make dollar moves of the same typical size. The model used here is **geometric Brownian motion**: the *percentage* move is Brownian.

$$
dS_t = \mu S_t\,dt + \sigma S_t\,dW_t. \tag{2}
$$

Read the equation as a recipe for a short interval $dt$:

- the stock grows by a deterministic fraction $\mu\,dt$ (the **drift** $\mu$ is the expected rate of return);
- plus a random fraction $\sigma\,dW_t$ (the **volatility** $\sigma$ scales the Brownian increment).

Because the noise is multiplied by the current price $S_t$, a \$200 stock wiggles twice as many dollars as a \$100 stock, and $S_t$ stays positive. The $d$ on the left is the same kind of increment as $dW_t$: it is not a derivative, it is a small change.

![Geometric Brownian motion: stock paths, which stay positive](/blog/assets/2024/bsm/gbm-paths.png)

Each path is one draw of $W$, turned into a price by $(2)$. Compare with the previous figure: these paths cannot cross zero, and they spread in proportion to the level of $S$. A European call with the dashed strike pays the excess over $100$ if the path ends above the line, and zero otherwise. Pricing the call is averaging that payoff over every such path — under a fair-game probability we will define after the assumptions, not under the real-world drift $\mu$.

---

# Assumptions
{: #assumptions}

Four assumptions do the mathematics. A fifth is the trading plumbing that lets the mathematics be a *price*.

1. **The stock follows the geometric Brownian motion $(2)$, with $\mu$ and $\sigma$ constant.** One source of randomness, namely the single Brownian motion $W_t$. No sudden jumps, no volatility that itself wiggles. This is what makes $S_T$ lognormal.

2. **The interest rate $r$ is a known constant.** You may borrow or lend any amount at this rate. A dollar deposited in the **money-market account** (a riskless savings account) grows to $B_t = e^{rt}$. The exponential is **continuous compounding**: interest is added every instant, so the growth factor over time $t$ is $e^{rt}$ rather than $(1+r)^t$. Merton later let $r$ wander; the two-$\Phi$ formula does not survive that generalization in this form.

3. **No dividends during the life of the option.** A cash dividend drops $S$ by the amount paid and would change both the hedge and the law of $S_T$. The repair, recorded at the end, is one letter: a continuous yield $q$ replaces $S_t$ by $S_t e^{-q\tau}$ and $r$ by $r-q$ inside $d_1,d_2$.

4. **No arbitrage, continuous trading, a complete market.** An **arbitrage** is a riskless profit — a free lunch. **Continuous trading** means you may rebalance at every instant. A market is **complete** when every payoff you can write down can be manufactured by trading the stock and the money-market account. Here there is one source of noise and two traded assets, so the market is complete. The manufactured (replicating) portfolio's value *is* the price, and that is why the physical drift $\mu$ will cancel: the hedge does not contain it.

Plumbing, said once: you may sell a stock you do not own (**short selling**) and use the cash, securities may be held in any fractional amount, and there are no transaction costs. None of that enters an integral.

The gap between this universe and listed options is the subject of Derman and Miller's *The Volatility Smile*. The market still *quotes* in the language of the formula we are about to write.

---

# Martingales
{: #martingales}

A **stochastic process** is a family of random variables indexed by time — a random path. A process $M_t$ is a **martingale** if

$$
\mathbb{E}[M_T\mid \text{information up to time }t] = M_t.
$$

In words: a martingale is a **fair game**. Given what you know now, the expected future value *is* the present value. You should not expect to win or to lose. The notation $\mathcal{F}_t$ is the usual name for “the information available at time $t$,” so the same sentence is written $\mathbb{E}[M_T\mid\mathcal{F}_t]=M_t$.

Brownian motion itself is a martingale: $\mathbb{E}[W_T\mid W_t]=W_t$, because the remaining increment $W_T-W_t$ has mean $0$ and is independent of the past. The physical stock $S_t$ is *not* a martingale — it has drift $\mu$, which is why anyone bothers to own it.

Derivative pricing lives on a different assignment of probabilities, written $\mathbb{Q}$ and called the **risk-neutral measure**. A **probability measure** is just a consistent way of assigning probabilities to outcomes. The real-world measure is written $\mathbb{P}$. We say $\mathbb{Q}$ is **equivalent** to $\mathbb{P}$ when the two agree on which events are impossible (probability zero); they may disagree on how likely the possible events are. Under $\mathbb{Q}$ the **discounted** stock $S_t/B_t$ — the stock measured in time-$0$ dollars, by dividing out the growth of the money-market account — **is** a martingale: every traded asset earns $r$ on average, so risk is not paid extra. The call price is then an expectation under this fair-game measure, multiplied by $e^{-r\tau}$ to bring the future payoff back to today.

Two stand-ins, for the rest of the note:

- Brownian motion $W_t$ stands in for the market's noise.
- A martingale stands in for the market's fairness, once the probabilities have been changed so that risk is not paid extra.

---

# Itô's lemma
{: #itos-lemma}

You already know the chain rule. If $f$ is a smooth function of a smooth path $x(t)$, then $df = f'(x)\,dx$. Taylor's formula actually produces a second term, $\tfrac12 f''(x)\,(dx)^2$, which Calculus 1 throws away because $(dx)^2$ is negligible compared to $dx$.

For Brownian motion that discard is illegal: $(dW_t)^2 = dt$, same size as the terms you kept. **Itô's lemma** is the chain rule with that leftover put back.

Let $X_t$ satisfy $dX_t = a\,dt + b\,dW_t$, with $a$ and $b$ allowed to depend on $X$ and $t$. For a function $f(t,x)$ that is twice differentiable in $x$ and once in $t$ (the usual meaning of **smooth** here),

$$
df(t,X_t) = \Bigl(f_t + a f_x + \tfrac12 b^2 f_{xx}\Bigr)dt + b f_x\,dW_t. \tag{3}
$$

The first two terms in the $dt$ coefficient are the ordinary chain rule. The third is Itô's correction. It is present because Taylor's formula produces a $\tfrac12 f_{xx}(dX)^2$ term and $(dX)^2 = b^2\,dt$ is of order $dt$, not smaller.

Apply this to $f(s)=\ln s$ and to the stock $(2)$. Then $f_s = 1/s$, $f_{ss} = -1/s^2$, and

\begin{align*}
d\ln S_t
&= \frac{1}{S_t}\,dS_t + \tfrac12\Bigl(-\frac{1}{S_t^2}\Bigr)(\sigma S_t\,dW_t)^2 \\
&= \mu\,dt + \sigma\,dW_t - \tfrac12\sigma^2\,dt \\
&= \bigl(\mu - \tfrac12\sigma^2\bigr)dt + \sigma\,dW_t.
\end{align*}

The correction *lowers* the drift of the logarithm by $\tfrac12\sigma^2$. Integrate from $t$ to $T$ and use $W_T-W_t \stackrel{d}{=} \sqrt{\tau}\,Z$ with $Z\sim\mathcal{N}(0,1)$:

$$
S_T = S_t\exp\Bigl(\bigl(\mu-\tfrac12\sigma^2\bigr)\tau + \sigma\sqrt{\tau}\,Z\Bigr). \tag{4}
$$

Thus $\ln S_T$ is Gaussian, so $S_T$ is **lognormal**, with

$$
\mathbb{E}[\ln S_T\mid S_t] = \ln S_t + \bigl(\mu-\tfrac12\sigma^2\bigr)\tau, \qquad \mathrm{Var}(\ln S_T\mid S_t) = \sigma^2\tau.
$$

The $\tfrac12\sigma^2$ that left the log-drift returns in the mean of the lognormal: $\mathbb{E}[S_T\mid S_t] = S_t e^{\mu\tau}$. Nothing is lost. It is booked in a different ledger. Under the fair-game probabilities of the next section the same calculation will hold with $\mu$ replaced by $r$, and that lognormal is the one we will integrate against.

We now have the four tools. Time to write the price.

---

# The Black–Scholes–Merton formula
{: #the-blackscholesmerton-formula}

Fischer Black and Myron Scholes published the following in 1973; Robert Merton derived the same price from a more general theory the same year. The **spot** $S_t$ is the stock price right now. The **volatility** $\sigma$ is how wildly the *logarithm* of the stock wiggles, measured as a standard deviation per square-root year. The **time remaining** is $\tau = T-t$. The risk-free interest rate $r$ is constant. Then the European call is worth

$$
C(S_t,K,T) = S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2), \tag{1}
$$

$$
d_1 = \frac{\ln(S_t/K)+\bigl(r+\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}, \qquad d_2 = d_1 - \sigma\sqrt{\tau}.
$$

In English, before we derive it: the call is a package of $\Phi(d_1)$ shares, minus a package of $K$ dollars delivered at expiry with probability $\Phi(d_2)$, brought back to today by the discount $e^{-r\tau}$. The two numbers $d_1$ and $d_2$ are just places on the bell curve. We will see exactly which places.

![A European call: the kink at expiry, the smooth price today](/blog/assets/2024/bsm/call-payoff.png)

The brown line is the expiry payoff you already understand. The blue curve is $(1)$, drawn as a function of today's spot, with one year left, $r=5\%$, $\sigma=20\%$. The shaded gap is **time value**: extra worth from still having time left for the stock to wander. The rest of the note is why the blue curve is that shape.

## A numerical check
{: #a-numerical-check}

Take the call we walked through by hand: spot $S = 100$, strike $K = 100$, one year left, $r = 5\%$, $\sigma = 20\%$. Then

$$
d_1 = \frac{\ln(1) + (0.05 + 0.02)\cdot 1}{0.20} = 0.35, \qquad d_2 = 0.15,
$$

$\Phi(0.35) \approx 0.6368$, $\Phi(0.15) \approx 0.5596$, and

$$
C \approx 100\cdot 0.6368 - 100\cdot e^{-0.05}\cdot 0.5596 \approx 10.45.
$$

So the rain check on a 100-dollar stock, struck at 100, one year out, is worth about ten dollars and forty-five cents. That is the number the algebra below is trying to explain.

<table>
  <thead>
    <tr>
      <th>Symbol</th>
      <th>Meaning</th>
      <th>In the example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>\(S\)</td>
      <td>spot — the stock price right now</td>
      <td>100</td>
    </tr>
    <tr>
      <td>\(K\)</td>
      <td>strike — the price the call lets you buy at</td>
      <td>100</td>
    </tr>
    <tr>
      <td>\(r\)</td>
      <td>risk-free interest rate, compounded continuously, held constant</td>
      <td>0.05</td>
    </tr>
    <tr>
      <td>\(\tau = T-t\)</td>
      <td>time remaining until expiry, in years</td>
      <td>1</td>
    </tr>
    <tr>
      <td>\(\sigma\)</td>
      <td>volatility — standard deviation of the log return, per square-root year</td>
      <td>0.20</td>
    </tr>
    <tr>
      <td>\(\Phi\)</td>
      <td>standard normal cdf, \(P(Z\le x)\), defined above</td>
      <td>\(\Phi(0.35)\approx 0.6368\), \(\Phi(0.15)\approx 0.5596\)</td>
    </tr>
  </tbody>
</table>

The same arithmetic in Python:

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

---

# Risk-neutral pricing
{: #risk-neutral-pricing}

Equation $(1)$ does not contain $\mu$, the stock's expected return. That is the first surprise, and it is the reason a market can exist: two people who disagree about whether the stock will go up can still agree on the call price, provided they agree on $\sigma$.

The mechanism is a change of probabilities. We already named the fair-game measure $\mathbb{Q}$ in the martingales section. Here is how you get there from the real world.

**Girsanov's theorem** is the fact that you may add a drift to a Brownian motion and still have a Brownian motion, provided you change which paths you treat as likely. The tilt we want is the **market price of risk** $\theta = (\mu-r)/\sigma$: excess return on the stock per unit of volatility. Set

$$
W_t^{\mathbb{Q}} = W_t + \theta t.
$$

Then $W^{\mathbb{Q}}$ is Brownian motion under the risk-neutral measure $\mathbb{Q}$ (the notation $\mathbb{Q}\sim\mathbb{P}$ means the two measures are equivalent: they agree on which events are impossible). Substitute $dW = dW^{\mathbb{Q}} - \theta\,dt$ into $(2)$:

\begin{align*}
dS_t
&= \mu S_t\,dt + \sigma S_t\bigl(dW_t^{\mathbb{Q}} - \theta\,dt\bigr) \\
&= r S_t\,dt + \sigma S_t\,dW_t^{\mathbb{Q}}. \tag{5}
\end{align*}

The physical drift $\mu$ has been replaced by $r$. That is the content of "risk-neutral."

Let $\tilde S_t = S_t e^{-rt}$ be the stock in time-$0$ dollars. The ordinary product rule, plus Itô (the mixed increment $dS\cdot d(e^{-rt})$ is a $dW\cdot dt$ term, which the multiplication table sends to $0$), gives, under $\mathbb{Q}$,

$$
d\tilde S_t = \sigma\tilde S_t\,dW_t^{\mathbb{Q}}.
$$

No $dt$ term: $\tilde S$ is a $\mathbb{Q}$-martingale, so $\mathbb{E}^{\mathbb{Q}}[\tilde S_T\mid\mathcal{F}_t] = \tilde S_t$. In a complete, arbitrage-free market the time-$t$ price of a payoff $h(S_T)$ is the discounted risk-neutral expectation

$$
V(S_t,t) = e^{-r\tau}\,\mathbb{E}^{\mathbb{Q}}\bigl[h(S_T)\bigm\vert\mathcal{F}_t\bigr].
$$

For the call, $h(x)=(x-K)^+$:

$$
C(S_t,K,T) = e^{-r\tau}\,\mathbb{E}^{\mathbb{Q}}\bigl[(S_T-K)^+\bigm\vert\mathcal{F}_t\bigr]. \tag{6}
$$

Under $\mathbb{Q}$, $(4)$ holds with $\mu=r$, so $S_T$ is lognormal with parameters

$$
m = \ln S_t + \bigl(r-\tfrac12\sigma^2\bigr)\tau, \qquad s^2 = \sigma^2\tau. \tag{7}
$$

Equation $(6)$ is now an integral against that lognormal. Two traders who disagree about $\mu$ still agree on $C$ if they agree on $\sigma$: $\mu$ is not in $(7)$.

---

# Toolkit: the lognormal
{: #toolkit-the-lognormal}

This is the engine. Let $Y\sim\mathcal{N}(m,s^2)$ and $X=e^Y$, so $X$ is lognormal and $X>0$ with probability $1$. Completing the square in the Gaussian integral for $e^Y$ gives the mean; a second moment computation gives the variance:

$$
\mathbb{E}[X] = e^{m+s^2/2}, \qquad \mathrm{Var}(X) = \bigl(e^{s^2}-1\bigr)e^{2m+s^2}. \tag{8}
$$

The density of $X$ follows from the change of variable $y=\ln x$, $dy = dx/x$:

$$
f_X(x) = \frac{1}{s\,x\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{\ln x-m}{s}\Bigr)^2\Bigr), \qquad x>0. \tag{9}
$$

The extra $1/x$ is the stretching factor from the substitution (sometimes called the Jacobian): $dy=dx/x$. The cdf is the Gaussian cdf evaluated at $\ln x$:

$$
F_X(x) = \Phi\Bigl(\frac{\ln x-m}{s}\Bigr). \tag{10}
$$

The call does not need $\mathbb{E}[X]$ and does not need $\mathbb{E}[X\mid X>K]$. It needs the contribution of the upper tail, the **partial expectation**

$$
L_X(K) := \mathbb{E}\bigl[X\,1_{\{X>K\}}\bigr] = \int_K^{\infty} x\,f_X(x)\,dx. \tag{11}
$$

The symbol $1_{\{X>K\}}$ is the **indicator** of the event $\{X>K\}$: it equals $1$ when $X>K$ and $0$ otherwise, so $X\,1_{\{X>K\}}$ keeps $X$ on the upper tail and throws the rest away.

This is not the conditional tail expectation $\mathbb{E}[X\mid X>K]$, which would divide $(11)$ by $1-F_X(K)$. (That mix-up appears in some notes, including Rouah's; the integral they write is $(11)$, and $(11)$ is the object that enters the call.)

Substitute $(9)$. The $x$ in the integrand cancels the $1/x$ in the density:

$$
L_X(K) = \int_K^{\infty} \frac{1}{s\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{\ln x-m}{s}\Bigr)^2\Bigr)\,dx.
$$

Change variable $y=\ln x$, so $x=e^y$ and $dx=e^y\,dy$. The lower limit becomes $\ln K$:

$$
L_X(K) = \int_{\ln K}^{\infty} \frac{e^y}{s\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{y-m}{s}\Bigr)^2\Bigr)\,dy. \tag{12}
$$

The exponent in the integrand is $y - (y-m)^2/(2s^2)$. Expand the square and collect terms over a common denominator:

\begin{align*}
y - \frac{(y-m)^2}{2s^2}
&= \frac{2s^2 y - (y^2 - 2my + m^2)}{2s^2}
= \frac{-y^2 + 2(m+s^2)y - m^2}{2s^2}.
\end{align*}

Rewrite the quadratic in $y$ by completing the square. The identity $y^2 - 2(m+s^2)y = \bigl(y-(m+s^2)\bigr)^2 - (m+s^2)^2$ turns the numerator into

$$
-\bigl(y-(m+s^2)\bigr)^2 + (m+s^2)^2 - m^2 = -\bigl(y-(m+s^2)\bigr)^2 + 2ms^2 + s^4.
$$

Divide by $2s^2$:

$$
y - \frac{(y-m)^2}{2s^2} = -\frac{\bigl(y-(m+s^2)\bigr)^2}{2s^2} + m + \frac{s^2}{2}.
$$

The constant $m+s^2/2$ comes out of the integral, and what remains is a normal density with mean $m+s^2$ and variance $s^2$:

$$
L_X(K) = e^{m+s^2/2}\int_{\ln K}^{\infty}\frac{1}{s\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{y-(m+s^2)}{s}\Bigr)^2\Bigr)\,dy. \tag{13}
$$

The integral is $\mathbb{P}\bigl(\mathcal{N}(m+s^2,\,s^2)>\ln K\bigr)$, which in standard units is $\Phi\bigl((-\ln K+m+s^2)/s\bigr)$. Therefore

$$
L_X(K) = e^{m+s^2/2}\,\Phi\Bigl(\frac{-\ln K + m + s^2}{s}\Bigr). \tag{14}
$$

That is the identity Route I spends. Completing the square shifted the mean of $Y$ from $m$ to $m+s^2$. In the call, that shift is exactly the gap between $d_2$ and $d_1$.

---

# Route I: two lognormal integrals
{: #route-i-two-lognormal-integrals}

Start from $(6)$ and split the payoff on the event $\{S_T>K\}$. Write $F$ for the cdf of $S_T$ under $\mathbb{Q}$, so $\int g\,dF$ means the expected value of $g(S_T)$ — if $F$ has density $f$, this is the ordinary integral $\int g(x)\,f(x)\,dx$:

\begin{align*}
C
&= e^{-r\tau}\int_K^{\infty}(S_T-K)\,dF(S_T) \\
&= e^{-r\tau}\int_K^{\infty} S_T\,dF(S_T) \;-\; e^{-r\tau}K\int_K^{\infty} dF(S_T). \tag{15}
\end{align*}

Under $\mathbb{Q}$, $S_T$ is lognormal with the parameters $(7)$. The first integral is the partial expectation $L_{S_T}(K)$. Feed $(7)$ into $(14)$:

\begin{align*}
e^{m+s^2/2}
&= \exp\Bigl(\ln S_t + \bigl(r-\tfrac12\sigma^2\bigr)\tau + \tfrac12\sigma^2\tau\Bigr)
= S_t e^{r\tau},
\end{align*}

and the argument of $\Phi$ is

\begin{align*}
\frac{-\ln K + m + s^2}{s}
&= \frac{-\ln K + \ln S_t + \bigl(r-\tfrac12\sigma^2\bigr)\tau + \sigma^2\tau}{\sigma\sqrt{\tau}}
= \frac{\ln(S_t/K)+\bigl(r+\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}
= d_1.
\end{align*}

So $L_{S_T}(K) = S_t e^{r\tau}\,\Phi(d_1)$, and the first term of $(15)$ is $S_t\Phi(d_1)$.

The second integral is the upper tail of the cdf. By $(10)$,

$$
\int_K^{\infty} dF(S_T) = 1 - F(K) = 1 - \Phi\Bigl(\frac{\ln K - m}{s}\Bigr).
$$

The argument is

$$
\frac{\ln K - m}{s} = \frac{\ln K - \ln S_t - \bigl(r-\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}} = -d_2,
$$

and $1-\Phi(-d_2)=\Phi(d_2)$. The second term of $(15)$ is therefore $K e^{-r\tau}\Phi(d_2)$. Combine:

$$
C = S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2),
$$

which is $(1)$.

**Reading the two terms.** $\Phi(d_2)=\mathbb{Q}(S_T>K)$ is the risk-neutral probability of exercise, so the second term is a **cash-or-nothing** contract: $K$ dollars paid at $T$ if and only if the call finishes **in the money** ($S_T>K$), and nothing otherwise. (A claim to one dollar at $T$ is a **zero-coupon bond**, worth $e^{-r\tau}$ today, which is why $K$ is multiplied by $e^{-r\tau}$.) The first term is a **share-or-nothing**: you receive one share if $S_T>K$, and nothing otherwise. $\Phi(d_1)$ is the same exercise probability after the mean shift $m\mapsto m+s^2$ that $(14)$ performed — equivalently, as Route II will show, the exercise probability when the unit of account is the stock itself.

![Two evaluations of the same bell curve](/blog/assets/2024/bsm/phi-anatomy.png)

For the at-the-money numbers above (spot equals strike), $d_1$ and $d_2$ sit $\sigma\sqrt{\tau}=0.20$ apart. That gap is the Itô correction, visible on the page.

**Put-call parity.** A European call minus a European put with the same strike and expiry is a **forward** — a contract that obliges you to buy the stock at $K$ at time $T$, with no choice. A forward on a non-dividend stock is worth $S_t - K e^{-r\tau}$:

$$
C - P = S_t - K e^{-r\tau}.
$$

This is an accounting identity, not a pricing model. Substitute $(1)$:

$$
P = K e^{-r\tau}\,\Phi(-d_2) - S_t\,\Phi(-d_1).
$$

For those same numbers, $P\approx 5.57$. The call is worth more than the put because the forward is already profitable once $r>0$.

**Remark (standard-normal coordinates).** Writing $S_T = S_t\exp\bigl((r-\sigma^2/2)\tau + \sigma\sqrt{\tau}\,Z\bigr)$ with $Z\sim\mathcal{N}(0,1)$, the event $\{S_T>K\}$ becomes $\{Z>-d_2\}$, and the partial expectation $\mathbb{E}[S_T 1_{\{Z>-d_2\}}]$ is the same completed square as $(12)$–$(14)$, now in the variable $Z$. Same algebra, different name for the integration variable.

---

# Route II: change of numeraire
{: #route-ii-change-of-numeraire}

A **numeraire** is the asset used as the unit of account. Quote everything in dollars and the numeraire is the money-market account $B_t=e^{rt}$. Quote everything in *shares* and the numeraire is $S_t$. For a numeraire $N$ there is a measure $\mathbb{N}$ that makes every asset, divided by $N$, a martingale, and the price of a payoff $V(S_T,T)$ is

$$
V(S_t,t) = N_t\;\mathbb{E}^{\mathbb{N}}\left[\frac{V(S_T,T)}{N_T}\,\Bigm\vert\,\mathcal{F}_t\right]. \tag{16}
$$

For $N=B$ this is $(6)$ and $\mathbb{N}=\mathbb{Q}$. Take $N=S$ instead. The call, measured in shares, is $(1-KZ_T)^+$ with $Z=1/S$, and $\Phi(d_1)$ will appear as an ordinary probability under the associated measure $\mathbb{Q}^{S}$.

Start from $(5)$. The relative bond $\tilde B_t = B_t/S_t$ is not a $\mathbb{Q}$-martingale: Itô produces leftover drift $\sigma^2$. Kill it by Girsanov in the other direction,

$$
W_t^{\mathbb{Q}^{S}} = W_t^{\mathbb{Q}} - \sigma t,
$$

so $d\tilde B_t = -\sigma\tilde B_t\,dW_t^{\mathbb{Q}^{S}}$ is a $\mathbb{Q}^{S}$-martingale. Relative to the stock, the bond is now a fair game.

For $Z_t=1/S_t$ the derivatives are $Z_S=-1/S^2$ and $Z_{SS}=2/S^3$. Itô plus $(5)$, then the change of Brownian motion, gives

$$
dZ_t = -r Z_t\,dt - \sigma Z_t\,dW_t^{\mathbb{Q}^{S}}.
$$

One more Itô, on $Y=\ln Z$:

$$
dY_t = -\bigl(r+\tfrac12\sigma^2\bigr)dt - \sigma\,dW_t^{\mathbb{Q}^{S}}.
$$

So $\ln Z_T$ is normal with mean and variance

$$
u = -\ln S_t - \bigl(r+\tfrac12\sigma^2\bigr)\tau, \qquad v=\sigma^2\tau,
$$

and $Z_T$ is lognormal. In particular $\mathbb{E}^{\mathbb{Q}^{S}}[Z_T]=e^{u+v/2}=e^{-r\tau}/S_t$, which is the martingale property $\mathbb{E}^{\mathbb{Q}^{S}}[B_T/S_T]=B_t/S_t$.

The share-denominated call is nonzero when $Z_T<1/K$. Equation $(16)$ becomes

$$
C = S_t\,\mathbb{E}^{\mathbb{Q}^{S}}\bigl[(1-KZ_T)^+\bigm\vert\mathcal{F}_t\bigr] = S_t\bigl(I_1-I_2\bigr),
$$

$$
I_1 = \mathbb{Q}^{S}\bigl(Z_T<1/K\bigr), \qquad I_2 = K\,\mathbb{E}^{\mathbb{Q}^{S}}\bigl[Z_T\,1_{\{Z_T<1/K\}}\bigr].
$$

By the lognormal cdf $(10)$,

$$
I_1 = \Phi\Bigl(\frac{\ln(1/K)-u}{\sqrt{v}}\Bigr) = \Phi(d_1).
$$

$\Phi(d_1)$ is the probability of exercise when the unit of account is the stock.

The second piece is $K$ times a lower-tail partial expectation, which is the full mean minus the upper-tail identity $(14)$ applied to $Z$ at the barrier $1/K$. The $\Phi$ argument of that upper tail is $-d_2$, so

$$
I_2 = K\Bigl(e^{u+v/2}-e^{u+v/2}\Phi(-d_2)\Bigr) = K\cdot\frac{e^{-r\tau}}{S_t}\cdot\Phi(d_2).
$$

Therefore

$$
C = S_t\bigl(\Phi(d_1)-\tfrac{K e^{-r\tau}}{S_t}\Phi(d_2)\bigr) = S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2).
$$

Same formula. The two $\Phi$ terms are now both probabilities, each belonging to the numeraire that multiplies it.

<table>
  <thead>
    <tr>
      <th>Numeraire</th>
      <th>Measure</th>
      <th>Martingale</th>
      <th>\(\mathbb{Q}^{\,\cdot}(S_T&gt;K)\)</th>
      <th>Role in (1)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>bond \(B_{t}=e^{rt}\)</td>
      <td>\(\mathbb{Q}\)</td>
      <td>\(S_{t}/B_{t}\)</td>
      <td>\(\Phi(d_{2})\)</td>
      <td>multiplies the cash \(Ke^{-r\tau}\)</td>
    </tr>
    <tr>
      <td>stock \(S_{t}\)</td>
      <td>\(\mathbb{Q}^{S}\)</td>
      <td>\(B_{t}/S_{t}\)</td>
      <td>\(\Phi(d_{1})\)</td>
      <td>multiplies the share \(S_{t}\)</td>
    </tr>
  </tbody>
</table>

---

# The PDE, briefly
{: #the-pde-briefly}

Black and Scholes did not start from $(6)$. They started from a portfolio $\Pi=-V+\Delta S$ (short one option, long $\Delta$ shares). Expand $dV$ with Itô's lemma, choose $\Delta=V_S$ so the $dW$ terms cancel — that choice is **delta-hedging**, and $V_S$ is the **delta** of the option — and require the now-riskless $\Pi$ to earn $r$, or else there is an arbitrage against the money-market account. The result is the Black–Scholes **partial differential equation** (PDE): an equation relating the partial derivatives of $V$ with respect to $t$ and $S$,

$$
V_t + rS V_S + \tfrac12\sigma^2 S^2 V_{SS} - rV = 0, \tag{17}
$$

with $V(S,T)=(S-K)^+$. The drift $\mu$ cancelled with the $dW$ terms. The second derivative $V_{SS}$ is the **gamma**; $\tfrac12\sigma^2 S^2 V_{SS}$ is Itô's correction, now sitting in a PDE.

The **Feynman–Kac theorem** is the dictionary between $(17)$ and $(6)$: a PDE of this shape, with drift coefficient $rS$ and discount $r$, is solved by $e^{-r\tau}\mathbb{E}^{\mathbb{Q}}[h(S_T)\mid S_t]$ along the stock $(5)$. The hedging argument produces the PDE; Feynman–Kac translates it into the integral Route I already evaluated.

A further change of variables — $x=\ln(S/K)$, time-to-go rescaled by $\sigma^2/2$, an exponential prefactor to absorb discounting — turns $(17)$ into the **heat equation** $W_{\tilde\tau}=W_{xx}$, the same PDE that describes temperature spreading along a rod. The solution that starts as a spike at the origin and then smears out is a Gaussian (the **heat kernel**). Integrate a Gaussian and you get $\Phi$. The algebra is written out in Rouah §7 of the [hosted note](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf). The bell curve in $(1)$ is both the law of where geometric Brownian motion ends up and the shape of spreading heat: the same assumption, two costumes.

---

# Limitations
{: #limitations}

**Dividends.** A continuous yield $q$ changes the risk-neutral drift of $S$ from $r$ to $r-q$. The same Route I, with $m=\ln S_t+(r-q-\sigma^2/2)\tau$, produces Merton's formula

$$
C = S_t e^{-q\tau}\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2),
$$

$r$ replaced by $r-q$ inside $d_1$ and $d_2$ as well. Index options live here ($q$ is the basket yield), FX options live here ($q$ is the foreign rate), and futures options live here ($q=r$: Black 1976).

**The smile.** After 1987 the market stopped believing in a single $\sigma$. **Implied volatility** is the number $\sigma$ you must feed into $(1)$ to recover the price the market is actually quoting. Plot that number against strike and you get a smile, or in equities a smirk. Traders still quote in Black–Scholes implied vol. They do not believe the lognormal assumption that produced it.

**Jumps, stochastic vol, Americans.** Merton added sudden jumps (a Poisson process: events that arrive at random times). Heston let $\sigma_t$ itself wander. Dupire showed that a whole surface of implied vols is equivalent to a local-vol model — $\sigma$ depends on $S$ and $t$ — that refits every ordinary call and put. None of these has a two-$\Phi$ formula of the same shape. The American put has no closed form of this kind; a binomial tree (the coin-flip walk, used as a calculator) is the honest computation.

What has been proved is a theorem about a complete market driven by one Brownian motion: the unique no-arbitrage price of $(S_T-K)^+$ is $(1)$. Using that theorem as a price, as a quoting convention, or as the first term of an approximation is a separate decision.

---

# References
{: #references}

- Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. [Local copy](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf). [Wayback, 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf).
- F. Black and M. Scholes, [The Pricing of Options and Corporate Liabilities](https://www.cs.princeton.edu/courses/archive/fall09/cos323/papers/black_scholes73.pdf), *JPE* 81 (1973).
- R. C. Merton, [Theory of Rational Option Pricing](https://www.jstor.org/stable/3003143), *Bell Journal* 4 (1973).
- K. Itô, [On Stochastic Differential Equations](https://projecteuclid.org/euclid.memo/1183518816), *Mem. AMS* (1951).
- J. Hull, *Options, Futures, and Other Derivatives*.
- S. Shreve, *Stochastic Calculus for Finance II*.
- E. Derman and M. B. Miller, *The Volatility Smile*.
