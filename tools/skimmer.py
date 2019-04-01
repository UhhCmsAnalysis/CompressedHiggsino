import os
import sys
import numpy as np
import ROOT

#condier putting a copy of this over in CommonNtuples/NtupleMaker/CuttingEdge/...
try: infilename = sys.argv[1]
except: infilename = '/nfs/dust/cms/user/beinsam/CommonNtuples/MC_BSM/CompressedHiggsino/TChiZW/OfficialScan_hackfleisch/*.root'

    
def find_deltaR(v1, vList):
    min_deltaR = 999.9
    for i in vList:
        deltaR = v1.DeltaR(i)
        if deltaR < min_deltaR:
            min_deltaR = deltaR
    return min_deltaR


def find_m(vList):
    v1 = ROOT.TLorentzVector()
    for i in vList:
        v1 += i
    return v1.M()


def find_weight(chain, nEvtsDict, xSecDict):
    m = 0.0
    for i in range(chain.nMC):
        if chain.mcPID[i] == 1000021:    # MC particle no for gluino
            m = float(chain.mcMass[i])
            break

    n_events = 1
    for i, j in nEvtsDict.items():
        if m < i:
            n_events = j
            break

    return xSecDict[m] / n_events

if 'data' in infilename: isdata = True
else: isdata = False

sw = ROOT.TStopwatch()
sw.Start()

chain_in = ROOT.TChain('TreeMaker2/PreSelection')
chain_in.Add(infilename)
chain_in.Show(0)
n_entries = chain_in.GetEntries()
print 'Total entries: ' + str(n_entries)

shortname = infilename.split('/')[-1].strip()
shortname = shortname.replace('*','')
#file_out = ROOT.TFile('skim_' + shortname, 'recreate')
#dir_out = file_out.mkdir('TreeMaker2')
#dir_out.cd()
#tree_out = chain_in.CloneTree(0)#this is the one that's used
###tree_out = chain_in.CloneTree()    # Copy entire tree

# For MC with single cross section
# crossSection = 1.0

# For SUSY MC scan
n_eventsDict = {975: 150000, 9999: 20000}
crossSectionDict = {}
#with open('./SusyCrossSections13TevGluGlu.txt') as f_crossSection:
# for l in f_crossSection:
#     line = l.split()
#     crossSectionDict[float(line[0])] = float(line[1])

masspoints = []
fout_dict = {}
tout_dict = {}

verbosity = 100000
for j_entry in range(n_entries):
# for j_entry in range(100000):
    i_entry = chain_in.LoadTree(j_entry)
    if i_entry < 0:
        break
    nb = chain_in.GetEntry(j_entry)
    if nb <= 0:
        continue
    if j_entry % verbosity == 0:
        #print 'Processing entry ' + str(j_entry)
        print 'Processing entry %d of %d' % (j_entry, n_entries),'('+'{:.1%}'.format(1.0*j_entry/n_entries)+')'

    mChi20, mChi10 = -1,-1
    for igp, gp in enumerate(chain_in.GenParticles):
        if abs(chain_in.GenParticles_PdgId[igp])==1000024: mChi20 = round(gp.M(),1)
        if abs(chain_in.GenParticles_PdgId[igp])==1000022: mChi10 = round(gp.M(),1)
        #print igp, chain_in.GenParticles_PdgId[igp], gp.M(), '('+str(chain_in.GenParticles_ParentIdx[igp])+')'
        if mChi20>-1 and mChi10>-1: break

    if mChi20==-1 or mChi10==-1: 
        print 'something bad happened'
        exit(0)
    masspoint = (mChi20,mChi10)
    if not masspoint in masspoints:
        print 'new mass point', masspoint
        masspoints.append(masspoint)
        fout_dict[masspoint] = ROOT.TFile('TChiWZ_mNlsp%dmLsp%d'%(mChi20,mChi10)+'_'+shortname,'recreate')
        dir_out = fout_dict[masspoint].mkdir('TreeMaker2')
        dir_out.cd()        
        tout_dict[masspoint] = chain_in.CloneTree(0)

    #if isdata: weight[0] = 1.0
    #else: weight[0] = 1.0#find_weight(chain_in, n_eventsDict, crossSectionDict)    
    #fout_dict[masspoint].cd()
    tout_dict[masspoint].Fill()

for masspoint in fout_dict:
    fout_dict[masspoint].Write()
    fout_dict[masspoint].Close()

sw.Stop()
print 'Real time: ' + str(sw.RealTime() / 60.0) + ' minutes'
print 'CPU time:  ' + str(sw.CpuTime() / 60.0) + ' minutes'
