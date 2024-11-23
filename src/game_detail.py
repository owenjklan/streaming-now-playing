from pathlib import Path
from typing import Optional


class GameDetail(object):
    def __init__(
            self,
            game_title: str,
            game_platform: str = None,
            game_region: str = None,
            image_path: Optional[str | Path] = None,
    ) -> None:
        self.image_data = image_path
        self.image_path = None
        self.game_title = game_title
        self.game_region = game_region
        self.game_platform = game_platform

    @classmethod
    def from_dict(cls, data):
        return GameDetail(
            data['game_title'],
            data.get('game_platform', None),
            data.get('game_region', None),
            data.get('image_path', None),
        )

    def to_dict(self):
        return {
            'game_title': self.game_title,
            'game_platform': self.game_platform,
            'game_region': self.game_region,
            'image_path': self.image_path,
        }
