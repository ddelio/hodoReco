import ROOT
import numpy as np

root_file = "/Users/elegantuniverse/hodoReco/fers_dummy_data.root"
tree_name = "EventTree"
threshold = 1000

heatmap_entries = []

def rootInspect():
    f = ROOT.TFile.Open(root_file, "READ")
    t = f.Get(tree_name)
    print(f"Entries in {tree_name}:", t.GetEntries())
    t.Print()

def eventProcess():
    f = ROOT.TFile.Open(root_file, "READ")
    t = f.Get(tree_name)
    
    for i, ev in enumerate(t):
        b1 = getattr(ev, "FERS_Board1_energyHG")
        b2 = getattr(ev, "FERS_Board2_energyHG")
        
        for ix in range(64):
            if b1[ix] < threshold:
                continue
            for iy in range(64):
                if b2[iy] < threshold:
                    continue
                heatmap_entries.append((ix, iy))

def drawFullHeatmap():
    h2 = ROOT.TH2I("h2",
        "64x64 Coincidence Map;Board1 Index;Board2 Index",
        64, 0, 64,
        64, 0, 64
    )
    
    for x, y in heatmap_entries:
        h2.Fill(x, y)
    
    c = ROOT.TCanvas("c", "Coincidence Heatmap", 800, 700)
    h2.SetStats(False)
    h2.Draw("COLZ")
    
    for i in range(65):
        ROOT.TLine(i,0,i,64).Draw()
        ROOT.TLine(0,i,64,i).Draw()
    
    c.SaveAs("heatmap.pdf")
    print("Saved heatmap.pdf")

def main():
    rootInspect()
    eventProcess()
    drawFullHeatmap()

if __name__ == "__main__":
    main()
