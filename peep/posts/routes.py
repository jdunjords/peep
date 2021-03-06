from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort, current_app)
from flask_login import current_user, login_required
from peep import db
from peep.models import User, Post, PostImage, Comment, SubComment
from peep.posts.forms import PostForm, CommentForm
from peep.images.utils import save_picture, delete_picture


posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	
	form = PostForm(meta={'csrf': False})
	if form.validate_on_submit():

		# create the post and add it to the database
		post = Post(title=form.title.data, content=form.content.data, 
					author=current_user)
		db.session.add(post)
		db.session.commit()
	
		# if the filename isn't empty, user selected files for post
		if request.files['picture'].filename != '':
			
			# ensure no more than 10 images can be added to each post
			num_post_pics = len(form.picture.data)
			if num_post_pics > current_app.config['POST_PIC_LIMIT']:
				flash(f"Only {current_app.config['POST_PIC_LIMIT']} images allowed per post.", "info")
				return redirect(request.url)

			# iterate through the list of picture uploads
			for picture in form.picture.data:
				image_file = save_picture(picture, 'post_pics')
				post_image = PostImage(image_file=image_file, owner=current_user, post=post, \
										post_id=post.id, user_id=current_user.id)
				db.session.add(post_image)
				db.session.commit()

		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))

	return render_template("create_post.html", title="New Post", 
							form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):

	# get all comments for the current post
	comments = Comment.query.filter_by(post_id=post_id).all()

	subcomments = []
	for comment in comments:
		subcomments.append(SubComment.query.filter_by(parent_com_id=comment.id).all())

	# get all images for the current post
	post_images = PostImage.query.filter_by(post_id=post_id).all()

	# get the post (or return 404 if it doesn't exist)
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', comments=comments, subcomments=subcomments,
							title=post.title, post=post, post_images=post_images)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# HTTP response for a forbidden route
		abort(403)
	
	form = PostForm(meta={'csrf': False})
	if form.validate_on_submit():

		# update the title and content fields to save changes before checking images
		post.title = form.title.data
		post.content = form.content.data
		db.session.commit()

		# if the filename isn't empty, user selected some files to add
		if request.files['picture'].filename != '':
			num_current_pics = len(PostImage.query.filter_by(post_id=post_id).all())
			num_new_pics = len(form.picture.data)

			# check to see if the amount of new pics will exceed the picture limit on posts
			if num_current_pics + num_new_pics > current_app.config['POST_PIC_LIMIT']:
				flash('Newly added images exceeds image limit for this post', 'info')
				return redirect(request.url)

			# iterate through the list of picture uploads
			for picture in form.picture.data:
				image_file = save_picture(picture, 'post_pics')
				post_image = PostImage(image_file=image_file, owner=current_user, post=post, \
										post_id=post_id, user_id=current_user.id)
				db.session.add(post_image)
		
			# commit new post images
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

	# ensure that user is authenticated
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		# HTTP response for a forbidden route
		abort(403)

	# delete all comments on the post to keep referential integrity
	post_comments = Comment.query.filter_by(post_id=post_id).all()
	for post_comment in post_comments:
		subcomments = SubComment.query.filter_by(parent_com_id=post_comment.id).all()
		for subcomment in subcomments:
			db.session.delete(subcomment)
		db.session.delete(post_comment)

	# delete all of the post pictures
	post_images = PostImage.query.filter_by(post_id=post_id).all()
	if post_images:
		for post_image in post_images:
			delete_picture(post_image.image_file, "post_pics")
			db.session.delete(post_image)

	# now we can safely delete the post
	db.session.delete(post)
	db.session.commit()
	
	flash('Your post has been deleted!', 'success')
	return redirect(url_for('main.home'))


@posts.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):

	# get the current user's id so we know who wrote the comment
	user_id = current_user.id

	# create a comment form to either send or validate
	form = CommentForm(meta={'csrf': False})

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


@posts.route('/subcomment/<int:post_id>/<int:comment_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def subcomment(post_id, comment_id, user_id):
	
	# get the current user's id so we know who wrote the comment
	user_id = current_user.id

	# create a comment form to either send or validate
	form = CommentForm(meta={'csrf': False})

	# check that the form validates (i.e., comment has content)
	if form.validate_on_submit():

		# create new comment, attach it to current user and the post
		# that it's replying to
		subcomment = SubComment(parent_com_id=comment_id, user_id=user_id,
				   	            post_id=post_id, content=form.content.data)
		db.session.add(subcomment)
		db.session.commit()

		# redirect to the page for the post replied to
		return redirect(url_for("posts.post", post_id=post_id))

	# get the author of the post for display purposes
	comment_author = User.query.filter_by(id=user_id).first().username

	# render comment page
	return render_template("comment.html", form=form, 
							legend=f"Reply to {comment_author}", 
							post_id=post_id)


# create delete comment function
@posts.route('/post/<int:post_id>/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(post_id, comment_id):
	comment = Comment.query.get_or_404(comment_id)
	if comment.author != current_user:
		# HTTP response for a forbidden route
		abort(403)

	# delete all subcomments that refer to this comment id
	subcomments = SubComment.query.filter_by(parent_com_id=comment_id).all()
	for subcomment in subcomments:
		db.session.delete(subcomment)
	db.session.delete(comment)
	db.session.commit()

	flash('Your comment has been deleted!', 'success')
	return redirect(url_for('posts.post', post_id=post_id))


# create delete comment function
@posts.route('/post/<int:post_id>/subcomment/delete/<int:subcomment_id>', methods=['POST'])
@login_required
def delete_subcomment(post_id, subcomment_id):
	subcomment = SubComment.query.get_or_404(subcomment_id)
	if subcomment.author != current_user:
		# HTTP response for a forbidden route
		abort(403)

	# delete the subcomment
	db.session.delete(subcomment)
	db.session.commit()

	flash('Your subcomment has been deleted!', 'success')
	return redirect(url_for('posts.post', post_id=post_id))
