import re
import serial
import time

from apps.backend.mobileinternet.models import SerialConfig


class Sim800l:
    def __init__(self, serial_config: SerialConfig):
        self.serial_config = serial_config
        self.serial = serial.Serial()
        self.port = serial_config.port
        self.baudrate = serial_config.baudrate
        self.timeout = serial_config.timeout
        self.apn = serial_config.apn
        self.apn_user = serial_config.apn_user
        self.apn_pwd = serial_config.apn_pwd
        self.open()
        self.set_apn()

    def open(self):
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=self.timeout
            )
            return True
        except Exception as e:
            print(e)
            return False

    def is_open(self):
        return self.serial.is_open

    def close(self):
        self.serial.close()

    def ready(self):
        if self.send_command('AT', 0.5)[1] == 'OK':
            return True
        else:
            return False

    def send_command(self, command: str, sleep_time: int = 0):
        if not self.is_open():
            return 'Serial port is not open'
        cmd = '{0}\n'.format(command).encode()
        self.serial.write(cmd)
        time.sleep(sleep_time)
        response = self.serial.readlines()
        for i in range(len(response)):
            response[i] = response[i].decode().strip()
        return response

    def send_command_with_description(self, command: str, description: str,
                                      sleep_time: int = 0, strip_response: bool = True):
        cmd = '{0}\n'.format(command).encode()
        try:
            self.serial.write(cmd)
            time.sleep(sleep_time)
        except Exception as e:
            return 'Write timeout: {0}'.format(e)

        _lines = self.serial.readlines()
        lines = []
        for line in _lines:
            line = line.decode().strip()
            if strip_response and line != command and line != 'OK' and line != '':
                lines.append(line)
            else:
                lines.append(line)

        res = dict(
            command=command,
            result=lines,
            description=description
        )
        return res

    def set_apn(self):
        self.send_command("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\""),
        self.send_command("AT+SAPBR=3,1,\"APN\",\"{}\"".format(self.apn)),
        self.send_command("AT+SAPBR=3,1,\"USER\",\"{}\"".format(self.apn_user)),
        self.send_command("AT+SAPBR=3,1,\"PWD\",\"{}\"".format(self.apn_pwd))
        self.send_command("AT+SAPBR=1,1"),
        self.send_command("AT+SAPBR=1,1")

    def http_post(self, url, data):
        output = [self.send_command_with_description('AT+HTTPINIT', 'HTTP Init'),
                  self.send_command_with_description('AT+HTTPPARA="CID",1', 'Check Connect'),
                  self.send_command_with_description('AT+HTTPPARA="URL","{0}"'.format(url), 'HTTP URL'),
                  self.send_command_with_description('AT+HTTPSSL=1', 'HTTP SSL'),
                  self.send_command_with_description('AT+HTTPPARA="CONTENT","application/json"', 'HTTP Content'),
                  self.send_command_with_description('AT+HTTPDATA={0},10000'.format(len(data)), 'HTTP Data'),
                  self.send_command_with_description('{0}'.format(data), 'HTTP Data'),
                  self.send_command_with_description('AT+HTTPACTION=1', 'HTTP Action', 1),
                  self.send_command_with_description('AT+HTTPREAD', 'HTTP Read')]
        return output


def config_serial():
    config = SerialConfig.query.first()
    if config is None:
        return None
    else:
        try:
            return serial.Serial(
                port=config.port,
                baudrate=config.baudrate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=config.timeout
            )
        except:
            return None


def init_gprs(serial_port):
    output = [send_command(serial_port, "AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\""),
              send_command(serial_port, "AT+SAPBR=3,1,\"APN\",\"m3-world\""),
              send_command(serial_port, "AT+SAPBR=3,1,\"USER\",\"mms\""),
              send_command(serial_port, "AT+SAPBR=3,1,\"PWD\",\"mms\""),
              send_command(serial_port, "AT+SAPBR=1,1"),
              send_command(serial_port, "AT+SAPBR=1,1")]
    return output


def send_command(serial_port, command, description='', sleep=0):
    cmd = '{0}\n'.format(command).encode()
    try:
        serial_port.write(cmd)
        time.sleep(sleep)
    except Exception as e:
        return 'Write timeout{0}'.format(e)

    _lines = serial_port.readlines()
    lines = []
    for line in _lines:
        line = line.decode('utf-8').replace('\r', '').replace('\n', '')
        if line != command and line != 'OK' and line != '':
            lines.append(line)

    res = dict(
        command=command,
        result=lines,
        description=description
    )
    return res


def get_device_info(serial_port):
    output = [send_command(serial_port, 'ATI', 'Product'),
              send_command(serial_port, 'AT+GSV', 'Manufacturer')]
    return output


def get_sim_status(serial_port):
    init_gprs(serial_port)
    sim_status = send_command(serial_port, 'AT+CPIN?', 'SIM Status')
    phone_number = send_command(serial_port, 'AT+CNUM', 'Phone Number')
    ip_address = send_command(serial_port, 'AT+SAPBR=2,1', 'IP Address')

    sim_status['result'] = [sim_status['result'][0].split(':')[1].strip()]
    phone_number['result'] = [re.search(',\"(.*)\"', phone_number['result'][0]).group(1)]
    ip_address['result'] = [re.search('\"(.*)\"', ip_address['result'][0]).group(1)]
    output = [sim_status, phone_number, ip_address]
    return output


def get_ussd(serial_port, ussd_string):
    output = send_command(serial_port, 'AT', 'USSD')
    return output


def make_call(serial_port, number):
    output = [send_command(serial_port, "AT+CPIN?"),
              send_command(serial_port, "AT+CSQ"),
              send_command(serial_port, "AT+COPS?"),
              send_command(serial_port, "AT+CREG?"),
              send_command(serial_port, "ATD{0};".format(number))]
    return output


def stop_call(serial_port):
    output = send_command(serial_port, 'ATH', 'Hang Up Call')
    return output


def get(serial_port, url):
    output = [send_command(serial_port, 'AT+HTTPINIT', 'HTTP Init', 2),
              send_command(serial_port, 'AT+HTTPPARA="URL","{0}"'.format(url), 'HTTP URL', 1),
              send_command(serial_port, 'AT+HTTPPARA="CID",1', 'Check Connect', 1),
              send_command(serial_port, 'AT+HTTPACTION=0', 'HTTP Action', 2),
              send_command(serial_port, 'AT+HTTPREAD', 'HTTP Read', 10)]
    return output


def post(serial_port, url, data):
    output = [send_command(serial_port, 'AT+HTTPINIT', 'HTTP Init', 1),
              send_command(serial_port, 'AT+HTTPPARA="CID",1', 'Check Connect', 1),
              send_command(serial_port, 'AT+HTTPPARA="URL","{0}"'.format(url), 'HTTP URL', 1),
              send_command(serial_port, 'AT+HTTPSSL=1', 'HTTP SSL', 1),
              send_command(serial_port, 'AT+HTTPPARA="CONTENT","application/json"', 'HTTP Content', 1),
              send_command(serial_port, 'AT+HTTPDATA={0},10000'.format(len(data)), 'HTTP Data', 1),
              send_command(serial_port, '{0}'.format(data), 'HTTP Data', 1),
              send_command(serial_port, 'AT+HTTPACTION=1', 'HTTP Action', 2),
              send_command(serial_port, 'AT+HTTPREAD', 'HTTP Read', 10)]
    return output
