from pathlib import Path
from dataclasses import dataclass


@dataclass
class Configuration:
    app_path: Path = Path(__file__).parent.parent
    fonts_path: Path = app_path / 'fonts'
    themes_path: Path = app_path / 'themes'
    background_path: Path = app_path / 'background'
