import datetime

from app import app
from flask import render_template, request, redirect, url_for, session, g, flash
from flask_login import login_required, current_user, login_user, logout_user, LoginManager
from app.forms import LoginForm, RegistrationForm, QuestionForm
from app.models import User
from app import db
from app.token import generate_confirmation_token, confirm_token
from app.email import send_email
from app.decorator import check_confirmed
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
print(quiz.score)


@app.route('/')
def home():
    questions = quiz_interface.get_question()
    return render_template('index.html', title='Home', questions=questions)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(message='Incorrect credentials', category='red')
            return redirect(url_for('login'))
        # session['user_id'] = user.id
        session['marks'] = 0
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('login.html', form=form, title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # Verifying the user does not exist
            old_user = User.query.filter_by(email=form.email.data).first()
            if old_user:
                flash(message='User already exists, login instead!')
                return redirect(url_for('login'))
            user = User(username=form.username.data,
                        email=form.email.data,
                        marks=0,
                        registered_on=datetime.datetime.now(),
                        confirmed=False
                        )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            token = generate_confirmation_token(user.email)
            print(token)
            confirm_url = url_for('confirm_email', token=token, email=form.email.data, _external=True)
            subject = "Please confirm your email"
            send_email(to=user.email, subject=subject, confirm_url=confirm_url)

            login_user(user)

            # flash('A confirmation email has been sent via email.', 'red')
            return redirect(url_for("unconfirmed"))

    return render_template('register.html', title='Register', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'red')
    user_email = request.args.get('email')
    user = User.query.filter_by(email=user_email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'green')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'green')
    return redirect(url_for('home'))


@app.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect('home')
    flash('Please confirm your account!', 'error')
    return render_template('unconfirmed.html')

@app.route('/resend')
@login_required
def resend_confirmation():
    token = generate_confirmation_token(current_user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    subject = "Please confirm your email"
    send_email(to=current_user.email, subject=subject, confirm_url=confirm_url)
    flash('A new confirmation email has been sent.', 'green')
    return redirect(url_for('unconfirmed'))


@app.route('/question', methods=['GET', 'POST'])
@login_required
@check_confirmed
def question():
    form = QuestionForm()
    form.options.choices = ['True', 'False']
    questions = quiz_interface.get_question()
    if form.validate_on_submit():
        if request.method == 'POST':
            if questions:
                option = request.form['options']
                if option == 'True':
                    if quiz_interface.anwser_true() == 'green':
                        print(quiz_interface.anwser_true())
                        print(quiz.score)
                    else:
                        print(quiz_interface.anwser_true())
                        print(quiz.score)
                elif option == 'False':
                    if quiz_interface.anwser_false() == 'green':
                        print(quiz_interface.anwser_false())
                        print(quiz.score)
                    else:
                        print(quiz_interface.anwser_false())
                        print(quiz.score)
            else:
                return redirect(url_for('score'))
    return render_template('question.html', form=form, questions=questions, score=quiz.score)


@app.route('/score')
def score():
    score = quiz.score
    return render_template('score.html', score=score)


@app.route('/reset')
def reset():
    quiz_interface.refresh()
    return redirect(url_for('question'))


@app.route('/logout')
@login_required
def logout():
    # if not g.user:
    #     return redirect(url_for('login'))
    session.pop('user_id', None)
    session.pop('marks', None)
    logout_user()
    return redirect(url_for('home'))
