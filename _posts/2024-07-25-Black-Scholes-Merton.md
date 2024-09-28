---
layout: post
title: "Back-of-the-Envelope: Black Scholes Merton"
date: 2024-07-24
categories: wealth 
---

# What is an option?
In the context of finance, an option refers to a contract that gives its owner the right, but not the obligation, to buy or sell an underlying asset e.g. shares in a company... at a predetermined price on or before a specific date. Options are used for various purposes including risk management and speculation.

## Puts & Calls: Bets Against & Bets In Favor

Two flavors of options can be thought of bets against or bets in favor of the underlying asset: puts and calls.

A **call option** allows its holder to buy the underlying security at a specified strike price within a certain timeframe. The buyer pays an upfront premium to the seller, who agrees not to sell the asset but can do so if desired. If the market value exceeds the strike price (in-the-money), the call option becomes profitable for its holder as they purchase at lower rates and could then sell it or directly profit from the difference.

A **put option** provides its buyer with the right but not the obligation to sell an underlying asset at a specified price, known as the strike or exercise price, by a certain date. The seller of the put option has committed to buy the underlier if and when the holder chooses to execute their right.

## Europeans and Americans
Options in finance come in two types: European and American. Here's a detailed comparison between them based on 
various features:

1. **Exercise Timing**: The key difference lies in when the holder can exercise their option rights (buy or 
sell):
   - **European Options**: These can only be exercised at maturity, i.e., exactly at a specific date 
predetermined on the contract's expiration day. They do not allow exercising before this maturity date, which 
makes them simpler to price compared to American options but limits their use for certain strategies.
   - **American Options**: These can be exercised any time up until and including the option’s expiration date. 
This flexibility allows investors more control over whether or not to exercise an option based on market 
conditions, making them slightly more complex to price due to this added layer of decision-making.

2. **Pricing**: Given their differences in exercise timing, these options are priced differently using different 
mathematical models:
   - European Options: The most common pricing model used for European options is the Black-Scholes Model (BSM), 
which assumes constant volatility and risk-free interest rates over time. We delve into the BSM formula [later in the post](##How-do-we-price-one-of-these-things), so keep reading.
   - American Options: Pricing an American option generally involves numerical methods such as binomial trees, 
finite difference method or Monte Carlo simulation because of their flexibility in exercise timing. Each model 
has its own limitations and assumptions regarding the behavior of asset prices (volatility, return rates) and 
market conditions over time.

3. **Applications**: The choice between European and American options often comes down to specific investment 
strategies or needs of an investor due to their different exercise features:
   - **European Options**: These are typically used when a buyer is seeking protection (hedging) against losses 
in the underlying asset's price movements. For instance, they might be employed by companies holding large 
amounts of stock for hedging purposes or by investors who don’t need to exercise early due to specific market 
views.
   - **American Options**: Their flexible nature often suits buyers looking to speculate on future price changes 
in the underlying asset over a longer horizon, as they can choose the optimal time to exercise based on changing 
market conditions or news announcements affecting the underlier's value. However, their complexity and the need 
for advanced mathematical models make them more suitable for professional investors with deep trading expertise.

In summary, while both types of options grant a right to buy or sell an underlying asset at a predetermined 
price before maturity, European and American options vary significantly in terms of exercise timing, pricing 
methods, and their applications within investment strategies and risk management techniques.

## How do we price one of these things?



# What are the four assumptions?

1. The stock price follows a geometric Brownian motion with constant volatility and drift rate. This means the 
changes in stock prices over time have an exponential distribution, exhibit continuous compounding, and that 
this process is not influenced by other factors (e.g., market events).

2. There are no dividends during the option's life period. Dividends can reduce the price of a call or increase 
the price of a put because they decrease the stock price when paid out. By excluding them, we simplify 
calculations.

3. Markets are efficient, meaning that asset prices reflect all available information, and investors cannot 
profit from trading in an arbitrage opportunity (i.e., buying undervalued securities and selling overvalued 
ones). 

4. The risk-free interest rate is constant throughout the option's life. This assumption simplifies calculations 
by assuming that there are no investment opportunities with guaranteed returns over time.

This is how we can apply the argument that it should grow at the risk free rate, otherwise, as with our previous arguments, we would have an arbitrage opportunity.