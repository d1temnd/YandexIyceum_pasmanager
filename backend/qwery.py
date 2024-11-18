import sqlite3


def check_table_exists(db_name: str, table_name: str) -> bool:
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))

        table_exists = cursor.fetchone() is not None
        print(table_exists)

        conn.close()

        return table_exists
    except sqlite3.Error as e:
        print(f"Ошибка '{table_name}': {e}")
        return False


def create_table(db_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Создаем таблицу users
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_nicname TEXT NOT NULL
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
                password TEXT NOT NULL
                
            );
        """)

        conn.commit()
        print("успешно.")

    except sqlite3.Error as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        conn.close()


# create_table("users.db")


def check_user(db_name, Nic_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Проверяем, существует ли пользователь и получаем user_id
        cursor.execute("""
            SELECT user_id FROM users WHERE user_nicname = ? LIMIT 1;
        """, (Nic_name,))
        result = cursor.fetchone()

        if result:
            return True, result[0]  # Возвращаем True и user_id
        else:
            return False, None  # Если пользователя нет
    except sqlite3.Error as e:
        print(f"Ошибка работы с базой данных: {e}")
        return False, None
    finally:
        conn.close()


# print(check_user('../users.db', 'd1temnd'))


def create_user(db_name, Nic_name, user_id):
    if check_user(db_name, Nic_name)[0] or check_user(db_name, Nic_name)[1] == user_id:
        return False
    else:
        try:
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            # Проверяем, существует ли пользователь и получаем user_id
            cursor.execute("""
                INSERT INTO users (user_id, user_nicname) VALUES (?, ?);
            """, (int(user_id), str(Nic_name),))
            conn.commit()
            return True

        except sqlite3.Error as e:
            print(f"Ошибка работы с базой данных: {e}")
            return False
        finally:
            conn.close()

# print(create_user('../users.db', '3', 996027511))
