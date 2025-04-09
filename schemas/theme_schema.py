from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class Theme:
    font1: Optional[str] = field(default='DigitalNumbers-Regular.ttf')
    font1_size: Optional[float] = field(default=100)
    font1_color: Optional[tuple | str] = field(default='#169e4d')

    font2: Optional[str] = field(default='DejaVuSansMono.ttf')
    font2_size: Optional[float] = field(default=18)
    font2_color: Optional[tuple | str] = field(default='#ffffff')

    add_date: Optional[bool] = field(default=False)
    date_format: Optional[str] = field(default='%a, %d %B')

    background: Optional[str] = field(default='default.png')
    background_behavior: Literal['static', 'sorted-next', 'random'] = field(default='static')

    top_margin: Optional[float] = field(default=0)
    bottom_margin: Optional[float] = field(default=0)
    left_margin: Optional[float] = field(default=0)
    right_margin: Optional[float] = field(default=0)
