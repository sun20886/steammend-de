import pandas as pd
import numpy as np
import json
from elasticsearch import Elasticsearch
from pandasticsearch import Select

from sklearn.metrics.pairwise import linear_kernel  # for cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib.request import urlopen
from http.client import HTTPResponse


es = Elasticsearch(
    hosts=["http://127.0.0.1:9200"],

)

doc = {"query": {"match_all": {}}}

res = es.search(index='game_list01', body=doc, size=2226)
df = Select.from_dict(res).to_pandas()


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
        "_id": detail_data['steam_appid'],
        "required_age": detail_data['required_age'],
        "short_description": detail_data['short_description'],
        "supported_languages": detail_data['supported_languages'],
        "header_image": detail_data['header_image'],
        # "pc_requirements": detail_data['pc_requirements'],
        # "mac_requirements": detail_data['mac_requirements'],
        # "linux_requirements": detail_data['linux_requirements'],
        "publishers": detail_data['publishers'],
        "categories": detail_data['categories'],
        "genres": detail_data['genres'],
        "release_date": detail_data['release_date'],
        "tags": list(tags)
    }

    app_detail['pc_requirements.minimum'] = detail_data['pc_requirements'][
        'minimum'] if "minimum" in detail_data['pc_requirements'].keys() else None
    app_detail['pc_requirements.recommended'] = detail_data['pc_requirements'][
        'recommended'] if "recommended" in detail_data['pc_requirements'].keys() else None

    if type(detail_data['mac_requirements']) == dict:
        app_detail['mac_requirements.minimum'] = detail_data['mac_requirements'][
            'minimum'] if "minimum" in detail_data['mac_requirements'].keys() else None
        app_detail['mac_requirements.recommended'] = detail_data['mac_requirements'][
            'recommended'] if "recommended" in detail_data['mac_requirements'].keys() else None
    else:
        app_detail['mac_requirements.minimum'] = None
        app_detail['mac_requirements.recommended'] = None

    if type(detail_data['linux_requirements']) == dict:
        app_detail['linux_requirements.minimum'] = detail_data['linux_requirements'][
            'minimum'] if "minimum" in detail_data['linux_requirements'].keys() else None
        app_detail['linux_requirements.recommended'] = detail_data['linux_requirements'][
            'recommended'] if "recommended" in detail_data['linux_requirements'].keys() else None
    else:
        app_detail['linux_requirements.minimum'] = None
        app_detail['linux_requirements.recommended'] = None

    if "price_overview" in detail_data.keys():
        app_detail['price_overview.currency'] = detail_data['price_overview'][
            'currency'] if "currency" in detail_data['price_overview'].keys() else None
        app_detail['price_overview.initial'] = detail_data['price_overview'][
            'initial'] if "initial" in detail_data['price_overview'].keys() else None
        app_detail['price_overview.final'] = detail_data['price_overview']['final'] if "final" in detail_data['price_overview'].keys() else None
        app_detail['price_overview.discount_percent'] = detail_data['price_overview'][
            'discount_percent'] if "discount_percent" in detail_data['price_overview'].keys() else None
        app_detail['price_overview.initial_formatted'] = detail_data['price_overview'][
            'initial_formatted'] if "initial_formatted" in detail_data['price_overview'].keys() else None
        app_detail['price_overview.final_formatted'] = detail_data['price_overview'][
            'final_formatted'] if "final_formatted" in detail_data['price_overview'].keys() else None
    else:
        app_detail['price_overview.currency'] = None
        app_detail['price_overview.initial'] = None
        app_detail['price_overview.final'] = None
        app_detail['price_overview.discount_percent'] = None
        app_detail['price_overview.initial_formatted'] = None
        app_detail['price_overview.final_formatted'] = None

        # app_detail[''] = detail_data[''][''] if "" in detail_data[''].keys() else None
        # app_detail[''] = detail_data[''][''] if "" in detail_data[''].keys() else None

    app_detail['recommendations'] = detail_data['recommendations'] if "recommendations" in detail_data.keys() else None

    return app_detail


def caculate_cosine(appid):

    if appid not in df['_id']:
        new_app = get_detail_by_appid(appid)

    df.loc[len(df)] = new_app

    # Define TF-IDF Vectorizer Object
    tfidf = TfidfVectorizer()

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform([str(i) for i in df['tags']])

    # Output the shape of tfidf_matrix
    tfidf_matrix.shape

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    indices = pd.Series(df.index, index=df['_id']).drop_duplicates()

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
