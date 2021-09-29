# TEMPLATE used for automatic script submission of multiple datasets

from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'QCDPt170to300_Phase2HLTTDRSummer20ReRECOMiniAOD_CMSSW_1117_20210211'
config.General.workArea = 'crablog_mc'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../test/produce_HLT_Taus_and_L1Taus_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.section_("Data")
config.Data.inputDataset = '/QCD_Pt_170to300_TuneCP5_14TeV_pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/GEN-SIM-DIGI-RAW-MINIAOD'
#Data.useParent = True
config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
#config.Data.splitting = 'FileBased'
#config.Data.unitsPerJob = 1000
config.Data.splitting        = 'EventAwareLumiBased'
config.Data.unitsPerJob      = 100
config.Data.totalUnits = -1 #number of event
config.Data.outLFNDirBase = '/store/user/sbhowmik'
config.Data.publication = False
config.Data.outputDatasetTag = 'QCDPt170to300_Phase2HLTTDRSummer20ReRECOMiniAOD_CMSSW_1117_20210211'

config.section_("Site")
config.Site.storageSite = 'T2_EE_Estonia'
#config.Site.whitelist = ["T2_EE_Estonia"]

