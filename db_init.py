from peep import create_app

app = create_app()
app.app_context().push()

from peep import db
from peep.models import User, Image, Post

db.create_all()