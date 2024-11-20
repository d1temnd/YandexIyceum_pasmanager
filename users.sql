CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                user_nicname TEXT NOT NULL
            );

CREATE TABLE IF NOT EXISTS passMGR (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nic_name TEXT NOT NULL,
                name TEXT NOT NULL,
                site_url TEXT NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL
                
            );