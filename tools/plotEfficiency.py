from ROOT import *
from utils import *
gStyle.SetOptStat(0)
import sys

try: fname = sys.argv[1]
except: fname = 'histsEDM_pMSSM12_MCMC1_12_865833_21of100nFiles1.root' 

f = TFile(fname)
f.ls()

keys = f.GetListOfKeys()
canv = mkcanvas()

for key in keys:
	name = key.GetName()
	if not 'Pass' in name: continue
	if 'Vs' in name: continue
	hpass = f.Get(name)
	hall = f.Get(name.replace('Pass','All'))
	histoStyler(hall, kCyan-8)
	hall.SetFillColor(hall.GetLineColor())	
	hall.SetFillStyle(1001)
	eff = TEfficiency(hpass, hall)
	eff.SetLineWidth(2)
	kinvar = name[1:].replace('Pass','')
	hframe = hpass.Clone('hframe')
	hframe.Reset()
	hframe.GetYaxis().SetRangeUser(0,1.3)	
	hframe.GetXaxis().SetTitle(kinvar +' ['+units[kinvar]+']')
	hframe.GetYaxis().SetTitle('#epsilon')	
	hframe.SetTitle('')
	hframe.Draw()
	hall.Scale(1.0/hall.Integral(),'width')
	hall.Draw('hist same')
	eff.Draw('same')
	hframe.Draw('axis same')
	stamp()
	leg = mklegend(x1=.17, y1=.62, x2=.43, y2=.81)
	leg.AddEntry(eff, 'efficiency', 'l')
	leg.AddEntry(hall, 'spectrum', 'lfp')	
	leg.Draw()
	canv.Update()
	canv.Print('pdfs/eff_'+name+'.pdf')
	pause()
	



