from flask import Flask
from flask import request
from flask import render_template
from . import check
from . import xmlparse
from . import handler


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/wechat', methods=['GET'])
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


@app.route('/wechat', methods=['POST'])
def wechat_response():
    message = xmlparse.get_message_by_xml(request.data)
    reply = handler.message_handler(message)
    return render_template('reply.xml', msg=reply)


if __name__ == '__main__':
    app.run()
