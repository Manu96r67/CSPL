from flask import render_template, request, redirect, url_for, flash
from python.config import app, db  # Updated import
from python.models import Question

@app.route('/question')
def question():
    return render_template('sky.html')

# Route to handle question submission
@app.route('/submit_question', methods=['POST'])
def submit_question():
    department = request.form['Department']
    question = request.form['Question']
    answer_type = request.form.get('answer_type')
    
    # Insert the data into the database using SQLAlchemy
    try:
        new_question = Question(department=department, question=question, answer_type=answer_type)
        db.session.add(new_question)
        db.session.commit()
        flash('Question added successfully!', 'success')
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        flash(f'Error occurred: {e}', 'danger')
    
    return redirect(url_for('question'))