from unittest import TestCase

from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class BoggleTests(TestCase):
    """Test the boggle game functions."""

    @classmethod
    def setUpClass(cls):
        print("Inside Set Up Class")
        cls.test_game = Boggle()
        cls.words = "words.txt"
        cls.dict = cls.test_game.read_dict(cls.words)
        cls.board = cls.test_game.make_board()
        cls.fixed_board = [
            ['Y', 'K', 'E', 'D', 'H'], 
            ['Z', 'D', 'B', 'B', 'T'], 
            ['B', 'S', 'P', 'X', 'Z'], 
            ['X', 'K', 'R', 'R', 'F'], 
            ['R', 'X', 'B', 'U', 'Y'],
        ]

    @classmethod
    def tearDownClass(cls):
        print("Inside Tear Down Class")
        cls.fixed_board = []
        cls.board = []
        cls.test_game = []
        cls.dict = []

    def test_read_dict(self):
        """Read the words.txt file and test for existence of 'hello'"""
        self.assertIn('hello', self.dict)

    def test_make_board(self):
        """Test that a board is created"""
        
        self.assertEqual(len(self.board), 5)
        
        for i in self.board:
            # Check that each row has 5 elements
            self.assertEqual(len(i), 5)
            # Check that each row has is list type
            self.assertTrue(isinstance(i, list))
            for j in i:
                # Check that each item in board is a string
                self.assertTrue(isinstance(j, str))
                self.assertFalse(isinstance(j, int))

    def test_check_valid_word(self):
        """Test check_valid_word function on fixed_board"""
        
        board = self.fixed_board
        self.assertEqual(self.test_game.check_valid_word(board, "bed"), "ok")
        self.assertEqual(self.test_game.check_valid_word(board, "fur"), "ok")
        self.assertEqual(self.test_game.check_valid_word(board, "hello"), "not-on-board")
        self.assertEqual(self.test_game.check_valid_word(board, "sadfasva"), "not-word")
