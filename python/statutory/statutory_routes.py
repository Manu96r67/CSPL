from flask import render_template, request, redirect, url_for, flash
from python.config import app, db  # Updated import
from python.models import Statutory 

@app.route('/stautory')
def index_page():
    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    per_page = 5  # Number of records per page

    statutory_records1 = Statutory.query.order_by(Statutory.created_date.asc()).paginate(page=page, per_page=per_page)
    
    
    # statutory_records = Statutory.query.order_by(Statutory.created_date.asc()).all()
    return render_template('statutoryform.html', statutory_records=statutory_records1)

@app.route('/add_or_edit_statutory', methods=['POST'])
def add_or_edit_statutory():
    statutory_id = request.form.get('statutory_id')
    statutory_name = request.form.get('statutory_name')

    if statutory_id:  # Edit mode
        statutory = Statutory.query.get(statutory_id)
        if statutory:
            statutory.statutory_name = statutory_name
            db.session.commit()
            flash('Statutory updated successfully!', 'success')
        else:
            flash('Statutory not found.', 'error')
    else:  # Add mode
        new_statutory = Statutory(statutory_name=statutory_name)
        db.session.add(new_statutory)
        db.session.commit()
        flash('Statutory added successfully!', 'success')

    return redirect(url_for('index_page'))

@app.route('/delete_statutory/<int:statutory_id>', methods=['POST'])
def delete_statutory(statutory_id):
    try:
        # Find the statutory record by ID
        statutory_record = Statutory.query.get(statutory_id)
        
        if statutory_record:
            # Delete all related compliance records
            # Compliance.query.filter_by(statutory_id=statutory_id).delete()
            # Delete the statutory record
            db.session.delete(statutory_record)
            db.session.commit()
            flash('Statutory and related compliances deleted successfully!', 'success')
        else:
            flash('Statutory record not found.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting statutory: {str(e)}', 'error')
    
    return redirect(url_for('index_page'))