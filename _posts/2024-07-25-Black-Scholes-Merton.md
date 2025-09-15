---
layout: post
title: "Back-of-the-Envelope: Black Scholes Merton"
date: 2024-07-24
categories: wealth 
---

# Primer 
Herein we derive the formula for pricing an option. To follow this article, you will need to know the basics of differential equations and calculus.

## A Detour to Japan
To follow this derivation, you will need to learn about the world of stochastic calculus. This field was pioneered by Japanese mathematician Kiyosi Itô, who discovered an essential result in stochastic calculus that provides the mathematical foundation for analyzing continuous-time stochastic differential equations (SDEs). 

Here are its key components:

1. **Stochastic Processes**: In finance, many quantities—such as stock prices or interest rates—are modeled as stochastic processes rather than deterministic ones due to their inherent randomness and unpredictability over time. Stochastic differential equations (SDEs) are used to describe these dynamic systems mathematically. In a stochastic system, each movement from one state to the next is governed by a probability, in our case, for the financial markets, the probability is sampled from a normal distribution. The canonical name for such a motion is a Brownian motion from physics or martingale from economics.

2. **Itô's Lemma**: Itô's lemma is a powerful tool for finding the differential of functions of stochastic processes that satisfy an SDE, particularly when applied in financial modeling and derivative pricing. In essence, Ito's lemma enables us to understand how certain observable quantities (like option prices or portfolio 
values) change over time under volatility and random market conditions.

3. Functional Derivative: At its core, the lemma provides a formula for the differential of a function composed with a stochastic process defined by an SDE. For instance, if we have a function f(t, X(t)), where t denotes time and X(t) represents a stochastic process following an SDE, Ito's Lemma tells us how df changes in relation to dt (time increment) and dX (increment of the random variable).

4. **Formula**: The formula for Itô's lemma is given by:
$$
   df(t, X(t)) = \frac{\partial f}{\partial t}dt + \frac{\partial f}{\partial x}(dX) + \frac{1}{2}\frac{\partial^2f}{\partial x^2}(dX)^2
$$
   where $$\(df\)$$ represents the differential of the function $$\(f(t, X(t))\)$$, and $$\(dX\)$$ is an infinitesimal increment in the random variable $$\(X\)$$. The first term $$\(\frac{\partial f}{\partial t}dt\)$$ captures how the function changes with time. The second term $$\(\frac{\partial f}{\partial x}(dX)\)$$ reflects its sensitivity to changes in $$\(X(t)\)$$, while the last term, a stochastic integral, accounts for random fluctuations within this process.

- **Partial Derivatives**: These represent how each component of the function responds to independent and 
dependent variables—in our case, time t (partial derivative with respect to $$\(dt\)$$) and value $$X(t)$$ (partial derivatives with respect to $$\(dX\)$$).
- **Stochastic Integral Term**: This term incorporates not only changes in the variable but also random fluctuations inherent to stochastic processes. It is a weighted average of squared increments, accounting for both small positive and negative variations within these increments.

In financial mathematics, Itô's lemma plays an instrumental role by allowing analysts and traders to derive the dynamic pricing models (like Black-Scholes formula) that govern modern derivative markets—essentially helping us understand how prices evolve in response to market conditions and risk factors over time.

# What is an option?
Is it optional to know what an option is? No! In the context of finance, an option refers to a contract that gives its owner the right, but not the obligation, to buy or sell an underlying asset e.g. shares in a company... at a predetermined price on or before a specific date. Options are used for various purposes including risk management and speculation.

## Puts & Calls: Bets Against & Bets In Favor

Two flavors of options can be thought of bets against or bets in favor of the underlying asset: puts and calls.

A **call option** allows its holder to buy the underlying security at a specified strike price within a certain timeframe. The buyer pays an upfront premium to the seller, who agrees not to sell the asset but can do so if desired. If the market value exceeds the strike price (in-the-money), the call option becomes profitable for its holder as they purchase at lower rates and could then sell it or directly profit from the difference.

A **put option** provides its buyer with the right but not the obligation to sell an underlying asset at a specified price, known as the strike or exercise price, by a certain date. The seller of the put option has committed to buy the underlier if and when the holder chooses to execute their right.

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

![bsm](/blog/assets/2024/bsm/bsm-canonical.png)
Where N is the normal distribution function.

## What are the four assumptions?

BSM requires one to make four reasonable assumptions about the market. Further exploration of the difference between the ideal world of BSM and flesh-and-blood markets is discussed in [the Volatility Smile](https://www.wiley.com/en-us/The+Volatility+Smile-p-9781118959169), a seminal book in finance. We couch discussion of the nuances of the assumptions themselves for a future post.

1. The stock price follows a geometric Brownian motion with constant volatility and drift rate. This means the 
changes in stock prices over time have an exponential distribution, exhibit continuous compounding, and that 
this process is not influenced by other factors (e.g., market events).

2. There are no dividends during the option's life period. Dividends can reduce the price of a call or increase 
the price of a put because they decrease the stock price when paid out. By excluding them, we simplify calculations.

3. Markets are efficient, meaning that asset prices reflect all available information, and investors cannot profit from trading in an arbitrage opportunity (i.e., buying undervalued securities and selling overvalued ones). 

4. The risk-free interest rate is constant throughout the option's life. This assumption simplifies calculations by assuming that there are no investment opportunities with guaranteed returns over time.

## The BSM Economy
To understand BSM, you will need to learn some stocastic calculus.
![1](/blog/assets/2024/bsm/bsm-1.png)
![2](/blog/assets/2024/bsm/bsm-2.png)

## Deriving From Integration
![Valuing a Call](/blog/assets/2024/bsm/business-1.png)
![eqn 17](/blog/assets/2024/bsm/add-17.png)
![eqn 19](/blog/assets/2024/bsm/add-19.png)

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

  
- **Filtration**: Filtration $$\(\mathcal{F}_t\)$$ symbolizes our growing knowledge about market events and information up to time t. It's a mathematical structure that models how we gain more insight into asset price dynamics as time progresses, incorporating new data or observable trends within the financial ecosystem.

- **Conditional Expectation**: The conditional expectation $$\(E[S_T | F_t]\)$$ represents our best guess (or expected value) of the future price $$\(S_T\)$$, taking into account all available information up to time t as $$(\(\mathcal{F}_t\))$$. This includes any historical data, current market conditions, and relevant assumptions or models that could influence asset prices.

![more2](/blog/assets/2024/bsm/more-2.png)
So, what's equation 10? We must take a detour to explore the lognormal distribution.
![detour](/blog/assets/2024/bsm/detour-1.png)
![detour2](/blog/assets/2024/bsm/detour-2.png)

![more3](/blog/assets/2024/bsm/more-3.png)
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
In short, the change of numeraire is a method that simplifies pricing derivatives by changing the reference asset (the numeraire) used to measure value. When we do this, we switch to a new probability measure but retain certain properties, like the fact that discounted asset prices behave in a predictable way (the martingale property). For standard derivatives like European call options, using the risk-free bond as the numeraire makes the pricing straightforward and leads to well-known formulas like Black-Scholes.
![more4](/blog/assets/2024/bsm/more-4.png)
![add14](/blog/assets/2024/bsm/add-14.png)
![more5](/blog/assets/2024/bsm/more-5.png)
![more6](/blog/assets/2024/bsm/more-6.png)
![more7](/blog/assets/2024/bsm/more-7.png)
![more8](/blog/assets/2024/bsm/more-8.png)

### Further reading

Excellent post on 4 ways to derive BSM
[Fabrice Douglas Rouah](https://www.frouah.com/finance%20notes/Black%20Scholes%20Formula.pdf)

