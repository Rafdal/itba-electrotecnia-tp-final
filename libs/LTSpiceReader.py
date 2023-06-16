import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np


class ReadLTSpice:
    def __init__(self, folder="data", idx=None):
        self.varListData = []
        self.is_montecarlo = False
        self.filename = ""

        self.colors = {
            "V": "blue",
            "I": "red",
            "?": "black",
        }

        filepath = self.getFilePath(folder, idx)

        self.l = ltspice.Ltspice(filepath)

        # parse the file
        self.l.parse()

        print(self.l._mode)

        self.case_count = self.l.case_count
        self.varListNames = self.l.variables[1:]
        self.varListInfo = []

        if self.l._mode == "AC":
            self.x = self.l.get_frequency()
        else:
            self.x = self.l.get_time()

        print("Warning: Usando interpolación de datos")
        for varName in self.varListNames:
            if self.case_count > 1:
                self.is_montecarlo = True
                run = []
                for i in range(self.case_count):
                    # Al usar time=self.x, se interpola la señal para que tenga el mismo largo
                    if self.l._mode == "AC":
                        run.append(self.l.get_data(varName, case=i))
                    else:
                        run.append(self.l.get_data(varName, case=i, time=self.x))
                self.varListData.append(run)

            else:
                self.varListData.append(self.l.get_data(varName))

            if varName[0] == "I":
                self.varListInfo.append({
                    "name": varName.split("(")[1].split(")")[0],
                    "symbol": "I",
                    "unit": "A",
                })
            elif varName[0] == "V":
                self.varListInfo.append({
                    "name": varName.split("(")[1].split(")")[0],
                    "symbol": "V",
                    "unit": "V",
                })
            else:
                self.varListInfo.append({
                    "name": varName.split("(")[1].split(")")[0],
                    "symbol": "?",
                    "unit": "?",
                })

        self.data_points = len(self.x)

    def getFilePath(self, folder, idx):
        # define the folder paths
        local = os.getcwd()
        data_folder = os.path.join(local, folder)

        # get the list of filenames in the data folder
        data_filenames = os.listdir(data_folder)

        if idx is None:
            for i, name in enumerate(data_filenames):
                print(f"{i}:\t{name}")
            idx = int(input("Enter file index to Open: "))

        if idx > len(data_filenames):
            print(f"File index out of range")
            exit(1)

        # open the file
        self.filename = data_filenames[idx]
        filePath = os.path.join(data_folder, self.filename)
        print(f"Reading file: {self.filename}")
        return filePath
    
    def getSpice(self):
        return self.l

    def info(self):
        print(f"File: {self.filename}")
        print("Variable list:")
        for i, name in enumerate(self.varListNames):
            print(f"  {i:02}: \"{name}\"")
        if self.is_montecarlo:
            print(f"Monte Carlo Runs: {self.case_count}")
            mean = np.mean(self.data_points)
            maxDp = np.max(self.data_points)
            minDp = np.min(self.data_points)
            print(f"Data points (Mean: {mean}\tMax: {maxDp}\tMin: {minDp})")
        else:
            print(f"Monte Carlo: FALSE")
            print(f"Data points: {self.data_points}")
        pass