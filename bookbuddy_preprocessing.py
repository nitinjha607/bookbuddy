import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load datasets
books = pd.read_csv('Books.csv', low_memory=False)
ratings = pd.read_csv('Ratings.csv', low_memory=False)
users = pd.read_csv('Users.csv', low_memory=False)

# Display initial stats before preprocessing
print("\nBefore Preprocessing:")
print("Books dataset shape:", books.shape)
print("Ratings dataset shape:", ratings.shape)
print("Users dataset shape:", users.shape)

# Show a few records from each dataset before preprocessing
print("\nSample records from Books dataset:")
print(books.head(), "\n")
print("\nSample records from Ratings dataset:")
print(ratings.head(), "\n")
print("\nSample records from Users dataset:")
print(users.head(), "\n")

# Check for missing values before preprocessing
print("\nMissing values in Books dataset:\n", books.isnull().sum())
print("\nMissing values in Ratings dataset:\n", ratings.isnull().sum())
print("\nMissing values in Users dataset:\n", users.isnull().sum())

# Ensure the expected columns are present
expected_user_id = 'User-ID'
if expected_user_id not in ratings.columns:
    raise KeyError(f"'{expected_user_id}' column not found in the ratings file. Check the column names and update the script accordingly.")

# Check for duplicate entries and drop them
ratings_before_dedup = ratings.shape[0]
books_before_dedup = books.shape[0]
users_before_dedup = users.shape[0]

ratings.drop_duplicates(inplace=True)
books.drop_duplicates(inplace=True)
users.drop_duplicates(inplace=True)

# Stats after dropping duplicates
print(f"\nDuplicates removed in Ratings: {ratings_before_dedup - ratings.shape[0]}")
print(f"Duplicates removed in Books: {books_before_dedup - books.shape[0]}")
print(f"Duplicates removed in Users: {users_before_dedup - users.shape[0]}")

# Proceed with preprocessing
# Example: Group by User-ID to get user ratings count
user_ratings = ratings.groupby('User-ID').size()
print("\nUser ratings count summary:")
print(user_ratings.describe(), "\n")

# Prepare the dataset for further processing
# Merging datasets to create a unified DataFrame
merged_data = ratings.merge(books, on='ISBN', how='left').merge(users, on='User-ID', how='left')

# Display merged data for debugging
print("\nMerged data sample (first 5 rows):")
print(merged_data.head(), "\n")

# Further preprocessing steps

# 1. Handle missing values
print("\nMissing values in merged data before handling:\n", merged_data.isnull().sum())
merged_data.dropna(subset=['Book-Title', 'Book-Author', 'Publisher'], inplace=True)
print("\nMissing values in merged data after handling:\n", merged_data.isnull().sum())

# 2. Encode categorical variables
label_encoders = {}
for column in ['Book-Author', 'Publisher', 'Location']:
    le = LabelEncoder()
    merged_data[column] = le.fit_transform(merged_data[column].astype(str))  # Convert to str to handle NaNs
    label_encoders[column] = le

# 3. Split data into features and target
features = merged_data[['User-ID', 'ISBN', 'Book-Author', 'Publisher', 'Location']]
target = merged_data['Book-Rating']

# 4. Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Display post-processing stats
print("\nAfter Preprocessing:")
print("Merged dataset shape after preprocessing:", merged_data.shape)
print("\nSample records from Merged dataset:")
print(merged_data.head())

# 5. Display the shapes of the train and test sets
print("\nTraining features shape:", X_train.shape)
print("Testing features shape:", X_test.shape)

# Optionally, save the processed data to a new CSV if needed
merged_data.to_csv('merged_book_data.csv', index=False)

# Save the label encoders for future use
import joblib
for column, le in label_encoders.items():
    joblib.dump(le, f'label_encoder_{column}.joblib')

print("\nPreprocessing complete.")
