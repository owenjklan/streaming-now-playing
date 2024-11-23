import base64
import json
import os

import magic
from encodings.base64_codec import base64_encode

import requests
from lxml.html import fromstring

DOWNLOADS_BASE_DIR = "/home/owen/game_case_thumbs"


def extract_full_case_image(game_url: str) -> str:
    """
    This takes the URL from a search result, loads it then
    pulls the full case image from the site, saving it
    locally.
    """
    response = requests.get(game_url)

    page_tree = fromstring(response.text)
    game_case_url = page_tree.xpath("//div[@class='post-thumbnail']/img/@src")[0]
    print("Game case URL:", game_case_url)

    return game_case_url


def download_game_thumbnail(url: str) -> str:
    """
    Download an image (a thumbnail for our current purposes)
    from the supplied URL and encode it into a Data URL.
    """
    response = requests.get(url)
    b64_image_data = base64.b64encode(response.content).decode("utf-8")

    # Determine the mime type of the source image
    image_mime_type = magic.from_buffer(response.content, mime=True)

    return f"data:{image_mime_type};base64,{b64_image_data}"


def download_game_image(
        url: str, title: str, platform: str, region: str
) -> bool:
    """
    This will download an image, save it to disk and return the
    path to that file on disk.
    """
    # sanitise the title text to be filesystem-safe
    title = (title.lower()
             .replace(" ", "_")
             .replace("-", "_")
             .replace(".", "_")
             )
    extension = url.split(".")[-1]
    game_file_slug = (f"{title}_{platform}_{region}.{extension}").lower()

    # Get the image from the URL
    response = requests.get(url)

    # Save the downloaded image to disk
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

        # This will be used to inspect the game details of the selected
        # result to download the full game case image. Otherwise, we
        # just supply the thumbnails to the results page.
        game_page_url = game.xpath(".//a/@href")[1]  # TODO: This isn't the most robust

        # This will be encoded and supplied via a hidden field form
        # so the update endpoint can use it directly to send to the
        # websocket client to perform the actual update
        element = {
            "game_title": game_title,
            "game_region": game_region,
            "game_platform": game_platform,
            "game_page_url": game_page_url
        }

        thumbnail_data_url = download_game_thumbnail(
            game_thumb,
        )
        element["thumbnail_data_url"] = thumbnail_data_url
        element["encoded"] = base64.b64encode(bytes(json.dumps(element), "utf-8")).decode("utf-8")
        print("Search result JSON:", json.dumps(element, indent=4))
        returned_elements.append(element)

    return returned_elements