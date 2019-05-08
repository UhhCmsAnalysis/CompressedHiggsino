#! /usr/bin/env python

from ROOT import gROOT, TFile, TH1F, TMath, TLorentzVector, TH2F
from utils import *
import sys
from glob import glob
from DataFormats.FWLite import Events, Handle
from numpy.distutils.misc_util import gpaths


gROOT.SetBatch()        # don't pop up canvases
gROOT.SetStyle('Plain') # white background

# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideAboutPythonConfigFile#VarParsing_Example

try: filenames = sys.argv[1]
except: filenames = '/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/aodsim/higgsino_mu100_dm0.51Chi20Chi.m_AODSIM_*.root'

# /nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/aodsim/higgsino_mu100_dm0.51Chi20Chi.m_AODSIM_*.root
# /nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/aodsim/higgsino_mu100_dm0.66Chi20Chi.m_AODSIM_*.root
# /nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/M1M2Scan/aodsim/higgsino_mu100_dm0.86Chi20Chi.m_AODSIM_*.root
# /nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_37_569964_step2_AODSIM_*.root # dM = 0.46 GeV
# /nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_22_237840_step2_AODSIM_*.root # dM = 0.52 GeV
# /nfs/dust/cms/user/beinsam/LongLiveTheChi/aodsim/smallchunks/pMSSM12_MCMC1_12_865833_step2_AODSIM_*.root # dM = 20 GeV

inputFiles = glob(filenames)


def main():

	identifier = inputFiles[0][inputFiles[0].rfind('/')+1:].replace('.root','').replace('_step2','').replace('_AODSIM','').replace('_1*','').replace('*','')
	identifier+='nFiles'+str(len(inputFiles))
	
	print(identifier)

	fnew = TFile('histsEDM_'+identifier+'.root','recreate')
	events = Events(inputFiles)
	
	
	# GEN chi20 histos
	
	hChi20StatusBefore = TH1F("hChi20StatusBefore", "hChi20StatusBefore", 200, 0., 200.)
	hChi20StatusAfter = TH1F("hChi20StatusAfter", "hChi20StatusAfter", 200, 0., 200.)
	
	hPdgIdDaughters = TH1F("hPdgIdDaughters", "hPdgIdDaughters", 50, 0., 50.)
	hPdgIdDaughtersSUSY = TH1F("hPdgIdDaughtersSUSY", "hPdgIdDaughtersSUSY", 50, 0., 50.)

	hPtChi20Before = TH1F("hPtChi20Before", "hPtChi20Before", 150, 0, 1500.)
	hPtChi20After = TH1F("hPtChi20After", "hPtChi20After", 150, 0, 1500.)
	
	hChi20LogLabLengthVsPtLepton = TH2F("hChi20LogLabLengthVsPtLepton", "hChi20LogLabLengthVsPtLepton", 50, -2.0, 0., 150, 0., 1.5)
	
	
	# GEN lepton finding histos
	
	hLeptonsFound = TH1F("hLeptonsFound", "hLeptonsFound", 3, 0., 3.)
	
	hPtZgamma = TH1F("hPtZgamma", "hPtZgamma", 50, 0, 5.)
	
	hPtLepton = TH1F("hPtLepton", "hPtLepton", 50, 0, 5.)
	hEtaLepton = TH1F("hEtaLepton", "hEtaLepton", 100, -5., 5.)
	hLogTransverseDistLepton = TH1F("hLogTransverseDistLepton", "hLogTransverseDistLepton", 100, -3., 3.)
	
	hDrLeptonLepton = TH1F("hDrLeptonLepton", "hDrLeptonLepton", 100, 0., 5.)
	hLogDrLeptonLepton = TH1F("hLogDrLeptonLepton", "hLogDrLeptonLepton", 100, -5., 1.)
	
	hInvMassLepton = TH1F("hInvMassLepton", "hInvMassLepton", 100, 0, 5.)
	hLogInvMassLepton = TH1F("hLogInvMassLepton", "hLogInvMassLepton", 100, -5., 1.)
	
	
	# lepton matching histos
	
	hDrLeptonPfc = TH1F("hDrLeptonPfc", "hDrLeptonPfc", 100, 0, 1.)
	hDrLeptonTrack = TH1F("hDrLeptonTrack", "hDrLeptonTrack", 100, 0, 1.)	
	
	hSamePfcMatched = TH1F("hSamePfcMatched", "hSamePfcMatched", 2, 0., 2.)
	hParticleIdPfcMatched = TH1F("hParticleIdPfcMatched", "hParticleIdPfcMatched", 10, 0., 10.)
	
	hPtPfcMatched = TH1F("hPtPfcMatched", "hPtPfcMatched", 50, 0, 5.)
	hPtTrackMatched = TH1F("hPtTrackMatched", "hPtTrackMatched", 50, 0, 5.)


	# efficiency histos

	hChi20LabLengthAll = TH1F("hChi20LabLengthAll", "hChi20LabLengthAll", 50, 0., 1.)
	hChi20LabLengthPass = TH1F("hChi20LabLengthPass", "hChi20LabLengthPass", 50, 0., 1.)
	
	hChi20LogLabLengthAll = TH1F("hChi20LogLabLengthAll", "hChi20LogLabLengthAll", 50, -2.0, 0.)
	hChi20LogLabLengthPass = TH1F("hChi20LogLabLengthPass", "hChi20LogLabLengthPass", 50, -2.0, 0.)	

	hChi20LabLengthPfcMatchedAll = TH1F("hChi20LabLengthPfcMatchedAll", "hChi20LabLengthPfcMatchedAll", 50, 0., 1.)
	hChi20LabLengthPfcMatchedPass = TH1F("hChi20LabLengthPfcMatchedPass", "hChi20LabLengthPfcMatchedPass", 50, 0., 1.)
	
	hChi20LogLabLengthPfcMatchedAll = TH1F("hChi20LogLabLengthPfcMatchedAll", "hChi20LogLabLengthPfcMatchedAll", 50, -2.0, 0.)
	hChi20LogLabLengthPfcMatchedPass = TH1F("hChi20LogLabLengthPfcMatchedPass", "hChi20LogLabLengthPfcMatchedPass", 50, -2.0, 0.)
	
	hChi20LabLengthOnePfcMatchedAll = TH1F("hChi20LabLengthOnePfcMatchedAll", "hChi20LabLengthOnePfcMatchedAll", 50, 0., 1.)
	hChi20LabLengthOnePfcMatchedPass = TH1F("hChi20LabLengthOnePfcMatchedPass", "hChi20LabLengthOnePfcMatchedPass", 50, 0., 1.)
	
	hChi20LogLabLengthOnePfcMatchedAll = TH1F("hChi20LogLabLengthOnePfcMatchedAll", "hChi20LogLabLengthOnePfcMatchedAll", 50, -2.0, 0.)
	hChi20LogLabLengthOnePfcMatchedPass = TH1F("hChi20LogLabLengthOnePfcMatchedPass", "hChi20LogLabLengthOnePfcMatchedPass", 50, -2.0, 0.)	
	
	hPtLeptonAll = TH1F("hPtLeptonAll", "hPtLeptonAll", 30, 0, 3.)
	hPtLeptonPass = TH1F("hPtLeptonPass", "hPtLeptonPass", 30, 0, 3.)
	
	hPtLeptonPfcMatchedAll = TH1F("hPtLeptonPfcMatchedAll", "hPtLeptonPfcMatchedAll", 30, 0, 3.)
	hPtLeptonPfcMatchedPass = TH1F("hPtLeptonPfcMatchedPass", "hPtLeptonPfcMatchedPass", 30, 0, 3.)
	
	hPtLeptonPfcMatchedCorrectIdAll = TH1F("hPtLeptonPfcMatchedCorrectIdAll", "hPtLeptonPfcMatchedCorrectIdAll", 30, 0, 3.)
	hPtLeptonPfcMatchedCorrectIdPass = TH1F("hPtLeptonPfcMatchedCorrectIdPass", "hPtLeptonPfcMatchedCorrectIdPass", 30, 0, 3.)

	hPtAllLeptonPfcMatchedCorrectIdAll = TH1F("hPtAllLeptonPfcMatchedCorrectIdAll", "hPtAllLeptonPfcMatchedCorrectIdAll", 30, 0, 3.)
	hPtAllLeptonPfcMatchedCorrectIdPass = TH1F("hPtAllLeptonPfcMatchedCorrectIdPass", "hPtAllLeptonPfcMatchedCorrectIdPass", 30, 0, 3.)

	
	handle_tracks = Handle("vector<reco::Track>")
	label_tracks = ('generalTracks')
	handle_pfcands = Handle("std::vector<reco::PFCandidate>")
	label_pfcands = ('particleFlow')
	handle_genparticles = Handle("vector<reco::GenParticle>")
# 	label_genparticles = ('genParticlePlusGeant')
	label_genparticles = ('genParticles')


	nevents = events.size()
# 	nevents = 100
	
	allChi20s = 0.
	passedTrackMatched = 0.
	passedPfcMatched = 0.
	passedOnePfcMatched = 0.

	for ievent, event in enumerate(events):
		
		if ievent >= nevents: break
		if ievent % 20 == 0: print('analyzing event %d of %d' % (ievent, nevents))
		
		event.getByLabel(label_tracks, handle_tracks)
		event.getByLabel(label_pfcands, handle_pfcands)
		event.getByLabel(label_genparticles, handle_genparticles)

		tracks = handle_tracks.product()
		pfcands = handle_pfcands.product()
		genparticles = handle_genparticles.product()

		for gp in genparticles:

			if not (abs(gp.pdgId())==11 or abs(gp.pdgId())==13): continue

			gpTlv = TLorentzVector()
			gpTlv.SetPxPyPzE(gp.px(), gp.py(), gp.pz(), gp.energy())

			hPtAllLeptonPfcMatchedCorrectIdAll.Fill(gp.pt())

			drmin = 10
			idx = -1
			for ipfc, pfc in enumerate(pfcands):
				pfcTlv = TLorentzVector()
				pfcTlv.SetPxPyPzE(pfc.px(), pfc.py(), pfc.pz(), pfc.energy())
				
				dr = pfcTlv.DeltaR(gpTlv)
				if dr < drmin:
					drmin = dr
					idx = ipfc
			
			if drmin < 0.02 and pfcands[idx].pdgId() == gp.pdgId():
				hPtAllLeptonPfcMatchedCorrectIdPass.Fill(gp.pt())
				
		for gp in genparticles:
			
			if not (abs(gp.pdgId())==1000023): continue	
			
			decaylength = TMath.Sqrt(pow(gp.vx() - gp.daughter(0).vx(),2) + pow(gp.vy() - gp.daughter(0).vy(),2))
			logdecaylength = TMath.Log10(decaylength)
			
			hChi20StatusBefore.Fill(gp.status())
			hPtChi20Before.Fill(gp.pt())
			hLeptonsFound.Fill(0)
			
			if not decaylength > 0: continue
			
			
			### GEN lepton finding ###
			
			zgammaDaughterFound = False
			oneleptonDaughterFound = False
			twoleptonDaughtersFound = False
			
			lepton1 = None
			lepton2 = None
			
			for i in range(gp.numberOfDaughters()):
				pdgIdDaughter = abs(gp.daughter(i).pdgId())
				
				if pdgIdDaughter > 1000000: hPdgIdDaughtersSUSY.Fill(pdgIdDaughter % 1000000)
				else: hPdgIdDaughters.Fill(pdgIdDaughter)
					
				if pdgIdDaughter==22 or pdgIdDaughter==23:
					zgammaDaughterFound = True
					zgamma = gp.daughter(i)
					hPtZgamma.Fill(zgamma.pt())
					
				if pdgIdDaughter==11 or pdgIdDaughter==13:
					if oneleptonDaughterFound:
						twoleptonDaughtersFound = True
						hLeptonsFound.Fill(1)
						lepton2 = gp.daughter(i)
						hPtZgamma.Fill(TMath.Sqrt(pow(lepton1.px() + lepton2.px(),2) + pow(lepton1.py() + lepton2.py(),2)))
					else:
						oneleptonDaughterFound = True
						lepton1 = gp.daughter(i)
						
				if zgammaDaughterFound or twoleptonDaughtersFound: break
					
			if zgammaDaughterFound and not oneleptonDaughterFound:

				for i in range(zgamma.numberOfDaughters()):
					pdgIdDaughter = abs(zgamma.daughter(i).pdgId())
					
					if pdgIdDaughter==11 or pdgIdDaughter==13:
						if oneleptonDaughterFound:
							twoleptonDaughtersFound = True
							hLeptonsFound.Fill(2)
							lepton2 = zgamma.daughter(i)
						else:
							oneleptonDaughterFound = True
							lepton1 = zgamma.daughter(i)
													
					if twoleptonDaughtersFound: break
					
			if not twoleptonDaughtersFound: continue
			if not lepton1.charge() * lepton2.charge() < 0: continue
						
			hChi20StatusAfter.Fill(gp.status())
			hPtChi20After.Fill(gp.pt())
			
			
			### fill efficiency histos for 'All' ###
			
			allChi20s += 1
			
			hChi20LabLengthAll.Fill(decaylength)
			hChi20LabLengthPfcMatchedAll.Fill(decaylength)
			hChi20LabLengthOnePfcMatchedAll.Fill(decaylength)
			
			hChi20LogLabLengthAll.Fill(logdecaylength)
			hChi20LogLabLengthPfcMatchedAll.Fill(logdecaylength)
			hChi20LogLabLengthOnePfcMatchedAll.Fill(logdecaylength)
			
			
			### fill GEN lepton histos ###
			
			lepton1Tlv = TLorentzVector()
			lepton1Tlv.SetPxPyPzE(lepton1.px(),lepton1.py(),lepton1.pz(),lepton1.energy())
			lepton2Tlv = TLorentzVector()
			lepton2Tlv.SetPxPyPzE(lepton2.px(),lepton2.py(),lepton2.pz(),lepton2.energy())
			
			hDrLeptonLepton.Fill(lepton1Tlv.DeltaR(lepton2Tlv))
			hLogDrLeptonLepton.Fill(TMath.Log10(lepton1Tlv.DeltaR(lepton2Tlv)))
			
			hInvMassLepton.Fill((lepton1Tlv + lepton2Tlv).M())
			hLogInvMassLepton.Fill(TMath.Log10((lepton1Tlv + lepton2Tlv).M()))
			
			
			### lepton matching ###
					
			oneLeptonMatched = False
			twoLeptonsMatched = False
			oneLeptonPfcMatched = False
			twoLeptonsPfcMatched = False
			
			lepton1Matched = False
			lepton2Matched = False
			lepton1PfcMatched = False
			lepton2PfcMatched = False
			
			lepton1matchedPfcIdx = -1
			lepton2matchedPfcIdx = -1
			
			for lepton in (lepton1, lepton2):
				hLogTransverseDistLepton.Fill(TMath.Log10(TMath.Sqrt(pow(lepton.vx(),2) + pow(lepton.vy(),2))))
								
				leptonTlv = TLorentzVector()
				leptonTlv.SetPxPyPzE(lepton.px(),lepton.py(),lepton.pz(),lepton.energy())
				
				### fill GEN lepton histos ###
				hEtaLepton.Fill(lepton.eta())
				hPtLepton.Fill(lepton.pt())
				hChi20LogLabLengthVsPtLepton.Fill(logdecaylength, lepton.pt())
				
				### fill efficiency histos for 'All' ###
				hPtLeptonAll.Fill(lepton.pt())
				hPtLeptonPfcMatchedAll.Fill(lepton.pt())
				hPtLeptonPfcMatchedCorrectIdAll.Fill(lepton.pt())
	
				### matching to PFcandidates ###
				drmin = 10
				idx = -1
				for ipfc, pfc in enumerate(pfcands):
					pfcTlv = TLorentzVector()
					pfcTlv.SetPxPyPzE(pfc.px(), pfc.py(), pfc.pz(), pfc.energy())
					
					dr = pfcTlv.DeltaR(leptonTlv)
					if dr < drmin:
						drmin = dr
						idx = ipfc

				if not idx == -1:
					hPtPfcMatched.Fill(pfcands[idx].pt())
					hDrLeptonPfc.Fill(drmin)
				
					if drmin < 0.02:
						hPtLeptonPfcMatchedPass.Fill(lepton.pt())
						hParticleIdPfcMatched.Fill(pfcands[idx].particleId())
						
						if pfcands[idx].pdgId() == lepton.pdgId():
							hPtLeptonPfcMatchedCorrectIdPass.Fill(lepton.pt())
						
						if lepton == lepton1:
							lepton1PfcMatched = True
							lepton1matchedPfcIdx = idx
						if lepton == lepton2:
							lepton2PfcMatched = True
							lepton2matchedPfcIdx = idx
						
						if oneLeptonPfcMatched: twoLeptonsPfcMatched = True
						else: oneLeptonPfcMatched = True
	
				### matching to tracks ###
				drmin = 10
				idx = -1
				for itrack, track in enumerate(tracks):
					if track.numberOfValidHits()==0: continue
					if track.ndof()==0: continue
					
					trkTlv = TLorentzVector()
					trkTlv.SetPxPyPzE(track.px(), track.py(), track.pz(), track.p())
					
					dr = trkTlv.DeltaR(leptonTlv)
					if dr < drmin:
						drmin = dr
						idx = itrack
						
				if not idx == -1:
					hPtTrackMatched.Fill(tracks[idx].pt())
					hDrLeptonTrack.Fill(drmin)
	
					if drmin < 0.02:
						hPtLeptonPass.Fill(lepton.pt())
						
						if lepton == lepton1:
							lepton1Matched = True
						if lepton == lepton2:
							lepton2Matched = True
							
						if oneLeptonMatched: twoLeptonsMatched = True
						else: oneLeptonMatched = True
			
			
			### fill efficiency histos for 'Pass' ###
			
			if twoLeptonsMatched:
				
				passedTrackMatched += 1
				
				hChi20LabLengthPass.Fill(decaylength)
				hChi20LogLabLengthPass.Fill(logdecaylength)
				
			if twoLeptonsPfcMatched:
				
				passedPfcMatched += 1
				
				hChi20LabLengthPfcMatchedPass.Fill(decaylength)
				hChi20LogLabLengthPfcMatchedPass.Fill(logdecaylength)
				
				if lepton1matchedPfcIdx == lepton2matchedPfcIdx:
					hSamePfcMatched.Fill(1)
				else:
					hSamePfcMatched.Fill(0)
					
			if (lepton1Matched and lepton2PfcMatched) or \
				(lepton1PfcMatched and lepton2Matched) or \
				(lepton1PfcMatched and lepton2PfcMatched):
				
				passedOnePfcMatched += 1
				
				hChi20LabLengthOnePfcMatchedPass.Fill(decaylength)
				hChi20LogLabLengthOnePfcMatchedPass.Fill(logdecaylength)


	print('efficiencies:')
	print('both track matched: ', passedTrackMatched/allChi20s)
	print('both Pfc matched: ', passedPfcMatched/allChi20s)
	print('at least one Pfc matched: ', passedOnePfcMatched/allChi20s)
	
	
	### write histos ###					
	
	fnew.cd()
	
	# GEN chi20 histos
	hChi20StatusBefore.Write()
	hChi20StatusAfter.Write()	
	hPdgIdDaughters.Write()
	hPdgIdDaughtersSUSY.Write()
	hPtChi20Before.Write()
	hPtChi20After.Write()	
	hChi20LogLabLengthVsPtLepton.Write()
		
	# GEN lepton finding histos
	hLeptonsFound.Write()
	hPtZgamma.Write()	
	hPtLepton.Write()
	hEtaLepton.Write()
	hLogTransverseDistLepton.Write()
	hDrLeptonLepton.Write()
	hLogDrLeptonLepton.Write()
	hInvMassLepton.Write()
	hLogInvMassLepton.Write()
		
	# lepton matching histos	
	hDrLeptonPfc.Write()
	hDrLeptonTrack.Write()	
	hSamePfcMatched.Write()
	hParticleIdPfcMatched.Write()
	hPtPfcMatched.Write()
	hPtTrackMatched.Write()

	# efficiency histos
	hChi20LabLengthAll.Write()
	hChi20LabLengthPass.Write()	
	hChi20LogLabLengthAll.Write()
	hChi20LogLabLengthPass.Write()
	hChi20LabLengthPfcMatchedAll.Write()
	hChi20LabLengthPfcMatchedPass.Write()	
	hChi20LogLabLengthPfcMatchedAll.Write()
	hChi20LogLabLengthPfcMatchedPass.Write()
	hChi20LabLengthOnePfcMatchedAll.Write()
	hChi20LabLengthOnePfcMatchedPass.Write()
	hChi20LogLabLengthOnePfcMatchedAll.Write()
	hChi20LogLabLengthOnePfcMatchedPass.Write()
	hPtLeptonAll.Write()
	hPtLeptonPass.Write()	
	hPtLeptonPfcMatchedAll.Write()
	hPtLeptonPfcMatchedPass.Write()
	hPtLeptonPfcMatchedCorrectIdAll.Write()
	hPtLeptonPfcMatchedCorrectIdPass.Write()
	hPtAllLeptonPfcMatchedCorrectIdAll.Write()
	hPtAllLeptonPfcMatchedCorrectIdPass.Write()

	print ('just created ' + fnew.GetName())
	fnew.Close()

main()
