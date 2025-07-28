import ROOT
import numpy as np
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt

root_file = "/Users/elegantuniverse/hodoReco/run1069_250708073015.root"
tree_name = "EventTree"
threshold = 1200
WIDTH = 4
LENGTH = 16
AREA = WIDTH * LENGTH

print("Starting")

channel_map = [4,2,3,1,8,6,7,5,11,9,12,10,15,13,16,14,20,18,19,17,24,22,23,21,27,25,28,26,31,29,32,30,36,34,35,33,40,38,39,37,43,41,44,42,47,45,48,46,52,50,51,49,56,54,55,53,59,57,60,58,63,61,64,62]
channel_to_col = {
                    1: [4,8,11,15,20,24,27,31,36,40,43,47,52,56,59,63],
                    2: [2,6,9,13,18,22,25,29,34,38,41,45,50,54,57,61],
                    3: [3,7,12,16,19,23,28,32,35,39,44,48,51,55,60,64],
                    4: [1,5,10,14,17,21,26,30,33,37,42,46,49,53,58,62]
}
channel_to_row = {  1: [4,2,3,1],
                    2: [8,6,7,5],
                    3: [11,9,12,10],
                    4: [15,13,16,14],
                    5: [20,18,19,17],
                    6: [24,22,23,21],
                    7: [27,25,28,26],
                    8: [31,29,32,30],
                    9: [36,34,35,33],
                    10: [40,38,39,37],
                    11: [43,41,44,42],
                    12: [47,45,48,46],
                    13: [52,50,51,49],
                    14: [56,54,55,53],
                    15: [59,57,60,58],
                    16: [63,61,64,62]
}

corresponding_channels = {
}
 
channel_to_position = {}

for col, channels in channel_to_col.items():
    for row_idx, chan in enumerate(channels):
        channel_to_position[chan] = (col, row_idx)

def rootInspect():
    try:
        rt_file = ROOT.TFile.Open(root_file, "READ")
        tree = rt_file.Get("EventTree")
        print(tree.GetEntries())
        tree.Print()
        for branch in tree.GetListOfBranches():
            print(branch.GetName())
    finally:
        return
    
def convertMapping(hit_channel):
    return channel_to_position.get(hit_channel, ("?", "?"))

def numToChannel(index):
    return channel_map[index] if 0 <= index < len(channel_map) else "?"

def printMapping(hit_channels):  
    board = [["" for _ in range(WIDTH)] for _ in range(LENGTH)]
    for i in range(AREA):
        row = i // 4
        col = i % 4
        if i in hit_channels:
            board[row][col] = numToChannel(i)
        else:
            board[row][col] = "" 

    table = tabulate(
        board,
        headers="",
        showindex="",
        tablefmt="fancy_grid"
    )
    print(table)

def makeHeatMap(hit_channels):
    heatmap = np.zeros((LENGTH, WIDTH))
    for i in range(AREA):
        row = i // 4
        col = i % 4
        if i in hit_channels:
            heatmap[row][col] = 1
        else:
            heatmap[row][col] = 0

    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Hit Intensity')
    plt.title('Hit Channel Heatmap')
    plt.xlabel('Width')
    plt.ylabel('Length')
    plt.xticks(ticks=np.arange(WIDTH), labels=[f'Col {i+1}' for i in range(WIDTH)])
    plt.yticks(ticks=np.arange(LENGTH), labels=[f'Row {i+1}' for i in range(LENGTH)])
    plt.show()
            
        
def eventProcess():
    file = ROOT.TFile.Open(root_file)
    tree = file.Get(tree_name)
    branch_name = f"FERS_Board1_energyHG"
    for i, event in enumerate(tree):
        value = getattr(event, branch_name)
        event_list = []
        energies_list = []
        location_list = []
        for j in range(AREA):
            if value[j] > threshold:
                event_list.append(j)
                energies_list.append(value[j])
                location_list.append(convertMapping(j))
                if not event_list:
                    continue
                else: 
                    print(f"---------------Event {i}--------------- \n  Channel#: {event_list} \n  Energy: {energies_list} \n  Location: {location_list}")
                    printMapping(event_list)
                    #makeHeatMap(event_list)
            else:
                continue
        event_list = []

def checkIntersection(hit_channel)
    return corresponding_channels[hit_channel]


def main():
    rootInspect()
    eventProcess()
    return

if __name__ == "__main__":
    main()
