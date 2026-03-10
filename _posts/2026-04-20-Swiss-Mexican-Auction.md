---
layout: post
title: "Swiss-Mexican Auction"
date: 2026-04-20
mathjax: true
---

# [The Swiss-Mexican Auction: Solving Budget-Constrained Combinatorial Auctions at Scale](https://github.com/juleshenry/swiss-mexican-auction)

What if eBay let you bid on bundles?

You want a camera body, a specific lens, and a tripod -- but only if you can get all three. Buying the lens without the body is useless. Buying the body without the lens is expensive paperweight acquisition. You want the bundle, all or nothing.

This is the **exposure problem** in auction theory, and solving it optimally is NP-complete. The Swiss-Mexican Auction is a dual-layer framework that says: forget optimality. Get close enough, fast enough, at the scale of a real marketplace.

The project is on [GitHub](https://github.com/juleshenry/swiss-mexican-auction).

## The Problem: Satisfiability and Expenditure

Call it the SEP: Satisfiability and Expenditure Problem. You have a marketplace with $N$ items and $M$ bidders. Each bidder $i$ wants a specific bundle $O_i \subseteq \{1, ..., N\}$ (all or nothing) and has a hard budget ceiling $B_i$. The auctioneer wants to maximize total revenue while respecting three constraints:

1. **Budget**: No bidder pays more than $B_i$
2. **Indivisibility**: Either bidder $i$ gets the entire bundle $O_i$ or nothing
3. **Exclusivity**: Each item can be allocated to at most one bidder

This is simultaneously a Set Packing problem (maximize the number of non-overlapping bundles) and a Multi-Dimensional Knapsack problem (maximize revenue subject to capacity constraints). Both are NP-hard individually. Combined, the ILP formulation is:

$$\max \sum_{i=1}^{M} B_i \cdot x_i$$

subject to:

$$\sum_{i: j \in O_i} x_i \leq 1 \quad \forall j \in \{1, ..., N\}$$

$$x_i \in \{0, 1\} \quad \forall i$$

At eBay's scale -- 1.7 billion items, 134 million buyers -- exact ILP solutions are computationally impossible. The Swiss-Mexican Auction does not even try.

## The Two Layers

### The Swiss Layer (Constraints)

The "Swiss" layer is the rigid, formal mathematical scaffolding. It defines the ILP, establishes the feasibility space, and provides theoretical upper bounds via LP relaxation (relax $x_i \in \{0,1\}$ to $x_i \in [0,1]$ and solve the continuous problem with a linear solver). The LP relaxation gives you a ceiling: "no feasible allocation can exceed this revenue." You cannot achieve it, but you can measure how close your heuristic gets.

### The Mexican Layer (Execution)

The "Mexican" layer is the heuristic. Fast, fluid, good enough. The algorithm:

1. Compute each bidder's **value density**: $\rho_i = B_i / |O_i|$ (budget per item in the bundle)
2. Sort all bidders by $\rho_i$ in descending order
3. Iterate: for each bidder, check if all items in their bundle $O_i$ are still available. If yes, allocate. If any item is taken, skip.

That is it. $O(N \log N)$ time (dominated by the sort). The greedy heuristic favors bidders who pay the most per item -- the efficient bidders -- and allocates first-come-first-served among non-conflicting bundles.

## Results: 50,000 Items, 20,000 Bidders, 0.26 Seconds

The simulation generates a realistic marketplace:
- 50,000 items with log-normal price distributions
- 20,000 bidders with bundle sizes ranging from 1 to 15 items
- Budgets drawn from a distribution centered around the sum of desired item prices (with noise)

The greedy algorithm clears this market in **0.26 seconds**. It satisfies 36% of bidders (7,200 out of 20,000) with zero item conflicts, zero budget violations, and extracts ~$945,000 in revenue.

### The LP-Guided Hybrid

The "Swiss Fallback" improves on pure greedy. It solves the LP relaxation first (using SciPy's HiGHS solver), extracts the fractional solution weights, and uses them to re-rank bidders before running the greedy pass. Bidders that the LP heavily weights get priority in the greedy allocation.

On a smaller test market (500 items, 1,000 bidders), the hybrid closes **92.8%** of the gap between pure greedy and the theoretical LP upper bound, achieving an 8.8% revenue improvement. The LP solve adds computational cost, but for markets where the revenue stakes justify it, the hybrid is the clear winner.

## Two Emergent Phenomena

### The Anti-Whale Effect

The greedy algorithm naturally favors small, targeted bidders over large-bundle "whales." A bidder wanting 2 items with a $500 budget has $\rho = 250$ per item. A bidder wanting 15 items with a $2,000 budget has $\rho = 133$ per item. The small bidder ranks higher. By the time we reach the whale, several of their desired items are already allocated to smaller bidders, and the whale is skipped.

This produces a more **democratic** marketplace. The algorithm does not discriminate by total wealth -- it discriminates by efficiency. A buyer willing to pay a premium for a small, specific bundle is prioritized over a deep-pocketed buyer making a speculative grab at a large bundle. This is not a designed feature. It is an emergent property of sorting by value density.

### The Tequila-Snow Phase Transition

Market liquidity collapses non-linearly as desired bundle sizes grow. This is the "Tequila-Snow" phase transition, named by analogy to statistical mechanics.

When average bundle size is 1-2 items, the market is **liquid** -- most bidders can be satisfied because their bundles rarely conflict. When average bundle size exceeds 8-10 items, the market **freezes** -- almost no one gets their bundle because the probability of at least one item conflict approaches 1.

The critical insight: there is a **Viscous Goldilocks Zone** around bundle size 3-4 where the product of satisfaction rate and revenue per bidder is maximized. Smaller bundles have high satisfaction but low per-bidder revenue. Larger bundles have high per-bidder revenue but near-zero satisfaction. The sweet spot is in the middle. This has practical implications for marketplace design: if you are building an auction platform that supports bundling, you should nudge bidders toward bundles of 3-4 items for maximum overall market efficiency.

```mermaid
xychart-beta
    title "Tequila-Snow Phase Transition"
    x-axis "Average Bundle Size" [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
    y-axis "Satisfaction Rate (%)" 0 --> 100
    line [95, 72, 54, 41, 31, 24, 18, 14, 11, 8, 2]
```

## Future Horizons

The paper sketches several extensions:

**Quantum Annealing.** The ILP can be reformulated as a QUBO (Quadratic Unconstrained Binary Optimization) problem, which maps naturally onto an Ising model. D-Wave's quantum annealers natively solve QUBO problems. For a 50,000-item market, the Ising model would have 20,000 qubits (one per bidder) with pairwise couplings encoding item conflicts. Current quantum hardware cannot handle this scale, but the formulation is ready for when it can.

**Neural Mechanism Design.** Train a Graph Neural Network on the conflict graph (bidders as nodes, item conflicts as edges) to learn allocation strategies that generalize across market structures. The GNN could learn market-type-specific heuristics that outperform the generic value-density sort.

**Zero-Knowledge Proofs.** Bidders currently reveal their budgets to the auctioneer. With zk-SNARKs, bidders could prove "my budget exceeds the price of my bundle" without revealing the actual budget. Cryptographic privacy for auction participants.

The Swiss-Mexican Auction is not optimal. By construction, it cannot be -- the optimal solution is NP-complete. But it is fast, it is principled, it closes 93% of the optimality gap, and it clears a 50,000-item market in a quarter of a second. Sometimes good enough, fast enough, is the right answer.
