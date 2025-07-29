import ROOT
import numpy as np
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

#This would be the same as "one event" in a root file, except here, for testing purposes, there is every event activated

hit_channels_x = [1]
hit_channels_y = [64,64,64]


def buildHeatMapEntries(hit_channels_x, hit_channels_y):
    heatmap_matrix = np.zeros((64, 64))

    for x in hit_channels_x:
        for y in hit_channels_y:
            heatmap_matrix[y - 1, x - 1] += 1

    return heatmap_matrix
         

def main():
    heatmap_matrix = buildHeatMapEntries(hit_channels_x, hit_channels_y)
    print(f"Heatmap Entries: {heatmap_matrix}")

if __name__ == "__main__":
    main()
