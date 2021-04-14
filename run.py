from peep import create_app

app = create_app()

# Refresh db to get any newly added tables/columns
from peep import db, bcrypt
from peep.models import *
app.app_context().push()
db.create_all()

# create the deleted user if necessary
if not User.query.filter_by(username="[deleted]").first():
	deleted_hashed_password = bcrypt.generate_password_hash("deleteduser").decode('utf-8')
	deleted_user = User(username="[deleted]", email="deleted@peep.com", password=deleted_hashed_password)
	db.session.add(deleted_user)
	db.session.commit()

if __name__ == '__main__':
	app.run(debug=True)
