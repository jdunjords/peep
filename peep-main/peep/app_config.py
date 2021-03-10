#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask

app = Flask(__name__,
template_folder='templates',
static_folder='static',)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sites.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True  #链接数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True#链接数据库
app.config['SECRET_KEY'] = 'a20203233'
