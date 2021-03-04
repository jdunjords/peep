from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort)
from flask_login import current_user, login_required
from peep import db
from peep.models import Image
from peep.images.forms import ImageForm
from peep.images.utils import save_picture

images = Blueprint('images', __name__)

# Starter file where we can place routes that can handle
# the actions user wish to perform in images

@images.route('/upload-image', methods=['GET', 'POST'])
def new_image():
	form = ImageForm()
	# if form validates after user submits
	if form.validate_on_submit() and form.picture.data:
		image_file = save_picture(form.picture.data)
		image = Image(image_file=image_file, owner=current_user)
		db.session.add(image)
		db.session.commit()
		flash('Your image has been uploaded!', 'success')
		return redirect(url_for('users.user_images', username=current_user.username))
	return render_template('upload_image.html', title='Upload Image', 
                           form=form, legend='Upload Image')