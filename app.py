from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = "secret_pixel_key"

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'secret_number' not in session:
        reset_game()

    message = "Guess a number between 1 and 100!"
    game_over = False

    if request.method == 'POST':
        guess = int(request.form['guess'])
        session['attempts'] += 1
        
        if guess < session['secret_number']:
            message = "Too low! ⬆️"
        elif guess > session['secret_number']:
            message = "Too high! ⬇️"
        else:
            message = f"Correct! You found it in {session['attempts']} attempt(s)! 🎉"
            game_over = True
            
        if session['attempts'] >= 7 and not game_over:
            message = f"Game Over! The number was {session['secret_number']}. 💀"
            game_over = True

    return render_template('index.html', message=message, attempts=session['attempts'], game_over=game_over)

@app.route('/reset')
def reset():
    reset_game()
    return render_template('index.html', message="New game started! Guess between 1 and 100.", attempts=0, game_over=False)

def reset_game():
    session['secret_number'] = random.randint(1, 100)
    session['attempts'] = 0

if __name__ == '__main__':
    app.run(debug=True)