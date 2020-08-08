import pickle
import numpy as np
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression


def create_x(size, rank):
    """
    * 创建系数矩阵X
    * size - 2×size+1 = window_size
    * rank - 拟合多项式阶次
    * x - 创建的系数矩阵
    """
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m ** j for j in range(rank)]
        x.append(row)
    x = np.mat(x)
    return x


def savgol(data, window_size, rank):
    """
     * Savitzky-Golay平滑滤波函数
     * data - list格式的1×n纬数据
     * window_size - 拟合的窗口大小
     * rank - 拟合多项式阶次
     * ndata - 修正后的值
    """
    m = int((window_size - 1) / 2)
    odata = data.tolist()
    # 处理边缘数据，首尾增加m个首尾项
    for i in range(m):
        odata.insert(0, odata[0])
        odata.insert(len(odata), odata[len(odata) - 1])
    # 创建X矩阵
    x = create_x(m, rank)
    # 计算加权系数矩阵B
    b = (x * (x.T * x).I) * x.T
    a0 = b[m]
    a0 = a0.T
    # 计算平滑修正后的值
    ndata = []
    for i in range(len(data)):
        y = [odata[i + j] for j in range(window_size)]
        y1 = np.mat(y) * a0
        y1 = float(y1)
        ndata.append(y1)
    return np.array(ndata, dtype=float)


class SpecSVRModel(object):
    def __init__(self):
        self.mosi_model = SVR(kernel="rbf", C=100000, gamma="auto", epsilon=1e-3)
        self.don_model = SVR(kernel="rbf", C=100000, gamma="auto", epsilon=1e-3)

    def fit(self, database):
        x = database.database["spec"]
        x = [x.iloc[row_idx] for row_idx in range(x.shape[0])]
        x = np.array(x)
        mosi_y = database.database["mosi"].values
        don_y = database.database["don"].values
        self.mosi_model.fit(x, mosi_y)
        self.don_model.fit(x, don_y)

    def predict(self, x):
        return self.mosi_model.predict(x), self.don_model.predict(x)

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump((self.mosi_model, self.don_model), f)

    def load(self, filepath):
        with open(filepath, "rb") as f:
            self.mosi_model, self.don_model = pickle.load(f)


class SpecLRModel(object):
    def __init__(self):
        self.mosi_model = LinearRegression()
        self.don_model = LinearRegression()

    def fit(self, database):
        x = database.database["spec"]
        x = [x.iloc[row_idx] for row_idx in range(x.shape[0])]
        x = np.array(x)
        mosi_y = database.database["mosi"].values
        don_y = database.database["don"].values
        self.mosi_model.fit(x, mosi_y)
        self.don_model.fit(x, don_y)

    def predict(self, x):
        return self.mosi_model.predict(x), self.don_model.predict(x)

    def save(self, filepath):
        with open(filepath, "wb") as f:
            pickle.dump((self.mosi_model, self.don_model), f)

    def load(self, filepath):
        with open(filepath, "rb") as f:
            self.mosi_model, self.don_model = pickle.load(f)
