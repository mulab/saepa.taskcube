from flask import request
from flask import render_template
from flask import redirect
from flask import abort
from flask import g
from . import main
from .forms import UserForm
from .. import db
from .. import wechat_conf
from ..models import User
from ..models import Task
from sqlalchemy import func
from wechat_sdk import WechatBasic
from wechat_sdk.messages import *
import datetime


@main.before_request
def wechat_binder():
    g.wechat = WechatBasic(wechat_conf)


@main.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@main.route('/wechat', methods=['GET'])
def wechat_check():
    if g.wechat.check_signature(
        request.args.get('signature', ''),
        request.args.get('timestamp', ''),
        request.args.get('nonce', ''),
    ):
        return request.args.get('echostr', '')
    else:
        return 'check signature error'


@main.route('/wechat', methods=['POST'])
def wechat_response():
    g.wechat.parse_data(request.data)
    wechat = g.wechat
    openid = wechat.message.source
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        user = User(
            openid=openid,
        )
        db.session.add(user)
        db.session.commit()
    if isinstance(wechat.message, EventMessage):
        return wechat.response_text(
            content='嗨~魔方君终于等到你啦。在这里，你可以把跑步的里程兑换成公益捐款哦。'
                    '只需要每次跑完步动动手指，把跑步APP截图和里程回复给魔方君，就是在做公益哦。'
                    '同怀公益梦，即是有缘人。用双脚跑出爱，跑出可能。愿你和魔方君玩得开心~'
                    '回复关键词“跑步”，即可参与。'
        )
    elif isinstance(wechat.message, TextMessage):
        content = wechat.message.content
        if content == '绑定':
            return wechat.response_text(
                content='点击下面的链接绑定账号: \n'
                        'http://taskcube.heqinyao.com/wechat/login/%s' % openid
            )
        elif content == '跑步':
            return wechat.response_text(
                content='使用说明：\n'
                        '①今天跑了步，相把跑步里程换成公益捐款？试试回复关键词“兑换”吧\n'
                        '②回复一张【跑步app截图\n'
                        '③回复这次的【跑步里程（km）】，要与截图保持一致哦（回复数字即可）\n'
                        '④兑换成功'
            )
        elif content == '兑换':
            return wechat.response_text(
                content='今天跑步完成了吧~回复【跑步APP截图】来告诉魔方君这次的成果吧。'
                        'p.s.跑完步，散散步，喝口水，休息，休息一下。'
            )
        else:
            try:
                distance = float(content)
            except ValueError:
                return wechat.response_text(
                    content='指令错误'
                )
            task = Task.query.filter_by(user=user, finished=False).order_by(Task.id.desc()).first()
            if task is None:
                return wechat.response_text(
                    content='请先回复跑步截图~'
                )
            task.distance = distance
            task.finished = True
            task.finish_time = datetime.datetime.now()
            db.session.add(user)
            db.session.add(task)
            db.session.commit()
            return wechat.response_text(
                content='兑换成功！你通过此次跑步成功为孩子们的图书室添置了书籍，点击本网址查看个人跑步记录：'
                        'http://taskcube.heqinyao.com/wechat/share/%s/%s' % (user.id, task.id)
            )
    elif isinstance(wechat.message, ImageMessage):
        task = Task.query.filter_by(user=user, finished=False).order_by(Task.id.desc()).first()
        if task is not None:
            return wechat.response_text(
                content='还没有回复上一次跑步的里程~'
            )
        task = Task(key='run', distance=0, user=user, finished=False, finish_time=datetime.datetime.now())
        db.session.add(task)
        db.session.commit()
        return wechat.response_text(
            content='回复魔方君这次的【跑步里程（km）】吧~要与截图保持一致哦（回复数字即可，如回复“1.5”，即表示跑步里程为1.5km）'
        )
    else:
        return wechat.response_text(
            content='unknown'
        )


@main.route('/wechat/success', methods=['GET'])
def success():
    return render_template('success.html')


@main.route('/wechat/login/<openid>', methods=['GET', 'POST'])
def login(openid):
    form = UserForm()
    user = User.query.filter_by(openid=openid).first()
    if user is not None and user.email != '':
        return redirect('/wechat/success')
    if form.validate_on_submit():
        if user is None:
            user = User(
                name=form.name.data,
                email=form.email.data,
                mobile=form.mobile.data,
                openid=openid,
                credits=0
            )
        else:
            user.name = form.name.data
            user.email = form.email.data
            user.mobile = form.mobile.data
        db.session.add(user)
        db.session.commit()
        return redirect('/wechat/success')
    return render_template('login.html', form=form)


@main.route('/wechat/share/<userid>/<taskid>', methods=['GET', 'POST'])
def share(userid, taskid):
    user = User.query.filter_by(id=userid).first()
    task = Task.query.filter_by(id=taskid).first()
    if user is None or task is None:
        abort(404)
    user_distance = db.session.query(func.sum(Task.distance)).filter_by(user=user).scalar()
    total_distance = db.session.query(func.sum(Task.distance)).filter().scalar()
    task.distance = round(task.distance, 3)
    user_distance = round(user_distance, 3)
    total_distance = round(total_distance, 3)
    return render_template('share.html', user=user, task=task,
                           user_distance=user_distance, total_distance=total_distance)
