from flask import Flask, render_template, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/todo', methods=['POST'])
def task():
    body = request.json
    new_task = Todo(content=body.get('content'))
    print(new_task)

    try:
        db.session.add(new_task)
        db.session.commit()
        return 'saved'
    except:
        return 'There was an error'

    return 'nice'


if __name__ == "__main__":
    app.run(debug=True)
