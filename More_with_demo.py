from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="Unknow")
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return "Blog post " + str(self.id)


# all_posts = [
#     {
#         'title': 'Post 1',
#         'content': 'Contents of Post 1 will be here',
#         'author': 'Adams'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'Contents of Post 2 will be here too 2'
#     }
# ]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/posts', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_author = request.form['author']
        post_title = request.form['title']
        post_content = request.form['content']
        new_posts = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_posts)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
    return render_template('posts.html', posts=all_posts)


@app.route('/home/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == "POST":
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_posts = BlogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_posts)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

    # @app.route('/home/<string:name>')
    # def hello(name):
    #     return "Hello World, " + name + " is my name .I am learning flask"
    # @app.route('/onlyget', methods=['GET'])
    # def get_only():
    #     return "You can only get this webpage, 4"


if __name__ == "__main__":
    app.run(debug=True)
