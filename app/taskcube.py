from flask import Flask
from flask import request
from flask import render_template
from . import check


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
    return check_result


@app.route('/wechat', methods=['POST'])
def wechat_response():
    pass


if __name__ == '__main__':
    app.run()
