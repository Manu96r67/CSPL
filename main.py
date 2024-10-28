from python.config import app
from python.models import db
from python.user import user
from python.statutory import statutory_routes, compliance_routes, search_routes
from python.question import questionanswer
from python.due_deligence import due_deligence

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)