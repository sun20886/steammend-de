import pandas as pd
from sklearn.metrics.pairwise import linear_kernel  # for cosine similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from pandasticsearch import Select
import json
import dao
import steam_API_data


#elk에 없는 게임일 때 steamAPI로 디테일을 받아와서 데이터 프레임에 맞게 전처리
def preprocessing_appdetail(detail_data):
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
        "publishers": detail_data['publishers'],
        "tags": list(tags),
        "categories": detail_data['categories'],
        "genres": detail_data['genres'],
        "release_date": detail_data['release_date']
    }

    app_detail['pc_requirements.minimum'] = detail_data['pc_requirements'][
        'minimum'] if "minimum" in detail_data['pc_requirements'].keys() else []
    app_detail['pc_requirements.recommended'] = detail_data['pc_requirements'][
        'recommended'] if "recommended" in detail_data['pc_requirements'].keys() else []

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

    app_detail['recommendations'] = detail_data['recommendations'] if "recommendations" in detail_data.keys() else None

    return app_detail


def caculate_cosine(game, df_removed):
    
    if game['steam_appid'] not in df_removed['_id']:
        new_app = preprocessing_appdetail(game)

    df_removed.loc[len(df_removed)] = new_app

    # Define TF-IDF Vectorizer Object
    tfidf = TfidfVectorizer()

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform([str(i) for i in df_removed['tags']])

    # Output the shape of tfidf_matrix
    tfidf_matrix.shape

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # indices = pd.Series(df_removed.index, index=df_removed['_id']).drop_duplicates()  
    
    indices = pd.Series(list(range(len(df_removed))), index=df_removed['_id']).drop_duplicates()  

    return cosine_sim, indices



#비슷한 게임을 계산하여 반환
def get_recommendations(game, type, df_removed):
    
    cosine_sim, indices = caculate_cosine(game, df_removed)

    idx = indices[game['steam_appid']]

    # Get the pairwsie similarity scores of all games with that game
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the games based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)


    # Get the scores of the 5 most similar games
    if type=="main":
        sim_scores=sim_scores[1:2]
    
    elif type=="mydata":
        sim_scores = sim_scores[1:6]

    # Get the game indices
    appid_indices = [i[0] for i in sim_scores]

    result=df_removed.iloc[appid_indices, 2:]
    result_string=result.to_json(force_ascii=False, orient = 'records')
    result_json = json.loads(result_string)

    return result_json


#메인화면에 보여줄 추천 게임을 반환하는 함수
def get_main_recomm(top5_games, not_top5_games):

    df = Select.from_dict(dao.get_all_games_for_recomm()).to_pandas()
    
    df_removed=remove_duplication(not_top5_games, df)

    main_recommended_games=[]

    for game in top5_games:
        recommended=get_recommendations(top5_games[game], "main", df_removed)
        temp=recommended[0]
        main_recommended_games.append(temp)

    
    return main_recommended_games



#My Page의 My Recommend에서 보여줄 추천 게임들을 반환하는 함수
def get_my_recomm(top5_games, not_top5_games):

    df = Select.from_dict(dao.get_all_games_for_recomm()).to_pandas()
    
    df_removed=remove_duplication(not_top5_games, df)

    mydata_recommended_games=[]

    for game in top5_games:
        recommended=get_recommendations(top5_games[game], "mydata",df_removed)
        temp={
            "name":top5_games[game]['name'],
            "appid":top5_games[game]['steam_appid'],
            "recommend_list":recommended
        }

        mydata_recommended_games.append(temp)
    
    return mydata_recommended_games


def remove_duplication(not_top5_games, df):

    for id in not_top5_games:
        if len(df[df['_id'] == str(id)]) != 0:
            df.drop(df[df['_id'] == str(id)].index ,axis='index',inplace=True)
    
    return df