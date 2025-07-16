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

    all_events = []

    for ev in tree:
        raw_channels = rootToChannel(ev)
        mapped_channels = channelMap(raw_channels)
        clean_hits = eventThres(mapped_channels)
        reco_hits = channelProcess(clean_hits)
        all_events.append(reco_hits)

    return all_events

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

def printPair(reco_hits):
    for i, hit in enumerate(reco_hits):
        print(f"Event {i}: Track candidates -> {hit}")

def main():
    root_file = "/Users/elegantuniverse/hodoscope_readout/run1069_250708073015.rootd"
    file = ROOT.TFile.Open(root_file)
    tree = file.Get("EventTree")

    print("Inspecting ROOT file...")
    rootInspect(root_file)

    print("Processing events...")
    all_reconstructed = eventProcess(tree)

    print("Printing hit pairs...")
    printPair(all_reconstructed)

if __name__ == "__main__":
    main()
