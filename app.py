from schemas.theme_schema import Theme
from utils.utils import ImageCreator

ic = ImageCreator(tz='Asia/Tashkent', locales='ru_RU', theme=Theme(
    # font1='DigitalNumbers-Regular.ttf',
    # font1_size=100,
    # font1_color='#169e4d',
    # add_date=False,
    # # background='logite_soft.png',
    # background_behavior='static',
    # top_margin=-15
)
                  )
ic.img_generator(preview=True)
