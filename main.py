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

