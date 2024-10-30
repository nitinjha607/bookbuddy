# recommendation.py
import pandas as pd

# Load books data
books = pd.read_csv('Books.csv', encoding='ISO-8859-1')

def recommend_books(user_input, start_index=0, num_recommendations=6):
    processed_input = process_input(user_input)
    if 'title' in processed_input:
        title = processed_input['title']
        recommended_books = books[books['Book-Title'].str.contains(title, case=False)]
        return recommended_books['Book-Title'].tolist()[start_index:start_index + num_recommendations]
    elif 'genre' in processed_input:
        genre = processed_input['genre']
        genre_books = books[books['Book-Title'].str.contains(genre, case=False)]
        return genre_books['Book-Title'].tolist()[start_index:start_index + num_recommendations]
    else:
        return ["I'm sorry, I didn't understand that."]

def process_input(user_input):
    processed = {}
    if 'romantic' in user_input.lower():
        processed['genre'] = 'romantic'
    elif 'thriller' in user_input.lower():
        processed['genre'] = 'thriller'
    else:
        processed['title'] = user_input
    return processed
