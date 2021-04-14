from flask import render_template, request, redirect, url_for, flash, Blueprint, abort,session
from flask_login import login_user, current_user, logout_user, login_required
from peep import db, bcrypt
from peep.models import User, Post, Image, Comment, PostImage
from peep.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                   RequestResetForm, ResetPasswordForm)
from peep.users.utils import send_reset_email
from peep.images.utils import delete_picture, save_picture


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm(csrf_enabled=False)
	# check to see if the form validated correctly
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Your account has been created! You are now able to log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
	# simply redirect if user already logged in
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))

	# otherwise, create a form and send it back
	form = LoginForm(csrf_enabled=False)

	# check that the form validates
	if form.validate_on_submit():

		# get user from db from their email
		user = User.query.filter_by(email=form.email.data).first()

		# check that user exists and hashed passwords match
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			session['user_id'] = user.id
			# TODO next page needs to be validated to avoid open redirect vulnerability
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check email and password.', 'danger')
	
	return render_template("login.html", title="Login", form=form)


@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm(csrf_enabled=False)
	if form.validate_on_submit():
		# TODO delete old profile pic when updating new one
		if form.picture.data:
			picture_file = save_picture(form.picture.data, 'profile_pics')
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		# this avoids the "resend form" alert
		return redirect(url_for('users.account'))
	# populate form fields with users current data
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + \
						 current_user.image_file)
	return render_template('account.html', title='Account', 
							image_file=image_file, form=form)


@users.route('/user/<string:username>/posts')
def user_posts(username):
	# sets default to first page
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	posts = Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=5)

	# create a list of lists that contains all comments for all posts
	# list_all = []
	# for post in posts.items:
	# 	post_comments = Comment.query.filter_by(post_id=post.id).all()
	# 	list_all.append(post_comments)

	post_images = []
	for post in posts.items:
		images = PostImage.query.filter_by(post_id=post.id).all()
		post_images.append(images)
	
	return render_template('user_posts.html', posts=posts, user=user, post_images=post_images)


@users.route('/user/<string:username>/images')
def user_images(username):
	user = User.query.filter_by(username=username).first_or_404()

	# users can only view their own images
	if user != current_user:
		abort(403)

	# get page, and paginate images
	page = request.args.get('page', 1, type=int)
	images = Image.query.filter_by(owner=user)\
		.order_by(Image.date_uploaded.desc()).paginate(page=page, per_page=9)
	
	return render_template('user_images.html', images=images, user=user)


@users.route('/user/<string:username>/images/favorites')
def user_images_fav(username):
	user = User.query.filter_by(username=username).first_or_404()
	# users can only view their own images
	if user != current_user:
		abort(403)
	
	# get page, and paginate images
	page = request.args.get('page', 1, type=int)
	images = Image.query.filter_by(owner=user, favorited=True)\
		.order_by(Image.date_uploaded.desc()).paginate(page=page, per_page=9)
	
	return render_template('user_images_fav.html', images=images, user=user)


@users.route('/user/<string:username>/images/identified')
def user_images_identified(username):
	user = User.query.filter_by(username=username).first_or_404()
	# users can only view their own images
	if user != current_user:
		abort(403)

	# get page, and paginate images
	page = request.args.get('page', 1, type=int)
	images = Image.query.filter_by(owner=user, identified=True)\
		.order_by(Image.date_uploaded.desc()).paginate(page=page, per_page=9)
	
	return render_template('user_images_identified.html', images=images, user=user)


@users.route('/user/<string:username>/images/training')
def user_images_training(username):
	user = User.query.filter_by(username=username).first_or_404()
	# users can only view their own images
	if user != current_user:
		abort(403)

	# get page, and paginate images
	page = request.args.get('page', 1, type=int)
	images = Image.query.filter_by(owner=user, submit_for_training=True)\
		.order_by(Image.date_uploaded.desc()).paginate(page=page, per_page=9)

	return render_template('user_images_training.html', images=images, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		send_reset_email(current_user)
		flash('An email has been sent with instructions on how to reset your password', 'info')
		return redirect(url_for('users.account'))
	else:
		form = RequestResetForm()
		if form.validate_on_submit():
			user = User.query.filter_by(email=form.email.data).first()
			send_reset_email(user)
			flash('An email has been sent with instructions on how to reset your password', 'info')
			return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm(csrf_enabled=False)
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/account/delete', methods=['GET', 'POST'])
@login_required
def delete_account():
	
	# save the current user and log them out
	user = User.query.filter_by(id=current_user.id).first()
	logout_user()

	# delete all user images
	images = Image.query.filter_by(user_id=user.id).all()
	for image in images:
		delete_picture(image.image_file, 'user_uploads')
		db.session.delete(image)

	# delete all comments
	comments = Comment.query.filter_by(user_id=user.id).all()
	for comment in comments:
		db.session.delete(comment)

	# delete all post images
	post_images = PostImage.query.filter_by(user_id=user.id).all()
	for post_image in post_images:
		delete_picture(post_image.image_file, 'post_pics')
		db.session.delete(post_image)

	# delete profile picture
	if user.image_file != 'default.jpg':
		delete_picture(user.image_file, 'profile_pics')

	# delete all posts
	posts = Post.query.filter_by(user_id=user.id).all()
	for post in posts:
		db.session.delete(post)

	# delete user
	db.session.delete(user)
	db.session.commit()

	flash("Your account has been deleted. We're sorry to see you go!", "success")

	return redirect(url_for('main.home'))
