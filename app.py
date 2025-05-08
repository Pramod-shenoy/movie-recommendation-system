import streamlit as st
import requests
import gdown
import pickle
import os

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to download and load the similarity matrix
def load_similarity_matrix():
    # Use Streamlit Cloud's temporary directory to store files
    file_path = '/tmp/similarity.pkl'  # Temporary file path in the Cloud
    
    # Check if the similarity matrix file exists
    if not os.path.exists(file_path):
        # Your file ID (replace this with your actual file ID)
        url = 'https://drive.google.com/uc?id=1qGV37AwoOQPSIKe_nWMIxfAQD9-BgVAa'  # Google Drive link
        gdown.download(url, file_path, quiet=False)  # Download the file if not present

    # Load the similarity matrix
    with open(file_path, 'rb') as f:
        similarity = pickle.load(f)

    return similarity

# Function to recommend movies based on similarity matrix
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

# Load the similarity matrix (directly calling the function)
similarity = load_similarity_matrix()

# Your main Streamlit app code
st.header('Movie Recommender System')

# Assuming the movie data is loaded elsewhere in your app, like this:
movies = pickle.load(open('movie_list.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations when button is clicked
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    # Display recommendations in columns
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
