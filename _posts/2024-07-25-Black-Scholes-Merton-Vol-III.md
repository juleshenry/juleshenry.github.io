---
layout: post
title: "Back-of-the-Envelope: Black-Scholes-Merton, Vol. III: Nuance, and Other Approaches"
date: 2024-07-24 12:02:00
categories: wealth
mathjax: true
---

*Black-Scholes-Merton:* [Vol. I](/blog/2024/07/24/Black-Scholes-Merton) · [Vol. II](/blog/2024/07/24/Black-Scholes-Merton-Vol-II) · **Vol. III**

*The same formula, reached twice more — once as heat, once as a change of units — and then the assumptions, each pulled on until the formula bends or breaks.*

[Vol. II](/blog/2024/07/24/Black-Scholes-Merton-Vol-II) derived

$$
C \;=\; S_t\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2), \qquad d_{1,2} \;=\; \frac{\ln(S_t/K)+\bigl(r\pm\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}, \tag{1}
$$

by integrating the payoff against a lognormal whose drift is $r$. The rain check — $S=K=100$, $\tau=1$, $r=5\%$, $\sigma=20\%$ — costs $10.45$. This volume reaches $(1)$ by two other roads, then revisits the assumptions of [Vol. I](/blog/2024/07/24/Black-Scholes-Merton#3-the-bsm-assumptions).

- [The heat equation](#1-the-heat-equation)
- [Change of numeraire](#2-change-of-numeraire)
- [The assumptions, revisited](#3-the-assumptions-revisited)
- [What was proved](#what-was-proved)
- [References](#references)

---

# 1. The heat equation
{: #1-the-heat-equation}

Vol. II never wrote a differential equation for the option price. Black and Scholes did; it was their route. It needs Itô's lemma, Vol. II's $(3)$: for $dX=a\,dt+b\,dW$,

$$
df(t,X_t) \;=\; \Bigl(f_t + a f_x + \tfrac12 b^2 f_{xx}\Bigr)dt + b f_x\,dW_t. \tag{3}
$$

## The hedge

Let $V(S,t)$ be the option's price, and hold the portfolio $\Pi=-V+\Delta S$: short one option, long $\Delta$ shares. Expand $dV$ with $(3)$, using $dS=\mu S\,dt+\sigma S\,dW$:

$$
d\Pi \;=\; -\Bigl(V_t+\mu S V_S+\tfrac12\sigma^2S^2V_{SS}\Bigr)dt - \sigma S V_S\,dW + \Delta\bigl(\mu S\,dt+\sigma S\,dW\bigr).
$$

Choose $\Delta=V_S$. The $dW$ terms cancel — this is **delta-hedging** — and so do the $\mu$ terms. What is left has no randomness:

$$
d\Pi \;=\; -\Bigl(V_t+\tfrac12\sigma^2S^2V_{SS}\Bigr)dt.
$$

A riskless portfolio must earn the riskless rate, $d\Pi=r\Pi\,dt$, or there is a free lunch. Setting the two equal gives the Black–Scholes **PDE**:

$$
V_t + rS V_S + \tfrac12\sigma^2 S^2 V_{SS} - rV \;=\; 0, \tag{17}
$$

with $V(S,T)=(S-K)^+$. The $dW$ cancellation eats $\mu$, just as $\Delta=2/3$ did on the two-leaf tree. For the rain-check numbers, $\Delta=V_S=\Phi(d_1)\approx 0.637$.

## Heat in disguise

This is a linear parabolic PDE. You have seen one: the heat equation $u_t=u_{xx}$, which says a rod's temperature at a point rises when the point is colder than the average of its neighbours. Let $\tau=T-t$, $x=\ln(S/K)$, $V(S,t)=U(x,\tau)$. Then $V_t=-U_\tau$, $V_S=U_x/S$, and $S^2 V_{SS}=U_{xx}-U_x$. Substitute:

$$
U_\tau \;=\; \tfrac12\sigma^2 U_{xx} + \bigl(r-\tfrac12\sigma^2\bigr)U_x - r U.
$$

Rescale $\tilde\tau=\sigma^2\tau/2$, set $k=2r/\sigma^2$, and kill lower-order terms with $U=e^{\alpha x+\beta\tilde\tau}W$, $\alpha=(1-k)/2$, $\beta=\alpha^2+(k-1)\alpha-k$. Then

$$
W_{\tilde\tau} \;=\; W_{xx},
$$

the heat equation, with initial temperature profile $W(x,0)=e^{-\alpha x}(Ke^{x}-K)^+$. (Rain-check numbers: $k=2.5$, $\alpha=-3/4$, $\beta=-49/16$.) Time runs backwards from expiry: the kink in the payoff at $x=0$ is a hot spot on the rod, and time to expiry lets it diffuse.

The solution is the initial profile smeared by the heat kernel,

$$
W(x,\tilde\tau) \;=\; \int_{-\infty}^{\infty} G(x-y,\tilde\tau)\,W(y,0)\,dy, \qquad G(x,\tilde\tau)=\frac{1}{\sqrt{4\pi\tilde\tau}}\exp\Bigl(-\frac{x^2}{4\tilde\tau}\Bigr).
$$

$G$ is the density of $\mathcal{N}(0,2\tilde\tau)$, and $2\tilde\tau=\sigma^2\tau=\mathrm{Var}(\ln S_T)$ under $\mathbb{Q}$. The heat kernel *is* the lognormal of Vol. II, written in log-coordinates, and the integral above is Vol. II's integral $(15)$ with the substitutions undone. Evaluating it is the same completing-the-square, and returns $(1)$. **Feynman–Kac**, in this instance, is that sentence: the solution of the PDE is an expectation against the process.

What this road buys you is *numerics*. When the payoff or the boundary makes the integral intractable — an American put, a barrier — the PDE is still a PDE, and finite differences on a grid solve it.

---

# 2. Change of numeraire
{: #2-change-of-numeraire}

The two $\Phi$'s in $(1)$ are both probabilities that the call finishes in the money, $\{S_T>K\}$. Yet $\Phi(d_1)\approx 0.637$ and $\Phi(d_2)\approx 0.560$. Same event, two probabilities. The explanation is that they are measured in different units of account. To say that precisely we first need the tool Vol. II asserted: changing probabilities without changing the spread.

The calculation below follows Fabrice Douglas Rouah, *Four Derivations of the Black-Scholes Formula*. The original host is gone. A copy is [here](/blog/assets/2024/bsm/Black-Scholes-Formula-Rouah.pdf); the [Wayback capture of 19 July 2024](https://web.archive.org/web/20240719130017/https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf) is the provenance.

## Girsanov, from two Gaussians

On the tree, the likelihood ratio on one step is $p^*/p$ on up and $(1-p^*)/(1-p)$ on down. Then $\mathbb{E}^*[X]=\mathbb{E}[X\,\xi]$. Over $n$ steps, $\xi$ is the product of those ratios. That product *is* Girsanov, before the limit.

**One Gaussian.** Under $\mathbb{P}$, $W_t\sim\mathcal{N}(0,t)$. We want $\mathbb{Q}$ under which $W_t\sim\mathcal{N}(-\theta t,\,t)$, so that $W_t+\theta t$ is standard Wiener. Divide the two densities:

$$
\xi_t
\;=\;
\frac{\exp\bigl(-(w+\theta t)^2/2t\bigr)}{\exp\bigl(-w^2/2t\bigr)}\Bigg|_{w=W_t}
\;=\;
\exp\bigl(-\theta W_t - \tfrac12\theta^2 t\bigr).
$$

For any test function, $\mathbb{E}^{\mathbb{Q}}[f(W_t)]=\mathbb{E}^{\mathbb{P}}[f(W_t)\,\xi_t]$. Only the center moved; the variance $t$ did not. Independent increments multiply the same ratio across steps. That is **Girsanov's theorem**, from the Gaussian pdf — motivated here, not proved for general processes.

**Which $\theta$.** Rewrite the stock $dS=\mu S\,dt+\sigma S\,dW$ as

$$
dS \;=\; r S\,dt + \sigma S\Bigl(dW + \frac{\mu-r}{\sigma}\,dt\Bigr).
$$

The process in parentheses is Wiener plus a constant drift $\theta=(\mu-r)/\sigma$, the **market price of risk**: excess return per unit of volatility. Girsanov with that $\theta$ makes $W^{\mathbb{Q}}_t=W_t+\theta t$ a Wiener process under $\mathbb{Q}$, and

$$
dS_t \;=\; r S_t\,dt + \sigma S_t\,dW_t^{\mathbb{Q}}. \tag{5}
$$

This is what Vol. II assumed by analogy with the tree: $\mu$ becomes $r$, $\sigma$ stays. Under $\mathbb{Q}$,

$$
S_T \;=\; S_t\exp\Bigl(\bigl(r-\tfrac12\sigma^2\bigr)\tau + \sigma\sqrt{\tau}\,Z\Bigr), \qquad Z\sim\mathcal{N}(0,1). \tag{7}
$$

## Two numeraires

A **numeraire** is the unit you quote prices in. Dollars: the money-market account $B_t=e^{rt}$. Shares: the stock $S_t$. For each choice there is a measure that makes every asset, *divided by that numeraire*, a martingale. $\mathbb{Q}$ is the one for dollars-in-the-bank: $S_t/B_t$ is a fair game.

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

Vol. II split the call into a **cash-or-nothing** (receive $K$ if $S_T>K$) and an **asset-or-nothing** (receive the share if $S_T>K$). Under $\mathbb{Q}$ the cash-or-nothing is worth $Ke^{-r\tau}\,\mathbb{Q}(S_T>K)=Ke^{-r\tau}\Phi(d_2)$. The asset-or-nothing pays in *shares*, so price it in shares.

The density ratio that changes $\mathbb{Q}$ into $\mathbb{Q}^{S}$ is the terminal value of the new numeraire relative to the old, rebased to $1$ today:

$$
\frac{d\mathbb{Q}^{S}}{d\mathbb{Q}}
\;=\;
\frac{S_T/S_t}{B_T/B_t}
\;=\;
\frac{S_T}{S_t e^{r\tau}}.
$$

Under $\mathbb{Q}$, from $(7)$,

$$
\frac{S_T}{S_t e^{r\tau}}
\;=\;
\exp\bigl(-\tfrac12\sigma^2\tau + \sigma\sqrt{\tau}\,Z\bigr).
$$

That is the Girsanov density $\xi=\exp(-\theta W-\tfrac12\theta^2 t)$ from above, with $\theta=-\sigma$ and $W_{\tau}=\sqrt{\tau}\,Z$. The tilt *adds* $\sigma\sqrt{\tau}$ to $Z$. The event $\{S_T>K\}$ is $\{Z>-d_2\}$ under $\mathbb{Q}$; after the tilt it is $\{Z+\sigma\sqrt{\tau}>-d_2\}=\{Z>-d_1\}$, so

$$
\mathbb{Q}^{S}(S_T>K) \;=\; \Phi(d_1).
$$

The asset-or-nothing is therefore $S_t\,\Phi(d_1)$: today's share, times the exercise probability *in share units*. The cash-or-nothing is $Ke^{-r\tau}\,\Phi(d_2)$: discounted strike, times the exercise probability *in dollar units*. That is $(1)$, with both $\Phi$'s now ordinary probabilities, each belonging to the numeraire that multiplies it. No integral was completed; the square was completed once, inside Girsanov.

Why is the share-measure probability higher? Under $\mathbb{Q}^S$, outcomes are weighted by how many dollars the share is worth in them. The in-the-money outcomes are exactly the ones where the share is worth a lot, so they get more weight. $\Phi(d_1)-\Phi(d_2)$ is that reweighting.

The same trick is the workhorse whenever $r$ is not constant: price a payoff in units of a zero-coupon bond maturing at $T$, and the discount factor comes out of the expectation even when rates are random. That is the **$T$-forward measure**, and §3 uses it.

---

# 3. The assumptions, revisited
{: #3-the-assumptions-revisited}

Vol. I listed the assumptions before they were used. Now we know exactly where each was spent, so we can pull on each one and watch. The two-$\Phi$ shape is not a law of nature. It is a receipt for a short list of hypotheses. Perturb one and the formula either *morphs* (same skeleton, different inputs or an extra factor) or *breaks* (the completing-the-square step no longer lands on $\Phi$).

## The risk-free rate

Where it was spent: $r$ appears twice. It discounts, $e^{-r\tau}$; and it is the drift of the stock under $\mathbb{Q}$.

**Known, but not constant.** If $r(t)$ is a deterministic function of time, replace $r\tau$ everywhere by $\int_t^T r(u)\,du$. The formula survives intact; in practice you read that integral off today's yield curve, as the yield on a zero-coupon bond maturing at $T$.

**Random.** If $r_t$ is itself random and correlated with $S$, then $\mathbb{E}^{\mathbb{Q}}\bigl[e^{-\int r}(S_T-K)^+\bigr]$ no longer splits: the discount factor does not come out in front. The fix is §2's: use the $T$-maturity bond $P(t,T)$ as the numeraire. Under that measure the forward $F=S_t/P(t,T)$ is a martingale, and if $F$ is lognormal with total variance $v^2$, the call is

$$
C \;=\; P(t,T)\bigl[F\,\Phi(d_1) - K\,\Phi(d_2)\bigr], \qquad d_{1,2}=\frac{\ln(F/K)\pm\tfrac12 v^2}{v}.
$$

Two $\Phi$'s again, but $v^2$ now includes the bond's volatility and its correlation with the stock. For short-dated equity options this is a rounding error. For long-dated ones, or options on bonds, it is the whole story.

**Borrowing is not lending.** The hedge in §1 borrows to buy shares. If you borrow at $r_b$ and lend at $r_\ell<r_b$, a call-buyer's replication and a call-writer's replication cost different amounts, and no-arbitrage pins the price only to an interval, not a point. Black–Scholes is the midpoint of a band whose width is the spread.

**Negative, or near zero.** The lognormal needs a positive underlying. When the underlying is itself a rate, and rates can go through zero — euro rates after 2014 — the log in $d_{1,2}$ is undefined. Go back to an additive Gaussian, $S_T=S+\sigma\sqrt{\tau}\,Z$ (Bachelier, 1900), and the same integral gives a single $\Phi$ of $(S-K)/(\sigma\sqrt{\tau})$ plus a density term, with no logarithms. The log in $d_{1,2}$ is not decoration. It is the Jacobian of Vol. II §2, still visible in the answer.

## Dividends

Where it was spent: under $\mathbb{Q}$ the stock's drift had to be $r$, otherwise you could pocket the excess over the bond by holding it. And in Vol. I, Merton's no-early-exercise argument for calls.

If the stock pays a continuous **yield** $q$ — a cash stream $qS\,dt$ while you hold it — the capital-gain drift under $\mathbb{Q}$ must be $r-q$. Total return, gain plus yield, equals $r$. Any more is a free lunch.

The prepaid forward is then $S_t e^{-q\tau}$ instead of $S_t$. Vol. II's integral still closes. The share piece picks up $e^{-q\tau}$, and $r$ is replaced by $r-q$ inside $d_1$ and $d_2$:

$$
C \;=\; S_t e^{-q\tau}\,\Phi(d_1) - K e^{-r\tau}\,\Phi(d_2), \qquad d_{1,2} \;=\; \frac{\ln(S_t/K)+\bigl(r-q\pm\tfrac12\sigma^2\bigr)\tau}{\sigma\sqrt{\tau}}.
$$

Give the rain-check stock a $2\%$ yield. Then $d_1=0.25$, $d_2=0.05$, and $C\approx 9.23$, cheaper than $10.45$: the stock itself now pays you, so the call is less of a reason to hold.

The same skeleton prices three cousins, once you name what $q$ is.

- A call on an **index**. The stocks in the basket pay dividends, so the index has a yield $q$.
- A call on a **foreign currency** (Garman–Kohlhagen). Holding euros earns the euro interest rate $r_f$; that rate is $q$.
- A call on a **futures** (Black 1976). You put up no cash to hold the futures, so you save the financing $r$. That saving is a yield $q=r$, and the formula collapses to $e^{-r\tau}\bigl[F\Phi(d_1)-K\Phi(d_2)\bigr]$ — the bond-numeraire formula above, with a constant rate.

A **discrete cash** dividend of size $D$ just before $T$ is a different animal: $S_T$ is then a lognormal minus $D$, which is not lognormal, and $(1)$ as written does not apply. The common patch is to subtract the present value of $D$ from $S_t$ and apply $(1)$ to what is left. And a discrete dividend revives early exercise for American calls: just before the stock goes ex-dividend, the call-holder may do better to exercise and collect $D$ than to watch the share price drop by $D$.

## The smile

Where it was spent: one $\sigma$, constant, for every strike and every path. That is what made $\ln S_T$ a single Gaussian.

**Implied volatility** is the one input you cannot read off a screen, so the market reads it backwards. Given a quoted price, $\sigma_{\mathrm{imp}}$ is the number you feed into $(1)$ to recover that quote. Our formula at $20\%$ says $10.45$; if the market shows $12$, implied vol is some number above $20\%$. Traders quote "vol $22$" rather than a dollar price, because that number compares across strikes and tenors.

If the model were right, $\sigma_{\mathrm{imp}}$ would be the same for every strike. It is not. Before October 1987, equity implied vols were roughly flat. After the crash, out-of-the-money puts — insurance against another one — traded at prices no single $\sigma$ could fit. Plot $\sigma_{\mathrm{imp}}$ against strike and you get a U in currencies (a **smile**) and a downward slope in equities (a **smirk**: crash insurance is dear). Traders using $(1)$ this way are using it as a language. They do not believe $\ln S_T$ is Gaussian.

The smile is the market telling you which assumption to drop. Each fix corresponds to a line of Vol. II's derivation.

- **Fat tails.** If $\ln S_T$ is Student-$t$ rather than Gaussian, completing the square fails: that move is a property of $\exp(-\tfrac12 z^2)$, not of densities in general. No closed form; integrate numerically. Fatter tails than the lognormal make far-out-of-the-money options dearer, which is a smile.
- **Wandering volatility.** If $\sigma_t$ is itself random (Heston), then $s$ is random, and conditional on $s$ the stock is lognormal. The call is an *average* of Black–Scholes prices, one per realised $s$:
  $$
  \mathbb{E}[(S_T-K)^+] \;=\; \mathbb{E}\bigl[e^{m+s^2/2}\Phi(d_{+}(s)) - K\Phi(d_{-}(s))\bigr].
  $$
  Averaging over $s$ fattens both tails. Correlate $\sigma$ with $S$ negatively — vol rises when the market falls — and the left tail fattens more: a smirk.
- **Jumps.** Wiener paths are continuous; a crash is a gap. Merton added Poisson jumps on top of the Wiener process. Conditional on the number of jumps, $\ln S_T$ is Gaussian, so the price is a Poisson-weighted *sum* of $\Phi$-pairs. You cannot hedge a jump with $\Delta$ shares, so the market is no longer complete, and the price is no longer unique: it depends on what the market charges for jump risk.
- **Local volatility.** Or let $\sigma=\sigma(S,t)$, fitted so that every quoted strike is recovered exactly (Dupire, 1994). One function reproduces the whole smile today. But $S_T$ is then typically not lognormal, and the two-$\Phi$ formula is being used as a quoting dictionary, not as a model.

A deterministic but time-varying $\sigma(t)$, by contrast, changes nothing: $s^2=\int_t^T\sigma(u)^2\,du$ is still one number, and $(1)$ survives with that $s$. That is the **term structure** of volatility, and it is the one perturbation in this section that the formula absorbs.

## Everything else

**European exercise.** Vol. II integrated over the law of $S_T$ only; the path was invisible. An American put can be exercised at any time, so its value depends on the whole path of opportunities. There is a free boundary — a critical stock price below which you exercise — and no two-$\Phi$ formula. The honest computation is the tree of Vol. II with one change: at each node, take the maximum of exercising now and the discounted risk-neutral value of holding. Or the PDE of §1, with the constraint $V\ge (K-S)^+$ everywhere. Barrier options (knocked out if $S$ touches a level) and Asian options (paying on the average of $S$) break the formula for the same reason: the payoff sees the path.

**Frictionless and continuous.** The hedge in §1 rebalances continuously. With transaction costs, continuous rebalancing costs infinitely much, so you rebalance discretely and the hedge leaks. The price becomes a band again, widening with costs and with how often you trade.

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
    <tr><td>one \(\sigma\)</td><td>\(\sigma(t)\) deterministic; \(\sigma(S,t)\); smile \(\sigma(K)\)</td><td>survives as \(s^2=\int\sigma^2\); breaks; quoting dictionary</td></tr>
    <tr><td>payoff \((S_T-K)^+\)</td><td>American; barrier; Asian; cash-or-nothing</td><td>breaks; breaks; breaks; <em>is</em> the second \(\Phi\)</td></tr>
    <tr><td>\(r\) constant</td><td>\(r(t)\) deterministic; random \(r_t\)</td><td>survives; morphs (bond numeraire)</td></tr>
    <tr><td>one rate for borrowing and lending</td><td>\(r_b>r_\ell\)</td><td>a band, not a price</td></tr>
    <tr><td>pricing law is \(\mathbb{Q}\)</td><td>physical \(\mu\) instead of \(r\)</td><td>shape lives, number is wrong</td></tr>
    <tr><td>multiplicative, \(S_T>0\)</td><td>additive Gaussian (Bachelier)</td><td>different \(\Phi\), no \(\ln\)</td></tr>
    <tr><td>no dividends</td><td>yield \(q\); discrete \(D\)</td><td>morphs (\(e^{-q\tau}\)); patched</td></tr>
    <tr><td>frictionless, continuous</td><td>transaction costs</td><td>a band, not a price</td></tr>
  </tbody>
</table>

The assumptions are doing a lot of work. They are why a rain check on a stock has a two-line formula and a rain check on an average, or on a stock that can jump, does not.

---

# What was proved
{: #what-was-proved}

The theorem we proved is narrower than the word "option." It prices a European call on a stock that pays no dividend, driven by one Wiener process with a constant $\sigma$, in a market where you can trade continuously and without cost at a known rate $r$. In that complete market, the unique no-arbitrage price of $(S_T-K)^+$ is $(1)$. We reached it three ways: an integral against a lognormal, the heat equation, and a change of unit. Using that theorem as a price, as a quoting convention, or as the first term of an approximation is a separate decision.

Three volumes: the contract and its assumptions; the noise, the lognormal, and the integral; heat, numeraires, and nuance. The rain check is $10.45$.

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

---

*Black-Scholes-Merton:* [Vol. I](/blog/2024/07/24/Black-Scholes-Merton) · [Vol. II](/blog/2024/07/24/Black-Scholes-Merton-Vol-II) · **Vol. III**
