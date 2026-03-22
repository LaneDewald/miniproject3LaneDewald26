# MiniProject3LaneDewald
### INF601 - Advanced Programming in Python
### Lane Dewald
### Mini Project 3

#imports
from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watchlist.db'

db = SQLAlchemy(app)


# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    movies = db.relationship('Movie', backref='owner', lazy=True)


# Movie table
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(80))
    watched = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash('Username already taken.', 'danger')
        else:
            hashed = generate_password_hash(password)
            new_user = User(username=username, password=hashed)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in!', 'success')
            return redirect(url_for('watchlist'))
        else:
            flash('Incorrect username or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/watchlist')
def watchlist():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    movies = Movie.query.filter_by(user_id=session['user_id']).all()
    return render_template('watchlist.html', movies=movies)


@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if 'user_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']

        movie = Movie(title=title, genre=genre, user_id=session['user_id'])
        db.session.add(movie)
        db.session.commit()
        flash(f'"{title}" added!', 'success')
        return redirect(url_for('watchlist'))

    return render_template('add_movie.html')


@app.route('/toggle/<int:movie_id>')
def toggle_watched(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    movie.watched = not movie.watched
    db.session.commit()
    return redirect(url_for('watchlist'))


@app.route('/delete/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie removed.', 'info')
    return redirect(url_for('watchlist'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)