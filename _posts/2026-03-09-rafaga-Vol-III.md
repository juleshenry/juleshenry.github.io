---
layout: post
title: "Back-of-the-Envelope: Mean-Reverting VIX, Vol. III: Jumps, Vol-of-Vol and the Fourier Trick"
date: 2026-03-09 12:02:00
mathjax: true
categories: wealth
---

*Mean-Reverting VIX:* [Vol. I](/blog/2026/03/09/rafaga) · [Vol. II](/blog/2026/03/09/rafaga-Vol-II) · **Vol. III** · [Vol. IV](/blog/2026/03/09/rafaga-Vol-IV) · [Vol. V](/blog/2026/03/09/rafaga-Vol-V) · [Vol. VI](/blog/2026/03/09/rafaga-Vol-VI)

{% include vix-kit.html %}

*Two ways to give the VIX a fat right tail -- jumps and random vol-of-vol -- and the one piece of Fourier analysis that prices both. Then a correction: what actually went wrong when this project was in Python.*

[Vol. II](/blog/2026/03/09/rafaga-Vol-II) ended with a wall: VIX implied volatility nearly triples between the money and a strike of 50, and a log-normal model can only draw a flat line. We need $\ln\text{VIX}_T$ to have a heavier right tail than a Gaussian. Bao's thesis offers two mechanisms and a combination of both. We build the two that matter.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#jumps">jumps</a></li>
  <li><a href="#characteristic-functions">characteristic functions</a></li>
  <li><a href="#the-jump-term">deriving the jump term</a></li>
  <li><a href="#vol-of-vol">random vol-of-vol</a></li>
  <li><a href="#gil-pelaez">from characteristic function to option price</a></li>
  <li><a href="#numerics">the numerics, and a correction</a></li>
</ol>
</div>

---

# jumps
{: #jumps}

<div class="ev-def"><strong>Definition (Poisson process).</strong> A counting process $N_t$ with $N_0 = 0$ and independent increments, where the number of events in an interval of length $\Delta t$ is Poisson: $P(k \text{ events}) = \frac{(\lambda\Delta t)^k}{k!}e^{-\lambda\Delta t}$. The rate $\lambda$ is the expected number of events per year.</div>

Over a short interval there is either no event (probability $\approx 1-\lambda\Delta t$) or one (probability $\approx\lambda\Delta t$). Attach a random size $J$ to each event, drawn independently from an exponential distribution,

$$J\sim\text{Exp}(\eta), \qquad f_J(j) = \eta e^{-\eta j},\ j\ge0, \qquad \mathbb E[J] = 1/\eta,$$

and add the jumps to the rubber band of [Vol. I](/blog/2026/03/09/rafaga):

<div class="ev-def"><strong>Definition (MRLRJ).</strong> $d\ln\text{VIX}_t = \kappa(\theta-\ln\text{VIX}_t)\,dt + \sigma\,dW_t + J\,dN_t.$ Five parameters: $\kappa,\theta,\sigma$ as before, jump rate $\lambda$ and inverse mean log-jump $\eta$.</div>

Jumps are upward only. That is the physics of fear: the VIX spikes up and decays down, and the decay is already handled by mean reversion. A mean log-jump of $1/\eta = 0.3$ means the typical jump multiplies the VIX by $e^{0.3}\approx1.35$. Because a jump is a shock to $\ln\text{VIX}$, mean reversion then pulls it back at the same speed as any other shock.

This model is due to Psychoyios, Dotsis and Markellos (2010); the thesis develops its futures, options, hedging and convexity formulas. What it costs us is the Gaussian. $\ln\text{VIX}_T$ is now a Gaussian plus a random sum of decayed exponentials, and there is no closed-form density, so no $\Phi(d_1)$.

---

# characteristic functions
{: #characteristic-functions}

<div class="ev-def"><strong>Definition (characteristic function).</strong> For a random variable $X$, $\psi_X(s) = \mathbb E[e^{isX}] = \int e^{isx} f_X(x)\,dx$, the Fourier transform of its density.</div>

Three facts make this the right tool.

1. **It determines the distribution.** Knowing $\psi_X$ is the same as knowing $f_X$; Fourier inversion goes back.
2. **Independent pieces multiply.** If $X = A + B$ with $A, B$ independent, $\psi_X = \psi_A\psi_B$. Our $\ln\text{VIX}_T$ is exactly such a sum: a Gaussian part plus an independent jump part.
3. **It is often closed-form when the density is not.** That is the case here.

For a Gaussian $\mathcal N(\mu,v)$, $\psi(s) = e^{is\mu - s^2v/2}$. So under MRLR, with $\mu$, $v$ and $\phi = e^{-\kappa\tau}$ as in [Vol. II](/blog/2026/03/09/rafaga-Vol-II#vix-futures),

$$\psi_{\text{MRLR}}(s) = \exp\!\Big(is\mu - \tfrac12 s^2 v\Big).$$

Also note what $\psi$ at an imaginary argument gives: $\psi(-i) = \mathbb E[e^{X}] = \mathbb E[\text{VIX}_T] = F$. **The VIX future is the characteristic function evaluated at $s=-i$.** That will be used constantly.

---

# deriving the jump term
{: #the-jump-term}

The March post said the jump term comes "after considerable algebra". It is one substitution. Solve the MRLRJ equation with the integrating factor, as in Vol. I, and a jump of size $J_k$ at time $t_k$ contributes $e^{-\kappa(T-t_k)}J_k$ to $\ln\text{VIX}_T$: it decays like any other shock. So the jump part is $\sum_k e^{-\kappa(T - t_k)}J_k$, a compound Poisson sum with time-dependent weights. For such a sum over $[t, T]$,

$$\mathbb E\Big[\exp\Big(is\sum_k e^{-\kappa(T-t_k)}J_k\Big)\Big] = \exp\Big(\lambda\int_0^{\tau}\big(\mathbb E\big[e^{is e^{-\kappa h}J}\big]-1\big)\,dh\Big),$$

(split $[t, T]$ into small intervals, each with probability $\lambda\,dh$ of one jump, and multiply). The exponential distribution has $\mathbb E[e^{iuJ}] = \frac{\eta}{\eta - iu}$, so the integrand is

$$\frac{\eta}{\eta - is e^{-\kappa h}} - 1 = \frac{is\,e^{-\kappa h}}{\eta - is\,e^{-\kappa h}}.$$

Substitute $x = e^{-\kappa h}$, $dh = -\frac{dx}{\kappa x}$, running from $x=1$ to $x=\phi$:

$$\lambda\int_\phi^1 \frac{is}{\kappa(\eta - isx)}\,dx = \frac{\lambda}{\kappa}\Big[-\ln(\eta - isx)\Big]_\phi^1 = \frac{\lambda}{\kappa}\ln\frac{\eta - is\phi}{\eta - is}.$$

Multiply by the Gaussian part:

$$\boxed{\ \psi_{\text{MRLRJ}}(s) = \exp\!\Big(is\mu - \tfrac12 s^2 v + \frac{\lambda}{\kappa}\ln\frac{\eta - is\phi}{\eta - is}\Big)\ }$$

Three checks. At $\lambda = 0$ it is MRLR. The factor $\lambda/\kappa$ says fast mean reversion shrinks the cumulative effect of jumps, because each one is forgotten sooner. And at $s = -i$,

$$F = \psi(-i) = e^{\mu + v/2}\Big(\frac{\eta - \phi}{\eta - 1}\Big)^{\lambda/\kappa},$$

which is finite only if $\eta>1$. Exponential jumps in $\ln\text{VIX}$ are Pareto jumps in the VIX, with tail index $\eta$; at $\eta\le1$ the jumps have infinite mean and so does the VIX. Any calibration has to respect $\eta > 1$, and the thesis never says so.

---

# random vol-of-vol
{: #vol-of-vol}

Jumps are one way to fatten the tail. The other is to notice that the vol-of-vol $\sigma$ itself is not constant: when the VIX rises, it rises more violently. Replace $\sigma$ by a random variance with its own rubber band, the square-root process of Heston (1993):

<div class="ev-def"><strong>Definition (MRLRSV).</strong>
$$d\ln\text{VIX}_t = \kappa(\theta - \ln\text{VIX}_t)\,dt + \sqrt{V_t}\,dW_t,\qquad dV_t = \kappa_v(\theta_v - V_t)\,dt + \sigma_v\sqrt{V_t}\,dZ_t,$$
with $d\langle W, Z\rangle_t = \rho\,dt$. Seven parameters: $\kappa,\theta$; the variance's speed $\kappa_v$, level $\theta_v$, own volatility $\sigma_v$, starting value $V_0$; and the correlation $\rho$.</div>

With $\rho > 0$, a VIX rally raises the vol-of-vol, which makes further rallies larger. That fattens the right tail as jumps do, but it has to build up, so it acts more at long maturities than short ones. Jumps are instantaneous and act most at short maturities.

The model is **affine**: its drift and variance are linear in the state $(X, V)$ with $X = \ln\text{VIX}$. For such models the characteristic function has exponential-affine form. Guess

$$\psi = \exp\big(a(\tau) + b(\tau)\,V_t + c(\tau)\,X_t\big),$$

require that $\psi$ be a martingale in $t$ (it is a conditional expectation of a fixed payoff), and match the coefficients of $X$, $V$ and 1. The $X$-coefficient decays like any shock, $c = is\,e^{-\kappa\tau}$. With $u(h) = is\,e^{-\kappa h}$, the $V$-coefficient solves a **Riccati equation** and $a$ is its integral:

$$b' = \tfrac12 u^2 + \rho\sigma_v\,u\,b + \tfrac12\sigma_v^2 b^2 - \kappa_v b,\quad b(0) = 0; \qquad a = is\,\theta(1-\phi) + \kappa_v\theta_v\int_0^\tau b\,dh.$$

In Heston's stock model the coefficients are constant and the Riccati equation has an elementary solution. Here $u(h)$ decays with $h$, and the solution needs Kummer confluent hypergeometric functions. The thesis tried them, found them unstable and slow, and recommends Runge–Kutta instead. So do we: classic fourth-order RK4, one integration per value of $s$.

**Why not both?** MRLRSVJ puts jumps and random vol-of-vol together. In the thesis it fits no better than MRLRSV (percentage errors within 0.01 points of each other) at the price of two more parameters. We leave it out.

---

# from characteristic function to option price
{: #gil-pelaez}

We have $\psi$; we want $C = D\,\mathbb E^{\mathbb Q}[(\text{VIX}_T - K)^+]$. Split the payoff at $\text{VIX}_T = K$:

$$C = D\Big(\mathbb E\big[\text{VIX}_T\,\mathbf 1\{\text{VIX}_T > K\}\big] - K\,\mathbb Q(\text{VIX}_T > K)\Big) = D\big(F\,\Pi_1 - K\,\Pi_2\big).$$

$\Pi_2 = \mathbb Q(\ln\text{VIX}_T > \ln K)$ is a probability, and the **Gil-Pelaez** theorem (1951) recovers tail probabilities straight from the characteristic function:

$$\Pi_2 = \frac12 + \frac1\pi\int_0^\infty \frac{\operatorname{Im}\big(e^{-iuk}\psi(u)\big)}{u}\,du, \qquad k = \ln K.$$

(Where does it come from? $\mathbf 1\{X>k\} = \tfrac12 + \tfrac12\operatorname{sign}(X-k)$, and the sign function has the Fourier representation $\operatorname{sign}(y) = \frac2\pi\int_0^\infty \frac{\sin(uy)}{u}du$. Take expectations and swap the integrals.)

$\Pi_1 = \mathbb E[\text{VIX}_T\mathbf 1\{\cdot\}]/F$ is the same kind of probability, under a measure that weights each outcome by $\text{VIX}_T/F$. Its characteristic function is $\psi(u - i)/\psi(-i)$, so the same formula applies with that in place of $\psi(u)$. Under MRLR the two collapse to $\Phi(d_1)$ and $\Phi(d_2)$ and we are back to Black; with jumps or random vol-of-vol they are two integrals, and the price is **one pair of integrals per strike**. No Monte Carlo, no PDE grid.

---

# the numerics, and a correction
{: #numerics}

In practice the integral is truncated at a point $U$ where $\lvert\psi(U)\rvert < 10^{-12}$, and evaluated by composite 16-point Gauss–Legendre quadrature on $[0, U]$. Every strike of one expiry shares the same nodes, so $\psi$ is computed once per maturity and reused. For MRLRSV that matters: each node is an RK4 solve. The Riccati equation is **stiff** for large $\lvert s\rvert$ (its Jacobian grows like $\sigma_v\lvert s\rvert$), so the step size must shrink as $s$ grows, and the code chooses it per node.

Two failure modes turned up only when calibration started throwing wild parameters at the pricer. As $\sigma\to0$ in MRLRJ, the characteristic function stops decaying -- the jump term alone has modulus bounded away from zero -- and an adaptive cutoff grows without limit. One calibration run spent 321 seconds on one maturity before the cutoff was capped at $U = 400$, a point beyond which $\ln\text{VIX}_T$ would have a standard deviation under 2%, far from any real VIX market. And huge $\sigma_v$ made RK4 need thousands of steps per node. Both are now bounded, and both bounds are documented in the paper.

The code is checked by 34 assertions ([tests](https://github.com/juleshenry/rafaga/blob/main/julia_impl/test/runtests.jl)): the Fourier pricer reproduces the MRLR closed form to $10^{-8}$; MRLRJ with $\lambda\to0$ and MRLRSV with $\sigma_v\to0$ reduce to MRLR; $F = \psi(-i)$ matches the closed-form futures; prices fall and are convex in $K$ and respect arbitrage bounds; Euler Monte Carlo with 200,000 paths agrees within four standard errors; and a ten-times-smaller RK4 step moves no price by more than $10^{-4}$.

Now the correction. The first version of this project was Python, in files named, with escalating confidence, `cool.py`, `cooler.py` and `coolest.py`. It returned probabilities greater than one. I suppressed the warnings -- I wrote `warnings.simplefilter(action='ignore', category=integrate.IntegrationWarning)` in a project whose entire purpose was integration -- and eventually rewrote it in Julia.

<div class="cs-q"><strong>March 2026 said:</strong> "Python's <code>float64</code> maps this to exactly zero -- underflow -- and the integrand becomes discontinuous... Julia has <code>BigFloat</code> as a first-class citizen... No underflow. No overflow. No lies."</div>
<div class="cs-a"><strong>The data says:</strong> Double precision was never the problem. The Julia code evaluated the characteristic function in <code>BigFloat</code> and then <em>converted it back to</em> <code>ComplexF64</code> before integrating, and ran the normal CDF in <code>Float64</code>; every price it produced was a double-precision computation. The rebuilt pricer is plain <code>Float64</code>, and it agrees with a 25-digit <code>BigFloat</code> quadrature to $10^{-9}$ on the thesis' most extreme jump parameters ($\lambda = 169$ jumps a year). An integrand that underflows to zero where it is $e^{-200}$ is correct, not broken. The logarithm's branch cut is not a hazard either: for real $u$ both $\eta - iu\phi$ and $\eta - iu$ have positive real part, so their ratio never crosses the negative real axis.</div>

The Python files are gone, so I cannot say exactly what broke. A probability above one from a Gil-Pelaez integral is the classic symptom of the *integration* going wrong -- truncating before $\psi$ has decayed, or an adaptive routine giving up on an oscillating integrand -- and that is what the suppressed `IntegrationWarning` was trying to say. The lesson I drew in March, that the right tool beat the popular one, was the wrong lesson. The right one: *when your numbers are impossible, read the warning before you change the language*.

---

# where this goes
{: #where-this-goes}

We can now price VIX futures and options under three models, fast and accurately. What we cannot yet do is choose their parameters. The thesis did that for one day in 2011, and published the answers without the method. [Vol. IV](/blog/2026/03/09/rafaga-Vol-IV) reconstructs the method, tests the answers, and finds that several of the parameters are not really there.

---

**Next:** [Vol. IV: Calibration, and What the Thesis Didn't Say](/blog/2026/03/09/rafaga-Vol-IV)

*Mean-Reverting VIX:* [Vol. I](/blog/2026/03/09/rafaga) · [Vol. II](/blog/2026/03/09/rafaga-Vol-II) · **Vol. III** · [Vol. IV](/blog/2026/03/09/rafaga-Vol-IV) · [Vol. V](/blog/2026/03/09/rafaga-Vol-V) · [Vol. VI](/blog/2026/03/09/rafaga-Vol-VI)
