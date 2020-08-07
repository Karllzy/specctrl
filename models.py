import numpy as np
from sklearn.svm import SVC


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
        row = [m**j for j in range(rank)]
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
        odata.insert(len(odata), odata[len(odata)-1])
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


class SpecModel:
    def __init__(self):
        self.data_base = {0: [np.zeros(1, 255), (0.67, )]}

    def add_data(self, idx=None, x=None, y=None):
        if idx is not None:
            if idx in self.data_base:
                if x is not None:
                    self.data_base[idx][0] = x
                if y is not None:
                    self.data_base[idx][1] = y
        else:
            idx = int(max(self.data_base.keys()) + 1)
            self.data_base[idx] = [np.zeros(1, 255), 0.5]
            if x is not None:
                self.data_base[idx][0] = x
            if y is not None:
                self.data_base[idx][1] = y

    def get_data(self, idx):
        if idx in self.data_base.keys():
            return self.data_base[idx][0], self.data_base[idx][1]


if __name__ == '__main__':
    clf = SVC(C=1.0, kernel='rbf', degree=3, gamma='auto', coef0=0.0, shrinking=True,
              probability=False, tol=0.001, cache_size=200, class_weight=None,
              verbose=False, max_iter=-1, decision_function_shape='ovr',
              random_state=None)
    import specctrl
    zxh = specctrl.SpecCtrl()
    x, y = [], []
    wave_len, spec = zxh.get_spec(first=True)
    x.append(wave_len)
    y.append(input('Please input the CLASS:'))
    for i in range(3):
        wave_len, spec = zxh.get_spec(first=False)
        x.append(spec)
        y.append(input('Please input the CLASS:'))

    x, y = np.array(x), np.array(y)
    clf.fit(x, y)

    wave_len, spec = zxh.get_spec()
    spec = np.array(spec)
    spec = spec.reshape((1, -1))
    print(clf.predict(spec))


