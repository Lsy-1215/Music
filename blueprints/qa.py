from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm, AnswerForm, PopQuestionForm, RockQuestionForm, PopAnswerForm, RockAnswerForm
from models import QuestionModel, AnswerModel, PopQuestionModel, RockQuestionModel, PopAnswerModel, RockAnswerModel
from exts import db
from decorators import login_required

bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    # return "这是首页"
    return render_template("index.html")


@bp.route("/user-profile", methods=['GET', 'POST'])
def user_profile():
    if request.method == 'GET':
        questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
        popquestions = PopQuestionModel.query.order_by(PopQuestionModel.create_time.desc()).all()
        rockquestions = RockQuestionModel.query.order_by(RockQuestionModel.create_time.desc()).all()
        return render_template("user-profile.html", questions=questions, popquestions=popquestions, rockquestions=rockquestions)
    else:
        print("历史记录失败")
        return redirect(url_for("qa.user_profile"))


@bp.route("/chat", methods=['GET', 'POST'])
@login_required
def publish_qa():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        # 当数据很多时，就需要采用分页
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
            # todo:跳转到这篇的详情页
            return redirect(url_for("qa.publish_qa"))
        else:
            print(form.errors)
            return redirect(url_for("qa.publish_qa"))


@bp.route("/pop-chat", methods=['GET', 'POST'])
@login_required
def publish_qa_pop():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        popquestions = PopQuestionModel.query.order_by(PopQuestionModel.create_time.desc()).all()
        return render_template("pop-chat.html", popquestions=popquestions)
    else:
        form = PopQuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = PopQuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇的详情页
            return redirect('/pop-chat')
            # return redirect(url_for("qa.publish_qa_pop"))
        else:
            print(form.errors)
            return redirect(url_for("qa.publish_qa_pop"))


@bp.route("/rock-chat", methods=['GET', 'POST'])
@login_required
def publish_qa_rock():
    if not g.user:
        return redirect(url_for("auth.signIn"))
    if request.method == 'GET':
        rockquestions = RockQuestionModel.query.order_by(RockQuestionModel.create_time.desc()).all()
        return render_template("rock-chat.html", rockquestions=rockquestions)
    else:
        form = RockQuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = RockQuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo:跳转到这篇的详情页
            return redirect("/rock-chat")
        else:
            print(form.errors)
            return redirect(url_for("qa.publish_qa_rock"))


@bp.route("/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)


@bp.route("/detail_pop/<qa_id>")
def qa_detail_pop(qa_id):
    question = PopQuestionModel.query.get(qa_id)
    return render_template("detail-pop.html", question=question)


@bp.route("/detail_rock/<qa_id>")
def qa_detail_rock(qa_id):
    question = RockQuestionModel.query.get(qa_id)
    return render_template("detail-rock.html", question=question)


@bp.route("/answer", methods=['POST'])
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))


@bp.route("/popanswer", methods=['POST'])
@login_required
def public_answer_pop():
    form = PopAnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = PopAnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail_pop", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail_pop", qa_id=request.form.get("question_id")))


@bp.route("/rockanswer", methods=['POST'])
@login_required
def public_answer_rock():
    form = RockAnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = RockAnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail_rock", qa_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("qa.qa_detail_rock", qa_id=request.form.get("question_id")))


@bp.route("/search")
def search():
      # 查询方式：
      # /search?q=flask
      # /search/<q>
      # post, request.form
      q = request.args.get("q")
      questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
      return render_template("chat.html", questions=questions)


@bp.route("/search_pop")
def search_pop():
      # 查询方式：
      # /search?q=flask
      # /search/<q>
      # post, request.form
      q = request.args.get("q")
      popquestions = PopQuestionModel.query.filter(PopQuestionModel.title.contains(q)).all()
      return render_template("pop-chat.html", popquestions=popquestions)


@bp.route("/search_rock")
def search_rock():
      # 查询方式：
      # /search?q=flask
      # /search/<q>
      # post, request.form
      q = request.args.get("q")
      rockquestions = RockQuestionModel.query.filter(RockQuestionModel.title.contains(q)).all()
      return render_template("rock-chat.html", rockquestions=rockquestions)


@bp.route("/delete_zhuti", methods=['POST'])
def delete_zhuti():
    question_id = request.form.get("question_id")
    zhuti1 = QuestionModel.query.filter(QuestionModel.id == question_id).first()
    db.session.delete(zhuti1)
    db.session.commit()
    # return render_template("user-profile.html")  错误
    return redirect("/user-profile")


@bp.route("/delete_pop", methods=['POST'])
def delete_pop():
    question_id = request.form.get("question_id")
    pop1 = PopQuestionModel.query.filter(PopQuestionModel.id == question_id).first()
    db.session.delete(pop1)
    db.session.commit()
    # return render_template("user-profile.html")  错误
    return redirect("/user-profile")


@bp.route("/delete_rock", methods=['POST'])
def delete_rock():
    question_id = request.form.get("question_id")
    rock1 = RockQuestionModel.query.filter(RockQuestionModel.id == question_id).first()
    db.session.delete(rock1)
    db.session.commit()
    # return render_template("user-profile.html")  错误
    return redirect("/user-profile")





# url传参
# 邮件发送（验证码）
# ajax
# orm数据库
# JinJa2模板
# cookie和session原理
# 搜索
# ......

