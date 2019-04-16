from . import *
from app import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json
import string
import math
import time
import re
from nltk.stem import WordNetLemmatizer

@irsystem.route('/', methods=['GET'])
def search():
    activities = request.args.get('activities')
    likes = request.args.get('likes')
    dislikes = request.args.get('dislikes')
    nearby = request.args.get('nearby')
    returnTypes = request.args.get('Returntypes')
    wnl = WordNetLemmatizer()

    if not activities and not likes:
        return render_template('search.html', data=[])

    inverted_index = None 
    word_id_lookup = None 
    name_id_lookup = None
    idf = None
    inverted_dict_id_word = None
    inverted_dict_id_name = None
    doc_norms = None
    niche_value = None
    reviews_data = None
    wikivoyage_lite = None

    with app.open_resource('static/data/inverted_index.json') as wil_file:
        inverted_index = json.load(wil_file)

    with app.open_resource('static/data/word_id_lookup.json') as wil_file:
        word_id_lookup = json.load(wil_file)

    with app.open_resource('static/data/name_id_lookup.json') as wil_file:
        name_id_lookup = json.load(wil_file)

    with app.open_resource('static/data/idf.json') as wil_file:
        idf = json.load(wil_file)

    with app.open_resource('static/data/inverted_dict_id_word.json') as wil_file:
        inverted_dict_id_word = json.load(wil_file)

    with app.open_resource('static/data/inverted_dict_id_name.json') as wil_file:
        inverted_dict_id_name = json.load(wil_file)

    with app.open_resource('static/data/doc_norms.json') as wil_file:
        doc_norms = json.load(wil_file)

    with app.open_resource('static/data/nicheness.json') as wil_file:
        niche_value = json.load(wil_file)

    with app.open_resource('static/data/new_combined_reddit.json') as wil_file:
        reviews_data = json.load(wil_file)

    with app.open_resource('static/data/wikivoyage_lite_relevant.json') as wil_file:
        wikivoyage_lite = json.load(wil_file)

    # results
    results_list = []
    # entry fields
    name = "name"
    reviews = "reviews"
    nicheness = "nicheness"
    sim = "sim"
    url = "url"

    activities = activities.lower()
    activities = re.findall(r'[^,\s]+', activities)
    likes = likes.lower()
    likes = re.findall(r'[^,\s]+', likes)
    dislikes = dislikes.lower()
    dislikes = re.findall(r'[^,\s]+', dislikes)

    def cos_sim(query):
        query_dict = {}
        ranking = [0] * len(doc_norms)
        for query_type in range(len(query)):
            if query_type == 0:
                weight = 2
            elif query_type == 1:
                weight = 1
            else:
                weight = -1
            for token in set(query[query_type]):
                token = wnl.lemmatize(token)
                # Activity may not be in word_id_lookup
                if token not in word_id_lookup:
                    continue
                token_id = str(word_id_lookup[token])
                if token in inverted_index:
                    query_dict[token] = idf[token_id]
                    for idx, count in inverted_index[token]:
                        ranking[idx] += weight * \
                            query_dict[token] * count * idf[token_id]

        sum_sq = 0
        for v in query_dict:
            sum_sq += query_dict[v] * query_dict[v]
        norm_q = math.sqrt(sum_sq)

        for i in range(len(ranking)):
            if inverted_dict_id_name[str(i)] in wikivoyage_lite and float(doc_norms[str(i)]) != 0 and float(norm_q) != 0:
                ranking[i] = (ranking[i]/(float(norm_q) * float(doc_norms[str(i)])), i)
            else:
                ranking[i] = (0,i)

        sorted_ranking = sorted(ranking, key=lambda x: x[0], reverse=True)
        final_ranking = sorted_ranking[:50]
        final_ranking = [
            (inverted_dict_id_name[str(x[1])], x[0]) for x in final_ranking]
        return final_ranking

    def boolean_search(query):
        ranking = [0] * len(doc_norms)
        for query_type in range(len(query)):
            if query_type == 0:
                weight = 2
            elif query_type == 1:
                weight = 1
            else:
                weight = -1
            for token in set(query[query_type]):
                # Activity may not be in word_id_lookup
                if token not in word_id_lookup:
                    continue
                token_id = str(word_id_lookup[token])
                if token in inverted_index:
                    for idx, count in inverted_index[token]:
                        ranking[idx] += weight * count

        ranking = [(ranking[i], i) for i in range(len(ranking)) if inverted_dict_id_name[str(i)] in wikivoyage_lite]

        sorted_ranking = sorted(ranking, key=lambda x: x[0], reverse=True)
        final_ranking = sorted_ranking[:20]
        final_ranking = [
            (inverted_dict_id_name[str(x[1])], x[0]) for x in final_ranking]
        return final_ranking

    #data = cos_sim([activities, likes, dislikes])
    data = boolean_search([activities, likes, dislikes])

    sim_niche_list = []
    for loc in data:
        niche_score = niche_value[loc[0]]
        sim_niche_list.append((loc[0], niche_score, loc[1]))

    # sort by niche value
    sim_sorted_by_niche = sorted(
        sim_niche_list, key=lambda x: x[1], reverse=True)
    top_10 = sim_sorted_by_niche[:10]

    def get_reviews(locs):
        revs = reviews_data[locs]
        return revs

    for loc in top_10:
        entry = {}
        entry[name] = wikivoyage_lite[loc[0]]['title']
        entry[reviews] = get_reviews(loc[0])
        entry[nicheness] = str(round(loc[1],2))
        entry[sim] = str(round(loc[2],2))
        entry[url] = wikivoyage_lite[loc[0]]['url']
        results_list.append(entry)

    data = results_list

    return render_template('search.html', data=data)
