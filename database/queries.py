import sqlite3

def initiate_database(database_name):
    create_users_table = '''
CREATE TABLE IF NOT EXISTS users(chat_id TEXT UNIQUE NOT NULL, is_admin BOOLEAN NOT NULL);'''
    create_messages_table = '''
CREATE TABLE IF NOT EXISTS messages(body TEXT NOT NULL, chat_id TEXT NOT NULL, FOREIGN KEY(chat_id) REFERENCES users(chat_id) ON DELETE CASCADE);
'''
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute(create_users_table)
        cursor.execute(create_messages_table)

def create_user(database_name, message):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
INSERT INTO users(chat_id, is_admin) VALUES(:id, false)
''', ({"id": message.chat.id}))

def get_user(database_name, message):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute('''
    SELECT * FROM users WHERE chat_id = :id;
    ''', ({"id": message.chat.id}))
        return result.fetchall()
            

def save_message(database_name, message, content):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        data = ({"id": message.chat.id, "message": content})
        cursor.execute('''INSERT INTO messages(body, chat_id) VALUES(:message, :id);''', data)

def get_messages(database_name, message):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT body FROM messages WHERE chat_id = :id;", ({"id": message.chat.id}))
        res = [x[0] for x in result.fetchall()]
        return res


def is_user_admin(database_name, message):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM users WHERE chat_id = :id;", ({"id": message.chat.id}))
        return result.fetchall()

def make_admin(database_name, message):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE users 
        SET is_admin = true 
        WHERE chat_id = :id;""", ({"id": message.chat.id}))

def see_users(database_name):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM users;")
        return result.fetchall()

def reset_database(database_name):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users;")
        cursor.execute("DELETE FROM messages;")

def see_messages(database_name):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute("SELECT * FROM messages;")
        return result.fetchall()