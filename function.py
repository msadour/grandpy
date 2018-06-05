import sys
import googlemaps
import wikipedia
from googletrans import Translator
from vocabulary import *

API_KEY = 'AIzaSyAU03xryXnIa2xywviwVyWP_src_KALY-I'
CSE_ID = '009839873311021651636:ffnd3ndvdby'


def parse_sentance(sentance):
    """
    Clean ut8 character
    :param sentance:
    :return: sentance
    """
    sentance = sentance.replace("b\'", '')
    sentance = sentance.replace("b\'.", '.')
    sentance = sentance.replace(".b", ".")
    sentance = sentance.replace("\'.", '.')
    sentance = sentance.replace('b"\\n', ' ')
    sentance = sentance.replace('"', '')
    sentance = sentance.replace('\\x82', 'é')
    sentance = sentance.replace('\\x90', 'É')
    sentance = sentance.replace('\\x8a', 'è')
    sentance = sentance.replace('\\x88', 'ê')
    sentance = sentance.replace('\\x87', 'c')
    sentance = sentance.replace('\\x85', 'à')
    sentance = sentance.replace('\\x97', 'ù')
    sentance = sentance.replace('?u', 'oeu')

    sentance = sentance.replace('\xc3\xa9', 'é')
    sentance = sentance.replace('\xc3\xa0', 'à')
    sentance = sentance.replace('\xc3\xaa', 'ê')
    sentance = sentance.replace('\xc5\x93', 'oe')

    return sentance


def translate(text, dest):
    """
    (Not used for the moment) Translate a text.
    :param text:
    :return: text_translate
    """
    translator = Translator()
    text_translate = translator.translate(text, dest=dest).text
    return text_translate


def get_emplacement_maps(search):
    """
    Get a emplacement on google maps of the search
    :param search:
    :return: dict_location
    """
    try:
        gmaps = googlemaps.Client(key=API_KEY)
        # Geocoding an address

        geocode_result = gmaps.geocode(search, language='fr')[0]
        dict_location = {}
        for libelle, item in geocode_result.items():
            if libelle == 'formatted_address':
                dict_location['adresse'] = item
            elif libelle == 'geometry':
                dict_location['latitude'] = item['location']['lat']
                dict_location['longitude'] = item['location']['lng']
            elif libelle == 'types':
                dict_location['types'] = '/'.join(item)
        return dict_location
    except:
        return False


def get_description_wiki(search):
    """
    Get a description from wikipedia.
    :param search:
    :return: description
    """
    try:
        wikipedia.set_lang("fr")
        srch = wikipedia.search(search, "html.parser")
        data = wikipedia.page(srch, "html.parser").content
        data = data.split('.')
        description = ''
        for d in data[:3]:
            description = description + str(d.encode(sys.stdout.encoding, errors='replace')) + '.'
            description = parse_sentance(description)
        return description
    except:
        return False


def get_type_place(place):
    """
    (Not used for the moment) Get type of place (city, street...).
    :param place:
    :return: type
    """
    try:
        types_place_maps = get_emplacement_maps(place)['types'].split('/')
        for type in types_place_maps:
            if type in KEYS_WORDS_ABOUT_EMPLACEMENT:
                return type
        return False
    except:
        return False


def extract_information_request(sentance):
    """
    Extract good information from search
    :param sentance:
    :return: dict_request
    """
    sentance = sentance.replace('?', '')
    sentance = sentance.replace('.', '')
    dict_request = {}
    list_words = sentance.split(' ')
    list_words_for_search = list_words
    for word in list_words:
        if "d'" in word:
            list_words_for_search = list_words[list_words.index(word):]
            break
        if word in WORD_ABOUT_WHAT:
            list_words_for_search = list_words[list_words.index(word) + 1:]
            break

    information = " ".join(list_words_for_search)
    information = information.replace("d'", '')
    for word in WORD_PLEASE:
        information = information.replace(word, '')
    dict_request['information'] = information
    type_search = get_type_search(information)
    dict_request['type_search'] = type_search
    error = get_if_error(type_search)
    dict_request.update(error)
    return dict_request


def get_type_search(information):
    """
    return type of search : place, description or twice
    :param information:
    :return: type of search
    """
    emplacement = get_emplacement_maps(information)
    description = get_description_wiki(information)
    if not emplacement and description:
        return 'description'
    elif emplacement and not description:
        return 'place'
    elif emplacement and description:
        return 'place description'
    else:
        return 'error'


def get_if_error(type_search):
    """
    Check (and return if it is) error for a search
    :param type_search:
    :return: error
    """
    dict_error = {'error_place': False, 'error_description': False}
    if type_search == 'place':
        dict_error['error_description'] = True
    elif type_search == 'description':
        dict_error['error_place'] = True
    elif type_search == 'error':
        dict_error['error_place'] = True
        dict_error['error_description'] = True

    return dict_error




