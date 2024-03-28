import streamlit as st
import pandas as pd
import pickle
import difflib

st.title("Movie Recommendation System")

@st.cache(allow_output_mutation=True)
def load_model():
    with open('movies_data.pkl', 'rb') as f:
        movies_data = pickle.load(f)

    with open('movies_similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)

    return movies_data, similarity

def get_recommendations(movie_name, movies_data, similarity):
    list_of_all_titles = movies_data['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    if len(find_close_match) > 0:
        close_match = find_close_match[0]
        index_of_the_movie = movies_data[movies_data.title == close_match]['index'].values[0]
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

        recommendations = []
        for i, movie in enumerate(sorted_similar_movies):
            index = movie[0]
            title_from_index = movies_data[movies_data.index==index]['title'].values[0]
            recommendations.append(f"{i+1}. {title_from_index}")
            if i >= 29:
                break
        return recommendations
    else:
        return ["Sorry, no matching movie found."]

movies_data, similarity = load_model()

movie_name = st.text_input('Enter your favourite movie name:')
if movie_name:
    recommendations = get_recommendations(movie_name, movies_data, similarity)
    st.subheader('Movies suggested for you:')
    st.write('\n'.join(recommendations))
