#
#
# pow settings file
# 
import json
import pow_comments.encoders
import os

server_settings = {
    "app_name"          :   "pow_comments",
    "port"              :   8080,
    "debug"             :   True,
    "https"             :   False,
    "template_path"     :   os.path.join(os.path.dirname(__file__), "views"),
    "static_url_prefix" :   "/static/",
    "static_path"       :   os.path.join(os.path.dirname(__file__), "static"),
    "login_url"         :   "/login",
    "xsrf_cookies"      :   True,
    "cookie_secret"     :   "254f2254-6bb0-1312-1104-3a0786ce285e",
}

templates = {
    "template_path"     :   server_settings["template_path"],
    "handler_path"      :   os.path.join(os.path.dirname(__file__), "handlers"),
    "model_path"        :   os.path.join(os.path.dirname(__file__), "models"),
    "stubs_path"        :   os.path.join(os.path.dirname(__file__), "stubs")
}

myapp = {
    "default_format"    :   "json",
    "supported_formats" :   ["json", "csv", "xml"],
    "base_url"          :   "https://localhost",
    "encoder"           :   {
            "json"  :   pow_comments.encoders.Json(ensure_ascii=False),
            "csv"   :   pow_comments.encoders.JsonToCsv(),
            "xml"   :   pow_comments.encoders.JsonToXml()
    },
    "page_size"         : 10,
    "enable_authentication"     :   False,   # False, simple or custom
    "auto_schema"   :   True
}


database = {
    "type"      :   "sqlite",
    "dbname"    :   r"sql.db",   # better leave the r to enable absolute paths with backslashes 
    "host"      :   None,       
    "port"      :   None,   
    "user"      :   None,
    "passwd"    :   None
}

#from handlers.very_raw_own_handler import VeryRawOwnHandler
routes = [
            #(r'.*', VeryRawOwnHandler)
        ]

