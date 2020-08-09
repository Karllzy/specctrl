import pandas as pd
import numpy as np


class SpecDataBase(object):
    def __init__(self):
        self.database = pd.DataFrame(
            {"spec": [], "time": [], "mosi": [], "don": []})
        self.shape = (0, 4)

    def __str__(self):
        return self.database.__str__()

    def add(self, spec, meas_time, mosi, don):
        self.database.loc[self.database.shape[0]] = [
            spec, meas_time, mosi, don]
        self.shape = (self.shape[0] + 1, self.shape[1])

    def set_label(self, index, mosi, don):
        self.database.loc[index, "mosi"] = mosi
        self.database.loc[index, "don"] = don

    def remove(self, index):
        self.database.drop(index=index, inplace=True)
        self.database.reset_index(drop=True, inplace=True)
        self.shape = (self.shape[0] - 1, self.shape[1])

    def remove_label(self, index):
        self.database.loc[index, ["mosi", "don"]] = np.NaN

    def get_row(self, index):
        return self.database.iloc[index, :].copy()

    def load(self, file_path, is_append=False):
        # tmp_data = pd.read_excel(file_path, header=0)
        with open(file_path, 'rb') as f:
            tmp_data = pd.read_excel(f, sheet_name="index", header=0)
            temp = pd.read_excel(f, sheet_name="data", header=0)
            wave_length = np.array(temp.columns.values.tolist(), dtype=np.float)
            temp = temp.values
            # tmp_data["spec"] = [temp[i, :] for i in range(temp.shape[0])]
            tmp_data.insert(0, "spec", [temp[i, :]
                                        for i in range(temp.shape[0])])
        if is_append:
            self.database = self.database.append(tmp_data)
        else:
            self.database = tmp_data.copy()
        self.database.reset_index(drop=True, inplace=True)
        self.shape = self.database.shape
        return wave_length

    def save(self, file_path, header=None):
        data_spec = self.database.loc[:, "spec"]
        data_spec = np.array([data_spec.iloc[i]
                              for i in range(data_spec.shape[0])])
        data_spec = pd.DataFrame(data_spec)
        if header is not None:
            data_spec.columns = header
        with pd.ExcelWriter(file_path) as writer:  # doctest: +SKIP
            self.database.iloc[:, 1:].to_excel(
                writer, sheet_name='index', index=False)
            data_spec.to_excel(writer, sheet_name="data", index=False)
