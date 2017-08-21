"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def euclidean_distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bounding_box(ns):
    if len(ns) == 0:
        return ((-1, -1), (-1, -1))
    (rows, columns) = zip(*ns)
    return ((min(rows), min(columns)), (max(rows), max(columns)))


def box_area(a):
    ((min_row, min_column), (max_row, max_column)) = a
    return (max_row - min_row + 1.) * (max_column - min_column + 1.)


def intersection_box(a, b):
    ((min_row_a, min_column_a), (max_row_a, max_column_a)) = a
    ((min_row_b, min_column_b), (max_row_b, max_column_b)) = b
    return ((max(min_row_a, min_row_b), max(min_column_a, min_column_b)), (min(max_row_a, max_row_b), min(max_column_a, max_column_b)))


def center_score(game, player):
    opp = game.get_opponent(player)

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(opp)

    center_location = (game.height / 2., game.width / 2.)

    own_distance = manhattan_distance(own_location, center_location)
    opp_distance = manhattan_distance(opp_location, center_location)

    return float(own_distance - opp_distance)


def opponent_score(game, player):
    opp = game.get_opponent(player)

    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(opp)

    center_location = (game.height / 2., game.width / 2.)

    distance = manhattan_distance(own_location, opp_location)

    return float(distance)


def intersection_score(game, player):
    opp = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opp)

    moves_intersection = set(own_moves) & set(opp_moves)

    return float(len(moves_intersection))


def spread_score(game, player):
    own_moves = game.get_legal_moves(player)

    own_box = bounding_box(own_moves)

    return box_area(own_box)


def spread_difference_score(game, player):
    opp = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opp)

    own_box = bounding_box(own_moves)
    opp_box = bounding_box(opp_moves)

    return box_area(own_box) - box_area(opp_box)


def spread_intersection_score(game, player):
    opp = game.get_opponent(player)

    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(opp)

    own_box = bounding_box(own_moves)
    opp_box = bounding_box(opp_moves)

    return box_area(intersection_box(own_box, opp_box))


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    p = len(game.get_blank_spaces()) / (game.height * game.width)

    if p <= 0.2:
        return intersection_score(game, player)
    elif p <= 0.4:
        return opponent_score(game, player)
    elif p <= 0.7:
        return spread_difference_score(game, player)
    else:
        return spread_score(game, player)


def custom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return center_score(game, player)


def custom_score_3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return opponent_score(game, player)


def custom_score_4(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return intersection_score(game, player)


def custom_score_5(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return spread_score(game, player)


def custom_score_6(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return spread_difference_score(game, player)


def custom_score_7(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return spread_intersection_score(game, player)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        self.NONE = (-1, -1)


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = self.NONE

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.NONE

        if not depth:
            return random.choice(legal_moves)

        forecast_lambda = lambda m: self.minimax_score(game.forecast_move(m), depth - 1)

        if self is game.active_player:
            return max(legal_moves, key = forecast_lambda)
        if self is game.inactive_player:
            return min(legal_moves, key = forecast_lambda)

    def minimax_score(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if not depth:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        forecast_scores = [self.minimax_score(game.forecast_move(m), depth - 1) for m in legal_moves]

        if self is game.active_player:
            return max(forecast_scores)
        if self is game.inactive_player:
            return min(forecast_scores)


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        best_move = self.NONE
        try:
            search_depth = self.search_depth
            while True:
                best_move = self.alphabeta(game, search_depth)
                search_depth = search_depth + 1

        except SearchTimeout:
            pass

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return self.NONE

        if not depth:
            return random.choice(legal_moves)

        if self is game.active_player:
            score = float("-inf")
        if self is game.inactive_player:
            score = float("inf")

        move = random.choice(legal_moves)

        for m in legal_moves:
            s = self.alphabeta_score(game.forecast_move(m), depth - 1, alpha, beta)
            if self is game.active_player and s > score:
                score = s
                move = m
                if score >= beta:
                    return move
                alpha = max(alpha, score)
            if self is game.inactive_player and s < score:
                score = s
                move = m
                if score <= alpha:
                    return move
                beta = min(beta, score)

        return move

    def alphabeta_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if not depth:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return game.utility(self)

        if self is game.active_player:
            score = float("-inf")
        if self is game.inactive_player:
            score = float("inf")

        for m in legal_moves:
            s = self.alphabeta_score(game.forecast_move(m), depth - 1, alpha, beta)
            if self is game.active_player and s > score:
                score = s
                if score >= beta:
                    return score
                alpha = max(alpha, score)
            if self is game.inactive_player and s < score:
                score = s
                if score <= alpha:
                    return score
                beta = min(beta, score)

        return score
