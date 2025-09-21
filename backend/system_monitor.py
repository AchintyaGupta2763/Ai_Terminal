import psutil

def get_cpu_usage():
    return f"CPU Usage: {psutil.cpu_percent()}%"

def get_memory_usage():
    mem = psutil.virtual_memory()
    return f"Memory Usage: {mem.percent}% ({mem.used // (1024*1024)} MB / {mem.total // (1024*1024)} MB)"

def get_process_list(limit=20):
    procs = [f"{p.pid}\t{p.name()}" for p in psutil.process_iter(['name'])]
    return "\n".join(procs[:limit])
