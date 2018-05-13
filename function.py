import sys
import googlemaps
import wikipedia
from googletrans import Translator
from vocabulary import *

API_KEY = 'AIzaSyAU03xryXnIa2xywviwVyWP_src_KALY-I'
CSE_ID = '009839873311021651636:ffnd3ndvdby'


def parse_sentance(sentance):
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
    return sentance


def translate(text):
    translator = Translator()
    text_translate = translator.translate(text, dest='fr').text
    return text_translate


def get_emplacement_maps(search):
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
    try:
        wikipedia.set_lang("fr")
        srch = wikipedia.search(search, "html.parser")
        data = wikipedia.page(srch, "html.parser").content
        data = data.split('.')
        desc = ''
        for d in data[:3]:
            desc = desc + str(d.encode(sys.stdout.encoding, errors='replace')) + '.'
        desc = parse_sentance(desc)
        return desc
    except:
        return False


def get_type_place(place):
    try:
        types_place_maps = get_emplacement_maps(place)['types'].split('/')
        for type in types_place_maps:
            if type in KEYS_WORDS_ABOUT_EMPLACEMENT:
                return type
        return False
    except:
        return False


def extract_information_request(sentance):
    sentance = sentance.replace('?', '')
    sentance = sentance.replace('.', '')
    dict_request = {}
    is_search_emplacement = False
    is_search_information = False
    is_search_on_all_sentance = False
    list_words = sentance.split(' ')
    information = None
    for word in list_words:
        if word in WORD_ABOUT_EMPLACEMENT:
            is_search_emplacement = True
        if word in WORD_ABOUT_INFORMATION:
            is_search_information = True

    if is_search_information == False and is_search_emplacement == False:
        type_search = 'place description'
        is_search_on_all_sentance = True
    elif is_search_information == True and is_search_emplacement == True:
        type_search = 'place description'
    elif is_search_information == True and is_search_emplacement == False:
        type_search = 'description'
    elif is_search_information == False and is_search_emplacement == True:
        type_search = 'place'
    dict_request['type_search'] = type_search

    # Extract the keys word from request
    if is_search_on_all_sentance:
        dict_request['information'] = sentance
    else:
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
    error = check_information_valide(information, type_search)
    dict_request.update(error)
    return dict_request


def check_information_valide(information, type_search):
    dict_error = {'error_place': False, 'error_description': False}
    if type_search == 'place':
        place_check = get_emplacement_maps(information)
        if not place_check:
            dict_error['error_place'] = True
    elif type_search == 'information':
        information_check = get_description_wiki(information)
        if not information_check:
            dict_error['error_description'] = True
    elif type_search == 'place information':
        place_check = get_emplacement_maps(information)
        information_check = get_description_wiki(information)
        if not place_check and not information_check:
            dict_error['error_place'] = True
            dict_error['error_description'] = True
        if not place_check:
            dict_error['error_place'] = True
        elif not information_check:
            dict_error['error_description'] = True
    return dict_error


# def get_type_search(sentance):
#     sentance = sentance.lower()
#     list_word = sentance.split(" ")
#     if len(list_word) == 1:
#         word = list_word[0]
#         type_place = get_type_place(word)
#         if type_place is not False:
#             return 'place'
#         else:
#             wiki = get_description_wiki(word)
#             if wiki is not False:
#                 return 'information'
#     else:
#         is_place = False
#         type_place = get_type_place(sentance)
#         if type_place is not False:
#             return 'place'
#         else:
#             for word in list_word:
#                 if word in WORD_ABOUT_EMPLACEMENT:
#                     is_place = True
#             if is_place:
#                 return 'place information'
#             else:
#                 return 'information'
#     return 'error'

