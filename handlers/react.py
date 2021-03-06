import tornado.ioloop
import tornado.web
from pow_comments.handlers.base import BaseHandler
from pow_comments.application import app

@app.add_route("/react/*")
class ReactHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("react.tmpl")


@app.add_route("/react2/*")
class ReactHandler2(tornado.web.RequestHandler):
    def get(self):
        self.render("react2.tmpl")
