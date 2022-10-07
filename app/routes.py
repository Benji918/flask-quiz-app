from app import app
from flask import render_template, request, redirect, url_for, session, g, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User
from app import db
from app.question_logic import question_model
from app.question_logic import data
from app.question_logic import quiz_brain
from app.question_logic import ui

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


# user to gert the id of the currently logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


question_bank = []
get_data = data.get_data()
for question in get_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = question_model.Question(question_text, question_answer)
    question_bank.append(new_question)

quiz = quiz_brain.QuizBrain(question_bank)
quiz_interface = ui.Quizinterface(quiz)


@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        # session['user_id'] = user.id
        session['marks'] = 0
        login_user(user, remember=True)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
            return redirect(next_page)
        return redirect(url_for('home'))
    # if g.user:
    #     return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.password.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['marks'] = 0
        return redirect(url_for('home'))
    # if g.user:
    #     return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/question', methods=['GET', 'POST'])
def question():
    form = QuestionForm()
    form.options.choices = ['True', 'False']
    questions = quiz_interface.get_question()
    if form.validate_on_submit():
        if request.method == 'POST':
            if quiz.still_has_questions():
                option = request.form['options']
                if option == 'True':
                    if quiz_interface.anwser_true() == 'green':
                        print(quiz_interface.anwser_true())
                        flash(message='Correct!', category='green')
                        return redirect(url_for('question'))
                    else:
                        print(quiz_interface.anwser_true())
                        flash(message='Wrong!', category='red')
                        return redirect(url_for('question'))
                else:
                    if quiz_interface.anwser_false() == 'green':
                        print(quiz_interface.anwser_false())
                        flash(message='Correct!', category='green')
                        return redirect(url_for('question'))
                    else:
                        print(quiz_interface.anwser_false())
                        flash(message='Wrong!', category='red')
                        return redirect(url_for('question'))
            else:
                return render_template('score.html')
    return render_template('question.html', form=form, questions=questions)


@app.route('/score')
def score():
    # if not g.user:
    #     return redirect(url_for('login'))
    # g.user.marks = session['marks']
    # db.session.commit()
    return render_template('score.html')


@app.route('/logout')
@login_required
def logout():
    if not g.user:
        return redirect(url_for('login'))
    session.pop('user_id', None)
    session.pop('marks', None)
    logout_user()
    return redirect(url_for('home'))
