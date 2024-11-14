import sqlite3


def check_table_exists(db_name: str, table_name: str) -> bool:
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Выполняем запрос для проверки существования таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))

        # Получаем результат
        table_exists = cursor.fetchone() is not None
        print(table_exists)

        # Закрываем соединение
        conn.close()

        return table_exists
    except sqlite3.Error as e:
        print(f"Ошибка при проверке таблицы '{table_name}': {e}")
        return False


def create_table(db_name):
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Создаем таблицу users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT
            );
        """)

        # Создаем таблицу user_data
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passMGR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                name TEXT NOT NULL,
                site_url TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)

        # Сохраняем изменения
        conn.commit()
        print("Таблицы созданы успешно.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        # Закрываем соединение
        conn.close()


# create_table("users.db")
# def add_db(name_db: str, name_table: str, colum: str, data: str) -> None:
