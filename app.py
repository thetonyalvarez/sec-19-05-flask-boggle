import json

from flask import Flask, request, render_template, redirect, session, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)

app.config['SECRET_KEY'] = "8dsvasva9sdv"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

FOUNDWORDS = []


@app.route('/')
def show_index():
    """redirect index to /game"""
    if 'size' in session:
        session.pop('size')
    
    return render_template('set-board-size.html')

@app.route('/set-board-size', methods=['GET','POST'])
def set_board_size():
    
    if request.method == 'POST':

        size = int(request.form['size'])
        session['size'] = size

        global boggle_game
        boggle_game = Boggle(session['size'])
        session['board'] = boggle_game.make_board()
        
        return redirect('/game')

    else:
        return redirect("/")



@app.route('/game')
def show_game():
    """Render new game"""
    
    if 'size' not in session:
        return redirect("/")

    session['found_words'] = []
    FOUNDWORDS = []

    return render_template('game.html', board=session['board'], size=session['size'])



@app.route('/user-guess', methods=['GET', 'POST'])
def handle_guess():
    """Handle user's word guess"""
    
    if 'size' not in session:
        return redirect("/")
    
    # get guess from form
    resp = request.json['guess']
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
        return jsonify({
            "result": check,
            "resp": {
                "found_words": session['found_words'],
                "last_searched_word": resp

            },
        })

@app.route('/game-over', methods=['GET', 'POST'])
def game_over():
    """End the game and clear out necessary session keys"""
    
    if 'size' not in session:
        return redirect("/")
    
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
    """Handle restart game button and clear out board with new instance of game"""
    session.pop('board')

    return redirect('/')