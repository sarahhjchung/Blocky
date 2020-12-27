from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten, generate_goals
from player import _get_block, create_players, HumanPlayer, RandomPlayer,\
    SmartPlayer
from renderer import Renderer
from settings import COLOUR_LIST


def set_children(block: Block, colours: List[Optional[Tuple[int, int, int]]]) \
        -> None:
    """Set the children at <level> for <block> using the given <colours>.

    Precondition:
        - len(colours) == 4
        - block.level + 1 <= block.max_depth
    """
    size = block._child_size()
    positions = block._children_positions()
    level = block.level + 1
    depth = block.max_depth

    block.children = []  # Potentially discard children
    for i in range(4):
        b = Block(positions[i], size, colours[i], level, depth)
        block.children.append(b)


@pytest.fixture
def renderer() -> Renderer:
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    pygame.init()
    return Renderer(750)


@pytest.fixture
def child_block_a() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[0], 0, 0)


@pytest.fixture
def child_block_b() -> Block:
    """Create a reference child block with a size of 750 and a max_depth of 0.
    """
    return Block((0, 0), 750, COLOUR_LIST[3], 0, 0)


@pytest.fixture
def board_16x16() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def board_16x16_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    return board


@pytest.fixture
def board_16x16_rotate1() -> Block:
    """Create a reference board where the top-right block on level 1 has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 2)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[0], colours)

    return board


@pytest.fixture
def flattened_board_16x16() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1]],
        [COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[3]],
        [COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]

@pytest.fixture
def board_32x32() -> Block:
    """Create a reference board with a size of 750 and a max_depth of 2.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], None, COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[0], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[2]]
    set_children(board.children[0].children[1], colours)

    return board


@pytest.fixture
def board_32x32_swap0() -> Block:
    """Create a reference board that is swapped along the horizontal plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [COLOUR_LIST[2], None, COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], None, COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[1], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[2]]
    set_children(board.children[1].children[1], colours)

    return board

@pytest.fixture
def board_32x32_swap1() -> Block:
    """Create a reference board that is swapped along the vertical plane.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [COLOUR_LIST[3], COLOUR_LIST[1], COLOUR_LIST[2], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], None, COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[2]]
    set_children(board.children[3].children[1], colours)

    return board

@pytest.fixture
def board_32x32_swap0_child0_rotate3_child0child0() -> Block:
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [None, COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board, colours)

    # Level 2
    colours = [None, COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[1]]
    set_children(board.children[0], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0]]
    set_children(board.children[0].children[0], colours)

    return board

@pytest.fixture
def board_32x32_rotate1() -> Block:
    """Create a reference board where the entire board has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], None]
    set_children(board, colours)

    # Level 2
    colours = [None, COLOUR_LIST[1], COLOUR_LIST[3], COLOUR_LIST[0]]
    set_children(board.children[3], colours)

    # Level 3
    colours = [COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[2], COLOUR_LIST[2]]
    set_children(board.children[3].children[0], colours)

    return board


@pytest.fixture
def board_32x32_rotate3() -> Block:
    """Create a reference board where the entire board has been
    rotated counter-clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [COLOUR_LIST[3], None, COLOUR_LIST[2], COLOUR_LIST[1]]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[3], COLOUR_LIST[0], None, COLOUR_LIST[1]]
    set_children(board.children[1], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0]]
    set_children(board.children[1].children[2], colours)

    return board


@pytest.fixture
def board_32x32_rotate1_rotate3_child3_rotate3_child3child1() -> Block:
    """Create a reference board where the entire board has been
    rotated clockwise.
    """
    # Level 0
    board = Block((0, 0), 750, None, 0, 3)

    # Level 1
    colours = [COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[3], None]
    set_children(board, colours)

    # Level 2
    colours = [COLOUR_LIST[0], None, COLOUR_LIST[1], COLOUR_LIST[3]]
    set_children(board.children[3], colours)

    # Level 3
    colours = [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[0]]
    set_children(board.children[3].children[1], colours)

    return board


@pytest.fixture
def flattened_board_32x32() -> List[List[Tuple[int, int, int]]]:
    """Create a list of the unit cells inside the reference board."""
    return [
        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1]],

        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1]],

        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1]],

        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[2],
         COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1], COLOUR_LIST[1]],

        [COLOUR_LIST[1], COLOUR_LIST[0], COLOUR_LIST[1], COLOUR_LIST[1],
         COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],

        [COLOUR_LIST[2], COLOUR_LIST[2], COLOUR_LIST[1], COLOUR_LIST[1],
         COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],

        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]],

        [COLOUR_LIST[0], COLOUR_LIST[0], COLOUR_LIST[3], COLOUR_LIST[3],
         COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3], COLOUR_LIST[3]]
    ]


class TestTask2:
    """A collection of methods to test task two implementations"""
    def test_block_2_squares_a(self, board_16x16) -> None:
        squares = set(_block_to_squares(board_16x16))
        expected = {((1, 128, 181), (563, 0), 188),
                    ((199, 44, 58), (375, 0), 188),
                    ((199, 44, 58), (375, 188), 188),
                    ((255, 211, 92), (563, 188), 188),
                    ((138, 151, 71), (0, 0), 375),
                    ((199, 44, 58), (0, 375), 375),
                    ((255, 211, 92), (375, 375), 375)
                    }
        assert squares == expected

    def test_block_2_squares_b(self, board_32x32) -> None:
        squares = set(_block_to_squares(board_32x32))
        expected = {((138, 151, 71), (469, 0), 94),
                    ((199, 44, 58), (375, 0), 94),
                    ((1, 128, 181), (375, 94), 94),
                    ((138, 151, 71), (469, 94), 94),
                    ((1, 128, 181), (563, 0), 188),
                    ((199, 44, 58), (375, 188), 188),
                    ((255, 211, 92), (563, 188), 188),
                    ((138, 151, 71), (0, 0), 375),
                    ((199, 44, 58), (0, 375), 375),
                    ((255, 211, 92), (375, 375), 375)
                    }
        assert squares == expected

    def test_block_2_squares_no_children(self) -> None:
        board = Block((0, 0), 750, (138, 151, 71), 0, 3)
        squares = set(_block_to_squares(board))
        expected = {((138, 151, 71), (0,0), 750)}
        assert squares == expected

    def test_smash_on_child_a(self, child_block_a) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block_a.smash()

        assert len(child_block_a.children) == 0
        assert child_block_a.colour == COLOUR_LIST[0]

    def test_smash_on_child_b(self, child_block_b) -> None:
        """Test that a child block cannot be smashed.
        """
        child_block_b.smash()

        assert len(child_block_b.children) == 0
        assert child_block_b.colour == COLOUR_LIST[3]

    def test_smash_on_parent_with_no_children(self, board_32x32) -> None:
        """Test that a block not at max_depth and with no children can be
        smashed.
        """
        block = board_32x32.children[1]
        block.smash()

        assert len(block.children) == 4
        assert block.colour is None

        for child in block.children:
            if len(child.children) == 0:
                # A leaf should have a colour
                assert child.colour is not None
                # Colours should come from COLOUR_LIST
                assert child.colour in COLOUR_LIST
            elif len(child.children) == 4:
                # A parent should not have a colour
                assert child.colour is None
            else:
                # There should only be either 0 or 4 children (RI)
                assert False


class TestTask3:
    """A collection of methods to test task three implementations"""
    def test_generate_goals_len(self) -> None:
        goals = generate_goals(3)
        assert len(goals) == 3

    def test_generate_goals_type(self) -> None:
        goals = generate_goals(2)
        for goal in goals:
            assert isinstance(goal, type(goals[0]))

    def test_generate_goals_colour(self) -> None:
        goals = generate_goals(3)
        for i in range(len(goals) - 1):
            for j in range(i + 1, len(goals)):
                assert goals[i].colour != goals[j].colour


class TestTask4:
    """A collection of methods to test task four implementations"""

    def test_get_block(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (0,0), 1)
        the_block = Block((0,0), 375, COLOUR_LIST[2], 1, 3)
        assert get_block == the_block

    def test_get_block_level_under(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (0,0), 2)
        assert get_block == Block((0,0), 375, COLOUR_LIST[2], 1, 3)

    def test_get_block_level_none1(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (0,750), 0)
        assert get_block is None

    def test_get_block_level_none2(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (750,750), 0)
        assert get_block is None

    def test_get_block_level_none3(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (750,0), 0)
        assert get_block is None

    def test_get_block_level_none4(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (750,375), 0)
        assert get_block is None

    def test_get_block_level_none5(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (244,750), 0)
        assert get_block is None

    def test_get_block_board(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (35, 127), 0)
        assert get_block == board_32x32

    def test_get_block_corner(self, board_32x32) -> None:
        get_block = _get_block(board_32x32, (376, 376), 1)
        the_block = Block((375, 375), 375, COLOUR_LIST[3], 1, 3)
        assert get_block == the_block

    def test_create_players_id(self) -> None:
        players = create_players(2, 1, [3])
        for i in range(len(players)):
            assert players[i].id == i

    def test_create_players_difficulty(self) -> None:
        players = create_players(1, 0, [3, 6, 300])
        s_player1 = players[1]
        s_player2 = players[2]
        s_player3 = players[3]
        assert s_player1.difficulty == 3
        assert s_player2.difficulty == 6
        assert s_player3.difficulty == 300

    def test_create_players_nums(self) -> None:
        players = create_players(0, 2, [3, 6])
        h_count = 0
        r_count = 0
        s_count = 0
        for player in players:
            if type(player) == HumanPlayer:
                h_count += 1
            if type(player) == RandomPlayer:
                r_count += 1
            if type(player) == SmartPlayer:
                s_count += 1
        assert h_count == 0
        assert r_count == 2
        assert s_count == 2


class TestTask5:
    """A collection of methods to test task five implementations"""
    def test_update_children_positions(self, board_32x32) -> None:
        block1 = board_32x32.children[0]
        block2 = board_32x32.children[1]
        block1._update_children_positions((0,0))
        block2._update_children_positions((375,0))
        assert block1.position == (0,0)
        assert block2.position == (375,0)
        assert block1.children[3].position == (188,188)
        assert block1.children[1].children[3].position == (94,94)

    def test_smashable1(self, board_32x32) -> None:
        block = board_32x32.children[3]
        assert block.smashable()

    def test_smashable2(self, board_32x32) -> None:
        block = board_32x32.children[0].children[2]
        assert block.smashable()

    def test_smashable3(self, board_32x32) -> None:
        block = board_32x32.children[0]
        assert not block.smashable()

    def test_swap0(self, board_32x32, board_32x32_swap0) -> None:
        assert board_32x32.swap(0)
        assert board_32x32 == board_32x32_swap0

    def test_swap1(self, board_32x32, board_32x32_swap1) -> None:
        assert board_32x32.swap(1)
        assert board_32x32 == board_32x32_swap1

    def test_swap0_rotate3(self, board_32x32,
                           board_32x32_swap0_child0_rotate3_child0child0) \
            -> None:
        assert board_32x32.children[0].swap(0)
        assert board_32x32.children[0].children[0].rotate(3)
        assert board_32x32 == board_32x32_swap0_child0_rotate3_child0child0

    def test_rotate1(self, board_32x32, board_32x32_rotate1) -> None:
        assert board_32x32.rotate(1)
        assert board_32x32 == board_32x32_rotate1

    def test_rotate3(self, board_32x32, board_32x32_rotate3) -> None:
        assert board_32x32.rotate(3)
        assert board_32x32 == board_32x32_rotate3

    def test_rotate1_rotate3_rotate3(self, board_32x32,
                                     board_32x32_rotate1_rotate3_child3_rotate3_child3child1) -> None:
        assert board_32x32.rotate(1)
        assert board_32x32.children[3].rotate(3)
        assert board_32x32.children[3].children[1].rotate(3)
        assert board_32x32 == board_32x32_rotate1_rotate3_child3_rotate3_child3child1

    def test_paint_leaf(self, board_32x32) -> None:
        assert board_32x32.children[0].children[1].children[2].paint\
            (COLOUR_LIST[2])
        assert board_32x32.children[0].children[1].children[2].colour == \
            COLOUR_LIST[2]

    def test_paint_leaf_wrong_colour(self, board_32x32) -> None:
        assert not board_32x32.children[0].children[1].children[2].paint \
            (COLOUR_LIST[0])

    def test_paint_leaf_wrong_children1(self, board_32x32) -> None:
        assert not board_32x32.children[0].children[1].paint(COLOUR_LIST[0])

    def test_paint_leaf_wrong_children2(self, board_32x32) -> None:
        assert not board_32x32.children[0].paint(COLOUR_LIST[0])

    def test_paint_leaf_wrong_level1(self, board_32x32) -> None:
        assert not board_32x32.children[1].paint(COLOUR_LIST[0])

    def test_paint_leaf_wrong_level2(self, board_32x32) -> None:
        assert not board_32x32.children[0].children[2].paint(COLOUR_LIST[0])

    def test_combine1(self, board_32x32) -> None:
        assert board_32x32.children[0].children[1].combine()
        assert board_32x32.children[0].children[1].colour == COLOUR_LIST[2]

    def test_combine_wrong1(self, board_32x32) -> None:
        assert not board_32x32.children[0].combine()

    def test_combine_wrong2(self, board_32x32) -> None:
        assert not board_32x32.children[1].combine()

    def test_combine_wrong3(self, board_32x32) -> None:
        assert not board_32x32.children[0].children[2].combine()

    def test_combine2(self, board_16x16) -> None:
        assert board_16x16.children[0].combine()
        assert board_16x16.children[0].colour == COLOUR_LIST[1]

    def test_create_copy1(self, board_32x32) -> None:
        board2 = board_32x32.create_copy()
        assert board_32x32 == board2

    def test_create_copy2(self, board_32x32) -> None:
        board2 = board_32x32.create_copy()
        assert id(board_32x32) != id(board2)


class TestTask6:
    """A collection of methods to test task six implementations"""
    def test_flatten(self, board_32x32, flattened_board_32x32) -> None:
        assert _flatten(board_32x32) == flattened_board_32x32

    def test_flatten_leaf(self, board_32x32) -> None:
        leaf = board_32x32.children[0].children[1].children[2]
        assert _flatten(leaf) == [[COLOUR_LIST[0]]]

    def test_perimeter_goal(self, board_32x32) -> None:
        goal = PerimeterGoal(COLOUR_LIST[2])
        assert goal.score(board_32x32) == 9

    def test_perimeter_goal_swap(self, board_32x32_swap0) -> None:
        goal = PerimeterGoal(COLOUR_LIST[1])
        assert goal.score(board_32x32_swap0) == 12

    def test_perimeter_goal_rotate(self, board_32x32_rotate1) -> None:
        goal1 = PerimeterGoal(COLOUR_LIST[2])
        goal2 = PerimeterGoal(COLOUR_LIST[3])
        assert goal1.score(board_32x32_rotate1) == 9
        assert goal2.score(board_32x32_rotate1) == 10


class TestTask7:
    """A collection of methods to test task seven implementations"""
    def test_blob_goal3(self, board_32x32) -> None:
        goal = BlobGoal(COLOUR_LIST[3])
        assert goal.score(board_32x32) == 20

    def test_blob_goal0(self, board_32x32) -> None:
        goal = BlobGoal(COLOUR_LIST[0])
        assert goal.score(board_32x32) == 4

    def test_blob_goal1(self, board_32x32_rotate1) -> None:
        goal = BlobGoal(COLOUR_LIST[1])
        assert goal.score(board_32x32_rotate1) == 16

    def test_blob_goal_other(self, board_32x32) -> None:
        board_32x32.children[0].children[2].colour = COLOUR_LIST[0]
        goal = BlobGoal(COLOUR_LIST[0])
        assert goal.score(board_32x32) == 5

    def test_blob_goal_16(self, board_16x16) -> None:
        board_16x16.children[1].colour = COLOUR_LIST[1]
        goal = BlobGoal(COLOUR_LIST[1])
        assert goal.score(board_16x16) == 10


class TestTask8:
    """A collection of methods to test task eight implementations"""


if __name__ == '__main__':
    pytest.main(['A2_testing_suite.py'])
