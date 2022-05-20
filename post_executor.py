import matplotlib.pyplot as plt
import numpy as np
import socket
import time
import math
import datetime
from datetime import datetime
import os
import keyboard
# import pressure_sensor_gait_cycle as gait
import utils_sensor_data as utils

joint = "Lower_body"
date = "2022-04-13"
trials = ["Fauzan_1_gait_cycle", "Fauzan_2_gait_cycle", "Raafay_1_gait_cycle", "Raafay_2_gait_cycle", "Raafay_3_gait_cycle", "Raafay_4_gait_cycle"]

for trial in trials:
    utils.gait_cycle_mean_tester(joint, date, trial)
