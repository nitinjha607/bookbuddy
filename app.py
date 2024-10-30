from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load dataset
books = pd.read_csv('Books.csv', encoding='ISO-8859-1')

def recommend_books(user_input):
    # Search for books based on user input
    if 'romantic' in user_input.lower():
        genre_books = books[books['Book-Title'].str.contains("romantic", case=False)]
    elif 'thriller' in user_input.lower():
        genre_books = books[books['Book-Title'].str.contains("thriller", case=False)]
    else:
        genre_books = books[books['Book-Title'].str.contains(user_input, case=False)]

    return genre_books['Book-Title'].tolist()[:6] if not genre_books.empty else ["Sorry, I couldn't find that book."]

def recommend_more_books():
    # This can be customized to fetch more random books or more from a specific genre
    # Here we will just fetch a random sample of books from the dataset
    return books['Book-Title'].sample(n=3).tolist()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    recommendations = recommend_books(user_input)
    return jsonify(recommendations)

@app.route('/more_recommend', methods=['POST'])
def more_recommend():
    more_recommendations = recommend_more_books()
    return jsonify(more_recommendations)

if __name__ == '__main__':
    app.run(debug=True)
