import io
import os
import urllib.request
import zipfile

import dropbox
import numpy
import wand.drawing
import wand.font
import wand.image
from PIL import Image, ImageDraw, ImageFont
from transliterate import translit

from cards.templates.card_templates import _card_templates, _CardUserRole
from config import card_airtable


def check_artifacts():
    """Проверить и загрузить все артефакты для карточек"""
    
    artifacts_path = 'artifacts'
    artifacts_url = os.getenv('STORAGE_URL')
    artifacts_file_name = 'artifacts.zip'
        
    def download_artifacts():
        print('Загрузка артефактов...')
        urllib.request.urlretrieve(artifacts_url, artifacts_file_name)
        print('Распаковка артефактов...')
        with zipfile.ZipFile(artifacts_file_name, 'r') as zip_ref:
            zip_ref.extractall(f'{os.getcwd()}/{artifacts_path}')
    
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 2 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 2 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))
    
    # download_artifacts()
    if not os.path.isdir(artifacts_path):
        print('По API')
    else:
        print('Проверка наличия изменений...')
        
        # dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'), scope=['files.metadata.read'])
        # dbx_backgroud_image_folder = dbx.files_list_folder('/card/backgroud_image').entries
        # dbx_font_folder = dbx.files_list_folder('/card/font').entries
        
        # print(dbx_backgroud_image_folder)
        # print(dbx_font_folder)
        
        print(list_files(f'{os.getcwd()}/{artifacts_path}'))
        
        # сравнение различий по названию и размеру файла
        
    print('Артефакты готовы')

# TODO: Изменить работу с шаблонами на HTML → image с помощью imgkit или pyppeteer (будет ли работать на сервере?)
# https://stackoverflow.com/questions/60598837/html-to-image-using-python
class Card:
    ROLE = _CardUserRole
    
    def __init__(self, user, role, card_issued_date, level) -> None:
        self.role = role
        self.card_issued_date = card_issued_date
        self.level = level
        self.user = user
        
        self.font_color = _card_templates[self.role]['font_color']
        self.position_full_name = _card_templates[self.role]['position_full_name']
        self.position_role = _card_templates[self.role]['position_role']
        self.position_card_issued_date = _card_templates[self.role]['position_card_issued_date']
        self.position_user_id = _card_templates[self.role]['position_user_id']
        self.position_level = _card_templates[self.role]['position_level']
    
    @staticmethod
    def get_filled_without_image():
        records = card_airtable.get_all(formula="AND({image}='', {is_filled}=TRUE())")
        return records
    
    @staticmethod
    def upload_image(record_id, image_url):
        fields = {
            'image': [{
                'url': image_url
            }]
        }
        res = card_airtable.update(record_id, fields)
        print('res', res)
        
    def generate(self) -> Image:
        full_name = translit(f'{self.user.name.upper()} {self.user.surname.upper()}', 'ru', reversed=True)
        
        role = self.role.upper()
        card_issued_date = 'issued: ' + self.card_issued_date
        user_id = f'{str(self.user.id)}'
        level = str(self.level)
        
        cards_bg_path = 'artifacts/card/background_image'
        cards_font_path = 'artifacts/card/font'
        
        background = Image.open(f'{cards_bg_path}/card_{self.role}_v1.png')
        
        font_color = self.font_color
        position_full_name = self.position_full_name
        position_role = self.position_role
        position_card_issued_date = self.position_card_issued_date
        position_user_id = self.position_user_id
        position_level = self.position_level
        
        
        draw = ImageDraw.Draw(background)
        
        font_futura_bold = ImageFont.truetype(f'{cards_font_path}/futura_bold.ttf', 186)
        draw.text(position_role, role, font_color, font=font_futura_bold)
        
        font_avenir_next = ImageFont.truetype(f'{cards_font_path}/avenir_next_regular.ttf', 64)
        draw.text(position_card_issued_date, card_issued_date, font_color, font=font_avenir_next)
        
        font_futura_normal = ImageFont.truetype(f'{cards_font_path}/futura_normal.ttf', 110)
        draw.text(position_user_id, user_id, font_color, font=font_futura_normal)
        
        font_futura_bold = ImageFont.truetype(f'{cards_font_path}/futura_bold.ttf', 218)
        draw.text(position_level, level, font_color, font=font_futura_bold)
        
        # Create a black canvas 400x120
        with wand.image.Image(width=3047, height=1913, pseudo='xc:transparent') as image:
            with wand.drawing.Drawing() as draw2:
                # Draw once in yellow with positive kerning
                draw2.font_size = 130
                draw2.font = f'{cards_font_path}/futura_normal.ttf'
                print('##', draw2.font)
                draw2.fill_color = font_color
                draw2.text_kerning = 10.0
                draw2.text(position_full_name[0], position_full_name[1]+108, full_name)
                draw2(image)
            
            # wand.Image to pillow.Image
            mb = image.make_blob(format='png')
            ba = bytearray(mb)
            img_buffer = numpy.asarray(ba, dtype='uint8')
            bytes_io = io.BytesIO(img_buffer)
            pil_img = Image.open(bytes_io)
        
        # ImageDraw.Draw(pil_img)
        # bg = Image.new()
        # bg.paste()
        # print(type(im.getcolors()))
        # print(type(pil_img))
        # print(pil_img.size)
        # print(background.size)
        
        # pil_img.show()
        # background.show()
        out = Image.alpha_composite(background.convert('RGBA'), pil_img.convert('RGBA'))
        
        
        # out.show()
        # out.save(f'tmp/{user.role}.png')
        return out
