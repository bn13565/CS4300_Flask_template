from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
import pickle
import json
from nltk.tokenize import TreebankWordTokenizer
import string

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

    if not activities:
        print("hi")
        data = []
        return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)

    activities = activities.split(",")
    activities = [x.strip(' ') for x in activities]
    likes = likes.split(",")
    likes = [x.strip(' ') for x in likes]
    dislikes = dislikes.split(",")
    dislikes = [x.strip(' ') for x in dislikes]

    # activities = ['swimming']
    # likes = ['beach']
    # dislikes = ['mountain']
    activities_and_likes = activities + likes

    with open ('./data/word_id_lookup.json') as wil_file:
        word_id_lookup = json.load(wil_file)
    with open ('./data/name_id_lookup.json') as wil_file:
        name_id_lookup = json.load(wil_file)

    inverted_dict_id_word = dict([[v,k] for k,v in word_id_lookup.items()])

    with open ('./data/tf.pickle', 'rb') as f:
        tf_transcripts = pickle.load(f)
        tf_array = tf_transcripts.toarray()

    with open ('./data/inverted_index.json') as wil_file:
       result = json.load(wil_file)

    # result = {}
    # for i in range(len(tf_array)):
    #     for j in range(len(tf_array[i])):
    #         token = inverted_dict_id_word[j]
    #         score = tf_array[i][j]
    #         if score != 0:
    #             if token in result:
    #                 result[token].append((int(i), int(score)))
    #             else:
    #                 result[token] = [(int(i), int(score))]
    #print(result)
    if activities_and_likes[0] in result:
        answer = set([x[0] for x in result[activities_and_likes[0]]])
        for token in activities_and_likes[1:]:
            if token in result:
                docs = [x[0] for x in result[token]]
                answer = answer.intersection(set(docs))
            else:
                answer = []
        answer = list(answer)
        data = answer[:10]

    else:
        data = []


    #print(list(answer))

    # with open('./data/stuff.json', 'w') as outfile:
    #     json.dump(result, outfile)
    #     outfile.write('\n')


    # with open ('./data/tfidf.pickle', 'rb') as f:
    #     tf_idf_transcripts = pickle.load(f)
    #
    # with open ('./data/preprocessed_wikivoyage.json') as pwn_file:
    #     wikivoyage = json.load(pwn_file)

    return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)


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



    # if not activity:
    #     isActivity =
    # else:
    #     output_message = "Your search: " + query
    #     data = range(5)
