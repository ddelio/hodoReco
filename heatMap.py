
import ROOT
import math

# 1) Load coordinates
coords = []
with open("coords.txt") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) != 2: continue
        try:
            x, y = map(int, parts)
        except ValueError:
            continue
        if 0 <= x < 64 and 0 <= y < 64:
            coords.append((x, y))
if not coords:
    raise RuntimeError("No valid coordinates found in coords.txt")


h2 = ROOT.TH2I("h2", "64 by 64 Event Grid;X idx;Y idx", 64, 0, 64, 64, 0, 64)
hx = ROOT.TH1I("hx", "Counts vs X;X idx;Counts", 64, 0, 64)
hy = ROOT.TH1I("hy", "Counts vs Y;Y idx;Counts", 64, 0, 64)

for x, y in coords:
    h2.Fill(x, y)
    hx.Fill(x)
    hy.Fill(y)

# Compute modal center 
def get_mode(hist):
    best_bin, best_count = 1, hist.GetBinContent(1)
    for b in range(2, hist.GetNbinsX() + 1):
        cnt = hist.GetBinContent(b)
        if cnt > best_count:
            best_count, best_bin = cnt, b
    return best_bin - 1

mode_x = get_mode(hx)
mode_y = get_mode(hy)

# MM Conversion
pitch_mm   = 0.6
center_idx = 63/2.0
to_mm = lambda i: (i - center_idx) * pitch_mm
mode_x_mm, mode_y_mm = to_mm(mode_x), to_mm(mode_y)

# Fit Gaussians
fit_x = ROOT.TF1("fit_x","gaus",0,64)
fit_y = ROOT.TF1("fit_y","gaus",0,64)
hx.Fit(fit_x,"Q")
hy.Fit(fit_y,"Q")

# Canvas and pads
canvas = ROOT.TCanvas("c","Heatmap with Marginals",800,800)
pad_x = ROOT.TPad("pad_x","",0.0,0.75,0.75,1.0)
pad_y = ROOT.TPad("pad_y","",0.75,0.0,1.0,0.75)
pad_h = ROOT.TPad("pad_h","",0.0,0.0,0.75,0.75)
for p in (pad_x,pad_y,pad_h):
    p.SetMargin(0,0,0,0)
    p.Draw()

# X‑histogram settings
pad_x.cd()
hx.SetStats(False)
hx.Draw("bar")
fit_x.SetLineStyle(2); fit_x.Draw("same")
txt1 = ROOT.TLatex(0.95,0.95,f"#mu={hx.GetMean():.2f}, #sigma={hx.GetRMS():.2f}")
txt1.SetNDC(); txt1.SetTextAlign(31); txt1.Draw()

# Y-histogram settings
pad_y.cd()
pad_y.SetGridx(0)
pad_y.SetGridy(0)
hy.SetStats(False)
hy.Draw("Hbar")
maxCnt = hy.GetMaximum()
hy.GetXaxis().SetRangeUser(0, maxCnt * 1.2)
entries = hy.GetEntries()
width   = hy.GetBinWidth(1)
N       = hy.GetNbinsX()
gpdf = ROOT.TGraph()
gpdf.SetLineColor(ROOT.kRed)
gpdf.SetLineWidth(2)
for b in range(1, N+1):
    ycen = hy.GetBinCenter(b)
    xpdf = fit_y.Eval(ycen) * entries * width
    gpdf.SetPoint(b-1, xpdf, ycen)
txt2 = ROOT.TLatex(0.95, 0.95, f"#mu={hy.GetMean():.2f}, #sigma={hy.GetRMS():.2f}")
txt2.SetNDC(); txt2.SetTextAlign(31); txt2.SetTextSize(0.04)
txt2.Draw()
hy.GetXaxis().SetTitle("Counts")
hy.GetYaxis().SetTitle("Y idx")

# Heatmap settings
pad_h.cd()
h2.SetStats(False); h2.Draw("COLZ")
for i in range(65):
    for L in (ROOT.TLine(i,0,i,64), ROOT.TLine(0,i,64,i)):
        L.SetLineColor(ROOT.kGray); L.SetLineWidth(1); L.Draw()
marker = ROOT.TMarker(mode_x+0.5,mode_y+0.5,20)
marker.SetMarkerColor(ROOT.kWhite); marker.SetMarkerSize(1.5); marker.Draw()
txt_center = ROOT.TLatex(0.15,0.90,f"To Center: X={-mode_x_mm:+.2f} mm, Y={-mode_y_mm:+.2f} mm")
txt_center.SetNDC(); txt_center.SetTextSize(0.04); txt_center.SetTextColor(ROOT.kWhite); txt_center.Draw()
xax,yax = h2.GetXaxis(), h2.GetYaxis()
xax.SetTitle("X position (mm)"); yax.SetTitle("Y position (mm)")
for idx,mm in zip(range(0,64,10),range(-18,19,6)):
    xax.SetBinLabel(idx+1,f"{mm:+.0f}"); yax.SetBinLabel(idx+1,f"{mm:+.0f}")

# 10) Save PDF
canvas.SaveAs("heatmap_with_xy_marginals.pdf")
print(f"Modal center at X={mode_x_mm:+.2f} mm, Y={mode_y_mm:+.2f} mm")
