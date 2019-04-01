from ROOT import *
from utils import *
from glob import glob
import sys
try: 
    inputfilename = sys.argv[1]
except:
    inputfilename =  'root://cmsxrootd.fnal.gov//store/user/sbein/pMSSM_MCMC1_38_870285.root'
    inputfilename = '/nfs/dust/cms/user/beinsam/CommonNtuples/NtupleMaker/CMSSW_8_0_28/src/TreeMaker/Production/test/Output/pMSSM_MCMC1_38_870285_dm13*.root'

#gROOT.ProcessLine(open('src/UsefulJet.cc').read())
#exec('from ROOT import *')
if 'pMSSM' in inputfilename: issig = True
else: issig = False

    
def drMinObjCol(track, jets):
    deltaRmin = 999
    for jet in jets:
        deltaRmin = min(deltaRmin,jet.DeltaR(track))
    return deltaRmin

def dphiMinObjCol(track, jets):
    deltaPhimin = 999
    for jet in jets:
        deltaPhimin = min(deltaPhimin,abs(jet.DeltaPhi(track)))
    return deltaPhimin	

newfile = TFile('effHists_'+inputfilename.split('/')[-1].replace('*','STAR'),'recreate')       

some_freaky_chain = TChain('TreeMaker2/PreSelection') #t.Add('root://cmsxrootd.fnal.gov/'+inputfilename)
some_freaky_chain.Add(inputfilename)
verbosity = 1000

some_freaky_chain.Show(0)
nentries = some_freaky_chain.GetEntries() 
#nentries = min(1000,nentries)

print 'Nevents = ', nentries
hHT = TH1F('hHt','hHt',100,0,5000)
hHT_weighted = TH1F('hHt_weighted','hHt_weighted',100,0,5000)

hGenElPtAll = TH1F('hGenElPtAll','hGenElPtAll',15,0,15)
histoStyler(hGenElPtAll,kBlack)
hGenMuPtAll = TH1F('hGenMuPtAll','hGenMuPtAll',15,0,15)
histoStyler(hGenMuPtAll,kBlack)
hGenElPtPassLep = TH1F('hGenElPtPassLep','hGenElPtPassLep',15,0,15)
histoStyler(hGenElPtPassLep,kBlack)
hGenMuPtPassLep = TH1F('hGenMuPtPassLep','hGenMuPtPassLep',15,0,15)
histoStyler(hGenMuPtPassLep,kBlack)
hGenElPtPassTrack = TH1F('hGenElPtPassTrack','hGenElPtPassTrack',15,0,15)
histoStyler(hGenElPtPassTrack,kBlack)
hGenMuPtPassTrack = TH1F('hGenMuPtPassTrack','hGenMuPtPassTrack',15,0,15)
histoStyler(hGenMuPtPassTrack,kBlack)

hMinDrGenElTrack = TH1F('hMinDrGenElTrack','hMinDrGenElTrack',50,0,0.1)
histoStyler(hMinDrGenElTrack,kBlack)
hMinDrGenMuTrack = TH1F('hMinDrGenMuTrack','hMinDrGenMuTrack',50,0,0.1)
histoStyler(hMinDrGenMuTrack,kBlack)
hMinDrGenElLep = TH1F('hMinDrGenElLep','hMinDrGenElLep',50,0,0.1)
histoStyler(hMinDrGenElLep,kBlack)
hMinDrGenMuLep = TH1F('hMinDrGenMuLep','hMinDrGenMuLep',50,0,0.1)
histoStyler(hMinDrGenMuLep,kBlack)


for iEntry in range(nentries):
    if iEntry % verbosity ==0:
        prog = str(round(100*(float(iEntry) / float(nentries)),2))+'%'
        print 'Processed Events: ', iEntry ,' | Done: ', prog
    some_freaky_chain.GetEntry(iEntry)
    weight = 1#some_freaky_chain.CrossSection
    hHT.Fill(some_freaky_chain.HT)
    hHT_weighted.Fill(some_freaky_chain.HT,some_freaky_chain.CrossSection)

  
    genels, genmus = [], []
    for igen, genp in enumerate(some_freaky_chain.GenParticles):        
        if not some_freaky_chain.GenParticles_ParentId[igen]==1000023: continue
        if not abs(genp.Eta())<2.4: continue        
        if abs(some_freaky_chain.GenParticles_PdgId[igen]) == 11:
            genels.append(some_freaky_chain.GenParticles[igen])
            fillth1(hGenElPtAll,genp.Pt())
        if abs(some_freaky_chain.GenParticles_PdgId[igen]) == 13:
            genmus.append(some_freaky_chain.GenParticles[igen])
            fillth1(hGenMuPtAll, genp.Pt())

    for genel in genels:
        for ichi, track in enumerate(some_freaky_chain.chiCands):
            if not abs(some_freaky_chain.chiCands_dzVtx[ichi])<0.05: continue        
            if not abs(some_freaky_chain.chiCands_dxyVtx[ichi])<0.03: continue
            if not some_freaky_chain.chiCands_trkRelIso[ichi]<0.01: continue  
            drminElTrack = drMinObjCol(track, genels)
            if drminElTrack<0.01:
                fillth1(hGenElPtPassTrack, genel.Pt())
                fillth1(hMinDrGenElTrack, drminElTrack)                        
                if some_freaky_chain.chiCands_trackLeptonIso[ichi]<0.01:         
                    fillth1(hGenElPtPassLep, genel.Pt())            
                    fillth1(hMinDrGenElLep, drminElTrack)
                    break
                else:
                    break

    for genmu in genmus:    
        for ichi, track in enumerate(some_freaky_chain.chiCands):
            if not abs(some_freaky_chain.chiCands_dzVtx[ichi])<0.03: continue        
            if not abs(some_freaky_chain.chiCands_dxyVtx[ichi])<0.05: continue
            drminMuTrack = drMinObjCol(track, genmus)
            if drminMuTrack<0.01:
                fillth1(hMinDrGenMuTrack, drminMuTrack)    
                fillth1(hGenMuPtPassTrack, genmu.Pt())
                if some_freaky_chain.chiCands_trackLeptonIso[ichi]<0.01:         
                    fillth1(hGenMuPtPassLep, genmu.Pt())            
                    fillth1(hMinDrGenMuLep, drminMuTrack)            
                    break
                else: 
                    break
        
        

    

hMinDrGenElTrack.Write()
hMinDrGenElLep.Write()
hMinDrGenMuTrack.Write()
hMinDrGenMuLep.Write()

hGenElPtAll.Write()
hGenElPtPassTrack.Write()
hGenElPtPassLep.Write()
hGenMuPtAll.Write()
hGenMuPtPassTrack.Write()
hGenMuPtPassLep.Write()

newfile.cd()
hHT.Write()
hHT_weighted.Write()


print 'just created', newfile.GetName()
newfile.Close()
