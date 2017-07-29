from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#sets the database

app.secret_key = 'A0Zr98j/2yX R~XHH!jmN]LWX/,?RT'
#sets the secret key


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(120))
    #this column is a string of up to 120 chars in length holding the title of the post
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner_id):
        self.name = name
        self.body = body

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blogpost', backref='user', lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        self.password = password

posts = []

@app.route('/', methods=['GET', 'POST'])
def index():
    posts = Blogpost.query.all()
    return render_template("blog.html", title="Build-A-Blog", posts=posts)

@app.route('/blog')
def blog():
    post_id = request.args.get('id')
    post = Blogpost.query.get(post_id)
    return render_template("blogpost.html", title="Build-A-Blog", post=post)

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

    if request.method == 'POST':
        name = request.form['name']
        body = request.form['body']

        # you need to remove the hardcoded value here and get it from the login
        owner_id = 1

        post = Blogpost(name, body, owner_id)
        db.session.add(post)
        db.session.commit()
        
        #redirect to index if succesful
        return redirect(url_for("blog", id=post.id))

    else :
        return render_template("newpost.html",title="New Post")

@app.route('/login', methods=['GET', 'POST'])
def login():

@app.route('signup', methods=['GET', 'POST'])
def signup():
    #template defaults
    signup_fields = {}
    signup_errors = {}
    signup_has_error = False

    if request.method == 'POST':
        #sets values for the fields
        signup_fields['username'] = request.form['username']
        signup_fields['password'] = request.form['password']
        signup_fields['password_confirm'] = request.form['password_confirm']

        # error for username
        if not signup_fields['username'] or len(signup_fields['username']) < 3 #or signup_fields['username'] in(whatever the database list of usernames is):
            errors['username'] = "Complete the username field. Must be 3 characters or more"
            has_error = True

        # error for password
        if not signup_fields['password'] or len(signup_fields['password']) < 3:
            errors['password'] = "Password is invalid. Must be 3 characters or more and less than 20 characters with no spaces"
            has_error = True

        # error for password_confirm
        if signup_fields['password']  != signup_fields['password_confirm']:
            errors['password_confirm'] = "Passwords do not match"
            has_error = True

if __name__ == '__main__':
    app.run(debug=True)
