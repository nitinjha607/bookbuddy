import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load data
books = pd.read_csv('Books.csv', encoding='ISO-8859-1')
users = pd.read_csv('Users.csv', encoding='ISO-8859-1')
ratings = pd.read_csv('Ratings.csv', encoding='ISO-8859-1')

# Print first few rows
print(books.head())
print(users.head())
print(ratings.head())

# Fix the DtypeWarning
users['Age'] = pd.to_numeric(users['Age'], errors='coerce')  # Convert 'Age' to numeric, coerce invalid entries to NaN

# Fill missing values
users['Age'] = users['Age'].fillna(25)  # Replace NaN with 25

# Prepare the dataset by merging user ratings and books data
merged_data = ratings.merge(users, on='User-ID', how='inner')
merged_data = merged_data[['Age', 'Book-Rating']]  # Keep only relevant columns

# Split the data into features (X) and target (y)
X = merged_data[['Age', 'Book-Rating']].values
y = merged_data['Book-Rating'].values

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Build the model
model = Sequential()
model.add(tf.keras.Input(shape=(2,)))  # Input layer with 2 features (Age and Book-Rating)
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))  # Output layer

# Compile the model
model.compile(optimizer='adam', loss='mse')

# Train the model
history = model.fit(X_train_scaled, y_train, epochs=5, validation_data=(X_test_scaled, y_test))

# Save the model
model.save('bookbuddy_recommender_model.h5')

# Evaluate the model
loss = model.evaluate(X_test_scaled, y_test)
print(f"Test Loss: {loss}")

