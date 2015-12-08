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
    # '任务': view_tasks,
    # '积分': query_credits,
    # '查询': query_credits
}


def handle(message):
    if message.get('Event', '') == 'subscribe':
        reply = '欢迎参与【“你跑一公里，助梦一公里”线上活动】！不论在操场还是健身房，不论在白天还是黑夜，只要您在跑步，' \
                '即可使用该平台进行记录跑步里程记录。与其他清华学子一起，实现“450公里”跑步里程目标后，金雅拓公司（Gemalto）即为河北魏县一中的贫困学子提供往返北京的车票，圆梦其北京之行。\n' \
                '首先，请您【绑定账号】：http://taskcube.hqythu.me/wechat/login/%s\n' \
                '绑定账号成功后，回复任意内容继续。'
        return reply
    openid = message.get('FromUserName', '')
    user = User.query.filter_by(openid=openid).first()
    if user is None:
        raise UserNotRegisteredException()
    elif message['Content'] in commands:
        reply = commands[message['Content']](user)
    elif message['Content'] == '01':
        task = Task.query.filter_by(user=user, finished=False).order_by(Task.start_time.desc()).first()
        if task is not None:
            return '你还有跑步没有完成'
        speed = 2.5
        task = Task(key='run', name='run', credit=0, start_time=datetime.now(),
                    user=user, finished=False, need_validation=True, speed=speed)
        db.session.add(task)
        db.session.commit()
        reply = '开始慢速跑！当您跑步结束后，请回复【end】以记录跑步里程。'
    elif message['Content'] == '02':
        task = Task.query.filter_by(user=user, finished=False).order_by(Task.start_time.desc()).first()
        if task is not None:
            return '你还有跑步没有完成'
        speed = 4.0
        task = Task(key='run', name='run', credit=0, start_time=datetime.now(),
                    user=user, finished=False, need_validation=True, speed=speed)
        db.session.add(task)
        db.session.commit()
        reply = '开始快速跑！当您跑步结束后，请回复【end】以记录跑步里程。'
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
        task.distance = duration.total_seconds() * task.speed / 1000.0
        task.finished = True
        user.total_time += duration
        user.total_distance += task.distance
        user.credits += 1
        db.session.add(task)
        db.session.add(user)
        db.session.commit()
        duration = duration.total_seconds()
        hours = round(duration // 3600)
        duration %= 3600
        mins = round(duration // 60)
        scds = round(duration % 60)
        reply = '完成了跑步，本次跑步时间: %sh %sm %ss。本次跑步 %s km。' % (hours, mins, scds, round(task.distance, 3))
        reply += '点击查看【个人跑步里程档案】 http://taskcube.hqythu.me/wechat/share/%s/%s\n' % (user.id, task.id)
        reply += '（请分享至朋友圈，邀请更多朋友加入公益健康跑喔）\n\n'
        reply += '在您下一次开始跑步前：\n' \
                 '回复【01】进入慢速跑模式；\n' \
                 '回复【02】进入中/快速跑模式；'
    else:
        reply = '在您开始跑步前：\n' \
                '回复【01】进入慢速跑模式；\n' \
                '回复【02】进入中/快速跑模式；\n\n' \
                '在您完成跑步后：\n' \
                '回复【end】记录跑步里程，形成个人跑步里程档案；\n\n' \
                '您也可以报名12月12日上午10:30~11:30于紫操的线下跑步活动，届时有精美礼品赠送，和1小时志愿工时补助。' \
                '报名请点击：http://www.sojump.com/m/6647877.aspx'
    return reply
