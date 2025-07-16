import numpy as np 

def rootToChannel(event):
    adc_values = ev.hodo_adc
    channels = ev.hodo_ch
    return [{"channel": ch, "adc": adc} for ch, adc in zip(channels, adc_values)]

def channelMap(channel_num):
#Takes in channel number (1-64) and gives back physical id

    '''mapped = []
    for entry in raw_channels:
        ch = entry['channel']
        adc = entry['adc']
        plane = 'X' if ch % 2 == 0 else 'Y'
        position = ch // 2
        mapped.append({"plane": plane, "pos": position, "adc": adc})
    return mapped'''
    
    channels = ['A1','A2','A3','A4','A5','A6','A7','A8',
                'B8','B7','B6','B5','B4','B3','B2','B1',
                'C1','C2','C3','C4','C5','C6','C7','C8',
                'D8','D7','D6','D5','D4','D3','D2','D1',
                'E1','E2','E3','E4','E5','E6','E7','E8',
                'F8','F7','F6','F5','F4','F3','F2','F1',
                'G1','G2','G3','G4','G5','G6','G7','G8',
                'H8','H7','H6','H5','H4','H3','H2','H1'
    ]
    return channels[channel_num - 1]
    

def channelProcess(channel_num):
#Takes in channel number (1-64) and gives back physical position along x/y axis
    
    '''x_hits = [c['pos'] for c in mapped_channels if c['plane'] == 'X']
    y_hits = [c['pos'] for c in mapped_channels if c['plane'] == 'Y']
    return [(x, y) for x in x_hits for y in y_hits]  '''
    
    X = [-19.2, -18.6, -18.0, -17.4, -16.8, -16.2, 
         -15.6, -15.0, -14.4, -13.8, -13.2, -12.6, 
         -12.0, -11.4, -10.8, -10.2, -9.6, -9.0, 
         -8.4, -7.8, -7.2, -6.6, -6.0, -5.4, -4.8, 
         -4.2, -3.6, -3.0, -2.4, -1.8, -1.2, -0.6,
        0.0, 0.6, 1.2, 1.8, 2.4, 3.0, 3.6, 4.2,4.8,
        5.4, 6.0, 6.6, 7.2, 7.8, 8.4, 9.0, 9.6, 10.2,
        10.8, 11.4, 12.0, 12.6,13.2, 13.8, 14.4, 
        15.0, 15.6, 16.2, 16.8,17.4, 18.0, 18.6, 19.2
        ]
    
    return X[channel_num - 1]
