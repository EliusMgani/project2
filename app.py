from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db = SQLAlchemy(app)


all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the Content of the Post 1. LAlalalala.',
        'author': 'Lee'
    },
    {
        'title': 'Post 2',
        'content': 'This is the Content of the Post 2. LAlalalala.',
        'author': 'Jar'
    },
    {
        'title': 'Post 3',
        'content': 'This is the Content of the Post 3. LAlalalala.'
    }
]


@app.route('/')
def home():
    return '<h1>Sheet.. Give me that, Please..!!</h1>'


@app.route('/hello')
def hello():
    return 'Hello World..!!'


@app.route('/user/<string:name>')
def user(name):
    return 'My Name is ' + name


@app.route('/hey/<string:name>/get/<int:id>')
def hey(name, id):
    return 'My Name is ' + name + ' and My Id is ' + str(id)


@app.route('/index')
def index():
    return render_template('index.html')


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(50), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return '< BlogPost %r >' % self.id


@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'There was a Problem When Posting a Post, Try Again Later..'

    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'There is a Problem When Deleting, Try Again later..!!'


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']

        try:
            db.session.commit()
            return redirect('/posts')

        except:
            return 'Check Well Your Spelling and Try Again Later..!!'
    else:
        return render_template('/edit.html', post=post)


@app.route('/posts/new/', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')

        except:
            return 'There was a Problem When Posting a Post, Try Again Later..'

    else:
        return render_template('new_posts.html')


if __name__ == '__main__':
    app.run(debug=True)