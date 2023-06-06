import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np
from backend.LTSpiceReader import ReadLTSpice

# FILE INDEX TO OPEN
idx = 1

data = ReadLTSpice(folder="data", idx=idx)
data.info()

l = data.getSpice()

case_count = l.case_count


varListNames = l.variables
varListData = []

montecarlo = False
for varName in varListNames:
    if case_count > 1:
        montecarlo = True
        run = []
        for i in range(case_count):
            run.append(l.get_data(varName, case=i))
        varListData.append(run)
    else:
        varListData.append(l.get_data(varName))

time = varListData[0]



for i in [5,6,7,8,9,10]:

    print(f"Plotting {varListNames[i]}")

    if montecarlo:
        for t, run in zip(time, varListData[i]):
            plt.plot(t, run, linewidth=0.5)
    # plt.plot(time, varListData[i], c='black', linewidth=0.5)
    # plt.scatter(time[0:300], varListData[i][0:300], s=0.1, c='black')
    else:
        plt.plot(time, varListData[i], linewidth=0.5)
        # plt.scatter(time[0:300], varListData[i][0:300], s=0.1, c='black')

plt.ylabel("Current (A)")
plt.xlabel('Time (s)')
plt.show()