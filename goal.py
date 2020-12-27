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
Misha Schwartz, and Jaisie Sin

=== Module Description ===

This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    goals = []
    chosen_goal = random.randint(0, 1)

    colour_list = []
    for colour in COLOUR_LIST:
        colour_list.append(colour)
    random.shuffle(colour_list)

    if chosen_goal == 0:
        for i in range(num_goals):
            goals.append(PerimeterGoal(colour_list[i]))
    else:
        for i in range(num_goals):
            goals.append(BlobGoal(colour_list[i]))
    return goals


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    copy = block.create_copy()
    _smash_to_unit_cells(copy)
    leaves = _leaves(copy)
    leaves.sort()
    leaves.reverse()
    if len(leaves) == 1:
        return [[leaves[0][1]]]
    else:
        flatten = []
        for _ in range(2 ** block.max_depth):
            column = []
            for _ in range(2 ** block.max_depth):
                square = leaves.pop()
                column.append(square[1])
            flatten.append(column)
        return flatten


# HELPER FUNCTION
def _leaves(block: Block) -> List[Tuple[Tuple[int, int], Tuple[int, int, int]]]:
    """Return a list of tuples of all the leaves' position and colour (in
    that order) in <block>.
    """
    if len(block.children) == 0:
        return [(block.position, block.colour)]
    else:
        leaves = []
        for child in block.children:
            leaves.extend(_leaves(child))
        return leaves


# HELPER FUNCTION
def _smash_to_unit_cells(block: Block) -> None:
    """Smash <block> to its unit cells if it's not already one. All the
    children of the smashed block must be of the same colour as the original
    colour. Any original leaves of <block> keeps its colour.
    """
    if block.level == block.max_depth:
        return None
    elif len(block.children) == 4:
        for child in block.children:
            _smash_to_unit_cells(child)
        return None
    else:
        original_colour = block.colour
        block.colour = None
        child_size = round(block.size / 2.0)
        x = block.position[0]
        y = block.position[1]
        children_positions = [(x + child_size, y), (x, y), (x, y + child_size),
                              (x + child_size, y + child_size)]
        for i in range(4):
            position = children_positions[i]
            level = block.level + 1
            child = Block(position, child_size, original_colour, level,
                          block.max_depth)
            block.children.append(child)
        for child in block.children:
            if child.level != child.max_depth:
                _smash_to_unit_cells(child)
        return None


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A player goal in the game of Blocky.

    The player must try to get as many of the target colour unit cells on the
    perimeter of the board.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on <board>.

        The score is calculated by counting how many blocks of the target
        colour is on the perimeter of <board>. Every unit cell block of the
        target colour on the perimeter counts as 1 point, while corner blocks
        count as 2 points.
        """
        flattened = _flatten(board)
        edge = [0, (2 ** board.max_depth) - 1]
        score = 0
        for i in range(len(flattened)):
            for j in range(len(flattened)):
                if flattened[i][j] == self.colour and \
                        ((i in edge and j not in edge) or
                         (j in edge and i not in edge)):
                    score += 1
                elif flattened[i][j] == self.colour and i in edge and j in edge:
                    score += 2
        return score

    def description(self) -> str:
        """Return a description of the goal, including the target colour."""
        return 'Create the most {} on the perimeter.'.format(
            colour_name(self.colour))


class BlobGoal(Goal):
    """A player goal in the game of Blocky.

    The player must try to get the largest connected blob of the target colour
    blocks.
    """

    def score(self, board: Block) -> int:
        """Return the current score for this goal on <board>.

        The score is calculated by counting all the unit cells in the largest
        connected blob of the target colour. Every unit cell block in the
        largest connected blob of the target colour counts as 1 point. A unit
        cell is connected to another if they share an edge (no corners).
        """
        flattened = _flatten(board)

        # create a visited board
        visited = []
        for i in range(len(flattened)):
            column = []
            for j in range(len(flattened)):
                column.append(-1)
            visited.append(column)

        # check which blob has the largest size
        largest = 0
        for i in range(len(visited)):
            for j in range(len(visited)):
                curr_size = 0
                if visited[i][j] == -1:
                    curr_size = self._undiscovered_blob_size((i, j), flattened,
                                                             visited)
                if curr_size > largest:
                    largest = curr_size
        return largest

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] < 0 or pos[0] >= len(board) or pos[1] < 0 or \
                pos[1] >= len(board):
            return 0
        elif visited[pos[0]][pos[1]] == -1 and self.colour \
                != board[pos[0]][pos[1]]:
            visited[pos[0]][pos[1]] = 0
            return 0
        elif visited[pos[0]][pos[1]] == 1 or visited[pos[0]][pos[1]] == 0:
            return 0
        else:
            curr_size = 1
            visited[pos[0]][pos[1]] = 1
            connected = [(pos[0], pos[1] - 1), (pos[0] + 1, pos[1]),
                         (pos[0], pos[1] + 1), (pos[0] - 1, pos[1])]
            for i in range(4):
                curr_size += self._undiscovered_blob_size(connected[i], board,
                                                          visited)
            return curr_size

    def description(self) -> str:
        """Return a description of the goal, including the target colour."""
        return 'Create the largest connected blob of {}.'.format(
            colour_name(self.colour))


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
