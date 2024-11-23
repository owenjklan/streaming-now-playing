#!/usr/bin/env python3
from pathlib import Path

from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from src.game_detail import GameDetail

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


@app.route('/widget')
def main():
    return render_template('widget/widget.html')


@socketio.on('connect')
def widget_connect():
    emit('server', test_game.to_dict())


if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=22222, debug=True)
