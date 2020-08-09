from tkinter import messagebox, Tk, Label, Entry, Button, StringVar, Menu, Listbox
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from specctrl import SpecCtrl
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import serial.tools.list_ports as sp


class WinConfig:
    connect_button = [8, 1, 70, 288, '连接/断开']
    lamp_button = [8, 1, 70, 348, '开灯/关灯']
    white_button, dark_button, sample_button = [8, 1, 150, 288, '白色参考'], [8, 1, 150, 348, '无光参考'], \
                                               [20, 1, 110, 408, '采集样本']
    model_select_button, model_save_button, model_train = [8, 1, 260, 288, '模型加载'], [8, 1, 260, 408, '模型保存'],\
                                                          [8, 1, 260, 348, '模型训练']
    data_save, pic_save, data_load = [8, 1, 370, 288, '数据保存'], [8, 1, 370, 408, '绘图保存'], \
                                     [8, 1, 370, 348, '数据加载']
    add_y, predict_button = [16, 1, 500, 205, '添加标签'], [16, 1, 500, 380, '开始预测']

    menu_text = {'control': '控制',
                 'connect/disconnect': '连接/断开',
                 'turn on/off lamp': '开灯/关灯',

                 'collect': '采集',
                 'white': '白色参考',
                 'dark': '无光参考',
                 'sample': '采集样本',

                 'model': '模型',
                 'model_load': '模型加载',
                 'model_save': '模型保存',
                 'model_train': '模型训练',

                 'data': '数据',
                 'data_save': '数据保存',
                 'plot_save': '绘图保存',
                 'data_load': '数据加载'
    }

    entry_place = {'label_entry': []}


class SpecWindow:
    def __init__(self):
        self.config = WinConfig()
        self.window = Tk()
        self.window.title('面粉品质在线监测系统 V1.1')
        self.window.geometry('620x458')
        self.status_var, self.output_var = StringVar(), StringVar()
        self.status_var.set('未连接')
        self.output_var.set('No Result')
        self.output_label = Label(self.window, textvariable=self.output_var)
        self.output_label.place(x=500, y=408)
        label_text = Label(self.window, text="预测结果:")
        label_text.place(x=420, y=408)
        self.status = False
        self.status_label = Label(self.window, textvariable=self.status_var, bg="red", width=618, height=1)
        self.status_label.pack()

        self.port_select_combobox = Combobox(self.window, width=6)
        label_text = Label(self.window, text="端口:")
        label_text.place(x=500, y=28)

        self.spec = SpecCtrl(dev_path='/dev/ttyUSB0', baud_rate=115200, timeout=5)

        self.connect_button = None
        self.lamp_button = None
        self.white_button, self.dark_button, self.sample_button = None, None, None
        self.model_selection, self.model_save, self.model_train = None, None, None
        self.data_save, self.pic_save, self.data_load, self.add_y = None, None, None, None
        self.predict_button = None

        self.label_entry, self.int_time_entry, self.avg_time_entry = None, None, None

        self.data_list_box = Listbox(self.window, width=25, height=4)
        self.data_list_box.place(x=420, y=60)
        label_text = Label(self.window, text="数据:")
        label_text.place(x=432, y=40, anchor='center')

        self.fig_area, self.canvas_area = None, None

        self.config_button()
        self.config_menu()
        self.config_entry()
        self.config_canvas()
        self.port_list = self.config_combobox()

    def run(self):
        self.window.mainloop()

    def config_button(self):
        w, h, x, y, txt = self.config.connect_button
        self.connect_button = Button(self.window, text=txt, width=w, height=h, command=self.disconnect_connect)
        self.connect_button.place(x=x, y=y, anchor="center")

        w, h, x, y, txt = self.config.lamp_button
        self.lamp_button = Button(self.window, text=txt, width=w, height=h, command=self.lamp_on_off)
        self.lamp_button.place(x=x, y=y, anchor="center")

        w, h, x, y, txt = self.config.white_button
        self.white_button = Button(self.window, text=txt, width=w, height=h, command=self.measure_white)
        self.white_button.place(x=x, y=y, anchor="center")
        w, h, x, y, txt = self.config.sample_button
        self.sample_button = Button(self.window, text=txt,  width=w, height=h, command=self.spec.connect)
        self.sample_button.place(x=x, y=y, anchor='center')
        w, h, x, y, txt = self.config.dark_button
        self.dark_button = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.dark_button.place(x=x, y=y, anchor="center")

        w, h, x, y, txt = self.config.model_select_button
        self.model_selection = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.model_selection.place(x=x, y=y, anchor="center")
        w, h, x, y, txt = self.config.model_save_button
        self.model_save = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.model_save.place(x=x, y=y, anchor="center")
        w, h, x, y, txt = self.config.model_train
        self.model_train = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.model_train.place(x=x, y=y, anchor="center")

        w, h, x, y, txt = self.config.data_save
        self.data_save = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.data_save.place(x=x, y=y, anchor="center")
        w, h, x, y, txt = self.config.pic_save
        self.data_save = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.data_save.place(x=x, y=y, anchor="center")
        w, h, x, y, txt = self.config.data_load
        self.data_load = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.data_load.place(x=x, y=y, anchor='center')

        w, h, x, y, txt = self.config.add_y
        self.add_y = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.add_y.place(x=x, y=y, anchor='center')

        w, h, x, y, txt = self.config.predict_button
        self.predict_button = Button(self.window, text=txt, width=w, height=h, command=self.spec.connect)
        self.predict_button.place(x=x, y=y, anchor='center')

    def config_menu(self):
        menu_bar = Menu(self.window)

        control_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.config.menu_text['control'], menu=control_menu)
        control_menu.add_command(label=self.config.menu_text['connect/disconnect'],
                                 command=self.disconnect_connect)
        control_menu.add_command(label=self.config.menu_text['turn on/off lamp'], command=self.lamp_on_off)

        collect_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.config.menu_text['collect'], menu=collect_menu)
        collect_menu.add_command(label=self.config.menu_text['white'], command=self.measure_white)
        collect_menu.add_command(label=self.config.menu_text['dark'], command=self.spec.connect)
        collect_menu.add_separator()
        collect_menu.add_command(label=self.config.menu_text['sample'], command=self.spec.connect)

        model_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.config.menu_text['model'], menu=model_menu)
        model_menu.add_command(label=self.config.menu_text['model_load'], command=self.spec.connect)
        model_menu.add_command(label=self.config.menu_text['model_save'], command=self.spec.connect)
        model_menu.add_command(label=self.config.menu_text['model_train'], command=self.spec.connect)

        data_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label=self.config.menu_text['data'], menu=data_menu)
        data_menu.add_command(label=self.config.menu_text['data_save'], command=self.spec.connect)
        data_menu.add_command(label=self.config.menu_text['data_load'], command=self.spec.connect)
        data_menu.add_separator()
        data_menu.add_command(label=self.config.menu_text['plot_save'], command=self.spec.connect)

        self.window.config(menu=menu_bar)

    def config_entry(self):
        self.label_entry = Entry(self.window, width=20)
        self.label_entry.place(x=500, y=175, anchor='center')
        label_text = Label(self.window, text="输入训练标签，以 , 分割:")
        label_text.place(x=495, y=150, anchor='center')

        int_time = StringVar(value='500')
        self.int_time_entry = Entry(self.window, width=10, textvariable=int_time)
        self.int_time_entry.place(x=550, y=340, anchor='center')
        label_text = Label(self.window, text='积分时间:')
        label_text.place(x=450, y=340, anchor='center')

        avg_time = StringVar(value='2')
        self.avg_time_entry = Entry(self.window, width=10, textvariable=avg_time)
        self.avg_time_entry.place(x=550, y=280, anchor='center')

        label_text = Label(self.window, text='平均扫描次数:')
        label_text.place(x=460, y=280, anchor='center')

    def config_canvas(self):
        f = Figure(figsize=(4, 2.3), dpi=100)
        self.fig_area = f.add_subplot(1, 1, 1)
        x = np.arange(0, 3, 0.01)
        y = np.sin(2*np.pi*x)

        line, = self.fig_area.plot(x, y)
        self.fig_area.set_xlabel('wave_length')
        self.fig_area.set_ylabel('value')

        self.canvas_area = FigureCanvasTkAgg(f, self.window)
        self.canvas_area.draw()
        self.canvas_area.get_tk_widget().place(x=10, y=35)

        # toolbar = NavigationToolbar2Tk(self.canvas_area, self.window)
        # toolbar.update()
        # self.canvas_area._tkcanvas.place(x=10, y=5)

    def config_combobox(self):
        port_list = list(sp.comports())
        if len(port_list) <= 0:
            print('No port Found')
        else:
            port_list = tuple([port_object[0] for port_object in port_list])
            self.port_select_combobox['values'] = port_list
            self.port_select_combobox.current(0)
            self.port_select_combobox.place(x=535, y=28)
        return port_list

    def disconnect_connect(self):
        if self.spec.status is True:
            self.spec.disconnect()
            self.status_var.set('未连接')
            self.status_label.config(bg='red')
        elif self.spec.status is False:
            port = self.port_select_combobox.get()
            self.spec.connect(port)
            if self.spec.status is True:
                self.status_var.set('已连接')
                self.status_label.config(bg='green')

    def lamp_on_off(self):
        print('没灯！')

    def measure_white(self):
        if self.spec.status is True:
            try:
                inter_time, avg_scan = int(self.int_time_entry.get()), int(self.avg_time_entry.get())
            except:
                print('给出数据不是整数')
                messagebox.showerror(title='数据类型错误', message='给出的积分时间或平均扫描次数不对')
                return 1
            self.spec.measure(mode='LIGHT', inter_time=inter_time, avg_scan=avg_scan)
        else:
            messagebox.showerror(title='未连接', message='还没有连接光谱仪')


if __name__ == '__main__':
    window = SpecWindow()
    window.run()

