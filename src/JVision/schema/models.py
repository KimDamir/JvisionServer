from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    queries = db.relationship('OcrQuery', back_populates='user')
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        super().__init__()
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class OcrQuery(db.Model):
    __tablename__ = 'queries'
    id = db.Column(db.Integer, primary_key=True)
    writing = db.Column(db.String(50), nullable=False)
    translation = db.Column(db.String(50))
    query_text = db.Column(db.String(50))
    time = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='queries')
    
    def __init__(self, writing, translation, query_text, time, user_id):
        self.writing = writing
        self.translation = translation
        self.query_text = query_text
        self.time = time
        self.user_id = user_id
        super().__init__()
    
    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'writing': self.writing,
           'translation': self.translation,
           'query_text': self.query_text,
           'time': self.time
       }