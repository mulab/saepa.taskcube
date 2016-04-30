import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from wechat_sdk import WechatConf


db = SQLAlchemy()
wechat_conf = WechatConf(
    token=os.getenv('TOKEN', 'token'),
    appid=os.getenv('APPID', 'appid'),
    appsecret=os.getenv('APPSECRET', 'appsecret'),
    encrypt_mode='normal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
