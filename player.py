"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human player, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """
    players = []
    goals = generate_goals(num_human + num_random + len(smart_players))
    for i in range(num_human):
        players.append(HumanPlayer(i, goals.pop()))
    for i in range(num_random):
        players.append(RandomPlayer(i + num_human, goals.pop()))
    for i in range(len(smart_players)):
        players.append(SmartPlayer(i + num_human + num_random, goals.pop(),
                                   smart_players[i]))
    return players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    if len(block.children) == 0 or level == 0:
        if _location_in_block(block, location):
            return block
        else:
            return None
    else:
        for child in block.children:
            block_location = _get_block(child, location, level - 1)
            if block_location is not None:
                return block_location
        return None


# HELPER FUNCTION
def _location_in_block(block: Block, location: Tuple[int, int]) -> bool:
    """Return True iff <block> includes <location>. <location> is a coordinate
    pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.
    """
    return (block.position[0] <= location[0] < block.position[0] + block.size
            and block.position[1] <= location[1] < block.position[1] +
            block.size)


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


# HELPER FUNCTION
def _random_move_generator(block: Block, colour: Tuple[int, int, int],
                           moves: List[Tuple[str, Optional[int]]]) -> \
            Optional[Tuple[str, Optional[int], Block]]:
    """Return a random, valid move from <moves> that works on <block>. Return
    None if there are no valid moves.

    If necessary, check if the action PAINT will be valid for <colour>.
    """
    valid = False
    move = None
    moves_copy = moves[:]
    random.shuffle(moves_copy)
    i = 0
    while not valid:
        copy_block = block.create_copy()
        potential_move = moves_copy[i]
        if potential_move == SMASH:
            if copy_block.smash():
                valid = True
                move = _create_move(SMASH, block)
        elif potential_move == SWAP_VERTICAL:
            if copy_block.swap(SWAP_VERTICAL[1]):
                valid = True
                move = _create_move(SWAP_VERTICAL, block)
        elif potential_move == SWAP_HORIZONTAL:
            if copy_block.swap(SWAP_HORIZONTAL[1]):
                valid = True
                move = _create_move(SWAP_HORIZONTAL, block)
        elif potential_move == ROTATE_COUNTER_CLOCKWISE:
            if copy_block.rotate(ROTATE_COUNTER_CLOCKWISE[1]):
                valid = True
                move = _create_move(ROTATE_COUNTER_CLOCKWISE, block)
        elif potential_move == ROTATE_CLOCKWISE:
            if copy_block.rotate(ROTATE_CLOCKWISE[1]):
                valid = True
                move = _create_move(ROTATE_CLOCKWISE, block)
        elif potential_move == PAINT:
            if copy_block.paint(colour):
                valid = True
                move = _create_move(PAINT, block)
        elif potential_move == COMBINE:
            if copy_block.combine():
                valid = True
                move = _create_move(COMBINE, block)
        i += 1
        if i >= len(moves):
            valid = True
    return move


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """Return a tuple representing <action> made on <block>.

    The tuple includes, in order, the name of the move, an optional parameter
    for the move, and the block to use the move on.
    """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)

            self._desired_action = None
            return move


class RandomPlayer(Player):
    """A random player.

    RandomPlayer will choose a random, valid move every turn.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <player_id> and <goal>.

        Initialize _proceed to be False.
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return None since RandomPlayer will select a block at random when
        generating a move.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the player clicking the mouse to proceed in generating
        a random move.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        move = None
        moves = [SMASH, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                 SWAP_HORIZONTAL, SWAP_VERTICAL, COMBINE, PAINT]
        valid = False
        while not valid:
            location_x = random.randint(board.position[0], board.position[0] +
                                        board.size - 1)
            location_y = random.randint(board.position[1], board.position[1] +
                                        board.size - 1)
            level = random.randint(0, board.max_depth)
            block = _get_block(board, (location_x, location_y), level)
            move = _random_move_generator(block, self.goal.colour, moves)
            if move is not None:
                valid = True

        self._proceed = False  # Must set to False before returning!
        return move


class SmartPlayer(Player):
    """A smart player.

    SmartPlayer will generate a number of random, valid moves based on its
    difficulty, and choose the smartest move out of them all to play.
    """
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    # _difficulty:
    #   The number of random, valid moves the player will generate to choose
    #   from.
    # == Representation Invariants concerning the private attributes ==
    #     _difficulty >= 0
    _proceed: bool
    _difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize this SmartPlayer with the given <player_id>, <goal>
        and <difficulty>.

        Initialize _proceed to be False.
        """
        Player.__init__(self, player_id, goal)
        self._proceed = False
        self._difficulty = difficulty

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return None since SmartPlayer will select a block at random when
        generating a move."""
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the player clicking the mouse to proceed in generating
        a 'smart' move."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        best_score = self.goal.score(board)
        move = (PASS[0], PASS[1], board)
        moves = [SMASH, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE,
                 SWAP_HORIZONTAL, SWAP_VERTICAL, COMBINE, PAINT]
        for _ in range(self._difficulty):
            new_copy = board.create_copy()
            copy_block = None
            potential_move = None
            valid = False
            while not valid:

                location_x = random.randint(board.position[0], board.position[0]
                                            + board.size - 1)
                location_y = random.randint(board.position[1], board.position[1]
                                            + board.size - 1)
                level = random.randint(0, board.max_depth)
                block = _get_block(board, (location_x, location_y), level)
                copy_block = _get_block(new_copy, (location_x, location_y),
                                        level)
                potential_move = _random_move_generator(block, self.goal.colour,
                                                        moves)
                if potential_move is not None:
                    valid = True
            if potential_move[0] == SMASH[0]:
                copy_block.smash()
            elif potential_move[0] == SWAP_HORIZONTAL[0]:
                copy_block.swap(potential_move[1])
            elif potential_move[0] == ROTATE_CLOCKWISE[0]:
                copy_block.rotate(potential_move[1])
            elif potential_move == PAINT:
                copy_block.paint(self.goal.colour)
            elif potential_move == COMBINE:
                copy_block.combine()
            potential_score = self.goal.score(new_copy)
            if potential_score > best_score:
                best_score = potential_score
                move = potential_move

        self._proceed = False  # Must set to False before returning!
        return move


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
