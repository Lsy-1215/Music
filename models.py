from exts import db
from datetime import datetime


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class EmailCaptchaModel(db.Model):
    __tablename__ = "email_captcha"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="questions")


class PopQuestionModel(db.Model):
    __tablename__ = "pop"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="popquestions")


class RockQuestionModel(db.Model):
    __tablename__ = "rock"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship(UserModel, backref="rockquestions")


class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="answer")


class PopAnswerModel(db.Model):
    __tablename__ = "popanswer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("pop.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系 以下两句中使用popanswers，保持一致
    question = db.relationship(PopQuestionModel, backref=db.backref("popanswers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="popanswers")


class RockAnswerModel(db.Model):
    __tablename__ = "rockanswer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键
    question_id = db.Column(db.Integer, db.ForeignKey("rock.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(RockQuestionModel, backref=db.backref("rockanswers", order_by=create_time.desc()))
    author = db.relationship(UserModel, backref="rockanswers")
