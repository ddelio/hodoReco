import ROOT
import sys
sys.path.append("CMSPLOTS")
import numpy as np
from utils.html_generator import generate_html
from runconfig import runNumber

root_file = "/Users/elegantuniverse/hodoReco/fers_dummy_data.root"
tree_name = "EventTree"
threshold = 1000

rootdir = f"results/root/Run{runNumber}/"
plotdir = f"results/plots/Run{runNumber}/"
htmldir = f"results/html/Run{runNumber}/"

heatmap_entries = []

def eventProcess():
    global heatmap_entries
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

def buildHeatMapEntries():
    heatmap_matrix = np.zeros((64, 64)) 

    for x, y in heatmap_entries:
        heatmap_matrix[y, x] += 1  
    

    return heatmap_matrix

def get_mode(hist):
    best_bin, best_count = 1, hist.GetBinContent(1)
    for b in range(2, hist.GetNbinsX() + 1):
        cnt = hist.GetBinContent(b)
        if cnt > best_count:
            best_count, best_bin = cnt, b
    return best_bin - 1

def makeHeatmaps():
    heatmap_matrix = buildHeatMapEntries()
    heatmap_matrix = buildHeatMapEntries()

    h2 = ROOT.TH2I("h2", "64 by 64 Event Grid;X idx;Y idx", 64, 0, 64, 64, 0, 64)
    hx = ROOT.TH1I("hx", "Counts vs X;X idx;Counts", 64, 0, 64)
    hy = ROOT.TH1I("hy", "Counts vs Y;Y idx;Counts", 64, 0, 64)

    for i in range(64):
        for j in range(64):
            count = heatmap_matrix[j, i]
            if count > 0:
                h2.Fill(i, j, count)
                hx.Fill(i, count)
                hy.Fill(j, count)

    mode_x = get_mode(hx)
    mode_y = get_mode(hy)
    pitch_mm = 0.6
    center_idx = 63 / 2.0
    to_mm = lambda i: (i - center_idx) * pitch_mm
    mode_x_mm, mode_y_mm = to_mm(mode_x), to_mm(mode_y)
    fit_x = ROOT.TF1("fit_x", "gaus", 0, 64)
    fit_y = ROOT.TF1("fit_y", "gaus", 0, 64)
    hx.Fit(fit_x, "Q")
    hy.Fit(fit_y, "Q")
    canvas = ROOT.TCanvas("c", "Heatmap with Marginals", 800, 800)
    pad_x = ROOT.TPad("pad_x", "", 0.0, 0.75, 0.75, 1.0)
    pad_y = ROOT.TPad("pad_y", "", 0.75, 0.0, 1.0, 0.75)
    pad_h = ROOT.TPad("pad_h", "", 0.0, 0.0, 0.75, 0.75)
    for p in (pad_x, pad_y, pad_h):
        p.SetMargin(0, 0, 0, 0)
        p.Draw()
    pad_x.cd()
    hx.SetStats(False)
    hx.Draw("bar")
    fit_x.SetLineStyle(2)
    fit_x.Draw("same")
    txt1 = ROOT.TLatex(0.95, 0.95, f"#mu={hx.GetMean():.2f}, #sigma={hx.GetRMS():.2f}")
    txt1.SetNDC()
    txt1.SetTextAlign(31)
    txt1.Draw()
    pad_y.cd()
    hy.SetStats(False)
    hy.Draw("Hbar")
    maxCnt = hy.GetMaximum()
    hy.GetXaxis().SetRangeUser(0, maxCnt * 1.2)
    entries = hy.GetEntries()
    width = hy.GetBinWidth(1)
    N = hy.GetNbinsX()
    gpdf = ROOT.TGraph()
    gpdf.SetLineColor(ROOT.kRed)
    gpdf.SetLineWidth(2)
    for b in range(1, N + 1):
        ycen = hy.GetBinCenter(b)
        xpdf = fit_y.Eval(ycen) * entries * width
        gpdf.SetPoint(b - 1, xpdf, ycen)
    txt2 = ROOT.TLatex(0.95, 0.95, f"#mu={hy.GetMean():.2f}, #sigma={hy.GetRMS():.2f}")
    txt2.SetNDC()
    txt2.SetTextAlign(31)
    txt2.SetTextSize(0.04)
    txt2.Draw()
    pad_h.cd()
    h2.SetStats(False)
    h2.Draw("COLZ")
    for i in range(65):
        for L in (ROOT.TLine(i, 0, i, 64), ROOT.TLine(0, i, 64, i)):
            L.SetLineColor(ROOT.kGray)
            L.SetLineWidth(1)
            L.Draw()
    marker = ROOT.TMarker(mode_x + 0.5, mode_y + 0.5, 20)
    marker.SetMarkerColor(ROOT.kWhite)
    marker.SetMarkerSize(1.5)
    marker.Draw()
    txt_center = ROOT.TLatex(0.15, 0.90, f"To Center: X={-mode_x_mm:+.2f} mm, Y={-mode_y_mm:+.2f} mm")
    txt_center.SetNDC()
    txt_center.SetTextSize(0.04)
    txt_center.SetTextColor(ROOT.kWhite)
    txt_center.Draw()
    xax, yax = h2.GetXaxis(), h2.GetYaxis()
    xax.SetTitle("X position (mm)")
    yax.SetTitle("Y position (mm)")
    for idx, mm in zip(range(0, 64, 10), range(-18, 19, 6)):
        xax.SetBinLabel(idx + 1, f"{mm:+.0f}")
        yax.SetBinLabel(idx + 1, f"{mm:+.0f}")

    canvas.SaveAs("/hodoHeatmap.png")
    print(f"Modal center at X={mode_x_mm:+.2f} mm, Y={mode_y_mm:+.2f} mm")
    return heatmap_matrix

def generateHTML():
    plots = ["hodoHeatmap.png"]
    outdir_plots = f"{plotdir}/Conditions_vs_Event"
    output_html = f"{htmldir}/Conditions_vs_Event/index.html"
    generate_html(plots, outdir_plots, plots_per_row=4,
                  output_html=output_html)
    return output_html

def main():
    eventProcess()
    makeHeatmaps()
    generateHTML()
    
if __name__ == "__main__":
    main()
