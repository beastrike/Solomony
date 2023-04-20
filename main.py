import os

from flask import Flask, redirect, g, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user, login_manager

proj_direct = os.path.dirname(os.path.abspath(__file__))
db_file = f"sqlite:///{os.path.join(proj_direct, 'task_database.db')}"

app = Flask(__name__)
login = LoginManager()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_file
app.secret_key = "very secret"
login.init_app(app)
login.login_view = 'login'
db = SQLAlchemy(app)
db.create_all()
db.session.commit()


class Task(db.Model):
    __tablename__ = 'Task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

    def __repr__(self):
        return f"<Title: {self.title}>"


class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))
    task_id = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<Username: {self.username}>"


@app.route('/', methods=['GET', 'POST'])
def welcome():
    return redirect('login')


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if len(request.form['password']) < 8:
            eggor = 'Bаш пароль должен состоять не менее чем из 8 символов. Пожалуйста, попробуйте еще раз.'
            return render_template('register.html', error=eggor)
        if request.form['password'] != request.form['repeat']:
            eggor = 'Пароли не совпадают. Пожалуйста, попробуйте еще раз.'
            return render_template('register.html', error=eggor)

        new_user = User(username=request.form['username'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")

    elif request.method == 'GET':
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user is None:
            eggorr = 'Недействительные учетные данные. Пожалуйста, попробуйте еще раз.'
            return render_template('login.html', error=eggorr)
        login_user(user)
        return redirect("/main")
    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('logged_in', None)
    return redirect('login')


@app.route('/main', methods=["GET", "POST"])
@login_required
def home():
    g.user = current_user
    tasks = None
    eggorr = None
    if request.form:
        try:
            # Ensure tasks are unique
            if request.form.get("title") in [task.title for task in Task.query.all()]:
                eggorr = "Эта задача уже существует."
            else:
                task = Task(id=1, title=request.form.get("title"), status=request.form.get("status"), user_id=g.user.id)
                tasks = Task.query.all()
                db.session.add(task)
                db.session.commit()
        except Exception as osh:
            print("Не удалось добавить задачу.")
            print(osh)
    todo = Task.query.filter_by(status='todo', user_id=g.user.id).all()
    done = Task.query.filter_by(status='done', user_id=g.user.id).all()
    doing = Task.query.filter_by(status='doing', user_id=g.user.id).all()
    tasks = Task.query.filter_by(user_id=g.user.id).all()
    return render_template("home.html", error=eggorr, tasks=tasks, todo=todo, doing=doing, done=done,
                           myuser=current_user)


@app.route("/update", methods=["POST"])
def update():
    try:
        name = request.form.get("name")
        task = Task.query.filter_by(title=name).first()
        newstatus = request.form.get("newstatus")
        task.status = newstatus
        db.session.commit()
    except Exception as e:
        print("Не удалось обновить статус задачи.")
        print(e)
    return redirect("/main")


@app.route("/delete", methods=["POST"])
def delete():
    zagolovok = request.form.get("title")
    task = Task.query.filter_by(title=zagolovok).first()
    db.session.delete(task)
    db.session.commit()
    return redirect("/main")


if __name__ == "__main__":
    app.run(debug=True)
