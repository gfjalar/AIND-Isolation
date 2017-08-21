# Heuristic Analysis

## Hardware Setup

Heuristic analysis was performed on a machine with `1.3 GHz Intel Core i5` processor and `4 GB 1600 MHz DDR3` of RAM.

## Performance Testing

All the tests were performed with `300ms` time limit threshold and `50ms` timeout for Alpha-Beta Players.

| Opponent \ Player | AB_Improved | AB_Custom | AB_Center_Diff | AB_Opponent | AB_Intersection | AB_Spread | AB_Spread_Diff | AB_Spread_Intersection |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** |
| Random | 89 : 11 | 95 : 5 | 90 : 10 | 92 : 8 | 86 : 14 | 92 : 8 | 92 : 8 | 92 : 8 |
| MM_Open | 76 : 24 | 73 : 27 | 68 : 32 | 76 : 24 | 65 : 35 | 73 : 27 | 74 : 26 | 74 : 26 |
| MM_Center | 93 : 7 | 93 : 7 | 91 : 9 | 82 : 18 | 83 : 17 | 86 : 14 | 83 : 17 | 82 : 18 |
| MM_Improved | 79 : 21 | 74 : 26 | 68 : 32 | 68 : 32 | 59 : 41 | 68 : 32 | 69 : 31 | 73 : 27 |
| AB_Open | 51 : 49 | 50 : 50 | 51 : 49 | 52 : 48 | 45 : 55 | 48 : 52 | 42 : 58 | 46 : 54 |
| AB_Center | 53 : 47 | 58 : 42 | 49 : 51 | 54 : 46 | 45 : 55 | 56 : 44 | 54 : 46 | 50 : 50 |
| AB_Improved | 0 : 0 | 48 : 52 | 36 : 64 | 49 : 51 | 44 : 56 | 47 : 53 | 50 : 50 | 47 : 53 |
| AB_Custom | 55 : 45 | 0 : 0 | 44 : 56 | 43 : 57 | 41 : 59 | 55 : 45 | 47 : 53 | 49 : 51 |
| AB_Center_Diff | 63 : 37 | 52 : 48 | 0 : 0 | 54 : 46 | 42 : 58 | 53 : 47 | 49 : 51 | 47 : 53 |
| AB_Opponent | 52 : 48 | 53 : 47 | 49 : 51 | 0 : 0 | 50 : 50 | 54 : 46 | 56 : 44 | 46 : 54 |
| AB_Intersection | 56 : 44 | 49 : 51 | 51 : 49 | 60 : 40 | 0 : 0 | 55 : 45 | 61 : 39 | 54 : 46 |
| AB_Spread | 51 : 49 | 46 : 54 | 46 : 54 | 53 : 47 | 45 : 55 | 0 : 0 | 51 : 49 | 47 : 53 |
| AB_Spread_Diff | 48 : 52 | 52 : 48 | 48 : 52 | 49 : 51 | 42 : 58 | 55 : 45 | 0 : 0 | 46 : 54 |
| AB_Spread_Intersection | 55 : 45 | 45 : 55 | 40 : 60 | 49 : 51 | 43 : 57 | 54 : 46 | 48 : 52 | 0 : 0 |
| | | | | | | | | |
| **Win Rate** | 63.2% | 60.6% | 56.2% | 60.1% | 53.1% | 61.2% | 59.7% | 57.9% |

## One-by-one Analysis

0. Center Distance Difference Heuristic(*AB_Center_Diff*)

  The heuristic measures the difference between the distance between the player's location and the center of the board and the opponent's location and the center of the board. It assumes the closer to the center the player is, the better. It additionally incorporates an assumption that the further from the center the opponent is, the better.

  The heuristic achieved 56.2% of win rate during the testing round which is one of the worst results in the set. It only slightly outperform the `Open Moves Intersection` heuristic.

0. Opponent Distance Heuristic(*AB_Opponent*)

  The heuristic measures the distance between the player's location and the opponent's location. It assumes that the further away the players are, the better. Another variant of this heuristic could be to assume the closer the players are, the better.

  The heuristic is one of the best in the tested set and achieved 60.1% win rate. What's worth noting is that it performs especially well agains the `Open Moves Intersection` heuristic.

0. Open Moves Intersection Heuristic(*AB_Intersection*)

  The heuristic measures the number of open moves that are present both in the player's open moves set and the opponent's open moves set at the same time. It assumes that the existence of *blocking* moves in such intersection signals a better state. A variant of this heuristic could give more value to a state where only one *blocking* move would be present in such intersection.

  The heuristic is by far the worst one from the tested set with 53.1% win rate. It has not achieved the majority of wins against any of the Alpha-Beta Opponents.

0. Open Moves Spread Heuristic(*AB_Spread*)

  Firstly, let's define spread as a rectangle area covering all the player's open moves on the board. The heuristic measures the area of such a rectangle for the player. It is similar to the open moves heuristic. However, it additionally values the directions in which the moves can be made. For example, a state where a player can move up and right or up and left would be worse by the meaning of the heuristic than a state where a player can move up and right and down and left.

  The `Open Moves Spread` heuristic is the performs the best out of the tested heuristic. It achieved 61.2% win rate which is only 2pp. short of the `Improved` heuristic. What's worth noting is that it lost the majority of the games to the Alpha-Beta Opponent using `Open Moves` heuristic.

0. Open Moves Spread Difference Heuristic(*AB_Spread_Diff*)

  The heuristic measures the difference of the areas of the spreads(*defined in AB_Spread section*) for the player and the opponent. It follows that the bigger the area of the spread, the better. Additionally, it tries to minimize the opponent's spread area.

  The heuristic achieved 59.7% win rate. It performed especially well against the `Open Moves Intersection` heuristic.

0. Open Moves Spread Intersection Heuristic(*AB_Spread_Intersection*)

  The heuristic measures the area of the intersection of the spreads(*defined in AB_Spread section*) for the player and the opponent. It assumes that the bigger the intersection between spreads is, the greater chance of blocking the opponent there is.

  The win rate for the heuristic is 57.9% which is not an impressive score at all.

0. Combined Heuristic(*AB_Custom*)

  The heuristic is a combination of `Open Moves Intersection`, `Opponent Distance`, `Open Moves Spread Difference`, `Open Moves Spread` heuristics. It uses `Open Moves Intersection` heuristic at the very early stages of the game, until 20% of the board is filled. In other words, at the very beginning of the game it tries to create a situation where the `player` has as many *blocking* moves as possible. A little later in the game, until 40% of the board is filled, it uses `Opponent Distance` heuristic. This means that at this point of the game, the player will be trying to follow the opponent. While getting closer to the end of the game, up until 70% of the board is filled, the heuristic changes to `Open Moves Spread Difference`. At this point in the game, the player will be trying to maximise the spread it can create while at the same time trying to reduce the opponent's spread. After 70% of the board is filled, it is very likely that there exists a partition of the board. That means that the player is likely not to have any effect on the opponent's spread anymore. Thus, it starts using the `Open Moves Spread` heuristic which is slightly less computationally demanding.

  The `Combined` heuristic comes in third in the set of the tested heuristics with 60.6% win rate.

## Summary

The proposed heuristic perform on par with the `Improved` heuristic. However, none of them outperform it. The heuristic that comes the closest to beating the `Improved` heuristic is the `Open Moves Spread` heuristic. I suggest further exploration of the impact each of the heuristic has on the game with distinction made as to at which point of the game it is being used.

A proposed improvement to the `Combined` heuristic could be a different composition of its components or an incorporation of the weighting factors into each of the heuristics it's using. For example it could be returing values like `0.2 * normalize(Opponent_Distance) + 0.8 * normalize(Center_Distance_Difference)`. Such weighting could be beneficial for the results. However, it would increase the computational complexity and would require fine-grained testing to find the perfect combination which is out of scope of this analysis.
