import sqlite3

connection = sqlite3.connect("Geeks.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS task (
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
task TEXT
)
""")
connection.commit()

def add_task(user_id, task):
    connection = sqlite3.connect
    c = connection.cursor()
    c.execute("INSERT INTO tasks (user_id, tasks) VALUES (?,?)", (user_id, task))
    connection.commit()
    connection.close()

def get_tasks(user_id):
    conn = sqlite3.connect
    c = connection.cursor()
    c.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
    tasks = c.fetchall()
    conn.close()
    
def clear_tasks(user_id):
    conn = sqlite3.connect
    c = connection.cursor()
    c.execute("DELTE FROM tasks WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()



