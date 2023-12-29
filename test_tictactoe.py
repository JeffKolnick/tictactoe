import unittest
import sys
import io

from unittest.mock import patch
from tictactoe import (
    draw_board,
    player_choice,
    three_in_a_row,
    is_legal_move,
    switch_turn,
    collect_legal_moves,
    find_win,
    find_block,
    find_corner,
    find_side,
    next_move,
)

class TestDrawBoard(unittest.TestCase):

    """
    Test cases for draw_board function
    """
    
    def test_draw_board_empty(self):
        
        # Test drawing an empty board
        with patch('builtins.print') as mocked_print:
            draw_board([['_'] * 3 for _ in range(3)])
            mocked_print.assert_any_call("___|___|___".format('_', '_', '_'))
            mocked_print.assert_any_call("___|___|___".format('_', '_', '_'))
            mocked_print.assert_any_call("   |   |   ".format(' ', ' ', ' '))

    def test_draw_board_partially_filled(self):
        
        # Test drawing a partially filled board
        board_state = [['X', 'O', '_'], ['_', 'X', 'O'], ['O', '_', 'X']]

        with patch('builtins.print') as mocked_print:
            draw_board(board_state)
            mocked_print.assert_any_call("_X_|_O_|___")
            mocked_print.assert_any_call("___|_X_|_O_")
            mocked_print.assert_any_call(" O |   | X ")   

    def test_draw_board_all_filled(self):
        
        # Test drawing a full board
        board_state = [['X', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'O']]

        with patch('builtins.print') as mocked_print:
            draw_board(board_state)
            mocked_print.assert_any_call("_X_|_O_|_X_")
            mocked_print.assert_any_call("_X_|_X_|_O_")
            mocked_print.assert_any_call(" O | X | O ")

    def test_draw_board_invalid_matrix(self):  
        
        # Test handling an invalid board_state
        with self.assertRaises(ValueError):
            draw_board([['_', '_'], ['_', '_']])   

    def test_draw_board_one_lowercase(self):
        
        # Test handling a lowercase letter
        board_state = [['X', 'O', 'X'], ['O', 'x', 'O'], ['O', 'X', 'O']]

        with self.assertRaises(ValueError):
            draw_board(board_state)
                

class TestPlayerChoice(unittest.TestCase) :

    """
    Test cases for player_choice function
    """

    @patch('builtins.input', side_effect = ['X'])
    def test_player_choice_valid_input(self, mock_input):
        
        # Test player selecting 'X'
        result = player_choice()
        self.assertEqual(result, 'X')

    @patch('builtins.input', side_effect = ['@', 'X'])
    def test_player_choice_invalid_input(self, mock_input):
        
        # Test player selecting '@' then 'X'
        result = player_choice()
        self.assertEqual(result, 'X')

    @patch('builtins.input', side_effect = [' O  '])        
    def test_player_choice_valid_input_with_spaces(self, mock_input):
        
        # Test player selecting ' O  ' (note spaces)
        result = player_choice()
        self.assertEqual(result, 'O')

class TestThreeInARow(unittest.TestCase):

    """
    Test cases for three_in_a_row function
    """
    
    def test_three_in_a_row_empty(self):
        
        # Test empty board (no win)
        board_state = [['_', '_', '_'],
                       ['_', '_', '_'],
                       ['_', '_', '_']]
        result = three_in_a_row(board_state, 'X')
        self.assertFalse(result)

    def test_three_in_a_row_horizontal(self):
        
        # Test partially filled board (horizontal win)
        board_state = [['X', 'X', 'X'],
                       ['O', 'O', '_'],
                       ['_', 'O', '_']]
        result = three_in_a_row(board_state, 'X')
        self.assertTrue(result)

    def test_three_in_a_row_vertical(self):
        
        # Test partially filled board (vertical win)
        board_state = [['X', 'O', 'O'],
                       ['X', 'O', '_'],
                       ['X', 'X', '_']]
        result = three_in_a_row(board_state, 'X')
        self.assertTrue(result)

    def test_three_in_a_row_diagonal(self):
        
        # Test partially filled board (diagonal win)
        board_state = [['X', 'O', 'O'],
                       ['O', 'X', '_'],
                       ['O', 'X', 'X']]
        result = three_in_a_row(board_state, 'X')
        self.assertTrue(result)

    def test_no_three_in_a_row(self):
        
        # Test partially filled board (no win)
        board_state = [['X', 'O', 'O'],
                       ['O', 'X', '_'],
                       ['O', 'X', '_']]
        result = three_in_a_row(board_state, 'X')
        self.assertFalse(result)

    def test_three_in_a_row_invalid_symbol(self):
        
        # Test partially filled board with '%'
        invalid_board_state = [['X', 'O', 'O'],
                       ['O', '%', '_'],
                       ['O', 'X', '_']]
        with self.assertRaises(ValueError):
            three_in_a_row(invalid_board_state, 'O')

    def test_three_in_a_row_invalid_matrix(self):
        
        # Test partially filled board with short second row
        invalid_board_state = [['X', 'O',],
                       ['O', '_'],
                       ['O', 'X', '_']]
        with self.assertRaises(ValueError):
            three_in_a_row(invalid_board_state, 'X')

    def test_three_in_a_row_vertical_lowercase(self):
        
        # Test partially filled board with 'x' (lowercase)        
        invalid_board_state = [['X', 'O', 'O'],
                       ['x', 'O', '_'],
                       ['X', 'X', '_']]
        with self.assertRaises(ValueError):
            three_in_a_row(invalid_board_state, 'X')

class TestIsLegalMove(unittest.TestCase):

    """
    Test cases for is_legal_move function
    """

    def setUp(self):
        # Define board_state for following tests
        self.board_state = [['_', '_', '_'],
                       ['_', 'X', '_'],
                       ['_', '_', '_']]

    def test_legal_move(self):
        # Test ability to report legal move      
        result = is_legal_move(self.board_state, 0, 1)
        self.assertTrue(result)

    def test_illegal_move_out_of_bounds(self):
        # Handle move out of matrix boundaries
        result = is_legal_move(self.board_state, 3, 1)
        self.assertFalse(result)

    def test_illegal_move_occupied_square(self):
        # Test ability to report illegal move
        result = is_legal_move(self.board_state, 1, 1)
        self.assertFalse(result)

    def test_illegal_move_invalid_symbols(self):
        # Handle board_state with invalid symbol '%'
        invalid_board_state = [['%', '_', '_'],
                       ['_', 'X', '_'],
                       ['_', '_', '_']]        
        with self.assertRaises(ValueError):
            is_legal_move(invalid_board_state, 0, 0)

class TestSwitchTurn(unittest.TestCase):

    """
    Test cases for switch_turn function
    """

    def test_switch_turn_X_to_O(self):
        # Test ability to switch active player from 'X' to 'O'
        result = switch_turn('X')
        self.assertEqual(result, 'O')

    def test_switch_turn_O_to_X(self):
        # Test ability to switch active player from 'O' to 'X'
        result = switch_turn('O')
        self.assertEqual(result, 'X')

    def test_switch_turn_invalid_symbol(self):
        # Handle passed invalid symbol 'A'
        with self.assertRaises(ValueError):
            switch_turn('A')

class TestCollectLegalMoves(unittest.TestCase):

    """
    Test cases for collect_legal_moves function
    """

    def test_collect_legal_moves(self):
        # Test list reports all legal moves available
        board_state = [['_', '_', '_'],
                       ['X', 'O', 'X'],
                       ['_', '_', 'O']]
        result = collect_legal_moves(board_state)
        self.assertEqual(result, [[0, 0], [0, 1], [0, 2], [2, 0], [2, 1]])

    def test_collect_legal_moves_invalid_board(self):
        # Handle passed improper matrix
        invalid_board_state = [['_', '_', '_'],
                       ['X', 'O'],
                       ['_', '_', 'O']]
        with self.assertRaises(ValueError):
            collect_legal_moves(invalid_board_state)
    
    def test_collect_legal_moves_invalid_symbol(self):
        # Handle passed board_state with invalid symbol 'f'
        invalid_board_state = [['_', 'f', '_'],
                       ['X', 'O', 'O'],
                       ['_', '_', 'O']]
        with self.assertRaises(ValueError):
            collect_legal_moves(invalid_board_state)

class TestFindWin(unittest.TestCase):

    """
    Test cases for find_win function
    """

    def setUp(self):        
        # Set up tests where computer makes move
        self.move_made = [False]
        
    def test_find_win_X(self):
        # Test ability to find potential win for 'X'
        board_state = [['X', 'O', '_'],
                       ['X', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'X'
        result = find_win(board_state, legal_moves, X_or_O, self.move_made)
        self.assertFalse(result)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(board_state, [['X', 'O', '_'],
                                       ['X', 'X', '_'],
                                       ['_', 'O', 'X']])
        
    def test_find_win_O(self):
        # Test ability to find potential win for 'O'
        board_state = [['X', 'O', '_'],
                       ['X', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        result = find_win(board_state, legal_moves, X_or_O, self.move_made)
        self.assertFalse(result)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(board_state, [['X', 'O', '_'],
                                       ['X', 'O', '_'],
                                       ['_', 'O', 'X']])

    def test_find_win_invalid_symbol(self):
        # Handle passed board_state with invalid symbol 'x'
        invalid_board_state = [['X', 'O', '_'],
                       ['x', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_win(invalid_board_state, legal_moves, X_or_O, self.move_made)        
        self.assertTrue(self.move_made == [False])

    def test_find_win_invalid_board(self):
        # Handle passed board_state with improper matrix
        invalid_board_state = [['X', 'O', '_'],
                       ['x', '_', '_'],
                       ['_', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_win(invalid_board_state, legal_moves, X_or_O, self.move_made)        
        self.assertTrue(self.move_made == [False])

    def test_find_win_move_made(self):
        # Test function does not make second move
        move_made = [True]
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'X'
        result = find_win(board_state, legal_moves, X_or_O, move_made)
        self.assertTrue(move_made == [True])
        self.assertEqual(result, None)

class TestFindBlock(unittest.TestCase):

    """
    Test cases for find_block function
    """

    def setUp(self):        
        # Set up tests where computer makes move
        self.move_made = [False]

    def test_find_block_X(self):
        # Test ability to find potential win for 'X' (human is 'X')
        board_state = [['X', '_', '_'],
                       ['X', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 1], [0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        result = find_block(board_state, legal_moves, X_or_O, self.move_made)
        self.assertEqual(result, 'X')
        self.assertTrue(self.move_made == [True])
        self.assertEqual(board_state, [['X', '_', '_'],
                                       ['X', 'O', '_'],
                                       ['_', 'O', 'X']])
        
    def test_find_block_O(self):
        # Test ability to find potential win for 'O' (human is 'O')
        board_state = [['_', 'O', '_'],
                       ['X', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 0], [0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'X'
        result = find_block(board_state, legal_moves, X_or_O, self.move_made)
        self.assertEqual(result, 'O')
        self.assertTrue(self.move_made == [True])
        self.assertEqual(board_state, [['_', 'O', '_'],
                                       ['X', 'X', '_'],
                                       ['_', 'O', 'X']])

    def test_find_block_invalid_symbol(self):
        # Handle passed board_state with invalid symbol 'x'
        invalid_board_state = [['X', 'O', '_'],
                       ['x', '_', '_'],
                       ['_', 'O', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_block(invalid_board_state, legal_moves, X_or_O, self.move_made)        
        self.assertTrue(self.move_made == [False])

    def test_find_block_invalid_board(self):
        # Handle passed board_state with improper matrix
        invalid_board_state = [['X', 'O', '_'],
                       ['x', '_', '_'],
                       ['_', 'X']]
        legal_moves = [[0, 2], [1, 1], [1, 2], [2, 0]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_block(invalid_board_state, legal_moves, X_or_O, self.move_made)        
        self.assertTrue(self.move_made == [False])

    def test_find_block_move_made(self):
        # Test function does not make second move
        move_made = [True]
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'X'
        result = find_block(board_state, legal_moves, X_or_O, move_made)
        self.assertTrue(move_made == [True])
        self.assertEqual(result, None)

class TestFindCorner(unittest.TestCase):

    """
    Test cases for find_corner function
    """

    def setUp(self):
        # Set up tests where computer makes move
        self.move_made = [False]

    def test_find_corner_valid_O(self):
        # Test ability to find corner move with 'O'
        board_state = [['X', 'O', 'X'],
                    ['O', '_', 'O'],
                    ['_', '_', 'X']]
        legal_moves = [[2, 0], [1, 1], [2, 1]]
        X_or_O = 'O'
        result = find_corner(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(result, 'X')
        self.assertEqual(board_state, [['X', 'O', 'X'],
                    ['O', '_', 'O'],
                    ['O', '_', 'X']])

    def test_find_corner_valid_X(self):
        # Test ability to find corner move with 'X'
        board_state = [['X', 'O', 'X'],
                    ['O', '_', 'O'],
                    ['_', '_', 'X']]
        legal_moves = [[2, 0], [1, 1], [2, 1]]
        X_or_O = 'X'
        result = find_corner(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(result, 'O')
        self.assertEqual(board_state, [['X', 'O', 'X'],
                    ['O', '_', 'O'],
                    ['X', '_', 'X']])

    def test_find_corner_invalid_board(self):
        # Handle improper matrix
        board_state = [['X', 'O'],
                    ['O', 'X']]
        legal_moves = [[1, 0], [1, 1]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_corner(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [False])

    def test_find_corner_no_legal_moves(self):
        # Test ability to handle no legal moves
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['X', 'O', 'X']]
        legal_moves = []
        X_or_O = 'O'
        find_corner(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [False])

    def test_find_corner_move_made(self):
        # Test ability to not make second move
        move_made = [True]
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'X'
        result = find_corner(board_state, legal_moves, X_or_O, move_made)
        self.assertTrue(move_made == [True])
        self.assertEqual(result, None)

class TestFindSide(unittest.TestCase):

    """
    Test cases for find_side function
    """

    def setUp(self):
        # Set up tests where computer makes move
        self.move_made = [False]

    def test_find_side_valid_O(self):
        # Test ability to find side move with 'X'
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'O'
        result = find_side(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(result, 'X')
        self.assertEqual(board_state[2][1], 'O')

    def test_find_side_valid_X(self):
        # Test ability to find side move with 'X'
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'X'
        result = find_side(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [True])
        self.assertEqual(result, 'O')
        self.assertEqual(board_state[2][1], 'X')

    def test_find_side_invalid_board(self):
        # Handle improper matrix
        board_state = [['X', 'O'],
                    ['O', 'X']]
        legal_moves = [[1, 0], [1, 1]]
        X_or_O = 'O'
        with self.assertRaises(ValueError):
            find_side(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [False])

    def test_find_side_no_legal_moves(self):
        # Handle no legal moves
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['X', 'O', 'X']]
        legal_moves = []
        X_or_O = 'O'
        find_side(board_state, legal_moves, X_or_O, self.move_made)
        self.assertTrue(self.move_made == [False])

    def test_find_side_move_made(self):
        # Test ability not to make second move
        move_made = [True]
        board_state = [['X', 'O', 'X'],
                    ['O', 'X', 'O'],
                    ['_', '_', '_']]
        legal_moves = [[2, 0], [2, 1], [2, 2]]
        X_or_O = 'X'
        result = find_side(board_state, legal_moves, X_or_O, move_made)
        self.assertTrue(move_made == [True])
        self.assertEqual(result, None)

class TestNextMove(unittest.TestCase):

    """
    Test cases for next_move function
    """

    def setUp(self):
        # Set up tests where computer makes move
        self.move_made = [False]
        
    def test_next_move_drawn_game(self):
        # Test ability to detect full board with no win state
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['O', 'X', 'O']]
        result = next_move(board_state, 'X', 'X', self.move_made)
        self.assertFalse(result)
        self.assertEqual(board_state, [['X', 'O', 'X'],
                                       ['O', 'X', 'O'],
                                       ['O', 'X', 'O']])

    def test_next_move_winner_X(self):
        # Test ability to find win with 'X'
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['X', 'O', '_']]
        result = next_move(board_state, 'X', 'O', self.move_made)
        self.assertFalse(result)       
        self.assertTrue(self.move_made == [True]) 
        self.assertEqual(board_state, [['X', 'O', 'X'],
                                       ['O', 'X', 'O'],
                                       ['X', 'O', 'X']])
        
    @patch('builtins.input', side_effect = ['3 3'])
    def test_next_move_player_valid_X(self, mock_input):
        # Test ability to find win with 'X' by human
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['X', 'O', '_']]
        result = next_move(board_state, 'X', 'X', self.move_made)        
        self.assertFalse(result)

    @patch('builtins.input', side_effect = ['3 3'])
    def test_next_move_player_valid_O(self, mock_input):
        # Test ability to allow move by human with 'O'
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['X', 'O', '_']]
        result = next_move(board_state, 'O', 'O', self.move_made)        
        self.assertEqual(result, 'X')

    @patch('builtins.input', side_effect = ['3 4', '3 3'])
    def test_next_move_player_invalid_O(self, mock_input):
        # Handle player entering out of bounds square followed by proper move
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['X', 'O', '_']]
        result = next_move(board_state, 'O', 'O', self.move_made)        
        self.assertEqual(result, 'X')

    def test_next_move_block_O(self):
        # Test computer ability to block human win
        board_state = [['X', 'O', 'X'],
                       ['O', 'X', 'O'],
                       ['X', 'O', '_']]
        result = next_move(board_state, 'O', 'X', self.move_made)
        self.assertEqual(result, 'X')        
        self.assertEqual(board_state, [['X', 'O', 'X'],
                                       ['O', 'X', 'O'],
                                       ['X', 'O', 'O']])      
                    
if __name__ == '__main__':
    unittest.main()
