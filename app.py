from flask import Flask, render_template, redirect, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    dsc = db.Column(db.String(500))
    dated = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"({self.srno}, {self.task}, {self.dsc}, {self.dated})"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        user_task = request.form["task"]
        user_dsc = request.form["dsc"]
        now = datetime.now()
        dated = now.strftime("%d/%m/%Y %H:%M:%S")
        todo = ToDo(task=user_task, dsc=user_dsc, dated=dated)
        
        db.session.add(todo)
        db.session.commit()
    
    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)

@app.route("/update/<int:srno>", methods=['GET', 'POST'])
def update(srno):
    if request.method == "POST":
        user_task = request.form["task"]
        user_dsc = request.form["dsc"]
        now = datetime.now()
        dated = now.strftime("%d/%m/%Y %H:%M:%S")
        
        todo = ToDo.query.filter_by(srno=srno).first()
        todo.task = user_task
        todo.dsc = user_dsc
        todo.dated = dated

        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = ToDo.query.filter_by(srno=srno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:srno>')
def delete(srno):
    delToDo = ToDo.query.filter_by(srno=srno).first()
    
    db.session.delete(delToDo)
    db.session.commit()

    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
