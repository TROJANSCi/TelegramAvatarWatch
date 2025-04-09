import json
from pathlib import Path
from typing import Optional, Any, Dict

from core.config import Configuration
from schemas import UserConfig

cfg = Configuration()


class User:

    def __init__(self) -> None:
        if cfg.user_config.is_file() is False:
            self.save_data({
                'locales': None,
                'tz': None,
                'theme': None,
                'encode': None
            })
        self._user = UserConfig(**self.data)

    @property
    def data(self) -> Dict[str, Any]:
        return json.loads(cfg.user_config.read_text(encoding='utf-8'))

    @property
    def theme(self) -> Path:
        theme_ = cfg.themes_path / self._user.theme
        if theme_.is_file():
            return theme_
        return cfg.themes_path / 'default.json'

    @theme.setter
    def theme(self, theme: Optional[Path]) -> None:
        to_save = self.data | {'theme': theme}
        self.save_data(data=to_save)
        self._user.theme = theme

    @property
    def locales(self) -> str:
        return self._user.locales

    @locales.setter
    def locales(self, locales: Optional[str]) -> None:
        to_save = self.data | {'locales': locales}
        self.save_data(data=to_save)
        self._user.locales = locales

    @property
    def encode(self) -> str:
        return self._user.encode

    @encode.setter
    def encode(self, encode: Optional[str]) -> None:
        to_save = self.data | {'encode': encode}
        self.save_data(data=to_save)
        self._user.encode = encode

    @property
    def tz(self) -> str:
        return self._user.tz

    @tz.setter
    def tz(self, tz: Optional[str]) -> None:
        to_save = self.data | {'tz': tz}
        self.save_data(data=to_save)
        self._user.tz = tz

    @classmethod
    def save_data(cls, data: dict[str, Any]) -> None:
        print('!!!', data)
        with open(cfg.user_config, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
