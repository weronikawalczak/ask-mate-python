from flask import Flask, render_template, redirect, request
import question

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_index():
    question_data = question.get_data()
    return render_template('index.html', questions=question_data)


@app.route('/add-question', methods=['GET'])
def add_question():
    return render_template('add_question.html')


@app.route('/add-question', methods=['POST'])
def save_question():
    question.save_question(request.form)
    return redirect('/')


if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )