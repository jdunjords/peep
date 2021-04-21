from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from peep import db, login_manager
from flask_login import UserMixin
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# tablename: 'user'
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	is_premium_member = db.Column(db.Boolean, nullable=False, default=False)
	num_uploads = db.Column(db.Integer, nullable=False, default=0)
	
	# convenient relationships
	post = db.relationship('Post', backref='author', lazy=True)
	comment = db.relationship('Comment', backref='author', lazy=True)
	image = db.relationship('Image', backref='owner', lazy=True)
	postimage = db.relationship('PostImage', backref='owner', lazy=True)
	subcomments = db.relationship('SubComment', backref='author', lazy=True)

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# tablename: 'post'
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	# create a relationship so each post image knows what post it refers to
	post = db.relationship('PostImage', backref='post', lazy=True)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

# tablename: 'postimage'
class PostImage(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image_file = db.Column(db.String(20), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

	def __repr__(self):
		return f"PostImage('{self.id}', '{self.image_file}', '{self.post_id}')"

# tablename: 'image'
class Image(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_uploaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	needs_review = db.Column(db.Boolean, nullable=False, default=False)
	favorited = db.Column(db.Boolean, nullable=False, default=False) 
	identified = db.Column(db.Boolean, nullable=False, default=False)
	submit_for_training = db.Column(db.Boolean, nullable=False, default=False) 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Image('{self.id}', '{self.date_uploaded}', '{self.image_file}', '{self.user_id}')"

# tablename: 'comment'
class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def repr(self):
		return f"Comment('{self.id}', '{self.content}','{self.post_id}', '{self.user_id}')"


#tablename: 'subcomments'
class SubComment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.Text, nullable=False)
	date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	parent_com_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def repr(self):
		return f"Sub-Comment('{self.id}', '{self.content}','{self.parent_com_id}', '{self.user_id}')"