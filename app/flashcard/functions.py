from tkinter import E
# from app.flashcard.models import UserTestCharacterResult, Characters, ChineseTexts
# from datetime import datetime
# one get or create function to use
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance

def recommended(user,textnumber=1, wordsnumber=5,characternumber=8):
    '''
    input: user
    output: {
        'text': [],
        'words':[],
        'characters': [],
    }
    '''

    pass
    # currentstatus = {
    #     'text':[],
    #     'words': [],
    #     'characters':[]
    # }

    # # get the current learning status of user
    # try: 
    #     testresult_false = UserTestCharacterResult.query.filter(known=False).limit(characternumber).all()
    #     testresult_lasttrue = UserTestCharacterResult.query.filter(known=True).last()
    # except Exception as e:
    #     return e

    # if len(testresult_false) < characternumber:
    #     characters = testresult_false + UserTestCharacterResult.query.filter(id>testresult_lasttrue.id).limit(characternumber).all()
    # else:
    #     characters = testresult_false

    # currentstatus['characters'] = [character.toJson for character in characters]

    # # get current learning texts


    # # get current learning words


    # return currentstatus

    

        


    

