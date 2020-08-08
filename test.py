import math

import numpy as np
from sklearn.metrics import *

from callMainWin import SpecDataBase
from specModel import SpecLRModel

SRC_DATA_PATH = "./test_data.xlsx"

if __name__ == '__main__':
    database = SpecDataBase()
    database.load(SRC_DATA_PATH)
    database_train = SpecDataBase()
    database_train.database = database.database.loc[:100, :]
    database_test = SpecDataBase()
    database_test.database = database.database.loc[101:, :]

    model = SpecLRModel()
    model.fit(database_train)
    x_test = np.array([database_test.database.loc[row, "spec"] for row in range(101, 101 + database_test.database.shape[0])])
    y_test = np.array(
        [database_test.database.loc[row, "mosi"] for row in range(101, 101 + database_test.database.shape[0])])
    y_pred, _ = model.predict(x_test)

    y_test = np.squeeze(y_test)
    y_pred = np.squeeze(y_pred)

    r2 = r2_score(y_test, y_pred)
    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    nrmse = math.sqrt(mean_squared_error(y_test, y_pred)) / np.mean(y_pred) * 100
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    nmbe = np.abs(np.sum(y_pred - y_test)) / y_test.shape[0] / np.mean(y_pred) * 100

    print("R^2=%.9f" % r2)
    print("RMSE=%.1f" % rmse)
    print("nRMSE=%.1f%%" % nrmse)
    print("MAPE=%.1f%%" % mape)
    print("nMBE=%.1f%%" % nmbe)
