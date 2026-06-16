import os
import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# 初始化Flask
app = Flask(__name__)
# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.root_path, "data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# 初始化数据库
db = SQLAlchemy(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 初始化数据库命令
@app.cli.command()
@click.option('--drop', is_flag=True)
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo("数据库初始化完成")

# 填充测试数据命令
@app.cli.command()
def forge():
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("测试数据生成完毕")

# 首页路由（数据库数据渲染网页）
@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    html = "用户名：" + user.name + "<br><br>电影列表：<br>"
    for mov in movies:
        html = html + mov.title + " — " + mov.year + "<br>"
    return html

if __name__ == "__main__":
    app.run(debug=True)