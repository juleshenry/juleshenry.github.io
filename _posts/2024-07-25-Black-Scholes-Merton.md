---
layout: post
title: "Back-of-the-Envelope: Black Scholes Merton"
date: 2024-07-24
categories: wealth 
---
# What is an option?
Is it optional to know what an option is? No!

In the context of finance, an option refers to a contract that gives its owner the right, but not the obligation, to buy or sell an underlying asset e.g. shares in a company or bushels of wheat at a predetermined price on or before a specific date.

Options are used for various purposes including risk management and speculation. Herein we derive the formula for pricing a European option.

## Calls & Puts: Bets In-Favor & Bets Against
Options come in two flavors. A *call* is a bet in-favor of the underlying asset whereas a *put* essentially is a bet against underlying asset.

A **call option** gives the purchaser the right, but not the obligation to purchase an underlying security, an asset like a stock or commodity, at a specified price, known as the *strike price*, within a certain timeframe, known as the *tenor*. For this right, the purchaser pays an upfront cost, known as the *premium*, to the seller.

If the market value of the security exceeds the strike price, the option becomes profitable, also known as in-the-money. To see this, note that the purchaser can now buy the asset at the strike price and sell the asset at the higher market rate, directly profiting from the difference. Otherwise, why would you execute the contract? You will buy an asset for a higher price than the market will, losing money, hence the option is otherwise out-of-the-money.

A **put option** achieves the opposite effect by enabling its purchaser the right but not the obligation to **sell** the underlying asset at a specified price.

## Europeans and Americans
Options in finance come in two types: European and American. Here's a detailed comparison between them based on 
various features:

1. **Exercise Timing**: The key difference lies in when the holder can exercise their option rights (buy or 
sell):
* **European Options**: These can only be exercised at maturity, i.e., exactly at a specific date 
predetermined on the contract's expiration day. They do not allow exercising before this maturity date, which 
makes them simpler to price compared to American options but limits their use for certain strategies.
* **American Options**: These can be exercised any time up until and including the option’s expiration date. 
This flexibility allows investors more control over whether or not to exercise an option based on market 
conditions, making them slightly more complex to price due to this added layer of decision-making.

2. **Pricing**: Given their differences in exercise timing, these options are priced differently using different 
mathematical models:
* European Options: The most common pricing model used for European options is the Black-Scholes Model (BSM), 
which assumes constant volatility and risk-free interest rates over time. We delve into the BSM formula [later in the post](#How-do-we-price-one-of-these-things), so keep reading.
* American Options: Pricing an American option generally involves numerical methods such as binomial trees, 
finite difference method or Monte Carlo simulation because of their flexibility in exercise timing. Each model has its own limitations and assumptions regarding the behavior of asset prices (volatility, return rates) and market conditions over time.

3. **Applications**: The choice between European and American options often comes down to specific investment 
strategies or needs of an investor due to their different exercise features:
* **European Options**: These are typically used when a buyer is seeking protection (hedging) against losses 
in the underlying asset's price movements. For instance, they might be employed by companies holding large 
amounts of stock for hedging purposes or by investors who don’t need to exercise early due to specific market 
views.
* **American Options**: Their flexible nature often suits buyers looking to speculate on future price changes 
in the underlying asset over a longer horizon, as they can choose the optimal time to exercise based on changing 
market conditions or news announcements affecting the underlier's value. However, their complexity and the need 
for advanced mathematical models make them more suitable for professional investors with deep trading expertise.

In summary, while both types of options grant a right to buy or sell an underlying asset at a predetermined price before maturity, European and American options vary significantly in terms of exercise timing, pricing methods, and their applications within investment strategies and risk management techniques.

# How do we price one of these things?

The canonical formula for the European option was developed by three economists Fischer Black and Myron Scholes, and Robert C. Merton, known as the Black–Scholes–Merton (BSM) model.

# Black-Scholes Model

```math
C = S⋅N(d_1) - K⋅e^{-r⋅τ}N(d_2)
```

```math
d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)τ}{\sigma\sqrt{τ}} \quad \text{and} \quad d_2 = d_1 - \sigma\sqrt{τ}
```

## Required Inputs:

- **S** = Current stock price  
- **K** = Option strike price  
- **r** = Risk-free interest rate  
- **τ** = Time remaining until option expiration, often expressed as T-t
- **σ** = Volatility of the stock

Where N is the normal distribution function.

## What are the four assumptions?

BSM requires one to make four reasonable assumptions about the market.

1. The stock price follows a geometric Brownian motion with constant volatility and drift rate. This means the 
changes in stock prices over time have an exponential distribution, exhibit continuous compounding, and that 
this process is not influenced by other factors (e.g., market events).

2. There are no dividends during the option's life period. Dividends can reduce the price of a call or increase 
the price of a put because they decrease the stock price when paid out. By excluding them, we simplify calculations.

3. Markets are efficient, meaning that asset prices reflect all available information, and investors cannot profit from trading in an arbitrage opportunity (i.e., buying undervalued securities and selling overvalued ones). 

4. The risk-free interest rate is constant throughout the option's life. This assumption simplifies calculations by assuming that there are no investment opportunities with guaranteed returns over time.

Further exploration of the difference between the ideal world of BSM and flesh-and-blood markets is discussed in [the Volatility Smile](https://www.wiley.com/en-us/The+Volatility+Smile-p-9781118959169), a seminal book in finance. We couch discussion of the nuances of the assumptions themselves for a future post.

## Stochastic Calculus part///The BSM Economy 
To understand BSM, you will need to learn some stocastic calculus.

There are two assets: a risky stock $S$ and riskless bond $B$. These assets are driven by the SDEs

$$
\begin{aligned}
dS_t &= \mu S_t dt + \sigma S_t dW_t \quad \\
dB_t &= r_t B_t dt
\end{aligned}
$$

The time zero value of the bond is $B_0 = 1$ and that of the stock is $S_0$. 
By Itô’s Lemma the value $V_t$ of a derivative written on the stock follows the diffusion

$$
\begin{aligned}
dV_t &= \frac{\partial V}{\partial t} dt + \frac{\partial V}{\partial S} dS + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} (dS)^2 \quad \text{(3)} \\
&= \frac{\partial V}{\partial t} dt + \frac{\partial V}{\partial S} dS + \frac{1}{2} \frac{\partial^2 V}{\partial S^2} \sigma^2 S^2 dt \\
&= \left( \frac{\partial V}{\partial t} + \mu S_t \frac{\partial V}{\partial S} + \frac{1}{2} \sigma^2 S_t^2 \frac{\partial^2 V}{\partial S^2} \right) dt + \left( \sigma S_t \frac{\partial V}{\partial S} \right) dW_t.
\end{aligned}
$$

### A Detour to Japan
To follow this derivation, you will need to learn about the world of stochastic calculus. This field was pioneered by Japanese mathematician Kiyosi Itô, who discovered an essential result in stochastic calculus that provides the mathematical foundation for analyzing continuous-time stochastic differential equations (SDEs). 

Here are its key components:

1. **Stochastic Processes**: In finance, many quantities—such as stock prices or interest rates—are modeled as stochastic processes rather than deterministic ones due to their inherent randomness and unpredictability over time. Stochastic differential equations (SDEs) are used to describe these dynamic systems mathematically. In a stochastic system, each movement from one state to the next is governed by a probability, in our case, for the financial markets, the probability is sampled from a normal distribution. The canonical name for such a motion is a Brownian motion from physics or martingale from economics.

2. **Itô's Lemma**: Itô's lemma is a powerful tool for finding the differential of functions of stochastic processes that satisfy an SDE, particularly when applied in financial modeling and derivative pricing. In essence, Ito's lemma enables us to understand how certain observable quantities (like option prices or portfolio 
values) change over time under volatility and random market conditions.

3. Functional Derivative: At its core, the lemma provides a formula for the differential of a function composed with a stochastic process defined by an SDE. For instance, if we have a function f(t, X(t)), where t denotes time and X(t) represents a stochastic process following an SDE, Ito's Lemma tells us how df changes in relation to dt (time increment) and dX (increment of the random variable).

4. **Formula**: The formula for Itô's Lemma is given by:
$$
df(t, X_t) = \frac{\partial f}{\partial t}\,dt + \frac{\partial f}{\partial x}\,dX_t + \frac{1}{2}\frac{\partial^2 f}{\partial x^2}\,(dX_t)^2,
$$
where:
- $df$ represents the differential of the function $f(t, X_t)$,
- $dX_t$ is the infinitesimal increment of the stochastic process $X_t$.

The first term, $\frac{\partial f}{\partial t}\,dt$, captures the explicit time dependence of $f$.  
The second term, $\frac{\partial f}{\partial x}\,dX_t$, reflects the sensitivity of $f$ to changes in $X_t$.  
The third term, $\frac{1}{2}\frac{\partial^2 f}{\partial x^2}\,(dX_t)^2$, accounts for the quadratic variation of the stochastic process—this is a key feature of Itô calculus that distinguishes it from ordinary calculus. In particular, when $X_t$ follows a diffusion process (e.g., $dX_t = \mu\,dt + \sigma\,dW_t$), the term $(dX_t)^2$ contributes a non-vanishing $O(dt)$ component (e.g., $\sigma^2\,dt$), which must be retained.

- **Partial Derivatives**: These measure how the function $f(t, X_t)$ changes with respect to its independent variables. Specifically:
  - $\frac{\partial f}{\partial t}$ captures the sensitivity to **time** $t$ (with $X_t$ held fixed),
  - $\frac{\partial f}{\partial x}$ and $\frac{\partial^2 f}{\partial x^2}$ capture the first- and second-order sensitivities to the **stochastic process** $X_t$ (with time held fixed).

- **Quadratic Variation Term**: The term $\frac{1}{2}\frac{\partial^2 f}{\partial x^2}(dX_t)^2$ arises from the **quadratic variation** of the stochastic process $X_t$. Unlike in ordinary calculus, $(dX_t)^2$ does not vanish; for Itô processes driven by Brownian motion, it contributes a deterministic $O(dt)$ component (e.g., if $dX_t = \mu\,dt + \sigma\,dW_t$, then $(dX_t)^2 = \sigma^2\,dt$). This term accounts for the cumulative effect of random fluctuations and is essential for correctly modeling dynamics in stochastic calculus.

In financial mathematics, Itô's lemma plays an instrumental role by allowing analysts and traders to derive the dynamic pricing models (like Black-Scholes formula) that govern modern derivative markets—essentially helping us understand how prices evolve in response to market conditions and risk factors over time.

## Deriving From Integration
The European call price $C(S_t, K, T)$ is the discounted time-$t$ expected value of $(S_T - K)^+$ under the EMM $\mathbb{Q}$ and when interest rates are constant. Hence from Equation (17) we have

$$
\begin{align}
C(S_t, K, T) &= e^{-rT} E^{\mathbb{Q}}\left[(S_T - K)^+ \mid \mathcal{F}_t\right] \tag{18}\\
&= e^{-rT} \int_K^{\infty} (S_T - K) dF(S_T) \\
&= e^{-rT} \int_K^{\infty} S_T dF(S_T) - e^{-rT} K \int_K^{\infty} dF(S_T).
\end{align}
$$
To evaluate the two integrals, we make use of the result derived in Section (3.3) that under $\mathbb{Q}$ and at time $t$ the terminal stock price $S_T$ follows the lognormal distribution with mean $\ln S_t + \left(r - \frac{\sigma^2}{2}\right)\tau$ and variance $\sigma^2\tau$, where $\tau = T - t$ is the time to maturity. The first integral in the last line of Equation (18) uses the conditional expectation of $S_T$ given that $S_T > K$

$$\int_K^{\infty} S_T dF(S_T) = E^{\mathbb{Q}}[S_T \mid S_T > K]$$
$$= L_{S_T}(K).$$

In the following sections we show four ways in which the Black-Scholes call price can be obtained. Under a constant interest rate $r$ the time-$t$ price of a European call option on a non-dividend paying stock when its spot price is $S_t$ and with strike $K$ and time to maturity $\tau = T - t$ is

$$C(S_t, K, T) = e^{-r\tau} E^{\mathbb{Q}}\left[(S_T - K)^+ \mid \mathcal{F}_t\right] \tag{17}$$

which can be evaluated to produce Equation (1), reproduced here for convenience

$$C(S_t, K, T) = S_t\Phi(d_1) - Ke^{-r\tau}\Phi(d_2)$$

where

$$d_1 = \frac{\log\frac{S_t}{K} + \left(r + \frac{\sigma^2}{2}\right)\tau}{\sigma\sqrt{\tau}}$$

and
$$
\begin{align}
d_2 &= d_1 - \sigma\sqrt{\tau}\\
&= \frac{\log\frac{S_t}{K} + \left(r - \frac{\sigma^2}{2}\right)\tau}{\sigma\sqrt{\tau}}.
\end{align}
$$

This conditional expectation is, from Equation (10)
$$
\begin{align}
L_{S_T}(K) &= \exp\left(\ln S_t + \left(r - \frac{\sigma^2}{2}\right)\tau + \frac{\sigma^2\tau}{2}\right)\\
&\quad \times\Phi\left(\frac{-\ln K + \ln S_t + \left(r - \frac{\sigma^2}{2}\right)\tau + \sigma^2\tau}{\sigma\sqrt{\tau}}\right)\\
&= S_t e^{r\tau} \Phi(d_1),
\end{align}
$$
so the first integral in the last line of Equation (18) is

$$S_t\Phi(d_1). \tag{19}$$

In the context of pricing a European Call Option, and in relation to the Black-Scholes Model (BSM), "EMM" stands for "Expected Maturity Market," which refers to the market state or conditions at maturity time T. Here's an 
expanded breakdown:

1. **The European call price C(St; K; T)**, in a Black-Scholes Model context, is calculated by discounting the 
expected payoff $$(S_T - K)$$ under certain probability distributions of future asset prices at maturity time T. This 
approach follows the risk-neutral valuation principle:
- **S_T** represents the stock price at option's expiration date T (maturity).
- **K** is the strike price—the predetermined price in the contract wherein, if $$S_T > K$$, a holder of European Call Option can buy shares from the seller for an amount equal to K.
- The discounted time-t expected value refers to calculating this payoff's present worth by taking its expectation (average over all possible future states) and then applying a risk-free rate discount factor "r" which represents the opportunity cost of capital or, more broadly, reflecting prevail points in financial markets.

2. **Expected Maturity Market (EMM Q):** This denotes the market's anticipated conditions at maturity time T, when the European Call Option will be evaluated for exercise rights. These market predictions include expected asset prices, volatility, and risk-free interest rates—all of which are taken into consideration in pricing the 
option under the Black-Scholes framework:
- **Expected Asset Prices (S_T)** at maturity represent future stock prices under different scenarios, derived from market forecasts or statistical distributions.
- **Volatility ($$\sigma$$)** refers to the degree of asset price fluctuations over a certain period and is usually an estimate based on historical data. It reflects the uncertainty surrounding the expected return of the underlying security.
- **Risk-free Interest Rates (r)** denote rates for riskless investments, such as government bonds or bank deposits in stable economic conditions. They provide a baseline to compare other risky securities' returns and are also used in discounting future cash flows.

  
- **Filtration**: The filtration $\{\mathcal{F}_t\}_{t \geq 0}$ represents the accumulation of information about market events up to time $t$. It is a mathematical structure that models how our knowledge of asset price dynamics evolves over time, incorporating new data, observable trends, and other relevant information available in the financial market.

- **Conditional Expectation**: The conditional expectation $\mathbb{E}[S_T \mid \mathcal{F}_t]$ is the best estimate (in the mean-square sense) of the future asset price $S_T$, given all information available up to time $t$, encoded in the sigma-algebra $\mathcal{F}_t$. This includes historical price paths, current market conditions, and any other observable information that may affect the asset’s future behavior.

Using Equation (7), the second integral in the last line of (18) can be written

$$
\begin{align}
e^{-r\tau} K \int_K^{\infty} dF(S_T) &= e^{-r\tau} K [1 - F(K)] \tag{20}\\
&= e^{-r\tau} K \left[1 - \Phi\left(\frac{\ln K - \ln S_t - \left(r - \frac{\sigma^2}{2}\right)\tau}{\sigma\sqrt{\tau}}\right)\right]\\
&= e^{-r\tau} K [1 - \Phi(-d_2)]\\
&= e^{-r\tau} K\Phi(d_2).
\end{align}
$$
Combining the terms in Equations (19) and (20) leads to the expression (1) for the European call price.

So, what's equation 10? We must take a detour to explore the lognormal distribution.

### The Lognormal PDF and CDF

In this Note we make extensive use of the fact that if a random variable $Y \in \mathbb{R}$ follows the normal distribution with mean $\mu$ and variance $\sigma^2$, then $X = e^Y$ follows the lognormal distribution with mean

$$E[X] = e^{\mu + \frac{1}{2}\sigma^2} \tag{4}$$

and variance

$$Var[X] = \left(e^{\sigma^2} - 1\right) e^{2\mu + \sigma^2}. \tag{5}$$

The pdf for $X$ is

$$dF_X(x) = \frac{1}{\sigma x\sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{\ln x - \mu}{\sigma}\right)^2\right) \tag{6}$$

and the cdf is

$$F_X(x) = \Phi\left(\frac{\ln x - \mu}{\sigma}\right) \tag{7}$$

where $\Phi(y) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^y e^{-\frac{1}{2}t^2} dt$ is the standard normal cdf.

### The Lognormal Conditional Expected Value

The expected value of $X$ conditional on $X > x$ is $L_X(K) = E[X | X > x]$. For the lognormal distribution this is, using Equation (6)

$$L_X(K) = \int_K^{\infty} \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{\ln x - \mu}{\sigma}\right)^2} dx.$$

Make the change of variable $y = \ln x$ so that $x = e^y$, $dx = e^y dy$ and the Jacobian is $e^y$. Hence we have

$$L_X(K) = \int_{\ln K}^{\infty} \frac{e^y}{\sigma\sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{y-\mu}{\sigma}\right)^2} dy. \tag{8}$$

Combining terms and completing the square, the exponent is

$$-\frac{1}{2\sigma^2}\left(y^2 - 2y\mu + \mu^2 - 2\sigma^2 y\right) = -\frac{1}{2\sigma^2}\left(y - \left(\mu + \sigma^2\right)\right)^2 + \mu + \frac{1}{2}\sigma^2.$$

Equation (8) becomes

$$L_X(K) = \exp\left(\mu + \frac{1}{2}\sigma^2\right) \frac{1}{\sigma} \int_{\ln K}^{\infty} \frac{1}{\sqrt{2\pi}} \exp\left(-\frac{1}{2}\left(\frac{y - \left(\mu + \sigma^2\right)}{\sigma}\right)^2\right) dy. \tag{9}$$

Consider the random variable $X$ with pdf $f_X(x)$ and cdf $F_X(x)$, and the scale-location transformation $Y = \sigma X + \mu$. It is easy to show that the Jacobian is $\frac{1}{\sigma}$, that the pdf for $Y$ is $f_Y(y) = \frac{1}{\sigma} f_X\left(\frac{y-\mu}{\sigma}\right)$ and that the cdf is $F_Y(y) = F_X\left(\frac{y-\mu}{\sigma}\right)$. Hence, the integral in Equation (9) involves the scale-location transformation of the standard normal cdf. Using the fact that $\Phi(-x) = 1 - \Phi(x)$ this implies that

$$L_X(K) = \exp\left(\mu + \frac{\sigma^2}{2}\right) \Phi\left(\frac{-\ln K + \mu + \sigma^2}{\sigma}\right). \tag{10}$$

# More stochastic calculus and fanciful maths
## Change of Numeraire

The principle behind pricing by arbitrage is that if the market is complete we can find a portfolio that replicates the derivative at all times, and we can find an equivalent martingale measure (EMM) $\mathbb{N}$ such that the discounted stock price is a martingale. Moreover, the EMM $\mathbb{N}$ determines the unique numeraire $N_t$ that discounts the stock price. The time-$t$ value $V(S_t, t)$ of the derivative with payoff $V(S_T, T)$ at time $T$ discounted by the numeraire $N_t$ is

$$V(S_t, t) = N_t E^{\mathbb{N}}\left[\frac{V(S_T, T)}{N_T} \mid \mathcal{F}_t\right]. \tag{21}$$

In the derivation of the previous section, the bond $B_t = e^{rt}$ serves as the numeraire, and since $r$ is deterministic we can take $N_T = e^{rT}$ out of the expectation and with $V(S_T, T) = (S_T - K)^+$ we can write

$$V(S_t, t) = e^{-r(T-t)} E^{\mathbb{N}}\left[(S_T - K)^+ \mid \mathcal{F}_t\right]$$

which is Equation (17) for the call price.

### Change of Numeraire
The change of numeraire is a technique in financial mathematics that helps simplify the pricing of derivatives, such as options. The numeraire is essentially the "unit of value" that we use to measure other assets. By changing this unit of measurement, we can sometimes make complicated pricing problems easier to solve.

1. What is a Numeraire?
A numeraire can be thought of as a reference asset against which all other assets are measured. In typical pricing problems, we often use a risk-free bond as the numeraire because it grows at a predictable rate, making it easier to handle in calculations. However, we can choose other assets as the numeraire, depending on the scenario.

2. Why Change the Numeraire?
In finance, different assets may behave differently under various market conditions. By switching the asset used as the numeraire, we can sometimes transform a complex pricing problem into one that's easier to calculate. This is particularly useful when pricing exotic options or handling currencies.

3. Martingale Property
A key concept in pricing derivatives is the martingale property. This means that, under the right conditions (no arbitrage opportunities), the discounted value of an asset evolves in such a way that its expected future value is equal to its current price. When we change the numeraire, we also change the "measure" (the mathematical lens) we use to view future prices, but the martingale property still holds under this new measure.

4. Using a Bond as the Numeraire
When we use a risk-free bond (which grows at the risk-free rate) as the numeraire, the pricing becomes relatively simple. For example, the price of a European call option (which pays off if the underlying asset’s price is higher than a set strike price) can be calculated by discounting the expected payoff of the option by the bond's growth rate.

5. Application to Option Pricing
In option pricing, changing the numeraire can be particularly useful. For instance, when pricing a European call option, we typically use the risk-free bond as the numeraire, leading to the familiar Black-Scholes pricing formula. This formula essentially discounts the future expected payoff of the option (based on the stock price exceeding the strike price) by the risk-free rate over time.

# Summary
In short, the change of numeraire is a method that simplifies pricing derivatives by changing the reference asset (the numeraire) used to measure value. When we do this, we switch to a new probability measure but retain certain properties, like the fact that discounted asset prices behave in a predictable way (the martingale property). For standard derivatives like European call options, using the risk-free bond as the numeraire makes the pricing straightforward and leads to well-known formulas like Black-Scholes-Merton.

\subsection{Black Scholes Under a Different Numeraire}

In this section we show that we can use the stock price $S_t$ as the numeraire and recover the Black-Scholes call price. We start with the stock price process in Equation (14) under the measure $\mathbb{Q}$ and with a constant interest rate

$$dS_t = rS_t dt + \sigma S_t dW_t^{\mathbb{Q}}. \tag{22}$$

The relative bond price price is defined as $\tilde{B} = \frac{B}{S}$ and by Itô's Lemma follows the process

$$d\tilde{B}_t = \sigma^2 \tilde{B}_t dt - \sigma \tilde{B}_t dW_t^{\mathbb{Q}}.$$

The measure $\mathbb{Q}$ turns $\tilde{S} = \frac{S}{B}$ into a martingale, but not $\tilde{B}$. The measure $\mathbb{P}$ that turns $\tilde{B}$ into a martingale is

$$W_t^{\mathbb{P}} = W_t^{\mathbb{Q}} - \sigma t \tag{23}$$

We want to find a measure $\mathbb{Q}$ such that under $\mathbb{Q}$ the discounted stock price that uses $B_t$ is a martingale. Write

$$
dS_t = r_t S_t dt + \sigma S_t dW_t^{\mathbb{Q}} \tag{14}
$$

where $W_t^{\mathbb{Q}} = W_t + \frac{\mu - r_t}{\sigma} t$. We have that under $\mathbb{Q}$, at time $t=0$, the stock price $S_t$ follows the lognormal distribution with mean $S_0 e^{r_t t}$ and variance $S_0^2 e^{2 r_t t} \left( e^{\sigma^2 t} - 1 \right)$, but that $S_t$ is not a martingale. Using $B_t$ as the numeraire, the discounted stock price is $\tilde{S}_t = \frac{S_t}{B_t}$ and $\tilde{S}_t$ will be a martingale. Apply Itô’s Lemma to $\tilde{S}_t$, which follows the SDE

$$
d\tilde{S}_t = \frac{\partial \tilde{S}}{\partial B} dB_t + \frac{\partial \tilde{S}}{\partial S} dS_t \tag{15}
$$

since all terms involving the second-order derivatives are zero. Expand Equation (15) to obtain

$$
\begin{aligned}
d\tilde{S}_t &= -\frac{S_t}{B_t^2} dB_t + \frac{1}{B_t} dS_t \tag{16} \\
&= -\frac{S_t}{B_t^2} (r_t B_t dt) + \frac{1}{B_t} \left( r_t S_t dt + \sigma S_t dW_t^{\mathbb{Q}} \right) \\
&= \sigma \tilde{S}_t dW_t^{\mathbb{Q}}.
\end{aligned}
$$

The solution to the SDE (16) is

$$
\tilde{S}_t = \tilde{S}_0 \exp\left( -\tfrac{1}{2} \sigma^2 t + \sigma W_t^{\mathbb{Q}} \right).
$$

We want to find a measure $\mathbb{Q}$ such that under $\mathbb{Q}$ the discounted stock price that uses $B_t$ is a martingale. Write

$$dS_t = r_t S_t dt + \sigma S_t dW_t^{\mathbb{Q}} \tag{14}$$

where $W_t^{\mathbb{Q}} = W_t + \frac{\mu - r_t}{\sigma}t$. We have that under $\mathbb{Q}$, at time $t = 0$, the stock price $S_t$ follows the lognormal distribution with mean $S_0 e^{r_t t}$ and variance $S_0^2 e^{2r_t t} \left(e^{\sigma^2 t} - 1\right)$, but that $S_t$ is not a martingale. Using $B_t$ as the numeraire, the discounted stock price is $\tilde{S}_t = \frac{S_t}{B_t}$ and $\tilde{S}_t$ will be a martingale. Apply Itô's Lemma to $\tilde{S}_t$, which follows the SDE

$$d\tilde{S}_t = \frac{\partial \tilde{S}}{\partial B} dB_t + \frac{\partial \tilde{S}}{\partial S} dS_t \tag{15}$$

since all terms involving the second-order derivatives are zero. Expand Equation (15) to obtain

\begin{align}
d\tilde{S}_t &= -\frac{S_t}{B_t^2} dB_t + \frac{1}{B_t} dS_t \tag{16}\\
&= -\frac{S_t}{B_t^2} (r_t B_t dt) + \frac{1}{B_t} \left(r_t S_t dt + \sigma S_t dW_t^{\mathbb{Q}}\right)\\
&= \sigma \tilde{S}_t dW_t^{\mathbb{Q}}.
\end{align}

The solution to the SDE (16) is

$$\tilde{S}_t = \tilde{S}_0 \exp\left(-\frac{1}{2}\sigma^2 t + \sigma W_t^{\mathbb{Q}}\right).$$

so that

$$d\tilde{B}_t = -\sigma \tilde{B}_t dW_t^{\mathbb{P}}$$

is a martingale under $\mathbb{P}$. The value of the European call is determined by using $N_t = S_t$ as the numeraire along with the payoff function $V(S_T, T) = (S_T - K)^+$ in the valuation Equation (21)
$$
\begin{align}
V(S_t, t) &= S_t E^{\mathbb{P}}\left[\frac{(S_T - K)^+}{S_T} \mid \mathcal{F}_t\right] \tag{24}\\
&= S_t E^{\mathbb{P}}\left[(1 - KZ_T) \mid \mathcal{F}_t\right]
\end{align}
$$
where $Z_t = \frac{1}{S_t}$. To evaluate $V(S_t, t)$ we need the distribution for $Z_T$. The process for $Z = \frac{1}{S}$ is obtained using Itô's Lemma on $S_t$ in Equation (22) and the change of measure in Equation (23)

$$
\begin{align}
dZ_t &= \left(-r + \sigma^2\right) Z_t dt - \sigma Z_t dW_t^{\mathbb{Q}}\\
&= -rZ_t dt - \sigma Z_t dW_t^{\mathbb{P}}.
\end{align}
$$

To find the solution for $Z_t$ we define $Y_t = \ln Z_t$ and apply Itô's Lemma again, to produce

$$dY_t = -\left(r + \frac{\sigma^2}{2}\right) dt - \sigma dW_t^{\mathbb{P}}. \tag{25}$$

We integrate Equation (25) to produce the solution

$$ Y_T - Y_t = -\left(r + \frac{\sigma^2}{2}\right)(T - t) - \sigma(W_T^P - W_t^P), $$

so that $Z_T$ has the solution

$$ Z_T = e^{\ln Z_t - (r + \frac{\sigma^2}{2})(T-t) - \sigma(W_T^P - W_t^P)}. $$

Now, since $W_T^P - W_t^P$ is identical in distribution to $W_\tau^P$, where $\tau = T - t$ is the time to maturity, and since $W_\tau^P$ follows the normal distribution with zero mean and variance $\sigma^2 \tau$, the exponent in Equation (26)

$$ \ln Z_t - \left(r + \frac{\sigma^2}{2}\right)(T - t) - \sigma(W_T^P - W_t^P), $$

follows the normal distribution with mean

$$ u = \ln Z_t - \left(r + \frac{\sigma^2}{2}\right) \tau = -\ln S_t - \left(r + \frac{\sigma^2}{2}\right) \tau $$

and variance $v = \sigma^2 \tau$. This implies that $Z_T$ follows the lognormal distribution with mean $e^{u + v/2}$ and variance $(e^v - 1)e^{2u + v}$. Note that $(1 - K Z_T)^+$ in the expectation of Equation (24) is non-zero when $Z_T < \frac{1}{K}$. Hence we can write this expectation as the two integrals

$$ E^P[(1 - K Z_T) | F_t] = \int_{-\infty}^k dF_{Z_T} - K \int_{-\infty}^k Z_T dF_{Z_T} $$

$$ = I_1 - I_2. $$

where $F_{Z_T}$ is the cdf of $Z_T$ defined in Equation (7). The first integral in Equation (27) is

$$ I_1 = F_{Z_T} \left( \frac{1}{K} \right) = \Phi \left( \frac{ \ln \frac{1}{K} - u }{ \sqrt{v} } \right) $$

$$ = \Phi \left( \frac{ -\ln K + \ln S_t + \left( r + \frac{\sigma^2}{2} \right) \tau }{ \sigma \sqrt{\tau} } \right) $$

$$ = \Phi(d_1). $$

Using the definition of $L_{Z_T}(x)$ in Equation (10), the second integral in Equation (27) is

$$ I_2 = K \left[ \int_{-\infty}^{\infty} Z_T \, dF_{Z_T} - \int_{\frac{1}{K}}^{\infty} Z_T \, dF_{Z_T} \right] $$

$$ = K \left[ E^{\mathbb{P}} [Z_T] - L_{Z_T} \left( \frac{1}{K} \right) \right] $$

$$ = K \left[ e^{u + v/2} - e^{u + v/2} \Phi \left( \frac{ -\ln \frac{1}{K} + u + v }{ \sqrt{v} } \right) \right] $$

$$ = K e^{u + v/2} \left[ 1 - \Phi \left( \frac{ -\ln \frac{S_t}{K} - \left( r - \frac{\sigma^2}{2} \right) \tau }{ \sigma \sqrt{\tau} } \right) \right] $$

$$ = \frac{K}{S_t} e^{-r \tau} \Phi (d_2) $$

since $1 - \Phi (-d_2) = \Phi (d_2)$. Substitute the expressions for $I_1$ and $I_2$ from Equations (28) and (29) into the valuation Equation (24)

$$ V(S_t, t) = S_t E^{\mathbb{P}} [(1 - K Z_T)^+ | \mathcal{F}_t] $$

$$ = S_t [I_1 - I_2] $$

$$ = S_t \Phi (d_1) - K e^{-r \tau} \Phi (d_2) $$

which is the Black-Scholes call price in Equation (1).

### Further reading

Excellent post on 4 ways to derive BSM
[Fabrice Douglas Rouah](https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf)

