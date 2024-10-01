from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Corrected spelling here
db = SQLAlchemy(app)

# Defining the Todo model
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    DateTime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f'{self.sno} - {self.title}'

# Defining the route for the homepage
@app.route('/' ,methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        print("posted")
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title,desc=desc)
        db.session.add(todo)
        # return redirect('/')
    db.session.commit()
    allTodo=Todo.query.all()
    return render_template('index.html',allTodo=allTodo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if request.method =='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=todo)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables within the app context
    app.run(debug=True)
