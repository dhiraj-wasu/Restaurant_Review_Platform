import numpy as np
import pandas as pd
###Importing libraries
import numpy as np
import pandas as pd
### Importing dataset


dataset = pd.read_csv('backend\\model\\a1_RestaurantReviews_HistoricDump.tsv', delimiter = '\t', quoting = 3)
dataset.shape
print(dataset.head())

### Data Preprocessing
import re
import nltk

nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()

all_stopwords = stopwords.words('english')
all_stopwords.remove('not')
corpus=[]

for i in range(0, 900):
  review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
  review = review.lower()
  review = review.split()
  review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
  review = ' '.join(review)
  corpus.append(review)
corpus
### Data transformation
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1420)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values
# Saving BoW dictionary to later use in prediction
import pickle
bow_path = 'backend\\model\\c1_BoW_Sentiment_Model.pkl'
pickle.dump(cv, open(bow_path, "wb"))
### Dividing dataset into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)
### Model fitting (Naive Bayes)
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)
# Exporting NB Classifier to later use in prediction
# import joblib
# joblib.dump(classifier, 'c2_Classifier_Sentiment_Model')
import joblib
import os

# Define the directory and file name
directory = 'backend\model'
file_name = 'c2_Classifier_Sentiment_Model.pkl'

# Ensure the directory exists
os.makedirs(directory, exist_ok=True)

# Full path to the file
full_path = os.path.join(directory, file_name)

# Dump the classifier to the specified path
joblib.dump(classifier, full_path)
###Model performance
y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)

accuracy_score(y_test, y_pred)
print("done")