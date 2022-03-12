# Import the database object (db) from the main application module
from datetime import datetime
from app import db
from pypinyin import pinyin,Style

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a User model
class Characters(Base):

    __tablename__ = 'characters'
    # which character
    name    = db.Column(db.String(8),  nullable=False)
    showingTimes = db.Column(db.Integer,default = 0)
    lastShown = db.Column(db.DateTime, nullable=True)
    probability = db.Column(db.Float)
    known = db.Column(db.Boolean, default=False)
    learning = db.Column(db.Boolean,default=False)
    pinyin = db.Column(db.String(100))


    # New instance instantiation procedure
    def __init__(self, name):
        self.name   = name
        self.getPinyin()
    
    def getPinyin(self):
        self.pinyin = pinyin(self.name,style=Style.TONE3)[0][0]

    def toJson(self):
        return {
            'name': self.name,
            'probability': self.probability,
            'pinyin': self.pinyin
        }
    
    def updateShowing(self):
        self.lastShown = datetime.now()
        self.showingTimes +=1

    def __repr__(self):
        return '<%r>' % (self.name)  



