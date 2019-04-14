from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json
from nltk.tokenize import TreebankWordTokenizer
import string
import math
import time

treebank_tokenizer = TreebankWordTokenizer()
wikivoyage = {}
tf_transcripts = {}
word_id_lookup = {}
tf_idf_transcripts = {}
name_id_lookup = {}
data = []
msgs = []

@irsystem.route('/', methods=['GET'])

def search():
    activities = request.args.get('activities')
    likes = request.args.get('likes')
    dislikes = request.args.get('dislikes')
    nearby = request.args.get('nearby')
    returnTypes = request.args.get('Returntypes')
    resultsPerPage = request.args.get('Results_per_page')
    page = request.args.get('page')

    with open ('./data/inverted_index.json') as wil_file:
       inverted_index = json.load(wil_file)

    with open ('./data/word_id_lookup.json') as wil_file:
        word_id_lookup = json.load(wil_file)

    with open ('./data/name_id_lookup.json') as wil_file:
        name_id_lookup = json.load(wil_file)

    with open ('./data/idf.json') as wil_file:
       idf = json.load(wil_file)

    with open ('./data/inverted_dict_id_word.json') as wil_file:
        inverted_dict_id_word = json.load(wil_file)

    with open ('./data/inverted_dict_id_name.json') as wil_file:
        inverted_dict_id_name = json.load(wil_file)

    with open ('./data/doc_norms.json') as wil_file:
        doc_norms = json.load(wil_file)

    if not activities or not likes:
        data = []
        return render_template('search.html', data=data)

    activities = activities.lower()
    activities = activities.split(",")
    activities = [x.strip(' ') for x in activities]
    likes = likes.lower()
    likes = likes.split(",")
    likes = [x.strip(' ') for x in likes]
    dislikes = dislikes.lower()
    dislikes = dislikes.split(",")
    dislikes = [x.strip(' ') for x in dislikes]

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
                #Activity may not be in word_id_lookup
                if token not in word_id_lookup:
                    continue
                token_id = str(word_id_lookup[token])
                if token in inverted_index:
                    query_dict[token] = idf[token_id]
                    for idx,count in inverted_index[token]:
                        ranking[idx] += weight * query_dict[token] * count * idf[token_id]

        sum_sq = 0
        for v in query_dict:
            sum_sq += query_dict[v] * query_dict[v]
        norm_q = math.sqrt(sum_sq)

        for i in range(len(ranking)):
            if float(doc_norms[str(i)]) != 0 and float(norm_q) != 0:
                ranking[i] = (ranking[i]/(float(norm_q) * float(doc_norms[str(i)])), i)
            else:
                ranking[i] = (0, i)

        sorted_ranking = sorted(ranking, key=lambda x: x[0], reverse=True)
        final_ranking = sorted_ranking[:10]
        final_ranking = [inverted_dict_id_name[str(x[1])] for x in final_ranking]
        return final_ranking

    data = cos_sim([activities, likes, dislikes])

    return render_template('search.html', data=data)
