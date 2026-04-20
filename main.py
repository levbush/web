from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import json
import os
from data.db_session import global_init, create_session
from data.job import Jobs
from data.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mars-one-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    with create_session() as s:
        return s.get(User, int(user_id))


@app.route('/index/<title>')
def index(title):
    return render_template('index.html', title=title)


@app.route('/training/<prof>')
def training(prof):
    return render_template('training.html', profession=prof)


@app.route('/list_prof/<list_type>')
def list_prof(list_type):
    profs = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 
             'врач', 'инженер по терраформированию', 'климатолог', 
             'специалист по радиационной защите', 'астрогеолог', 'гляциолог', 
             'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода', 
             'киберингенер', 'штурман', 'пилот дронов']
    
    list_tag = list_type if list_type in ['ul', 'ol'] else None
    return render_template('list_prof.html', profs=profs, list_tag=list_tag)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    context = {
        'title': 'Анкета',
        'surname': 'Watny',
        'name': 'Mark',
        'education': 'выше среднего',
        'profession': 'штурман марсохода',
        'sex': 'male',
        'motivation': 'Всегда мечтал застрять на Марсе!',
        'ready': 'True'
    }
    return render_template('auto_answer.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = bool(request.form.get('remember_me'))

        with create_session() as s:
            user = s.query(User).filter(User.email == email).first()

        if user and check_password_hash(user.hashed_password, password):
            login_user(user, remember=remember_me)
            return redirect('/')
        else:
            message = 'Invalid email or password'

    return render_template('login.html', title='Вход', message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/distribution')
def distribution():
    astronauts_list = [
        "Ридли Скотт",
        "Энди Уир",
        "Марк Уотни",
        "Венката Капур",
        "Тедди Сандерс",
        "Шон Бин"
    ]    
    return render_template('distribution.html', astronauts_list=astronauts_list)


@app.route('/table_param/<sex>/<int:age>')
def table(sex, age):
    return render_template('table.html', **locals())


@app.route('/member')
def member():
    path = os.path.join('templates', 'members.json')
    with open(path, encoding='utf-8') as f:
        members = json.load(f)

    return render_template('member.html', member=random.choice(members))


@app.route('/')
def works_log():
    with create_session() as s:
        jobs = s.query(Jobs).all()
        return render_template('works_log.html', title='Works Log', jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    data = {}

    if request.method == 'POST':
        data = request.form.to_dict()
        password = data.pop('password', '')
        password_again = data.pop('password_again', '')

        if password != password_again:
            message = 'Passwords do not match'
        else:
            with create_session() as s:
                if s.query(User).filter(User.email == data['email']).first():
                    message = 'User with this email already exists'
                else:
                    user = User(
                        email=data['email'],
                        surname=data['surname'],
                        name=data['name'],
                        age=data['age'] or None,
                        position=data['position'],
                        speciality=data['speciality'],
                        address=data['address'],
                        hashed_password=generate_password_hash(password),
                    )
                    s.add(user)
                    s.commit()
            return redirect('/')

    return render_template('register.html', title='Регистрация', message=message, **data)


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    message = None
    data = {}

    if request.method == 'POST':
        data = request.form.to_dict()
        with create_session() as s:
            job = Jobs(
                job=data['job'],
                team_leader=data['team_leader'] or current_user.id,
                work_size=data['work_size'] or 0,
                collaborators=data['collaborators'],
                is_finished=bool(data.get('is_finished')),
            )
            s.add(job)
            s.commit()
        return redirect('/')

    return render_template('add_job.html', title='Adding a job', message=message, **data)


def main():
    global_init('db.db')
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()