import pandas as pd
import numpy as np
import seaborn as sb
from sklearn import preprocessing
from sklearn import utils
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.base import ClassifierMixin
from sklearn.base import RegressorMixin
from sklearn.base import BaseEstimator
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import classification_report

df = pd.read_csv('C:/Users/Lenovo/Desktop/Proba zavrsnog rada - Copy.csv', header=0)
cols_to_drop = ['Date','open_btc','high_btc','low_btc','close_btc','Broj redova','Rezultat','MAVG 72','Avg','Mavg','Granica','Buduci Trend','Granica','EMA 12','EMA 72','MULTIPLIER 12','Change','GAIN','LOSS','AVG GAIN','AVG LOSS','RS','MSTD(12)','MSTD(72)','BT']
df = df.drop(cols_to_drop, axis=1)

sb.heatmap(df.isnull())

df['RSI'] = df['RSI'].interpolate()
df['MAVG'] = df['MAVG'].interpolate()
df['MACD'] = df['MACD'].interpolate()
df['MSTD'] = df['MSTD'].interpolate()

df = df.dropna()




X = df.values
y = df['BTZ'].values

X = np.delete(X,2,axis=1)



X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.3,random_state=0)
rf_clf = ensemble.RandomForestClassifier(n_estimators=40)
rf_clf.fit(X_train, y_train)

s = rf_clf.score(X_test, y_test)
print(s)

y_pred = rf_clf.predict(X_test)
confusion = confusion_matrix(y_test, y_pred)
print('Confusion Matrix\n')
print(confusion)
print('\nAccuracy: {:.2f}\n'.format(accuracy_score(y_test, y_pred)))

print('Weighted Precision: {:.2f}'.format(precision_score(y_test, y_pred, average='weighted')))
print('Weighted Recall: {:.2f}'.format(recall_score(y_test, y_pred, average='weighted')))
print('Weighted F1-score: {:.2f}'.format(f1_score(y_test, y_pred, average='weighted')))

print('\nClassification Report\n')
print(classification_report(y_test, y_pred, target_names=['Class 1', 'Class 2', 'Class 3']))


