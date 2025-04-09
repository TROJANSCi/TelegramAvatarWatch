from dataclasses import dataclass
from pathlib import Path


@dataclass
class UserConfig:
    theme: Path
    locales: str
    tz: str
    encode: str
