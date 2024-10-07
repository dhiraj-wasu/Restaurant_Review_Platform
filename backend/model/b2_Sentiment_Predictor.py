###Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from backend.RestaurantLeaderboard import Leaderboard###Importing dataset (from google drive)
# from google.colab import drive
# drive.mount('/content/drive')
# %cd /content/drive/MyDrive/Project2_Sentiment_Analysis
# !ls
def predictor(res_id):
    dataset = pd.read_csv('backend\\model\\a2_RestaurantReviews_FreshDump.tsv', delimiter = '\t', quoting = 3)
    dataset.head()
###Data cleaning
    import re
    import nltk

    nltk.download('stopwords')

    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    ps = PorterStemmer()

    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    corpus=[]
    print(dataset.shape)
    for i in range(0,dataset.shape[0]):
       review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
       review = review.lower()
       review = review.split()
       review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
       review = ' '.join(review)
       corpus.append(review)
###Data transformation
# Loading BoW dictionary
    from sklearn.feature_extraction.text import CountVectorizer
    import pickle
    cvFile='backend\\model\\c1_BoW_Sentiment_Model.pkl'
# cv = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open('./drive/MyDrive/Colab Notebooks/2 Sentiment Analysis (Basic)/3.1 BoW_Sentiment Model.pkl', "rb")))
    cv = pickle.load(open(cvFile, "rb"))

    X_fresh = cv.transform(corpus).toarray()
    X_fresh.shape
###Predictions (via sentiment classifier)
    import joblib
    # import pandas as pd
    import matplotlib.pyplot as plt

# Load the classifier
    classifier = joblib.load('backend\\model\\c2_Classifier_Sentiment_Model.pkl')

# Predict using the classifier
    y_pred = classifier.predict(X_fresh)
    print(y_pred)

# Add the predicted labels to the dataset
    dataset['predicted_label'] = y_pred.tolist()
    print(dataset.head())

# Save the dataset with predicted labels
    dataset.to_csv("c3_Predicted_Sentiments_Fresh_Dump.tsv", sep='\t', encoding='UTF-8', index=False)

# Load the dataset with predictions
    df = pd.read_csv("c3_Predicted_Sentiments_Fresh_Dump.tsv", delimiter='\t', quoting=3)

# Extract the predicted labels
    predicted_labels = df['predicted_label']

# Count the labels
    value_counts = predicted_labels.value_counts()

# Calculate the percentage of positive and negative comments
    total_comments = len(predicted_labels)
    positive_percentage = (value_counts.get(1, 0) / total_comments) * 100
    negative_percentage = (value_counts.get(0, 0) / total_comments) * 100

# Print the percentages
    # print(f"Positive comments: {positive_percentage:.2f}%")
    # print(f"Negative comments: {negative_percentage:.2f}%")
    score_delta = positive_percentage - negative_percentage
    print(score_delta)
            # Update the Redis leaderboard
    leaderboard =Leaderboard()
    leaderboard.update_score(res_id, score_delta)
     
# Create a bar plot for the distribution of predicted labels
#     plt.bar(value_counts.index, value_counts.values)

# # Add labels and title
#     plt.xlabel('Predicted Label')
#     plt.ylabel('Count')
#     plt.title('Distribution of Predicted Positive and Negative Comments')

# Show the plot
    # plt.show()
    return 1

