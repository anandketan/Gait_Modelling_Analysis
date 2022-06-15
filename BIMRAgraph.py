from mpl_toolkits import mplot3d
from collections import deque
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# fig = plt.figure()

df = pd.read_csv('raafay_trail4_IMU.csv')
Gait_Cycle2 = df['pct_gait_cycle']

IMU_LeftKneeFlexExt = df['LKFE']
IMU_RightKneeFlexExt = df['RKFE']
IMU_LeftKneeAbdAdd = df['LKAA']
IMU_RightKneeAbdAdd = df['RKAA']
IMU_LeftKneeRot = df['LKIE']
IMU_RightKneeRot = df['RKIE']

IMU_LeftAnkleFlexExt = df['LAFE']
IMU_RightAnkleFlexExt = df['RAFE']
IMU_LeftAnkleAbdAdd = df['LFAA']
IMU_RightAnkleAbdAdd = df['RFAA']
IMU_LeftAnkleRot = df['LFIE']
IMU_RightAnkleRot = df['RFIE']
# LeftFootProg = df['LAIE']
# RightFootProg = df['RAIE']

df = pd.read_csv('raafay_trail4.csv')
Gait_Cycle1 = df[' Sample']
LeftKneeFlexExt = df[' acmLKFE.M']
RightKneeFlexExt = df[' acmRKFE.M']
LeftKneeAbdAdd = df[' acmLKAA.M']
RightKneeAbdAdd = df[' acmRKAA.M']
LeftKneeRot = df[' acmLKIE.M']
RightKneeRot = df[' acmRKIE.M']

LeftAnkleFlexExt = df[' acmLAFE.M']
RightAnkleFlexExt = df[' acmRAFE.M']
LeftAnkleInversion = df[' acmLFAA.M']
RightAnkleInversion = df[' acmRFAA.M']
LeftAnkleRot = df[' acmLFIE.M']
RightAnkleRot = df[' acmRFIE.M']
LeftFootProg = df[' acmLAIE.M']
RightFootProg = df[' acmRAIE.M']


test_list = deque(IMU_LeftKneeFlexExt)
test_list.rotate(500)
test_list = list(test_list)
# leftkneeshift = LeftKneeFlexExt.max() - max(test_list)
# test_list = test_list + leftkneeshift
# rightkneeshift = RightKneeFlexExt.max() - IMU_RightKneeFlexExt.max()
# IMU_RightKneeFlexExt = IMU_RightKneeFlexExt + rightkneeshift
# print(leftkneeshift, rightkneeshift)
plt.plot(Gait_Cycle1, LeftKneeFlexExt, color='lightgreen', label='Left Knee', linewidth=6)
plt.plot(Gait_Cycle2, test_list, color='green', label='IMU_Left Knee', linewidth=2)
plt.plot(Gait_Cycle1, RightKneeFlexExt, color='lightsalmon', label='Right Knee', linewidth=6)
plt.plot(Gait_Cycle2, IMU_RightKneeFlexExt, color='red', label='IMU_Right Knee', linewidth=2)
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Knee Flexion/Extension")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()


test_list = deque(IMU_LeftKneeAbdAdd)
test_list.rotate(500)
test_list = list(test_list)
test_list2 = deque(IMU_RightKneeAbdAdd)
# test_list2.rotate(110)
test_list2 = list(test_list2)
# leftkneeshift = LeftKneeAbdAdd.max() - max(test_list)
# test_list = test_list + leftkneeshift
# rightkneeshift = RightKneeAbdAdd.max() - IMU_RightKneeRot.max()
# IMU_RightKneeRot = IMU_RightKneeRot + rightkneeshift
# print(leftkneeshift, rightkneeshift)
plt.plot(Gait_Cycle1, LeftKneeAbdAdd, color='lightgreen', label='Left Knee', linewidth=6)
plt.plot(Gait_Cycle2, test_list, color='green', label='IMU_Left Knee', linewidth=2)
plt.plot(Gait_Cycle1, RightKneeAbdAdd, color='lightsalmon', label='Right Knee', linewidth=6)
plt.plot(Gait_Cycle2, test_list2, color='red', label='IMU_Right Knee', linewidth=2)
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Knee Abduction/Adduction")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()


test_list = deque(IMU_LeftKneeRot)
test_list.rotate(500)
test_list = list(test_list)
# leftkneeshift = LeftKneeRot.max() - max(test_list)
# test_list = test_list + leftkneeshift
# rightkneeshift = RightKneeRot.min() - IMU_RightKneeRot.min()
# IMU_RightKneeRot = IMU_RightKneeRot + rightkneeshift
# print(leftkneeshift, rightkneeshift)
plt.plot(Gait_Cycle1, LeftKneeRot, color='lightgreen', label='Left Knee', linewidth=6)
plt.plot(Gait_Cycle2, test_list, color='green', label='IMU_Left Knee', linewidth=2)
plt.plot(Gait_Cycle1, RightKneeRot, color='lightsalmon', label='Right Knee', linewidth=6)
plt.plot(Gait_Cycle2, IMU_RightKneeRot, color='red', label='IMU_Right Knee', linewidth=2)
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Knee Rotation")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()

test_list = deque(IMU_LeftAnkleFlexExt)
test_list.rotate(500)
test_list = list(test_list)
# leftkneeshift = LeftAnkleFlexExt.max() - max(test_list)
# test_list = test_list + leftkneeshift
# rightkneeshift = RightAnkleFlexExt.max() - IMU_RightAnkleFlexExt.max()
# IMU_RightAnkleFlexExt = IMU_RightAnkleFlexExt + rightkneeshift
# print(leftkneeshift, rightkneeshift)
plt.plot(Gait_Cycle1, LeftAnkleFlexExt, color='lightgreen', label='Left Ankle', linewidth=6)
plt.plot(Gait_Cycle2, test_list, color='green', label='IMU_Left Ankle', linewidth=2)
plt.plot(Gait_Cycle1, RightAnkleFlexExt, color='lightsalmon', label='Right Ankle', linewidth=6)
plt.plot(Gait_Cycle2, IMU_RightAnkleFlexExt, color='red', label='IMU_Right Ankle', linewidth=2)
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Ankle DorsiFlexion/PlantarFlexion")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()


test_list = deque(IMU_LeftAnkleAbdAdd)
test_list.rotate(500)
test_list = list(test_list)
# leftkneeshift = LeftFootProg.max() - max(test_list)
# test_list = test_list + leftkneeshift + 11
# rightkneeshift = RightFootProg.max() - IMU_RightAnkleAbdAdd.max()
# IMU_RightAnkleAbdAdd = IMU_RightAnkleAbdAdd + rightkneeshift
# print(leftkneeshift, rightkneeshift)
plt.plot(Gait_Cycle1, LeftFootProg, color='lightgreen', label='Left Ankle', linewidth=6)
plt.plot(Gait_Cycle2, test_list, color='green', label='IMU_Left Ankle', linewidth=2)
plt.plot(Gait_Cycle1, RightFootProg, color='lightsalmon', label='Right Ankle', linewidth=6)
plt.plot(Gait_Cycle2, IMU_RightAnkleAbdAdd, color='red', label='IMU_Right Ankle', linewidth=2)
plt.xlabel("% Gait Cycle")
plt.ylabel("Degrees")
plt.title("Ankle Abduction/Adduction / Foot Progression")
plt.axhline(y=0, color='k')
plt.legend()
plt.show()