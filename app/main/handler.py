from .tasks import TaskList
from .exceptions import *
from .. import db
from ..models import User
from ..models import Task
from datetime import datetime


def handler(message):
    openid = message.get('FromUserName', '')
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        raise UserNotRegisteredException()
    try:
        task_config = TaskList[message['Content']]
    except KeyError:
        raise CommandNotFoundException()
    task_config['validator'](user)
    user.credits += task_config['credit']
    task = Task(name=task_config['name'], credit=task_config['credit'],
                datetime=datetime.now(), user=user)
    db.session.add(user)
    db.session.add(task)
    db.session.commit()
    return construct_reply_message(message,
                                   "您成功完成了任务：%s，获得了积分：%d" % (task.name, task.credit))


def construct_reply_message(msg, text):
    reply = {
        'FromUserName': msg['ToUserName'],
        'ToUserName': msg['FromUserName'],
        'MsgType': 'text',
        'CreateTime': msg['CreateTime'],
        'Content': text
    }
    return reply
