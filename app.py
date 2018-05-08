from flask import Flask, render_template, request
from function import *
import json

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
        if type_search == 'place':
            emplacement = get_emplacement_maps(information)
            dict_information = {'emplacement': emplacement, 'type_search': type_search}
        elif type_search == 'information':
            description = get_description_wiki(information)
            dict_information = {'description': description, 'type_search': type_search}
        elif type_search == 'place information':
            emplacement = get_emplacement_maps(information)
            description = get_description_wiki(information)
            dict_information = {'emplacement': emplacement, 'description': description, 'type_search':type_search}
        else:
            dict_information = {'type_search': 'error'}
        return json.dumps(dict_information)

if __name__ == '__main__':
    app.run(debug=True)
