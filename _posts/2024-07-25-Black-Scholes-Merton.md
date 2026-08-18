---
layout: post
title: "Back-of-the-Envelope: Black-Scholes-Merton"
date: 2024-07-24
categories: wealth
mathjax: true
---

The Black–Scholes–Merton formula prices a European call on a non-dividend stock. Fischer Black and Myron Scholes published the PDE and its solution in 1973; Robert Merton derived the same price from a more general theory the same year. The inputs are the spot $S_t$, the strike $K$, the time to expiry $\tau = T-t$, a constant interest rate $r$, and a constant volatility $\sigma$. The output is

$$
C(S_t,K,T) = S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2), \tag{1}
$$

$$
d_1 = \frac{\ln(S_t/K)+\bigl(r+\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}, \qquad d_2 = d_1 - \sigma\sqrt{\tau},
$$

where $\Phi$ is the standard normal cdf,

$$
\Phi(x) = \frac{1}{\sqrt{2\pi}}\int_{-\infty}^{x} e^{-u^2/2}\,du.
$$

This note derives $(1)$ from the lognormal law of $S_T$. The stock is a geometric Brownian motion; Itô's lemma makes $\ln S_T$ Gaussian; under the risk-neutral measure the parameters of that Gaussian are known; the call is then two integrals against a lognormal, and both integrals evaluate in closed form once you complete the square. A change of numeraire gives the same formula by a different bookkeeping. The PDE is recorded at the end as the same argument in another costume.

- [What is being priced](#what-is-being-priced)
- [A numerical check](#a-numerical-check)
- [Assumptions](#assumptions)
- [Wiener processes and martingales](#wiener-processes-and-martingales)
- [Itô's lemma](#itos-lemma)
- [Risk-neutral pricing](#risk-neutral-pricing)
- [Toolkit: the lognormal](#toolkit-the-lognormal)
- [Route I: two lognormal integrals](#route-i-two-lognormal-integrals)
- [Route II: change of numeraire](#route-ii-change-of-numeraire)
- [The PDE, briefly](#the-pde-briefly)
- [Limitations](#limitations)
- [References](#references)

The change-of-numeraire calculation follows Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. The original host is gone. A copy is [here](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf); the [Wayback capture of 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf) is the provenance.

---

# What is being priced
{: #what-is-being-priced}

A **European call** is the right, and not the obligation, to buy one share at a fixed strike $K$ at a single expiry $T$. At expiry the holder exercises if and only if $S_T > K$, so the payoff is

$$
(S_T - K)^+ = \max(S_T - K,\, 0).
$$

A **European put** is the right to sell at $K$, payoff $(K - S_T)^+$. An **American** contract may be exercised at any time up to $T$. That extra right is a genuine complication: the holder is solving an optimal-stopping problem, and there is no two-$\Phi$ formula for a general American put. One mercy, due to Merton: a call on a non-dividend stock is never exercised early, so the American call collapses to the European one. We price the European call. The European put then follows from put-call parity, not from a second integral.

![A European call: the kink at expiry, the smooth price today](/blog/assets/2024/bsm/call-payoff.png)

The brown line is the expiry payoff. The blue curve is the time-$t$ value of that lottery, for one year of remaining life and the parameters of the next section. The shaded gap is time value. Equation $(1)$ is a machine that draws the blue curve.

---

# A numerical check
{: #a-numerical-check}

Spot $S = 100$, strike $K = 100$, one year left, $r = 5\%$, $\sigma = 20\%$. Then

$$
d_1 = \frac{0 + (0.05 + 0.02)\cdot 1}{0.20} = 0.35, \qquad d_2 = 0.15,
$$

$\Phi(0.35) \approx 0.6368$, $\Phi(0.15) \approx 0.5596$, and

$$
C \approx 100\cdot 0.6368 - 100\cdot e^{-0.05}\cdot 0.5596 \approx 10.45.
$$

| Symbol | Meaning |
|---|---|
| $S_t$ | spot |
| $K$ | strike |
| $r$ | continuously compounded risk-free rate, constant |
| $\tau = T-t$ | time remaining, in years |
| $\sigma$ | volatility of the *log* return, per square-root year |
| $\Phi$ | standard normal cdf |

```python
from math import log, exp, sqrt, erf
Phi = lambda x: 0.5 * (1 + erf(x / sqrt(2)))
S, K, r, sig, tau = 100, 100, 0.05, 0.20, 1.0
d1 = (log(S/K) + (r + 0.5*sig*sig)*tau) / (sig*sqrt(tau))
d2 = d1 - sig*sqrt(tau)
print(S*Phi(d1) - K*exp(-r*tau)*Phi(d2))
# 10.450583572185565
```

---

# Assumptions
{: #assumptions}

Four assumptions do the mathematics. A fifth is the trading plumbing that lets the mathematics be a *price*.

1. **The stock is a geometric Brownian motion with constant coefficients.**
   $$
   dS_t = \mu S_t\,dt + \sigma S_t\,dW_t. \tag{2}
   $$
   Prices stay positive, returns compound, and the only randomness is a single Wiener process $W_t$. No jumps, no stochastic volatility. This is what makes $S_T$ lognormal.

2. **The short rate $r$ is a known constant.** Borrowing and lending are unlimited at $r$. The money-market account is then $B_t = e^{rt}$. Merton later let $r$ wander; the two-$\Phi$ formula does not survive that generalization in this form.

3. **No dividends during the life of the option.** A cash dividend drops $S$ by the amount paid and would change both the hedge and the law of $S_T$. The repair, recorded at the end, is one letter: a continuous yield $q$ replaces $S_t$ by $S_t e^{-q\tau}$ and $r$ by $r-q$ inside $d_1,d_2$.

4. **No arbitrage, continuous trading, a complete market.** One source of noise and two traded assets (stock and bond) means every reasonable payoff can be replicated. The replicating portfolio's value is the price, and that is why the physical drift $\mu$ will cancel: the hedge does not contain it.

Plumbing, said once: short sales are allowed, proceeds may be used, securities are perfectly divisible, there are no transaction costs. None of that enters an integral.

The gap between this universe and listed options is the subject of Derman and Miller's *The Volatility Smile*. The market still *quotes* in the language of $(1)$.

---

# Wiener processes and martingales
{: #wiener-processes-and-martingales}

The Wiener process $W_t$ (standard Brownian motion) is the stand-in for market noise: not for the *level* of prices, which have drift and stay positive, but for the irreducible jitter.

1. $W_0 = 0$.
2. Independent increments: $W_t - W_s$ is independent of the path up to $s$.
3. Gaussian increments: $W_t - W_s \sim \mathcal{N}(0,\,t-s)$. In particular the typical move over $\Delta t$ has size $\sqrt{\Delta t}$, not $\Delta t$.
4. Continuous paths, almost surely.

Paths are almost surely nowhere differentiable, so the ordinary chain rule does not apply. The multiplication table that replaces it is

$$
dt\cdot dt \to 0, \qquad dt\cdot dW_t \to 0, \qquad dW_t\cdot dW_t \to dt.
$$

The third rule is quadratic variation. Over a partition of $[0,t]$ into $n$ steps of length $\Delta t = t/n$, each increment satisfies $\mathbb{E}[(\Delta W_i)^2] = \Delta t$, the sum of the squares has expectation $t$, and the variance of that sum is $O(1/n)$. The sum converges to $t$ in probability: $\langle W\rangle_t = t$. In the infinitesimal shorthand, $(dW_t)^2 = dt$.

A process $M_t$ is a **martingale** if $\mathbb{E}[M_T\mid\mathcal{F}_t] = M_t$. Read $\mathcal{F}_t$ as the information available at time $t$. A martingale is a fair game: given what you know now, the expected future value is the present value. $W_t$ itself is a martingale. The physical stock $S_t$ is not — it has drift $\mu$. Derivative pricing lives on a different probability measure $\mathbb{Q}$, equivalent to the real-world measure $\mathbb{P}$, under which the *discounted* stock $S_t/B_t$ **is** a martingale. Under $\mathbb{Q}$ every traded asset earns $r$ on average. The call price is then an expectation under this fair-game measure, discounted at $r$.

Two stand-ins:

- $W_t$ stands in for the market's noise.
- A martingale stands in for the market's fairness, once the probabilities have been changed so that risk is not paid extra.

![Geometric Brownian motion: twelve draws of the same market](/blog/assets/2024/bsm/gbm-paths.png)

Each path is one realization of $W$, exponentiated so $S$ cannot go negative. A European call on the dashed strike pays the excess over $100$ if the path ends above the line, and zero otherwise. Pricing the call is averaging that payoff over every path, under $\mathbb{Q}$, not under $\mathbb{P}$.

---

# Itô's lemma
{: #itos-lemma}

Let $X_t$ satisfy $dX_t = a\,dt + b\,dW_t$, with $a$ and $b$ allowed to depend on $X$ and $t$. For smooth $f(t,x)$,

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

The $\tfrac12\sigma^2$ that left the log-drift returns in the mean of the lognormal: $\mathbb{E}[S_T\mid S_t] = S_t e^{\mu\tau}$. Nothing is lost. It is booked in a different ledger. Under $\mathbb{Q}$ the same calculation will hold with $\mu$ replaced by $r$, and that lognormal is the one Route I integrates against.

---

# Risk-neutral pricing
{: #risk-neutral-pricing}

Girsanov's theorem says a Brownian motion may be given an extra drift and remain a Brownian motion, provided the probabilities are changed. The tilt we want is the market price of risk $\theta = (\mu-r)/\sigma$, the stock's excess return per unit of volatility. Set

$$
W_t^{\mathbb{Q}} = W_t + \theta t.
$$

Then $W^{\mathbb{Q}}$ is Brownian motion under a measure $\mathbb{Q}\sim\mathbb{P}$. Substitute $dW = dW^{\mathbb{Q}} - \theta\,dt$ into $(2)$:

\begin{align*}
dS_t
&= \mu S_t\,dt + \sigma S_t\bigl(dW_t^{\mathbb{Q}} - \theta\,dt\bigr) \\
&= r S_t\,dt + \sigma S_t\,dW_t^{\mathbb{Q}}. \tag{5}
\end{align*}

The physical drift $\mu$ has been replaced by $r$. That is the content of "risk-neutral."

Let $\tilde S_t = S_t e^{-rt}$ be the stock in time-$0$ dollars. The product rule plus Itô (the cross variation $dS\cdot d(e^{-rt})$ vanishes) gives, under $\mathbb{Q}$,

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

This is the engine. Let $Y\sim\mathcal{N}(m,s^2)$ and $X=e^Y$, so $X$ is lognormal and $X>0$ almost surely. Completing the square in the Gaussian integral for $e^Y$ gives the mean; a second moment computation gives the variance:

$$
\mathbb{E}[X] = e^{m+s^2/2}, \qquad \mathrm{Var}(X) = \bigl(e^{s^2}-1\bigr)e^{2m+s^2}. \tag{8}
$$

The density of $X$ follows from the change of variable $y=\ln x$, $dy = dx/x$:

$$
f_X(x) = \frac{1}{s\,x\sqrt{2\pi}}\exp\Bigl(-\frac12\Bigl(\frac{\ln x-m}{s}\Bigr)^2\Bigr), \qquad x>0. \tag{9}
$$

The extra $1/x$ is the Jacobian. The cdf is the Gaussian cdf evaluated at $\ln x$:

$$
F_X(x) = \Phi\Bigl(\frac{\ln x-m}{s}\Bigr). \tag{10}
$$

The call does not need $\mathbb{E}[X]$ and does not need $\mathbb{E}[X\mid X>K]$. It needs the contribution of the upper tail, the **partial expectation**

$$
L_X(K) := \mathbb{E}\bigl[X\,1_{\{X>K\}}\bigr] = \int_K^{\infty} x\,f_X(x)\,dx. \tag{11}
$$

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

Start from $(6)$ and split the payoff on the event $\{S_T>K\}$:

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

**Reading the two terms.** $\Phi(d_2)=\mathbb{Q}(S_T>K)$ is the risk-neutral probability of exercise, so the second term is a cash-or-nothing binary: $K$ zero-coupon bonds that pay if and only if the call finishes in the money. The first term is a share-or-nothing binary. $\Phi(d_1)$ is the same exercise probability after the mean shift $m\mapsto m+s^2$ that $(14)$ performed — equivalently, as Route II will show, the exercise probability when the unit of account is the stock itself.

![Two evaluations of the same bell curve](/blog/assets/2024/bsm/phi-anatomy.png)

For the ATM numbers above, $d_1$ and $d_2$ sit $\sigma\sqrt{\tau}=0.20$ apart. That gap is the Itô correction, visible on the page.

**Put-call parity.** A European call minus a European put with the same strike and expiry is a forward, and a forward on a non-dividend stock is worth $S_t - K e^{-r\tau}$:

$$
C - P = S_t - K e^{-r\tau}.
$$

This is an accounting identity, not a pricing model. Substitute $(1)$:

$$
P = K e^{-r\tau}\,\Phi(-d_2) - S_t\,\Phi(-d_1).
$$

For the ATM numbers, $P\approx 5.57$. The call is worth more than the put because the forward is in the money once $r>0$.

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

| Numeraire | Measure | Martingale | $\mathbb{Q}^{\,\cdot}(S_T>K)$ | Role in $(1)$ |
|---|---|---|---|---|
| bond $B_t=e^{rt}$ | $\mathbb{Q}$ | $S_t/B_t$ | $\Phi(d_2)$ | multiplies the cash $Ke^{-r\tau}$ |
| stock $S_t$ | $\mathbb{Q}^{S}$ | $B_t/S_t$ | $\Phi(d_1)$ | multiplies the share $S_t$ |

---

# The PDE, briefly
{: #the-pde-briefly}

Black and Scholes did not start from $(6)$. They started from a portfolio $\Pi=-V+\Delta S$. Itô-expand $dV$, choose $\Delta=V_S$ so the $dW$ terms cancel (**delta-hedging**), and require the now-riskless $\Pi$ to earn $r$, or else there is an arbitrage against the money-market account. The result is the Black–Scholes PDE

$$
V_t + rS V_S + \tfrac12\sigma^2 S^2 V_{SS} - rV = 0, \tag{17}
$$

with $V(S,T)=(S-K)^+$. The drift $\mu$ cancelled with the $dW$ terms. The coefficient $V_{SS}$ is the gamma; $\tfrac12\sigma^2 S^2 V_{SS}$ is Itô's correction, now sitting in a PDE.

Feynman–Kac is the dictionary between $(17)$ and $(6)$: a parabolic PDE with drift coefficient $rS$ and discount $r$ is solved by $e^{-r\tau}\mathbb{E}^{\mathbb{Q}}[h(S_T)\mid S_t]$ along the diffusion $(5)$. The hedging argument produces the PDE; Feynman–Kac translates it into the integral Route I already evaluated.

A further change of variables — $x=\ln(S/K)$, time-to-go rescaled by $\sigma^2/2$, an exponential prefactor to absorb discounting — turns $(17)$ into the heat equation $W_{\tilde\tau}=W_{xx}$. The fundamental solution is a Gaussian, and the antiderivative of a Gaussian is $\Phi$. The algebra is written out in Rouah §7 of the [hosted note](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf). The Gaussian in $(1)$ is both the transition density of geometric Brownian motion and the heat kernel: the same assumption, two costumes.

---

# Limitations
{: #limitations}

**Dividends.** A continuous yield $q$ changes the risk-neutral drift of $S$ from $r$ to $r-q$. The same Route I, with $m=\ln S_t+(r-q-\sigma^2/2)\tau$, produces Merton's formula

$$
C = S_t e^{-q\tau}\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2),
$$

$r$ replaced by $r-q$ inside $d_1$ and $d_2$ as well. Index options live here ($q$ is the basket yield), FX options live here ($q$ is the foreign rate), and futures options live here ($q=r$: Black 1976).

**The smile.** After 1987 the market stopped believing in a single $\sigma$. Implied volatility against strike is a smile, or in equities a smirk. Traders still quote in Black–Scholes implied vol. They do not believe the lognormal assumption that produced it.

**Jumps, stochastic vol, Americans.** Merton added Poisson jumps. Heston let $\sigma_t$ diffuse. Dupire showed that a surface of implied vols is equivalent to a local-vol diffusion that refits every vanilla. None of these has a two-$\Phi$ formula of the same shape. The American put is an optimal-stopping problem; a binomial tree is the honest computation.

What has been proved is a theorem about a complete market driven by one Wiener process: the unique no-arbitrage price of $(S_T-K)^+$ is $(1)$. Using that theorem as a price, as a quoting convention, or as the first term of a perturbation is a separate decision.

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
