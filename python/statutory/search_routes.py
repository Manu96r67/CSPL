from flask import render_template, request, redirect, url_for, flash
from python.config import app  # Updated import
from python.models import Statutory  # Updated import

@app.route('/search')
def search():
    query = request.args.get('q')
    template = request.args.get('template')
    results = Statutory.query.filter(Statutory.statutory_name.ilike(f'%{query}%')).all()
    
    if template == 'statutoryform':
        return render_template('statutoryform.html', records=results)
    elif template == 'complianceform':
        return render_template('complianceform.html', records=results)
    else:
        flash("Invalid template specified.", "error")
        return redirect(url_for('index'))
