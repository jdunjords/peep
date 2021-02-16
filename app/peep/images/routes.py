from flask import (Blueprint, render_template, url_for, 
                   flash, redirect, request, abort)
from flask_login import current_user, login_required
from peep import db

images = Blueprint('images', __name__)

# Starter file where we can place routes that can handle
# the actions user wish to perform in images

@images.route('/images')
def display_images():
	pass

@images.classify('/classify')
def classify():
	pass

@images.route('/request-review')
def request_review():
	pass
