from .core import check_cpu_usage, check_disk_usage, check_memory_usage


def main():
    cpu = check_cpu_usage()
    memory = check_memory_usage()
    disk = check_disk_usage()
    print(f"CPU: {cpu}% MEM: {memory}% DISK: {disk}%")


if __name__ == "__main__":
    main()
