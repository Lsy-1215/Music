from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm

# /auth:访问视图函数的时候要加上/auth
bp = Blueprint("auth", __name__, url_prefix="/")


@bp.route("/index")
def index():
    return render_template("index.html")


@bp.route("/sign-in", methods=['GET', 'POST'])
def signIn():
    # return "这是登录页面"
    if request.method == 'GET':
        return render_template("sign-in.html")
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if not user:
                print("用户名在数据库中不存在")
                return redirect(url_for("auth.signIn"))
            if check_password_hash(user.password, password):
                # cookie:
                # cookie中不适合存储太多的数据，只适合存储少量的数据
                # cookie一般用来存放登录授权的东西
                # flask中的session是经过加密后存储在cookie中的
                session['user_id'] = user.id
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.signIn"))
        else:
            print(form.errors)
            return redirect(url_for("auth.signIn"))





# GET:从服务器上获取数据
# POST:将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("sign-up.html")
    else:
        # 验证用户提交的邮箱和验证码是否对应正确
        # 表单验证 flask-wtf:wtforms
        form = RegisterForm(request.form)
        if form.validate():
            # return "success"
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.signIn"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))


@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# bp.route:如果没有指定methods参数，默认就是get请求
@bp.route("/captcha/email")
def get_email_captcha():
    # 传参方式1： /captcha/email/<email>
    # 传参方式2： /captcha/email?email=xxxqq.com
    email = request.args.get("email")
    # 验证码：随机产生4位数字(0123456789*4)
    source = string.digits * 4
    captcha = random.sample(source, 4)
    # 将列表变成字符串
    captcha = "".join(captcha)
    message = Message(subject="demo验证码", recipients=[email], body=f"您的验证码是:{captcha}")
    mail.send(message)
    # memchched/redis
    # 用数据库的方式存储(相对较慢）
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # print(captcha)
    # 返回 RESTful API
    # {code:200/400/500,message:"xxxx", data:{}}
    return jsonify({"code": 200, "message": "", "data": None})


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["1379984281@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"
