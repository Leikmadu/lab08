import os
import pymysql

class ItemModel:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'database': os.getenv('DB_NAME'),
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }

    def get_all_items(self):
        try:
            conn = pymysql.connect(**self.config)
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM items')
            items = cursor.fetchall()
            cursor.close()
            conn.close()
            fixed = []
            for item in items:
                name = item['name']
                if isinstance(name, str):
                    try:
                        # Перекодировка из cp1252 в utf-8
                        name = name.encode('cp1252').decode('utf-8')
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass
                fixed.append({'name': name})
            return fixed
        except Exception as e:
            print(f'Error: {e}')
            return []
