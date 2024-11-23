import base64
import io
from pathlib import Path
from typing import Optional

from PIL import Image
import magic

GAME_CASE_IMAGE_HEIGHT = 150

class GameDetail(object):
    def __init__(
            self,
            game_title: str,
            game_platform: str = None,
            game_region: str = None,
            image_path: Optional[str | Path] = None,
    ) -> None:
        self.game_title = game_title
        self.game_region = game_region
        self.game_platform = game_platform

        # TODO: Remove the encoded knowledge of where to find the fallback image
        self._dummy_image_type = "image/png"
        self._dummy_image_path = Path(__file__).resolve(strict=True).parent.parent / "widget" / "dummy_image.png"
        self.image_path = image_path if image_path is not None else self._dummy_image_path
        self.image_type = magic.from_file(image_path, mime=True) if image_path is not None else self._dummy_image_type
        self.image_data = self._load_image_data()

    @classmethod
    def from_dict(cls, data):
        return GameDetail(
            data['game_title'],
            data.get('game_platform', None),
            data.get('game_region', None),
            data.get('image_path', None),
        )

    def _load_image_data(self) -> str:
        """
        This helper will load the supplied image (or the dummy image
        if image_path was None) and base64 encodes the data to
        be sent to the widget as a Data URL.
        """
        # Create a thumbnail that fits to 150x150, keeping aspect ratio
        image = Image.open(self.image_path)
        image.thumbnail(
            (GAME_CASE_IMAGE_HEIGHT, GAME_CASE_IMAGE_HEIGHT),
            Image.Resampling.LANCZOS
        )

        thumbnail_width, thumbnail_height = image.size
        # calculate new pos
        x = (GAME_CASE_IMAGE_HEIGHT - thumbnail_width) // 2
        y = (GAME_CASE_IMAGE_HEIGHT - thumbnail_height) // 2

        image_canvas = Image.new(image.mode, (GAME_CASE_IMAGE_HEIGHT, GAME_CASE_IMAGE_HEIGHT))
        image_canvas.paste(image, (x, y))
        image_bytes = io.BytesIO()
        image_canvas.save(image_bytes, format="PNG")
        encoded_string = base64.b64encode(
            image_bytes.getvalue()
        ).decode("utf-8")

        return f"data:image/png;base64,{encoded_string}"

    def to_dict(self):
        return {
            'game_title': self.game_title,
            'game_platform': self.game_platform,
            'game_region': self.game_region,
            'image_data': self.image_data,
        }
