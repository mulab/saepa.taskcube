from .tasks import TaskList
from .exceptions import *
from .. import db
from ..models import User
from ..models import Task
from datetime import datetime
from datetime import timedelta
from .util import construct_text_message


def view_tasks(user):
    return '还没有开发出来哦'


def query_credits(user):
    return '您的现有积分为: %s' % user.credits


commands = {
    '任务': view_tasks,
    '积分': query_credits,
    '查询': query_credits
}


def handle(message):
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
        task = Task(key=message['Content'], name=task_config['name'],
                    credit=task_config['credit'], start_time=datetime.now(), user=user)
        db.session.add(user)
        db.session.add(task)
        db.session.commit()
        reply = "您成功完成了任务：%s，获得了积分：%d" % (task.name, task.credit)
    elif message['Content'] == 'start':
        task = Task.query.filter_by(user=user, finished=False).order_by(Task.start_time.desc()).first()
        if task is not None:
            return '你还有跑步没有完成'
        task_config = TaskList['run']
        task_config['validator'](user)
        task = Task(key='run', name='run', credit=0, start_time=datetime.now(),
                    user=user, finished=False, need_validation=True)
        db.session.add(task)
        db.session.commit()
        reply = '开始跑步'
    elif message['Content'] == 'end':
        task = Task.query.filter_by(user=user, finished=False).order_by(Task.start_time.desc()).first()
        if task is None:
            return '你还没有开始跑步'
        start_time = task.start_time
        end_time = datetime.now()
        if start_time + timedelta(hours=2) < end_time:
            return '超时'
        duration = end_time - start_time
        task.end_time = end_time
        task.credit = 1
        task.duration = duration
        task.finished = True
        user.total_time += duration
        user.credits += 1
        db.session.add(task)
        db.session.add(user)
        db.session.commit()
        reply = '完成了跑步，本次跑步时间: %s s。累计跑步 %s s' % (duration, user.total_time)
    else:
        raise CommandNotFoundException()
    return reply
