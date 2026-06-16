from flask import Flask, url_for

app = Flask(__name__)

# 首页路由
@app.route('/')
def hello():
    return 'Hello'

# 带动态变量的用户路由 <name> 为动态参数
@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % name

# 用于测试url_for反向生成URL
@app.route('/test')
def test_url_for():
    # 根据视图函数名生成对应URL
    print(url_for('hello'))
    print(url_for('user_page', name='greyli'))
    print(url_for('user_page', name='peter'))
    print(url_for('test_url_for'))
    # 多余参数会拼接成查询字符串 ?num=2
    print(url_for('test_url_for', num=2))
    return 'Test page'