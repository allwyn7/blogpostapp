from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

application = Flask(__name__)
with application.app_context():
    application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(application)

    class BlogPost(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(100), nullable=False)
        content = db.Column(db.Text, nullable=False)
        author = db.Column(db.String(20), nullable=False, default='N/A')
        date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

        def __repr__(self):
            return "Post No. "+str(self.id)

    # @application.before_first_request
    # def create_tables():
    #     db.create_all()

    @application.route('/')
    def home():
        return render_template('index.html')

    @application.route('/posts', methods = ['GET','POST'])
    def posts():
        if request.method == 'POST':
            post_title = request.form['title']
            post_content = request.form['content']
            new_post = BlogPost(title=post_title, content=post_content, author="Allwyn")
            db.session.add(new_post)
            db.session.commit()
            return redirect('/posts')
        else:
            all_posts = BlogPost.query.order_by(BlogPost.date)
            return render_template('posts.html', users = all_posts)

    @application.route('/posts/delete/<int:id>')
    def delete(id):
        post = BlogPost.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')

    @application.route('/posts/edit/<int:id>', methods=['GET','POST'])
    def edit(id):
        post = BlogPost.query.get_or_404(id)
        if request.method =='POST':
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            return redirect('/posts')
        else:
            return render_template('edit.html', users=post)


if __name__ == "__main__":
    application.run(debug=True)
    