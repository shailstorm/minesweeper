"""
6.1010 Spring '23 Lab 7: Mines
"""

#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    state: ongoing
    """
    dimensions = (num_rows, num_cols)
    return new_game_nd(dimensions, bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.',  3,  1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    state: defeat
    """
    coordinates = (row, col)
    return dig_nd(game, coordinates)


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    rendered_loc = render_2d_locations(game, xray)
    rendered_board = ""
    for row in rendered_loc:
        for item in row:
            rendered_board += item
        rendered_board += "\n"
    return rendered_board[:-1]


# N-D IMPLEMENTATION

def get_at(array, coords):
    """
    returns val of array at coords.
    >>> get_at([['.', 3, 1, 0], ['.', '.', 1, 0]], (0, 1))
    3
    """
    if len(coords) == 1:
        return array[coords[0]]
    else:
        return get_at(array[coords[0]], coords[1:])


def set_at(array, coords, val):
    """
    sets value of array at coords to val specified.
    >>> arr = [['.', 3, 1, 0], ['.', '.', 1, 0]]
    >>> set_at(arr, (0, 1), 'a')
    >>> get_at(arr, (0, 1))
    'a'
    """
    if len(coords) == 1:
        array[coords[0]] = val
    else:
        set_at(array[coords[0]], coords[1:], val)

def new_array(dim, val):
    """
    returns new n-d array with dim dimensions.
    each value in the array is val.
    >>> new_array((3, 2), 4)
    [[4, 4], [4, 4], [4, 4]]
    """
    if len(dim) == 1:
        return [ val for tile in range(dim[0]) ]
    else:
        return [ new_array(dim[1:], val) for di in range(dim[0]) ]

def get_neighbors(dim, coords):
    """
    returns a set of all neighbors of value at given coordinates in a given game
    """
    neighbors = {tuple()}

    for c, di in zip(coords, dim):
        new_neigh = set()
        for neigh in neighbors:
            for x in (-1, 0, 1):
                if 0 <= c+x < di:
                    new_neigh.add(neigh + (c+x,))
            neighbors = new_neigh
    return neighbors-{coords}


def game_state(game):
    """
    returns state of that game. victory if all hiddens are bombs
    # bombs hidden + 
    # non bomb tiles revealed
    equal all_coords
    """
    bomb_count = 0
    nonbombs = 0
    num_tiles = len(get_all_coords(game["dimensions"]))
    for coord in get_all_coords(game["dimensions"]):
        coord_val = get_at(game["board"], coord)
        coord_h = get_at(game["hidden"], coord)
        # not hidden but is a bomb
        if coord_h is False and coord_val == ".":
            game["state"] = "defeat"
        elif coord_val == ".":
            bomb_count += 1
        elif coord_h is False and coord_val != ".":
            nonbombs += 1
    if bomb_count + nonbombs == num_tiles:
        game["state"] = "victory"
    

def get_all_coords(dimensions):
    """
    returns all coords
    """
    if len(dimensions) == 1:
        return [(coord,) for coord in range(dimensions[0])]
    else:
        return [(x,) + coord for x in range(dimensions[0]) 
                for coord in get_all_coords(dimensions[1:])]


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: ongoing
    """
    arr = new_array(dimensions, 0)
    for bomb_coord in bombs:
        set_at(arr, bomb_coord, ".")
        for neighbor in get_neighbors(dimensions, bomb_coord):
            if get_at(arr, neighbor) != ".":
                set_at(arr, neighbor, (get_at(arr, neighbor)+1))
                
    return {"board": arr,
            "dimensions": dimensions,
            "hidden": new_array(dimensions, True),
            "state": "ongoing"}


def dig_nd(game, coordinates, check_game_state=True):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    state: defeat
    """

    if game["state"] != "ongoing": # if game is done
        return 0
    
    if get_at(game["board"], coordinates) == ".": # if u hit a bomb
        set_at(game["hidden"], coordinates, False)
        game["state"] = "defeat"
        return 1

    if get_at(game["hidden"], coordinates): # if u dug at a hidden tile
        set_at(game["hidden"], coordinates, False)
        revealed = 1
    else: # if u dug at alr revealed tile
        return 0

    if get_at(game["board"], coordinates) == 0: # if u dug at a 0 tile
        set_at(game["hidden"], coordinates, False)
        for neighbor in get_neighbors(game["dimensions"], coordinates):
            if get_at(game["board"], neighbor) != ".":
                revealed += dig_nd(game, neighbor, False)
    if check_game_state is True:
        game_state(game)
    return revealed


def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    rendered_board = new_array(game["dimensions"], " ")
    for coord in get_all_coords(game["dimensions"]):
        coord_val = get_at(game["board"], coord)
        coord_h = get_at(game["hidden"], coord)
        if coord_h and not xray: # hidden and no xray
            set_val = "_"
        elif coord_val == 0: # not hidden and 0
            set_val = " "
        else: # not hidden and not 0
            set_val = str(coord_val)
        set_at(rendered_board, coord, set_val)
    return rendered_board


if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    #doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #

    dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    
    doctest.run_docstring_examples(
       render_2d_locations,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )
    
    doctest.run_docstring_examples(
       render_2d_board,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       new_game_2d,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       set_at,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       get_at,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       render_nd,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       new_game_nd,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       dig_nd,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )

    doctest.run_docstring_examples(
       render_nd,
       globals(),
       optionflags=_doctest_flags,
       verbose=False
    )
