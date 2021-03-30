from flask import Blueprint, render_template, request,session,redirect
from peep.models import Post,Comment
from peep import db
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	# sets default to first page
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	list_all = []
	for i in posts.items:
		result = Comment.query.filter_by(post_id=i.id).all()
		list_all.append(result)
	return render_template("home.html", posts=posts,list_all=list_all, title="home")

@main.route('/about')
def about():
	return render_template("about.html", title="about")

@main.route('/comment')
def comment():
	post_id = request.args.get('post_id')
	user_id = session['user_id']
	return render_template("comment.html",user_id=user_id,post_id=post_id,title="comment")
@main.route('/comment_post',methods=['POST'])
def comment_post():
	post_id = request.form.get('post_id')
	user_id = session['user_id']
	content = request.form.get('content')
	info = Comment(post_id=post_id, user_id=user_id,
				   content=content)
	db.session.add(info)
	db.session.commit()
	return redirect('/home')