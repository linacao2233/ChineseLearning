from app.flashcard.models import Characters
from app import db

import json

Config = {
    'file': '/Users/linacao/Documents/personalWork/ChineseLearning/text.json'
}

def loadCharacters():

    with open(Config['file'],'r', encoding='utf-8') as file:
        texts = json.load(file)

    # get all new charcters
    chars = ''.join(texts['newCharacters'].values())
    for char in chars:
        newchar = Characters(char)
        db.session.add(newchar)
        db.session.commit()

    return 0

def deleteCharacters():
    ''' this will delete all the characters in database, be careful while using'''
    pass

def cleanCharacters():
    '''this function checks all the duplicate characters in database and clean them'''

    pass

def updatepinyin():
    characters = Characters.query.all()
    for character in characters:
        character.getPinyin()
        db.session.commit()
    
    return 0


