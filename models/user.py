#
# Model
#
from sqlalchemy import Column, Integer, String, Sequence, Text
from pow_comments.powlib import relation
from pow_comments.dblib import Base 

#@relation.many_to_many("groups")
class User(Base):
    login = Column(String)
    password = Column(String)
    #email = Column(String)
    #test = Column(Text)
    
    # init
    def __init__(self, **kwargs):
        self.init_on_load(**kwargs)

    # your methods down here