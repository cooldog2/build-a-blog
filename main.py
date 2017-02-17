#build-a-blog
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
        t = jinja_env.get_template(template)
        return t.render(params)

    #writes the string
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

#====add the database -Define the entity by creating a class; inherits from import db
class Post(db.Model):
    title = db.StringProperty(required = True)    # "required = True" is a constratint:indicates that
                                                  #  a StringProperty is required to create an instance of Art class
    post = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

#writes output to the browser
class MainPage(Handler):
     #render forms while preserving fields
    def render_front(self, title = "", post = "", error = ""):
        posts = db.GqlQuery("SELECT * FROM Post "         #throws an ERROR if there's not a space after Art and ending quote
                            "ORDER BY created DESC ")
        # pass infornation to our template
        self.render("main_page.html", title = title, post = post, error = error, posts= posts)

    #render the blank form
    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")  #what user typed
        post = self.request.get("post")

        # if title and post:
        if title and post:
            #self.write("Thanks")
            a = Post(title = title, post = post) #creating a new instance of art (datetime is autocreated so no need to pass it in)
            a.put()                            #stores new art object in the database
            self.redirect("/")
        else:
            error = "we need both a title and post!."
            #self.render("front.html", error = error)    # put into a seperate function because it will be called from both Get & Post - to avoid having to repeat code
                                                         #new function name is render_front
          #replace above line with this one This renders form with the error message
          #if there is an error, returns what user typed in + the error message
            self.render_front(title, post, error)
        
app = webapp2.WSGIApplication([('/', MainPage)
    # ('/blog, BlogPage)
    ], debug=True)
