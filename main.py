#build-a-blog, 3/19/17 11:59 - working copy - WIP
import os
import webapp2
import jinja2   #the template language used to render the html

from google.appengine.ext import db

#use templates instead of string substitutions; autoescapes are used for each variable
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape=True)  #automaticaly auto escapes  all user input fields

class Handler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    #takes a template and returns a string of the rendered template
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)  #calls jinja to load file name stored in (template)
        return t.render(params)

    #writes the string
    def render(self, template, **kw):   #pass the template, and the fields to single.HTML TEMPLATE -SEE FLICKLIST6
        self.write(self.render_str(template, **kw))

#====add the database -Define the entity by creating a class; inherits from import db, model defines the id
class Post(db.Model):
     # "required = True" is a constratint:indicates that a StringProperty is
    #  required to create an instance of Post class
    title = db.StringProperty(required = True)
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#writes output to the browser
class MainPage(Handler):
     #render forms while preserving fields
    def render_front(self):
        posts = db.GqlQuery("SELECT * FROM Post "         #throws an ERROR if there's not a space after Post and ending quote
                            "ORDER BY created DESC limit 5 ")
        # pass infornation to our template
        self.render("front.html", posts = posts)

    #render the blank form
    def get(self):
        self.render_front()

class NewPost(Handler):
     #render forms while preserving fields
    def render_newpost(self, title = "", post = "", error = ""):
        self.render("newpost.html", title = title, post = post, error = error)
    #render the blank form
    def get(self):
        self.render_newpost()

    def post(self):
        title = self.request.get("title")  #what user typed
        post = self.request.get("post")

        if title and post:
            a = Post(title = title, post = post) #creating a new instance of art (datetime is autocreated so no need to pass it in)
            a.put() #stores new art object in the database
            blogid = a.key().id()
            self.redirect("/Blog/%s"% str(blogid))
        else:
            error = "we need both a title and post!."
        # renders form with the error message; if error return what was entered plus error message
            self.render_newpost(title, post, error)

class BlogPage(Handler):
    def get(self, id):
        #look up the blog post: get id using function get_by_id & convert id to integer
        blogpost = Post.get_by_id(int(id))
        if blogpost == None:
            error = "The id is not valid"
            self.response.write(error)
            # self.render("BlogPage.html", blogpost = blogpost)
        else:
            self.response.write(blogpost.title)
            self.response.write("<br>")
            self.response.write(blogpost.post)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    webapp2.Route('/Blog/<id:\d+>', BlogPage),
    ('/Blog/newpost', NewPost)
    ], debug=True)
