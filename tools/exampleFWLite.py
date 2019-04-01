#! /usr/bin/env python
from ROOT import *
from utils import *
import sys
from glob import glob
from DataFormats.FWLite import Events, Handle

gROOT.SetBatch() 
gROOT.SetStyle('Plain') 

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')
options.parseArguments()#twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example

try: inputFiles = options.inputFiles[0]
except: inputFiles = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_10_374794_step2_AODSIM_2of100.root'

#try: inputfile = sys.argv[1]
#except: inputfile = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_10_374794_step2_AODSIM_51of100.root'#sigpoint = 'pMSSM12_MCMC1_10_374794'#ctau 50 cm

def main():

    identifier = inputFiles[inputFiles.rfind('/')+1:].replace('.root','').replace('_AODSIM','').replace('_*','').replace('*','')
    
    fnew = TFile('example_'+identifier+'.root','recreate')
    
    filelist = glob(inputFiles)

    hNTracks = TH1F('hNTracks','hNTracks',30,0,1200)
    histoStyler(hNTracks,kRed+2)
    
    print 'filelist', filelist

    events = Events(filelist)
    #events = Events('/uscms_data/d3/sbein/LongLiveTheChi/22Apr2017/pMSSM12_MCMC1_27_200970_step2_AODSIM.root')

    handle_muons  = Handle ("std::vector<reco::Muon>")
    label_muons = ('muons')

    #handle_tracks  = Handle ("vector<reco::TrackExtra>")
    handle_tracks  = Handle ("vector<reco::Track>")
    label_tracks = ('generalTracks')
    handle_genparticles  = Handle ("vector<reco::GenParticle>")
    label_genparticles = ('genParticlePlusGeant')

 
    nevents = events.size()
    nevents = 100



    for ievent, event in enumerate(events):
        
        if ievent>=nevents: break
        if ievent%20==0: print 'analyzing event %d of %d' % (ievent, nevents)
            
        event.getByLabel (label_muons, handle_muons)
        event.getByLabel (label_tracks, handle_tracks)
        event.getByLabel (label_genparticles, handle_genparticles)
        
        muons = handle_muons.product()
        tracks = handle_tracks.product()

        charginoCandidates = []
        hNTracks.Fill(len(tracks))
        
        for track in tracks:
            if not track.pt()>55: continue
            if not abs(track.eta())<2.1: continue
            print 'high pT track', track.pt()
            
    fnew.cd()
    hNTracks.Write()
    print 'just created', fnew.GetName()
    fnew.Close()

            

main()
