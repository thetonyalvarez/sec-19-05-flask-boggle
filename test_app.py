import json

from app import app
from flask import session
from unittest import TestCase
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!
    @classmethod
    def setUpClass(cls):
        print("Inside setUpClass")
        cls.size = 5
        cls.board = [
            ['Y', 'K', 'E', 'D', 'H'], 
            ['Z', 'D', 'B', 'B', 'T'], 
            ['B', 'S', 'P', 'X', 'Z'], 
            ['X', 'K', 'R', 'R', 'F'], 
            ['R', 'X', 'B', 'U', 'Y'],
        ],
        cls.guess = "fur"
        cls.boggle_game = Boggle(cls.size)

    @classmethod    
    def tearDownClass(cls):
        print("Inside tearDownClass")

    def test_start_page(self):
        """Test that the start page is rendered"""
        with app.test_client() as client:

            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("What size board", html)

    def test_size_form_post(self):
        """Test whether the post request redirects to /game URL"""
        with app.test_client() as client:

            data = {'size': self.size}
            res = client.post('/set-board-size', data=data)
            
            self.assertEqual(res.status_code, 302)
            self.assertIn("/game", res.location)

    def test_size_form_get(self):
        """Test whether the get request redirects to '/' URL"""
        with app.test_client() as client:

            res = client.get('/set-board-size')

            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_game_page_redirect_if_no_size(self):
        """Tests if '/game' redirects back to home if no session['size']"""
        with app.test_client() as client:

            res = client.get('/game')
            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_game_page_render(self):
        """Test if /game is rendered when prop session['size'] exists"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['size'] = self.size
                change_session['board'] = self.board
            
            res = client.get('/game')
            
            html = res.get_data(as_text=True)
            
            self.assertIn("board-row", html)

    def test_user_guess_redirect_if_get(self):
        """Test that page redirects to home if user tries GET request"""
        with app.test_client() as client:

            res = client.get('/user-guess')
            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")


    # TODO: Error when posting data to url. Need to patch
    def test_user_guess_json_response(self):
        """Test that response is json"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['size'] = self.size
                change_session['board'] = self.boggle_game.set_board(self.board)
                
            data = {
                'guess': self.guess,
                'board': self.boggle_game.set_board(self.board)
            }

            print("SELF.BOARD", self.board)
            print("SESSION BOARD" , self.boggle_game.set_board(self.board))
            
            res = client.post('/user-guess', json=data)
            
    def test_game_over(self):
        """Test that game_over returns json data."""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['games_played'] = 121
                change_session['size'] = self.size
                change_session['high_score'] = 1

            data = {
                "finalScore": 10, 
                "size": self.size,
                "high_score": 1,
            }
            res = client.post('/game-over', json=data)

            self.assertEqual(res.get_json()['games_played'], 122)
            self.assertEqual(res.get_json()['high_score'], 10)
            
    def test_game_over_redirect(self):
        """Test redirect status code if someone visits /game-over without completing game."""
        with app.test_client() as client:
            
            res = client.get('/game-over')
            
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, "http://localhost/")

    def test_game_over_redirect_follow(self):
        """Test redirect follow if someone visits /game-over without completing game."""
        with app.test_client() as client:
            
            res = client.get('/game-over', follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
            
    def test_restart_redirect(self):
        """Test that board is cleared out and is redirected to index"""
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = self.board
                
            res = client.get('/restart', follow_redirects=True)
            
            self.assertEqual(res.status_code, 200)
