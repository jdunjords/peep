from flask import render_template, request, redirect, url_for, flash, Blueprint, abort,session
from flask_login import login_user, current_user, logout_user, login_required
from peep import db, bcrypt
from peep.models import User, Post, Image, Comment
from peep.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, 
                                   RequestResetForm, ResetPasswordForm)
from peep.users.utils import send_reset_email
from peep.images.utils import save_picture



users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
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
	form = LoginForm()

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
	form = UpdateAccountForm()
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
	list_all = []
	for post in posts.items:
		post_comments = Comment.query.filter_by(post_id=post.id).all()
		list_all.append(post_comments)
	
	return render_template('user_posts.html', posts=posts, 
							list_all=list_all, user=user)


@users.route('/user/<string:username>/images')
def user_images(username):
	user = User.query.filter_by(username=username).first_or_404()
	# users can only view their own images
	if user != current_user:
		abort(403)
	images = Image.query.filter_by(owner=user)\
		.order_by(Image.date_uploaded.desc()).all()
	return render_template('user_images.html', images=images, user=user)

@users.route('/user/<string:username>/favorites/images')
def user_fav_images(username):
	user = User.query.filter_by(username=username).first_or_404()
	# users can only view their own images
	if user != current_user:
		abort(403)
	images = Image.query.filter_by(owner=user)\
		.order_by(Image.date_uploaded.desc()).all()
	return render_template('fav_images.html', images=images, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions on how to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if user is None:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated! You are now able to log in.', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)
