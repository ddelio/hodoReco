from tabulate import tabulate
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 8
LENGTH = 8

channels = ['A1','A2','A3','A4','A5','A6','A7','A8',
                'B8','B7','B6','B5','B4','B3','B2','B1',
                'C1','C2','C3','C4','C5','C6','C7','C8',
                'D8','D7','D6','D5','D4','D3','D2','D1',
                'E1','E2','E3','E4','E5','E6','E7','E8',
                'F8','F7','F6','F5','F4','F3','F2','F1',
                'G1','G2','G3','G4','G5','G6','G7','G8',
                'H8','H7','H6','H5','H4','H3','H2','H1'
    ]

columns_to_chan = {
    'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4, 'A5': 5, 'A6': 6, 'A7': 7, 'A8': 8,
    'B1': 9, 'B2': 10, 'B3': 11, 'B4': 12, 'B5': 13, 'B6': 14, 'B7': 15, 'B8': 16,
    'C1': 17, 'C2': 18, 'C3': 19, 'C4': 20, 'C5': 21, 'C6': 22, 'C7': 23, 'C8': 24,
    'D1': 25, 'D2': 26, 'D3': 27, 'D4': 28, 'D5': 29, 'D6': 30, 'D7': 31, 'D8': 32,
    'E1': 33, 'E2': 34, 'E3': 35, 'E4': 36, 'E5': 37, 'E6': 38, 'E7': 39, 'E8': 40,
    'F1': 41, 'F2': 42, 'F3': 43, 'F4': 44, 'F5': 45, 'F6': 46, 'F7': 47, 'F8': 48,
    'G1': 49, 'G2': 50, 'G3': 51, 'G4': 52, 'G5': 53, 'G6': 54, 'G7': 55, 'G8': 56,
    'H1': 57, 'H2': 58, 'H3': 59, 'H4': 60, 'H5': 61, 'H6': 62, 'H7': 63, 'H8': 64
}

col_to_channels = {
    1: ['A1'], 2: ['A2'], 3: ['A3'], 4: ['A4'], 5: ['A5'], 6: ['A6'], 7: ['A7'], 8: ['A8'],
    9: ['B1'], 10: ['B2'], 11: ['B3'], 12: ['B4'], 13: ['B5'], 14: ['B6'], 15: ['B7'], 16: ['B8'],
    17: ['C1'], 18: ['C2'], 19: ['C3'], 20: ['C4'], 21: ['C5'], 22: ['C6'], 23: ['C7'], 24: ['C8'],
    25: ['D1'], 26: ['D2'], 27: ['D3'], 28: ['D4'], 29: ['D5'], 30: ['D6'], 31: ['D7'], 32: ['D8'],
    33: ['E1'], 34: ['E2'], 35: ['E3'], 36: ['E4'], 37: ['E5'], 38: ['E6'], 39: ['E7'], 40: ['E8'],
    41: ['F1'], 42: ['F2'], 43: ['F3'], 44: ['F4'], 45: ['F5'], 46: ['F6'], 47: ['F7'], 48: ['F8'],
    49: ['G1'], 50: ['G2'], 51: ['G3'], 52: ['G4'], 53: ['G5'], 54: ['G6'], 55: ['G7'], 56: ['G8'],
    57: ['H1'], 58: ['H2'], 59: ['H3'], 60: ['H4'], 61: ['H5'], 62: ['H6'], 63: ['H7'], 64: ['H8']
}

def numToChannel(chan):
    return col_to_channels.get(chan, ["?"])

def channelAlign():
    alignList = []
    for i in range (0, 64):
        alignList.append(f"{i}: {channels[i]}") 
    return alignList

def buildMap(alignList):
    for col in range(WIDTH*LENGTH):
        print(f"{channels[col]}", end=" ")
        if col % WIDTH == WIDTH - 1:
            print("\n")

def makeHeatMap():
    heatmap = np.zeros((LENGTH, WIDTH))

    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Hit Intensity')
    plt.title('Hit Channel Heatmap')
    plt.xlabel('Width')
    plt.ylabel('Length')
    plt.xticks(ticks=np.arange(WIDTH), labels=[f'Col {i+1}' for i in range(WIDTH)])
    plt.yticks(ticks=np.arange(LENGTH), labels=[f'Row {i+1}' for i in range(LENGTH)])
    for i in range(LENGTH):
        for j in range(WIDTH):
            plt.text(j, i, channels[i*WIDTH + j], ha='center', va='center', color='white')
    plt.show()

def buildRotFiberMap():
    '''for j in range(64):
        for i in range (13):
            print(i, end=" ")
        print("\n")
    heatmap = np.zeros((LENGTH, WIDTH))'''

    heatmap = np.zeros((13, 64))

    plt.imshow(heatmap, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Hit Intensity')
    plt.title('Hit Column Heatmap')
    plt.xlabel('Width')
    plt.ylabel('Length')
    plt.xticks(ticks=np.arange(64), labels=[f'Col {i+1}' for i in range(64)])
    plt.yticks(ticks=np.arange(13), labels=[f'Row {i+1}' for i in range(13)])
    for i in range(64):
        for j in range(13):
            plt.text(i, j, j+1, ha='center', va='center', color='white')
    plt.show()

def channelToCol(hit_channel):
    print(f"Channel {col_to_channels[hit_channel]} is in Column {hit_channel}")
    return hit_channel
    


def main():
    #alignList = channelAlign()
    #buildMap(alignList)   
    #makeHeatMap()   
    #buildRotFiberMap()   
    channelToCol(5)   

if __name__ == "__main__":
    main()
