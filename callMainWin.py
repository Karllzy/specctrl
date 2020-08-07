# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

import time

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QMainWindow, QApplication

from manWin import Ui_MainWindow  # 主界面
from specctrl import SpecCtrl
import threading

# 用于线程之间交流的全局变量
global wave_len, spec_value, int_time, avg_time, measure_mode, reading_status, isMeasuring
isMeasuring = False
global spectrometer
spectrometer = SpecCtrl()


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None, measure_callback=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.measure_callback = measure_callback
        self.setupUi(self)
        # my code here
        self.switch_connect_status(False)
        self.config_lineEdit()

        self.matplotlibWidget_spec.setVisible(False)
        self.matplotlibWidget_mosi.setVisible(False)
        self.matplotlibWidget_don.setVisible(False)

        self.checkBox_continuous.stateChanged.connect(self.measure_mode_changed)

        self.measure_thread = MeasureThread()
        self.measure_thread.start()
        self.measure_thread.trigger.connect(self.measure_finished)

        self.continuous_timer = QTimer(self)
        self.continuous_timer.timeout.connect(self.update_timer)

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
                # self.pushButton_white_ref.setEnabled(True)

    @pyqtSlot()
    def on_pushButton_dark_ref_clicked(self):
        global int_time, avg_time, measure_mode, isMeasuring
        int_time = self.lineEdit_int_time.text()
        avg_time = self.lineEdit_avg_time.text()

        int_time = 500 if int_time == "" else int(int_time)
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

        int_time = 500 if int_time == "" else int(int_time)
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
        if self.checkBox_continuous.isChecked():
            measure_interval = self.lineEdit_param_interval.text()
            measure_interval = 0 if measure_interval == "" else int(measure_interval)
            self.continuous_timer.start(measure_interval * 1000)
        else:
            global int_time, avg_time, measure_mode, isMeasuring
            int_time = self.lineEdit_int_time.text()
            avg_time = self.lineEdit_avg_time.text()
            int_time = 500 if int_time == "" else int(int_time)
            avg_time = 1 if avg_time == "" else int(avg_time)
            measure_mode = 'REFER'
            isMeasuring = True
            self.pushButton_sample.setEnabled(False)
            self.pushButton_white_ref.setEnabled(False)
            self.pushButton_dark_ref.setEnabled(False)

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.matplotlibwidget_dynamic.setVisible(True)
        self.matplotlibwidget_dynamic.mpl.start_dynamic_plot()

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
            self.tableWidget_data.setEnabled(status)

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

        mosi_validator = QDoubleValidator(self)
        don_validator = QDoubleValidator(self)
        mosi_validator.setRange(0, 100)
        don_validator.setRange(0, 1000000)
        self.lineEdit_mosi.setValidator(mosi_validator)
        self.lineEdit_don.setValidator(don_validator)

    def measure_mode_changed(self):
        print('measure mode changed')
        if self.checkBox_continuous.isChecked():
            self.lineEdit_param_interval.setEnabled(True)
        else:
            self.lineEdit_param_interval.setEnabled(False)
            self.continuous_timer.stop()

    def clear_all(self):
        self.matplotlibWidget_spec.mpl.axes.cla()
        self.matplotlibWidget_mosi.mpl.axes.cla()
        self.matplotlibWidget_don.mpl.axes.cla()

    def measure_finished(self):
        if self.checkBox_continuous.isChecked():
            if reading_status:
                measure_interval = self.lineEdit_param_interval.text()
                measure_interval = 0 if measure_interval == "" else int(measure_interval)
                self.matplotlibWidget_spec.setVisible(True)
                self.matplotlibWidget_spec.mpl.draw_spec(wave_len, spec_value)
                print('get wave_length shape: {}, spec shape: {}'.format(wave_len.shape, spec_value.shape))
                self.continuous_timer.start(measure_interval * 1000)
            else:
                print('read failed')
        else:
            if reading_status:
                self.matplotlibWidget_spec.setVisible(True)
                self.matplotlibWidget_spec.mpl.draw_spec(wave_len, spec_value)
                self.pushButton_white_ref.setEnabled(True)
                print('get wave_length shape: {}, spec shape: {}'.format(wave_len.shape, spec_value.shape))
                if measure_mode is "DARK":
                    self.pushButton_dark_ref.setEnabled(True)
                    self.pushButton_white_ref.setEnabled(True)
                else:
                    self.pushButton_sample.setEnabled(True)
                    self.pushButton_white_ref.setEnabled(True)
                    self.pushButton_dark_ref.setEnabled(True)
                    self.checkBox_continuous.setEnabled(True)
            else:
                print('read failed')

    def update_timer(self):
        self.measure_callback
        global isMeasuring
        while isMeasuring:
            pass
        isMeasuring = True
        self.continuous_timer.stop()


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


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
