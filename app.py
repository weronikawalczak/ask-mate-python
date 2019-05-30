from flask import Flask, render_template, redirect, request, url_for, session, escape, flash
import question
import answer
import data_manager
import user

app = Flask(__name__)


@app.route('/all')
def index():
    questions = question.get_data()
    if 'username' in session:
        user_data = session['username']
    else:
        return render_template('index.html', questions=questions)
    #     flash('Logged in as %s' % escape(session['username']))
    return render_template('index.html', questions=questions, user_data=user_data)


@app.route('/')
@app.route('/latest')
def get_latest():
    questions = question.get_latest()
    return render_template('index.html', questions=questions)


@app.route('/add-question')
def add_question():
    return render_template('add_question.html')


@app.route('/add-question', methods=['POST'])
def save_question():
    title = request.form['title']
    message = request.form['message']
    image = request.form['image']
    username = session['username']
    id_of_new_question = question.save_question(title, message, image, username)
    return redirect('/question/' + str(id_of_new_question))


@app.route('/question/<question_id>')
def question_detail(question_id):
    found_question = question.get_question(question_id)
    question_answers = answer.get_question_answers(question_id)
    found_comments = question.get_comments(question_id)
    question.increment_view(question_id)
    answers_comments = answer.get_answers_comments(question_answers)
    return render_template('question_details.html',
                           question=found_question,
                           answers=question_answers,
                           comments=found_comments,
                           answers_comments=answers_comments)


@app.route('/question/<question_id>/delete', methods=['GET'])
def delete_question(question_id):
    question.remove_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/edit', methods=['GET'])
def edit_question(question_id):
    found_question = question.get_question(question_id)
    return render_template('edit_question.html', question=found_question)


@app.route('/question/<question_id>/update', methods=['POST'])
def update_question(question_id):
    title = request.form['title']
    message = request.form['message']
    image = request.form['image']
    question.update_question(question_id, title, message, image)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/new-comment', methods=['GET'])
def add_comment_question(question_id):
    return render_template('add_comment.html', subject_id=question_id, subject="question", question_id=question_id)


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def save_comment(question_id):
    username = session['username']
    message = request.form['message']
    question.add_comment(question_id, message, username)
    return redirect('/question/' + str(question_id))


@app.route('/delete-comment/<comment_id>')
def delete_comment(comment_id):
    question_id = question.get_question_by_comment_id(comment_id)
    question.delete_comment(comment_id)
    return redirect('/question/' + str(question_id))


#ANSWERS
@app.route('/question/<question_id>/new-answer', methods=['POST'])
def add_answer(question_id):
    username = session['username']
    message = request.form['message']
    image = request.form['image']
    answer.add_answer(question_id, message, image, username)
    return redirect('/question/' + question_id)


@app.route('/answer/<answer_id>/edit')
def edit_answer(answer_id):
    found_answer = answer.get_answer(answer_id)
    return render_template('answer.html', answer=found_answer)


@app.route('/answer/<answer_id>/update', methods=['POST'])
def update_answer(answer_id):
    message = request.form['message']
    answer.update_answer(answer_id, message)
    question_id = answer.get_question_id(answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    question_id = answer.get_question_id(answer_id)
    answer.remove_answer(answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/answer/<answer_id>/vote')
def vote_for_answer(answer_id):
    answer.vote_for_answer(answer_id)
    question_id = answer.get_question_id(answer_id)
    user.gain_reputation(session['username'], 5)
    return redirect('/question/' + str(question_id))


@app.route('/question/<question_id>/vote')
def vote_for_question(question_id):
    question.vote_for_question(question_id)
    return redirect('/')


@app.route('/search', methods=['GET'])
def search():
    search_phrase = request.args.get('phrase')
    questions = data_manager.search(search_phrase)
    return render_template('index.html', questions=questions)


@app.route('/answer/<answer_id>/new-comment')
def add_comment_answer(answer_id):
    question_id = answer.get_question_id(answer_id) #Only for cancel button
    return render_template('add_comment.html', subject_id=answer_id, subject="answer", question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['POST'])
def save_comment_answer(answer_id):
    message = request.form['message']
    username = session['username']
    answer.add_comment(answer_id, message, username)
    question_id = answer.get_question_id(answer_id)
    return redirect('/question/' + str(question_id))


@app.route('/registration', methods=['GET'])
def show_register_template():
    return render_template('registration_login.html')


@app.route('/registration', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    repeated_password = request.form['repeated_password']
    try:
        user.register_user(username, password, repeated_password)
    except Exception as e:
        return redirect('/registration?error_message='+str(e))


@app.route('/list_users')
def list_users():
    users_info = data_manager.list_users()
    print(users_info)
    return render_template('list_users.html', list_users=users_info)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = user.login_user(request.form['username_login'], request.form['password_login'])
        if result:
            session['username'] = result['username']
            session['user_id'] = result['id']
            print("Logged in as " + request.form['username_login'])
            return redirect('/')
        else:
            print("Error logging in as " + request.form['username_login'])
            return redirect('/registration')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('index'))


@app.route('/user/<user_id>')
def user_page_render():
    return render_template('user_page.html')


@app.route('/user/<user_id>', methods=['POST'])
def user_page(user_id):
    user_question = user.get_questions_by_user_id(user_id)
    user_answers = user.get_answers_by_user_id(user_id)
    user_comments = user.get_comments_by_user_id(user_id)
    return render_template('user_page.html', user_question=user_question,
                           user_answers=user_answers, user_comments=user_comments)


if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )
