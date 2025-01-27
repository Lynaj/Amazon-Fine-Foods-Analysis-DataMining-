# -*- coding: utf-8 -*-
"""(Part A).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mxkzaZjoSIz4pb7MZG-k_RDRkyLhkxg2

#**Working with the Data**

### Adding the imports
"""

# Commented out IPython magic to ensure Python compatibility.
# Jupyter-specific.
# %matplotlib inline
import time
program_start = time.time()

# Colab specific.
from google.colab import files

# General
from sklearn.feature_extraction.text import TfidfVectorizer, HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import average_precision_score
from sklearn.metrics import recall_score
from sklearn.model_selection import KFold
from sklearn import neighbors
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm, ensemble
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set() # Set the default styling. 
from io import BytesIO
import csv
import pickle
from scipy.sparse import coo_matrix, vstack, csr_matrix

# Plot style settings.
plt.style.use('fivethirtyeight') # I'm a fan of this one.

"""### Reading the reduced file, taking the review and rating column"""

y = []
X = []
# open reduced CSV
with open('reduced_amazon_ff_reviews.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        X.append(row[5])
        y.append(row[8])

"""### Making a data frame called 'df' out of column 5 and 8"""

# columns 'Rating' and 'Text' are loaded into the df
df = pd.read_csv('reduced_amazon_ff_reviews.csv', usecols=[5, 8])

# top 5 records
df.head()

# basic info. 14906 records for the reduced
df.describe()

"""### Getting the count of each type of rating"""

# counts the total number of different labels
rating_counts = df.groupby('Rating')['Rating'].count()
rating_counts.head()

# getting the ratios of the ratings
rating_counts / len(df)

"""### Preparing the data for classification"""

# using a tfidf vecotrizer to convert review text into vectors also filters stopwords
vectorizer = TfidfVectorizer(stop_words='english')
X = vectorizer.fit_transform(df['Text'])

print(X.shape)
print(vectorizer.get_feature_names())

"""### Splitting the labels from the review text"""

# putting the ratings into the variable y
y = df['Rating']
y.head()

"""### Splitting up the training/testing with an 80/20 split"""

# split the data 80/20 and add random state 55
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=55)

# X_train containts text as a vector, and y_train contains the label
print(X_train)
print(y_train)

# X_test containts text as a vector, and y_test contains the label
print(X_test)
print(y_test)

"""#**Naive Bayes Classifier**"""

# Create instance of the NB classifier
modelNB = MultinomialNB()

# Fit to data (also called training the model
modelNB.fit(X_train, y_train)

# create NB prediction variable for the labels 
y_predNB = modelNB.predict(X_test)

# compute accuracy
accuracy_score(y_test, y_predNB)

"""This model correctly predicted the rating of a review about 65% of the time

### Precision Score
The precision is the ability of the classifier not to label as postiive a sample that is negative
"""

# best value is 1 and worst value is 0
print("Macro Precision:",precision_score(y_test, y_predNB, average='macro'))
print("Micro Precision:",precision_score(y_test, y_predNB, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predNB, average='weighted'))

"""**Macro Precision:** Calculates metrics for each label, and find the unweighted mean. Does not take label imbalance into account. <br>
**Micro Precision:** Calculates Metrics globally by counting the total true positives, false negatives, and false positives. <br>
**Weighted Precision:** Calculate metrics for each label, and find their average weighted by support (the number of true instances for each label). This alters ‘macro’ to account for label imbalance.<br><br>
Definitions taken from Scikit Learn documentation found [here](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.precision_score.html)

### Recall Score
The revall is intuitively the ability of the classifier to find all the positive samples
"""

# best value is 1 and worst value is 0
print("\nMacro Recall:", recall_score(y_test, y_predNB, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predNB, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predNB, average='weighted'))

"""Defintitions for the different types of recall are the same as precision. Documentation used can be found from SciKit [here](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.recall_score.html)

### 10 Fold Cross Validation

Evalulates a score by cross-validation. Takes the model, test attributes, and number of splits as parameters. SciKit documentation can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html)
"""

scoresNB = cross_val_score(modelNB, X_test, y_test, cv=10)

print("Accuracy: %0.2f(+/-%0.2f)" %(scoresNB.mean(), scoresNB.std()*2))
print(scoresNB)

"""#**kNN Classifier**"""

# create the kNN classifier 
modelK = neighbors.KNeighborsClassifier(n_neighbors=3)

# fit the model
modelK.fit(X_train, y_train)

# create prediction variable 
y_predK = modelK.predict(X_test)

print(y_predK)

"""### Accuracy score with 3NN"""

# accuracy score of 3NN
accuracy_score(y_test, y_predK) * 100

"""Predicted correctly about 53% of the time

### Trying different K values for kNN

Code chunk below checks the accuracy for different values of K from 1 to 10. <br> Code provided by Jason from the Collab Notebook
"""

# Code chunk provided by Jason in the Collab Notebook

# Create list to store results in outer scope.
acc_vs_k = []

# Let's try from k = 1 to k = 10.
for k in range(1, 11): # range(from inclusive beginning, to exclusive end)
  # Build model with k value.
  modelKnn = neighbors.KNeighborsClassifier(n_neighbors=k)
  
  # Fit the model with the training data.
  modelKnn.fit(X_train, y_train)

  # Use the fitted model to predict the classes for the test data.
  y_predKnn = modelKnn.predict(X_test)
  
  # Add the accuracy to the list for plotting.
  acc_vs_k.append(accuracy_score(y_test, y_predKnn))
  
print(acc_vs_k)

"""Returns the K with the highest accuracy from above. Code chunk provided by Jason"""

# Code chunk prvided by Jason in the Collab Notebook

idx_of_best_k = np.argmax(acc_vs_k)

# To avoid super-long lines, use a string with placeholders, pass it into
# print() calling format() on it to replace the placeholders.
# This is the so-called Pythonic way of doing things, which helps keep code
# clear and readable.
format_string = 'Best K value is {k_value} at index {idx} with acc of {acc}%.'
print(format_string.format(k_value=idx_of_best_k+1,
      idx=idx_of_best_k,
      acc=acc_vs_k[idx_of_best_k]*100))

"""### Precision and Recall for 3NN"""

# best value is 1 and worst value is 0
print("Macro Precision:",precision_score(y_test, y_predK, average='macro'))
print("Micro Precision:",precision_score(y_test, y_predK, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predK, average='weighted'))

print("Macro Recall:", recall_score(y_test, y_predK, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predK, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predK, average='weighted'))

"""### 10 Fold Cross Validation witk 3NN"""

scoresK = cross_val_score(modelK, X_test, y_test, cv=10)

print("Accuracy: %0.2f(+/-%0.2f)" %(scoresK.mean(), scoresK.std()*2))
print(scoresK)

"""### 10 Fold Cross Validation with 1-10 NN from above"""

scoresKNN = cross_val_score(modelKnn, X_test, y_test, cv = 10)

print("Accuracy: %0.2f(+/-%0.2f)" %(scoresKNN.mean(), scoresKNN.std()*2))
print(scoresKNN)

"""#**Decision Tree Classifier**

Decision Tree Classifiers use example code from the SciKit documentation found [here.](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html)
"""

# this classifier is using the gini index ("default") and no max depth
# it is also using the best split

# create decision tree classifier
dTreeClf = DecisionTreeClassifier() 

# train decision tree classifier
dTreeClf = dTreeClf.fit(X_train, y_train)

# predict response for test data set
y_predTree = dTreeClf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_predTree))

print("\nMacro Precision:", precision_score(y_test, y_predTree, average='macro'))
print("Micro Precision:", precision_score(y_test, y_predTree, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predTree, average='weighted' ))

print("\nMacro Recall:", recall_score(y_test, y_predTree, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predTree, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predTree, average='weighted'))

scoresT1 = cross_val_score(dTreeClf, X_test, y_test, cv=10)
print("\n10-Fold Accuracy: %0.2f(+/-%0.2f)" %(scoresT1.mean(), scoresT1.std()*2))
print(scoresT1)

"""We got a low accuracy so let's expeirment with dTree parameters"""

# this classifier is using entropy for the information gain and a max depth of 3
# it is also using the best split

# create decision tree classifier
dTreeClf = DecisionTreeClassifier(criterion="entropy", max_depth=3)

# train decision tree classifier
dTreeClf = dTreeClf.fit(X_train, y_train)

# predict response for test data set
y_predTree = dTreeClf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_predTree))

print("\nMacro Precision:", precision_score(y_test, y_predTree, average='macro'))
print("Micro Precision:", precision_score(y_test, y_predTree, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predTree, average='weighted' ))

print("\nMacro Recall:", recall_score(y_test, y_predTree, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predTree, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predTree, average='weighted'))

scoresT2 = cross_val_score(dTreeClf, X_test, y_test, cv=10)
print("\n10-Fold Accuracy: %0.2f(+/-%0.2f)" %(scoresT2.mean(), scoresT2.std()*2))
print(scoresT2)

# this classifier is using entropy for the gini and a max depth of 10
# it is also using the best split

# create decision tree classifier
dTreeClf = DecisionTreeClassifier(criterion="gini", max_depth=10)

# train decision tree classifier
dTreeClf = dTreeClf.fit(X_train, y_train)

# predict response for test data set
y_predTree = dTreeClf.predict(X_test)

print("Accuracy:", metrics.accuracy_score(y_test, y_predTree))

print("\nMacro Precision:", precision_score(y_test, y_predTree, average='macro'))
print("Micro Precision:", precision_score(y_test, y_predTree, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predTree, average='weighted' ))

print("\nMacro Recall:", recall_score(y_test, y_predTree, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predTree, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predTree, average='weighted'))

scoresT3 = cross_val_score(dTreeClf, X_test, y_test, cv=10)
print("\n10-Fold Accuracy: %0.2f(+/-%0.2f)" %(scoresT3.mean(), scoresT3.std()*2))
print(scoresT3)

"""Gini is the best criteria. And accuracy goes up slightly with a higher mex_depth but it isn't too noticable. Also as the Max Depth goes higher we run the risk of over classifying the tree

#**Random Forest Classifier**

### Making an instance of the classifier

Both Random Forest and SVM Classifiers are similar to Nathalie's Research code
"""

# creating an instance of the classification model
modelRF = ensemble.RandomForestClassifier(n_estimators=100)

# training the model
modelRF.fit(X_train, y_train)

"""###Finding the accuracy score of the random forest model"""

# making a RF prediction variable and calulcating the accuracy
y_predRF = modelRF.predict(X_test)

accuracy_score(y_test, y_predRF)

"""### Different precision and recall scores"""

print("\nMacro Precision:", precision_score(y_test, y_predRF, average='macro'))
print("Micro Precision:", precision_score(y_test, y_predRF, average='micro'))
print("Weighted Precision:", precision_score(y_test, y_predRF, average='weighted' ))

print("\nMacro Recall:", recall_score(y_test, y_predRF, average='macro'))
print("Micro Recall:", recall_score(y_test, y_predRF, average='micro'))
print("Weighted Recall:", recall_score(y_test, y_predRF, average='weighted'))

scoresRF = cross_val_score(modelRF, X_test, y_test, cv=10)
print("\n10-Fold Accuracy: %0.2f(+/-%0.2f)" %(scoresRF.mean(), scoresRF.std()*2))
print(scoresRF)

"""#**SVM Classifiers**

Function below trains the model so multiple SVM methods can be tested
"""

#function for accuracy and precision, see svm for parameters
def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # Fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)

    # Predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    if is_neural_net:
        predictions = predictions.argmax(axis=-1)

    return accuracy_score(y_test, predictions), precision_score(y_test, predictions, average=None).mean(), recall_score(y_test, predictions, average=None).mean()

"""SVM Methods used are:


*   SVM Linear
*   SVM RBF
*   SVM Polynomial
*   SVM Sigmoid 
*   RF<br>

Each method has it's accuracy, precision score, and recall score calculated. In addition to it's 10-Fold Cross Validation accuracy
"""

# SVM Linear
metrics = train_model(svm.SVC(kernel='linear', gamma='scale', random_state=42), X_train, y_train, X_test)
print("SVM, Kernel = 'linear',  ", metrics)

# SVM RBF
metrics = train_model(svm.SVC(kernel='rbf', gamma='scale'), X_train, y_train, X_test, )
print("SVM, Kernel = 'RBF' ,  ", metrics)

# SVM Polynomial
metrics = train_model(svm.SVC(kernel='poly', gamma='scale'), X_train, y_train, X_test)
print("SVM, Kernel = 'polynomial' ,  ", metrics)

# SVM Sigmoid
metrics = train_model(svm.SVC(kernel='sigmoid', gamma='scale'), X_train, y_train, X_test)
print("SVM, Kernel = 'sigmoid' ,  ", metrics)

# RF
metrics = train_model(ensemble.RandomForestClassifier(n_estimators=100), X_train, y_train, X_test)
print("RF, n_estimators = 100,  ", metrics)

# 10-Fold Cross validation

print("10-Fold Cross Validation Scores on TFIDF Vectors using SVM (Kernel = Linear)")
# 10-Fold Cross validation
clf_svm = svm.SVC(kernel='linear', gamma='scale', C=1, random_state=42)
scores_svm = cross_val_score(clf_svm, X_train, y_train, cv=10)
print(scores_svm)
print("Accuracy: %0.2f (+/- %0.2f)\n" % (scores_svm.mean(), scores_svm.std() * 2))

print("10-Fold Cross Validation Scores on TFIDF Vectors using SVM (Kernel = Polynomial)")
# 10-Fold Cross validation
clf_svm = svm.SVC(kernel='poly', gamma='scale', C=1, random_state=42)
scores_svm = cross_val_score(clf_svm, X_train, y_train, cv=10)
print(scores_svm)
print("Accuracy: %0.2f (+/- %0.2f)\n" % (scores_svm.mean(), scores_svm.std() * 2))

print("10-Fold Cross Validation Scores on TFIDF Vectors using SVM (Kernel = Sigmoid)")
# 10-Fold Cross validation
clf_svm = svm.SVC(kernel='sigmoid', gamma='scale', C=1, random_state=42)
scores_svm = cross_val_score(clf_svm, X_train, y_train, cv=10)
print(scores_svm)
print("Accuracy: %0.2f (+/- %0.2f)\n" % (scores_svm.mean(), scores_svm.std() * 2))

print("10-Fold Cross Validation Scores on TFIDF Vectors using SVM (Kernel = RBF)")
# 10-Fold Cross validation
clf_svm = svm.SVC(kernel='rbf', gamma='scale', C=1, random_state=42)
scores_svm = cross_val_score(clf_svm, X_train, y_train, cv=10)
print(scores_svm)
print("Accuracy: %0.2f (+/- %0.2f)\n" % (scores_svm.mean(), scores_svm.std() * 2))

"""---


#**Classification Methods using Full Data Set**

---

To classify the full data set, two methods are used. **Naive Bayes using a TFIDF vectorizer and partial fit** and using a **HashingVectorizer** on all classifiers

#**Naive Bayes on Full Data Set Using TfidfVectorizer**
"""

# set the full data set
full_data_set = "full_amazon_ff_reviews.csv"

# create the model
model = MultinomialNB()

# make lists for each chunk
X_test_chunk_list = []
y_test_chunk_list = []

# creating the vectorizer
vectorizer = TfidfVectorizer(stop_words='english')
do_once = 1

# read the data into the frame within a loop
for chunk in pd.read_csv(full_data_set, usecols=[5, 8], chunksize=100000):

    if(do_once == 1):
        X = vectorizer.fit_transform(chunk['Text'])
        do_once = 0
    else:
        X = vectorizer.transform(chunk['Text'])

    y = chunk['Rating']

    # split the data 80/20 and add random state 55
    X_train, X_test_chunk, y_train, y_test_chunk = train_test_split(X, y, test_size=0.2, random_state=55)

    # appened the chunks onto their respective lists
    X_test_chunk_list.append(X_test_chunk)
    y_test_chunk_list.append(y_test_chunk)

    model.partial_fit(X_train, y_train, classes=np.unique(y_train))

y_pred_list = [model.predict(test_chunk) for test_chunk in X_test_chunk_list]

# acccuracy score list
accuracy_score_list = [accuracy_score(y_test_chunk_list[index], y_pred_list[index]) for index in range(len(y_pred_list))] 

# precision score list
precision_score_list = [precision_score(y_test_chunk_list[index], y_pred_list[index], average=None).mean() for index in range(len(y_pred_list))]

# recall score list 
recall_score_list = [recall_score(y_test_chunk_list[index], y_pred_list[index], average=None).mean() for index in range(len(y_pred_list))]

print("---------------" + "AVG ACCURACY" + "---------------\n")
print(str(sum(accuracy_score_list)/len(accuracy_score_list))+'\n')

print("---------------" + "AVG PRECISION" + "---------------\n")
print(str(sum(precision_score_list)/len(precision_score_list))+ '\n')

print("---------------" + "AVG RECALL" + "---------------\n")
print(str(sum(recall_score_list)/len(recall_score_list))+ '\n')

# function that prints restils for the HashingVectorizer
def results_function(model, X_test, y_test, y_pred):
  print("Accuracy:", accuracy_score(y_test, y_pred))

  print("\nMacro Precision:", precision_score(y_test, y_pred, average='macro'))
  print("Micro Precision:", precision_score(y_test, y_pred, average='micro'))
  print("Weighted Precision:", precision_score(y_test, y_pred, average='weighted' ))

  print("\nMacro Recall:", recall_score(y_test, y_pred, average='macro'))
  print("Micro Recall:", recall_score(y_test, y_pred, average='micro'))
  print("Weighted Recall:", recall_score(y_test, y_pred, average='weighted'))

  scores = cross_val_score(model, X_test, y_test, cv=10)
  print("\n10-Fold Accuracy: %0.2f(+/-%0.2f)" %(scores.mean(), scores.std()*2))
  print(scores)

"""##Dataframe for full text"""

# create a dataframe that is using the full dataset 
H_df = pd.read_csv(full_data_set, usecols=[5, 8])

"""### Counting the Full Data"""

# counting the number of ratings in the full set
rating_counts_full = H_df.groupby('Rating')['Rating'].count()
rating_counts_full.head()

# getting the ratios of the ratings
rating_counts_full / len(H_df)

H_df.describe()

"""##Creating the HashingVectorizer"""

# creates the HashingVectorizer that will be used with the full data
H_vectorizer = HashingVectorizer(stop_words='english', alternate_sign=False)
H_X = H_vectorizer.transform(H_df['Text'])
H_y = H_df['Rating']

# splits the data 80/20 with random state 55
H_X_train, H_X_test, H_y_train, H_y_test = train_test_split(H_X, H_y, test_size=0.2, random_state=55)

"""##NB Classifier with HashingVectorizer"""

H_modelNB = MultinomialNB()
H_modelNB.fit(H_X_train, H_y_train)
H_y_predNB = H_modelNB.predict(H_X_test)

results_function(H_modelNB, H_X_test, H_y_test, H_y_predNB)

"""##kNN Classifier with HashingVectorizer and K = 3"""

H_modelK = neighbors.KNeighborsClassifier(n_neighbors=3)
H_modelK.fit(H_X_train, H_y_train)
H_y_predK = H_modelK.predict(H_X_test)

results_function(H_modelK, H_X_test, H_y_test, H_y_predK)

"""##Decision Tree Classifier with HashingVectorizer

###No params
"""

H_dTreeClf = DecisionTreeClassifier()
H_dTreeClf = H_dTreeClf.fit(H_X_train, H_y_train)
H_y_predTREE = H_dTreeClf.predict(H_X_test)

results_function(H_dTreeClf, H_X_test, H_y_test, H_y_predTREE)

"""###Params entropy & max_depth 3"""

H_dTreeClf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
H_dTreeClf = H_dTreeClf.fit(H_X_train, H_y_train)
H_y_predTREE3 = H_dTreeClf.predict(H_X_test)

results_function(H_dTreeClf, H_X_test, H_y_test, H_y_predTREE3)

"""###Params gini & max_depth 10"""

H_dTreeClf = DecisionTreeClassifier(criterion="gini", max_depth=10)
H_dTreeClf = H_dTreeClf.fit(H_X_train, H_y_train)
H_y_predTREE10 = H_dTreeClf.predict(H_X_test)

results_function(H_dTreeClf, H_X_test, H_y_test, H_y_predTREE10)

"""##Random Forest Classifier with HashingVectorizer"""

H_modelRF = ensemble.RandomForestClassifier(n_estimators=100)
H_modelRF = H_modelRF.fit(H_X_train, H_y_train)
H_y_predRF = H_modelRF.predict(H_X_test)

results_function(H_dTreeClf, H_X_test, H_y_test, H_y_predRF)

"""##SVM Classifiers with HashingVectorizer

###SVM LINEAR
"""

H_SVML = svm.SVC(kernel='linear', gamma='scale', random_state=42)
H_SVML = H_SVML.fit(H_X_train, H_y_train)
H_y_predL = H_SVML.fit.predict(H_X_test)

results_function(H_SVML, H_X_test, H_y_test, H_y_predL)

"""###SVM RBF"""

H_SVMRBF = svm.SVC(kernel='rbf', gamma='scale', random_state=42)
H_SVMRBF = H_SVMRBF.fit(H_X_train, H_y_train)
H_y_predRBF = H_SVMRBF.fit.predict(H_X_test)

results_function(H_SVMRBF, H_X_test, H_y_test, H_y_predRBF)

"""###SVM POLY"""

H_SVMP = svm.SVC(kernel='poly', gamma='scale', random_state=42)
H_SVMP = H_SVMP.fit(H_X_train, H_y_train)
H_y_predP = H_SVMP.fit.predict(H_X_test)

results_function(H_SVMP, H_X_test, H_y_test, H_y_predP)

"""###SVM SIGMOID"""

H_SVMSIG = svm.SVC(kernel='sigmoid', gamma='scale', random_state=42)
H_SVMSIG = H_SVMSIG.fit(H_X_train, H_y_train)
H_y_predSIG = H_SVMSIG.fit.predict(H_X_test)

results_function(H_SVMSIG, H_X_test, H_y_test, H_y_predSIG)

program_end = time.time()
print(program_end - program_start)