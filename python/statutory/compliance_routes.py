from flask import render_template, request, redirect, url_for, flash
from python.config import app, db  # Updated import
from python.models import Statutory, Compliance

@app.route('/complianceform')
def compliance_form(): 
    page = request.args.get('page', 1, type=int)  # Get the current page number, default is 1
    per_page = 5  # Number of records per page

    # statutory_records1 = Statutory.query.order_by(Statutory.created_date.asc()).paginate(page=page, per_page=per_page)
    statutory_records = Statutory.query.all()
    compliance_records = Compliance.query.order_by(Compliance.created_date.asc()).paginate(page=page, per_page=per_page)
    return render_template('complianceform.html',statutory_list=statutory_records,compliance_list1=compliance_records)

@app.route('/add_or_edit_compliance', methods=['POST'])
def add_or_edit_compliance():
    compliance_id = request.form.get('compliance_id')
    statutory_id = request.form.get('statutory_id')
    compliance_description = request.form.get('compliance')

    if compliance_id:  # Edit mode
        compliance = Compliance.query.get(compliance_id)
        if compliance:
            compliance.statutory_id = statutory_id
            compliance.description = compliance_description
            db.session.commit()
            flash('Compliance updated successfully!', 'success')
        else:
            flash('Compliance not found.', 'error')
    else:  # Add mode
        new_compliance = Compliance(
            statutory_id=statutory_id,
            description=compliance_description
        )
        db.session.add(new_compliance)
        db.session.commit()
        flash('Compliance added successfully!', 'success')

    return redirect(url_for('compliance_form'))

@app.route('/delete_compliance/<int:compliance_id>', methods=['POST'])
def delete_compliance(compliance_id):
    try:
        # Find the statutory record by ID
        compliance_records = Compliance.query.get(compliance_id)
        
        if compliance_records:
            # Delete all related compliance records
            # Compliance.query.filter_by(compliance_id=compliance_id).delete()
            # Delete the statutory record
            db.session.delete(compliance_records)
            db.session.commit()
            flash('Statutory and related compliances deleted successfully!', 'success')
        else:
            flash('Statutory record not found.', 'error')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting statutory: {str(e)}', 'error')
    
    return redirect(url_for('compliance_form'))