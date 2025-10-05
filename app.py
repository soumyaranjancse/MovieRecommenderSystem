import pandas as pd
import streamlit as st
import pickle
import requests
import io

# ------------------- Fetch Poster Function -------------------
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# ------------------- Load Pickle Files from Hugging Face -------------------
# Permanent links (hosted on Hugging Face)
similarity_url = "https://huggingface.co/datasets/Soumyaranjannn/movie_recommender_files/resolve/main/similarity.pkl"
movies_dict_url = "https://huggingface.co/datasets/Soumyaranjannn/movie_recommender_files/resolve/main/movie_dict.pkl"

# Cache the data so it’s downloaded only once
@st.cache_data(show_spinner=False)
def load_data():
    def load_pickle_from_url(url):
        response = requests.get(url)
        response.raise_for_status()  # ensures proper error if link fails
        return pickle.load(io.BytesIO(response.content))

    similarity = load_pickle_from_url(similarity_url)
    movies_dict = load_pickle_from_url(movies_dict_url)
    movies = pd.DataFrame(movies_dict)
    return similarity, movies


# ------------------- Show Loading Spinner -------------------
with st.spinner("Loading data... Please wait ⏳"):
    similarity, movies = load_data()


# ------------------- Recommendation Function -------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters


# ------------------- Streamlit App Layout -------------------
st.title("🎬 Movie Recommender System")
selected_movie_name = st.selectbox('🔍 Search for a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
