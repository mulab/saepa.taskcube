import os
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from app import create_app


app = create_app(os.getenv('FLASK_CONFIG') or 'default')


http_server = HTTPServer(WSGIContainer(app))
http_server.listen(80)
IOLoop.instance().start()
