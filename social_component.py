import json
import pickle
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy.sparse import csc_matrix
from scipy.sparse.linalg import svds
import re

# with open("./data/name_id_lookup.json", "r") as f:
#     name_ids = json.load(f)
#     results = {}
#     counter = 0
#
#     for key in name_ids:
#         new_key = urllib.parse.urlencode({'q':key})
#
#         url = "https://api.pushshift.io/reddit/search/comment/?&subreddit=travel&fields=score,body&sort_type=score&size=50"
#         api = requests.get(url, new_key)
#         api_call = api.content.decode('utf8').replace("''", '""')
#         api_call = ast.literal_eval(api_call)
#         results[key] = api_call["data"]
#         counter += 1
#         #print(counter)


# with open("./data/reddit.json", "w") as f:
#      json.dump(results, f)
# niche_lst = []
#
# with open("./data/reddit.json", "r") as f:
#      dict = json.load(f)
#      count = 0
#      for key in dict:
#          num_comments = len(dict[key])
#          if num_comments<2:
#              #niche_lst[key] = num_comments
#              niche_lst.append(key)
#
# results_niche = {}
# counter_niche = 0
# # l = list(niche_lst.items())
# #random.shuffle(niche_lst)
# # print(l)
# # niche_lst = dict(l)
# #print(len(niche_lst))
#
# for key in niche_lst:
#     new_key = urllib.parse.urlencode({'q':key})
#     #url = "https://api.pushshift.io/reddit/search/comment/?&fields=score,body,subreddit&sort_type=score&size=25"
#     url = "https://api.pushshift.io/reddit/search/comment/?&subreddit=shoestring,wanderlust,solotravel,travelhacks,backpacking,campingandhiking,adventures,remoteplaces,EarthPorn,MapPorn,VillagePorn,travelphotos,IWantOut,longtermtravel,digitalnomad,hitchiking,onebag,airbnb,travelpartners,cruise,asia,europe,AskEurope,Africa,northamerica,southamerica,Oceania,JapanTravel&fields=score,body&sort_type=score&size=5"
#     api = requests.get(url, new_key)
#     api_call = api.content.decode('utf8').replace("''", '""')
#     api_call = ast.literal_eval(api_call)
#     results_niche[key] = api_call["data"]
#     counter_niche += 1
#     # if len(api_call["data"]) == 0:
#     #     print("oops " + key)
#     if counter_niche % 500 == 0:
#         print(counter_niche)
# if counter_niche == 10:
#     break


# with open("./data/niche_reddit.json", "w") as f:
#      json.dump(results_niche, f)

# dict_new = {}
# lst_new = []
#
# with open("./data/niche_reddit.json", "r") as f:
#      dict_new = json.load(f)
#      count_new = 0
#      for key in dict_new:
#          num_comments = len(dict_new[key])
#          if num_comments<1:
#               count_new += 1
#               #niche_lst[key] = num_comments
#               lst_new.append(key)
#      print(lst_new)

# with open ('./data/preprocessed_wikivoyage_notext.json') as wil_file:
#     places = json.load(wil_file)
#
# inlinks = {}
# counter = 0
# for key,value in places.items():
#     val = value['in_links']
#     inlinks[key] = 0.0
#     if val <= 8:
#         inlinks[key] += 0.25
#     if val <= 3:
#         inlinks[key] += 0.50
#     if key in dict_new:
#         inlinks[key] += 0.25


#
# with open ('./data/inverted_index.json') as wil_file:
#    inverted_index = json.load(wil_file)
#
# with open ('./data/word_id_lookup.json') as wil_file:
#     word_id_lookup = json.load(wil_file)
#
# with open ('./data/name_id_lookup.json') as wil_file:
#     name_id_lookup = json.load(wil_file)
#
# with open ('./data/idf.json') as wil_file:
#    idf = json.load(wil_file)
#
# with open ('./data/inverted_dict_id_word.json') as wil_file:
#     inverted_dict_id_word = json.load(wil_file)
#
# with open ('./data/inverted_dict_id_name.json') as wil_file:
#     inverted_dict_id_name = json.load(wil_file)

# with open ('./data/preprocessed_wikivoyage_notext.json') as wil_file:
#     wiki = json.load(wil_file)
#
# display_names = {}
#
# for key in wiki:
#     display_name = wiki[key]["display_title"]
#     url = "https://en.wikivoyage.org/wiki/" + urllib.parse.quote(display_name)
#     display_names[key] = (display_name, url)
#
# with open("./data/display_name_url.json", "w") as f:
#       json.dump(display_names, f)

# reddit_shortened = {}

# with open('./data/reddit.json') as wil_file:
#     reviews = json.load(wil_file)

# for key in reviews:
#     if len(reviews[key]) > 5:
#         reddit_shortened[key] = reviews[key][:5]
#     else:
#         reddit_shortened[key] = reviews[key]

# urllib.parse.quote("bora bora")

#
# doc_norms = np.zeros(len(tf_array))
# doc_norms_dict = {}
#
# for key in idf:
#     key_name = inverted_dict_id_word[key]
#     for idx,count in inverted_index[key_name]:
#         score = np.square(count * idf[key])
#         doc_norms[idx] += score
#
# for i in range(len(doc_norms)):
#     doc_norms_dict[i] = doc_norms[i]
#
# #print(doc_norms_dict)
#
#
# with open("./data/reddit_shortened.json", "w") as f:
#     json.dump(reddit_shortened, f)


#
# with open ('./data/tf.pickle', 'rb') as f:
#     tf_transcripts = pickle.load(f)
#     tf_array = tf_transcripts.toarray()
#
# # tf_array = np.load('./data/tf.npy')
#
# with open('./data/inverted_dict_id_name.json') as wil_file:
#     inverted_dict_id_name = json.load(wil_file)
#
# with open('./data/word_id_lookup.json') as wil_file:
#     words = json.load(wil_file)
#
# with open('./data/wikivoyage_lite_relevant.json') as wil_file:
#     relevant = json.load(wil_file)
# print(len(relevant))



# for i in range(len(tf_array)):
#     if inverted_dict_id_name[str(i)] in relevant:
#         for j in range(len(tf_array[0])):
#             if tf_array[i][j] > 0:
#                 token = str(j)
#                 if token in result:
#                         result[token].append((i,int(tf_array[i][j])))
#                 else:
#                     result[token] = [(i, int(tf_array[i][j]))]
#
# #print(result)
#
# with open('./data/inverted_dict_id_word.json', "w") as f:
#     json.dump(result, f)
#
# sid = SentimentIntensityAnalyzer()
#
# with open('./data/combined_reddit.json') as wil_file:
#     reviews_data = json.load(wil_file)

#
#for key in reviews_data:
#     reviews_data[key] = reviews_data[key][:3]
#     reviews_data[key] = [x['body'][:300] for x in reviews_data[key]]
    #reviews_data[key] = [reviews_data[key][i][:300]]

# results = {}
# count = 0
# for key in reviews_data:
#
#     agg_score = 0.0
#     for i in range(len(reviews_data[key])):
#         if (reviews_data[key][i]['body'] != "No reviews available for this place"):
#             sentiments = sid.polarity_scores(reviews_data[key][i]['body'])
#             reviews_data[key][i] = (reviews_data[key][i]['body'], sentiments['compound'])
#             agg_score += sentiments['compound']
#         else:
#             reviews_data[key][i] = (reviews_data[key][i]['body'], 0.0)
#
#     agg_score = float(agg_score)/len(reviews_data[key])
#     results[key] = agg_score



#
# with open('./data/place_sentiments.json', "w") as f:
#     json.dump(results, f)
# sentiments = sid.polarity_scores(tStr)


# with open('./data/word_id_lookup.json') as wil_file:
#     lookup = json.load(wil_file)
#
# with open('./data/inverted_index.json') as wil_file:
#     inverted = json.load(wil_file)
#
# with open('./data/words.json') as wil_file:
#     words = json.load(wil_file)
#
# lst = words.split(",")
#
# ids = []
#
# for i in lst:
#     if i in lookup:
#         ids.append(str(lookup[i]))
#
# new_inverted = {}
#
# for key in inverted:
#     if key in ids:
#         new_inverted[key] = inverted[key]
#
# #print(len(new_inverted))
#
# with open('./data/trimmed_inverted_index.json', "w") as f:
#     json.dump(new_inverted, f)


# for key in wikivoyage_lite:
#     for place in wikivoyage_lite[key]['nearby_links']:
#         if place in wikivoyage_lite and key not in wikivoyage_lite[place]['nearby_links']:
#             wikivoyage_lite[place]['nearby_links'].append(key)
#
# #print(wikivoyage_lite)
# with open('./data/new_wiki.json', "w") as f:
#     json.dump(wikivoyage_lite, f)

# def get_reviews(locs):
#     revs = []
#   #   print(reviews_data['poncha springs'])
#     if reviews_data[locs] == []:
#             # print(3)
#         revs
#     elif len(reviews_data[locs]) <= 3:
#         for i in range(len(reviews_data[locs])):
#             revs.append(reviews_data[locs][0]['body'])
#     else:
#         for i in range(3):
#             revs.append(reviews_data[locs][0]['body'])
#     return revs

# with open('./data/word_id_lookup.json') as wil_file:
#     word_to_index = json.load(wil_file)
#
# with open('./data/inverted_dict_id_word.json') as wil_file:
#     index_to_word = json.load(wil_file)
#
# data = pickle.load(open( './data/tfidf.pickle', "rb" ) )
# my_matrix = data.transpose()
#
# from scipy.sparse.linalg import svds
# u, s, v_trans = svds(my_matrix, k=100)
# print(u.shape)
# print(s.shape)
# print(v_trans.shape)
# import matplotlib
# import numpy as np
# import matplotlib.pyplot as plt
# #%matplotlib inline
# plt.plot(s[::-1])
# plt.xlabel("Singular value number")
# plt.ylabel("Singular value")
# plt.show()

# words_compressed, _, docs_compressed = svds(my_matrix, k=40)
# docs_compressed = docs_compressed.transpose()
# # print(words_compressed.shape)
# # print(docs_compressed.shape)
#
# from sklearn.preprocessing import normalize
# words_compressed = normalize(words_compressed, axis = 1)
#
# def closest_words(word_in, k = 10):
#     if word_in not in word_to_index: return "Not in vocab."
#     sims = words_compressed.dot(words_compressed[word_to_index[word_in],:])
#     asort = np.argsort(-sims)[:k+1]
#     return [(index_to_word[str(i)],sims[i]/sims[asort[0]]) for i in asort[1:]]
#
# dict = {}
#
# for key in word_to_index:
#     dict[key] = [x[0] for x in closest_words(key)]
# #print(closest_words("movie"))
#
# with open('./data/query_expansion.json', "w") as f:
#     json.dump(dict, f)

# word_to_index = vectorizer.vocabulary_
# index_to_word = {i:t for t,i in word_to_index.iteritems()}
# print(words_compressed.shape)


#print(type(data))

with open('./data/combined_reddit.json') as wil_file:
    reddit = json.load(wil_file)

with open('./data/combined_reddit_sentiment.json') as wil_file:
    sentiments = json.load(wil_file)

dict = {}

for key in reddit:
     words = re.findall(r'[^,-/\s]+', key)
     dict[key] = []
     for k in range(len(reddit[key])):
         first = (reddit[key][k]['body'].lower()).find(key)
         sentiment_score = sentiments[key][k][1]

         if first == -1:
             first = (reddit[key][k]['body'].lower()).find(words[-1])
             if first == -1:
                 dict[key].append((reddit[key][k]['body'][:300], sentiment_score))
             else:
                 start = max(0, first - 150)
                 end = start + 300
                 #print(start)

                 #print(end)
                 text = reddit[key][k]['body'][start:end]
                 dict[key].append((text, sentiment_score))
         else:
             start = max(0, first - 150)
             end = start + 300
             #print(start)

             #print(end)
             text = reddit[key][k]['body'][start:end]
             dict[key].append((text, sentiment_score))


with open('./data/final_reddit.json', "w") as f:
    json.dump(dict, f)

#print(get_reviews("poncha springs"))
