---
layout: post
title: "Sucker Punch Nash Equilibrium"
date: 2026-03-04
mathjax: true
---

# Introduction

For those unfamliiar, Pokémon is a turn-based simultaneous action game where players select their moves without knowing the opponent's choice. Then, after both players have made their selections, the moves are executed based on their priority and the Pokémon's speed stats in singles battles, that's just two at once.

Each Pokemon has four moves from which to select, and the outcome of the battle depends on the interactions between these moves and the attributes of the Pokémon species, "held items" that have their own effects, and battlefield properties like weather and terrain. Moves also power points (PP) that limit their usage to a fixed number of times per battle. 

# Defining the Sucker Punch 
What is "Sucker Punch"? It's a move that permits the user to strike first (+1 priority) if the opponent is about to use an attack. If the opponent is not attacking, the move fails. It has 8 PP. Now, with the mighty Kingambit dominating Generation 9 with its mighty Sucker Punch, the move has become a staple in competitive play.

<div style="display: flex; justify-content: center; align-items: center; gap: 16px;">
  <img src="https://img.pokemondb.net/artwork/large/kingambit.jpg" alt="Kingambit" width="200" />
  <span style="font-size: 2em; font-weight: bold;">VS.</span>
  <img src="https://img.pokemondb.net/artwork/large/garchomp.jpg" alt="Garchomp" width="200" />
</div>

# Nash Equilibrium 

A scenario that often arises is a Sucker Punch end-game. Keeping things simple, we can imagine a +2 Atk boosted Kingambit with 8 PP of Sucker Punch against a weakened Garchomp. Both players are down to one Pokémon, so the winner of this duel determines the fate of the game. Let's assume if Sucker Punch hits, the Garchomp will faint instantly. Likewise, the Garchomp has an attacking move that can faint the Kingambit in one hit. Now, the Kingambit could also attack directly into the Garchomp's boosting move, and win, but since it is slower, if the Garchomp player attacks outright, the Garchomp player will strike first and win.

The situation is a Nash equilibrium: if the Kingambit player chooses to use Sucker Punch, they will win if the Garchomp player chooses to attack. However, if the Garchomp player chooses to use a non-attacking move (like Swords Dance), the Kingambit player's Sucker Punch will fail, resulting in a loss of one PP for the Kingambit. 
To formalize the "Sucker Punch 50/50," we must treat it as a **finite-horizon stochastic game**. We can solve for the **Mixed Strategy Nash Equilibrium (MSNE)** by using induction on the remaining Power Points ($n$).

---

### 1. The Game Model
Let $n$ be the remaining PP of Sucker Punch. We define the game state as $G_n$. In each turn, both players move simultaneously.

* **Kingambit (K)** chooses: **Sucker Punch ($S$)** or **Direct Attack ($A$)**.
* **Garchomp (G)** chooses: **Attacking Move ($M$)** or **Swords Dance ($D$)**.

**The Rules of Engagement:**
1. If $K$ plays $S$ and $G$ plays $M$: $K$ wins ($Payoff = 1$).
2. If $K$ plays $S$ and $G$ plays $D$: $S$ fails, PP drops to $n-1$. The game moves to state $G_{n-1}$.
3. If $K$ plays $A$ and $G$ plays $D$: $K$ wins ($Payoff = 1$).
4. If $K$ plays $A$ and $G$ plays $M$: $K$ is outsped and loses ($Payoff = 0$).

---

### 2. Inductive Equilibrium Analysis
Let $V_n$ be the **Value of the Game** (Kingambit's win probability) with $n$ PP remaining.

#### Base Case: $n=1$
At 1 PP, if Sucker Punch fails ($S, D$), Kingambit has 0 PP left and loses. The payoff matrix for $G_1$ is:

| Kingambit \ Garchomp | Attack ($M$) | Swords Dance ($D$) |
| :--- | :---: | :---: |
| **Sucker Punch ($S$)** | 1 | 0 |
| **Direct Attack ($A$)** | 0 | 1 |

To find the MSNE, Kingambit plays $S$ with probability $q_1$ such that Garchomp is indifferent.
$$1(q_1) + 0(1-q_1) = 0(q_1) + 1(1-q_1) \implies q_1 = 0.5$$
Thus, **$V_1 = 0.5$**.

#### Inductive Step: $n = k$
Assume the value of the game with $k-1$ PP is $V_{k-1}$. The matrix for $G_k$ is:

| Kingambit \ Garchomp | Attack ($M$) | Swords Dance ($D$) |
| :--- | :---: | :---: |
| **Sucker Punch ($S$)** | 1 | $V_{k-1}$ |
| **Direct Attack ($A$)** | 0 | 1 |

To find the equilibrium, Kingambit chooses $S$ with probability $q_k$ to make Garchomp's expected utility for $M$ and $D$ equal:
$$1(q_k) + 0(1-q_k) = V_{k-1}(q_k) + 1(1-q_k)$$
$$q_k = V_{k-1}q_k + 1 - q_k$$
$$q_k(2 - V_{k-1}) = 1 \implies \mathbf{q_k = \frac{1}{2 - V_{k-1}}}$$

The value of the game $V_k$ is simply the expected payoff at this equilibrium:
$$V_k = q_k \cdot 1 + (1-q_k) \cdot 0 = q_k$$

---

### 3. Solving the Recurrence
We have the recursive relation $V_n = \frac{1}{2 - V_{n-1}}$ with $V_1 = \frac{1}{2}$.

* $V_1 = 1/2$
* $V_2 = \frac{1}{2 - 1/2} = 2/3$
* $V_3 = \frac{1}{2 - 2/3} = 3/4$
* **General Solution:** $V_n = \frac{n}{n+1}$

---

### 4. Final Results for $n=8$
For Kingambit with 8 PP of Sucker Punch against an optimal Garchomp:

* **Kingambit's Strategy ($q_8$):** Should use Sucker Punch with probability **$8/9$** ($\approx 88.9\%$) and Direct Attack with probability **$1/9$** ($\approx 11.1\%$).
* **Garchomp's Strategy ($p_8$):** Should Attack with probability **$1/9$** and Swords Dance with probability **$8/9$**.
* **Win Probability:** Kingambit's rigorous win probability is **$88.9\%$**.

# Conclusion
A Sucker Punch endgame is a fascinating example of a Nash equilibrium in competitive Pokémon battling. It illustrates how players must strategically balance their choices based on the potential actions of their opponent, leading to a dynamic and engaging gameplay experience. Having a uniform number generator in hand is the only way to achieve optimal play in this scenario, which is commonly incorrectly thought to be a mind game of (wait X turns... then attack outright). To the contrary, the optimal play is to randomize your choices vis-a-vis power points.