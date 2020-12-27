from block import Block
from blocky import _block_to_squares
from goal import generate_goals, _flatten, _leaves, _smash_to_unit_cells, \
    PerimeterGoal, BlobGoal
from player import _get_block, _location_in_block, create_players, Player, \
    HumanPlayer, RandomPlayer, SmartPlayer


# TASK 2: INITIALIZE BLOCKS AND DRAW THEM --------------------------------------
def test__block_to_squares() -> None:
    """Test _block_to_squares.
    - test on a leaf block at level 0
    - test on a block with children
    """
    b = Block((-375, 375), 750, (1, 128, 181), 0, 1)
    assert _block_to_squares(b) == [((1, 128, 181), (-375, 375), 750)]
    assert b.smash()
    squares = _block_to_squares(b)
    assert len(squares) >= 4


def test_block_smash() -> None:
    """Test Block.smash.
    - test using smash on a leaf
    - test that the colour is None after smashing
    - test the block now has exactly 4 children
    - test using smash on a parent doesn't work
    - test using smash on a block at max_depth doesn't work
    """
    b = Block((-375, 375), 750, (0, 0, 0), 0, 3)
    assert b.smash()
    assert b.colour is None
    assert len(b.children) == 4
    assert b.smash() is False
    b1 = Block((0, 0), 100, (0, 0, 0), 0, 0)
    assert b1.smash() is False


# TASK 3: THE GOAL CLASSES AND RANDOM GOALS ------------------------------------
def test_generate_goals() -> None:
    """Test generate_goals.
    - length is num_goals
    - all elements of the list is the same type of goal
    - each goal has a different colour
    """
    goals = generate_goals(3)
    assert len(goals) == 3
    colours = []
    for goal in goals:
        colours.append(goal.colour)
    for colour in colours:
        assert colours.count(colour) == 1


# TASK 4: THE PLAYER CLASS AND RANDOM PLAYERS ----------------------------------
def test__get_block() -> None:
    """Test _get_block and my helper function _location_in_block.
    - helper:
    - when location is in block
    - when location is not in block
    - when location is on the edge of a block
    - function:
    - base case
    - children case
    """
    block = Block((0, 0), 100, (0, 0, 0), 0, 1)
    l1 = (50, 50)
    l2 = (200, 200)
    l3 = (100, 0)
    l4 = (99, 0)
    l5 = (0, 100)
    l6 = (30, 100)
    assert _location_in_block(block, l1)
    assert _location_in_block(block, l2) is False
    assert _location_in_block(block, l3) is False
    assert _location_in_block(block, l4)
    assert _location_in_block(block, l5) is False
    assert _location_in_block(block, l6) is False
    assert _get_block(block, l1, 1) == block
    assert _get_block(block, l2, 0) is None
    assert block.smash()
    child = _get_block(block, l1, 1)
    assert child == block.children[3]
    assert _get_block(block, l1, 0) == block
    assert _get_block(block, l2, 1) is None
    new_block = Block((0, 0), 100, (0, 0, 0), 0, 3)
    assert new_block.smash()
    child = _get_block(new_block, (60, 70), 2)
    assert child.level >= 1


def test_create_players() -> None:
    """Test create_players.
    - test order is correct
    - test numbers align
    - all their ids are unique and in order
    - unique goals (representation invariants?)
    """
    players = create_players(2, 1, [3])
    assert len(players) == 4
    assert isinstance(players[0], HumanPlayer) and players[0].id == 0
    assert isinstance(players[1], HumanPlayer) and players[1].id == 1
    assert isinstance(players[2], RandomPlayer) and players[2].id == 2
    assert isinstance(players[3], SmartPlayer) and players[3].id == 3
    assert players[3]._difficulty == 3


# TASK 5: THE BLOCKY ACTIONS ---------------------------------------------------
def test_block__update_children_positions() -> None:
    """Test Block._update_children_positions."""
    # BASE CASE
    block = Block((50, 50), 100, (0, 0, 0), 0, 2)
    block._update_children_positions((0, 0))
    assert str(block) == 'Leaf: colour=Black, pos=(0, 0), size=100, level=0\n'
    # CHILDREN OF LEVEL 1
    b1 = Block((50, 50), 100, (0, 0, 0), 0, 1)
    assert b1.smash()
    b1._update_children_positions((0, 0))
    assert b1.position == (0, 0)
    assert b1.children[0].position == (50, 0)
    assert b1.children[1].position == (0, 0)
    assert b1.children[2].position == (0, 50)
    assert b1.children[3].position == (50, 50)
    b1._update_children_positions((100, 100))
    assert b1.position == (100, 100)
    assert b1.children[0].position == (150, 100)
    assert b1.children[1].position == (100, 100)
    assert b1.children[2].position == (100, 150)
    assert b1.children[3].position == (150, 150)
    b1._update_children_positions((150, 75))
    assert b1.position == (150, 75)
    assert b1.children[0].position == (200, 75)
    assert b1.children[1].position == (150, 75)
    assert b1.children[2].position == (150, 125)
    assert b1.children[3].position == (200, 125)
    # CHILDREN WITH CHILDREN (can fail based on chance of the block not creating
    # any children)
    block._update_children_positions((50, 50))
    assert block.smash()
    block._update_children_positions((80, 0))
    assert block.children[0].children[0].position == (155, 0)
    assert block.children[0].children[1].position == (130, 0)
    assert block.children[0].children[2].position == (130, 25)
    assert block.children[0].children[3].position == (155, 25)


def test_block_swap() -> None:
    """Test Block.swap.
    - vertical (test in game)
    - horizontal (test in game)
    - block can't be swapped
    """
    block = Block((50, 50), 100, (0, 0, 0), 0, 2)
    assert block.swap(0) is False
    assert block.swap(1) is False


def test_block_rotate() -> None:
    """Test Block.rotate.
    - no children
    - 1 level of children (c and cc)
    - multiple levels of children (test in game)
    """
    # NO CHILDREN
    block = Block((50, 50), 100, (1, 128, 181), 0, 1)
    assert block.rotate(1) is False
    # CHILDREN AT MAX_DEPTH (CLOCKWISE)
    assert block.smash()
    block.children[0].colour = (1, 128, 181)
    block.children[1].colour = (1, 128, 181)
    block.children[2].colour = (138, 151, 71)
    block.children[3].colour = (199, 44, 58)
    assert block.children[0].position == (100, 50)
    assert block.children[1].position == (50, 50)
    assert block.children[2].position == (50, 100)
    assert block.children[3].position == (100, 100)
    assert block.rotate(1)
    assert block.children[0].colour == (1, 128, 181)
    assert block.children[1].colour == (138, 151, 71)
    assert block.children[2].colour == (199, 44, 58)
    assert block.children[3].colour == (1, 128, 181)
    assert block.children[0].position == (100, 50)
    assert block.children[1].position == (50, 50)
    assert block.children[2].position == (50, 100)
    assert block.children[3].position == (100, 100)
    # CHILDREN AT MAX_DEPTH (COUNTERCLOCKWISE)
    assert block.rotate(3)
    assert block.children[0].colour == (1, 128, 181)
    assert block.children[1].colour == (1, 128, 181)
    assert block.children[2].colour == (138, 151, 71)
    assert block.children[3].colour == (199, 44, 58)


def test_block_paint() -> None:
    """Test Block.paint.
    - leaf
    - max_depth only
    - different colour
    """
    block = Block((50, 50), 100, (0, 0, 0), 0, 1)
    assert block.paint((1, 128, 181)) is False
    assert block.smash()
    assert block.paint((1, 128, 181)) is False
    assert block.children[0].paint((0, 0, 0))
    assert block.children[0].colour == (0, 0, 0)


def test_block_combine() -> None:
    """Test Block.combine."""
    # NOT ALLOWED TO COMBINE
    b1 = Block((50, 50), 100, (0, 0, 0), 0, 1)
    b1_str = str(b1)
    assert b1.combine() is False
    assert str(b1) == b1_str
    b2 = Block((50, 50), 100, (0, 0, 0), 0, 2)
    assert b2.smash()
    b2_str = str(b2)
    assert b2.combine() is False
    assert str(b2) == b2_str
    # 3 OR 4 OF SAME COLOUR CHILDREN
    assert b1.smash()
    b1.children[0].colour = (1, 128, 181)
    b1.children[1].colour = (1, 128, 181)
    b1.children[2].colour = (1, 128, 181)
    b1.children[3].colour = (199, 44, 58)
    assert b1.combine()
    assert len(b1.children) == 0
    assert b1.colour == (1, 128, 181)
    # 2 OF SAME COLOUR AND 2 DIFFERENT UNIQUE BLOCKS
    b3 = Block((50, 50), 100, (0, 0, 0), 0, 1)
    assert b3.smash()
    b3.children[0].colour = (1, 128, 181)
    b3.children[1].colour = (1, 128, 181)
    b3.children[2].colour = (138, 151, 71)
    b3.children[3].colour = (199, 44, 58)
    assert b3.combine()
    assert len(b3.children) == 0
    assert b3.colour == (1, 128, 181)
    # TIE
    b4 = Block((50, 50), 100, (0, 0, 0), 0, 1)
    assert b4.smash()
    b4.children[0].colour = (1, 128, 181)
    b4.children[1].colour = (1, 128, 181)
    b4.children[2].colour = (199, 44, 58)
    b4.children[3].colour = (199, 44, 58)
    assert b4.combine() is False
    assert len(b4.children) == 4
    assert b4.colour is None


def test_block_create_copy() -> None:
    """Test Block.create_copy."""
    block = Block((50, 50), 100, (0, 0, 0), 0, 4)
    assert block.smash()
    copy = block.create_copy()
    assert copy == block
    assert copy is not block


# TASK 6: IMPLEMENT SCORING FOR PERIMETER GOALS --------------------------------
# check PerimeterGoal.score in the game
def test__flatten() -> None:
    """Test _flatten.
    - max_depth 0
    - max_depth 1
    """
    block = Block((50, 50), 100, (1, 128, 181), 0, 0)
    assert _flatten(block) == [[(1, 128, 181)]]
    b1 = Block((50, 50), 100, (1, 128, 181), 0, 1)
    assert _flatten(b1) == [[(1, 128, 181), (1, 128, 181)], [(1, 128, 181),
                                                              (1, 128, 181)]]
    assert b1.smash()
    assert _flatten(b1) == [[b1.children[1].colour, b1.children[2].colour],
                             [b1.children[0].colour, b1.children[3].colour]]


def test__leaves_helper() -> None:
    """Test helper function _leaves."""
    block = Block((0, 0), 100, (1, 128, 181), 0, 2)
    _smash_to_unit_cells(block)
    assert _leaves(block) == [(block.children[0].children[0].position,
                               block.children[0].children[0].colour),
                              (block.children[0].children[1].position,
                               block.children[0].children[1].colour),
                              (block.children[0].children[2].position,
                               block.children[0].children[2].colour),
                              (block.children[0].children[3].position,
                               block.children[0].children[3].colour),
                              (block.children[1].children[0].position,
                               block.children[1].children[0].colour),
                              (block.children[1].children[1].position,
                               block.children[1].children[1].colour),
                              (block.children[1].children[2].position,
                               block.children[1].children[2].colour),
                              (block.children[1].children[3].position,
                               block.children[1].children[3].colour),
                              (block.children[2].children[0].position,
                               block.children[2].children[0].colour),
                              (block.children[2].children[1].position,
                               block.children[2].children[1].colour),
                              (block.children[2].children[2].position,
                               block.children[2].children[2].colour),
                              (block.children[2].children[3].position,
                               block.children[2].children[3].colour),
                              (block.children[3].children[0].position,
                               block.children[3].children[0].colour),
                              (block.children[3].children[1].position,
                               block.children[3].children[1].colour),
                              (block.children[3].children[2].position,
                               block.children[3].children[2].colour),
                              (block.children[3].children[3].position,
                               block.children[3].children[3].colour)]


def test__smash_to_unit_cells() -> None:
    """Test helper function _smash_to_unit_cells."""
    b1 = Block((0, 0), 100, (1, 128, 181), 0, 3)
    _smash_to_unit_cells(b1)
    assert len(_leaves(b1)) == 64


# TASK 7: IMPLEMENT SCORING FOR BLOB GOAL --------------------------------------
# check BlobGoal.score in the game
def test_blobgoal__undiscovered_blob_size() -> None:
    """Test BlobGoal._undiscovered_blob_size.
    - gives largest blob of the colour and position
    - updates visited
    """
    block = Block((0, 0), 100, (1, 128, 181), 0, 1)
    assert block.smash()
    block.children[0].colour = (1, 128, 181)
    block.children[1].colour = (1, 128, 181)
    block.children[2].colour = (0, 0, 0)
    block.children[3].colour = (0, 0, 0)
    goal = BlobGoal((1, 128, 181))
    flattened = _flatten(block)
    visited = [[-1, -1], [-1, -1]]
    assert goal._undiscovered_blob_size((1, 0), flattened, visited) == 2
    assert visited == [[1, 0], [1, 0]]


# TASK 8: ADD RANDOM PLAYERS ---------------------------------------------------


# TASK 9: ADD SMART PLAYERS ----------------------------------------------------


if __name__ == '__main__':
    import pytest
    pytest.main(['test.py'])
