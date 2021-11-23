import numpy as np
import pyrealsense2 as rs
import time
import pandas as pd

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

global df
df_gyro = pd.DataFrame(columns = ['x','y','z'])
df_gyro = df_gyro.append({'x' : 0 ,'y' : 0, 'z':0}, ignore_index=True)
print(df_gyro)

def gyro_data(gyro):
    global df_gyro
    df_gyro = df_gyro.append({'x' : gyro.x,'y' : gyro.y, 'z' : gyro.z}, ignore_index=True)
    return np.asarray([gyro.x, gyro.y, gyro.z])

profile = pipeline.start(config)

try:
    while True:
        frame = pipeline.wait_for_frames()
        gyroscope = gyro_data(frame[0].as_motion_frame().get_motion_data())
        print(gyroscope)
        time.sleep(0.25)
finally:
    pipeline.stop()
    df_gyro.to_csv ('/home/kathir/Desktop/Biomechanics_Gait_Analysis/csv_data/4hz_gyro_dontuset.csv', index = False, header=True)

