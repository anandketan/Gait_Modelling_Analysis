import numpy as np
import pyrealsense2 as rs
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.accel, rs.format.motion_xyz32f, 250)
config.enable_stream(rs.stream.gyro, rs.format.motion_xyz32f, 200)

def gyro_data(gyro):
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