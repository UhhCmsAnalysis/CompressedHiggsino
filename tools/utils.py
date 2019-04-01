from ROOT import *
from array import array

tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 52
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.0001

units = {}
units['HardMet']='GeV'
units['Met']=units['HardMet']
units['Ht']='GeV'
units['St']='GeV'
units['NJets']=''
units['NCentralJets']=''
units['NForwardJets']=''
units['NLeptons']=''
units['BTags']=''
units['Jet1Pt']='GeV'
units['Jet1Eta']=''
units['Jet2Pt']='GeV'
units['Jet2Eta']=''
units['Jet3Pt']='GeV'
units['Jet3Eta']=''
units['Jet4Pt']='GeV'
units['Jet4Eta']=''
units['HardMetPhi']='rad'
units['DPhi1']='rad'
units['DPhi2']='rad'
units['DPhi3']='rad'
units['DPhi4']='rad'
units['SearchBins']=''
units['BestDijetMass']='GeV'
units['MinDeltaM']='GeV'
units['MaxDPhi']='rad'
units['MaxForwardPt'] = 'GeV'
units['MaxHemJetPt'] = 'GeV'
units['HtRatio'] = ''
units['MinDeltaPhi'] = ''
units['NPhotons'] = ''
units['DPhiPhoPho'] = ''
units['DmStar'] = ''
units['MStar'] = 'GeV'
units['ChipmLabLength'] = 'Log_{10}cm'

def histoStyler(h,color):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    #h.SetFillColor(color)
    size = 0.055
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(1.05)
    h.Sumw2()

def graphStyler(g,color):
    g.SetLineWidth(2)
    g.SetLineColor(color)
    g.SetMarkerColor(color)
    #g.SetFillColor(color)
    size = 0.055
    font = 132
    g.GetXaxis().SetLabelFont(font)
    g.GetYaxis().SetLabelFont(font)
    g.GetXaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleSize(size)
    g.GetXaxis().SetTitleSize(size)
    g.GetXaxis().SetLabelSize(size)   
    g.GetYaxis().SetLabelSize(size)
    g.GetXaxis().SetTitleOffset(1.0)
    g.GetYaxis().SetTitleOffset(1.05)
    
def mkcanvas(name='c1'):
    c1 = TCanvas(name,name,700,630)
    c1.SetBottomMargin(.15)
    c1.SetLeftMargin(.14)
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mkcanvas_wide(name):
    c1 = TCanvas(name,name,1200,700)
    c1.Divide(2,1)
    c1.GetPad(1).SetBottomMargin(.14)
    c1.GetPad(1).SetLeftMargin(.14)
    c1.GetPad(2).SetBottomMargin(.14)
    c1.GetPad(2).SetLeftMargin(.14)    
    c1.GetPad(1).SetGridx()
    c1.GetPad(1).SetGridy()
    c1.GetPad(2).SetGridx()
    c1.GetPad(2).SetGridy()    
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mklegend(x1=.17, y1=.62, x2=.43, y2=.85, color=kWhite):
    lg = TLegend(x1, y1, x2, y2)
    lg.SetFillColor(color)
    lg.SetTextFont(42)
    lg.SetBorderSize(0)
    lg.SetShadowColor(kWhite)
    lg.SetFillStyle(0)
    return lg

def fillth1(h,x, weight=1):
	xp = min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon)
	#print 'x, xp', x, xp
	h.Fill(xp, weight)

def fillth2(h,x,y,weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon), weight)
    
def namewizard(name):
    if 'Mht' in name:
        return 'Offline H_{T}^{miss} [GeV]'
    if 'Met' in name:
        return 'Offline E_{T}^{miss} [GeV]'
    if 'Ht' in name:
        return 'Offline HT [GeV]'
    return name



def mkEfficiencies(hPassList, hAllList):
    gEffList = []
    for i in range(len(hPassList)):
        hPassList[i].Sumw2()
        hAllList[i].Sumw2()
        g = TGraphAsymmErrors(hPassList[i],hAllList[i],'cp')
        FixEfficiency(g,hPassList[i])
        g.SetMarkerSize(3)
        gEffList.append(g)
    return gEffList

def mkEfficiencyRatio(hPassList, hAllList,hName = 'hRatio'):#for weighted MC, you need TEfficiency!
    hEffList = []
    for i in range(len(hPassList)):
        hPassList[i].Sumw2()
        hAllList[i].Sumw2()    
        g = TGraphAsymmErrors(hPassList[i],hAllList[i],'cp')
        print 'RATIO........'
        FixEfficiency(g,hPassList[i])
        hEffList.append(hPassList[i].Clone('hEff'+str(i)))
        hEffList[-1].Divide(hAllList[i])
        cSam1 = TCanvas('cSam1')
        print 'this is the simply divided histogram:'
        hEffList[-1].Draw()
        cSam1.Update()

        print 'now putting in the uncertainties under ratio'
        for ibin in range(1,hEffList[-1].GetXaxis().GetNbins()+1):
            print 'setting errory(ibin)=',ibin,g.GetX()[ibin],g.GetErrorY(ibin)
            print 'compared with histo',ibin,
            hEffList[-1].SetBinError(ibin,1*g.GetErrorY(ibin-1))
            print 'errory(ibin)=',g.GetX()[ibin],g.GetErrorY(ibin-1)
        #histoStyler(hEffList[-1],hPassList[i].GetLineColor())

        cSam2 = TCanvas('cSam2')
        print 'this is the after divided histogram:'
        hEffList[-1].Draw()
        cSam2.Update()


        hEffList[-1].Draw()
    hRatio = hEffList[0].Clone(hName)
    hRatio.Divide(hEffList[1])
    hRatio.GetYaxis().SetRangeUser(0.95,1.05)
    c3 = TCanvas()
    hRatio.Draw()
    c3.Update()
    return hRatio


def pause(str_='push enter key when ready'):
        import sys
        print str_
        sys.stdout.flush() 
        raw_input('')

datamc = 'MC'
def stamp(lumi='n/a'):    
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.12*tl.GetTextSize())
    tl.DrawLatex(0.155,0.85, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/1.12*tl.GetTextSize())
    xlab = 0.25
    tl.DrawLatex(xlab,0.85, ('MC' in datamc)*' work '+'in progress')
    tl.SetTextFont(regularfont)
    tl.DrawLatex(0.68,0.85,'#sqrt{s} = 13 TeV')# (L = '+str(lumi)+' fb^{-1})


#------------------------------------------------------------------------------
def mkcdf(hist, minbin=1):
    hist.Scale(1.0/hist.Integral(1,hist.GetXaxis().GetNbins()))
    c = [0.0]*(hist.GetNbinsX()-minbin+2+1)
    j=1
    for ibin in xrange(minbin, hist.GetNbinsX()+1):
        c[j] = c[j-1] + hist.GetBinContent(ibin)
        j += 1
    c[j] = hist.Integral()
    return c

def mkroc(name, hsig, hbkg, lcolor=kBlue, lwidth=2, ndivx=505, ndivy=505):
    from array import array
    csig = mkcdf(hsig)
    cbkg = mkcdf(hbkg)
    npts = len(csig)
    esig = array('d')
    ebkg = array('d')
    for i in xrange(npts):
        esig.append(1 - csig[npts-1-i])
        ebkg.append(1 - cbkg[npts-1-i])
    g = TGraph(npts,esig,ebkg)
    g.SetName(name)
    g.SetLineColor(lcolor)
    g.SetLineWidth(lwidth)

    g.GetXaxis().SetTitle("#epsilon_{s}")
    g.GetXaxis().SetLimits(0,1)

    g.GetYaxis().SetTitle("#epsilon_{b}")
    g.GetHistogram().SetAxisRange(0,1, "Y");

    g.GetHistogram().SetNdivisions(ndivx, "X")
    g.GetHistogram().SetNdivisions(ndivy, "Y")
    return g


    
def calcTrackIso(trk, tracks):
    ptsum =  -trk.pt()
    for track in tracks:
        dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
        if dR<0.3: ptsum+=track.pt()
    return ptsum/trk.pt()

def calcTrackJetIso(trk, jets):
    for jet in jets:
        if not jet.pt()>30: continue
        if  TMath.Sqrt( (trk.eta()-jet.eta())**2 + (trk.phi()-jet.phi())**2)<0.5: return False
    return True

def calcMiniIso(trk, tracks):
    pt = trk.pt()
    ptsum = -pt
    if pt<=50: R = 0.2
    elif pt<=200: R = 10.0/pt
    else: R = 0.05
    for track in tracks:
        dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
        if dR<R: ptsum+=track.pt()
    return ptsum/trk.pt()
