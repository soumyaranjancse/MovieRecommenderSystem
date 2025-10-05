import pandas as pd
import streamlit as st
import pickle
import requests
import gdown  # 👈 to download large files from Google Drive

# ------------------- Fetch Poster Function -------------------
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


# ------------------- Load Pickle Files from Google Drive -------------------
# Replace with your actual Google Drive File IDs
similarity_id = "1TkT1W6nFMPykhiWJO59BtzAHol7me2XZ"   # ✅ your similarity.pkl file ID
movies_dict_id = "1Cq0JDbuDtILFBnKSkq39UmK1PqvpX-n9"   # ✅ your movie_dict.pkl file ID

# Download the files using gdown
gdown.download(f"https://drive.google.com/uc?id={similarity_id}", "similarity.pkl", quiet=False)
gdown.download(f"https://drive.google.com/uc?id={movies_dict_id}", "movie_dict.pkl", quiet=False)

# Load pickle data
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

with open("movie_dict.pkl", "rb") as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)


# ------------------- Recommendation Function -------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

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
