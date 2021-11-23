from threading import Thread
import subprocess

t1 = Thread(target=subprocess.run, args=(["/home/kathir/miniconda3/envs/gait/bin/python", "script1.py"],))
t2 = Thread(target=subprocess.run, args=(["/home/kathir/miniconda3/envs/gait/bin/python", "script2.py"],))

t1.start()
t2.start()

t1.join()
t2.join()