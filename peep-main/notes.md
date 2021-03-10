# Re-making database after adding another model
From an interactive python interpreter:
```
from peep import create_all
app = create_all()
app.app_context().push()
from peep import db
from peep.models import User, Image, Post
db.create_all()
```
