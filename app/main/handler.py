from .tasks import TaskList
from .exceptions import *
from .. import db
from ..models import User
from ..models import Task
from datetime import datetime


def view_tasks(user):
    return '还没有开发出来哦'


def query_credits(user):
    return '您的现有积分为: %s' % user.credits


commands = {
    '任务': view_tasks,
    '积分': query_credits,
    '查询': query_credits
}


def handler(message):
    openid = message.get('FromUserName', '')
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        raise UserNotRegisteredException()
    if message['Content'] in commands:
        reply = commands[message['Content']](user)
    elif message['Content'] in TaskList:
        task_config = TaskList[message['Content']]
        task_config['validator'](user)
        user.credits += task_config['credit']
        task = Task(name=task_config['name'], credit=task_config['credit'],
                    datetime=datetime.now(), user=user)
        db.session.add(user)
        db.session.add(task)
        db.session.commit()
        reply = "您成功完成了任务：%s，获得了积分：%d" % (task.name, task.credit)
    else:
        raise CommandNotFoundException()
    return construct_reply_message(message, reply)


def construct_reply_message(msg, text):
    reply = {
        'FromUserName': msg['ToUserName'],
        'ToUserName': msg['FromUserName'],
        'MsgType': 'text',
        'CreateTime': msg['CreateTime'],
        'Content': text
    }
    return reply
