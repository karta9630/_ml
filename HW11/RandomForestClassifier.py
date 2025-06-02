import pandas as pd
import numpy as np
import warnings
import seaborn as sn
import matplotlib.pyplot as plt  
import seaborn as sns  
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score  # 导入额外的评估函数
from imblearn.over_sampling import SMOTE

warnings.filterwarnings("ignore")

data = pd.read_csv('ckd-dataset-v2.csv')


numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

for col in data.select_dtypes(include=['object']).columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

data = pd.get_dummies(data, columns=['class'], drop_first=True)

scaler = StandardScaler()
data[['wbcc', 'grf']] = scaler.fit_transform(data[['wbcc', 'grf']])

X = data.drop(columns=[col for col in data.columns if col.startswith('class_')])
y = data[[col for col in data.columns if col.startswith('class_')]]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=100)

#  RandomForestClassifier
model = RandomForestClassifier(random_state=42, max_samples=0.3, bootstrap=True)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

conf_matrix = confusion_matrix(y_test, y_pred)
conf_matrix[0, 0], conf_matrix[1, 1] = conf_matrix[1, 1], conf_matrix[0, 0]

print("Confusion Matrix:")
print(conf_matrix)


row_sums = conf_matrix.sum(axis=1, keepdims=True)

percent_matrix = conf_matrix.astype('float') / row_sums  


precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)


print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"accuracy:{accuracy:.2f}")
print(f"Training set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

sn.heatmap(percent_matrix, annot=True, fmt='.2f', cmap='Blues',
           xticklabels=['Positive', 'Negative'], yticklabels=['Positive', 'Negative']
            )
