import ROOT
import numpy as np
from hodoChannel import hodoChannel

file = ROOT.TFile("something.root")
tree = file.Get("hodoTree")
THRESHOLD = 1200 #???

def rootInspect(file, tree_name="EventTree"):
    try:
        file = ROOT.TFile.Open(file)
        if not file or file.IsZombie():
            print(f"Error: Could not open ROOT file '{file}'")
            return []

        tree = file.Get(tree_name)
        if not tree:
            print(f"Error: TTree '{tree_name}' not found in file.")
            return []

        branches = tree.GetListOfBranches()
        channel_names = [branch.GetName() for branch in branches]

        print(f"Channels (branches) in '{tree_name}':")
        for name in channel_names:
            print(f" - {name}")

        return channel_names

    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

def eventProcess():
    # Michael
    return


def eventThres(event, channels, threshold=THRESHOLD):
   
    x_hits = []
    y_hits = []

    for name in channels:
        value = getattr(event, name)
        if value is None:
            continue

        if value > threshold:
            hc = hodoChannel(name)
            if hc.isX():         # or however the hell we decide to spereate x and y 
                x_hits.append(name)
            else:
                y_hits.append(name)

    return x_hits, y_hits


def eventChannelInfo(event, channels, threshold=THRESHOLD):
    """
    For this 'event', find every channel whose value > threshold,
    instantiate a hodoChannel for it, and print all of its info.
    """
    print("=== Fired channels info ===")
    for name in channels:
        value = getattr(event, name, None)
        if value is None or value <= threshold:
            continue

        hc = hodoChannel(name)

        print(f"\nChannel '{name}':")
        print(f"  - raw value       : {value}")
        print(f"  - is X?           : {hc.isX()}")
        print(f"  - is Y?           : {hc.isY()}")

        public_attrs = [a for a in dir(hc)
                        if not a.startswith("_")
                        and not callable(getattr(hc, a))]
        if public_attrs:
            print("  -- other attributes:")
            for attr in public_attrs:
                val = getattr(hc, attr)
                print(f"     • {attr:15s} = {val}")



def main():
    # Michael
    return

