import os
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw

TEMPLATE_PATH = os.path.join('image', 'ticket_template.png')
FONT_PATH = 'files/ofont_ru_DSEraser2.ttf'
FONT_SIZE = 15
BLACK = (0, 0, 0, 255)
SURAME_OFFSET = (50, 120)
NAME_OFFSET = (115, 120)
SITY_OF_DEPARTYRE_OFFSET = (45, 190)
SITY_OF_ARRIVAL_OFFSET = (45, 255)
DATA_OFFSET = (275, 255)


def generate_ticket(name, surname, sity_of_departyre, sity_of_arrival, selected_flight_date):
    base = Image.open(TEMPLATE_PATH).convert('RGBA')
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(base)
    draw.text(SURAME_OFFSET, surname, font=font, fill=BLACK)
    draw.text(NAME_OFFSET, name, font=font, fill=BLACK)
    draw.text(SITY_OF_DEPARTYRE_OFFSET, sity_of_departyre, font=font, fill=BLACK)
    draw.text(SITY_OF_ARRIVAL_OFFSET, sity_of_arrival, font=font, fill=BLACK)
    draw.text(DATA_OFFSET, selected_flight_date, font=font, fill=BLACK)
    temp_file = BytesIO()
    base.save(temp_file, 'png')
    temp_file.seek(0)
    return temp_file

# a = generate_ticket('Yuri', 'Penkov', 'Санкт-Петербург', 'Пхукет', '05-12-2022')

