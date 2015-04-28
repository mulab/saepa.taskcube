from flask import request
from flask import render_template

from . import main
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
    reply = handler.message_handler(message)
    return render_template('reply.xml', msg=reply)
