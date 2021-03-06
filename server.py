#
#
# pow server
# khz / 2016
#

import tornado.httpserver
import os
import os.path
import sys

from pow_comments.config import server_settings 
from pow_comments.powlib import merge_two_dicts
from pow_comments.application import Application
#from pow_comments.application import app
app=Application()
if __name__ == "__main__":

    #tornado.options.parse_command_line()
    #from tornado.log import enable_pretty_logging
    #enable_pretty_logging()
    #print(dir(tornado.options.options))

    tornado.options.options.log_file_prefix ='pow.log'
    tornado.options.options.log_file_num_backups=5
    # size of a single logfile
    tornado.options.options.log_file_max_size = 10 * 1000 * 1000
    tornado.options.parse_command_line()

    #app = tornado.web.Application(handlers=routes, **app_settings)
    print()
    print(50*"-")
    print("starting the pow server Server ")
    print(50*"-")
    print("visit: https://localhost:" + str(server_settings["port"]))
    print("  DB: " + str(app.settings["db"]))
    #app.listen(app_settings["port"], **server_settings)#
    #app=Application()
    #print(app)
    print()
    print(50*"-")
    print("Final routes (order matters from here on ;) " )
    print(50*"-")
    for idx,elem in enumerate(app.handlers[0][1]):
        print("#"+str(idx)+": " + str(elem.regex) + " --> " + str(elem.handler_class))

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(server_settings["port"])
    tornado.ioloop.IOLoop.instance().start()
