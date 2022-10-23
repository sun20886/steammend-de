import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# import nltk
# import string
# import re
import json
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.porter import PorterStemmer
# from nltk.stem.wordnet import WordNetLemmatizer
# from scipy import stats
from sklearn.metrics.pairwise import linear_kernel  # for cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.request import urlopen
from http.client import HTTPResponse

file_path = 'data/seller_game.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

df = pd.DataFrame(data)


def get_detail_by_appid(appid):
    appid = str(appid)
    url = "https://store.steampowered.com/api/appdetails?appids="
    HTTPResponse = urlopen(url+appid)
    detail_data = json.load(HTTPResponse)[appid]['data']

    tags = set()
    for i in detail_data['categories']:
        tags.add(i['description'])

    for i in detail_data['genres']:
        tags.add(i['description'])

    app_detail = {
        "name": detail_data['name'],
        "steam_appid": detail_data['steam_appid'],
        "required_age": detail_data['required_age'],
        "short_description": detail_data['short_description'],
        "supported_languages": detail_data['supported_languages'],
        "header_image": detail_data['header_image'],
        "pc_requirements": detail_data['pc_requirements'],
        "mac_requirements": detail_data['mac_requirements'],
        "linux_requirements": detail_data['linux_requirements'],
        "publishers": detail_data['publishers'],
        # "categories": detail_data['categories'],
        # "genres": detail_data['genres'],
        "tags": list(tags)
    }

    return app_detail


def caculate_cosine(appid):

    if appid not in df['steam_appid']:
        new_app = get_detail_by_appid(appid)

    print(new_app)

    df.loc[len(df)] = new_app

    # Define TF-IDF Vectorizer Object
    tfidf = TfidfVectorizer()

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform([str(i) for i in df['tags']])

    # Output the shape of tfidf_matrix
    tfidf_matrix.shape

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df['steam_appid']).drop_duplicates()

    return cosine_sim, indices


def get_recommendations(appid):

    cosine_sim, indices = caculate_cosine(appid)

    idx = indices[appid]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 5 most similar movies
    sim_scores = sim_scores[1:6]

    # Get the movie indices
    appid_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df.iloc[appid_indices]


# print(get_recommendations(1016900))
