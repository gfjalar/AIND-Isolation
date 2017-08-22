"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def bounding_box(spaces):
    (rows, columns) = zip(*spaces)
    return ((min(rows), min(columns)), (max(rows), max(columns)))


def box_spaces(box):
    ((min_row, min_column), (max_row, max_column)) = box
    return [(row, column) for row in range(min_row, max_row + 1) for column in range(min_column, max_column + 1)]


def open_moves_score(game, player, multiplier = 1.0):
    return multiplier * len(game.get_legal_moves(player))


def bounding_box_blank_spaces_score(game, player, multiplier = 1.0):
    location = game.get_player_location(player)
    moves = game.get_legal_moves(player)

    spaces = box_spaces(bounding_box(moves + [location]))

    return multiplier * len(set(game.get_blank_spaces()) & set(spaces))


def blank_spaces_proximity_score(game, player, multiplier = 1.0):
    own_location = game.get_player_location(player)
    opp_location = game.get_player_location(game.get_opponent(player))

    blank_spaces = [space for space in game.get_blank_spaces() if manhattan_distance(space, own_location) < manhattan_distance(space, opp_location)]

    return multiplier * len(blank_spaces)


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

    p = game.move_count / (game.height * game.width)
    opp = game.get_opponent(player)

    if p <= 0.33:
        return open_moves_score(game, player) - open_moves_score(game, opp, 1.62)
    elif p <= 0.66:
        return bounding_box_blank_spaces_score(game, player, 1.62) - bounding_box_blank_spaces_score(game, opp)
    elif p <= 1.0:
        return blank_spaces_proximity_score(game, player)


def custom_score_2(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp = game.get_opponent(player)

    return open_moves_score(game, player) - open_moves_score(game, opp, 1.62)


def custom_score_3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp = game.get_opponent(player)

    return bounding_box_blank_spaces_score(game, player, 1.62) - bounding_box_blank_spaces_score(game, opp)


def custom_score_4(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    opp = game.get_opponent(player)

    return blank_spaces_proximity_score(game, player) - blank_spaces_proximity_score(game, opp)


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
        # Return the NONE move if there are no legal moves to make
        if not legal_moves:
            return self.NONE

        # Return a random move if the depth limit has been reached
        if not depth:
            return random.choice(legal_moves)

        # Initialize a lambda function which return minimax score for some legal move
        forecast_lambda = lambda m: self.minimax_score(game.forecast_move(m), depth - 1)

        # Apply the initialized lamda function to all the legal moves and choose max/min respectively
        if self is game.active_player:
            return max(legal_moves, key = forecast_lambda)
        if self is game.inactive_player:
            return min(legal_moves, key = forecast_lambda)

    def minimax_score(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the SCORE if the depth limit has been reached
        if not depth:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        # Return the UTILITY score if there are no legal moves to make
        if not legal_moves:
            return game.utility(self)

        # Initialize an array with minimax scores for all the legal moves
        forecast_scores = [self.minimax_score(game.forecast_move(m), depth - 1) for m in legal_moves]

        # Return max/min of the minimax scores respectively
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

        # Initialize the best move
        best_move = self.NONE
        try:
            # Initialize the search depth
            search_depth = self.search_depth
            while True:
                # Reinitialize the best move
                best_move = self.alphabeta(game, search_depth)
                # Increment the search depth
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
        # Return the NONE move if there are no legal moves to make
        if not legal_moves:
            return self.NONE

        # Return a random move if the depth limit has been reached
        if not depth:
            return random.choice(legal_moves)

        # Initialize the score to -inf/+inf respectively
        if self is game.active_player:
            score = float("-inf")
        if self is game.inactive_player:
            score = float("inf")

        # Initialize the move to a random move
        move = random.choice(legal_moves)

        for m in legal_moves:
            # Initialize s to the alphabeta score for the next legal move
            s = self.alphabeta_score(game.forecast_move(m), depth - 1, alpha, beta)
            # Update score, move and alpha/beta if s is better than the score
            if self is game.active_player and s > score:
                score = s
                move = m
                # Return the move if the score cannot be improved anymore
                if score >= beta:
                    return move
                alpha = max(alpha, score)
            if self is game.inactive_player and s < score:
                score = s
                move = m
                # Return the move if the score cannot be improved anymore
                if score <= alpha:
                    return move
                beta = min(beta, score)

        return move

    def alphabeta_score(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # Return the SCORE if the depth limit has been reached
        if not depth:
            return self.score(game, self)

        legal_moves = game.get_legal_moves()
        # Return the UTILITY score if there are no legal moves to make
        if not legal_moves:
            return game.utility(self)

        # Initialize the score to -inf/+inf respectively
        if self is game.active_player:
            score = float("-inf")
        if self is game.inactive_player:
            score = float("inf")

        for m in legal_moves:
            # Initialize s to the alphabeta score for the next legal move
            s = self.alphabeta_score(game.forecast_move(m), depth - 1, alpha, beta)
            # Update score and alpha/beta if s is better than the score
            if self is game.active_player and s > score:
                score = s
                # Return the score if it cannot be improved anymore
                if score >= beta:
                    return score
                alpha = max(alpha, score)
            if self is game.inactive_player and s < score:
                score = s
                # Return score if it cannot be improved anymore
                if score <= alpha:
                    return score
                beta = min(beta, score)

        return score
