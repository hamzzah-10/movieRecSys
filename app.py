import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_similarities = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_similarities:
        movie_id = movies_list.iloc[i[0]].movie_id
        # movies poster

        recommended_movies.append(movies_list.iloc[i[0]]['title'])
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=752d637d54a08dcb12cbeb37229eae9e".format(movie_id))
    data = response.json()
    print(data)
    return "https://media.themoviedb.org/t/p/w600_and_h900_bestv2" + data['poster_path']


st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select your favorite movie?',
    movies_list['title'].values
)

if st.button('Recommend'):
    recommended_movies, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    
    for i in range(5):
        with globals()[f"col{i+1}"]:
            st.image(posters[i])
            st.write(recommended_movies[i])         