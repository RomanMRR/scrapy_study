## Сохранение в Json и XML

1. Запустить паук с параметром -o или -O, например
    ```
   scrapy crawl scrap_me -O data.json
   ```
   `-o` - добавит в файл json/xml новую информацию

   `-O` - перезапишет собранную информацию
2. Определить формат и путь сохранения собранных результатов в `setting.py`. Например
   ```python
   from scrapy_study.items import JsonXmlItem
    
   FEEDS = {
    'data/%(name)s.xml': {
        'format': 'xml',
        'encoding': 'utf8',
        'store_empty': False,
        'item_classes': [JsonXmlItem, 'json_xml.items.JsonXmlItem'],
        'overwrite': True,
        'indent': 4,
        'item_export_kwargs': {
            'export_empty_fields': True,
        },
    }
   }
   ```
   Здесь:
    - `store_empty` установлен на False, что означает необходимость пропускать записи без данных при экспорте
    - В параметрах `item_export_kwargs` задается словарь аргументов для экспорта элементов. В данном случае
      используется
      только один аргумент - `export_empty_fields`, установленный на `True` для экспорта полей даже если они
      являются
      пустыми.
    - `indent` задаёт количество пробелов для формирования файла

   Более подробно обо всех настройках можно
   прочесть [здесь](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds)

## 