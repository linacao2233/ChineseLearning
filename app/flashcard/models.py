# Import the database object (db) from the main application module
from datetime import datetime
from email.policy import default
from app import db
from pypinyin import pinyin,Style
from app.flashcard.functions import get_or_create

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

    characterProgress = db.relationship('UserCharacterProgress',
                                        backref='characters',
                                        lazy = True)
    testCharacterResult = db.relationship('UserTestCharacterResult',
                                        backref='characters',
                                        lazy = True)

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


class User(Base):
    __tablename__ = 'user'
    name = db.Column(db.String(100))
    characterProgress = db.relationship('UserCharacterProgress',
                                        backref='user',
                                        lazy = True)
    testCharacterResult = db.relationship('UserTestCharacterResult',
                                        backref='user',
                                        lazy = True)
    testScoreRecord = db.relationship('UserTestScoreRecord',
                                        backref='user',
                                        lazy = True)  

    def __init__(self,name):
        self.name = name 

class UserCharacterProgress(Base):
    __tablename__ = 'userProgress'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

    showingTimes = db.Column(db.Integer,default = 0)
    lastShown = db.Column(db.DateTime, nullable=True)
    probability = db.Column(db.Float)
    known = db.Column(db.Boolean, default=False)
    learning = db.Column(db.Boolean,default=False)

    def __init__(self,user,character):
        self.user_id = User.query.filter_by(name=user).first().id
        self.character_id = Characters.query.filter_by(name=character).first().id

    
class UserTestCharacterResult(Base):
    __tablename__ = 'userTestCharacterResult'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testtime = db.Column(db.DateTime)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    testresult = db.Column(db.Boolean, default=False)

    def __init__(self,user,character,result,time=datetime.now()):
        #self.user_id = User.query.filter_by(name=user).first().id
        #self.character_id = Characters.query.filter_by(name=character).first().id
        self.user_id = get_or_create(db.session, User, name=user).id
        self.character_id = get_or_create(db.session,Characters, name=character).id
        self.testresult = result
        self.testtime = time

    def toJson(self):
        return {
            'name': self.user.name,
            'character': self.characters.name,
            'result': self.testresult
        }

class UserTestScoreRecord(Base):
    __tablename__ = 'scorerecord'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    testtime = db.Column(db.DateTime)
    testscore = db.Column(db.Integer, default = 0)

    def __init__(self,user,score,time=datetime.now()):
         self.user_id = get_or_create(db.session,User,name=user).id
         self.testscore = score
         self.testtime = time
       



