import glob
import subprocess
import re

def get_esp_devices():
    try:
        output = subprocess.check_output(["timeout", "2", "avahi-browse", "-ptr", "_arduino._tcp"]).decode('utf-8')
    except subprocess.CalledProcessError:
        return []

    devices = []  
    pattern = re.compile(r'=;[^;]+;IPv4;([^;]+);_arduino\._tcp;local;([^;]+);([\d\.]+);(\d+);(.*)')
    
    for match in pattern.findall(output):
        device_info = {
            "hostname": match[1],
            "ip": match[2],
            "port": match[3],
        }

        # Tách các thông số như tcp_check, ssh_upload, board, auth_upload
        attributes = match[4].split('" "')
        for attr in attributes:
            key_value = attr.replace('"', '').split('=')
            if len(key_value) == 2:
                device_info[key_value[0]] = key_value[1]

        devices.append(device_info)

    return devices

def get_usb_serial_info():
    devices = glob.glob("/dev/ttyUSB*")  # Tìm tất cả các cổng ttyUSB*
    devices += glob.glob("/dev/ttyACM*")  # Tìm tất cả các cổng ttyAMA*
    usb_info = []

    for dev in devices:
        try:
            output = subprocess.check_output(["udevadm", "info", "--query=all", "--name=" + dev]).decode('utf-8')
            info = {
                "device": dev,
                "vendor": None,
                "product": None,
                "serial": None,
                "vendor_db": None,
                "model_db": None
            }

            for line in output.split("\n"):
                if "E: ID_VENDOR=" in line:
                    info["vendor"] = line.split("=")[1]
                elif "E: ID_MODEL=" in line:
                    info["product"] = line.split("=")[1]
                elif "E: ID_SERIAL=" in line:
                    info["serial"] = line.split("=")[1]
                elif "E: ID_VENDOR_FROM_DATABASE=" in line:
                    info["vendor_db"] = line.split("=")[1]
                elif "E: ID_MODEL_FROM_DATABASE=" in line:
                    info["model_db"] = line.split("=")[1]

            usb_info.append(info)

        except subprocess.CalledProcessError:
            continue

    return usb_info

def get_board_fqbn(board_name):
    try:
        cmd = "/home/baonv/bin/arduino-cli board listall | grep " + board_name
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
    except subprocess.CalledProcessError:
        return None

    result = []
    for line in output.split("\n"):
        parts = list(filter(None, line.split("  ")))
        if len(parts) >= 2:
            result.append((parts[0], parts[1]))
    return result

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'bin', 'hex', 'elf', 'ino'}