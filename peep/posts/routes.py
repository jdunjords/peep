from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort)
from flask_login import current_user, login_required
from peep import db
from peep.models import Post, PostImage, Comment
from peep.posts.forms import PostForm, CommentForm
from peep.images.utils import save_picture, delete_picture
import os

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		if form.picture.data:
			image_fn = save_picture(form.picture.data, 'post_pics')
			image = PostImage(image_file=image_fn, owner=current_user)
			db.session.add(image)
			db.session.commit()
			post = Post(title=form.title.data, content=form.content.data, 
					author=current_user, image_file=image_fn)
		else:
			post = Post(title=form.title.data, content=form.content.data, 
					author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template("create_post.html", title="New Post", 
							form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):

	# get all comments for the current post
	comments = Comment.query.filter_by(post_id=post_id).all()

	post = Post.query.get_or_404(post_id)
	return render_template('post.html', comments=comments, 
							title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# HTTP response for a forbidden route
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		if form.picture.data:
			image_fn = save_picture(form.picture.data, 'post_pics')
			image = PostImage(image_file=image_fn, owner=current_user)
			db.session.add(image)
			post.image_file = image_fn
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template("create_post.html", title="Update Post", 
							form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# HTTP response for a forbidden route
		abort(403)

	# delete all comments on the post to keep referential integrity
	# post_comments = Comment.query.filter_by(post_id=post_id).all()
	Comment.query.filter_by(post_id=post_id).delete()
	# db.session.delete(post_comments)
	# db.session.commit()

	# now we can safely delete the post
	db.session.delete(post)
	db.session.commit()

	# delete post pictures if necessary
	if post.image_file != None:
		delete_picture(post.image_file, "post_pics")
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))


@posts.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):

	# get the current user's id so we know who wrote the comment
	user_id = current_user.id

	# create a comment form to either send or validate
	form = CommentForm()

	# check that the form validates (i.e., comment has content)
	if form.validate_on_submit():

		# create new comment, attach it to current user and the post
		# that it's replying to
		comment = Comment(post_id=post_id, user_id=user_id,
				   content=form.content.data)
		db.session.add(comment)
		db.session.commit()

		# redirect to the page for the post replied to
		return redirect(url_for("posts.post", post_id=post_id))

	# get the author of the post for display purposes
	post_author = Post.query.filter_by(id=post_id).first().author.username

	# render comment page
	return render_template("comment.html", form=form, 
							legend=f"Reply to {post_author}", 
							post_id=post_id)

# create delete comment function
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(id)
	if comment.author != current_user:
		# HTTP response for a forbidden route
		abort(403)

	# # delete all comments on the post to keep referential integrity
	# # post_comments = Comment.query.filter_by(post_id=post_id).all()
	# Comment.query.filter_by(post_id=post_id).delete()
	# # db.session.delete(post_comments)
	# # db.session.commit()

	# # now we can safely delete the post
	# db.session.delete(post)
	# db.session.commit()

	# delete the comment
	# commit to db

	flash('Your comment has been deleted!', 'success')
	return redirect(url_for('posts.post', post_id=post.id))
