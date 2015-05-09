from datetime import datetime


def empty_validator(user):
    pass


def each_day_validator(user):
    pass


def time_validator(user):
    now = datetime.now()


TaskList = {
    '1': {
        'name': '1',
        'validator': each_day_validator,
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
