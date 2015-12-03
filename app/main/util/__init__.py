__author__ = 'hqythu'


def construct_text_message(msg, text):
    reply = {
        'FromUserName': msg['ToUserName'],
        'ToUserName': msg['FromUserName'],
        'MsgType': 'text',
        'CreateTime': msg['CreateTime'],
        'Content': text
    }
    return reply
