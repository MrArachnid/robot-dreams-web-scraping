import sqlite3

class Lesson7Pipeline:
    def __init__(self):
        super().__init__()
        self.connection = None
        self.cursor = None

    def open_spider(self, spider):
        self.connection = sqlite3.connect(f'{spider.name}.db')
        self.cursor = self.connection.cursor()
        sql = f'''
            CREATE TABLE IF NOT EXISTS {spider.name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                author TEXT
            )'''
        self.cursor.execute(sql)

    def process_item(self, item, spider):
        self.cursor.execute(
            f'INSERT INTO {spider.name}  (text, author) VALUES (?, ?)',
            (item['text'], item['author'])
        )
        self.connection.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()