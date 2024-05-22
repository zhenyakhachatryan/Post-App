from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime,timezone


db=SQLAlchemy()

class USER(UserMixin,db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    full_name=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(60),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    last_seen=db.Column(db.DateTime, default=datetime.now(timezone.utc))

       

class POST(db.Model):
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    user=db.relationship('USER',backref=db.backref('posts',lazy=True))
    post=db.Column(db.Text,nullable=False)
    images=db.Column(db.String(100),nullable=True)
    post_date=db.Column(db.DateTime,default=datetime.now(timezone.utc))
  
    
class LIKE(db.Model):
    __tablename__='likes'
    id=db.Column(db.Integer,primary_key=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    user = db.relationship('USER', backref=db.backref('likes', lazy=True))
    post = db.relationship('POST', backref=db.backref('likes', lazy=True))    

class COMMENT(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    user=db.relationship('USER',backref=db.backref('comments',lazy=True))
    comment=db.Column(db.Text,nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('posts.id'),nullable=False)
    post=db.relationship('POST',backref=db.backref('comments',lazy=True))
    date=db.Column(db.DateTime,default=datetime.now(timezone.utc))
    answer=db.Column(db.Boolean,default=False,nullable=False)
    recipient=db.Column(db.Integer,default=0,nullable=False)
    


       
