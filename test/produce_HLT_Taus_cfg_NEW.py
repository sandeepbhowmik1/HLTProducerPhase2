# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: Phase2 -s HLT:75e33 --processName=HLTX --conditions auto:phase2_realistic_T21 --geometry Extended2026D77 --era Phase2C11I13M9 --eventcontent FEVTDEBUGHLT --filein=/store/relval/CMSSW_12_3_0_pre5/RelValTTbar_14TeV/GEN-SIM-RECO/123X_mcRun4_realistic_v4_2026D77noPU-v1/10000/0311b450-0085-4f1a-bf35-dc06c4c2bba7.root -n 10 --nThreads 1 --no_exec
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C11I13M9_cff import Phase2C11I13M9

process = cms.Process('HLTX',Phase2C11I13M9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D77Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.load('HLTrigger.Configuration.HLT_75e33_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#--------------------------------------------------------------------------------
# CV: switch between offline-like and Pixel vertices

vertices = "OfflineVertices"
#vertices = "OnlineVertices"
#vertices = "OnlineVerticesTrimmed"

srcVertices = None
srcBeamSpot = None
if vertices == "OfflineVertices":
    srcVertices = 'offlinePrimaryVertices'
    srcBeamSpot = 'offlineBeamSpot'
elif vertices == "OnlineVertices":
    srcVertices = 'hltPhase2PixelVertices'
    srcBeamSpot = 'hltOnlineBeamSpot'
elif vertices == "OnlineVerticesTrimmed":
    srcVertices = 'hltPhase2TrimmedPixelVertices'
    srcBeamSpot = 'hltOnlineBeamSpot'
else:
    raise ValueError("Invalid configuration parameter vertices = '%s' !!" % vertices)

# CV: enable/disable L1 emulator
#runL1Emulator = False
runL1Emulator = True
#--------------------------------------------------------------------------------

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/relval/CMSSW_12_3_0_pre5/RelValTTbar_14TeV/GEN-SIM-RECO/123X_mcRun4_realistic_v4_2026D77noPU-v1/10000/0311b450-0085-4f1a-bf35-dc06c4c2bba7.root'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    accelerators = cms.untracked.vstring('*'),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Phase2 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.RECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('NTuple_produce_HLT_Taus.root'),
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep *_ak4GenJets*_*_*',                   ## PRESENT ONLY IN RAW
        'keep *_hltGtStage2Digis*_*_*',             ## PRESENT ONLY IN RAW
        'keep *_hltTriggerSummaryRAW*_*_*',         ## PRESENT ONLY IN RAW
        'keep *_ak4PFJetsCorrected*_*_*',           ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_hlt*Tau*_*_*',                      ## PRODUCED BY addHLTPFTaus FUNCTION BELOW
        'keep *_particleFlowTmp_*_*',               ## KEEP REFERENCE TO reco::PFCandidate COLLECTION GIVEN AS INPUT TO addHLTPFTaus FUNCTION
        'keep *_muons1stStep_*_*',                  ## KEEP REFERENCE TO reco::Track COLLECTIONS FOR ALL TYPES OF MUONS USED AS INPUT TO PARTICLE-FLOW ALGORITHM
        'keep *_globalMuons_*_*',                   ## KEEP REFERENCE TO reco::Track COLLECTIONS FOR ALL TYPES OF MUONS USED AS INPUT TO PARTICLE-FLOW ALGORITHM
        'keep *_standAloneMuons_*_*',               ## KEEP REFERENCE TO reco::Track COLLECTIONS FOR ALL TYPES OF MUONS USED AS INPUT TO PARTICLE-FLOW ALGORITHM
        'keep *_tevMuons_*_*',                      ## KEEP REFERENCE TO reco::Track COLLECTIONS FOR ALL TYPES OF MUONS USED AS INPUT TO PARTICLE-FLOW ALGORITHM
        'keep *_electronGsfTracks_*_*',             ## KEEP REFERENCE TO reco::GsfTrack COLLECTION FOR ELECTRONS USED AS INPUT TO PARTICLE-FLOW ALGORITHM
        'keep *_generalTracks_*_*',                 ## KEEP REFERENCE TO reco::Track COLLECTION GIVEN AS INPUT TO addHLTPFTaus FUNCTION
        'keep *_offlinePrimaryVertices_*_*',        ## KEEP REFERENCE TO reco::Vertex COLLECTION GIVEN AS INPUT TO addHLTPFTaus FUNCTION 
        'keep *_hltPhase2PixelVertices_*_*',        ## PRODUCED BELOW
        'keep *_hltPhase2TrimmedPixelVertices_*_*', ## PRODUCED BELOW
        'keep *_hltKT6PFJets_*_*',                  ## PRODUCED BELOW
        'keep *_hltPFMET*_*_*',                     ## PRODUCED BELOW
        'keep *_hltPuppiMET*_*_*',                  ## PRODUCED BELOW
        'keep *_hltPackedPFCandidates*_*_*',        ## PRODUCED BELOW
        'keep *_prunedGenParticles_*_*',            ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_ak4GenJets_*_*',                    ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_ak8GenJets_*_*',                    ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_slimmedGenJets__*',                 ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_slimmedTaus_*_*',                   ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_slimmedJets_*_*',                   ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_packedPFCandidates_*_*',            ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_slimmedAddPileupInfo_*_*',          ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_addPileupInfo_*_*',                 ## PRESENT ONLY IN RAW
        'keep *_offlineSlimmedPrimaryVertices_*_*', ## PRESENT ONLY IN MINIAOD/RECO
        'keep *_generatorSmeared_*_*',              ## CV: ALLOWS TO PRODUCE FULL COLLECTION OF genParticles FOR DEBUGGING PURPOSES 
        'keep *_generator_*_*',                     ## CV: NEEDED TO MAKE PTHAT PLOTS FOR QCD MULTIJET MC SAMPLES
        'keep *_*BeamSpot*_*_*',                    ## Need the beamspot
    )

)

# Additional output definition

# Other statements
from HLTrigger.Configuration.CustomConfigs import ProcessName
process = ProcessName(process)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T21', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
#process.reconstruction_step = cms.Path()
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)


# Schedule definition
# process.schedule imported from cff in HLTrigger.Configuration
#process.schedule.extend([process.endjob_step,process.FEVTDEBUGHLToutput_step])
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.endjob_step,process.RECOoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from HLTrigger.Configuration.customizeHLTforMC
from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 

#call to customisation function customizeHLTforMC imported from HLTrigger.Configuration.customizeHLTforMC
process = customizeHLTforMC(process)

# End of customisation functions

#Setup FWK for multithreaded
process.options.numberOfThreads=cms.untracked.uint32(4)
process.options.numberOfStreams=cms.untracked.uint32(4)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(1)

from HLTrigger.Configuration.HLT_75e33.modules.particleFlowSuperClusterHGCal_cfi import particleFlowSuperClusterHGCal
process.reconstruction_step += process.particleFlowSuperClusterHGCal

#--------------------------------------------------------------------------------
# CV: add HLT tau reconstruction
process.taucustomreco = cms.Sequence()

# run HLT tau reconstruction
from HLTrigger.Phase2HLTPFTaus.tools.addHLTPFTaus import addHLTPFTaus
srcPFCandidates = "particleFlowTmp"
for algorithm in [ "hps", "shrinking-cone" ]:
  for isolation_maxDeltaZOption in [ "primaryVertex", "leadTrack" ]:
    for isolation_minTrackHits in [ 3, 5, 8 ]:

      suffix = "%iHits" % isolation_minTrackHits
      isolation_maxDeltaZ            = None
      isolation_maxDeltaZToLeadTrack = None
      if isolation_maxDeltaZOption == "primaryVertex":
        isolation_maxDeltaZ            =  0.15 # value optimized for offline tau reconstruction at higher pileup expected during LHC Phase-2
        isolation_maxDeltaZToLeadTrack = -1.   # disabled
        suffix += "MaxDeltaZ"
      elif isolation_maxDeltaZOption == "leadTrack":
        isolation_maxDeltaZ            = -1.   # disabled
        isolation_maxDeltaZToLeadTrack =  0.15 # value optimized for offline tau reconstruction at higher pileup expected during LHC Phase-2
        suffix += "MaxDeltaZToLeadTrack"
      else:
        raise ValueError("Invalid parameter isolation_maxDeltaZOption = '%s' !!" % isolation_maxDeltaZOption)
      if srcVertices == "offlinePrimaryVertices":
        suffix += "WithOfflineVertices"
      elif srcVertices == "hltPhase2PixelVertices":
        suffix += "WithOnlineVertices"
      elif srcVertices == "hltPhase2TrimmedPixelVertices":
        suffix += "WithOnlineVerticesTrimmed"
      else:
        raise ValueError("Invalid parameter srcVertices = '%s' !!" % srcVertices)

      pftauSequence = addHLTPFTaus(process, algorithm,
        srcPFCandidates, srcVertices, srcBeamSpot,
        isolation_maxDeltaZ, isolation_maxDeltaZToLeadTrack, isolation_minTrackHits,
        suffix)
      process.taucustomreco += pftauSequence

process.reconstruction_step += process.taucustomreco

hlt_pfTauLabel = 'HpsPFTau'
hlt_srcVertices = 'offlinePrimaryVertices'
suffix = '8HitsMaxDeltaZWithOfflineVertices'
from HLTrigger.Phase2HLTPFTaus.tools.addDeepTauDiscriminator import addDeepTauDiscriminator
hlt_srcPFTaus = 'hltSelected%ss%s' % (hlt_pfTauLabel, suffix)
hlt_srcPFJets = 'hlt%sAK4PFJets%s' % (hlt_pfTauLabel, suffix)
deepTauSequenceName = "hltDeep%sSequence%s" % (hlt_pfTauLabel, suffix)
deepTauSequence = addDeepTauDiscriminator(process, hlt_srcPFTaus, hlt_srcPFJets, hlt_srcVertices,
        hlt_pfTauLabel, suffix, deepTauSequenceName)
process.reconstruction_step += deepTauSequence


# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

#--------------------------------------------------------------------------------   
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

dump_file = open('dump.py','w')
dump_file.write(process.dumpPython())

#process.options.numberOfThreads = cms.untracked.uint32(4)

#--------------------------------------------------------------------------------   
