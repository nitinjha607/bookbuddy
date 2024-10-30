import pandas as pd

# Load books data
books = pd.read_csv('Books.csv', encoding='ISO-8859-1')

# Print columns for debugging
print("Columns in Books DataFrame:", books.columns.tolist())

def recommend_books(user_input, start_index=0, num_recommendations=6):
    processed_input = process_input(user_input)

    if 'title' in processed_input:
        try:
            title = processed_input['title']
            recommended_books = books[books['Book-Title'].str.contains(title, case=False)]
            if not recommended_books.empty:
                return recommended_books['Book-Title'].tolist()[start_index:start_index + num_recommendations]
            else:
                return ["Sorry, I couldn't find that book."]
        except KeyError as e:
            return [f"Error: {str(e)}"]

    if 'genre' in processed_input:
        genre_books = books[books['Book-Title'].str.contains(processed_input['genre'], case=False)]
        if not genre_books.empty:
            return genre_books['Book-Title'].tolist()[start_index:start_index + num_recommendations]
        else:
            return ["Sorry, I couldn't find any books in that genre."]

    return ["I'm sorry, I didn't understand that."]


def process_input(user_input):
    # Basic processing to determine if the input is a title or genre request
    processed = {}
    if 'romantic' in user_input.lower():
        processed['genre'] = 'romantic'
    elif 'thriller' in user_input.lower():
        processed['genre'] = 'thriller'
    else:
        processed['title'] = user_input  # Treat all else as a title
    return processed


# Main interaction loop
print("Welcome to BookBuddy! You can tell me the kind of book you are looking for. Type 'exit' to quit.")

start_index = 0  # To keep track of where to start showing recommendations
num_recommendations = 6  # Number of recommendations to show

while True:
    user_input = input("What kind of book are you looking for? ")

    if user_input.lower() == 'exit':
        print("Goodbye!")
        break

    if user_input.lower() == 'more':
        start_index += num_recommendations  # Move to the next set of recommendations

    recommended_books = recommend_books(user_input, start_index)

    if recommended_books and isinstance(recommended_books, list):
        response = "Recommended Books:\n" + "\n".join(recommended_books)  # Each book on a new line
    else:
        response = "Sorry, I couldn't find any recommendations."

    print(response)
