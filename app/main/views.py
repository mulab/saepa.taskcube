from flask import request
from flask import render_template
from flask import redirect
from . import main
from .forms import UserForm
from .. import db
from ..models import User
from .util import check
from .util import xmlparse
from .util import handler


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
    openid = message.get('FromUserName', '')
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        reply = handler.construct_reply_message(
            message,
            '你需要绑定账号：<a href="taskcube.hqythu.me/wechat/login/%s">点击</a>' % openid
        )
    else:
        user.credits += 1
        db.session.add(user)
        db.session.commit()
        reply = handler.construct_reply_message(message, '你获得了积分：%d' % user.credits)
    return render_template('reply.xml', msg=reply)


@main.route('/wechat/success', methods=['GET'])
def success():
    return render_template('success.html')


@main.route('/wechat/login/<openid>', methods=['GET', 'POST'])
def login(openid):
    form = UserForm()
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
