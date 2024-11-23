#!/usr/bin/env python3
import base64
import json
from pathlib import Path

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from src.game_detail import GameDetail
from src.search import send_search

HTML_BASE_DIR = Path(__file__).resolve().parent / 'html'
WIDGET_BASE_DIR = HTML_BASE_DIR / 'widget'
SEARCH_BASE_DIR = HTML_BASE_DIR / 'search'
print(f"HTML source base directory: {HTML_BASE_DIR}")

app = Flask(
    __name__,
    static_folder=HTML_BASE_DIR,
    template_folder=HTML_BASE_DIR,
)
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')

TEST_DATA = {
    "game_title": "Test Game With a Rather Long Title",
    "game_platform": "TurboGrafx 16",
    "game_region": "Australian Exclusive",
    "image_path": WIDGET_BASE_DIR / 'sega-rally-cd.jpg',
}

test_game = GameDetail.from_dict(TEST_DATA)

# Search handling
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        # age = request.form['age']
        # return render_template('age.html',age=age)
        search_args = request.form.to_dict()
        print(json.dumps(search_args, indent=4))
        search_results = send_search(search_args)
        return (
            render_template(
                'search/results.html',
                results=search_results
            )
        )
    elif request.method == 'GET':
        return render_template('search/search.html')
    else:
        pass  # Flask should have rejected unsupported methods

    return "OK"

# Update the widget with new details
@app.route("/update", methods=["POST"])
def update():
    update_params = request.form.to_dict()
    # print(json.dumps(update_params, indent=4))
    decoded_parameters = json.loads(base64.b64decode(update_params["update_params"]).decode("utf-8"))
    # # print(decoded_parameters)
    # print(json.dumps(decoded_parameters, indent=4))

    new_game = GameDetail.from_dict(decoded_parameters)
    emit('server', new_game.to_dict())
    return "OK Game updated"

# Widget-handling routes etc
@app.route('/widget')
def main():
    return render_template('widget/widget.html')


@socketio.on('connect')
def widget_connect():
    emit('server', test_game.to_dict())


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=22222, debug=True)
