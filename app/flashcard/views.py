# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
# from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
import json

# Import module forms

from app.flashcard.models import Characters

# Define the blueprint: 'auth', set its url prefix: app.url/auth
flashcard = Blueprint('flashcard', __name__, url_prefix='/flashcard')

# Set the route and accepted methods
@flashcard.route('/', methods=['GET', 'POST'])
def get_cards():
    args = request.args
    number = int(args.get('n',8))
    page = int(args.get('page',1))

    chars_page = Characters.query.paginate(page=page, per_page=number)

    chars = chars_page.items

    jsonfiles = [{'name': a.name, 'pinyin':a.pinyin} for a in chars]
    response = jsonify(jsonfiles)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

