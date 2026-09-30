---
layout: post
title: "Back-of-the-Envelope: Mean-Reverting VIX, Vol. IV: Calibration, and What the Thesis Didn't Say"
date: 2026-03-09 12:03:00
mathjax: true
categories: wealth
---

*Mean-Reverting VIX:* [I](/blog/2026/03/09/rafaga) · [II](/blog/2026/03/09/rafaga-Vol-II) · [III](/blog/2026/03/09/rafaga-Vol-III) · **IV** · [V](/blog/2026/03/09/rafaga-Vol-V) · [VI](/blog/2026/03/09/rafaga-Vol-VI)

{% include vix-kit.html %}

*Calibration turns a model into numbers. The thesis published its numbers but not its method. This volume reconstructs the method, tests the published numbers without the data they came from, and finds that some of them could have been anything.*

After [Vol. III](/blog/2026/03/09/rafaga-Vol-III) we can price VIX futures and options under MRLR, MRLRJ and MRLRSV. What we do not have is parameters. The historical fit of [Vol. I](/blog/2026/03/09/rafaga#what-22-years-say) gives real-world ($\mathbb P$) values; prices need risk-neutral ($\mathbb Q$) ones, and the only source of those is the option market itself.

<div class="cs-toc">
<strong>Contents</strong>
<ol>
  <li><a href="#calibration">what calibration is</a></li>
  <li><a href="#the-recipe">the thesis' recipe</a></li>
  <li><a href="#what-is-missing">what is missing, and what we chose</a></li>
  <li><a href="#consistency">testing 2011 without the 2011 data</a></li>
  <li><a href="#identification">parameters that are not there</a></li>
</ol>
</div>

---

# what calibration is
{: #calibration}

<div class="ev-def"><strong>Definition (calibration).</strong> Given market prices $C^{\text{mkt}}_j$ of options with strikes $K_j$, and a model with parameters $p$ producing prices $C^{\text{mod}}_j(p)$, calibration picks
$$\hat p = \arg\min_p\ \mathcal L\big(C^{\text{mod}}(p),\, C^{\text{mkt}}\big)$$
for some loss $\mathcal L$.</div>

That one line hides four decisions, and every one of them changes the answer: which quotes, which loss, which optimizer, and which parameter values are allowed. A published calibration that does not state all four cannot be reproduced. Keep that in mind for the next two sections.

---

# the thesis' recipe
{: #the-recipe}

Chapter 7 of the thesis states the first two decisions clearly.

**Quotes.** Delayed Cboe quotes of VIX calls, downloaded on 26 September 2011 at 10:01 ET, with spot VIX at 42.3. Six expiries were listed, from October 2011 to March 2012. Calls with a zero bid are dropped, then calls with zero open interest; the last two expiries are dropped as illiquid. That leaves 30, 31, 32 and 35 calls in the first four expiries. Prices are the bid–ask mid.

**Loss.** The obvious choice is mean squared error, $\sum_j (C^{\text{mod}}_j - C^{\text{mkt}}_j)^2$. It is dominated by the expensive in-the-money calls: a 5% miss on a 20-dollar call counts ten thousand times more than a 5% miss on a 20-cent one. Fitting logarithms, $\sum_j(\ln C^{\text{mod}}_j - \ln C^{\text{mkt}}_j)^2$, has the opposite problem. Following Rebonato, the thesis adds the two:

$$\mathcal L_{\text{MMLSE}} = \sum_j \big(C^{\text{mod}}_j - C^{\text{mkt}}_j\big)^2 + \alpha\sum_j\big(\ln C^{\text{mod}}_j - \ln C^{\text{mkt}}_j\big)^2, \qquad \alpha = 8.$$

It fits each expiry separately, with every parameter free -- including $\theta$ -- and the spot VIX plugged in as the starting value. Fit quality is reported as the percentage error $\text{PE} = \text{mean}\,\lvert C^{\text{mod}} - C^{\text{mkt}}\rvert/C^{\text{mkt}}$ and the mean absolute error (MAE):

<table class="cs-err">
  <thead><tr><th>Sep 2011, PE</th><th>Oct 11</th><th>Nov 11</th><th>Dec 11</th><th>Jan 12</th></tr></thead>
  <tbody>
    <tr><td>MRLR</td><td>6.91%</td><td>4.66%</td><td>6.61%</td><td>5.73%</td></tr>
    <tr><td>MRLRJ</td><td>3.25%</td><td>3.81%</td><td>5.21%</td><td>3.11%</td></tr>
    <tr><td>MRLRSV</td><td>3.18%</td><td>3.68%</td><td>5.07%</td><td>2.98%</td></tr>
  </tbody>
</table>

The thesis' conclusions follow: MRLR is worst, jumps or random vol-of-vol fix it, and they fix it about equally.

---

# what is missing, and what we chose
{: #what-is-missing}

The other two decisions -- the optimizer and the allowed parameter region -- are not in the thesis. Neither are the quotes, only their counts. That is not unusual for a thesis. It does mean nobody can recompute Table 7.2, including me.

So the rebuilt code has to choose, and states its choices ([`calibration.jl`](https://github.com/juleshenry/rafaga/blob/main/julia_impl/src/calibration.jl); Section 5 of the [paper](https://github.com/juleshenry/rafaga/blob/main/paper/rafaga.pdf)):

<table class="cs-err">
  <thead><tr><th>Decision</th><th>Choice</th></tr></thead>
  <tbody>
    <tr><td>quotes</td><td>as the thesis: calls, positive bid and open interest, mid prices, first four monthly expiries</td></tr>
    <tr><td>loss</td><td>as the thesis: MMLSE with $\alpha = 8$</td></tr>
    <tr><td>parameters</td><td>positive ones as $e^x$; $\eta = 1 + e^x$ (so the future exists, Vol. III); $\rho = \tanh x$; MRLRSV box-bounded, $\kappa\in[0.1, 50.1]$, $\theta\in[1,5]$, $\kappa_v,\theta_v<50$, $\sigma_v, V_0<30$</td></tr>
    <tr><td>optimizer</td><td>Nelder–Mead from 10 random starts (6 for MRLRSV), seeds $1{+}k$, plus one restart from each optimum; at most 3,000 iterations and 300 s per run</td></tr>
  </tbody>
</table>

<div class="cs-q"><strong>March 2026 said:</strong> "Minimize this using Nelder-Mead... Starting guess: $\kappa = 5$, $\theta = 2.8$, $\sigma = 1$, $\lambda = 2$, $\eta = 2$. The optimizer converges to physically meaningful parameters. The MAPE settles under 3%."</div>
<div class="cs-a"><strong>The data says:</strong> That calibration fitted <em>last traded prices</em> of one expiry, which can be hours or days stale, from a single starting point, with parameters forced positive by <code>abs()</code> -- which makes the loss non-smooth exactly where the optimizer is working. None of that makes it wrong, but none of it can tell a good fit from a lucky one. The last section of this volume shows what "physically meaningful" parameters turn out to mean.</div>

---

# testing 2011 without the 2011 data
{: #consistency}

Without the quotes we cannot check the thesis' errors. We can still check its *parameters*, and whether this code reads them the way the thesis meant.

The idea: Tables 7.5 (MRLRJ) and 7.6 (MRLRSV) were fitted separately to the **same** quotes. Each model's prices sit, on average, 0.12–0.21 from the market (Table 7.3). Two sets of prices that are each that close to one market must be close to each other. So price both parameter sets with this code at the thesis' inputs (VIX 42.3, strikes 20 to 90) and compare them. If the code had the jump term's sign wrong, or read $\eta$ as a mean rather than a rate, or mis-scaled the Riccati equation, two structurally different models would disagree. If the code is right, they must agree.

<table class="cs-err">
  <thead><tr><th>Expiry</th><th>mean |MRLRJ − MRLRSV|</th><th>allowed by Table 7.3</th><th>mean |MRLR − MRLRJ|</th></tr></thead>
  <tbody>
    <tr><td>18 Oct 2011</td><td>0.035</td><td>0.238</td><td>0.173</td></tr>
    <tr><td>15 Nov 2011</td><td>0.019</td><td>0.359</td><td>0.105</td></tr>
    <tr><td>20 Dec 2011</td><td>0.022</td><td>0.409</td><td>0.079</td></tr>
    <tr><td>17 Jan 2012</td><td>0.022</td><td>0.261</td><td>0.121</td></tr>
  </tbody>
</table>

They agree to two to three and a half cents at every maturity, ten times tighter than required, while MRLR sits further away, as it should. The implied volatilities match the levels in the thesis' Figure 7.3 as well (for October, MRLRJ gives 1.27, 1.39 and 1.48 at strikes 40, 60 and 80, against a plotted range of 1.2–1.8). This is as close to reproducing the thesis as its publication allows, and it says the code and the thesis agree ([script](https://github.com/juleshenry/rafaga/blob/main/julia_impl/scripts/reproduce_paper.jl), [output](https://github.com/juleshenry/rafaga/blob/main/results/paper_2011_check.md)).

The same exercise recovers numbers the thesis never printed. The model futures implied by its parameters are 37.8–38.5 for October 2011 falling to about 32 for December: a backwardated curve, as the text says it was. And it shows the undisclosed bounds. **$\theta = 3.00$ in all four MRLRJ fits, and $\rho = 1.00$ in all four MRLRSV fits.** Estimates do not land on round numbers four times in a row. Those are parameters pressed against a wall that the thesis never mentions, and their "fitted values" are the location of the wall.

---

# parameters that are not there
{: #identification}

Now the deeper problem. Take MRLR and a single expiry. The model's prices depend on its three parameters only through two numbers: the mean $\mu$ and variance $v$ of $\ln\text{VIX}_T$ ([Vol. II](/blog/2026/03/09/rafaga-Vol-II#options)),

$$\mu = \phi\ln\text{VIX}_t + (1-\phi)\,\theta, \qquad v = \frac{\sigma^2}{2\kappa}\big(1-\phi^2\big), \qquad \phi = e^{-\kappa\tau}.$$

Three parameters, two numbers. For any $\kappa$ you like there is a $\theta$ that restores $\mu$ and a $\sigma$ that restores $v$, and the prices do not change. The loss has a ridge: a line of parameter values along which it is exactly flat.

<div class="ev-def"><strong>Definition (identification).</strong> A parameter is <em>identified</em> by some data if different values of it produce different distributions of that data. If two parameter values fit every possible dataset equally well, no amount of data can tell them apart.</div>

It is not a subtle effect. On the October 2026 expiry, fix $\kappa$ and refit $\theta$, $\sigma$:

<table class="cs-err">
  <thead><tr><th>fixed $\kappa$</th><th>best loss</th><th>$\theta$</th><th>$\sigma$</th></tr></thead>
  <tbody>
    <tr><td>0.5</td><td>120.910550</td><td>−11.63</td><td>2.61</td></tr>
    <tr><td>2</td><td>120.910550</td><td>−0.99</td><td>2.73</td></tr>
    <tr><td>8</td><td>120.910550</td><td>1.66</td><td>3.20</td></tr>
    <tr><td>32</td><td>120.910550</td><td>2.28</td><td>5.08</td></tr>
  </tbody>
</table>

Identical to nine digits, with long-run VIX levels $e^\theta$ ranging from $10^{-5}$ to 10. The thesis reports MRLR reversion speeds of $\kappa = 11.05$, 11.43, 9.88 and 12.58. Those are points on a ridge; the optimizer stopped wherever it happened to be.

<div class="cs-q"><strong>March 2026 said:</strong> "The parameters $\kappa$ and $\theta$ remain stable and physically interpretable across different calibration windows... The reversion speed $\kappa$ sits in the 3-8 range, implying a half-life of 30-80 trading days. This is not a fitted artifact."</div>
<div class="cs-a"><strong>The data says:</strong> From one expiry, $\kappa$ is exactly a fitted artifact. In the 2026 fits of <a href="/blog/2026/03/09/rafaga-Vol-V">Vol. V</a> it ranges from 0.009 to 88.5 across models and maturities. The 3–8 range is what the <em>time series</em> gives ($\kappa = 5.57$ in <a href="/blog/2026/03/09/rafaga#what-22-years-say">Vol. I</a>), and it is identified there for a reason: 22 years of daily data watch the VIX revert over every horizon at once. One option expiry watches one horizon.</div>

The jump model is not immune. Its parameters enter through more than two numbers, so the ridge is not exactly flat, but it is close. In 2026 the MRLRJ fits beyond October slide down it to $\kappa\approx0.01$ and $\theta\approx-15$ to $-23$. Along that slide the product $\kappa\theta$ stays near $-0.2$, and the drift $\kappa(\theta - \ln\text{VIX})\approx\kappa\theta$ becomes a constant. That is, the model quietly stops mean-reverting and turns into a Brownian motion with drift plus jumps. The per-maturity fit cannot tell reversion from drift, and it does not need to, because both price one expiry equally well.

The practical rule that falls out: **a per-maturity calibration measures prices, not dynamics.** Its parameters are coordinates on a surface that fits a smile. Reading a half-life off them, or a long-run level, or a jump frequency, needs something that constrains more than one horizon at a time: a time series, or several expiries fitted together. [Vol. V](/blog/2026/03/09/rafaga-Vol-V) tries the second.

---

# where this goes
{: #where-this-goes}

We have a reconstructed recipe that matches the thesis where the thesis can be checked, and a warning about how to read what it produces. Time to point it at a market fifteen years younger.

---

**Next:** [Vol. V: Twenty Twenty-Six](/blog/2026/03/09/rafaga-Vol-V)

*Mean-Reverting VIX:* [Vol. I](/blog/2026/03/09/rafaga) · [Vol. II](/blog/2026/03/09/rafaga-Vol-II) · [Vol. III](/blog/2026/03/09/rafaga-Vol-III) · **Vol. IV** · [Vol. V](/blog/2026/03/09/rafaga-Vol-V) · [Vol. VI](/blog/2026/03/09/rafaga-Vol-VI)
