---
layout: post
title: "Back-of-the-Envelope: Mean-Reverting VIX, Vol. VI: Trading It, Honestly"
date: 2026-03-09 12:05:00
description: "Five trades a fitted VIX smile suggests, checked against the 2026 results: one fear premium measured, one hedge ratio inverted, three ideas left unsupported."
mathjax: true
categories: wealth
---

*Mean-Reverting VIX:* [I](/blog/2026/03/09/rafaga) · [II](/blog/2026/03/09/rafaga-Vol-II) · [III](/blog/2026/03/09/rafaga-Vol-III) · [IV](/blog/2026/03/09/rafaga-Vol-IV) · [V](/blog/2026/03/09/rafaga-Vol-V) · **VI**

{% include vix-kit.html %}

*A model that fits the smile suggests five ways to make money. This volume puts each one against the results of [Vol. V](/blog/2026/03/09/rafaga-Vol-V). One survives as a measurement, one inverts, two are undercut by what calibration can and cannot see, and one is beyond what this research tested. None of this is investment advice; none of it is backtested.*

Fitting a smile does not give you a crystal ball. It gives you a precise description of how the market *currently* prices risk, and every trade below is a bet that the description differs from what will happen, or from itself. The question for each is simple: does anything in the research support it?

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#premium">Selling the fear premium</a></li>
  <li><a href="#skew">Relative value on the skew</a></li>
  <li><a href="#hedging">Jump-aware hedging</a></li>
  <li><a href="#calendar">Calendar spreads on mean reversion</a></li>
  <li><a href="#spx">VIX against SPX</a></li>
  <li><a href="#next">What would actually move this forward</a></li>
  <li><a href="#lesson">The lesson</a></li>
</ol>
</div>

---

# Selling the fear premium
{: #premium}

The idea: options price VIX spikes under $\mathbb Q$, history delivers them under $\mathbb P$ ([Vol. II](/blog/2026/03/09/rafaga-Vol-II#two-worlds)), and if $\mathbb Q$ expects far more spikes than $\mathbb P$, selling out-of-the-money VIX calls collects the difference. The obvious way to measure the gap is $\lambda_{\mathbb Q}$ against $\lambda_{\mathbb P}$.

That comparison does not survive [Vol. IV](/blog/2026/03/09/rafaga-Vol-IV#identification): the fitted jump rate moves from 5.2 to 2.1 across four maturities as the fit slides along its ridge, so there is no single $\lambda_{\mathbb Q}$ to compare. The model-free version in [Vol. V](/blog/2026/03/09/rafaga-Vol-V#regime) does survive. Here it is in money: the price you would have received selling October 2026 calls at the bid on 29 September, against their average payoff in history (the 1,667 days from 2004 to early 2026 with the VIX between 14 and 18, around the 16.04 spot, looking 16 trading days ahead to expiry, discounted):

<table class="cs-err">
  <thead><tr><th>strike</th><th>bid</th><th>historical expected payoff</th><th>bid ÷ expected payoff</th></tr></thead>
  <tbody>
    <tr><td>20</td><td>0.90</td><td>0.63</td><td>1.4</td></tr>
    <tr><td>25</td><td>0.47</td><td>0.26</td><td>1.8</td></tr>
    <tr><td>30</td><td>0.28</td><td>0.15</td><td>1.9</td></tr>
    <tr><td>40</td><td>0.13</td><td>0.075</td><td>1.7</td></tr>
  </tbody>
</table>

Sellers were paid 1.4 to 1.9 times what these calls have historically paid out. That is the premium, and it is largest in the tail, where the jumps are. **This is the one idea of the five that the data support**, as a measurement.

As a strategy, three things stand in the way. The historical outcomes above 30 are 24 overlapping days from five episodes (the May 2010 flash crash, August 2011, the COVID crash of February–March 2020, the turn of 2022 and April 2025), so the "expected payoff" in the tail is really five events averaged. Two famous spikes are not even in it: February 2018 and August 2024 had reverted below 30 within sixteen trading days. Short calls lose everything they collected many times over when one of those events arrives: 5 February 2018 took the VIX from 17 to 37 in a day. And this is one day's chain. A premium you would trade needs to be measured on hundreds of days, with the losing days counted in full. The model's role is modest but real: MRLRJ reproduces the option-implied tail probabilities of [Vol. V](/blog/2026/03/09/rafaga-Vol-V#regime) to within half a percentage point, so it can price the premium strike by strike and at strikes that are not quoted.

---

# Relative value on the skew
{: #skew}

The idea: fit the smile, find the strikes that sit off it (say a block trade has pushed one strike up), and sell that strike against its fairly priced neighbor. With a fit error under 3%, the argument goes, MRLRJ has the resolution to see such dislocations.

The trade's logic is sound; the resolution argument runs backwards. On 29 September, across the four expiries, MRLRJ put 100%, 98%, 98% and 93% of its prices *inside* the bid–ask spread. A dislocation you can trade has to exceed the spread you pay to trade it, and the model found almost none. That is not the model failing; it is the market being efficient on that day, at the precision the model can see. What the model *can* do is flag the few quotes that fall outside the spread and watch whether they persist from day to day. That is a screening tool, and it needs a panel of days to know whether its flags mean anything.

---

# Jump-aware hedging
{: #hedging}

The idea: a VIX option has to be hedged with VIX futures, and Black's delta ignores jumps, so a jump-aware delta ought to be larger.

Here is that comparison for the October fit ([script](https://github.com/juleshenry/rafaga/blob/main/julia_impl/scripts/hedge_ratios.jl)). For each strike, the MRLRJ futures hedge ratio $\partial C/\partial F$, against the Black delta at the volatility that reproduces the same price:

<table class="cs-err">
  <thead><tr><th>strike</th><th>MRLRJ call</th><th>MRLRJ hedge ratio</th><th>Black delta</th><th>ratio</th></tr></thead>
  <tbody>
    <tr><td>16</td><td>1.91</td><td>0.646</td><td>0.772</td><td>0.84</td></tr>
    <tr><td>18</td><td>1.21</td><td>0.272</td><td>0.491</td><td>0.56</td></tr>
    <tr><td>20</td><td>0.90</td><td>0.186</td><td>0.348</td><td>0.54</td></tr>
    <tr><td>25</td><td>0.51</td><td>0.103</td><td>0.184</td><td>0.56</td></tr>
    <tr><td>30</td><td>0.32</td><td>0.064</td><td>0.113</td><td>0.57</td></tr>
    <tr><td>40</td><td>0.15</td><td>0.031</td><td>0.054</td><td>0.57</td></tr>
  </tbody>
</table>

<div class="cs-q"><strong>The tempting claim:</strong> For a short-dated out-of-the-money VIX call, the MRLRJ delta exceeds the Black delta, by something like 30–40%.</div>
<div class="cs-a"><strong>The data says:</strong> The opposite. The MRLRJ hedge ratio is 16–46% <em>smaller</em>. Hedging with Black's delta at the market's implied volatility would over-hedge an out-of-the-money VIX call by nearly a factor of two.</div>

There is a clean reason. In every model of this family, $\ln\text{VIX}_T = \phi\ln\text{VIX}_t + (\text{something independent of }\text{VIX}_t)$ with $\phi = e^{-\kappa\tau}$, so $\text{VIX}_T$ scales like $\text{VIX}_t^{\,\phi}$, and so does $F$. Differentiate the call and the future with respect to $\text{VIX}_t$ and divide:

$$\frac{\partial C}{\partial F} = D\,\Pi_1,$$

where $\Pi_1$ is the probability of finishing in the money under the measure that weights each outcome by $\text{VIX}_T/F$, from [Vol. III](/blog/2026/03/09/rafaga-Vol-III#gil-pelaez). Black's delta is $D\,\Phi(d_1)$ at a volatility inflated to pay for the jump tail, and for an out-of-the-money strike that inflation pushes $\Phi(d_1)$ up. An out-of-the-money VIX call is mostly worth its jump tail, and moving the VIX level today barely changes the odds of a 35% jump tomorrow.

The practical caveat is bigger than the formula. In a jump model no futures position hedges the jump itself: the hedge ratio neutralizes small moves, and the jump risk is what you are paid for and cannot delta away. And the ratio comes from the October fit, the one maturity whose parameters looked sensible.

---

# Calendar spreads on mean reversion
{: #calendar}

The idea: after a spike, near-dated options price sustained panic; $\kappa$ says how fast the VIX will fall back; sell the near expiry, buy the deferred one, weighted by the model's decay curve.

Two results undercut this. First, [Vol. IV](/blog/2026/03/09/rafaga-Vol-IV#identification): the options do not identify $\kappa$. Across the 2026 fits it ranges from 0.009 to 88.5. Second, [Vol. V](/blog/2026/03/09/rafaga-Vol-V#term-structure): no constant-parameter model fits the four expiries together; the best one prices half the quotes inside the spread. A calendar spread is a bet on the *relationship between* expiries, which is exactly what these models do not capture.

The defensible $\kappa$ is the historical one, 5.57 per year, half-life 31 trading days ([Vol. I](/blog/2026/03/09/rafaga#what-22-years-say)). And the decay runs in logs, not in VIX points. From 40, with a long-run level of 17.7, the median $\mathbb P$-path of a log-OU is about 26.6 after 31 trading days and about 21.7 after 62; halving the distance in points would say about 29 and 23. Comparing that real-world decay with the decay the futures curve implies is a legitimate idea. It is a statement about $\mathbb P$ against $\mathbb Q$ across maturities, and nothing in this research has tested it.

---

# VIX against SPX
{: #spx}

The idea: compute a theoretical VIX from SPX options and trade its gap to VIX derivatives. The VIX is defined from SPX options ([Vol. I](/blog/2026/03/09/rafaga#what-the-vix-is)), so a joint model is the natural endgame. But this research modeled the VIX alone and never touched an SPX quote. There is nothing here to support or refute the trade; it belongs in the next section.

---

# What would actually move this forward
{: #next}

- **A panel.** Nearly everything in [Vol. V](/blog/2026/03/09/rafaga-Vol-V) is one day. [`fetch_cboe.jl`](https://github.com/juleshenry/rafaga/blob/main/julia_impl/scripts/fetch_cboe.jl) saves a snapshot in a second; run it every close for a year and the fear premium, the stability of the jump shape $\eta$, and the persistence of off-smile quotes all become measurable.
- **Time-dependent parameters.** The thesis' own answer to the term structure: $\theta_t$ to match the futures curve exactly, $\sigma_t$ to match at-the-money volatility per maturity. It will fit; the question is whether what is left over is stable.
- **Clustered jumps.** Two of the five largest one-day percentage rises in the VIX since 2004 were four months apart in 2024. Poisson jumps are independent by construction. A self-exciting (Hawkes) jump process lets one spike raise the odds of the next.
- **Rough volatility and joint SPX–VIX models.** The modern frontier, and the only route to the SPX trade. Both are bigger projects than a 2013 thesis.

---

# The lesson
{: #lesson}

It would be easy to end on a lesson about tools: double precision bad, `BigFloat` good, and a model from 2013 that prices VIX derivatives to 97% accuracy in 2026.

The results say something different. The tool is not the problem: double precision agrees with a 25-digit `BigFloat` quadrature to $10^{-9}$. The model is good at what it does, which is fit one expiry's smile inside the bid–ask spread, thirteen years after the thesis and in a completely different market. What it does not do is *measure* the things it is tempting to read off it (the reversion speed, the long-run level, the jump rate), because a single expiry cannot see them. And the most useful number in the whole series did not come from a parameter at all. It came from comparing the option market's tail probabilities with history, and it says the market pays about twice the historical rate for a VIX spike.

The count: one package, three models, 34 tests, a five-page [paper](https://github.com/juleshenry/rafaga/blob/main/paper/rafaga.pdf), one full option chain, one premium measured, one delta inverted, and a list of things still to test.

Ráfaga. A gust. Fewer of the numbers hold up than a first fit suggests, and the ones that do are real. And the VIX, as always, reverts to the mean, at least under $\mathbb P$.
