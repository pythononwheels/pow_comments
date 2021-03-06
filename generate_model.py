#
# generate model
#

import argparse
import tornado.template as template
import os
from pow_comments.config import templates
from pow_comments.powlib import pluralize

def camel_case(name):
    """
        converts this_is_new to ThisIsNew
        and this in This
    """
    return "".join([x.capitalize() for x in name.split("_")])

def generate_model(model_name=None, appname=None):
    """ generates a small model with the given modelname
        also sets the right db and table settings and further boilerplate configuration.
        Template engine = tornado.templates
    """
    #
    # set some attributes
    #
    loader = template.Loader(templates["stubs_path"])
    model_class_name = camel_case(model_name)
    print("model_class_name: " + model_class_name)
    model_name_plural = pluralize(model_name)
    print("model_name_plural: " + model_name_plural)
    #
    # create the model
    #
    ofile = open(os.path.join(templates["model_path"], model_name+".py"), "wb")
    res = loader.load("sql_model_template.py").generate( 
        model_name=model_name, 
        model_name_plural=model_name_plural, 
        model_class_name=model_class_name,
        appname=appname
        )
    ofile.write(res)
    ofile.close()
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', "--name", action="store", 
                        dest="name", help='-n modelname',
                        required=True)
    #
    # db type
    # 
    # parser.add_argument('-d', "--db", action="store", 
    #                     dest="db", help='-d which_db (mongo || tiny || peewee_sqlite) default = tiny',
    #                     default="tiny", required=True)
    args = parser.parse_args()
    #
    # show some args
    #
    print("all args: ", args)
    #print(dir(args))
    #print("pluralized model name: ", pluralize(args.name))
    generate_model(args.name, appname="pow_comments")