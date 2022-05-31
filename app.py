from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:VERT50VINT60@localhost/db_lab3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    __tablename__ = 'Articles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='article', lazy=True)

    def __init__(self, title, description, content):
        self.title = title
        self.description = description
        self.content = content

    def __repr__(self):
        return '<Article %r>' % self.id


class Comment(db.Model):
    __tablename__ = 'Comments'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)

    article_id = db.Column(db.Integer, db.ForeignKey('Articles.id', ondelete='CASCADE'))

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return '<Comment %r>' % self.id



@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


# articles

@app.route('/articles')
def articles():
    articles = Article.query.order_by(Article.date.desc()).all()

    return render_template('articles.html', articles=articles)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']

        if not title or not description or not content:
            return 'Fields cannot be empty!'
        
        article = Article(title, description, content)

        db.session.add(article)
        db.session.commit()
        
        return redirect('/articles')

    return render_template('create-article.html')


@app.route('/articles/<int:id>')
def get_article(id):
    article = Article.query.filter_by(id=id).first()

    return render_template('get-article.html', article=article)


@app.route('/articles/<int:id>/update', methods=['POST', 'GET'])
def update_article(id):
    article = Article.query.filter_by(id=id).first()

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']

        if not title or not description or not content:
            return 'Fields cannot be empty!!'
        
        article.title = title
        article.descripion = description
        article.content = content

        db.session.commit()

        return redirect('/articles')

    return render_template('update-article.html', article=article)


@app.route('/articles/<int:id>/delete')
def delete_article(id):
    article = Article.query.filter_by(id=id).first()

    if article:
        db.session.delete(article)
        db.session.commit()

        return redirect('/articles')
    else:
        return 'Object not found!'


# comments

@app.route('/article/<int:article_id>', methods=['POST', 'GET'])
def create_comment(article_id):
    article = Article.query.filter_by(id=article_id).first()

    if request.method == 'POST':
        content = request.form['content']

        if not content:
            return 'Comment cannot be empty!!'
        
        comment = Comment(content)
        comment.article = article

        db.session.add(comment)
        db.session.commit()

    return redirect(f'/articles/{article_id}')


@app.route('/articles/<int:article_id>/comments/<int:comment_id>/update', methods=['POST', 'GET'])
def update_comment(article_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if request.method == 'POST':
        content = request.form['content']

        if not content:
            return 'Comment cannot be empty!'

        comment.content = content
        db.session.commit()

        return redirect(f'/articles/{article_id}')

    return render_template('update-comment.html', comment=comment)


@app.route('/articles/<int:article_id>/comments/<int:comment_id>/delete')
def delete_comment(article_id, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        return 'Object not found!'
    
    db.session.delete(comment)
    db.session.commit()

    return redirect(f'/articles/{article_id}')


if __name__ == '__main__':
    app.run(debug=True)
