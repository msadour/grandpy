from flask import Flask, render_template, request
from function import *
import json
import random
from vocabulary import *

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/get_user_request', methods=['GET'])
def get_user_request():
    if request.method == "GET":
        request_user = request.args.get('question')
        information_extracted = extract_information_request(request_user)
        type_search = information_extracted['type_search']
        information = information_extracted['information']
        emplacement = get_emplacement_maps(information)
        description = get_description_wiki(information)
        error = get_if_error(type_search)

        if type_search == 'error':
            dict_information = {'type_search': 'error'}
        else:
            dict_information = {'emplacement': emplacement, 'description': description, 'type_search': type_search}

        dict_information.update({'sentance_place': random.choice(SENTANCE_PLACE_GRANDPY),
                                 'sentance_description': random.choice(SENTANCE_DESCRIPTION_GRANDPY)})

        dict_information.update(error)

        return json.dumps(dict_information)

if __name__ == '__main__':
    app.run(debug=True)
