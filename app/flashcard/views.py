# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, \
                  flash, g, session, redirect, url_for

import random

# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
import json

# Import module forms

from app.flashcard.models import Characters, UserCharacterProgress, UserTestCharacterResult,UserTestScoreRecord,User
from app.flashcard.functions import get_or_create,recommended

# Define the blueprint: 'auth', set its url prefix: app.url/auth
flashcard = Blueprint('flashcard', __name__, url_prefix='/flashcard')

# Set the route and accepted methods
@flashcard.route('/', methods=['GET', 'POST'])
def get_cards():
    args = request.args
    number = int(args.get('n',8))
    page = int(args.get('page',1))
    user = args.get('user')


    chars_page = Characters.query.paginate(page=page, per_page=number)
    chars = chars_page.items

    jsonfiles = [{'name': a.name, 'pinyin':a.pinyin} for a in chars]
    print(jsonfiles)

    response = jsonify(jsonfiles)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@flashcard.route('/learning', methods=['GET', 'POST'])
def get_learningcards():
    args = request.args
    number = int(args.get('n',8))
    user = args.get('user','Ayla')

#    chars = recommended(user=user,characternumber=number)
    currentstatus = {
        'text':[],
        'words': [],
        'characters':[]
    }
    userid = User.query.filter_by(name=user).first().id

    # get the current learning status of user
    currentlearning = UserCharacterProgress.query.filter_by(
                       learning=True).all()
    learningnumber = len(currentlearning)
    
    # get some notlearning ones
    notlearning = UserCharacterProgress.query.filter_by(learning=False).limit(4*number-learningnumber).all()
    
    combinedlist = currentlearning + notlearning

    for result in combinedlist:
        result.calProbability()
        db.session.add(result)
        db.session.commit()
    
    # return fixed number of characters by calculating probility

    returnlist = random.choices(combinedlist,
                                weights=[x.probability for x in combinedlist],
                                k=number)
    
    jsontoreturn = [x.toJson() for x in returnlist]
    
    return jsonify(jsontoreturn)


@flashcard.route('/updateresult', methods =['GET', 'POST'])
def recordResults():
    user = request.json.get('user','ayla')
    results = request.json.get('testresults')

    addedresults = []

    for (key,value) in results.items():
        characterresult = UserTestCharacterResult(
            user = user,
            character = key,
            result = value,
        )
        db.session.add(characterresult)
        db.session.commit()
        addedresults.append(characterresult.toJson())
    
    response = jsonify(addedresults)
    return response
    

@flashcard.route('/character', methods=['GET', 'POST'])
def get_character_results():
    chars = UserTestCharacterResult.query.all()
    
    jsonfiles = [a.toJson() for a in chars]

    response = jsonify(jsonfiles)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response