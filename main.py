from flask import Flask, redirect, render_template, request, url_for, session, flash
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

    def __init__(self, name, body, user):
        self.name = name
        self.body = body
        self.owner_id = user.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    posts = db.relationship('Blogpost', backref='user', lazy='dynamic')

    def get_user_by_username(username):
        return User.query.filter_by(username=username).first()

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'blog', 'index']
    print(request.endpoint)
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('login')


@app.route('/', methods=['GET', 'POST'])
def index():
    users = User.query.all()
    return render_template("index.html", title="Blogz", users=users)

@app.route('/blog')
def blog():

    owner_id = request.args.get('user')
    post_id = request.args.get('id')

    if owner_id:
        posts = Blogpost.query.filter_by(owner_id=owner_id).all()
        return render_template("blog.html", title="Blogz", posts=posts)
    elif post_id:
        post = Blogpost.query.get(post_id)
        return render_template("blogpost.html", title="Blogz", post=post)
    else:
        posts = Blogpost.query.all()
        return render_template("blog.html", title="Blogz", posts=posts)
    

@app.route('/newpost', methods=['GET', 'POST'])
def newpost():

    if session['username']:
        user = User.get_user_by_username(session['username'])

        # if this user is not found redirect to login
        if not user:
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


    if request.method == 'POST':

        name = request.form['name']
        body = request.form['body']
        author = user
    
        post = Blogpost(name, body, author)
        db.session.add(post)
        db.session.commit()
        
        #redirect to index if succesful
        return redirect(url_for("blog", id=post.id))

    else :
        return render_template("newpost.html",title="New Post")




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/newpost')
        elif user and user.password != password:
            flash('User password incorrect', 'error')
        else:
            flash('User does not exist', 'error')

    return render_template('login.html') 
        

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        if username == '' or password == '' or verify == '':
            flash("One or more fields are empty", "error")
            return redirect('/signup')

        if password != verify:
            flash("Your passwords did not match", "error")
            return redirect('/signup')

        if len(username) < 3:
            flash("Your username cannot be less than three characters", "error")
            return redirect('/signup')

        if len(password) < 3:
            flash("Your username cannot be less than three characters", "error")
            return redirect('/signup')

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash("Username already existing_user", "error")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
