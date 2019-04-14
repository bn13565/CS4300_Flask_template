from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json
from nltk.tokenize import TreebankWordTokenizer
import string
import math
import time

project_name = "Ilan's Cool Project Template"
net_id = "Ilan Filonenko: if56"
treebank_tokenizer = TreebankWordTokenizer()
wikivoyage = {}
tf_transcripts = {}
word_id_lookup = {}
tf_idf_transcripts = {}
name_id_lookup = {}
output_message = "Hey bitches"
data = []
msgs = []

def tokenize(query):
    tokenized_query = treebank_tokenizer.tokenize(query.lower())
    tokenized_set = list(set([x for x in tokenized_query if x not in string.puntuation]))

def tokenize_listings(listing):
    results = ""
    eat = listing['eat']
    for x in eat:
        results+= x['description']
    sleep = listing['sleep']
    for x in sleep:
        results+= x['description']
    drink = listing['drink']
    for x in drink:
        results+= x['description']
    do = listing['do']
    for x in do:
        results+= x['description']
    see = listing['see']
    for x in see:
        results+= x['description']
    return tokenize(results)

@irsystem.route('/', methods=['GET'])

def search():
    activities = request.args.get('activities')
    likes = request.args.get('likes')
    dislikes = request.args.get('dislikes')
    nearby = request.args.get('nearby')
    returnTypes = request.args.get('Returntypes')
    resultsPerPage = request.args.get('Results_per_page')
    page = request.args.get('page')

    tfidf_array = []
    tf_array = []

    # with open ('./data/tfidf.pickle', 'rb') as f:
    #     tf_idf_transcripts = pickle.load(f)
    #     tfidf_array = tf_idf_transcripts.toarray()

    #start_time = time.time()

    # with open ('./data/tf.pickle', 'rb') as f:
    #     tf_transcripts = pickle.load(f)
    #     tf_array = tf_transcripts.toarray()

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

    #print(time.time() - start_time)

    #start_time = time.time()


    #print(time.time() - start_time)

    if not activities or not likes:
        data = []
        return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

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

    #start_time = time.time()
    data = cos_sim([activities, likes, dislikes])
    #print(time.time() - start_time)

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


# with open ('./data/preprocessed_wikivoyage.json') as pwn_file:
#     wikivoyage = json.load(pwn_file)

# for p, r in wikivoyage:
#     tokens = tokenize_listings(r['listings'])
#     msgs.append((p,tokens))
# result = {}
# for i in range(len(msgs)):
#     token_set  = msgs[i][1]
#     for token in token_set:
#         if token in result:
#             result[token].append((msgs[i][0], token_set.count(token)))
#         else:
#             result[token]  = ((msgs[i][0], token_set.count(token)))
