import os
import ltspice
import matplotlib.pyplot as plt
import numpy as np


class ReadLTSpice:
    def __init__(self, folder="data", idx=None):
        varListData = []
        self.montecarlo = False

        # define the folder paths
        local = os.getcwd()
        data_folder = os.path.join(local, folder)

        # get the list of filenames in the data folder
        data_filenames = os.listdir(data_folder)

        if idx is None:
            for i, name in enumerate(data_filenames):
                print(f"{i}:\t{name}")
            i = input("Enter file index to Open: ")

        if idx > len(data_filenames):
            print(f"File index out of range")
            return

        # open the first file in the list
        self.filename = data_filenames[idx]
        filePath = os.path.join(data_folder, self.filename)
        print(f"Reading file: {self.filename}")
        self.l = ltspice.Ltspice(filePath)

        # parse the file
        self.l.parse()

        self.case_count = self.l.case_count

        self.varListNames = self.l.variables

        for varName in self.varListNames:
            if self.case_count > 1:
                self.montecarlo = True
                run = []
                for i in range(self.case_count):
                    run.append(self.l.get_data(varName, case=i))
                varListData.append(run)
            else:
                varListData.append(self.l.get_data(varName))

        self.time = varListData[0]
    
    def getSpice(self):
        return self.l

    def info(self):
        print(f"File: {self.filename}")
        print(f"Data points: {len(self.time)}")
        print(f"Monte Carlo: {self.montecarlo}")
        print(f"Runs: {self.case_count}")
        print("Variable list:")
        for i, name in enumerate(self.varListNames):
            print(f"{i}:\t{name}")
        pass