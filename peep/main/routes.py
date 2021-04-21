from flask import Blueprint, render_template, request
from peep.models import Post, Comment, PostImage
from peep import db


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
	# sets default to first page
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

	# create a list of lists that contains all comments for all posts
	comments_all = []
	for post in posts.items:
		comments = Comment.query.filter_by(post_id=post.id).all()
		if comments != None and len(comments) >= 2:
			comments_all.append(comments[:2])
		else:
			comments_all.append(comments)

	post_images = []
	for post in posts.items:
		images = PostImage.query.filter_by(post_id=post.id).all()
		post_images.append(images)

	return render_template("home.html", posts=posts, post_images=post_images, 
	                       comments_all=comments_all, title="home")


@main.route('/about')
def about():
	return render_template("about.html", title="about")