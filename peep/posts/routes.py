from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort)
from flask_login import current_user, login_required
from peep import db
from peep.models import Post,PostImage
from peep.posts.forms import PostForm
from peep.images.utils import save_picture
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
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', title=post.title, post=post)


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
	db.session.delete(post)
	db.session.commit()
	if post.image != none:
		delete_post(post.image, "post_pics")
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))

