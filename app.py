from flask import Flask, render_template, request, session, redirect, url_for
from game.engine import GameEngine
from game import display
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'

def get_engine():
    if 'engine' not in session:
        engine = GameEngine()
        session['engine'] = engine.to_dict()
    else:
        engine = GameEngine.from_dict(session['engine'])
    return engine

def save_engine(engine):
    session['engine'] = engine.to_dict()

@app.route('/', methods=['GET', 'POST'])
def play_game():
    engine = get_engine()

    if request.method == 'POST':
        action = request.form.get('action', '').upper()

        if action == 'EXIT':
            session.clear()
            return redirect(url_for('play_game'))

        if action == 'REVEAL':
            engine.reveal_all()
            
        elif action in ['U', 'D', 'L', 'R']:
            engine.move(action)

        save_engine(engine)


    map_text = display.render_map(grid=engine.grid,player_pos=engine.player_pos,seen=engine.seen,footsteps=engine.footsteps,reveal_temp=engine.reveal_temp)
    return render_template('game.html', engine=engine,map_text=map_text,message=engine.msg)


if __name__ == '__main__':
    app.run(debug=True)
