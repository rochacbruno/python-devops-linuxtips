import psutil


def check_cpu_usage():
    return psutil.cpu_percent(interval=1)


def check_memory_usage():
    return psutil.virtual_memory().percent


def check_disk_usage():
    return psutil.disk_usage("/").percent
