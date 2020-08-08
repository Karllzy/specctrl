import numpy as np
from sklearn.svm import SVC





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