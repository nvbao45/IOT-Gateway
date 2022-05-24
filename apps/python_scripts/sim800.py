import re
import serial
import time


class SerialConfigParam:
    def __init__(self, port, baudrate, timeout, apn, apn_user, apn_pwd):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.apn = apn
        self.apn_user = apn_user
        self.apn_pwd = apn_pwd


class Sim800l:
    def __init__(self, serial_config: SerialConfigParam):
        self.serial_config = serial_config
        self.serial = serial.Serial()
        self.port = serial_config.port
        self.baudrate = serial_config.baudrate
        self.timeout = serial_config.timeout
        self.apn = serial_config.apn
        self.apn_user = serial_config.apn_user
        self.apn_pwd = serial_config.apn_pwd
        self.sim_status = None
        self.phone_number = None
        self.ip_address = None
        self.product_name = None
        self.manufacturer = None
        self.open()
        self.set_apn()

    def config(self, port, baudrate, timeout, apn, apn_user, apn_pwd):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.apn = apn
        self.apn_user = apn_user
        self.apn_pwd = apn_pwd

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
        if self.send_command('AT', 0.5)[0] == 'AT':
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
            if strip_response:
                if line != command and line != 'OK' and line != '':
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
        self.set_apn()
        output = [self.send_command_with_description('AT+HTTPINIT', 'HTTP Init'),
                  self.send_command_with_description('AT+HTTPPARA="CID",1', 'Check Connect'),
                  self.send_command_with_description('AT+HTTPPARA="URL","{0}"'.format(url), 'HTTP URL'),
                  self.send_command_with_description('AT+HTTPSSL=1', 'HTTP SSL'),
                  self.send_command_with_description('AT+HTTPPARA="CONTENT","application/json"', 'HTTP Content'),
                  self.send_command_with_description('AT+HTTPDATA={0},10000'.format(len(data)), 'HTTP Data'),
                  self.send_command_with_description('{0}'.format(data), 'HTTP Data'),
                  self.send_command_with_description('AT+HTTPACTION=1', 'HTTP Action', 1),
                  self.send_command_with_description('AT+HTTPREAD', 'HTTP Read'),
                  self.send_command_with_description('AT+HTTPTERM', 'HTTP Term')]
        return output

    def http_get(self, url):
        output = [self.send_command_with_description('AT+HTTPINIT', 'HTTP Init', 1),
                  self.send_command_with_description('AT+HTTPPARA="URL","{0}"'.format(url), 'HTTP URL', 1),
                  self.send_command_with_description('AT+HTTPPARA="CID",1', 'Check Connect', 1),
                  self.send_command_with_description('AT+HTTPACTION=0', 'HTTP Action', 2),
                  self.send_command_with_description('AT+HTTPREAD', 'HTTP Read', 5)]
        return output

    def call(self, number):
        self.send_command("AT+CPIN?")
        self.send_command("AT+CSQ")
        self.send_command("AT+COPS?")
        self.send_command("AT+CREG?")
        self.send_command("ATD{0};".format(number))
        return "Calling {0}".format(number)

    def hangup(self):
        self.send_command('ATH')
        return 'Hanging up'

    def get_device_info(self):
        self.product_name = self.send_command_with_description('ATI', 'Product', 1)
        self.manufacturer = self.send_command_with_description('AT+GMI', 'Manufacturer', 1)

    def get_sim_status(self):
        sim_status = self.send_command_with_description('AT+CPIN?', 'SIM Status', 1)
        phone_number = self.send_command_with_description('AT+CNUM', 'Phone Number', 1)
        ip_address = self.send_command_with_description('AT+SAPBR=2,1', 'IP Address', 1)

        sim_status['result'] = [sim_status['result'][0].split(':')[1].strip()]
        phone_number['result'] = [re.search(',\"(.*)\"', phone_number['result'][0]).group(1)]
        ip_address['result'] = [re.search('\"(.*)\"', ip_address['result'][0]).group(1)]
        self.sim_status = sim_status
        self.ip_address = ip_address
        self.phone_number = phone_number
