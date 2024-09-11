import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# User-item interaction matrix (example)
user_item_matrix = np.array([
    [5, 3, 0, 1],  # User 0
    [4, 0, 0, 1],  # User 1
    [1, 1, 0, 5],  # User 2
    [1, 0, 0, 4],  # User 3
    [0, 1, 5, 4],  # User 4
])

# Calculate cosine similarity between users
user_similarity = cosine_similarity(user_item_matrix)

# Function to predict ratings for a user
def predict_ratings(user_idx, user_item_matrix, user_similarity):
    # Get the user's ratings
    user_ratings = user_item_matrix[user_idx]
    
    # Calculate the mean only for non-zero ratings
    non_zero_indices = user_ratings != 0
    if non_zero_indices.sum() == 0:
        user_ratings_mean = 0
    else:
        user_ratings_mean = user_ratings[non_zero_indices].mean()
    
    # Subtract mean from ratings
    user_ratings_diff = user_ratings.copy()
    user_ratings_diff[non_zero_indices] -= user_ratings_mean
    
    # Predict ratings only for items the user hasn't rated yet (0 in the matrix)
    unrated_items = user_ratings == 0
    ratings_pred = np.zeros_like(user_ratings)
    
    for i in np.where(unrated_items)[0]:
        # For each unrated item, compute weighted sum of ratings from similar users
        weighted_sum = 0
        similarity_sum = 0
        for other_user_idx in range(user_item_matrix.shape[0]):
            if other_user_idx != user_idx and user_item_matrix[other_user_idx, i] != 0:
                weighted_sum += user_similarity[user_idx, other_user_idx] * (user_item_matrix[other_user_idx, i] - user_item_matrix[other_user_idx].mean())
                similarity_sum += np.abs(user_similarity[user_idx, other_user_idx])
        
        if similarity_sum > 0:
            ratings_pred[i] = user_ratings_mean + (weighted_sum / similarity_sum)
        else:
            ratings_pred[i] = user_ratings_mean
    
    return ratings_pred

# Get recommendations for User 0
predicted_ratings_user_0 = predict_ratings(0, user_item_matrix, user_similarity)
print("Predicted ratings for User 0:", predicted_ratings_user_0)
