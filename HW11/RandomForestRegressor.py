import pandas as pd
import numpy as np
import warnings
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

warnings.filterwarnings("ignore")

data = pd.read_csv('ckd-dataset-v2.csv')

numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns
data[numeric_cols] = data[numeric_cols].fillna(data[numeric_cols].mean())

for col in data.select_dtypes(include=['object']).columns:
    data[col].fillna(data[col].mode()[0], inplace=True)

data = pd.get_dummies(data, columns=['class'], drop_first=True)

y = data['grf']  # 預測 grf
X = data.drop(columns=['grf'])  # 其餘欄位作為特徵

scaler = StandardScaler()
numeric_features = X.select_dtypes(include=['float64', 'int64']).columns
X[numeric_features] = scaler.fit_transform(X[numeric_features])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=100)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error (MSE): {mse:.2f}')
print(f'Root Mean Squared Error (RMSE): {rmse:.2f}')
print(f'R² Score: {r2:.2f}')
plt.figure(figsize=(6, 6))
sn.regplot(x=y_test, y=y_pred, line_kws={"color": "red"})
plt.xlabel('True GRF')
plt.ylabel('Predicted GRF')
plt.title('Random Forest Regression')
plt.grid(True)
plt.show()