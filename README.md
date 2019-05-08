# Compressed higgsino
This is a package for analyzing events with higgsino-like LSPs on the NAF.
## Set up code

```
cmsrel CMSSW_10_1_0
cd CMSSW_10_1_0/src
cmsenv
git clone https://github.com/UhhCmsAnalysis/CompressedHiggsino.git
cd CompressedHiggsino/
mkdir output output/smallchunks output/mediumchunks output/bigchunks
mkdir jobs
mkdir pdfs
```
## run FWLite event analyzer script over signal AOD to generate histograms
### example:

run over a signal file
```
python tools/makeEfficiencyHists.py
```
this can also take the input file as an argument (wildcards accepted)

## extract histograms from root file to build the efficiency
### example:

make an efficiency plot
```
python tools/plotEfficiency.py histsEDM_pMSSM12_MCMC1_12_865833_25of100nFiles11.root
```
