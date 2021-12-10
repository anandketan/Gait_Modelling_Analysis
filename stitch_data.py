import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.DataFrame()

for folder in os.listdir("DataFolder\\right_knee\\2021-11-23"):
    for file in os.listdir(os.path.join("DataFolder\\right_knee\\2021-11-23",folder)):
        if "allSensorData" in file:
            print(file)
            dataset = pd.read_csv("DataFolder\\right_knee\\2021-11-23\\"+folder+"\\"+file,
                               usecols=["AccX_C", "AccY_C", "AccZ_C", "GyroX_C", "GyroY_C", "GyroZ_C", "_CRollQ", "AccX_D",
                                        "AccY_D", "AccZ_D", "GyroX_D", "GyroY_D", "GyroZ_D", "_DRollQ", "_EStep"])
            print(dataset)
            df = df.append(dataset)
            print(df)

df.to_csv("Stitched_data_Nikhil_2021-11-23.csv")