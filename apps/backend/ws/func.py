import psutil
import shutil
import platform


def get_system_info():
    cpu = psutil.cpu_percent()
    ram_used = psutil.virtual_memory().percent
    ram_total = psutil.virtual_memory().total
    ram_available = psutil.virtual_memory().available
    total, used, free = shutil.disk_usage("/")
    cpu_temp = None

    if platform.system() == "Linux":
        sensors_temp = psutil.sensors_temperatures()
        if sensors_temp:
            if "cpu_thermal" in sensors_temp:
                cpu_temp = sensors_temp['cpu_thermal'][0][1]
            else:
                cpu_temp = "N/A"
        else:
            cpu_temp = "N/A"
    else:
        cpu_temp = "N/A"

    info = dict(
        cpu=cpu,
        cpu_temp=cpu_temp,
        ram_used=ram_used,
        ram_free=ram_available // (2**20),
        ram_total=ram_total // (2**20),
        disk_total=total // (2**30),
        disk_free=free // (2**30),
        disk_used=used // (2**30)
    )
    return info
