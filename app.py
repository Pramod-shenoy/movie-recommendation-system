import pickle
import streamlit as st
import requests
import os
import gdown


# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except Exception as e:
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Poster"


# Function to download and load the similarity matrix from Google Drive
@st.cache_resource
def load_similarity_matrix():
    file_path = "similarity.pkl"

    # Check if the file exists locally
    if not os.path.exists(file_path):
        # URL to your Google Drive file (replace with your actual file ID)
        url = 'https://drive.google.com/uc?id=1qGV37AwoOQPSIKe_nWMIxfAQD9-BgVAa'
        gdown.download(url, file_path, quiet=False)

    # Load the similarity matrix from the local file
    with open(file_path, 'rb') as f:
        similarity = pickle.load(f)

    return similarity


# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


# Streamlit UI
st.header('Movie Recommender System')

# Load movie list (Assuming you already have movie_list.pkl or a similar file)
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Load the similarity matrix using the function
similarity = load_similarity_matrix()

# Movie list dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
