from flask import Flask, render_template
import question

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_index():
    question_data = question.get_data()
    return render_template('index.html', questions=question_data)

if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )