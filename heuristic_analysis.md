# Heuristic Analysis

## Hardware Setup

Heuristic analysis was performed on a machine with `1.3 GHz Intel Core i5` processor and `4 GB 1600 MHz DDR3` of RAM.

## Performance Testing

All the tests were performed with `300ms` time limit threshold and `50ms` timeout for Alpha-Beta Players.

| Opponent \ Player | AB_Improved | AB_Custom | AB_Open_Diff | AB_Bounding_Box | AB_Proximity |
| :--- | :---: | :---: | :---: | :---: | :---: |
| | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** | **Won : Lost** |
| Random | 9 : 1 | 10 : 0 | 8 : 2 | 9 : 1 | 10 : 0 |     
| MM_Open | 7 : 3 | 7 : 3 | 9 : 1 | 9 : 1 | 8 : 2 |     
| MM_Center | 8 : 2 | 7 : 3 | 9 : 1 | 9 : 1 | 8 : 2 |     
| MM_Improved | 7 : 3 | 8 : 2 | 8 : 2 | 7 : 3 | 6 : 4 |     
| AB_Open | 4 : 6 | 6 : 4 | 5 : 5 | 6 : 4 | 5 : 5 |     
| AB_Center | 5 : 5 | 8 : 2 | 7 : 3 | 6 : 4 | 9 : 1 |     
| AB_Improved | 0 : 0 | 6 : 4 | 5 : 5 | 5 : 5 | 5 : 5 |     
| AB_Custom | 6 : 4 | 0 : 0 | 7 : 3 | 5 : 5 | 6 : 4 |     
| AB_Open_Diff | 5 : 5 | 4 : 6 | 0 : 0 | 5 : 5 | 3 : 7 |     
| AB_Bounding_Box | 5 : 5 | 5 : 5 | 5 : 5 | 0 : 0 | 6 : 4 |     
| AB_Proximity | 5 : 5 | 4 : 6 | 5 : 5 | 6 : 4 | 0 : 0 |
| | | | | | |
| **Win Rate** | 61.0% | 65.0% | 68.0% | 67.0% | 66.0% |

## One-by-one Analysis

0. Open Moves Multiplied Difference Heuristic(*AB_Open_Diff*)

  The heuristic measures the difference between the number of player's open moves and the number of opponent's open moves. Additionaly, it multiplies the number of opponent's open move by the multiplier value, `1.62`(the golden ratio). The effect of such multiplication is that the player is more likely to choose the moves that decreases the number of moves the opponent is able to make.

  The heuristic achieved `68%` of win rate during the testing round which is the best result. What's worth noting is that the heuristic is extremely easy to compute.

0. Bounding Box Blank Spaces Difference Heuristic(*AB_Bounding_Box*)

  The heurestic measures the difference between the number of blank spaces within the player's bounding box(*the smallest rectangular area projected on board that contains all the open moves as well as the player's location*) and the number of blank spaces within the opponent's bounding box.

  The heuristic scored `67%` of wins during the testing round. An interesting thing about this heuristic is that it successfully captures how *free* the player's surrounding is.

0. Blank Spaces Proximity Difference Heuristic(*AB_Proximity*)

  The heuristic measures the difference between the number of blank spaces that are closer to the player and the number of blank spaces that are closer to the opponent. It discards the number of blank spaces that are equally as close to the player and the opponent. It tries to capture how much of the board is *controlled* by the player.

  During the testing round, it achieved `66%` win rate which is the third result among the tested heuristics.

0. Combined Heuristic(*AB_Custom*)

  The heuristic is a combination of `Open Moves Multiplied Difference`, `Bounding Box Blank Spaces Difference`, `Blank Spaces Proximity` heuristics. It uses `Open Moves Multiplied Difference` heuristic at the very early stages of the game, until 33% of the board is filled. Therefore, at the very beginning of the game, the player tries to increase the number of open moves it has while proactively chasing the opponent. Then, until the 66% of the board is filled, `Bounding Box Blank Spaces Difference` heuristic is used. At this stage, there still might not be a clear separation on the board. Thus, the player will try to increase the number of free spaces around self while decreasing the same value for the opponent. At the end of the game, the player will start using `Blank Spaces Proximity` heuristic. The *difference* part of it is ditched for the ease of computation. Thus, the player will only try to increase the number of spaces it controls.

  The `Combined` heuristic comes in fourth in the set of the tested heuristics with `65%` win rate.

## Summary

The proposed heuristics perform on par with the `Improved` heuristic. Given the table of results, I would recommend using the `Open Moves Multiplied Difference` heuristic as it achieved the best score among the tested heuristics, it is the easiest one to compute among the proposed heuristics, equally as easy to implement and understand.

Furthermore, I would suggest trying to improve on the `Combined` heuristic as customising the player's behaviour according to the current situation on the board(eg. how filled the board is) has real potential as the proposed version already hints.
