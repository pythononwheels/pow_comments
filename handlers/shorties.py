import tornado.ioloop
import tornado.web
from pow_comments.handlers.base import BaseHandler
from pow_comments.application import app
#
# you can use regex in the routes as well:
# (r"/([^/]+)/(.+)", ObjectHandler),
# any regex goes. any group () will be handed to the handler 
# 
@app.add_route("/dash/*")
class DashboardHandler(BaseHandler):
    def get(self):
        self.render("dash.tmpl")

@app.add_route("/thanks/*")
class ThanksHandler(BaseHandler):
    def get(self):
        self.render("thanks.tmpl")

@app.add_route("/index/*", pos=-1)
@app.add_route("/", pos=-2)
class IndexdHandler(BaseHandler):
    def get(self):
        self.render("index.tmpl")

@app.add_route(".*", pos=-3)
class ErrorHandler(BaseHandler):
    def get(self):
        return self.render("404.tmpl", url=self.request.uri)



