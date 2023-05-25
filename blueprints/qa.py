from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm
from models import QuestionModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    # return "这是首页"
    return render_template("index.html")


@bp.route("/chat", methods=['GET', 'POST'])
@login_required
def publish_qa():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
        return render_template("chat.html", questions=questions)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇的详情页,先跳转到首页
            return redirect(url_for("qa.publish_qa"))
        else:
            print(form.error)
            return redirect(url_for("qa.publish_qa"))


@bp.route("/pop-chat", methods=['GET', 'POST'])
@login_required
def publish_qa_pop():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
        return render_template("pop-chat.html", questions=questions)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇的详情页,先跳转到首页
            return redirect("/")
        else:
            print(form.error)
            return redirect(url_for("qa.publish_qa"))


@bp.route("/rock-chat", methods=['GET', 'POST'])
@login_required
def publish_qa_rock():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
        return render_template("rock-chat.html", questions=questions)
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇的详情页,先跳转到首页
            return redirect("/")
        else:
            print(form.error)
            return redirect(url_for("qa.publish_qa"))


@bp.route("/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)
