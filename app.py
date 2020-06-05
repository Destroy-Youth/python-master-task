from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import jsonpickle


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
# db.init_app(app)


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def saved(self):
        return self.id

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)


class TodoDTO():

    def __init__(self, id, content, completed, date_created):
        self.id = id
        self.content = content
        self.completed = completed
        self.date_created = date_created


class TodoService():

    @staticmethod
    def todo_dto_mapper(todo):
        todo_dto = TodoDTO(todo.id, todo.content,
                           todo.completed, todo.date_created)
        return todo_dto


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/todo', methods=['POST'])
def newTask():
    body = request.json
    new_task = Todo(content=body.get('content'))
    print(new_task)

    try:
        db.session.add(new_task)
        db.session.commit()
        return 'saved'
    except:
        return 'There was an error'


@app.route('/todo', methods=['GET'])
def allTasks():
    tasks = Todo.query.order_by(Todo.date_created).all()
    json_tasks = []
    for task in tasks:
        json_tasks.append(TodoService.todo_dto_mapper(task))
    print(json_tasks)
    return jsonpickle.encode(json_tasks, unpicklable=False)


@app.route('/todo/first', methods=['GET'])
def lastCreatedTasks():
    task = Todo.query.order_by(Todo.date_created).first()
    task_dto = TodoService.todo_dto_mapper(task)
    return jsonpickle.encode(task_dto, unpicklable=False)


if __name__ == "__main__":
    app.run(debug=True)
