import numpy as np
import csv

def getGainPhase(data):
    print("data shape:", data.shape)
    gain = 20*np.log10(np.abs(data))
    phase = fixPhaseJumps(np.angle(data, deg=True))
    return gain, phase

def fixPhaseJumps(phase):
    # Find the jumps in the zin_p plot
    jumps = np.where(np.abs(np.diff(phase)) > 180)[0] + 1

    # Add or subtract multiples of 360 to each point in the phase plot
    for i in range(len(jumps)):
        if phase[jumps[i]] > phase[jumps[i]-1]:
            phase[jumps[i]:] -= 360
        else:
            phase[jumps[i]:] += 360
    return phase

def constrainTime(start = None, end = None, data=[]):
    # get indexes of the points with the closest value to 56kHz
    idx0 = 0
    idx1 = len(data[0]) - 1
    if start is not None:
        idx0 = np.abs(data[0] - start).argmin()
    if end is not None:
        idx1 = np.abs(data[0] - end).argmin()
    new_data = []
    for arr in data:
        new_data.append(arr[idx0:idx1])
    return new_data

def constrainFrec(start = None, end = None, data=[]):
    # get indexes of the points with the closest value to 56kHz
    idx0 = 0
    idx1 = len(data[0]) - 1
    if start is not None:
        idx0 = np.abs(data[0] - start).argmin()
    if end is not None:
        idx1 = np.abs(data[0] - end).argmin()
    new_data = []
    for arr in data:
        new_data.append(arr[idx0:idx1])
    return new_data

def constrainData(start = 0, end = 1.0, data=[]):
    # constrain data points to percentage of the total
    size = len(data[0])
    start = int(size * 0.65)
    end = int(size * 0.85)
    for arr in data:
        arr = arr[start:end]
    return data

def exportCSV(filename, npArrs = (), headers = []):
    # Define the file path and name
    csvdata = np.column_stack(npArrs)
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if headers:
            writer.writerow(headers)
        writer.writerows(csvdata)