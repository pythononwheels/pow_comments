from pow_comments.handlers.base import BaseHandler
from pow_comments.models.comment import Comment
from pow_comments.config import myapp, database
from pow_comments.application import app
import tornado.web

@app.add_rest_routes("comment")
class commentHandler(BaseHandler):

    # 
    # every pow handler automatically gets these RESTful routes
    # thru the @app.add_rest_routes() decorator.
    #
    # 1  GET    /comment        #=> index
    # 2  GET    /comment/1      #=> show
    # 3  GET    /comment/new    #=> new
    # 4  GET    /comment/1/edit #=> edit 
    # 5  GET    /comment/page/1 #=> page
    # 6  GET    /comment/search #=> search
    # 7  PUT    /comment/1      #=> update
    # 8  POST   /comment        #=> create
    # 9  DELETE /comment/1      #=> destroy
    #

    # standard supported http methods are:
    # SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT", "OPTIONS")
    # you can overwrite any of those directly or leave the @add_rest_routes out to have a basic 
    # handler.

    def show(self, id=None):
        m=Comment()
        res=m.find_one(Comment.id==id)
        self.success(message="Comment show", data=res.json_dump())

    def index(self):
        m=Comment()
        res = m.find_all(as_json=True)
        self.success(message="Comment, index", data=res)         
    
    def page(self, page=0):
        m=Comment()
        page_size=myapp["page_size"]
        if database["type"] == "sqlite":
            limit=page_size
        else:
            limit=(page*page_size)+page_size
        res = m.find_all(as_json=True, 
            limit=limit,
            offset=page*page_size
            )
        self.success(message="Comment page: #" +str(page), data=res )  

    @tornado.web.authenticated
    def edit(self, id=None):
        self.success(message="Comment, edit id: " + str(id))

    @tornado.web.authenticated
    def new(self):
        self.success("Comment, new")

    @tornado.web.authenticated
    def create(self):
        self.success(message="Comment, create")

    @tornado.web.authenticated
    def update(self, id=None):
        self.success("Comment, update id: " + str(id))

    @tornado.web.authenticated
    def destroy(self, id=None):
        self.success("Comment, destroy id: " + str(id))
