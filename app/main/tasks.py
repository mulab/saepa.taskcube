from .. import db
from ..models import User
from ..models import Task
from datetime import datetime
from datetime import time
from datetime import timedelta
from .exceptions import *


def empty_validator(user):
    pass


def eachday_validator(user):
    recent_task = user.tasks.filter_by(key='1').order_by(Task.datetime.desc()).first()
    if recent_task is None:
        return
    now = (datetime.utcnow() + timedelta(hours=8)).date()
    if (recent_task.datetime + timedelta(hours=8)).date() == now:
        raise AlreadyDoTodayException()


def time_validator(user):
    now = (datetime.utcnow() + timedelta(hours=8)).time()
    start = time(hour=6, minute=0)
    end = time(hour=7, minute=0)
    if start <= now <= end:
        pass
    else:
        raise TimeNotMatchException()


TaskList = {
    '1': {
        'name': '1',
        'validator': eachday_validator,
        'credit': 1
    },
    '2': {
        'name': '2',
        'validator': time_validator,
        'credit': 2
    },
    '3': {
        'name': '3',
        'validator': empty_validator,
        'credit': 3
    }
}
