from functools import wraps
from flask import g, redirect, url_for


# 装饰器
def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.signIn"))
    return inner


# @login_required
# def publish_question(question_id):
#     pass
# # 等价于
# login_required(publish_question)(question_id)
