# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import time
from datetime import datetime

import numpy as np
import pandas as pd
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIntValidator, QStandardItem, QStandardItemModel, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QAbstractItemView, QFileDialog, QMessageBox

from manWin import Ui_MainWindow  # 主界面
from specctrl import SpecCtrl
from specModel import SpecSVRModel, SpecLRModel

# 用于线程之间交流的全局变量
global wave_len, spec_value, int_time, avg_time, measure_mode, reading_status, isMeasuring
isMeasuring, measure = False, "DARK"
global spectrometer
spectrometer = SpecCtrl()


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # my code here
        self.switch_connect_status(False)
        self.config_lineEdit()

        self.model_SVR = SpecSVRModel()
        self.model_LR = SpecLRModel()

        self.matplotlibWidget_spec.setVisible(False)

        self.checkBox_continuous.stateChanged.connect(
            self.measure_mode_changed)

        self.model_data = QStandardItemModel(0, 3)
        self.model_data.setHorizontalHeaderLabels(['采集时间', '水分', 'DON'])
        self.database = SpecDataBase()
        self.tableView_data.setModel(self.model_data)
        self.tableView_data.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_data.horizontalHeader().setStretchLastSection(True)
        self.tableView_data.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView_data.clicked.connect(self.fresh_plot)

        self.measure_thread = MeasureThread()
        self.measure_thread.start()
        self.measure_thread.trigger.connect(self.measure_finished)

        self.continuous_timer = QTimer(self)
        self.continuous_timer.timeout.connect(self.update_timer)

        self.label_don.setFont(QFont("SimSun", 14))
        self.label_don_level.setFont(QFont("SimSun", 14))
        self.label_mosi.setFont(QFont("SimSun", 14))

    @pyqtSlot()
    def on_pushButton_connect_clicked(self):
        if spectrometer.status:
            spectrometer.disconnect()
            self.switch_connect_status(False, 'spec')
            self.matplotlibWidget_spec.setVisible(False)
        else:
            spectrometer.connect()
            if spectrometer.status:
                self.lineEdit_int_time.setEnabled(True)
                self.lineEdit_avg_time.setEnabled(True)
                self.pushButton_dark_ref.setEnabled(True)
                self.switch_connect_status(True, 'data')
                # self.pushButton_white_ref.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_dark_ref_clicked(self):
        global int_time, avg_time, measure_mode, isMeasuring
        int_time = self.lineEdit_int_time.text()
        avg_time = self.lineEdit_avg_time.text()

        int_time = 50 if int_time == "" else int(int_time)
        avg_time = 1 if avg_time == "" else int(avg_time)
        measure_mode = 'DARK'
        # 开始测量，等结束了唤醒measure finished
        # self.measure_thread.start()
        isMeasuring = True
        self.pushButton_sample.setEnabled(False)
        self.pushButton_white_ref.setEnabled(False)
        self.pushButton_dark_ref.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_white_ref_clicked(self):
        global int_time, avg_time, measure_mode, isMeasuring
        int_time = self.lineEdit_int_time.text()
        avg_time = self.lineEdit_avg_time.text()

        int_time = 50 if int_time == "" else int(int_time)
        avg_time = 1 if avg_time == "" else int(avg_time)
        measure_mode = 'LIGHT'
        # 开始测量，等结束了唤醒measure finished
        # self.measure_thread.start()
        isMeasuring = True
        self.pushButton_sample.setEnabled(False)
        self.pushButton_white_ref.setEnabled(False)
        self.pushButton_dark_ref.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_sample_clicked(self):
        """
        Slot documentation goes here.
        """
        global int_time, avg_time, measure_mode, isMeasuring
        if self.checkBox_continuous.isChecked():
            measure_interval = self.lineEdit_param_interval.text()
            measure_interval = 0 if measure_interval == "" else int(
                measure_interval)
            measure_mode = 'REFER'
            self.continuous_timer.start(measure_interval * 1000)
        else:
            int_time = self.lineEdit_int_time.text()
            avg_time = self.lineEdit_avg_time.text()
            int_time = 50 if int_time == "" else int(int_time)
            avg_time = 1 if avg_time == "" else int(avg_time)
            measure_mode = 'REFER'
            isMeasuring = True
            self.pushButton_sample.setEnabled(False)
            self.pushButton_white_ref.setEnabled(False)
            self.pushButton_dark_ref.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_add_label_clicked(self):
        if self.tableView_data.currentIndex().isValid() == False:
            return
        index = self.tableView_data.currentIndex().row()
        mosi = np.nan if self.lineEdit_mosi.text() is "" else float(self.lineEdit_mosi.text())
        don = np.nan if self.lineEdit_don.text() is "" else float(self.lineEdit_don.text())
        self.database.set_label(index, mosi, don)
        self.model_data.setItem(index, 1, QStandardItem(str(mosi)))
        self.model_data.setItem(index, 2, QStandardItem(str(don)))

    @pyqtSlot()
    def on_pushButton_del_label_clicked(self):
        if self.tableView_data.currentIndex().isValid() == False:
            return
        index = self.tableView_data.currentIndex().row()
        mosi = np.nan
        don = np.nan
        self.database.remove_label(index)
        self.model_data.setItem(index, 1, QStandardItem(str(mosi)))
        self.model_data.setItem(index, 2, QStandardItem(str(don)))

    @pyqtSlot()
    def on_pushButton_del_data_clicked(self):
        if self.tableView_data.currentIndex().isValid() == False:
            return
        index = self.tableView_data.currentIndex().row()
        self.database.remove(index=index)
        self.model_data.removeRow(index)

    @pyqtSlot()
    def on_pushButton_save_data_clicked(self):
        if self.database.shape[0] == 0:
            return
        fname, _ = QFileDialog.getSaveFileName(self, "Save File", filter="EXCEL Files (*.xlsx)")
        if fname is not '':
            self.database.save(fname, header=[wave_len[i] for i in range(wave_len.shape[0])])

    @pyqtSlot()
    def on_pushButton_load_data_clicked(self):
        global wave_len
        fname, _ = QFileDialog.getOpenFileName(self, "Save File", filter="EXCEL Files (*.xlsx)")
        if fname is "":
            return
        self.model_data.clear()
        self.model_data.setHorizontalHeaderLabels(['采集时间', '水分', 'DON'])
        wave_len = self.database.load(file_path=fname, is_append=True)
        for row_idx in range(self.database.shape[0]):
            temp = self.database.get_row(row_idx)
            content = [QStandardItem(str(temp["time"])), QStandardItem(str(temp["mosi"])),
                       QStandardItem(str(temp["don"]))]
            self.model_data.appendRow(content)
        self.tableView_data.resizeColumnsToContents()

    @pyqtSlot()
    def on_pushButton_save_model_clicked(self):
        model = {"线性回归": self.model_LR, "支持向量回归": self.model_SVR}[self.comboBox_model_selection.currentText()]
        fname, _ = QFileDialog.getSaveFileName(self, "Save Model", filter="Model File (*.model)")
        if fname is not '':
            model.save(fname)

    @pyqtSlot()
    def on_pushButton_load_model_clicked(self):
        model = {"线性回归": self.model_LR, "支持向量回归": self.model_SVR}[self.comboBox_model_selection.currentText()]
        fname, _ = QFileDialog.getOpenFileName(self, "Load Model", filter="Model File (*.model)")
        if fname is not '':
            model.load(fname)
            self.checkBox_pred.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_train_model_clicked(self):
        model = {"线性回归": self.model_LR, "支持向量回归": self.model_SVR}[self.comboBox_model_selection.currentText()]
        self.pushButton_train_model.setEnabled(False)
        self.pushButton_load_model.setEnabled(False)
        self.pushButton_save_model.setEnabled(False)
        QApplication.processEvents()
        if self.database.shape[0] is not 0:
            model.fit(self.database)
        QMessageBox.information(self, "训练完毕", '训练完毕')
        self.pushButton_train_model.setEnabled(True)
        self.pushButton_load_model.setEnabled(True)
        self.pushButton_save_model.setEnabled(True)
        self.checkBox_pred.setEnabled(True)

    def switch_connect_status(self, status=True, set_range='all'):
        assert set_range in ["all", 'spec', 'data']
        if (set_range is "spec") or (set_range is "all"):
            self.lineEdit_int_time.setEnabled(status)
            self.lineEdit_avg_time.setEnabled(status)
            self.lineEdit_param_interval.setEnabled(status)

            self.pushButton_dark_ref.setEnabled(status)
            self.pushButton_white_ref.setEnabled(status)
            self.pushButton_sample.setEnabled(status)

            self.checkBox_continuous.setEnabled(status)
            self.checkBox_continuous.setChecked(False)
            self.checkBox_pred.setEnabled(status)

        if (set_range is "data") or (set_range is "all"):
            self.lineEdit_mosi.setEnabled(status)
            self.lineEdit_don.setEnabled(status)
            self.pushButton_add_label.setEnabled(status)
            self.pushButton_save_data.setEnabled(status)
            self.pushButton_save_model.setEnabled(status)
            self.pushButton_train_model.setEnabled(status)
            self.pushButton_del_label.setEnabled(status)
            self.pushButton_del_data.setEnabled(status)
            self.comboBox_model_selection.setEnabled(status)
            self.tableView_data.setEnabled(status)

    def config_lineEdit(self):
        int_time_validator = QIntValidator(self)
        avg_time_validator = QIntValidator(self)
        param_interval_validator = QIntValidator(self)
        int_time_validator.setRange(2, 40000)
        avg_time_validator.setRange(1, 500)
        param_interval_validator.setRange(0, 6000)
        self.lineEdit_int_time.setValidator(int_time_validator)
        self.lineEdit_avg_time.setValidator(avg_time_validator)
        self.lineEdit_param_interval.setValidator(param_interval_validator)

        # mosi_validator = QDoubleValidator(self)
        # don_validator = QDoubleValidator(self)
        # mosi_validator.setRange(0, 100)
        # don_validator.setRange(0, 1000000)
        # self.lineEdit_mosi.setValidator(mosi_validator)
        # self.lineEdit_don.setValidator(don_validator)

    def measure_mode_changed(self):
        print('measure mode changed')
        if self.checkBox_continuous.isChecked():
            self.lineEdit_param_interval.setEnabled(True)
        else:
            self.lineEdit_param_interval.setEnabled(False)
            self.continuous_timer.stop()

    def clear_all(self):
        self.matplotlibWidget_spec.mpl.axes.cla()

    def measure_finished(self):
        if self.checkBox_continuous.isChecked():
            if reading_status:
                measure_interval = self.lineEdit_param_interval.text()
                measure_interval = 0 if measure_interval == "" else int(
                    measure_interval)
                self.matplotlibWidget_spec.setVisible(True)
                self.matplotlibWidget_spec.mpl.draw_spec(wave_len, spec_value)
                if self.checkBox_pred.isChecked():
                    model = {"线性回归": self.model_LR, "支持向量回归":
                                self.model_SVR}[self.comboBox_model_selection.currentText()]
                    mosi, don = model.predict(spec_value.reshape(1, -1))
                    self.label_mosi.setText(str(mosi[0]))
                    self.label_don.setText(str(don[0]))
                    self.label_don_level.setText(str("超标" if don[0] > 1 else "合格"))
                self.add_spec()
                print('get wave_length shape: {}, spec shape: {}'.format(
                    wave_len.shape, spec_value.shape))
                self.continuous_timer.start(measure_interval * 1000)
            else:
                print('read failed')
        else:
            if reading_status:
                self.matplotlibWidget_spec.setVisible(True)
                self.matplotlibWidget_spec.mpl.draw_spec(wave_len, spec_value)
                self.pushButton_white_ref.setEnabled(True)
                self.add_spec()
                if self.checkBox_pred.isChecked() and measure_mode is "REFER":
                    model = {"线性回归": self.model_LR, "支持向量回归":
                                self.model_SVR}[self.comboBox_model_selection.currentText()]
                    mosi, don = model.predict(spec_value.reshape(1, -1))
                    self.label_mosi.setText(str(mosi[0]))
                    self.label_don.setText(str(don[0]))
                    self.label_don_level.setText(str("超标" if don[0] > 1 else "合格"))
                print('get wave_length shape: {}, spec shape: {}'.format(
                    wave_len.shape, spec_value.shape))
                if measure_mode is "DARK":
                    self.pushButton_dark_ref.setEnabled(True)
                    self.pushButton_white_ref.setEnabled(True)
                else:
                    self.pushButton_sample.setEnabled(True)
                    self.pushButton_white_ref.setEnabled(True)
                    self.pushButton_dark_ref.setEnabled(True)
                    self.checkBox_continuous.setEnabled(True)
                    self.checkBox_continuous.setChecked(False)
            else:
                print('read failed')

    def update_timer(self):
        global isMeasuring
        while isMeasuring:
            pass
        isMeasuring = True
        self.continuous_timer.stop()

    def add_spec(self):
        now_str = datetime.now().strftime("%H:%M:%S")
        mosi = np.nan if self.lineEdit_mosi.text() is "" else float(self.lineEdit_mosi.text())
        don = np.nan if self.lineEdit_don.text() is "" else float(self.lineEdit_don.text())
        row_list = [QStandardItem(now_str), QStandardItem(
            str(mosi)), QStandardItem(str(don))]
        self.model_data.appendRow(row_list)
        self.database.add(spec=spec_value, meas_time=now_str, mosi=mosi, don=don)

    def fresh_plot(self):
        global wave_len, spec_value
        idx = self.tableView_data.currentIndex().row()
        temp = self.database.get_row(idx)
        spec_value = temp["spec"]
        self.lineEdit_don.setText(str(temp["don"]))
        self.lineEdit_mosi.setText(str(temp['mosi']))
        self.matplotlibWidget_spec.mpl.draw_spec(wave_len=wave_len, spec_val=spec_value)
        self.matplotlibWidget_spec.setVisible(True)
        if self.checkBox_pred.isChecked():
            model = {"线性回归": self.model_LR, "支持向量回归": self.model_SVR}[self.comboBox_model_selection.currentText()]
            model.predict(spec_value.reshape(1, -1))


class MeasureThread(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(MeasureThread, self).__init__()

    def run(self):
        while True:
            global isMeasuring
            if isMeasuring:
                global measure_mode, int_time, avg_time, wave_len, spec_value
                try:
                    print("spectrometer status : {}".format(spectrometer.status))
                    wave_len, spec_value = spectrometer.measure(mode=measure_mode, inter_time=int_time,
                                                                avg_scan=avg_time,
                                                                transmission_wait=0.001)
                    # self.checkBox_pred.setEnabled(True)
                    global reading_status
                    reading_status = True
                except:
                    reading_status = False
                    print("Get problem when reading the spectrometer")
                    spectrometer.disconnect()
                isMeasuring = False
                # 循环完毕后发出信号
                self.trigger.emit()
            time.sleep(0.05)


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


if __name__ == "__main__":
    try:
        import sys

        app = QApplication(sys.argv)
        ui = MainWindow()
        ui.show()
        sys.exit(app.exec_())
    except:
        sys.exit()

