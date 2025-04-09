import locale
from io import BytesIO
from locale import setlocale, LC_ALL
from time import strftime
from datetime import datetime
from random import choice
from typing import Optional
from zoneinfo import ZoneInfo

from PIL import ImageFont, ImageDraw, Image

from schemas.theme_schema import Theme
from core.config import Configuration

cfg = Configuration()


class ImageCreator:
    background_now: str = None

    def __init__(
            self,
            tz: Optional[str],
            locales: Optional[str],
            theme: Optional[Theme],
            encoding: Optional[str] = 'utf-8'
    ) -> None:
        self._tz = ZoneInfo(tz) if tz else ZoneInfo('Asia/Tashkent')
        self._locales = locales if locales else 'ru_RU'
        self._theme = theme if theme else Theme()
        self._encoding = encoding or 'utf-8'
        setlocale(LC_ALL, self.locales)

    @property
    def tz(self) -> Optional[ZoneInfo]:
        return self._tz

    @tz.setter
    def tz(self, tz: Optional[str]) -> None:
        self._tz = ZoneInfo(tz)

    @property
    def locales(self) -> Optional[str]:
        return self._locales

    @locales.setter
    def locales(self, locales: Optional[str]) -> None:
        if locales:
            resolved = locale.locale_alias.get(locales.lower())
            if resolved:
                self._locales = resolved.split('.')[0]
            else:
                self._locales = locales  # оставить как есть
        else:
            self._locales = 'ru_RU'
        setlocale(LC_ALL, self._locales)

    @property
    def theme(self) -> Optional[Theme]:
        return self._theme

    @theme.setter
    def theme(self, theme: Optional[Theme]) -> None:
        self._theme = theme

    @property
    def encoding(self) -> Optional[str]:
        return self._encoding

    @encoding.setter
    def encoding(self, encoding: Optional[str]) -> None:
        self._encoding = encoding

    @property
    def background(self) -> str:
        background_ = (cfg.background_path / self.theme.background)
        if self.theme.background_behavior == 'sorted-next':
            sorted_background = sorted([bck.__str__() for bck in background_.iterdir() if bck.is_file()])
            if self.background_now is None:
                self.background_now = sorted_background[0]
                return sorted_background[0]
            else:
                idx = ((sorted_background.index(self.background_now) + 1) % len(sorted_background))
                self.background_now = sorted_background[idx]
                return sorted_background[idx]

        elif self.theme.background_behavior == 'random':
            bkg = choice([bck for bck in background_.iterdir() if bck.is_file() and bck != self.background_now])
            self.background_now = str(bkg)
            return bkg

        else:
            return background_.__str__() if background_.is_file() else background_.iterdir().__next__()

    def data_to_string(self) -> str:
        return strftime(self.theme.date_format)

    def time_to_string(self) -> str:
        return datetime.now(tz=self.tz).replace(tzinfo=None).strftime('%H:%M')

    def img_generator(self, preview: Optional[bool] = False):
        time_ = self.time_to_string()
        font1 = ImageFont.truetype(font=cfg.fonts_path / self.theme.font1, size=self.theme.font1_size)

        background = Image.open(self.background).convert('RGBA')
        draw = ImageDraw.Draw(background)
        W, H = background.size
        bbox = draw.textbbox((0, 0), time_, font=font1)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((W - w) / 2 + self.theme.left_margin,
                   (H - h) / 2 + self.theme.top_margin),
                  text=time_,
                  font=font1,
                  fill=self.theme.font1_color)

        if self.theme.add_date:
            font = (cfg.fonts_path / self.theme.font2) if self.theme.font2 else (cfg.fonts_path / self.theme.font1)
            font2 = ImageFont.truetype(font=font, size=self.theme.font2_size or self.theme.font1_size)
            date_ = self.data_to_string()
            bbox = draw.textbbox((0, 0), date_, font=font2)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((W - w) / 2 + self.theme.left_margin,
                       (H - h) / 2 + self.theme.top_margin + (H // 3)),
                      text=date_,
                      font=font2,
                      fill=self.theme.font2_color)

        img_byte_arr = BytesIO()
        background.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        if preview:
            background.show()

        return img_byte_arr
