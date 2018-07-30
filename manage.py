# encoding: utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from exts import db
from models import User

from app import app

manager = Manager(app)
migrate = Migrate(app, db)

# python manager.py db init 初始化
# python manager.py db migrate 生成迁移文件
# python manager.py db upgrade 更新到数据库
manager.add_command('db', MigrateCommand)


def main():
    manager.run()

if __name__ == '__main__':
    main()
