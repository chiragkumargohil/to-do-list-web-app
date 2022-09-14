from flask import Flask, render_template, redirect, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

DB_PATH = 'database.db'

def create_database():    
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS "todo" (
                "srno"	INTEGER NOT NULL UNIQUE,
                "task"	TEXT NOT NULL,
                "dsc"	TEXT,
                "dated"	TEXT NOT NULL,
                PRIMARY KEY("srno" AUTOINCREMENT)
            );""")
    
    conn.commit()
    conn.close()

@app.route("/", methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    if request.method == "POST":
        user_task = request.form["task"]
        user_dsc = request.form["dsc"]
        now = datetime.now()
        dated = now.strftime("%d/%m/%Y %H:%M:%S")
        
        cur.execute('''INSERT INTO todo (task, dsc, dated) VALUES (?, ?, ?);''', (user_task, user_dsc, dated))
        conn.commit()
    
    cur.execute("SELECT * FROM todo")
    allToDo = cur.fetchall()
    conn.close()

    return render_template('index.html', allToDo=allToDo)

@app.route("/update/<int:number>", methods=['GET', 'POST'])
def update(number):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    if request.method == "POST":
        user_srno = number
        user_task = request.form["task"]
        user_dsc = request.form["dsc"]
        now = datetime.now()
        dated = now.strftime("%d/%m/%Y %H:%M:%S")
        
        cur.execute('''UPDATE todo SET task= ?, dsc= ?, dated= ? WHERE srno= ?;''', (user_task, user_dsc, dated, user_srno))
        conn.commit()
        conn.close()

        return redirect('/')
    
    cur.execute('''SELECT * FROM todo WHERE srno= ?;''', (number,))
    todo = cur.fetchone()
    conn.close()

    return render_template('update.html', todo=todo)

@app.route('/delete/<int:number>')
def delete(number):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("DELETE FROM todo WHERE srno = ?", (number,))

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == '__main__':
    create_database()
    app.run()