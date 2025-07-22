from tabulate import tabulate

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

def main():
    alignList = channelAlign()
    buildMap(alignList)            

if __name__ == "__main__":
    main()
