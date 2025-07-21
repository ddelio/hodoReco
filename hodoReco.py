import ROOT
import numpy as np
import matplotlib.pyplot as plt
from hodoChannel import hodoChannel

file = ROOT.TFile("something.root")
tree = file.Get("hodoTree")
THRESHOLD = 1200 #???
PITCH_MM = .6

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

def load_coords_from_reco(reco_list, grid_size=64):
    """
    Turn your list of reconstructed hits into a Nx2 numpy array,
    filtering out None and out-of-bounds pairs.
    """
    coords = []
    for hit in reco_list:
        if hit is None:
            continue
        
        x, y = hit
        if 0 <= x < grid_size and 0 <= y < grid_size:
            coords.append((x, y))
    coords = np.array(coords, dtype=int)
    if coords.size == 0:
        raise RuntimeError("No valid reconstructed coordinates!")
    return coords

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

   
    
    coords = load_coords_from_reco(all_reconstructed)
    vals_x, cnts_x = np.unique(coords[:,0], return_counts=True)
    mode_x = vals_x[np.argmax(cnts_x)]
    vals_y, cnts_y = np.unique(coords[:,1], return_counts=True)
    mode_y = vals_y[np.argmax(cnts_y)]

   
    mid_idx     = (64/2 - 0.5)        
    chan_to_mm  = lambda i: (i - mid_idx) * PITCH_MM
    mode_x_mm   = chan_to_mm(mode_x)
    mode_y_mm   = chan_to_mm(mode_y)
    offset_x_mm = (mode_x - mid_idx) * PITCH_MM
    offset_y_mm = (mode_y - mid_idx) * PITCH_MM

   
    grid = np.zeros((64, 64), dtype=int)
    for x, y in coords:
        grid[y, x] += 1

   
    fig, ax = plt.subplots(figsize=(6,6))
    cax = ax.imshow(
        grid,
        origin="lower",
        interpolation="nearest",
        cmap="Reds",
        vmin=0,
        vmax=grid.max()
    )

    
    major_mm = np.arange(-18, 19, 6)                        
    major_ch = major_mm / PITCH_MM + mid_idx              
    minor_ch = np.arange(-0.5, 64, 1)                

    ax.set_xticks(major_ch)
    ax.set_yticks(major_ch)
    ax.set_xticks(minor_ch, minor=True)
    ax.set_yticks(minor_ch, minor=True)

    ax.grid(which='minor', color='grey', linestyle='-', linewidth=0.1)
    ax.tick_params(which='minor', length=0)
    ax.tick_params(which='major', length=0)

    ax.set_xticklabels([f"{m:+.0f}" for m in major_mm])
    ax.set_yticklabels([f"{m:+.0f}" for m in major_mm])

    
    ax.scatter(
        mode_x, mode_y,
        s=50, c='white', marker='o',
        label=f"Center ({mode_x_mm:+.2f} mm, {mode_y_mm:+.2f} mm)"
    )
    offset_text = f"Move by: ({-offset_x_mm:+.2f} mm, {-offset_y_mm:+.2f} mm)"
    ax.text(
        0.02, 0.02, offset_text,
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment='bottom',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7)
    )

    ax.set_title("Event Counts per 64×64 Fiber Grid\nwith Modal Center (mm)")
    ax.set_xlabel("X position (mm)")
    ax.set_ylabel("Y position (mm)")
    ax.legend(loc="upper right")

    fig.colorbar(cax, label="Counts")
    plt.tight_layout()
    plt.savefig("heatmap64_with_modal_center_mm.png", dpi=150)
    plt.close(fig)

    print("Heatmap saved as 'heatmap64_with_modal_center_mm.png'")
    print(f"Modal center at ({mode_x_mm:+.2f} mm, {mode_y_mm:+.2f} mm)")

if __name__ == "__main__":
    main()
