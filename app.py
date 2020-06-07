from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_api import FlaskAPI, status

from datetime import datetime
import json
import jsonpickle

# app = FlaskAPI(__name__)
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
def new_todo():
    body = request.json
    new_todo = Todo(content=body.get('content'))

    try:
        db.session.add(new_todo)
        db.session.commit()
        return make_response(), status.HTTP_201_CREATED

    except:
        return make_response(), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/todo', methods=['PUT'])
def update_todo():

    task_to_update = Todo.query.get_or_404(request.json.get('id'))
    task_to_update.content = request.json.get('content')

    try:
        db.session.commit()
        return make_response(), status.HTTP_200_OK
    except:
        return make_response(), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/todo/<int:id>', methods=['DELETE'])
def todo(id):

    todo_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo_to_delete)
        db.session.commit()
        return make_response(), status.HTTP_200_OK

    except:
        return make_response(), status.HTTP_500_INTERNAL_SERVER_ERROR


@app.route('/todo', methods=['GET'])
def all_todos():
    todos = Todo.query.order_by(Todo.date_created).all()
    json_todos = []
    for todo in todos:
        json_todos.append(TodoService.todo_dto_mapper(todo))
    return jsonpickle.encode(json_todos, unpicklable=False)


@app.route('/todo/first', methods=['GET'])
def last_created_todos():
    todo = Todo.query.order_by(Todo.date_created).first()
    todo_dto = TodoService.todo_dto_mapper(todo)
    return jsonpickle.encode(todo_dto, unpicklable=False)


if __name__ == "__main__":
    app.run(debug=True)
