# from unittest import TestCase
# from app import app
# from flask import session
# from boggle import Boggle

# app.config['TESTING'] = True
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# class UnitTests(TestCase):


# class FlaskTests(TestCase):

#     # TODO -- write tests for every view function / feature!

#     def test_guess_form(self):
#         with app.test_client() as client:
            
#             res = client.get('/game')
#             html = res.get_data(as_text=True)

#             self.assertEqual(res.status_code, 200)
#             self.assertIn("form", html)
    
#     # def test_guess_submit(self):
#     #     with app.test_client() as client:
#     #         data = {'guess': 'orange'}
#     #         res = client.post('/user-guess', data=data)
#     #         # html = res.get_data(as_text=True)
#     #         import pdb
#     #         pdb.set_trace()
#     #         self.assertEqual(res.status_code, 200)
#     #         # self.assertIn("", html)

#     # def test_redirection(self):
#     #     with app.test_client() as client:
#     #         res = client.get('/')

#     # def test_redirection_followed(self):