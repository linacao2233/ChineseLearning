from app.flashcard.models import *
from app import db

import json,sys

Config = {
    'file': 'static/text.json'
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


def loadTexts():
    with open(Config['file'],'r', encoding='utf-8') as file:
        texts = json.load(file)
    
    for (key,value) in texts['title'].items():
        text = texts['text'].get(key,'')
        words = texts['words'].get(key,'')
        subject = value
        characters = texts['newCharacters'].get(key,[])
        print(characters)

        newtext = ChineseTexts(subject,text,words=words)
        db.session.add(newtext)
        db.session.commit()
        
        newtext.addCharacters(list(characters))

        db.session.add(newtext)
        db.session.commit()


def updateUserProgress():
    '''
    use test results to update user character progress
    '''
    testprogress = UserTestCharacterResult.query.all()
    for test in testprogress:
        result = get_or_create(db.session,UserCharacterProgress,
                  user=test.user.name,
                  character=test.characters.name)
        result.known = test.testresult
        result.lastShown = test.testtime

        db.session.add(result)
        db.session.commit()

def initiateUserProgress():
    '''
    set all learning parameters to be 1, load all characters to user progress
    '''
    chars = Characters.query.all()
    users = User.query.all()

    for user in users:
        for char in chars:
            progressinstance = UserCharacterProgress.query.filter_by(
                             user = user,
                             characters = char
            ).first()

            if progressinstance:
                result = progressinstance
            else:
                result = UserCharacterProgress(user.name,char.name)

            result.learning = False
            result.known = False

            db.session.add(result)
            db.session.commit()


