import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Phase2C9_cff import Phase2C9

process = cms.Process('RECO2',Phase2C9)

process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '111X_mcRun4_realistic_T15_v4', '')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/VBFHToTauTau_M125_14TeV_powheg_pythia8_correctedGridpack_tuneCP5/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/084C8B72-BC64-DE46-801F-D971D5A34F62.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)
#-------------------------------------------------------------------------------- 
# L1 NN Tau Path 
process.L1T_NNTau = cms.Path()
process.load("L1Trigger.Phase2L1ParticleFlow.L1NNTauProducer_cff")
process.L1NNTauProducer.L1PFObjects = cms.InputTag("l1pfCandidates","PF")
process.L1T_NNTau += process.L1NNTauProducer

process.L1NNTauProducerPuppi = process.L1NNTauProducer.clone()
process.L1NNTauProducerPuppi.L1PFObjects = cms.InputTag("l1pfCandidates","Puppi")
process.L1T_NNTau += process.L1NNTauProducerPuppi
#-------------------------------------------------------------------------------- 

#--------------------------------------------------------------------------------
# L1 HPS Taus path 
process.L1T_HPSPFTau = cms.Path()
process.l1emulatorSequence = cms.Sequence()
process.load('L1Trigger.L1CaloTrigger.Phase1L1TJets_cff')
process.l1emulatorSequence += process.Phase1L1TJetsSequence
from L1Trigger.Phase2L1Taus.HPSPFTauProducerPF_cfi import HPSPFTauProducerPF
setattr(process, "HPSPFTauProducerPF", HPSPFTauProducerPF)
process.l1emulatorSequence += getattr(process, "HPSPFTauProducerPF")
process.L1T_HPSPFTau += process.l1emulatorSequence
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# HLT Taus path
process.HLT_Tau_Unseeded = cms.Path()
process.taucustomreco = cms.Sequence()
algorithm = "hps"
srcPFCandidates = "particleFlowTmp"
srcVertices = "offlinePrimaryVertices"
srcBeamSpot = "offlineBeamSpot"
isolation_maxDeltaZ = 0.15
isolation_maxDeltaZToLeadTrack = -1.
isolation_minTrackHits = 8
suffix = "8HitsMaxDeltaZWithOfflineVertices"
from HLTrigger.Phase2HLTPFTaus.tools.addHLTPFTaus import addHLTPFTaus
pftauSequence = addHLTPFTaus(process, algorithm,
        srcPFCandidates, srcVertices, srcBeamSpot,
        isolation_maxDeltaZ, isolation_maxDeltaZToLeadTrack, isolation_minTrackHits,
        suffix)
process.taucustomreco += pftauSequence
process.HLT_Tau_Unseeded += process.taucustomreco

pfTauLabel = 'HpsPFTau'
from HLTrigger.Phase2HLTPFTaus.tools.addDeepTauDiscriminator import addDeepTauDiscriminator
srcPFTaus = 'hltSelected%ss%s' % (pfTauLabel, suffix)
srcPFJets = 'hlt%sAK4PFJets%s' % (pfTauLabel, suffix)
deepTauSequenceName = "hltDeep%sSequence%s" % (pfTauLabel, suffix)
deepTauSequence = addDeepTauDiscriminator(process, srcPFTaus, srcPFJets, srcVertices,
                                          pfTauLabel, suffix, deepTauSequenceName)
process.HLT_Tau_Unseeded += deepTauSequence
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# Output path  
process.RECOoutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('RECO'),
        filterName = cms.untracked.string('')
    ),
    fastCloning = cms.untracked.bool(False),
    fileName = cms.untracked.string('NTuple_produce_HLT_CrossTrigger_10events.root'),
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
        'keep *_HPSPFTauProducerPF_*_*',           ## ADDED BY L1 EMULATOR
        'keep *_l1pfCandidates_PF_*',               ## ADDED BY L1 EMULATOR
        'keep *_l1pfProducer*_z0_*',                ## ADDED BY L1 EMULATOR
        'keep *_pfTracksFromL1Tracks*_*_*',         ## ADDED BY L1 EMULATOR
        'keep *_pfClustersFrom*_*_*',               ## ADDED BY L1 EMULATOR
        'keep *_TTTracksFromTracklet_*_*',          ## ADDED BY L1 EMULATOR
        'keep *_VertexProducer_*_*',                ## ADDED BY L1 EMULATOR
        'keep *_ak4PFL1PF_*_*',                     ## ADDED BY L1 EMULATOR
        'keep *_ak4PFL1PFCorrected_*_*',            ## ADDED BY L1 EMULATOR
        'keep *_kt6L1PFJetsPF_rho_*',               ## ADDED BY L1 EMULATOR
        'keep *_kt6L1PFJetsNeutralsPF_rho_*',       ## ADDED BY L1 EMULATOR
        'keep *_l1pfCandidates_PF_*',               ## ADDED BY L1 EMULATOR
        'keep *_l1pfCandidates_Puppi_*',            ## ADDED BY L1 EMULATOR
        'keep *_L1TkPrimaryVertex_*_*',             ## ADDED BY L1 EMULATOR
        'keep *_*BeamSpot*_*_*',                    ## Need the beamspot
        "keep *_*_L1PFTausNN_*",                    ## Save NNPUPPI Tau
        'keep *_hltEgammaGsfElectronsL1Seeded_*_*', ## Save HLT Electri L1Seeded
        'keep *_hltEgammaGsfElectronsUnseeded_*_*', ## Save HLT Electri Unseeded
        'keep *_hltPhase2L3Muons_*_*',              ## Save HLT Muon
        'keep *_hltPhase2L3MuonsNoID_*_*',          ## Save HLT Muon NoID
        'keep *_genParticles_*_*',
        'keep *_tauGenJetsSelectorAllHadrons_*_*',
    )

)
process.RECOoutput_step = cms.EndPath(process.RECOoutput)
#--------------------------------------------------------------------------------



#-------------------------------------------------------------------------------- 
# copy of HLTrigger/Configuration/python/HLT_75e33_cfg.py

#process.load("HLTrigger/Configuration/HLT_75e33/source_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/alongMomElePropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/AnalyticalPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/AnalyticalPropagatorParabolicMF_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/AnyDirectionAnalyticalPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloMPropagatorAlong_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloMPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/beamHaloNavigationSchoolESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloPropagatorAlong_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloSHPropagatorAlong_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloSHPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BeamHaloSHPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/bmbtfParamsSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/BTagRecord_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/bwdAnalyticalPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/bwdElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/bwdGsfElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/caloConfig_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/caloConfigSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/caloDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloGeometryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/caloSimulationParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloTopologyBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloTowerConstituentsMapBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloTowerHardcodeGeometryEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloTowerTopologyEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CaloTPGTranscoder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateBoostedDoubleSecondaryVertexAK8Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateBoostedDoubleSecondaryVertexCA15Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateChargeBTagComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateCombinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateCombinedSecondaryVertexSoftLeptonComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateCombinedSecondaryVertexSoftLeptonCvsLComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateCombinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateGhostTrackComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeCombinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeCombinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeOnlyJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeOnlyJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeTrackCounting3D2ndComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateNegativeTrackCounting3D3rdComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidatePositiveCombinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidatePositiveCombinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidatePositiveOnlyJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidatePositiveOnlyJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateSimpleSecondaryVertex2TrkComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateSimpleSecondaryVertex3TrkComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateTrackCounting3D2ndComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/candidateTrackCounting3D3rdComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CastorDbProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CastorHardcodeGeometryEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsComputerCvsB_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsComputerCvsL_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsNegativeComputerCvsB_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsNegativeComputerCvsL_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsPositiveComputerCvsB_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/charmTagsPositiveComputerCvsL_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/chi2CutForConversionTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2EstimatorForMuonTrackLoader_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2EstimatorForMuRefit_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2EstimatorForRefit_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2MeasurementEstimator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2MeasurementEstimatorForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2MeasurementEstimatorForOutIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/Chi2MeasurementEstimatorForP5_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CloseComponentsMerger5D_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CloseComponentsMerger_forPreId_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ClusterShapeHitFilterESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/combinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/combinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/conv2StepFitterSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/conv2StepRKTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/convStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/convStepFitterSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/convStepRKTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/cosmicsNavigationSchoolESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CSCChannelMapperESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CSCChannelMapperESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CSCGeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CSCIndexerESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/CSCIndexerESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ctppsBeamParametersESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ctppsGeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ctppsInterpolatedOpticalFunctionsESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ctppsOpticalFunctionsESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/detachedQuadStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/detachedQuadStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/detachedTripletStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/detachedTripletStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/doubleVertex2TrkComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/DTGeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/DummyDetLayerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/duplicateDisplaceTrackCandidatesChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/duplicateTrackCandidatesChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/EcalBarrelGeometryEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/EcalElectronicsMappingBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/EcalLaserCorrectionService_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalNextToDeadChannelESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalSeverityLevel_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalSimulationParametersEB_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalSimulationParametersEE_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ecalSimulationParametersES_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/EcalTrigTowerConstituentsMapBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/eegeom_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ElectronChi2_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/electronChi2_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ElectronMaterialEffects_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ElectronMaterialEffects_forPreId_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/electronTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/es_hardcode_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/es_prefer_es_hardcode_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/es_prefer_ppsDBESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/essourceEcalNextToDead_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/essourceEcalSev_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/essourceSev_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/EstimatorForSTA_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/fakeForIdealAlignment_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/fakeTwinMuxParams_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/FittingSmootherRKP5_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/FlexibleKFFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/fwdAnalyticalPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/fwdElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/fwdGsfElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GEMGeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ghostTrackComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlbMuKFFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlobalDetLayerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlobalParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlobalParametersRcdSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlobalTag_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GlobalTrackingGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GsfElectronFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GsfTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GsfTrajectoryFitter_forPreId_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GsfTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/GsfTrajectorySmoother_forPreId_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HBDarkeningEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcal_db_producer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalDDDRecConstants_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalDDDSimConstants_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalDDDSimulationConstants_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HcalHardcodeGeometryEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalOOTPileupESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalRecAlgos_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalSimulationParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HcalTimeSlewEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hcalTopologyIdeal_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HcalTrigTowerGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HEDarkeningEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HepPDTESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalEEGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalEENumberingInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalEEParametersInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalEETopologyBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalHESciGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalHESciTopologyBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalHEScNumberingInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalHEScParametersInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalHESilGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/HGCalHESilTopologyBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalHESiNumberingInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalHESiParametersInitialize_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hgcalTriggerGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/highPtTripletStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/highPtTripletStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hitCollectorForCosmicDCSeeds_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hitCollectorForOutInMuonSeeds_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltCandidateJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltCandidateJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPBwdElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2ChargeMeasurementEstimator16_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2ChargeMeasurementEstimator2000_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2ChargeMeasurementEstimator30_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2ChargeMeasurementEstimator9_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2MeasurementEstimator100_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPChi2MeasurementEstimator30_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPDummyDetLayerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPFastSteppingHelixPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPFastSteppingHelixPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPFwdElectronPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPGlobalDetLayerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPKFFittingSmootherWithOutliersRejectionAndRK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPKFTrajectorySmootherForMuonTrackLoader_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPKFUpdator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPL3MuKFTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPMeasurementTracker_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPMuonTransientTrackingRecHitBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPRKTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPRKTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPRungeKuttaTrackerPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPSmartPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPSmartPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPSmartPropagatorAnyOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPSteppingHelixPropagatorAlong_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPSteppingHelixPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPTrackAlgoPriorityOrder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltESPTTRHBuilderPixelOnly_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPhase2L3MuonHighPtTripletStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPhase2L3MuonHighPtTripletStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPhase2L3MuonInitialStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPhase2L3MuonPixelTrackCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPhase2L3MuonTrackAlgoPriorityOrder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltPixelTracksCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hltTTRBWR_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/hoDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/idealForDigiCSCGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/idealForDigiDTGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/idealForDigiMTDGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/idealForDigiTrackerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/impactParameterMVAComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/initialStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/initialStepChi2EstPreSplitting_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/jetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/jetCoreRegionalStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/jetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFitterForRefitInsideOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFitterForRefitOutsideIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFittingSmootheForSTA_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFittingSmootherBeamHalo_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFittingSmootherForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFFittingSmootherWithOutliersRejectionAndRK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFSmootherForMuonTrackLoader_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFSmootherForMuonTrackLoaderL3_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFSmootherForRefitInsideOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFSmootherForRefitOutsideIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFSwitching1DUpdatorESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectoryFitterBeamHalo_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectoryFitterForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectoryFitterForOutIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectoryFitterForSTA_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectorySmootherBeamHalo_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectorySmootherForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFTrajectorySmootherForSTA_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KFUpdatorESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/KullbackLeiblerDistance5D_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/L1DTConfigFromDB_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/l1ugmtdb_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/LooperFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/LooperTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/LooperTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/lowPtGsfEleFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/lowPtQuadStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/lowPtQuadStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/lowPtTripletStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/lowPtTripletStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MaterialPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MaterialPropagatorParabolicMF_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ME0GeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MeasurementTracker_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mixedTripletStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mixedTripletStepClusterShapeHitFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mixedTripletStepPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mixedTripletStepPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mixedTripletStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MRHChi2MeasurementEstimator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MRHFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MRHTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MRHTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MTDCPEESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mtdDetLayerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mtdGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mtdNumberingGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mtdParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MTDTimeCalibESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/mtdTopology_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MTDTransientTrackingRecHitBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MuonDetLayerGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonGeometryConstants_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MuonNumberingInitialization_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonSeededFittingSmootherWithOutliersRejectionAndRK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonSeededMeasurementEstimatorForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonSeededMeasurementEstimatorForOutIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonSeededMeasurementEstimatorForOutInDisplaced_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/muonSeededTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/MuonTransientTrackingRecHitBuilderESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/myTTRHBuilderWithoutAngle_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/myTTRHBuilderWithoutAngle4MixedPairs_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/myTTRHBuilderWithoutAngle4MixedTriplets_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/myTTRHBuilderWithoutAngle4PixelPairs_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/myTTRHBuilderWithoutAngle4PixelTriplets_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/navigationSchoolESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeCombinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeCombinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeOnlyJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeOnlyJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFElectronByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFElectronByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFElectronByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFElectronComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFMuonByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFMuonByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFMuonByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeSoftPFMuonComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeTrackCounting3D2ndComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/negativeTrackCounting3D3rdComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/OppositeAnalyticalPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/OppositeAnalyticalPropagatorParabolicMF_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/OppositeMaterialPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/OppositeMaterialPropagatorParabolicMF_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/oppositeToMomElePropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ParabolicParametrizedMagneticFieldProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/phase2StripCPEESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/phase2StripCPEGeometricESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/PixelCPEGenericESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelLessStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelLessStepClusterShapeHitFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelLessStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelPairStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelPairStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/pixelTrackCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveCombinedMVAV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveCombinedSecondaryVertexV2Computer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveOnlyJetBProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveOnlyJetProbabilityComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFElectronByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFElectronByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFElectronByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFElectronComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFMuonByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFMuonByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFMuonByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/positiveSoftPFMuonComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ppsDBESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/preshowerDetIdAssociator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/PropagatorWithMaterialForLoopers_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/PropagatorWithMaterialForLoopersOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/PropagatorWithMaterialForMTD_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RK1DFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RK1DTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RK1DTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RKFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RKOutliers1DFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RKTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RKTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RPCConeBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/rpcconesrc_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RPCGeometryESModule_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RungeKuttaTrackerPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/RungeKuttaTrackerPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/simpleSecondaryVertex2TrkComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/simpleSecondaryVertex3TrkComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siPixel2DTemplateDBObjectESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siPixelFakeGainOfflineESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siPixelFakeGainOfflineESSource_prefer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SiPixelFEDChannelContainerESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siPixelQualityESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siPixelTemplateDBObjectESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siStripBackPlaneCorrectionDepESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/sistripconn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siStripGainESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siStripGainSimESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siStripLorentzAngleDepESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/siStripQualityESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SiStripRecHitMatcherESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorAnyOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorAnyRK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorAnyRKOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorRK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SmartPropagatorRKOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFElectronByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFElectronByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFElectronByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFElectronComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFMuonByIP2dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFMuonByIP3dComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFMuonByPtComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/softPFMuonComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorAlong_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorAlongNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorAny_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorAnyNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2Along_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2AlongNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2Any_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2AnyNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2Opposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorL2OppositeNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorOpposite_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/SteppingHelixPropagatorOppositeNoError_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/StraightLinePropagator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/StripCPEESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/stripCPEESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/StripCPEfromTrackAngleESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/templates_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/templates2_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecFlexibleKFFittingSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepChi2Est_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepClusterShapeHitFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepFitterSmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepFitterSmootherForLoopers_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepRKTrajectoryFitter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepRKTrajectoryFitterForLoopers_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepRKTrajectorySmoother_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepRKTrajectorySmootherForLoopers_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tobTecStepTrajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/totemDAQMappingESSourceXML_TimingDiamond_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/totemDAQMappingESSourceXML_TotemTiming_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/totemDAQMappingESSourceXML_TrackingStrip_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/tpparams12_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackAlgoPriorityOrder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackCleaner_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackCounting3D2ndComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackCounting3D3rdComputer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackerGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackerNumberingGeometry_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackerParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TrackerRecoGeometryESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackerTopology_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trackSelectionLwtnn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TrackTriggerSetup_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/trajectoryCleanerBySharedHits_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TrajectoryCleanerBySharedHitsForConversions_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TransientTrackBuilderESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTClusterAlgorithm_neighbor_Phase2TrackerDigi__cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTClusterAlgorithm_official_Phase2TrackerDigi__cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTClusterAlgorithm_official_Phase2TrackerDigi__prefer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTRHBuilderAngleAndTemplate_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ttrhbwor_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ttrhbwr_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTStubAlgorithm_cbc3_Phase2TrackerDigi__cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTStubAlgorithm_official_Phase2TrackerDigi__cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/TTStubAlgorithm_official_Phase2TrackerDigi__prefer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/twinmuxParamsSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/VolumeBasedMagneticFieldESProducer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/XMLIdealGeometryESSource_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/XMLIdealGeometryESSource_CTPPS_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/eventsetup/ZdcHardcodeGeometryEP_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_AK4PFPuppiJet520_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Diphoton30_23_IsoCaloId_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Diphoton30_23_IsoCaloId_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_DoubleEle23_12_Iso_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_DoubleEle25_CaloIdL_PMS2_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_DoubleEle25_CaloIdL_PMS2_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_DoublePFPuppiJets128_DoublePFPuppiBTagDeepCSV_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_DoublePFPuppiJets128_DoublePFPuppiBTagDeepFlavour_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Ele26_WP70_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Ele26_WP70_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Ele32_WPTight_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Ele32_WPTight_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_IsoMu24_FromL1TkMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Mu37_Mu27_FromL1TkMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Mu50_FromL1TkMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFHT200PT30_QuadPFPuppiJet_70_40_30_30_TriplePFPuppiBTagDeepCSV_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFHT200PT30_QuadPFPuppiJet_70_40_30_30_TriplePFPuppiBTagDeepFlavour_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFHT330PT30_QuadPFPuppiJet_75_60_45_40_TriplePFPuppiBTagDeepCSV_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFHT330PT30_QuadPFPuppiJet_75_60_45_40_TriplePFPuppiBTagDeepFlavour_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFPuppiHT1070_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_PFPuppiMETTypeOne140_PFPuppiMHT140_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Photon108EB_TightID_TightIso_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Photon108EB_TightID_TightIso_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Photon187_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_Photon187_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/HLT_TriMu_10_5_5_DZ_FromL1TkMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_DoubleNNTau52_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_DoublePFPuppiJets112_2p4_DEta1p6_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_DoubleTkMuon_15_7_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_PFHT400PT30_QuadPFPuppiJet_70_55_40_40_2p4_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_PFPuppiHT450off_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_PFPuppiMET220off_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_SingleNNTau150_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_SinglePFPuppiJet230off_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_SingleTkMuon_22_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkEle25TkEle12_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkEle36_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkEm37TkEm24_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkEm51_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkIsoEle22TkEm12_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkIsoEle28_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkIsoEm22TkIsoEm12_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TkIsoEm36_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/L1T_TripleTkMuon_5_3_3_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_BTV_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Ele5_Open_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Ele5_Open_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Ele5_WP70_Open_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Ele5_WP70_Open_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_JME_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Photon100EB_TightID_TightIso_Open_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Photon100EB_TightID_TightIso_Open_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Photon100_Open_L1Seeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/MC_Photon100_Open_Unseeded_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/paths/l1tReconstructionPath_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CkfBaseTrajectoryFilter_block_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/ckfBaseTrajectoryFilterP5_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CkfTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/ckfTrajectoryFilterBeamHaloMuon_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/ClusterShapeTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/conv2CkfTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/convCkfTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CSCSegAlgoDF_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CSCSegAlgoRU_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CSCSegAlgoSK_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CSCSegAlgoST_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/CSCSegAlgoTC_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/detachedQuadStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/detachedQuadStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/detachedTripletStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/detachedTripletStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/DTLinearDriftFromDBAlgo_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/GlobalMuonTrackMatcher_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/GroupedCkfTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HFRecalParameterBlock_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HGCAL_cceParams_toUse_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HGCAL_chargeCollectionEfficiencies_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HGCAL_ileakParam_toUse_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HGCAL_noise_fC_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HGCAL_noise_heback_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hgceeDigitizer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hgchebackDigitizer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hgchefrontDigitizer_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/highPtTripletStepTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/highPtTripletStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/highPtTripletStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/highPtTripletStepTrajectoryFilterInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTIter0Phase2L3FromL1TkMuonGroupedCkfTrajectoryFilterIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTIter0Phase2L3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTIter2Phase2L3FromL1TkMuonPSetGroupedCkfTrajectoryBuilderIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTIter2Phase2L3FromL1TkMuonPSetTrajectoryFilterIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonHighPtTripletStepTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonHighPtTripletStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonHighPtTripletStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonHighPtTripletStepTrajectoryFilterInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonInitialStepTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonInitialStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonPSetPvClusterComparerForIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2L3MuonSeedFromProtoTracks_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2PSetPvClusterComparerForIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/hltPhase2SeedFromProtoTracks_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTPSetMuonCkfTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTPSetMuonCkfTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTPSetTrajectoryBuilderForGsfElectrons_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTPSetTrajectoryFilterForElectrons_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTSiStripClusterChargeCutLoose_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/HLTSiStripClusterChargeCutNone_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/initialStepTrajectoryBuilder_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/initialStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/initialStepTrajectoryFilterBasePreSplitting_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/initialStepTrajectoryFilterPreSplitting_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/initialStepTrajectoryFilterShapePreSplitting_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/jetCoreRegionalStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtGsfEleTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtQuadStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtQuadStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtTripletStepStandardTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtTripletStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/lowPtTripletStepTrajectoryFilterInOut_cfi")
#process.load("HLTrigger/Configuration/HLT_75e33/psets/maxEvents_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/ME0SegAlgoRU_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/ME0SegmentAlgorithm_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/mixedTripletStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/muonSeededTrajectoryBuilderForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/muonSeededTrajectoryBuilderForOutInDisplaced_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/muonSeededTrajectoryFilterForInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/muonSeededTrajectoryFilterForOutIn_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/muonSeededTrajectoryFilterForOutInDisplaced_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/options_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/pixelLessStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/pixelPairStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/pixelPairStepTrajectoryFilterBase_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/pixelPairStepTrajectoryFilterInOut_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/PixelTripletHLTGenerator_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/pSetPvClusterComparerForIT_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/seedFromProtoTracks_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/SiStripClusterChargeCutLoose_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/SiStripClusterChargeCutNone_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/SiStripClusterChargeCutTight_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/tobTecStepInOutTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/tobTecStepTrajectoryFilter_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/TrackAssociatorParameters_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/TrajectoryFilterForConversions_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/psets/TrajectoryFilterForElectrons_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/DBService_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/DQMStore_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/FastTimerService_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/MessageLogger_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/SimpleMemoryCheck_cfi")
process.load("HLTrigger/Configuration/HLT_75e33/services/Timing_cfi")


process.schedule = cms.Schedule(*[
    # simulation of the Trigger Primitivs and Level 1 Trigger
    process.l1tReconstructionPath,

    # Jets/MET L1T paths
    process.L1T_SinglePFPuppiJet230off,
    process.L1T_PFPuppiHT450off,
    process.L1T_PFPuppiMET220off,

    # Jets/MET HLT paths
    process.HLT_AK4PFPuppiJet520,
    process.HLT_PFPuppiHT1070,
    process.HLT_PFPuppiMETTypeOne140_PFPuppiMHT140,

    # b-tagging L1T paths
    process.L1T_PFHT400PT30_QuadPFPuppiJet_70_55_40_40_2p4,
    process.L1T_DoublePFPuppiJets112_2p4_DEta1p6,

    # b-tagging HLT paths
    process.HLT_PFHT330PT30_QuadPFPuppiJet_75_60_45_40_TriplePFPuppiBTagDeepCSV_2p4,
    process.HLT_PFHT200PT30_QuadPFPuppiJet_70_40_30_30_TriplePFPuppiBTagDeepCSV_2p4,
    process.HLT_DoublePFPuppiJets128_DoublePFPuppiBTagDeepCSV_2p4,
    process.HLT_PFHT330PT30_QuadPFPuppiJet_75_60_45_40_TriplePFPuppiBTagDeepFlavour_2p4,
    process.HLT_PFHT200PT30_QuadPFPuppiJet_70_40_30_30_TriplePFPuppiBTagDeepFlavour_2p4,
    process.HLT_DoublePFPuppiJets128_DoublePFPuppiBTagDeepFlavour_2p4,

    # Muons L1T paths
    process.L1T_SingleTkMuon_22,
    process.L1T_DoubleTkMuon_15_7,
    process.L1T_TripleTkMuon_5_3_3,

    # Muons HLT paths
    process.HLT_Mu50_FromL1TkMuon,
    process.HLT_IsoMu24_FromL1TkMuon,
    process.HLT_Mu37_Mu27_FromL1TkMuon,
    process.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_FromL1TkMuon,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,

    # E/Gamma L1T paths
    process.L1T_TkEm51,
    process.L1T_TkEle36,
    process.L1T_TkIsoEm36,
    process.L1T_TkIsoEle28,
    process.L1T_TkEm37TkEm24,
    process.L1T_TkEle25TkEle12,
    process.L1T_TkIsoEm22TkIsoEm12,
    process.L1T_TkIsoEle22TkEm12,

    # E/Gamma unseeded paths
    process.HLT_Ele32_WPTight_Unseeded,
    process.HLT_Ele26_WP70_Unseeded,
    process.HLT_Photon108EB_TightID_TightIso_Unseeded,
    process.HLT_Photon187_Unseeded,
    process.HLT_DoubleEle25_CaloIdL_PMS2_Unseeded,
    process.HLT_Diphoton30_23_IsoCaloId_Unseeded,
    # E/Gamma seeded paths
    process.HLT_Ele32_WPTight_L1Seeded,
    process.HLT_Ele26_WP70_L1Seeded,
    process.HLT_Photon108EB_TightID_TightIso_L1Seeded,
    process.HLT_Photon187_L1Seeded,
    process.HLT_DoubleEle25_CaloIdL_PMS2_L1Seeded,
    process.HLT_DoubleEle23_12_Iso_L1Seeded,
    process.HLT_Diphoton30_23_IsoCaloId_L1Seeded,

    # Taus L1T paths
    process.L1T_DoubleNNTau52,
    process.L1T_SingleNNTau150,

    # MC-like paths, without any filters
    process.MC_JME,
    process.MC_BTV,
    process.MC_Ele5_Open_Unseeded,
    process.MC_Ele5_WP70_Open_Unseeded,
    process.MC_Ele5_Open_L1Seeded,
    process.MC_Ele5_WP70_Open_L1Seeded,
    process.MC_Photon100_Open_Unseeded,
    process.MC_Photon100EB_TightID_TightIso_Open_Unseeded,
    process.MC_Photon100_Open_L1Seeded,
    process.MC_Photon100EB_TightID_TightIso_Open_L1Seeded,

    # L1 NN Tau Path
    process.L1T_NNTau,

    # L1 HPS Taus path
    process.L1T_HPSPFTau,

    # HLT Taus path
    process.HLT_Tau_Unseeded,

    # Output path
    process.RECOoutput_step,


])
