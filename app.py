from flask import Flask, request, render_template, redirect, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

# Your Flask app configuration and routes go here

if __name__ == '__main__':
    app.run(debug=True)

responses = []
# ...
toolbar = DebugToolbarExtension(app)

@app.route('/')
def home():
    return render_template('survey_start.html', survey=satisfaction_survey)

@app.route('/begin', methods=["POST"])
def start_survey():
    return redirect ("/question/0")

@app.route('/questions/<int:question_id>', methods=["GET", "POST"])
def question(question_id):

    if (responses is None):
        return redirect ('/')
    if (len(responses) == len(survey.questions)):
        return redirect ('/thank-you')
    if (len(responses) != question_id):
            flash(f"Invalid question id: {question_id}")
            return redirect (f'/questions/{len(responses)}')

    question = survey.questions[question_id]
    return render_template('questions.html', question_num=question_id, question=question)


@app.route('/answers', methods=['POST'])
def handle_answers():

    if request.method == 'POST':
        user_answer = request.form['answer']
        responses.append(user_answer)
    if (len(responses) == len(survey.questions)):
        return redirect ('/thank-you')
    else:
        return redirect (f"/question/{len(responses)}")
        

@app.route('/thank-you')
def complete():
    return render_template('completion.html')