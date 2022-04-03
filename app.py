import json

from flask import Flask, request, render_template, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = "8dsvasva9sdv"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

FOUNDWORDS = []

board = boggle_game.make_board()


@app.route('/')
def show_index():
    session['board'] = board
    
    return redirect('/game')


@app.route('/game')
def show_game():
    size = len(board)
    session['found_words'] = []
    FOUNDWORDS = []
    

    
    return render_template('game.html', board=session['board'], size=size)



@app.route('/user-guess', methods=['POST'])
def handle_guess():
    
    print(session['found_words'])

    # get guess from form
    resp = json.loads(request.data)['guess']
    check = boggle_game.check_valid_word(session['board'], resp)

    if check == "ok" and resp not in FOUNDWORDS:
        # create a session key to store set of found words
        FOUNDWORDS.append(resp)
        session['found_words'] = FOUNDWORDS

        return jsonify({
            "result":"ok",
            "resp": {
                "found_words": session['found_words'],
                "last_searched_word": resp

            },
        })

    else:
        print(check, session['found_words'], resp)
        
        return jsonify({
            "result": check,
            "resp": {
                "found_words": session['found_words'],
                "last_searched_word": resp

            },
        })

@app.route('/game-over', methods=['POST'])
def game_over():
    session.pop('found_words', None)
    global FOUNDWORDS
    FOUNDWORDS = []
    
    session['games_played'] = session.get('games_played', 0) + 1

    score = request.json['finalScore']
    
    if score > session['high_score']:
        session['high_score'] = score
    
    return jsonify({
        "high_score": session['high_score'],
        "games_played": session['games_played']
    })

@app.route('/restart')
def restart_game():
    session.pop('board')
    
    new_boggle_game = Boggle()
    board = new_boggle_game.make_board()
    session['board'] = board

    return redirect('/game')