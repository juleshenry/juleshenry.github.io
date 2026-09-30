---
layout: post
title: "Back-of-the-Envelope: Black-Scholes-Merton, Vol. I: Options, Explained"
date: 2024-07-24 12:00:00
categories: wealth
mathjax: true
---

*Black-Scholes-Merton:* **I** · [II](/blog/2024/07/24/Black-Scholes-Merton-Vol-II) · [III](/blog/2024/07/24/Black-Scholes-Merton-Vol-III)

Is it optional to know what an "option" is? No!

Many people have heard of this financial instrument but don't know how it's priced. If you can do calculus, differential equations, and remember a stats course, this series builds that price from scratch, in three volumes, taken in order.

<div class="note">
<p><strong>Roadmap</strong></p>
<ol>
<li><strong>Options, explained</strong> (this volume). Calls and puts, bought and written. European, American, and Bermudan exercise. The list of assumptions Black, Scholes, and Merton make, in plain language, before any of them is used.</li>
<li><strong><a href="/blog/2024/07/24/Black-Scholes-Merton-Vol-II">Deriving BSM from scratch</a>.</strong> A Wiener process is the noise, a martingale is a fair game. The lognormal, set against the normal. A stock built as a lognormal process, then the formula from elementary statistics and calculus: completing the square, twice.</li>
<li><strong><a href="/blog/2024/07/24/Black-Scholes-Merton-Vol-III">Nuance, and other approaches</a>.</strong> The same answer as the heat equation. The same answer as a change of numeraire, where $\Phi(d_1)$ and $\Phi(d_2)$ become ordinary probabilities. Then the assumptions, revisited: the risk-free rate, dividends, the smile.</li>
</ol>
</div>

Volumes I and II use nothing but algebra, calculus, and the Central Limit Theorem — every step is proved on the page, with one exception: Itô's lemma is motivated by Taylor's theorem and checked by hand on one path, not proved in general. Volume III uses Girsanov's theorem, motivated by finite trees and a ratio of Gaussian densities, not proved in full generality. Where an argument is a heuristic rather than a proof, it is flagged as one.

- [Puts and calls](#1-puts-and-calls)
- [European, American, Bermudan](#2-european-american-bermudan)
- [The BSM assumptions](#3-the-bsm-assumptions)
- [Where this goes](#where-this-goes)

---

# 1. Puts and calls
{: #1-puts-and-calls}

In ordinary English, optional means you do not have to. In finance that is almost the definition.

An **option** is a contract that gives its owner the *right*, and not the obligation, to buy or sell something at a pre-agreed price. The something is the **underlying** — a share of stock, a bushel of wheat. The pre-agreed price is the **strike**, written $K$. The deadline is **expiry**, written $T$. For that right you pay money up front, the **premium**. The rest of this series is the question: what must the premium be?

You already know the everyday version. A rain check that lets you buy a TV at today's price next month is a call option on the TV. If the store drops the price, you ignore the rain check and buy cheaper. If the store raises the price, you use the rain check. You will only exercise when it helps you. That one-sidedness is the whole point.

## Calls and puts

A **call** is the right to *buy* the underlying at the strike. It pays you when the underlying finishes *above* $K$. A **put** is the right to *sell* the underlying at the strike. It pays you when the underlying finishes *below* $K$.

Every contract has two sides. The **buyer** (the **holder**, **long** the option) pays the premium today and owns the right. The **seller** (the **writer**, **short** the option) *captures* that premium today and takes on the matching **obligation**. Whatever the buyer can choose to do, the writer can be forced to do. The buyer's profit is the writer's loss, dollar for dollar.

To see the cash move, fix a working premium of $10$. We do not yet know whether $10$ is the *right* price — that is the rest of the series — but we need a number to subtract. A stock trades at $100$ today. Strike $K=100$, expiry in one year.

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

The series prices the *call*. The put will fall out later from an accounting identity, not a second integral.

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

At expiry the payoff is arithmetic. The hard question is *today's* premium. Before touching it, one more property of the contract: *when* you are allowed to exercise.

---

# 2. European, American, Bermudan
{: #2-european-american-bermudan}

Everything above assumed you exercise at expiry. Contracts differ on whether you may exercise sooner. The names are geographic, and not about where the options trade.

- A **European** option may be exercised only at the single instant $T$.
- An **American** option may be exercised at any moment up to and including $T$.
- A **Bermudan** option may be exercised on a fixed list of dates — say, the first of each month — up to $T$. Bermuda sits in the Atlantic, between Europe and America. So does the contract.

In practice, options on individual US stocks are American. Options on the S&P 500 index (SPX) are European. Bermudans live mostly in interest rates: a callable bond whose issuer may redeem it on any coupon date is a bond with a Bermudan option attached.

A right you are not forced to use cannot hurt you. So, same strike, same expiry, same underlying:

$$
\text{European} \;\le\; \text{Bermudan} \;\le\; \text{American}.
$$

The interesting question is whether the inequalities are strict — whether the extra right is ever *worth* anything.

## The call: never exercise early

Take the call from above, $K=100$, one year left, and suppose the stock has already rallied to $S=130$. Exercising now pockets $30$. Should you?

Compare two portfolios. **A**: one call plus $Ke^{-r\tau}$ in the bank, where $r$ is the interest rate and $\tau=T-t$ is the time left. **B**: one share. At expiry the bank has grown to $K$. If $S_T>K$, portfolio A exercises and holds a share, like B. If $S_T\le K$, A holds $K\ge S_T$ in cash. A is worth at least as much as B in every state, so it cannot cost less today (else buy A, sell B, and pocket the difference for free):

$$
C \;\ge\; S - K e^{-r\tau} \;>\; S - K \qquad (r>0).
$$

With $r=5\%$: $C\ge 130-95.12=34.88$, which beats the $30$ from exercising. Exercising throws away two things: the interest on $K$ (you pay the strike a year early), and the insurance (if the stock falls back below $100$, the unexercised call would have let you walk away). You should *sell* the call, not exercise it.

This is **Merton's theorem**: for a call on a stock that pays no dividend, early exercise is never optimal, so the American, Bermudan, and European calls all have the same price. That is why this series may price the European call and lose nothing.

## The put: sometimes exercise early

The same argument fails for the put. Suppose the stock collapses to $S=1$, with $K=100$ and a year left. Exercising now hands you $99$ in cash today. Waiting cannot give you more than $100$, a year from now, which is worth $Ke^{-r\tau}=95.12$ today. Here waiting costs interest on a large sum, and the insurance is nearly worthless because the stock has almost nowhere left to fall. Exercise.

So the American put is *strictly* more valuable than the European one, and there is no closed-form formula for it: the holder must decide, at every instant, whether to stop. Vol. III returns to this.

## Dividends break the call argument

A dividend is cash paid to whoever holds the share. The option holder does not get it, and the share price drops by about the dividend when it is paid. If a large dividend is about to go out, exercising the call just before it — to become a shareholder in time to collect — can be optimal. Merton's theorem needs no dividends. That is one of the assumptions in the next section.

---

# 3. The BSM assumptions
{: #3-the-bsm-assumptions}

Black–Scholes–Merton is a theorem, and a theorem has hypotheses. Here they are, stated once, before any of them is used. Each is followed by what it means for the stock in your brokerage account, and whether it is true.

1. **The stock follows geometric Brownian motion.** Its percentage moves are random, continuous (no overnight gaps), and have a constant average rate $\mu$ and a constant size $\sigma$, the **volatility**. The consequence, derived in Vol. II, is that $S_T$ is lognormal. *True-ish*: daily returns are roughly bell-shaped, but crashes happen more often than a bell curve allows, and $\sigma$ drifts over time.
2. **There is a constant, known risk-free rate $r$.** You may borrow or lend any amount at $r$, and the same $r$ applies both ways. *Approximately*: Treasury bills set $r$, but you borrow at more than you lend, and rates change.
3. **The stock pays no dividends** during the life of the option. *Often false*, and easy to repair — Vol. III.
4. **The option is European.** For a call, §2 showed this costs nothing when assumption 3 holds.
5. **Frictionless trading.** No commissions, no bid–ask spread, no taxes. You may trade continuously, in any fraction of a share, and short-sell freely with full use of the proceeds. *False*, but small for large traders in liquid stocks.
6. **No arbitrage.** There is no portfolio that costs nothing, can never lose money, and sometimes makes money. This is the engine: every price in the series is pinned by showing that any other price hands someone a free lunch, as the call's lower bound in §2 did.
7. **The market is complete.** One source of randomness drives the stock, and there are two assets to trade (the stock and the bank). With as many assets as sources of noise plus one, any payoff can be manufactured by trading — and then its price is the cost of manufacturing it.

What is *not* on the list is just as important. There is no assumption about $\mu$: the formula will not care whether you think the stock is going up. There is no assumption about anyone's appetite for risk. These two omissions are the surprise of the derivation.

<table>
  <thead>
    <tr>
      <th>Assumption</th>
      <th>Used in</th>
      <th>Revisited in</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>GBM, constant \(\sigma\)</td><td>Vol. II §3: \(S_T\) is lognormal</td><td>Vol. III §3: the smile, jumps, stochastic vol</td></tr>
    <tr><td>constant \(r\)</td><td>Vol. II §3: discounting, replacing \(\mu\) by \(r\)</td><td>Vol. III §3: time-varying and random rates</td></tr>
    <tr><td>no dividends</td><td>Vol. II §3: drift is \(r\) under the pricing law</td><td>Vol. III §3: yield \(q\), discrete dividends</td></tr>
    <tr><td>European</td><td>Vol. II §3: payoff depends on \(S_T\) only</td><td>Vol. III §3: American puts, trees</td></tr>
    <tr><td>frictionless, no arbitrage, complete</td><td>Vol. II §3: the two-leaf tree; Vol. III §1: the hedge</td><td>Vol. III §3: jumps make the market incomplete</td></tr>
  </tbody>
</table>

---

# Where this goes
{: #where-this-goes}

We know what a call pays at expiry, why we may price the European one, and what is assumed about the world. What we do not know is how $S$ wanders between now and $T$. That needs a model of pure noise, a definition of a fair game, and a distribution that stays positive. Those are the first three stops in Vol. II, and the formula is the fourth.

---

**Next:** [Vol. II: Deriving BSM from Scratch](/blog/2024/07/24/Black-Scholes-Merton-Vol-II)

*Black-Scholes-Merton:* **Vol. I** · [Vol. II](/blog/2024/07/24/Black-Scholes-Merton-Vol-II) · [Vol. III](/blog/2024/07/24/Black-Scholes-Merton-Vol-III)
