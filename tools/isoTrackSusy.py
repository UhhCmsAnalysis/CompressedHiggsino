from ROOT import *
from utils import *
from glob import glob
import sys
try: 
    inputfilename = sys.argv[1]
except:
    #inputfilename =  'root://cmsxrootd.fnal.gov//store/user/sbein/pMSSM_MCMC1_38_870285.root'
    inputfilename = '/nfs/dust/cms/user/beinsam/NaturalSusy/Output/ntuple_sidecar/smallchunks/pMSSM_MCMC1_38_870285_dm13_chi20chi10_SIM_*.root'
    #'/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/pMSSM_MCMC1_38_870285_chi+chi0_RA2AnalysisTree.root'

#gROOT.ProcessLine(open('src/UsefulJet.cc').read())
#exec('from ROOT import *')
if 'pMSSM' in inputfilename: issig = True
else: issig = False

selectionsets = {}
inf = 9999
#selectionsets order: HT,MET,NJets,DeltaPhi1,DeltaPhi2
#selectionsets['2ostracks'] = [(0,inf),(0,inf),(0,inf),(0,inf),(0,inf),(0,inf),(0,inf)]
#selectionsets['2sstracks'] = [(0,inf),(0,inf),(0,inf),(0,inf),(0,inf),(0,inf),(0,inf)]
#selectionsets['baseline'] = [(150,inf),(150,inf),(0,inf),(0,inf),(0,inf),(0,inf),(0,inf)]
selectionsets['softmonojet']   = [(10,inf),(10,inf),(1,1),(0,inf),(0,inf),(0,inf),(0,inf)]
selectionsets['monojet']   = [(150,inf),(150,inf),(1,1),(0,inf),(0,inf),(0,inf),(0,inf)]


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


isocutlist = []
for i in range(1,5):
    isocutlist.append(0.01*i)
isocutlist.append(999)

hDiMuGenM = TH1F('hDiMuGenM','hDiMuGenM',100,0,19)
hDiElGenM = TH1F('hDiElGenM','hDiElGenM',100,0,19)

hPtZstar = TH1F('hPtZstar','hPtZstar',40,0,40)
hPtChi = TH1F('hPtChi','hPtChi',50,0,500)

hDeltaEtaGen = TH1F('hDeltaEtaGen','hDeltaEtaGen',500,0,5)
hDeltaPhiGen = TH1F('hDeltaPhiGen','hDeltaPhiGen',300,0,3)
hDeltaEtaTrack = TH1F('hDeltaEtaTrack','hDeltaEtaTrack',500,0,5)

hDeltaEtaZstarJet = TH1F('hDeltaEtaZstarJet','hDeltaEtaZstarJet',500,0,5)
hDeltaPhiZstarJet = TH1F('hDeltaPhiZstarJet','hDeltaPhiZstarJet',400,0,4)

newfile = TFile('hists_Had'+inputfilename.split('/')[-1],'recreate')

hMETdict = {}
hHTdict = {}
hNJetsdict = {}
hBTagsdict = {}
hDeltaPhi1dict = {}
hDeltaPhi2dict = {}
hQGLeadingJetdict = {}
hNIsoTracksdict = {}
h2OsTrackMassdict = {}
h2SsTrackMassdict = {}
h2TrackMassdict = {}
hDrTrackJet = {}
hDrTrackJetPtW = {}


for selectionset in selectionsets:
    hMETdict[selectionset] = TH1F('hMET_'+selectionset,'hMET_'+selectionset,100,0,1000)
    hHTdict[selectionset] = TH1F('hHT_'+selectionset,'hHT_'+selectionset,300,0,3000)
    hNJetsdict[selectionset] = TH1F('hNJets_'+selectionset,'hNJets_'+selectionset,12,0,12)
    hBTagsdict[selectionset] = TH1F('hBTags_'+selectionset,'hBTags_'+selectionset,4,0,4)
    hDeltaPhi1dict[selectionset] = TH1F('hDeltaPhi1_'+selectionset,'hDeltaPhi1_'+selectionset,10,0,3.2)
    hDeltaPhi2dict[selectionset] = TH1F('hDeltaPhi2_'+selectionset,'hDeltaPhi2_'+selectionset,10,0,3.2)
    hQGLeadingJetdict[selectionset] = TH1F('hQGLeadingJet_'+selectionset,'hQGLeadingJet_'+selectionset,30,-0.25,1.25)
    for iiso, iso in enumerate(isocutlist):
        thingy = selectionset+'_iso'+str(int(100*iso))
        hNIsoTracksdict[thingy] = TH1F('hNIsoTracks_'+thingy,'hNIsoTracks_'+thingy,100,0,100)
        h2OsTrackMassdict[thingy] = TH1F('h2OsTrackMass_'+thingy,'h2OsTrackMass_'+thingy,40,0,40)  
        h2SsTrackMassdict[thingy] = TH1F('h2SsTrackMass_'+thingy,'h2SsTrackMass_'+thingy,40,0,40)
        h2TrackMassdict[thingy] = TH1F('h2TrackMass_'+thingy,'h2TrackMass_'+thingy,40,0,40)   
        hDrTrackJet[thingy] = TH1F('hDrTrackJet_'+thingy,'hDrTrackJet_'+thingy,40,0,4)     
        hDrTrackJetPtW[thingy] = TH1F('hDrTrackJetPtW'+thingy,'hDrTrackJetPtW'+thingy,40,0,4)             

some_freaky_chain = TChain('TreeMaker2/PreSelection') #t.Add('root://cmsxrootd.fnal.gov/'+inputfilename)
some_freaky_chain.Add(inputfilename)
verbosity = 1000

hPt1VsPt2GenLeps = TH2F('hPt1VsPt2GenLeps','hPt1VsPt2GenLeps',20,0,20,20,0,20)

some_freaky_chain.Show(0)
nentries = some_freaky_chain.GetEntries() 
#nentries = min(1000,nentries)

print 'Nevents = ', nentries
hHT = TH1F('hHt','hHt',100,0,5000)
hHT_weighted = TH1F('hHt_weighted','hHt_weighted',100,0,5000)

mass = {} 
massOS= {}    
massSS = {}     
isotracks_plus = {}
isotracks_minus = {} 
isotracks = {}  
drtrackjet = {}
drtrackjetPtW = {}

for iEntry in range(nentries):
    if iEntry % verbosity ==0:
        prog = str(round(100*(float(iEntry) / float(nentries)),2))+'%'
        print 'Processed Events: ', iEntry ,' | Done: ', prog
    some_freaky_chain.GetEntry(iEntry)
    weight = 1#some_freaky_chain.CrossSection
    hHT.Fill(some_freaky_chain.HT)
    hHT_weighted.Fill(some_freaky_chain.HT,some_freaky_chain.CrossSection)

    jets = []
    for jet in some_freaky_chain.Jets:
        if not jet.Pt()>30: continue
        if not abs(jet.Eta())<2.4: continue
        jets.append(jet)

    if len(some_freaky_chain.Jets)>0:
        qgj1 = some_freaky_chain.Jets_qgLikelihood[0]
    else:
        gqj1 = -1.0

    if not len(jets)>0: continue

    
    if issig:    
        aveEtaGen = 0
        ngen = 0
        vec4EtaGen = TLorentzVector()
        genelp, genelm, genmup_, genmum = [], [], [], []
        genleps = []

        for igen, gen in enumerate(some_freaky_chain.GenParticles):
            if some_freaky_chain.GenParticles_PdgId[igen]==1000023: hPtChi.Fill(gen.Pt(),weight)
            if not some_freaky_chain.GenParticles_ParentId[igen]==1000023: continue
            #if not some_freaky_chain.GenParticles_Status[igen]==1: continue        
            if some_freaky_chain.GenParticles_PdgId[igen]==1000022: 
                hPtZstar.Fill((gen-some_freaky_chain.GenParticles[some_freaky_chain.GenParticles_ParentIdx[igen]]).Pt())
                continue
            ngen+=1
            aveEtaGen+=gen.Eta()
            vec4EtaGen+=gen
            genleps.append(gen)
            #print 'considering lep', some_freaky_chain.GenParticles_PdgId[igen], gen.Pt()
            #if not some_freaky_chain.GenParticles[igen].Pt()>2: continue
            #if not some_freaky_chain.GenParticles_ParentId[igen]==1000023: continue
            if some_freaky_chain.GenParticles_PdgId[igen]==11:
                genelm.append(gen)
            if some_freaky_chain.GenParticles_PdgId[igen]==-11:
                genelp.append(gen)
            if some_freaky_chain.GenParticles_PdgId[igen]==13:
                genmum.append(gen)
            if some_freaky_chain.GenParticles_PdgId[igen]==-13:
                genmup_.append(gen)
            if len(genelp)>=1 and len(genelm)>=1:
                maxpt = max(genelp[0].Pt(),genelm[0].Pt())
                minpt = min(genelm[0].Pt(),genelp[0].Pt())
                hPt1VsPt2GenLeps.Fill(maxpt,minpt,weight) 
                m = (genelp[0]+genelm[0]).M()
                if m>0.001: fillth1(hDiElGenM, m, weight)
            if len(genmup_)>=1 and len(genmum)>=1:
                maxpt = max(genmup_[0].Pt(),genmum[0].Pt())
                minpt = min(genmup_[0].Pt(),genmum[0].Pt())
                hPt1VsPt2GenLeps.Fill(maxpt,minpt,weight) 
                m = (genmup_[0]+genmum[0]).M()
                if m>0.001: fillth1(hDiMuGenM, (genmup_[0]+genmum[0]).M(), weight)

        try: aveEtaGen = aveEtaGen*1.0/ngen
        except: pass
        #print ngen, 'aveEta(gen)', aveEtaGen
        #print len(genleps)
        for lep in genleps: 
            deta = abs(lep.Eta()-aveEtaGen)
            if deta<0.0001: print 'funny small one:', lep.Pt()
            if len(genleps)>1: 
                hDeltaEtaGen.Fill(deta)
        if len(genleps)>1:                 
            fillth1(hDeltaPhiGen, abs(genleps[0].DeltaPhi(genleps[1])),weight)
            
        fillth1(hDeltaEtaZstarJet, abs(jets[0].DeltaR(vec4EtaGen)),weight)
        fillth1(hDeltaPhiZstarJet, abs(vec4EtaGen.DeltaPhi(jets[0])), weight)
        if abs(vec4EtaGen.DeltaPhi(jets[0]))<0.001:
            print '====='
            for igen, gen in enumerate(some_freaky_chain.GenParticles):
                        if some_freaky_chain.GenParticles_PdgId[igen]==1000023: hPtChi.Fill(gen.Pt(),weight)
                        if not some_freaky_chain.GenParticles_ParentId[igen]==1000023: continue
                        #if not some_freaky_chain.GenParticles_Status[igen]==1: continue        
                        if some_freaky_chain.GenParticles_PdgId[igen]==1000022: 
                            continue
                        print some_freaky_chain.GenParticles_PdgId[igen]
        #print genleps[0].DeltaR(genleps[1]), abs(genleps[0].DeltaPhi(genleps[1])), abs(genleps[0].Eta()-genleps[1].Eta())
            
    #clear these:
    
    isotracks_plus.clear()
    isotracks_minus.clear()
    #print '======---='	
    for iiso, iso in enumerate(isocutlist):
        isotracks_plus[iso] = []
        isotracks_minus[iso] = []        
        isotracks[iso] = []
    ntrk = 0
    aveEtaRec = 0
    vec4EtaRec = TLorentzVector()
    for ichi, chi in enumerate(some_freaky_chain.chiCands):
    #try briefly to get back TTbar shape, then try with PFCandidates and well-done iso, then look at 
    #fireworks on these events, then start 2 new productions. a glimmer of hope before the productions 
    #would be nice.
        #print chi.Pt()
        if not abs(chi.Eta())<2.4: continue
        #if not chi.Pt()<15: continue
        if not chi.Pt()>2: continue
        if not some_freaky_chain.chiCands_trackQualityHighPurity[ichi]: continue
        if not abs(some_freaky_chain.chiCands_dzVtx[ichi])<0.05: continue        
        if not abs(some_freaky_chain.chiCands_dxyVtx[ichi])<0.03: continue
        #dphijet = dphiMinObjCol(chi, jets)        
        #if not dphijet>1: continue
        drjet = drMinObjCol(chi, jets)        
        if not drjet>1: continue
        ntrk+=1
        aveEtaRec+=chi.Eta()
        vec4EtaRec+=chi
        #if not some_freaky_chain.chiCands_trkMiniRelIso[ichi]<0.1: continue    	
        #if some_freaky_chain.chiCands_charge[ichi]==1: nchi_pos+=1
        #elif: nchi_neg+=1
        #print 'some_freaky_chain.chiCands_trkRelIso[ichi]', some_freaky_chain.chiCands_trkRelIso[ichi]
        for iiso, iso in enumerate(isocutlist):            
            if not (some_freaky_chain.chiCands_trkRelIso[ichi]<iso): continue        
            t1 = TLorentzVector()
            t1.SetPtEtaPhiE(some_freaky_chain.chiCands[ichi].Pt(),some_freaky_chain.chiCands[ichi].Eta(),some_freaky_chain.chiCands[ichi].Phi(),some_freaky_chain.chiCands[ichi].Energy())
            isotracks[iso].append(t1)
            if some_freaky_chain.chiCands_charge[ichi]>0: isotracks_plus[iso].append(t1)
            else: isotracks_minus[iso].append(t1)
    try:aveEtaRec = aveEtaRec*1.0/ntrk
    except: aveEtaRec = 999

    for track in isotracks[isocutlist[-1]]:
        hDeltaEtaTrack.Fill(abs(track.Eta()-aveEtaRec),weight)

    #print ntrk, 'aveEtaRec', aveEtaRec

    #if ngen*ntrk==0: continue
    #print '===========deltaEta scalar/vector ', abs(aveEtaRec-aveEtaGen)
    #print '===========deltaEta vector ', abs(vec4EtaRec.Eta()-vec4EtaGen.Eta())

    btags = some_freaky_chain.BTags 
    massOS.clear()
    massSS.clear()
    mass.clear()
    #print 'len(isotracks)', isocutlist[0], len(isotracks[isocutlist[0]])
    #if not len(isotracks[isocutlist[0]])==2: continue	
    #print 'passed'    
    #print isotracks

    for iiso, iso in enumerate(isocutlist):
        massOS[iso] = []
        for ip in range(len(isotracks_plus[iso])):
            for im in range(len(isotracks_minus[iso])):
                massOS[iso].append((isotracks_plus[iso][ip]+isotracks_minus[iso][im]).M())
        massSS[iso] = []
        for iip1 in range(len(isotracks_plus[iso])):
            for iip2 in range(iip1):
                massSS[iso].append((isotracks_plus[iso][iip1]+isotracks_plus[iso][iip2]).M())
        allvec = TLorentzVector()
        allvec.SetPxPyPzE(0,0,0,0)
        mass[iso] = []
        drtrackjet[iso] = []
        drtrackjetPtW[iso] = []
        for iip1 in range(len(isotracks[iso])):
            drtrackjet[iso].append(some_freaky_chain.Jets[0].DeltaR(isotracks[iso][iip1]))
            drtrackjetPtW[iso].append(isotracks[iso][iip1].Pt())
            if not abs(isotracks[iso][iip1].Eta()-aveEtaRec)<1.1: continue#vec4EtaGen.Eta()
            allvec+=isotracks[iso][iip1]
        mass[iso].append(allvec.M())                

    fv = [some_freaky_chain.HT,some_freaky_chain.MET,some_freaky_chain.NJets,abs(some_freaky_chain.DeltaPhi1),abs(some_freaky_chain.DeltaPhi2),abs(some_freaky_chain.DeltaPhi3),abs(some_freaky_chain.DeltaPhi4)]
    #print fv


    for selectionset in selectionsets:
        passes = True
        for i in range(len(fv)):
            #print i, selectionset
            passes = (fv[i]>=selectionsets[selectionset][i][0] and fv[i]<=selectionsets[selectionset][i][1])
            if not passes:
                #print 'failed', fv[i]
                break

        if not passes:
            continue


        fillth1(hHTdict[selectionset],fv[0],weight)
        fillth1(hMETdict[selectionset],fv[1],weight)
        fillth1(hNJetsdict[selectionset],fv[2],weight)
        fillth1(hBTagsdict[selectionset],btags,weight)
        fillth1(hDeltaPhi1dict[selectionset],fv[3],weight)
        fillth1(hDeltaPhi2dict[selectionset],fv[4],weight)
        fillth1(hQGLeadingJetdict[selectionset],qgj1,weight)
        #if selectionset=='monojet': print '=================filled met', hMETdict[selectionset].GetEntries()
        
        for iiso, iso in enumerate(isocutlist):
            thingy = selectionset+'_iso'+str(int(100*iso))  
            fillth1(hNIsoTracksdict[thingy],len(isotracks_plus[iso])+len(isotracks_minus[iso]),weight)
            for m in massOS[iso]:
                if m>0.0001: fillth1(h2OsTrackMassdict[thingy],m,weight)
            for m in massSS[iso]: 
                if m>0.0001: fillth1(h2SsTrackMassdict[thingy],m,weight) 
            for m in mass[iso]:
                if m>0.0001: fillth1(h2TrackMassdict[thingy],m,weight)
            for idr, dr in enumerate(drtrackjet[iso]): 
                fillth1(hDrTrackJet[thingy],dr,weight)                    
                fillth1(hDrTrackJetPtW[thingy],dr,drtrackjetPtW[iso][idr]*weight) 
                #if selectionset=='monojet' and iiso==len(isocutlist)-1: 
                #    print 'filled iso thingy', hDrTrackJet[thingy].GetEntries()

newfile.cd()
hHT.Write('hHt')
hHT_weighted.Write('hHt_weighted')


for selectionset in selectionsets:
    hMETdict[selectionset].Write()
    hHTdict[selectionset].Write()
    hNJetsdict[selectionset].Write()
    hBTagsdict[selectionset].Write()
    hDeltaPhi1dict[selectionset].Write()
    hDeltaPhi2dict[selectionset].Write()
    hQGLeadingJetdict[selectionset].Write()
    for iiso, iso in enumerate(isocutlist):    
        thingy = selectionset+'_iso'+str(int(100*iso))
        hNIsoTracksdict[thingy].Write()        
        h2OsTrackMassdict[thingy].Write()
        h2SsTrackMassdict[thingy].Write()    
        h2TrackMassdict[thingy].Write()    
        hDrTrackJet[thingy].Write()
        hDrTrackJetPtW[thingy].Write()        

hDiElGenM.Write()
hDiMuGenM.Write()
hPt1VsPt2GenLeps.Write()
hDeltaEtaTrack.Write()
hDeltaEtaGen.Write()
hDeltaPhiGen.Write()
hPtChi.Write()
hPtZstar.Write()
hDeltaEtaZstarJet.Write()
hDeltaPhiZstarJet.Write()
print 'just created', newfile.GetName()
newfile.Close()
