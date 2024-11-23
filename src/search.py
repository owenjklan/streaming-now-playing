import base64
import json
import os
from encodings.base64_codec import base64_encode

import requests
from lxml.html import fromstring

DOWNLOADS_BASE_DIR = "/home/owen/game_case_thumbs"


def download_game_image(url: str, title: str, platform: str, region: str) -> bool:
    title = (title.lower()
             .replace(" ", "_")
             .replace("-", "_")
             .replace(".", "_")
             )
    extension = url.split(".")[-1]
    game_file_slug = (f"{title}_{platform}_{region}.{extension}").lower()
    response = requests.get(url)
    full_path = os.path.join(DOWNLOADS_BASE_DIR, game_file_slug)
    with open(full_path, "wb") as f:
        f.write(response.content)
        print(f"Downloaded to {full_path}")
    return full_path


def send_search(search_params: dict) -> None:
    URL = "https://cdromance.org"
    search_params["s"] = search_params.pop("title")
    response = requests.get(URL, params=search_params)

    page_tree = fromstring(response.text)
    game_elements = page_tree.xpath("//div[@class='game-container']")

    returned_elements = []

    for game in game_elements:
        game_thumb = game.xpath(".//img/@src")[0]
        game_title = game.xpath(".//div[@class='game-title']")[0].text_content()
        game_region = str(game.xpath(".//div[@class='region']/@title")[0]).removeprefix('Region').strip()
        game_platform = game.xpath(".//div[contains(@class, 'console')]")[0].text_content()

        element = {
            "game_title": game_title,
            "game_region": game_region,
            "game_platform": game_platform,
            "thumbnail": game_thumb
        }

        thumbnail_path = download_game_image(
            game_thumb,
            game_title,
            game_platform,
            game_region
        )
        element["image_path"] = thumbnail_path
        print("PRE-ENCODED PARAMS:")
        print(json.dumps(element, indent=4))
        element["encoded"] = base64.b64encode(bytes(json.dumps(element), "utf-8")).decode("utf-8")
        print("ENCODED PARAMS:")
        print(json.dumps(element, indent=4))
        returned_elements.append(element)

    return returned_elements