import sqlite3


def check_table_exists(db_name, table_name):
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Выполняем запрос для проверки существования таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))

        # Получаем результат
        table_exists = cursor.fetchone() is not None

        # Закрываем соединение
        conn.close()

        return table_exists
    except sqlite3.Error as e:
        print(f"Ошибка при проверке таблицы '{table_name}': {e}")
        return False


