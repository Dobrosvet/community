from typing import List
from card import Card
from config import user_airtable



class User:
    def __init__(self, id: int, name: str, surname: str) -> None:
        # , cards: List[Card]
        self.id = id
        self.name = name
        self.surname = surname
        # self.cards = cards
    
    @staticmethod
    def get_all(query={}):
        # TODO: Определить ORM для работы с Airtable через классы
        
        records = user_airtable.get_all(query)
        
        # record_id = 'reciihTu8r1H5zisE'
        # Создать новую запись
        # airtable.insert({'Field 4': 'John'})
        
        # Обновить запись
        # record = airtable.get(record_id)
        # fields = {'Field 4': 'Test'}
        # airtable.update(record['id'], fields)
        
        # Загрузить изображение
        # record = airtable.get(record_id)
        # fields = {
        #     'img': [{
        #         'url': 'https://yastatic.net/s3/home/services/block/browser.svg'
        #         # 'url': 'https://dl.airtable.com/.attachments/acc4437c009cf39a3788365c3e47f23c/4eeefdfd/photo_2022-09-03_23-36-15.jpg'
        #     }]
        # }
        # res = airtable.update(record['id'], fields)
        # print('record', record)
        
        
        # print(json.dumps(record, indent=2))
        
        return records
    
    @staticmethod
    def get_one(id):
        record = user_airtable.get(id)
        return record


