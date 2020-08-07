import serial
import time
import numpy as np

class SpecCtrl:
    def __init__(self, dev_path='COM5', baud_rate=115200, timeout=0.5):
        assert baud_rate in [115200, 38400, 921600]
        self.status = False
        self.dev_path, self.baud_rate, self.timeout = dev_path, baud_rate, timeout
        # self.connect()
        self.dark, self.reference = None, None

    def connect(self, dev_path=None):
        if dev_path is None:
            dev_path = self.dev_path
        if self.status is True:
            print('Already Connected!')
            return True
        try:
            self.ser = serial.Serial(dev_path, self.baud_rate, timeout=self.timeout)
        except:
            print('Connect Failed!')
            self.status = False
        else:
            self.status = True
            # print('Connect Successful!')
        try:
            result = self.command(output_mode='BIN')
            if result == b"BIM\r":
                self.status = True
                print('Connect Successful!')
                return True
            else:
                print('Response not Correct, already disconnect!')
                self.status = False
                return False
        except:
            self.status = False
            print('打不出来东西')
            return False

    def command(self, cmd=b'IDN?', interact=False, reset=False, output_mode='STR', wait_time=None):
        assert output_mode in ['BIN', 'STR']
        if self.status is False:
            print('Device not Connected!')
            return 1
        if reset:
            result = input('Are you sure you want to reset the Device? Input <Y> to Confirm.')
            if result != 'Y':
                print('Cancel RESET!')
                return 0
            cmd = b'RST\r'
            self.ser.write(cmd)
            print('Reset Successful!')
            return 0
        if interact:
            while True:
                cmd = input('Please input command (end with <Enter>, press<Q> to quit): \n')
                if cmd == 'q' or cmd == 'Q':
                    return 0
                elif cmd in ['BIN', 'STR']:
                    output_mode = cmd
                elif cmd in ['wait', 'WAIT', 'Wait']:
                    try:
                        wait_time = float(input('Please input How Long I should wait.'))
                    except:
                        print('智障！')
                        continue
                else:
                    cmd = b'*' + cmd.encode(encoding="ascii") + b'\r'
                    self.ser.write(cmd)
                    if wait_time is not None:
                        time.sleep(wait_time)
                    if output_mode == 'BIN':
                        res = self.ser.read(10000)
                        print(type(res))
                        print(res)
                    elif output_mode == 'STR':
                        print(self.ser.read(10000).decode('ascii'))
        else:
            cmd = b'*' + cmd + b'\r'
            try:
                self.ser.write(cmd)
                if wait_time is not None:
                    time.sleep(wait_time)
            except:
                print('Command Write Failed!')
            if output_mode == "BIN":
                return self.ser.read(10000)
            elif output_mode == 'STR':
                return self.ser.read(10000).decode('ascii')

    def disconnect(self):
        self.ser.close()
        self.status = False
        print('Disconnect!')

    def measure(self, mode='DARK', inter_time=500, avg_scan=2, transmission_wait=0.1):
        """
        Get the Spectra.

        :param transmission_wait:
        :param mode:
        :param inter_time:
        :param avg_scan:
        :return: (wave_len, spec)
        """
        if self.status is not True:
            return None
        assert mode in ['DARK', 'LIGHT', 'REFER']
        result = None
        if mode == 'DARK':
            wait = inter_time * avg_scan / 1000 + 0.05 + transmission_wait
            result = self.command(b'meas:dark ' + str(inter_time).encode('ascii') + b' ' + str(avg_scan).encode('ascii')
                                  + b' 7', output_mode='BIN', wait_time=wait)
            result = result[2:-2].decode('ascii')
            result = result.split('\r')
            wave_len = np.array([r.split('\t')[0] for r in result], dtype=float)
            spec = np.array([r.split('\t')[1] for r in result], dtype=float)
            self.dark = spec
            result = (wave_len, spec)
        if mode == 'LIGHT':
            wait = inter_time * avg_scan / 1000 + 0.05 + transmission_wait
            result = self.command(b'meas:light ' + str(inter_time).encode('ascii') + b' ' + str(avg_scan).encode('ascii')
                                  + b' 7', output_mode='BIN', wait_time=wait)
            result = result[2:-2].decode('ascii')
            result = result.split('\r')
            wave_len = np.array([r.split('\t')[0] for r in result], dtype=float)
            spec = np.array([r.split('\t')[1] for r in result], dtype=float)
            self.reference = spec
            result = (wave_len, spec)
        if mode == 'REFER':
            wait = inter_time * avg_scan / 1000 + 0.05 + transmission_wait
            result = self.command(
                b'meas:refer ' + str(inter_time).encode('ascii') + b' ' + str(avg_scan).encode('ascii')
                + b' 7', output_mode='BIN', wait_time=wait)
            result = result[2:-2].decode('ascii')

            result = result.split('\r')
            wave_len = np.array([r.split('\t')[0] for r in result], dtype=float)
            spec = np.array([r.split('\t')[1] for r in result], dtype=float)
            # spec = (spec - self.dark) / self.reference - self.dark
            result = (wave_len, spec)
        return result

    def get_spec(self, inter_time=500, avg_scan=2, first=False):
        if self.status is not True:
            return None
        if first:
            _ = input('Start measure DARK, Please turn off the light!')
            wave_len, spec = self.measure(mode='DARK', inter_time=inter_time, avg_scan=avg_scan)
            plt.plot(wave_len, spec)
            _ = input('Start measure REFER, Please turn on the light!')
            wave_len, spec = self.measure(mode='LIGHT', inter_time=inter_time, avg_scan=avg_scan)
            plt.plot(wave_len, spec)
        _ = input('Start measure SAMPLE, Please put on the sample!')
        wave_len, spec = self.measure(mode='REFER', inter_time=inter_time, avg_scan=avg_scan)
        plt.plot(wave_len, spec)
        plt.show()
        return wave_len, spec


if __name__ == '__main__':
    import matplotlib.pylab as plt
    import models
    sensor = SpecCtrl(dev_path='COM5', baud_rate=115200)
    sensor.connect()
    # result = sensor.command(b'PARAmeter?')

    # print(result)
    # result = sensor.command(b'IDN?')
    # print(result)
    # sensor.command(interact=True)

    # print(result)
    # result = result.split(' ')
    # result = [int(a) for a in result[1:-2] if a !='']
    # print(result)

    # wave_len, spec = sensor.get_spec(first=True, inter_time=50, avg_scan=3)
    # sg_spec = models.savgol(spec, 5, 2)
    # plt.plot(wave_len, spec, label='before sg')
    # plt.plot(wave_len, sg_spec, label='after sg')
    #
    # plt.legend()
    # plt.show()
    # sensor.command(interact=True)
    sensor.get_spec(inter_time=5, avg_scan=1, first=True)
    sensor.disconnect()

