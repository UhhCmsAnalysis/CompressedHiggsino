#! /usr/bin/env python
from ROOT import *
from utils import *
import sys
from glob import glob
from DataFormats.FWLite import Events, Handle
#from trackmethods import *


verbose = False

gROOT.SetBatch()        # don't pop up canvases
gROOT.SetStyle('Plain') # white background

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example

try: filenames = sys.argv[1]
except: filenames = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_12_865833_step2_AODSIM_2*.root'

inputFiles = glob(filenames)

methodlib = []

def main():

	identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('_step2','').replace('_AODSIM','').replace('_*','').replace('*','')
	identifier+='nFiles'+str(len(inputFiles))

	fnew = TFile('histsEDM_'+identifier+'.root','recreate')
	events = Events(inputFiles)
	#events = Events('/uscms_data/d3/sbein/LongLiveTheChi/22Apr2017/pMSSM12_MCMC1_27_200970_step2_AODSIM.root')
	
	
	hGenChiEtaPos = TH1F("hGenChiEtaPos", "hGenChiEtaPos", 50, 0, 5)
	hGenChiEtaNeg = TH1F("hGenChiEtaNeg", "hGenChiEtaNeg", 50, 0, 5)
	hDrChipmTrack = TH1F("hDrChipmTrack", "hDrChipmTrack", 50, 0, .2)
	hDrChipmPFCand = TH1F("hDrChipmPFCand", "hDrChipmPFCand", 50, 0, .2)
	hDrRandomTrackTrack = TH1F("hDrRandomTrackTrack", "hDrRandomTrackTrack", 50, 0, .2)
	hChipmLabLengthAll = TH1F("hChipmLabLengthAll", "hChipmLabLengthAll", 50, -0.5, 3.5)
	hChipmLabLengthPass = TH1F("hChipmLabLengthPass", "hChipmLabLengthPass", 50, -0.5, 3.5)
	hDrMinVsChipmLabLength = TH2F("hDrMinVsChipmLabLength", "hDrMinVsChipmLabLength", 25, -1.0, 3.0, 20, 0, 0.2)
	hDrMinPFVsChipmLabLength = TH2F("hDrMinPFVsChipmLabLength", "hDrMinPFVsChipmLabLength", 25, -1.0, 3.0, 20, 0, 0.2)

	hChipmLabLengthVsEtaAll = TH2F("hChipmLabLengthVsEtaAll", "hChipmLabLengthVsEtaAll", 100, -2.4, 2.4, 40, .5, 3.5)
	hChipmLabLengthVsEta2MohPass = TH2F("hChipmLabLengthVsEta2MohPass", "hChipmLabLengthVsEta2MohPass", 100, -2.4, 2.4, 40, .5, 3.5)
	hChipmLabLengthVsEta5MohPass = TH2F("hChipmLabLengthVsEtaEta5MohPass", "hChipmLabLengthVsEtaEta5MohPass", 100, -2.4, 2.4, 40, .5, 3.5)
	hChipmLabLengthVsEtaPixelOnlyPass = TH2F("hChipmLabLengthVsEtaPixelOnlyPass", "hChipmLabLengthVsEtaPixelOnlyPass", 100, -2.4, 2.4, 40, .5, 3.5)
	hChipmLabLengthVsEtaPixelOnly0MohPass = TH2F("hChipmLabLengthVsEtaPixelOnly0MohPass", "hChipmLabLengthVsEtaPixelOnly0MohPass", 100, -2.4, 2.4, 40, .5, 3.5)	


	hSigDeDx = TH1F("hSigDeDx", "hSigDeDx", 100, 0, 25)
	histoStyler(hSigDeDx, kBlack)
	hBkgDeDx_ = TH1F("hBkgDeDx", "hBkgDeDx", 100, 0, 25)
	histoStyler(hBkgDeDx, kBlack)
	hSigIsolation = TH1F("hSigIsolation", "hSigIsolation", 100, 0, 2.5)
	histoStyler(hSigIsolation, kBlack)
	hBkgIsolation = TH1F("hBkgIsolation", "hBkgIsolation", 100, 0, 2.5)
	histoStyler(hBkgIsolation, kBlack)
	hSigMiniIsolation = TH1F("hSigMiniIsolation", "hSigMiniIsolation", 100, 0, 2.5)
	histoStyler(hSigMiniIsolation, kBlack)
	hBkgMiniIsolation = TH1F("hBkgMiniIsolation", "hBkgMiniIsolation", 100, 0, 2.5)
	histoStyler(hBkgMiniIsolation, kBlack)
	hSigChi2oNdof = TH1F("hSigChi2oNdof", "hSigChi2oNdof", 100, 0, 10)
	histoStyler(hSigChi2oNdof, kBlack)
	hBkgChi2oNdof = TH1F("hBkgChi2oNdof", "hBkgChi2oNdof", 100, 0, 10)
	histoStyler(hBkgChi2oNdof, kBlack)   

	hSigDeDxVsP = TH2F("hSigDeDxVsP", "hSigDeDxVsP", 50,0,1500, 40, 0, 20)
	hBkgDeDxVsP = TH2F("hBkgDeDxVsP", "hBkgDeDxVsP", 50,0,1500, 40, 0, 20)


	#handle_muons  = Handle ("std::vector<reco::Muon>")
	#label_muons = ('muons')

	#handle_tracks  = Handle ("vector<reco::TrackExtra>")
	handle_tracks  = Handle ("vector<reco::Track>")
	label_tracks = ('generalTracks')
	handle_pfcands  = Handle ("std::vector<reco::PFCandidate>")
	label_pfcands = ('particleFlow')
	dEdxTrackHandle = Handle ("edm::ValueMap<reco::DeDxData>");
	label_dEdXtrack = 'dedxHarmonic2'
	handle_genparticles  = Handle ("vector<reco::GenParticle>")
	label_genparticles = ('genParticlePlusGeant')


	liboffuturehists = {}
	listoffuturehists = []
	nevents = events.size()
	#nevents = 100

	for ievent, event in enumerate(events):
		if ievent>=nevents: break
		if ievent%20==0: print 'analyzing event %d of %d' % (ievent, nevents)
		#event.getByLabel (label_muons, handle_muons)
		event.getByLabel (label_tracks, handle_tracks)
		event.getByLabel (label_pfcands, handle_pfcands)
		event.getByLabel(label_dEdXtrack, dEdxTrackHandle)
		event.getByLabel (label_genparticles, handle_genparticles)


		# get the product
		#muons = handle_muons.product()
		tracks = handle_tracks.product()
		pfcands = handle_pfcands.product()
		dEdxTrack = dEdxTrackHandle.product()
		genparticles = handle_genparticles.product()

		#print '='*10
		if not (dEdxTrack.size()==tracks.size()): 
			print 'bad times'
			exit(0)

		listOfOffLimitFakes = []
		for gp in genparticles:
			#print dir(gp)
			#exit(0)
		
			if not (abs(gp.pdgId())==1000024 and gp.status()): continue

			if gp.eta()>0: hGenChiEtaPos.Fill(gp.eta())
			elif gp.eta()<0: hGenChiEtaNeg.Fill(-gp.eta())            
			if not (gp.pt()>15): continue
		
			try:
				log10decaylength = TMath.Log10(TMath.Sqrt(pow(gp.daughter(0).vx() - gp.vx(),2) + pow(gp.daughter(0).vy()-gp.vy(),2)))
			except: 
				print 'no daughters!'
				log10decaylength = -1
			chipmTlv = TLorentzVector()
			chipmTlv.SetPxPyPzE(gp.px(),gp.py(),gp.pz(),gp.energy())
			hChipmLabLengthAll.Fill(log10decaylength)

			fillth2(hChipmLabLengthVsEtaAll, gp.eta(), log10decaylength)
			#===#pfcandidates
			drmin = 10
			idx = -1
			eta = -11
			for ipfc, pfc in enumerate(pfcands):
				#print dir(pfc)
				pfcTlv = TLorentzVector()
				pfcTlv.SetPxPyPzE(pfc.px(), pfc.py(), pfc.pz(), pfc.pt())
				dr = pfcTlv.DeltaR(chipmTlv)
				if dr<drmin:
					drmin = dr
					idx = ipfc
			hDrMinPFVsChipmLabLength.Fill(log10decaylength, drmin)
			hDrChipmPFCand.Fill(drmin)
			#===#

			drmin = 10
			idx = -1
			eta = -11
			for itrack, track in enumerate(tracks):
				if not track.pt()>10: continue
				if track.numberOfValidHits()==0: continue
				if track.ndof()==0: continue                
				trkTlv = TLorentzVector()
				trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.pt())
				dr = trkTlv.DeltaR(chipmTlv)
				if dr < 0.05: listOfOffLimitFakes.append(itrack)
				if dr<drmin:
					drmin = dr
					idx = itrack

			if idx==-1: continue
			if verbose:
				print '+++++++++++++'
				print 'chargino pt=', gp.pt()
				print 'best matched pt = ', tracks[idx].pt()
				print 'drmin', drmin
			
			hDrMinVsChipmLabLength.Fill(log10decaylength, drmin)
			hDrChipmTrack.Fill(drmin)
			hitpattern = tracks[idx].hitPattern()
			if not (idx == reco.TrackRef(tracks, idx).index()):
				print 'highly unusual but no guaranteed concern'; exit(0)       
			if not (tracks[idx].numberOfValidHits() == hitpattern.numberOfValidHits()):
				print 'strangeness!'; exit(0)

			#dedx = dEdxTrack.get(reco.TrackRef(tracks, idx).index()).dEdx()
			try: dedx = dEdxTrack.get(idx).dEdx()
			except:
				dedx = 1
				print 'no dedx for index', idx
			chi2ondof = tracks[idx].chi2()/tracks[idx].ndof()
			if ievent==0: 
				#print dir(tracks[idx])
				#print methods
				a = 1
			if not drmin<0.02:  continue
			
			if not log10decaylength>0: continue
					
		
			hChipmLabLengthPass.Fill(log10decaylength)
			hSigDeDx.Fill(dedx)
			hSigDeDxVsP.Fill(gp.p(),dedx)
			hSigChi2oNdof.Fill(chi2ondof)    
			trkIso = calcTrackIso(track, tracks)
			trkJetIso = True#calcTrackJetIso(track, jets)
			trkMiniIso = calcMiniIso(track, tracks)
			if trkJetIso: hSigIsolation.Fill(trkIso)
			else: hSigIsolation.Fill(2.4)
			hSigMiniIsolation.Fill(trkMiniIso)
			
			moh = hitpattern.trackerLayersWithoutMeasurement(hitpattern.MISSING_OUTER_HITS)
			if hitpattern.numberOfValidTrackerHits()==hitpattern.numberOfValidPixelHits(): 
				fillth2(hChipmLabLengthVsEtaPixelOnlyPass, gp.eta(), log10decaylength)
				if moh==0: fillth2(hChipmLabLengthVsEtaPixelOnly0MohPass, gp.eta(), log10decaylength)
			if not moh>=2: continue
			fillth2(hChipmLabLengthVsEta2MohPass, gp.eta(), log10decaylength)
			if not moh>=5: continue
			fillth2(hChipmLabLengthVsEta5MohPass, gp.eta(), log10decaylength)
			                          
		for itrack, track in enumerate(tracks):
			if not track.pt()>10: continue
			if itrack in listOfOffLimitFakes: continue
			if track.ndof()==0: continue
			#dedx = dEdxTrack.get(reco.TrackRef(tracks, itrack).index()).dEdx()
			try: dedx = dEdxTrack.get(itrack).dEdx()
			except:
				dedx = 1
				print 'no bkg dedx for index', idx                
			hBkgDeDx_.Fill(dedx)
			hBkgDeDxVsP.Fill(track.p(),dedx)
			chi2ondof = track.chi2()/track.ndof()
			hBkgChi2oNdof.Fill(chi2ondof) 
			hitpattern = track.hitPattern()
			trkIso = calcTrackIso(track, tracks)
			trkJetIso = True#calcTrackJetIso(track, jets)
			trkMiniIso = calcMiniIso(track, tracks)
			if trkJetIso: hBkgIsolation.Fill(trkIso)
			else: hBkgIsolation.Fill(2.4)
			hBkgMiniIsolation.Fill(trkMiniIso)                        



	fnew.cd()

	hGenChiEtaPos.Write()
	hGenChiEtaNeg.Write()

	hSigIsolation.Write()
	hSigMiniIsolation.Write()
	hBkgIsolation.Write()
	hBkgMiniIsolation.Write()   
	
	hDrChipmTrack.Write()
	hDrChipmPFCand.Write()
	hDrRandomTrackTrack.Write()
	hChipmLabLengthAll.Write()
	hChipmLabLengthPass.Write()
	hDrMinVsChipmLabLength.Write()
	hDrMinPFVsChipmLabLength.Write()
	hSigDeDx.Write()            
	hBkgDeDx_.Write()
	hSigChi2oNdof.Write()            
	hBkgChi2oNdof.Write()
	hSigDeDxVsP.Write()
	hBkgDeDxVsP.Write()
	print 'just created', fnew.GetName()
	hChipmLabLengthVsEtaAll.Write()
	hChipmLabLengthVsEta2MohPass.Write()
	hChipmLabLengthVsEta5MohPass.Write()
	hChipmLabLengthVsEtaPixelOnlyPass.Write()	
	hChipmLabLengthVsEtaPixelOnly0MohPass.Write()
	fnew.Close()



main()
