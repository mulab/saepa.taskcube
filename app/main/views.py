from flask import request
from flask import render_template
from flask import redirect
from flask import Markup
from flask import abort
from . import main
from .forms import UserForm
from .. import db
from ..models import User
from ..models import Task
from .util import check
from .util import xmlparse
from .util import construct_text_message
from . import handler
from .exceptions import *
from sqlalchemy import func


@main.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'


@main.route('/wechat', methods=['GET'])
def wechat_check():
    check_result = check.check_signature(
        request.args.get('signature', ''),
        request.args.get('timestamp', ''),
        request.args.get('nonce', ''),
        request.args.get('echostr', '')
    )
    if check_result:
        return request.args.get('echostr', '')
    else:
        return ''


@main.route('/wechat', methods=['POST'])
def wechat_response():
    message = xmlparse.get_message_by_xml(request.data)
    # TODO: 在Exception类内部处理回复信息而不是在这里使用多路的选择
    try:
        reply = construct_text_message(
            message,
            handler.handle(message)
        )
    except UserNotRegisteredException:
        reply = construct_text_message(
            message,
            Markup('欢迎参与【“你跑一公里，助梦一公里”线上活动】！不论在操场还是健身房，不论在白天还是黑夜，只要您在跑步，'
                   '即可使用该平台进行记录跑步里程记录。与其他清华学子一起，实现“450公里”跑步里程目标后，金雅拓公司（Gemalto）即为河北魏县一中的贫困学子提供往返北京的车票，圆梦其北京之行。\n'
                   '首先，请您【绑定账号】：http://taskcube.hqythu.me/wechat/login/%s\n'
                   '绑定账号成功后，回复任意内容继续。' %
                   message.get('FromUserName', ''))
        )
    except CommandNotFoundException:
        reply = construct_text_message(
            message,
            '不知道您在说什么。'
        )
    except AlreadyDoTodayException:
        reply = construct_text_message(
            message,
            '您今天已经领取过该任务了。'
        )
    except TimeNotMatchException:
        reply = construct_text_message(
            message,
            '现在这个时间不能领取该任务。'
        )
    # except:
    #     reply = construct_text_message(
    #         message,
    #         '系统出了一点问题'
    #     )
    return render_template('reply_text.xml', msg=reply)


@main.route('/wechat/success', methods=['GET'])
def success():
    return render_template('success.html')


@main.route('/wechat/login/<openid>', methods=['GET', 'POST'])
def login(openid):
    form = UserForm()
    user = User.query.filter_by(openid=openid).first()
    if user is not None:
        return redirect('/wechat/success')
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            email=form.email.data,
            mobile=form.mobile.data,
            openid=openid,
            credits=0
        )
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
    task.distance = round(task.distance, 3)
    user.total_distance = round(user.total_distance, 3)
    total_distance = db.session.query(func.sum(User.total_distance)).filter().scalar()
    total_distance = round(total_distance, 3)
    return render_template('share.html', user=user, task=task, total_distance=total_distance)
