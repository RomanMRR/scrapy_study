## Сохранение в Json и XML

1. Запустить паука с параметром -o или -O, например
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
   
   После этой настройки, запускаем паука как обычно
   ```
   scrapy crawl scrap_me
   ```

   Более подробно обо всех настройках можно
   прочесть [здесь](https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds)

## Сохранение картинок

1. Включаем в `setting.py` нужный pipeline

```python3
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
```

2. Указываем место сохранения картинок

```python3
IMAGES_STORE = 'images'
```

3. В `items.py` определяем поля, называть нужно точно так же, как ниже

```python3
class ImageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
```

4. В классе паука в `image_urls` собираем ссылки на картинки. И возвращаем из метода сформированный `item`. `image_urls`
   должен быть списком. Например:

 ```python3
item['image_urls'] = []
for product in products:
    item['image_urls'].append(product.xpath('.//img[contains(@class, "wp-post-image")]/@src').get())
yield item
```

После включённый в `settings.py` pipeline сделает всё за нас: скачает картинки, ссылки на которые мы собрали
в `image_urls`