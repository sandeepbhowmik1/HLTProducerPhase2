# TEMPLATE used for automatic script submission of multiple datasets

from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'TTToSemiLepton_Phase2HLTTDRSummer20ReRECOMiniAOD_CMSSW_1113_20201207'
config.General.workArea = 'crablog_mc'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '../test/produceL1HPSPFTaus_and_NNTaus_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.section_("Data")
config.Data.inputDataset = '/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT'
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
config.Data.outputDatasetTag = 'TTToSemiLepton_Phase2HLTTDRSummer20ReRECOMiniAOD_CMSSW_1113_20201207'

config.section_("Site")
config.Site.storageSite = 'T2_EE_Estonia'
#config.Site.whitelist = ["T2_EE_Estonia"]

