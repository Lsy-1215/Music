import wtforms
from wtforms.validators import Email, Length, EqualTo
from models import UserModel, EmailCaptchaModel
from exts import db


# Form:主要就是用来验证前端提交的数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    cpassword = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致")])

    # 自定义验证
    # 1.邮箱是否已经被注册

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已经被注册！")

    # 2.验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱或验证码错误！")
        # todo:可以删掉captcha_model，但以下方式不推荐，会频繁操作数据库，可以写一个函数定期清理一次
        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()



class LoginForm(wtforms.Form):
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])

