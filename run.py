from peep import create_app

app = create_app()

# Refresh db to get any newly added tables/columns
from peep import db
from peep.models import *
app.app_context().push()
db.create_all()

if __name__ == '__main__':
	app.run(debug=True)
