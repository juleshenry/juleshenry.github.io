---
layout: post
title: "Sucker Punch Nash Equilibrium"
date: 2026-03-04
---

# Introduction

For those unfamliiar, Pokémon is a turn-based simultaneous action game where players select their moves without knowing the opponent's choice. Then, after both players have made their selections, the moves are executed based on their priority and the Pokémon's speed stats in singles battles, that's just two at once.

Each Pokemon has four moves from which to select, and the outcome of the battle depends on the interactions between these moves and the attributes of the Pokémon species, "held items" that have their own effects, and battlefield properties like weather and terrain. Moves also power points (PP) that limit their usage to a fixed number of times per battle. 

# Defining the Sucker Punch 
What is "Sucker Punch"? It's a move that permits the user to strike first (+1 priority) if the opponent is about to use an attack. If the opponent is not attacking, the move fails. It has 8 PP. Now, with the mighty Kingambit dominating Generation 9 with its mighty Sucker Punch, the move has become a staple in competitive play.

# Nash Equilibrium 

A scenario that often arises is a Sucker Punch end-game. Keeping things simple, we can imagine a +2 Atk boosted Kingambit with 8 PP of Sucker Punch against a weakened Garchomp. Both players are down to one Pokémon, so the winner of this duel determines the fate of the game. Let's assume if Sucker Punch hits, the Garchomp will faint instantly. Likewise, the Garchomp has an attacking move that can faint the Kingambit in one hit. Now, the Kingambit could also attack directly into the Garchomp's boosting move, and win, but since it is slower, if the Garchomp player attacks outright, the Garchomp player will strike first and win.

The situation is a Nash equilibrium: if the Kingambit player chooses to use Sucker Punch, they will win if the Garchomp player chooses to attack. However, if the Garchomp player chooses to use a non-attacking move (like Swords Dance), the Kingambit player's Sucker Punch will fail, resulting in a loss of one PP for the Kingambit. 

The optimal play, therefore can be calculated via induction. Imagine Kingambit has Sucker Punch PP of 1. If the Garchomp player chooses to attack, Kingambit wins. If the Garchomp player chooses to Swords Dance,, Kingambit loses. Therefore, the Garchomp player could choose to Swords Dance, leading to a loss of PP for Kingambit and exhaust its ability to strike first. Conversely, the Kingambit could outright attack, which would win if the Garchomp player chooses to Swords Dance. It is clear to see this is a classic "rock-paper-scissors" scenario, where the optimal play depends on the opponent's choice, and there is no dominant strategy for either player, resulting in 50% Sucker Punch and 50% direct attack for the Kingambit player, and 50% attack and 50% Swords Dance for the Garchomp player.

Now, for 2 PP of Sucker Punch, we begin induction by noticing that 66% of the time, the Garchomp player will choose to Swords Dance, and 33% of the time, they will choose to attack. Therefore, the Kingambit player should choose to Sucker Punch 66% of the time and attack 33% of the time. Finally, we can deduce that up to 8 PP, the mixed Nash equilibrium is 7/8 chance Sucker Punch and 1/8 direct attack for the Kingambit player, and the inverse for the Garchomp player.

# Conclusion
A Sucker Punch endgame is a fascinating example of a Nash equilibrium in competitive Pokémon battling. It illustrates how players must strategically balance their choices based on the potential actions of their opponent, leading to a dynamic and engaging gameplay experience. Having a uniform number generator in hand is the only way to achieve optimal play in this scenario, which is commonly incorrectly thought to be a mind game of (wait X turns... then attack outright). To the contrary, the optimal play is to randomize your choices according to the game theoretical optimal play at each moment.