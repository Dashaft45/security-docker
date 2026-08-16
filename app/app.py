from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Create a SQLite database connection
def init_db():
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INT, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users VALUES (1, 'admin', 'SuperSecretPassword@ss!')")
    return conn

db_conn = init_db()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')

    # Vulnerable SQL quetry (SQL Injection)
        query = f"SELECT * FROM users WHERE username = '{username}'"

        try:
            cursor = db_conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            if user:
                return f"Успешный вход! Добро пожаловать, {user[1]}."
            return "Неверный логин."

        except Exception as e:
            return f"Ошибка базы данных: {str(e)}"


    return '''
    <form method="post">
        Username: <input type="text" name="username"><br>
        <input type="submit" value="Login">
    </form>
'''

if __name__ == '__main__':
    # host='0.0.0.0' обязателен, чтобы приложение принимало запросы извне контейнера
    app.run(host='0.0.0.0', port=5000)
