#!/usr/bin/python
# -*- coding: utf-8 -*-
from app_config import app
from models2 import db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

manager = Manager(app)
#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app,db)
#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
