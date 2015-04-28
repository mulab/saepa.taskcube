def message_handler(message):
    if message['MsgType'] == 'event':
        return event_handler(message)
    elif message['MsgType'] == 'text':
        return text_handler(message)
    else:
        return None


def event_handler(message):
    pass


def text_handler(message):
    return construct_reply_message(message, message['Content'])


def construct_reply_message(msg, text):
    reply = {}
    reply['FromUserName'] = msg['ToUserName']
    reply['ToUserName'] = msg['FromUserName']
    reply['MsgType'] = 'text'
    reply['CreateTime'] = msg['CreateTime']
    reply['Content'] = text
    return reply
