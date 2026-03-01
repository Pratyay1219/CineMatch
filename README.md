# 🎬 CineMatch - Movie Recommendation System

A full-stack Movie Recommendation System built using FastAPI, Streamlit, and TMDB API.

This application recommends similar movies based on content similarity and dynamically fetches posters, ratings, and details.

---

## 🚀 Live Demo

[https://your-render-link.com](https://cinematch-kzy1.onrender.com/)

---

## ✨ Features

- Search any movie instantly  
- Get similar movie recommendations  
- Dynamic poster fetching from TMDB  
- FastAPI backend for recommendation logic  
- Interactive Streamlit frontend  
- TF-IDF + Cosine Similarity based model  
- Deployable on Render  

---

## 🏗️ Tech Stack

Backend:
- FastAPI
- Python
- Pandas
- NumPy
- Scikit-learn

Frontend:
- Streamlit

API:
- TMDB (The Movie Database API)

Deployment:
- Render

---

## 🧠 How It Works

1. Movie metadata (genres, keywords, overview, etc.) is processed.
2. TF-IDF Vectorization converts text into numerical features.
3. Cosine similarity is computed between movies.
4. When a user selects a movie:
   - The backend finds the most similar movies.
   - TMDB API fetches posters.
   - Streamlit displays results in a grid layout.

---

## 📂 Project Structure

movie-recommendation-system/

- app.py                → Streamlit Frontend  
- main.py               → FastAPI Backend  
- movies.pkl            → Processed movie dataset  
- similarity.pkl        → Cosine similarity matrix  
- requirements.txt  
- README.md  

---

## ⚙️ Installation (Run Locally)

### 1. Clone the Repository

git clone https://github.com/Pratyay1219/CineMatch  
cd CineMatch  

### 2. Create Virtual Environment

python -m venv venv  

Activate it:

Windows:  
venv\Scripts\activate  

Mac/Linux:  
source venv/bin/activate  

### 3. Install Dependencies

pip install -r requirements.txt  

### 4. Add TMDB API Key

Create a `.env` file in the root folder:

TMDB_API_KEY=your_api_key_here  

### 5. Run Backend

uvicorn main:app --reload  

### 6. Run Frontend

streamlit run app.py  

---

## 🌍 Deployment on Render

1. Push your project to GitHub  
2. Create a new Web Service on Render  
3. Add environment variable:  
   TMDB_API_KEY=your_api_key  
4. Deploy  

---

## 📈 Future Improvements

- User authentication system  
- Collaborative filtering  
- Hybrid recommendation system  
- Movie trailers integration  
- Watchlist feature  
- User rating system  


## ⭐ Support

If you like this project, give it a star on GitHub.
