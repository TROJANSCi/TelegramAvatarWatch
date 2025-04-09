from schemas.theme_schema import Theme
from utils.utils import ImageCreator

ic = ImageCreator(tz='Asia/Tashkent', locales='ru_RU', theme=Theme(
    font1='StickNoBills-ExtraBold.ttf',
    font1_size=180,
    font1_color='#ffffff',
    add_date=False,
    background='logite_soft.png',
    background_behavior='static',
    top_margin=-90
)
                  )
ic.img_generator(preview=True)
