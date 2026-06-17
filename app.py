from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# 配置SQLite数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型：电影表
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

# 初始化数据库+插入截图里的8条初始电影数据
with app.app_context():
    db.create_all()
    # 判断是否已有数据，避免重复插入
    if not Movie.query.first():
        movies_init = [
            Movie(title='My Neighbor Totoro', year='1988'),
            Movie(title='Dead Poets Society', year='1989'),
            Movie(title='A Perfect World', year='1993'),
            Movie(title='Leon', year='1994'),
            Movie(title='Mahjong', year='1996'),
            Movie(title='King of Comedy', year='1999'),
            Movie(title='Devils on the Doorstep', year='1999'),
            Movie(title='The Pork of Music', year='2012')
        ]
        db.session.add_all(movies_init)
        db.session.commit()

# 主页：展示列表、新增电影
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取新增表单数据
        title = request.form.get('name')
        year = request.form.get('year')
        if title and year:
            new_movie = Movie(title=title, year=year)
            db.session.add(new_movie)
            db.session.commit()
        return redirect(url_for('index'))
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# 编辑电影页面 GET展示原有数据 / POST更新数据
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.title = request.form['name']
        movie.year = request.form['year']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)

# 删除电影接口
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)