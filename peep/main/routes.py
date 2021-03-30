from flask import Blueprint, render_template, request
from peep.models import Post, Comment
from peep import db
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	# sets default to first page
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

	# create a list of lists that contains all comments for all posts
	list_all = []
	for i in posts.items:
		result = Comment.query.filter_by(post_id=i.id).all()
		list_all.append(result)

	return render_template("home.html", posts=posts, list_all=list_all, title="home")


@main.route('/about')
def about():
	return render_template("about.html", title="about")