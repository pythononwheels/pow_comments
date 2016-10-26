import re
import os
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Unicode, Text, Boolean, Numeric, BigInteger
from sqlalchemy import Table



def get_class_name(name):
    """
        tries to return a CamelCased class name as good as poosible
        capitalize
        split at underscores "_" and capitelize the following letter
        merge
        this_is_Test => ThisIsTest
        test => Test
        testone => Testone
    """
    #print("class_name: " + "".join([c.capitalize() for c in name.split("_")]))
    return "".join([c.capitalize() for c in name.split("_")])


#see: http://stackoverflow.com/questions/38987/how-to-merge-two-python-dictionaries-in-a-single-expression
def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

# (pattern, search, replace) regex english plural rules tuple
# taken from : http://www.daniweb.com/software-development/python/threads/70647
rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', '\1ice'),
    ('child$', 'child$', 'children'),
    ('booth$', 'booth$', 'booths'),
    ('foot$', 'foot$', 'feet'),
    ('ooth$', 'ooth$', 'eeth'),
    ('l[eo]af$', 'l([eo])af$', 'l\1aves'),
    ('sis$', 'sis$', 'ses'),
    ('man$', 'man$', 'men'),
    ('ife$', 'ife$', 'ives'),
    ('eau$', 'eau$', 'eaux'),
    ('lf$', 'lf$', 'lves'),
    ('[sxz]$', '$', 'es'),
    ('[^aeioudgkprt]h$', '$', 'es'),
    ('(qu|[^aeiou])y$', 'y$', 'ies'),
    ('$', '$', 's')
    )
def regex_rules(rules=rule_tuple):
    # also to pluralize
    for line in rules:
        pattern, search, replace = line
        yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)

def plural(noun):
    #print noun
    # the final pluralisation method.
    for rule in regex_rules():
        result = rule(noun)
        #print result
        if result:
            return result

def pluralize(noun):
    return plural(noun)

def singularize(word):
    specials = {
        "children" : "child",
        "mice"  : "mouse",
        "lice" : "louse",
        "men" : "man",
        "feet" : "foot",
        "women" : "woman"  
    }
    if word in specials.keys():
        return specials[word]
    # taken from:http://codelog.blogial.com/2008/07/27/singular-form-of-a-word-in-python/
    sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
              lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
              lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
              lambda w: w[-2:] == 'es' and w[:-2],
              lambda w: w[-1:] == 's' and w[:-1],
              lambda w: w,
              ]
    word = word.strip()
    singleword = [f(word) for f in sing_rules if f(word) is not False][0]
    return singleword


def rel_dec(what, who):
    # We're going to return this decorator
    def simple_decorator(f):
        # This is the new function we're going to return
        # This function will be used in place of our original definition
        def wrapper():
            print(what)
            f()
            print(who)
        return wrapper
    return simple_decorator


#
# a class decorator that executes at import.
# ala flask app.route()
# does all the magic monkey patching stuff like:
#   * has_many
#   * setup the schema
#   * one to one
#   * many to many
#
# see: http://ains.co/blog/things-which-arent-magic-flask-part-1.html
# 
# For the relation part see: 
# http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#building-a-relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class powDecNew():
    def __init__(self):
        self.relations = {}
    # rel is a plural string of the related model ("adresses", "comments"
    #
    # the has many magic
    #
    def has_many(self, child_as_str):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        def decorator(parent_class):
            parent_name = parent_class.__name__.lower()
            parent_class_name = parent_class.__name__

            child_class_name = get_class_name(singularize(child_as_str))
            child_module_name = singularize(child_as_str)
            #print(sorted(locals().keys()))
            #print(sorted(globals().keys()))
            import sys
            if "pow_comments.models." + child_module_name in sys.modules.keys():
                #print(dir(sys.modules["pow_comments.models." + child_module_name]))
                child_klass = getattr(sys.modules["pow_comments.models." + child_module_name], child_class_name)
            else:
                import importlib
                mod = importlib.import_module('pow_comments.models.' + child_module_name)
                #mod = __import__('pow_comments.models.'+rel_module_name, fromlist=[rel_class_name])
                child_klass = getattr(mod, child_class_name)

            setattr(parent_class, child_as_str, relationship(child_class_name, 
                order_by=child_klass.id,
                back_populates=parent_name))
            setattr(child_klass, parent_name + "_id", Column(Integer, ForeignKey(pluralize(parent_name)+".id")))
            setattr(child_klass, parent_name, relationship(parent_class_name, back_populates=child_as_str))
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_class_name + " has many: " + child_as_str)
            return parent_class
        return decorator


    def many_to_many(self, children):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        from pow_comments.dblib import Base
        def decorator(parent_class):
            parent_name = parent_class.__name__.lower()
            parent_class_name = parent_class.__name__
            
            #
            # create the new association Table and class
            #
            assoc_table = Table("association_" + parent_name + "_" + children,
                Base.metadata, 
                Column(parent_name + "_id", Integer, ForeignKey(pluralize(parent_name) + ".id")),
                Column(singularize(children)+"_id", Integer, ForeignKey(children + ".id"))
                )
            
            child_class_name = singularize(children).capitalize()
            child_module_name = singularize(children)

            #
            # set the parent attribute
            #
            setattr(parent_class, children, relationship(child_class_name, 
                secondary=assoc_table,
                back_populates=pluralize(parent_name)))

            import sys
            if "pow_comments.models." + child_module_name in sys.modules.keys():
                #print(dir(sys.modules["pow_comments.models." + child_module_name]))
                child_klass = getattr(sys.modules["pow_comments.models." + child_module_name], child_class_name)
            else:
                import importlib
                mod = importlib.import_module('pow_comments.models.' + child_module_name)
                #mod = __import__('pow_comments.models.'+rel_module_name, fromlist=[rel_class_name])
                child_klass = getattr(mod, child_class_name)
            #
            # set the child attribute
            #
            setattr(child_klass, pluralize(parent_name), 
                relationship(parent_class_name, 
                    secondary=assoc_table, back_populates=children ))
            
            
           
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_class_name + " has many-to-many: " + children)
            return parent_class
        return decorator

    #
    # the has many magic
    #
    def belongs_to(self, parent_as_str):
        # cls is the class that has many of the related models (e.g. User, Post)
        # the "parent" class
        # rel_as_str is the plueral name of the child class (adresses, comments)
        # klass below is the real class instance of the child
        def decorator(child_class):
            child_name = child_class.__name__.lower()
            
            parent_class_name = parent_as_str.capitalize()
            parent_module_name = parent_as_str
            import sys
            if ("pow_comments.models."+parent_module_name) in sys.modules.keys():
                parent_klass = getattr(sys.modules["pow_comments.models."+parent_module_name], parent_class_name)
            else:
                import importlib
                mod = importlib.import_module('pow_comments.models.' + parent_module_name)
                #mod = __import__('pow_comments.models.'+rel_module_name, fromlist=[rel_class_name])
                klass = getattr(mod, parent_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(cls, rel_as_str, relationship(rel_class_name, 
                order_by=klass.id,
                back_populates=cls_name))
            setattr(klass, cls_name + "_id", Column(Integer, ForeignKey(pluralize(cls_name)+".id")))
            setattr(klass, cls_name, relationship(cls_name.capitalize(), back_populates=rel_as_str))
            ##print(dir(rel))
            print("RELATION: I see a: " + cls_name.capitalize() + " has many: " + rel_as_str)
            return cls
        return decorator
    #
    # A one to many relationship places a foreign key on the child table 
    # referencing the parent. 
    # relationship() is then specified on the parent, as 
    # referencing a collection of items represented by the child:
    #
    # usage: @relationparent
    def one_to_many(self, child_as_str):
        # cls is the class that has many of the related models (e.g. User, Post)
        # klass below is the real class instance of the child
        def decorator(parent):
            # parent is the parent class of the relation
            parent_name = parent.__name__.lower()
            #print("parent_name: " + parent_name)
            child_class_name = singularize(child_as_str).capitalize()
            child_module_name = singularize(child_as_str)
            #print("child_class_name: " + child_class_name)
            #print("child_module_name: " + child_module_name)
            mod = __import__('pow_comments.models.'+child_module_name, fromlist=[child_class_name])
            klass = getattr(mod, child_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(parent, child_as_str, relationship(child_class_name))
            setattr(klass, parent_name + "_id", Column(Integer, ForeignKey(pluralize(parent_name)+".id")))
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_name.capitalize() + " has many: " + child_as_str)
            return parent
        return decorator

    #
    # One To One is essentially a bidirectional relationship with a scalar 
    # attribute on both sides. To achieve this, the uselist flag indicates 
    # the placement of a scalar attribute instead of a collection on 
    # the âmanyâ side of the relationship. 
    #
    def one_to_one(self, child_as_str):
        # cls is parent class (Post)
        # child_as_str is the singular name of the child (related class)
        # klass below is the real class instace of the child
        # one-to-one
        def decorator(parent):
            # cls is the parent class of the relation
            parent_name = parent.__name__.lower()
            #print("cls_name: " + cls_name)
            child_class_name = child_as_str.capitalize()
            child_module_name = child_as_str
            #print("child_class_name: " + child_class_name)
            #print("child_module_name: " + child_module_name)
            mod = __import__('pow_comments.models.'+child_module_name, fromlist=[child_class_name])
            klass = getattr(mod, child_class_name)
            #print("rel_class: " + str(klass))
            #print(dir(klass))
            setattr(parent, child_as_str, relationship(child_class_name, 
                uselist=False,
                back_populates=parent_name))
            setattr(klass, parent_name + "_id", Column(Integer, ForeignKey(parent_name+".id")))
            setattr(klass, parent_name, relationship(parent_name.capitalize(), back_populates=child_as_str))
            ##print(dir(rel))
            print("RELATION: I see a: " + parent_name.capitalize() + " has many: " + child_as_str)
            return parent
        return decorator
    #
    # tree
    # see:
    #
    def tree(self):
        # cls is the class that has many of the related models (e.g. User, Post)
        # klass below is the real class instance of the child
        def decorator(cls):
            # parent is the parent class of the relation
            cls_name = cls.__name__.lower()
            #print(cls_name)
            setattr(cls, "tree_parent_id", Column(Integer, ForeignKey(pluralize(cls_name)+".id")))
            setattr(cls, "tree_children", relationship(cls_name.capitalize()))
            ##print(dir(rel))
            print("RELATION: I see a tree: " + cls_name.capitalize() )
            return cls
        return decorator

    #
    # sets up a sqlqlchemy schema from a cerberus schema dict
    # goal is to go seamlessly to NoSql AND to bring validation in
    # the schema definition at once!
    # ONE definition for SQL, NoSQL and Validation.
    # 
    def setup_schema(self, what=""):
        def decorator(cls):
            print("setup_schema:" + cls.__name__.lower())
            #print("what: " + what)
            #print("schema is: " + str(cls.schema))
            #
            # create a sqlalchemy model from the schema
            #
            colclass = None
            
            #
            # now set the right sqlalchemy type for the column
            #
            for elem in cls.schema.keys():
                #print(elem)
                if cls.schema[elem]["type"] == "integer":
                    if "sqltype" in cls.schema[elem]:
                        if cls.schema[elem]["sqltype"].lower() == "biginteger":
                            setattr(cls, elem, Column(elem, BigInteger))
                    else:
                        setattr(cls, elem, Column(elem, Integer))
                elif cls.schema[elem]["type"] == "float":
                    setattr(cls, elem, Column(elem, Float))
                elif cls.schema[elem]["type"] == "string":
                    if "sqltype" in cls.schema[elem]:
                        if cls.schema[elem]["sqltype"].lower() == "text":
                                setattr(cls, elem, Column(elem, Text))
                        elif cls.schema[elem]["sqltype"].lower() == "unicode":
                            if "maxlength" in cls.schema[elem]:
                                setattr(cls, elem, Column(elem, Unicode(length=cls.schema[elem]["maxlength"])))
                            else:
                                setattr(cls, elem, Column(elem, Unicode))
                    else:    
                        if "maxlength" in cls.schema[elem]:
                            setattr(cls, elem, Column(elem, String(length=cls.schema[elem]["maxlength"])))
                        else:
                            setattr(cls, elem, Column(elem, String))
                elif cls.schema[elem]["type"] == "bool":
                    setattr(cls, elem, Column(elem, Boolean))
                elif cls.schema[elem]["type"] == "date":
                    setattr(cls, elem, Column(elem, Date))
                elif cls.schema[elem]["type"] == "datetime":
                    setattr(cls, elem, Column(elem, DateTime))
                elif cls.schema[elem]["type"] == "number":
                    setattr(cls, elem, Column(elem, Numeric))
                else:
                    raise Exception("Wrong Datatype in schema") 
            
            return cls
        return decorator


relation = powDecNew()

