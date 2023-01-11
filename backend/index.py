
import io
import json
import os
import re
from datetime import datetime
from time import sleep
from urllib import request

import dropbox
from dropbox.files import WriteMode

from card import Card, check_artifacts
from config import card_airtable
from user import User

# TODO: Поправить архитектуру проекта
# D:\OpenLongevity\community\base_layers\card_boss_v1.png
# D:\OpenLongevity\community\backend\base_layers

def check_and_generate_cards():
    # 1. Получить записи карточек которые не сгенерированы и которые отмечены заполненными
    # User.get_all({'image': []})
    card_records_without_images = Card.get_filled_without_image()
    
    print(card_records_without_images)
    cards = []
    for card_record in card_records_without_images:
        card_fields = card_record['fields']
        name_card_fields = set(card_fields)
        name_card_fields_require = set(['card_issued_date', 'level', 'uuid', 'user_uuid', 'role'])
        
        # Проверить необходимые поля из таблицы `card`
        # print('i1', len(name_card_fields.intersection(name_card_fields_require)))
        # print('i1', len(name_card_fields_require))
        if len(name_card_fields.intersection(name_card_fields_require)) == len(name_card_fields_require):
            user_uuid = card_fields['user_uuid'][0]
            user_record = User.get_one(user_uuid)
            user_fields = user_record['fields']
            name_user_fields = set(user_fields)
            name_user_fields_require = set(['uuid', 'id', 'name', 'surname'])
            
            # Проверить необходимые поля из таблицы `user`
            # print('i2', name_user_fields.intersection(name_user_fields_require))
            if len(name_user_fields.intersection(name_user_fields_require)) == len(name_user_fields_require):
                # print('uf', user_fields)
                user = User(id=user_fields['id'], name=user_fields['name'], surname=user_fields['surname'])
                card = Card(user, role=card_fields['role'], card_issued_date=card_fields['card_issued_date'], level=card_fields['level'])
                
                image = card.generate()
                
                # !не сохраняя файл на диск
                # image_file = io.BytesIO()
                # image.save(image_file, "JPEG")
                # image_file.seek(0)
                
                image_path = f'{card.role}.jpg'
                image.convert(mode='RGB').save(image_path, format='JPEG', optimize=True, quality=95)
                
                # Загружаем изображение в хранилище с общедоступным url
                dbx = dropbox.Dropbox(os.getenv('DROPBOX_ACCESS_TOKEN'), scope=['files.metadata.read', 'files.content.read', 'files.content.write'])
                r = 0
                with open(image_path, 'rb') as file:
                    r = dbx.files_upload(file.read(), f'/tmp/{image_path}', mode=WriteMode('overwrite'))
                    # print('Данные загр файла')
                
                link = dbx.sharing_create_shared_link(f'/tmp/{image_path}')
                url = link.url
                
                # Постоянная ссылка для загрузки файла
                dl_url = re.sub(r"\?dl\=0", "?raw=1", url)
                
                # ! Исправить ошибку окончания срока действия токена
                # ! dropbox.exceptions.AuthError: AuthError('cf404a45d0504299bbe9026d5b754d83', AuthError('expired_access_token', None))
                
                print('ССЫЛКА')
                print(dl_url)
                
                # print(card_record)
                
                
                # Загрузить изображение в Airtable
                Card.upload_image(card_record['id'], dl_url)
                
                # print('БАХ')
                
                break
        else:
            continue
        # for field in card_record['fields']:
            # cards.append(Card())
            # print('f', card_record['fields'][field])
    
    # print(cards)
    
    r = {
        'id': 'recbXcD5MxFWPwy7m',
        'createdTime': '2022-09-15T21:28:42.000Z',
        'fields': {
            'card_issued_date': '2022-09-15T21:29:00.000Z',
            'level': 10000,
            'uuid': 'fjker-r3928h',
            'user_uuid': ['recvrOn45PaUWebUx'],
            'role': 'boss',
            'name (from user_uuid)': ['Михаил'],
            'surname (from user_uuid)': ['Батин']
        }
    }
    
      
def upload_image():
    pass
    
    # print(card_records_without_images)
    
    # 2. Каждую запись проверить, корректно ли заполнена карточка
    # 3. Если да — сгенерировать изображение карточки
    
    
    # 5. Загрузить изображение в хранилище (временно?) для получения общедоступного url
    
    
    # 6. Загрузить изображение в Airtable
    img_u = ''
    # Card.upload_image('recbXcD5MxFWPwy7m', img_u)
    
    # 7. Удалить временное изображение из хранилища так как изображение уже загружено
    
    # 8. Связать uuid новой записи карточки с uuid записи пользователя

def main():
    # Загружаем артефакты для работы с карточками
    # check_artifacts()
    
    count = 0
    while True:
        count += 1
        print('Проверка:',count)
        check_and_generate_cards()
        sleep(1)
    
    
    print('Готово')
    
    # Примеры
    
    # Получить всех пользователей
    # print(json.dumps(User.get_all(), indent=2))
    # Получить одного пользователя
    # print(json.dumps(User.get_one(id='reciihTu8r1H5zisE'), indent=2))
    
    # Данные конкретного пользователя
    # user_data = {
    #     'name': 'Dmitry',
    #     'surname': 'Prokofiev',
    #     'role': User.ROLE.ADMIN,
    #     'card_issued_date': datetime.now().strftime('%d %B %Y'),
    #     'id': f'{69:04d}',
    #     'level': 1
    # }
    
    # Сгенерировать для одного пользователя одну карточку
    # user = User(*user_data)

if __name__ == '__main__':
    main()
