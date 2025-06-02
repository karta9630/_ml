import pandas as pd
import numpy as np
import warnings
import seaborn as sn
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score

warnings.filterwarnings("ignore")

data = pd.read_csv('ckd-dataset-v2.csv')

for col in data.select_dtypes(include=['object']).columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

data = pd.get_dummies(data, columns=['class'], drop_first=True)
y = data[[col for col in data.columns if col.startswith('class_')]]
X = data.drop(columns=[col for col in data.columns if col.startswith('class_')])

# 4. 標準化特徵
scaler = StandardScaler()
X[['wbcc', 'grf']] = scaler.fit_transform(X[['wbcc', 'grf']])

X_train, X_test, y_train, y_test = train_test_split(X, y.values.ravel(), test_size=0.4, random_state=200)

kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X_train)

y_pred = kmeans.predict(X_test)

conf_matrix = confusion_matrix(y_test, y_pred)
row_sums = conf_matrix.sum(axis=1, keepdims=True)
conf_matrix_percent = conf_matrix.astype('float') / row_sums

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)

# 10. 輸出結果
print("Confusion Matrix:")
print(conf_matrix)
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"Accuracy: {accuracy:.2f}")
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

sn.heatmap(conf_matrix_percent, annot=True, fmt='.2f', cmap='Blues',
           xticklabels=['Positive', 'Negative'], yticklabels=['Positive', 'Negative'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('KMeans Clustering')
plt.show()
