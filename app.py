from flask import Flask, render_template, url_for, request, redirect  
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable = False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__(self):
       return f'<Task {self.id}>' 

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = ToDo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
            
        except: 
            return 'There was an issue adding your task'

    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
        
    except SQLAlchemyError:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('index'))
            
        except SQLAlchemyError:
            return 'There was an issue updating your task', 500
    else:
        print('this is update get')
        return render_template('update.html', task=task)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
