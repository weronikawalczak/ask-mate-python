from flask import Flask, render_template, redirect, request
import question
import answer

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def index():
    order_direction = request.args.get('order_direction')
    if order_direction is None:
        order_direction = 'desc'

    questions = question.get_data()
    return render_template('index.html', questions=questions, order_direction=order_direction)


@app.route('/add-question')
def add_question():
    return render_template('add_question.html')


@app.route('/add-question', methods=['POST'])
def save_question():
    title = request.form['title']
    message = request.form['message']
    image = request.form['image']
    id_of_new_question = question.save_question(title, message, image)
    return redirect('/question/' + str(id_of_new_question))


@app.route('/question/<question_id>')
def question_detail(question_id):
    found_question = question.get_question(question_id)
    question_answers = answer.get_question_answers(question_id)
    return render_template('question_details.html', question=found_question, answers=question_answers)


@app.route('/question/<question_id>/delete', methods=['GET'])
def delete_question(question_id):
    question.remove_question(question_id)
    return redirect('/')


# @app.route('/question/<question_id>', methods=['GET'])
# def display_question(question_id):
#     data = question.test(question_id)
#     #question_data = question.get_data()
#     return render_template('question_details.html', item=data)
#
#
if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )


