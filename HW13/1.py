import numpy as np
import matplotlib.pyplot as plt

# 生成人工資料（[-2,3], [-3,4]）
X_class1 = np.array([[2, 3], [3, 4], [4, 5]])
X_class2 = np.array([[-1, -3], [-2, -2], [-3, -4]])

# 合併資料並給定標籤 (+1, -1)
X = np.vstack((X_class1, X_class2))
y = np.array([1]*3 + [-1]*3)

# 初始化權重
weights = np.zeros(2)

# Hebbian 學習規則：w_new = w_old + η * x * y
learning_rate = 0.1

for xi, target in zip(X, y):
    weights += learning_rate * xi * target

print("學習後的權重：", weights)

# 視覺化資料與分類邊界
def plot_decision_boundary(w):
    x_vals = np.linspace(-5, 5, 100)
    y_vals = -(w[0]/w[1]) * x_vals
    plt.plot(x_vals, y_vals, 'k--')

plt.scatter(X_class1[:, 0], X_class1[:, 1], color='blue', label='Class +1')
plt.scatter(X_class2[:, 0], X_class2[:, 1], color='red', label='Class -1')
plot_decision_boundary(weights)
plt.legend()
plt.title('Hebbian Learning Decision Boundary')
plt.grid(True)
plt.show()
