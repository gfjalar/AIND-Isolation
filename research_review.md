# [*Mastering the game of Go with deep neural networks and tree search*](https://storage.googleapis.com/deepmind-media/alphago/AlphaGoNaturePaper.pdf) summary

The paper describes the development of a deep neural networks and tree search based Go playing program.

## Goals

The goal of the program is to effectively select moves and evaluate positions in one of the most challenging of classical games for AI, Go.

## Techniques

The described program uses deep convolutional neural networks of 19 × 19 images as the representation of the position on a Go board. The training consists of training supervised learning policy network. Then, a reinforcement learning policy network is trained. Finally, a value network is trained. Aforementioned is combined with Monte-Carlo Tree Search to provide an efficient and proficient Go player.

### Supervised learning of policy networks

Supervised policy is performed on the dataset of expert moves. For the AlphaGo player, the supervised learning of policy networks was performed on 30 million Go board positions collected from the KGS Go Server.

## Reinforcement learning of policy networks

Reinforcement learning of policy networks is performed between the current iteration of the policy network and a randomly chosen, historical one in order to prevent overfitting.

## Reinforcement learning of value networks

The use of value networks asserts that a single best move is selected rather than a presentation of distribution of probabilities. For reinforcement learning of value networks, a dataset of 30 million of distinct positions was prepared and fed to plays between Reinforcement Learning Policy Network and the current iteration of Reinforcement Learning of Value Networks.

## Searching with policy and value networks

AlphaGo uses Monte-Carlo Tree Search algorithm with policy and value networks in order to find the next best move. Leaf nodes are evaluated both by the value network, as well as a random play until the termination using a specific policy.

Evaluation preferred by AlphaGo requires immense computational power, hence it is the most effective when run asynchronously in a multi-threaded environment. Additionally, while search is being processed on the CPUs, the GPUs can take care of computing the policy and value networks.

## Results

The described AlphaGo program outperforms any existing Go playing programs, as well as humans.

### Supervised learning of policy networks

13-layer supervised policy network described in the paper predicted expert moves on a test set with 57.0% accuracy which beats the previous state of the art techniques by 12.6pp.

## Reinforcement learning of policy networks

Reinforcement learning policy networks described in the paper beats the supervised learning one in 80% of the cases. When tested agains the strongest open-source Go player out there, Pachi, it won 85% of the games.

## Evaluating the playing strength of AlphaGo

AlphaGo was tested in a tournament against such computer players as Crazy Stone, Zen, Pachi and Fuego. During the tournament AlphaGo won 99.8% of its games.

The AlphaGo player was also tested against a professional 2 dan Go player, Fan Hui. It won the formal Go match against him 5 games to 0 with no handicap.
