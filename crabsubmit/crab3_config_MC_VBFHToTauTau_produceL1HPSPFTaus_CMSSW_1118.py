# TEMPLATE used for automatic script submission of multiple datasets

from WMCore.Configuration import Configuration
config = Configuration()

config.section_("General")
config.General.requestName = 'VBFHToTauTau_Old_DeepTauId_2stage_1118_20210602'
config.General.workArea = 'crablog_mc'
config.General.transferOutputs = True
config.General.transferLogs    = True

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
#config.JobType.psetName = '../test/produce_HLT_Taus_1stage_cfg.py'
config.JobType.psetName = '../test/produce_HLT_Taus_cfg.py'
config.JobType.allowUndistributedCMSSW = True
config.JobType.numCores = 4
config.JobType.maxMemoryMB = 8000

config.section_("Data")
config.Data.inputDataset = '/VBFHToTauTau_M125_14TeV_powheg_pythia8_correctedGridpack_tuneCP5/Phase2HLTTDRSummer20ReRECOMiniAOD-PU200_111X_mcRun4_realistic_T15_v1-v1/FEVT'
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
config.Data.outputDatasetTag = 'VBFHToTauTau_Old_DeepTauId_2stage_1118_20210602'

config.section_("Site")
config.Site.storageSite = 'T2_EE_Estonia'
#config.Site.whitelist = ["T2_EE_Estonia"]

