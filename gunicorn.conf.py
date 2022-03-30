import multiprocessing
import os

bind = "0.0.0.0:8080"
chdir = os.path.dirname(os.path.abspath(__file__))
log_file = "-"
preload_app = True
worker_class = "aiohttp.worker.GunicornWebWorker"
worker_tmp_dir = "/dev/shm"
workers = multiprocessing.cpu_count() * 2 + 1
