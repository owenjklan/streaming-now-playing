#!/usr/bin/env python3
import base64
import json
from pathlib import Path

import click
from flask import Flask, render_template, request, url_for
from flask_socketio import SocketIO, emit

from game_detail import GameDetail
from search import send_search, download_game_image, extract_full_case_image

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

NULL_GAME = {
    "game_title": "No current game has been set",
    "game_platform": "",
    "game_region": "",
    "image_path": None
}

current_game = GameDetail.from_dict(NULL_GAME)

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
                results=search_results,
                results_css=url_for('static', filename='search/results.css'),
                update_url=url_for('update'),
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
    """
    The parameters necessary to download the full game case image
    are provided in the payload. The payload is in the correct
    format to send to the client mostly unmodified. The modifications
    we do make are essentially setting the image data after the
    case image has been downloaded.
    """
    global current_game
    decoded_parameters = request.json

    # We need to extract the full case image from the game
    # details page and save it to disk.
    game_case_url = extract_full_case_image(decoded_parameters["game_page_url"])
    game_case_path = download_game_image(
        game_case_url,
        decoded_parameters["game_title"],
        decoded_parameters["game_platform"],
        decoded_parameters["game_region"]
    )
    decoded_parameters["image_path"] = game_case_path

    new_game = GameDetail.from_dict(decoded_parameters)
    socketio.emit('server', new_game.to_dict())
    current_game = new_game
    return "OK Game updated"

# Dashboard routes
@app.route('/dashboard')
def dashboard():
    dashboard_js_url = url_for('static', filename='dashboard/dashboard.js')
    dashboard_css_url = url_for('static', filename='dashboard/dashboard.css')
    search_js_url = url_for('static', filename='search/search.js')
    print("Dashboard JS URL:", dashboard_js_url)
    return render_template(
        'dashboard/dashboard.html',
        dashboard_js=dashboard_js_url,
        dashboard_css=dashboard_css_url,
        search_js=search_js_url,
    )


# Widget-handling routes etc
@app.route('/widget')
def main():
    return render_template('widget/widget.html')


@socketio.on('connect')
def widget_connect():
    emit('server', current_game.to_dict())


@click.command()
@click.option("--port", "-p", "port", type=int, default=22222)
@click.option("--bind-ip", "-b", "bind_ip", type=str, default="0.0.0.0")
@click.option("--debug", "-D", "debug_flag", is_flag=True)
def main(bind_ip: str, port: int, debug_flag: bool):
    socketio.run(app, host=bind_ip, port=port, debug=debug_flag)


if __name__ == '__main__':
    main()
