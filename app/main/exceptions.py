from ..exceptions import TaskcubeException


class UserNotRegisteredException(TaskcubeException):
    pass


class CommandNotFoundException(TaskcubeException):
    pass


class AlreadyDoTodayException(TaskcubeException):
    pass


class TimeNotMatchException(TaskcubeException):
    pass
