__author__ = "Vanshita Sehrawat"

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cassandra.cluster import Cluster
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
vsession = cluster.connect()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db =SQLAlchemy(app)


class TableContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return 'Table Content' + str(self.id)




@app.route('/')
def index():
    return render_template('index.html')
@app.route('/posts', methods=['GET','POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = TableContent(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = TableContent.query.order_by(TableContent.date_posted).all()
        return render_template('posts.html', posts=all_posts)
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = TableContent.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')
@app.route('/posts/edit/<int:id>', methods=['GET','POST'])
def edit(id):
    post = TableContent.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)




@app.route('/home/users/<string:name>/posts/<int:id>')
def hello_world(name, id):
    return 'Hello,' + name + ", you id is: " + str(id)

@app.route('/onlyget', methods = ['GET'])
def get_req():
    return 'you can only get this webpage.1'
if __name__ == '__main__':
    app.run(host='0.0.0.0')
