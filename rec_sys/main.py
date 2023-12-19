import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter


def jaccard_similarity(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union


def normalize(value, min_value, max_value, new_min_value=0, new_max_value=1):
    normalized_value = (value - min_value) / (max_value - min_value) * (new_max_value - new_min_value) + new_min_value
    return normalized_value


def calculate_mean(lst):
    return sum(lst) / len(lst)


def get_mode(numbers):
    count = Counter(numbers)
    max_count = max(count.values())
    mode = [k for k, v in count.items() if v == max_count]
    return mode


def get_recommendations(user_anime_uids: list[int]):
    anime_data = pd.read_csv(r'C:\Users\theme\PycharmProjects\TomokoApi\rec_sys\data\anime_base.csv')
    anime_data = anime_data.drop_duplicates(subset='title')

    anime_synopsis = anime_data['synopsis'].fillna('')

    anime_uid_data = anime_data['uid']

    anime_to_index = pd.Series(anime_data.index, index=anime_data['uid'])

    tfidf = TfidfVectorizer(stop_words='english')
    anime_matrix = tfidf.fit_transform(anime_synopsis)

    indicies = anime_to_index[user_anime_uids]

    user_anime_data = anime_data.iloc[indicies]

    anime_test_summary = anime_synopsis[indicies].values
    anime_test_matrix = tfidf.transform(anime_test_summary)
    sim_scores = cosine_similarity(anime_test_matrix, anime_matrix).tolist()[0]
    sim_scores = sorted(enumerate(sim_scores), key=lambda i: i[1], reverse=True)

    user_anime_genres = user_anime_data.iloc[:, 10:].values
    user_anime_episodes = user_anime_data['episodes'].values
    max_episodes_value = user_anime_data['episodes'].max()
    user_episodes_mode = min(get_mode(user_anime_episodes))

    upd_sim_scores = []
    for row_idx, sim_score in sim_scores:
        row = anime_data.iloc[row_idx]
        genres = anime_data.iloc[row_idx, 10:].values

        episodes_coef = 0
        score_coef = 0

        if not pd.isna(row['episodes']):
            episodes_coef = (1 - normalize(row['episodes'],
                                           user_episodes_mode,
                                           max_episodes_value))
        if not pd.isna(row['score']):
            score_coef = normalize(row['score'], 0, 10, -1.5, .5)

        # genres_coef = calculate_mean(
        #     cosine_similarity([genres], user_anime_genres).tolist()[0])

        # print(genres_coef)
        # + (.5 * (1 - abs(sim_score)) * genres_coef)
        upd_sim_scores.append((row_idx, sim_score + \
                               (.5 * (1 - abs(sim_score)) * episodes_coef) + \
                               (.5 * (1 - abs(sim_score)) * score_coef)
                               ))

    # Sort anime by similarity
    # sim_scores = sorted(upd_sim_scores, key=lambda i: i[1], reverse=True)

    sim_scores = sorted(enumerate(upd_sim_scores), key=lambda i: i[1], reverse=True)

    movie_indexes = [i[0] for i in sim_scores]

    return [anime_uid_data[i] for i in movie_indexes[1:6] if i in anime_uid_data]