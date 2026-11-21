"""Regression: retiring Gray as foundation must not unpublish existing proofs."""
from pathlib import Path
import tomllib
import hashlib
import unittest

ROOT = Path(__file__).resolve().parents[1]

# Exact Git blob hashes of the 23 earlier theorem-source repairs already
# present in canonical main at PR #2339's merger (2026-10-21). These are
# NOT presumed equivalent to the frozen v5.291 source or merely cosmetic:
# pin their full bytes so that ANY later edit requires explicit review.
# This exception is a versioned provenance check, NOT Lean proof authority.
# Version-bound v1.7 Lean 4 prerequisite: strict exact Git blob only.
# The unchanged legacy/v5.291 snapshot remains the historical source.
# This reviewed replacement is subject to independent Lean and axiom audit,
# not authorization to weaken v1.7 statements or global Governance.
PR3555_V17_OPERADIC_REVIEWED_BLOB = {
    "KUOS/DependentOriginationOperadicMultiConditionV1_7.lean": "92350cbc0ff050ddfc011b6841f0ef582b9ca5b4",
}

# Pinned exact current-source v1.8–v1.13 repairs; original legacy bytes remain frozen.
# Source-blob review does not replace Lean kernel or independent CI validation.
PR3555_V18_V113_REVIEWED_BLOBS = {
    "KUOS/DependentOriginationHigherMulticategoryCoherenceV1_8.lean": "36ab51f8eefe18584c7c4e56e79cd8399aeaa961",
    "KUOS/DependentOriginationCausalMonoidalProcessV1_10.lean": "51657eed7ef67efd71c80e6c6c33f4b1efd62c35",
    "KUOS/DependentOriginationMarginalNoSignallingV1_11.lean": "f63ca5a22952520e6d2d7e551a4c2bb0a7bc24cf",
    "KUOS/DependentOriginationJointCausalFactorizationV1_12.lean": "dd732790976af821c1c4c7b806cb099d7cc1e048",
    "KUOS/DependentOriginationEnrichedContextV1_13.lean": "7daa0119c4c8eef35a861ba7b925bf6524fc84b3",
}

# Source-certified Lean4 v1.14–v1.15 boundary repairs; archive preserved.
PR3555_V114_V115_REVIEWED_BLOBS = {
    "KUOS/DependentOriginationStackDescentV1_14.lean": "d57177de97b58f77049cddf22fdfe53d16ea1c6b",
    "KUOS/DependentOriginationInfinityCoherenceV1_15.lean": "db66456d5d497bcdcae089ce74e5046a4a1c5146",
}

# Explicit reviewed v1.17 typed comparison source; frozen original unchanged.
# IsEmpty is a well-typed Type-level nonexistence certificate, not a global
# equivalence/fibrancy assertion. This byte guard is not Lean proof authority.
PR3555_V117_TYPED_NERVE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGlobularNerveComparisonV1_17.lean": "714411f14ff3efe16dcc4b7c3a8973dd261b840e",
}

PR2339_INTEGRATED_PROOF_BLOBS = {
    "KUOS/DependentOriginationAbstractPresentationDescentV4_49.lean": "452b8485f401478bc11c642f463786efa3c1fc5e",
    "KUOS/DependentOriginationArbitraryFactorizationScalarV3_72.lean": "b433ca2ded5e50ed662e36a661cca63a3b97f436",
    "KUOS/DependentOriginationCantorCriticalExponentV4_34.lean": "2e8f81af6feaf2a1a2c4f6f0e5fa442a24c62bab",
    "KUOS/DependentOriginationCorrectedGeneratedRouteV2_97.lean": "2f04b822519e7e4817a3a3661d6bb642d220e4b2",
    "KUOS/DependentOriginationCounterComparisonObstructionV3_68.lean": "3f953183a00b511f96a575dd97d9e039ce9772db",
    "KUOS/DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43.lean": "73a3d4922bd856e41e1c4f58b161e0b82b5076e6",
    "KUOS/DependentOriginationExactUniversalAmbientStrongTransCoherentExtensionV5_08.lean": "e169d3b5e548e4f39b952f415a554ad7f1d07b7d",
    "KUOS/DependentOriginationExactUniversalGlobalCounitStrongTransV4_88.lean": "cc243caf513f1459dc437ebe3a108e1333178318",
    "KUOS/DependentOriginationExactUniversalMappingBicategoryV4_69.lean": "5a4222e66af3ee27bdf31455bb0da6fb6d8bb1a3",
    "KUOS/DependentOriginationExactUniversalMappingCoherenceV4_68.lean": "7d7b85ecc1c5d2112811d227d7b20ad267f12516",
    "KUOS/DependentOriginationExactUniversalMappingHorizontalV4_64.lean": "e895cb3e66d00d633cce20e300d4b77658e5a4fa",
    "KUOS/DependentOriginationExactUniversalTargetNaturalityV4_55.lean": "ea24d7e7cc4ab5227780258b4fd198d6d0210cda",
    "KUOS/DependentOriginationFiveRouteFactorizationV2_98.lean": "9e0cc6652f73dfaf570182a2a0911ced1e2b4a36",
    "KUOS/DependentOriginationGeneratedCorrectionGaugeNormalFormV2_99.lean": "7f5bd9068d8d5fa0a954e868fcbeb7e7f8169bab",
    "KUOS/DependentOriginationGeneratedFactorizationV2_68.lean": "b85952f2530326e80f52cd825e9ec5d8f2be0c54",
    "KUOS/DependentOriginationGeneratedHolonomyCountermodelLoopV2_69.lean": "faed2213a8ea885e9e9fbfb5b62258da99780b44",
    "KUOS/DependentOriginationGlobalFootprintGluingV3_16.lean": "69f879ee77246a1730b5f62f5581a1e68bb75dd5",
    "KUOS/DependentOriginationHexagramEdgeCoboundaryV3_92.lean": "974ce0aabae6838c75a59046a17b3b9dfd8c5412",
    "KUOS/DependentOriginationLowerRankFinitenessV3_45.lean": "014b58970d36a6dacd23dcc80085a6976a50972b",
    "KUOS/DependentOriginationOctahedralResidualCancellationV3_99.lean": "54feaa22583365d9cf0269b89e48fa88d642aa77",
    "KUOS/DependentOriginationOverlapStarTransitivityV3_20.lean": "b2ceb0928735266c3d2590d38201afa0ea88e51b",
    "KUOS/DependentOriginationReassociatedSourceCounitInterchangerV5_77.lean": "d2f982cda906296ddc15acdcdc6f5ec248a51878",
    "KUOS/DependentOriginationStrongTransPostcompositionIdentityTriangulatorV5_63.lean": "168cb60903b3ea7b5a87c0ae6cb9d2791b684598",
}


# v1.25 core-spine ASCII diagram accidentally ended its Lean block comment with -/.
# Replaces only the diagram marker by an unambiguous Unicode arrow.
# Original legacy/v5.291 byte sequence remains unchanged. Not proof authority.
PR3555_V125_CORESPINE_COMMENT_BLOB = {
    "KUOS/DependentOriginationCoreSpineV1_25.lean": "1ecc2afc53b3395cde11746f8488abfe80c497ca",
}

# Historical v1.30 was ill-typed against SSet-valued, scaled (n,i) horn API.
# Exact reviewed proof preserves forward/backward admissibility and filler
# equivalence fields, with explicitly typed SSet and scaling universes.
# This source-blob provenance guard is NOT a Lean certification receipt.
PR3555_V130_LEGACY_TYPED_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledHornPresentationInvariantV1_30.lean": "4f32b06a8c0e36cafc19dafae774c0077c7801bd",
}

# Main-based exact preservation ledger: reviewed v1.60 and v1.61 geometry
# corrections for the pinned Mathlib UnionProd API (research proof-port lineage).
# Historical v5.291 theorem bytes remain frozen. This is NOT Lean certification.
PR3555_V160_V161_UNIONPROD_REVIEWED_BLOBS = {
    "KUOS/DependentOriginationStandardTypeAEndpointPrismPairingV1_60.lean": "3a039fc3eba760d2fb4bfbe62d8fac5ab3fa87b6",
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61.lean": "932d03cd7d4c33a5ffcc5cce03467c6a3a7bf3a3",
}

# The old model-equivalence and coherent normalization v1.31/v1.32 proofs used
# unlifted B/C horn families with lifted source/target maps. Repair carries
# explicit sourceBridge/targetBridge and requires all admissibility, coherent
# round-trip and filler-reflection evidence. Legacy snapshots remain frozen.
# The exact blobs are history protection, not Lean certification.
PR3555_V131_V132_LEGACY_TYPED_BRIDGE_BLOBS = {
    "KUOS/DependentOriginationModelEquivalenceScaledHornPresentationV1_31.lean": "043d16f86bed74c1e37424328fc70f0fa6e2ca77",
    "KUOS/DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32.lean": "dd20dedea5a9d64d9aac989c9dd807ec9afbea6e",
}

# v1.33/v1.34 corrected normalized lifted homotopy/prism witness layers.
# All original/unlifted rectifications remain separate required certificates.
# Exact source bytes protect history; they do not certify a new world by themselves.
PR3555_V133_V134_LIFTED_HOMOTOPY_REVIEWED_BLOBS = {
    "KUOS/DependentOriginationScaledHornHomotopyDescentV1_33.lean": "1b597bddf42581e836f5eb914db6425e2197ef1c",
    "KUOS/DependentOriginationGlobalDuskinPrismHomotopyV1_34.lean": "31a442eb309c1fd0d1185cff0e28c84bc7a5a671",
}

# Lean4 v1.35 genuine normal-lax Duskin cylinder: SSet/ULift universe-safe repair.
# Historical declaration source is frozen; this corrected exact blob is a
# witnessed candidate, not Lean kernel authority on another HEAD.
PR3555_V135_STRONG_CYLINDER_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStrongTransformationDuskinCylinderV1_35.lean": "03b35036177ebc1ef13a055073877a0c9a319976",
}

# Lean4 v1.36 typed strong cylinder exact research-GREEN source.
# Source hash is integrity evidence, not automatic proof/merge authority.
PR3555_V136_STRONG_UNCURRYING_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStrongTransformationCylinderUncurryingV1_36.lean": "bf67ce6b167ecf88e877e874e3e6533c6d45de7d",
}

# Additional v1.36 helper files do not occur in the frozen legacy tree.
# They are checked separately so the historical exception set stays exact.
PR3555_V136_STRONG_UNCURRYING_HELPER_BLOBS = {
    "KUOS/DependentOriginationMixedWhiskerPastingV1_36.lean": "74cfd1997d8c5ec0233db5ab473bf381b2367583",
    "KUOS/DependentOriginationMixedLeftUnitorPastingV1_36.lean": "e3d7a47a45c425040bac9f41675df049bc8ba228",
    "KUOS/DependentOriginationMixedRightUnitorPastingV1_36.lean": "339054b357f4799ad17e29ad6849b595240b0185",
    "KUOS/DependentOriginationPairwiseNormalLaxRoundTripBridgeV1_36.lean": "6a2fceb562a53d13429dc8f839d70a88547e7643",
}


# Lean4 v1.37: explicit independent raw/ULift homotopy-class bridge premises.
# Final raw Duskin iff remains; no unconditional homotopy-class descent is assumed.
# The corrected source is independently certified in its bounded candidate world.
PR3555_V137_CLASS_BRIDGED_HOMOTOPY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationHomotopyClassScaledHornInvariantV1_37.lean": "af1bedd2bcaeac026d3554e359536d925f17cc93",
}

# v1.38 strictification: independent local six-declaration Lean/axiom success.
# Conditional source/target strictification witnesses remain required. No automatic fibrancy.
PR3555_V138_STRICTIFICATION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationHomotopyClassStrictificationV1_38.lean": "08399f0feca20eb8664b2673797a4c785d2588b0",
}

# Lean4 v1.39: genuine SSet.ι₀/SSet.ι₁ endpoints and conditional cylinder proof.
# Exact research candidate independently Lean/MCP and 6-axiom audited.
PR3555_V139_CYLINDER_EXTENSION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledHornCylinderExtensionV1_39.lean": "5cf4f8f6c986ae948ee96bbcfb66ab2540390e1e",
}

# v1.40 exact genuine unionProd pushout attachment (local kernel certified).
# Witnesses remain conditional; source SHA is provenance, not broad authority.
PR3555_V140_PUSHOUT_ATTACHMENT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledHornAttachmentLiftingV1_40.lean": "4592abde6c597d426225a3e587751e5971f2d209",
}

# v1.41 typed ScaledSSet terminal RLP and conditioned attachment lifting;
# exact SHA provenance, not unconditional fibrancy authority.
PR3555_V141_TERMINAL_RLP_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledTerminalRLPV1_41.lean": "0fbc69ccfebbdc75ab61f5836c8ebec9488a84d6",
}

# v1.42 canonical generated scaled-anodyne closure, independently certified.
# This SHA checks source provenance only: no standard scaled-anodyne equality.
PR3555_V142_GENERATED_ANODYNE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledAnodyneGeneratorClosureV1_42.lean": "86e95f82493748b0c7706071196a378d779fa7af",
}

# v1.43 independently audited reducibility repair; factorization stays required.
# Exact source provenance is not unconditional WFS or global merge authority.
PR3555_V143_CONDITIONAL_WFS_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledAnodyneWFSUniversalityV1_43.lean": "833c8e772b7f35a3b5bd36995703ed257bac20c7",
}

# v1.44 conditional small-object factorization; source-bound nine-declaration proof audit.
# Exact byte provenance does not assert unconditional small-object hypothesis or WFS.
PR3555_V144_SMALL_OBJECT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledSmallObjectArgumentV1_44.lean": "ea3d9c2edff775235af266d10b87316f65aeb60d",
}

# v1.45 conditional on the explicit ScaledSSet model; independently proven canonical WFS.
# Exact source SHA protects provenance, not equivalence to standard scaled-anodyne classes.
PR3555_V145_COLIMITS_PRESENTABILITY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledColimitsPresentabilityV1_45.lean": "c5f22f11809a82d4b11fff94091fd7b4f946d8ae",
}

# v1.46 external generated-class comparison under explicit mutual generation premises.
# SHA is provenance only; no external standard/Lurie generator family is instantiated.
PR3555_V146_EXTERNAL_GENERATOR_COMPARISON_REVIEWED_BLOB = {
    "KUOS/DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46.lean": "0f60b58223bc854b3922996067f72b4ba90ae879",
}

# v1.47 external Duskin fibrancy under two independent universe-safe presentations.
# SHA guards exact audited current proof only; Lurie generators are not instantiated.
PR3555_V147_EXTERNAL_DUSKIN_FIBRANCY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationExternalScaledDuskinFibrancyV1_47.lean": "01b0bf486e90615aae3b5abea6994a0985af5e07",
}

# v1.48: factorized scaled-anodyne comparison under explicit external generation premises.
# SHA guards the independently audited source; no standard/Lurie equality asserted.
PR3555_V148_SCALED_ATTACHMENT_FACTORIZATION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledAnodyneAttachmentFactorizationV1_48.lean": "90f67bf0aefb6ecfe2dec7adfc8876ec2b39a31a",
}

# v1.49: type-(A) scaled horn scalings, exact machine-reviewed class reducibility.
# Conditional standard type-(A) specialization, not a full Lurie comparison.
PR3555_V149_STANDARD_TYPE_A_REDUCIBLE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAScaledHornFamilyV1_49.lean": "c3824bb243367beb7df55491e47b5d91b4ac9be9",
}

# v1.50: typed standard type-(A) endpoint pushout-product generator comparison.
# Exact source provenance only; external stability remains an explicit premise.
PR3555_V150_ENDPOINT_PUSHOUT_GENERATOR_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAEndpointPushoutProductV1_50.lean": "48ae0b637350ee8bfb63926327a4285d05b79af5",
}

# v1.51 native Leibniz pushout mate under the existing parametrized adjunction.
# The exact blob guard preserves independently audited proof source; no extra axiom.
PR3555_V151_NATIVE_LEIBNIZ_MATE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51.lean": "ed074ccd29f3b1ece21d5d4a1b5b136cf8a3400a",
}

# v1.52: explicit scaled cartesian interval cylinder equality under fixed Lean.
# This exact SHA is source provenance and does not assert full external anodyne equality.
PR3555_V152_SCALED_CARTESIAN_INTERVAL_REVIEWED_BLOB = {
    "KUOS/DependentOriginationScaledCartesianIntervalCylinderV1_52.lean": "e12da806d1e8da9758c51b1c2139245b7f8e47b9",
}

# v1.53 exact reviewed generated source scaling and enrichment proofs.
# History stays frozen; this SHA is provenance, not global fibrancy authority.
PR3555_V153_SOURCE_ENRICHMENT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53.lean": "e1101bc30b4e30a00a43a0ca6125cb1165c79227",
}

# v1.54 source-bound epi precomposition and conditional generated LLP descent.
# Exact reviewed source only; no unconditional external stability is asserted.
PR3555_V154_GENERATED_LLP_DESCENT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54.lean": "72d318ccb09a307251d7f204b9c0120e78bc7e26",
}

# v1.55 categorical scaled Leibniz pushout: exact source admission after
# independent pinned Lean / real MCP / declaration axiom certification.
# Frozen legacy/v5.291 source remains byte-for-byte untouched.
PR3555_V155_SCALED_LEIBNIZ_PUSHOUT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55.lean": "be2fb30122c82a086304845cedc9a0964b524148",
}

# v1.56 type-(B) scaling-only pushout: exact independently verified source.
# Historical v5.291 source is immutable; the new byte guard is not wider proof authority.
PR3555_V156_TYPE_B_SCALING_PUSHOUT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeBScalingPushoutV1_56.lean": "eb3f6d6105989fe07f7bba70e8c7fc7c84b5e67a",
}

# v1.57 two standard type-(B) collapse completions: source-specific Lean proof.
# Frozen legacy/v5.291 bytes remain immutable; this is not global proof authority.
PR3555_V157_TYPE_B_COLLAPSE_COMPLETION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeBThreeSimplexCompletionV1_57.lean": "735fc7afffc7806bf6eac41c6c8fdc60a6cea95a",
}

# v1.58 type-(C) collapsed edge: version-bound 57-hunk repair plus strict tactic lint.
# The original historical file remains unchanged; this is proof-source provenance only.
PR3555_V158_TYPE_C_COLLAPSED_EDGE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeCCollapsedEdgeV1_58.lean": "d9cb40f0093ec3ef4998ab9420b7d17251337a72",
}

# v1.59 standard A/B/C cellular Leibniz comparison: reviewed full-source provenance.
# Full-source exception is not an independent Lean proof certificate.
PR3555_V159_ABC_LEIBNIZ_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardABCLeibnizCellularComparisonV1_59.lean": "9388efc5b44873409133e30fbe7b30fbabdf6b52",
}

# v1.62 independently reviewed boundary-prism scaled cells, exact-source integrity only.
# A provenance allowlist is not a Lean proof certificate.
PR3555_V162_BOUNDARY_PRISM_SCALED_CELLS_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62.lean": "f90bbb80115cea04267c4a76b995a512d7239aa9",
}

# v1.63 pinned pairing-core and prism dimension dichotomy: exact-source provenance.
# This exact-blob exception is not by itself Lean certification.
PR3555_V163_PRISM_DIMENSION_DICHOTOMY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63.lean": "e9e164f1e71c726de1b5fb7a33a2eb57f98fb6b9",
}

# v1.64 standard type-A boundary prism staircase: exact-source proof provenance.
# This reviewed byte exception is not itself a Lean kernel certificate.
PR3555_V164_STAIRCASE_NORMAL_FORM_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64.lean": "9feee00d150a91150c1c2b3320000829fde4b9d8",
}

# v1.65 standard type-(A) boundary prism cell-pushout criterion.
# Independently certified on exact parent source; one reviewed proof blob only.
PR3555_V165_CELL_PUSHOUT_CRITERION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65.lean": "ca821e08da5e45e424734ed9e6692c6b42613933",
}

# v1.66 all-type-A boundary prism compatibility: exact independently reviewed Lean source.
# This single-byte SHA allowlist is provenance-only, not permission to weaken proofs.
PR3555_V166_CELL_A_COMPATIBILITY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismCellACompatibilityV1_66.lean": "689d0135a4a85d25afae2dbc209a02db0cbd30d8",
}

# v1.67 N=2 maximal-scaling frontier, exact reviewed Lean source.
# Exact-blob provenance is not a global fibrancy or proof-authority claim.
PR3555_V167_N2_MAXIMAL_FRONTIER_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismN2MaximalFrontierV1_67.lean": "b75410426cadb22421191a4a4be4641f787b6669",
}

# v1.69 fixed three-simplex A/B residual table: exact independently certified source.
# This reviewed-source SHA is a provenance guard, not a proof of global descent.
PR3555_V169_THREE_RESIDUAL_TABLE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismThreeResidualClassificationV1_69.lean": "8d235658c173045070a056dd9fac7627059847ed",
}

# v1.70 cellwise A/B classification: exact independently certified source.
# Reviewed SHA is a provenance guard, not a global descent theorem.
PR3555_V170_CELLWISE_AB_CLASSIFICATION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismCellwiseABClassificationV1_70.lean": "000b106019b2940d1cd36937edca6957c270f38d",
}

# v1.71 scaled rank filtration: exact independently Lean/MCP/14-axiom-certified source.
# Reviewed Git blob permits this one present-day formal repair, not global rankwise descent.
PR3555_V171_SCALED_RANK_FILTRATION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismScaledRankFiltrationV1_71.lean": "f7d1e61cefa8e448fb3a8eb6c825a66e9c88db65",
}

# v1.72 rankwise A/B cellularity: exact independent proof-audit source.
# This SHA guard is admissible only after v1.72 producer and 26/26 axioms SUCCESS.
PR3555_V172_RANKWISE_AB_CELLULARITY_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseABCellularityV1_72.lean": "79fd2591bf03e8b2dd2a49848a009699235eaef0",
}

# v1.73 exact rankwise scaled pushout: strict pinned Lean + actual Lean MCP +
# independent 21 public-declaration axioms required BEFORE adoption.
PR3555_V173_RANKWISE_SCALED_PUSHOUT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseScaledPushoutV1_73.lean": "08a532c2793a382a5a59f4aee887d5843704c2fd",
}

# v1.74 simultaneous standard-A rank phase, adopted ONLY after selected
# CodeAI candidate real Lean MCP + independent strict 26/26 public axioms success.
# Candidate source blob db34c44b30cbd6c5bd4aa113e320643aba21577c, exact-source CI #44486900395.
# Provenance guard is separate from full PR Governance certification.
PR3555_V174_SIMULTANEOUS_A_PHASE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousAPhaseV1_74.lean": "db34c44b30cbd6c5bd4aa113e320643aba21577c",
}

# v1.75 simultaneous standard-B rank phase. Admit only the exact source after
# pinned Lean, actual Lean MCP and independent 31-declaration axiom audit.
# This source-integrity guard is separate from full PR Governance certification.
PR3555_V175_SIMULTANEOUS_B_PHASE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRankwiseSimultaneousBPhaseV1_75.lean": "e25e593ee859bbf66a26e8e83ee8d1a17d22659b",
}

# v1.76 A/B two-phase raw successor gluing and actual functor rank-step transport.
# Exact source audited by independent pinned Lean / 41-axiom CI #44839558196.
# This blob guards present-day proof adoption; archived v5.291 bytes are frozen.
PR3555_V176_ALTERNATING_RAW_PAIR_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeABoundaryPrismRawTransfiniteV1_76.lean": "c2aa2dff8fb981650f4fa655545c7101fa1750c8",
}

# v1.77 genuine scaled type-(A) opposite endpoint A-cell and unretracted
# natural-number transfinite A/B gluing, 47 public declarations.
# Exact original-name source Git blob certified at current PR head
# 734f77b71f0fa711fc1bb9222464d1c0e8871b23 by independent pinned
# Lean/47-axiom job 136722302746, workflow 44863621483 completed SUCCESS.
# This guards source integrity only; full PR Governance remains separate.
PR3555_V177_OPPOSITE_ENDPOINT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardTypeAEndpointOppositeCellCertificateV1_77.lean": "d786495a68268e01634f6f8143ebe09241bffc3e",
}

# v1.78 post-endpoint canonical comparison: residual and reverse comparison
# assumptions remain independent; 11 public declarations, exact original-name
# source blob b406155d78506527b53549f0cf232d55f084ac86.
# PR #3555 adopted exact Lean/11-axiom job 136762130797 in
# workflow #44876464005 completed SUCCESS. Integrity pin is not PR approval.
PR3555_V178_POST_ENDPOINT_COMPARISON_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardABCPostEndpointCanonicalComparisonV1_78.lean": "b406155d78506527b53549f0cf232d55f084ac86",
}

# v1.79 positive residual/reverse canonical comparison — strictly conditional.
# Original-name Lean/14-public-declaration independent axiom audit job
# 136775715155, workflow #44880891351, exact prior PR head
# 1fcb10fea83f81d219facf92b2f28be2f9298652 completed SUCCESS.
# Only the exact independently checked proof blob is whitelisted.
# Residual comparison directions are NOT proven inhabited by this.
PR3555_V179_POSITIVE_RESIDUAL_REVIEWED_BLOB = {
    "KUOS/DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79.lean": "cd9a58880341e70a2290387d21d144613464c8c0",
}

# v1.80 adopted original-name source, exact independently certified CI #44895756512,
# job 136820933587 at HEAD 9b741c3b5defc9674afbba7c21419771bbca59b4:
# Strict Lean SUCCESS, 30/30 axiom audit, standard three only, no sorryAx/errors/warnings.
# Source integrity receipt only: no general endpoint RLP, PR merge, or canonical equivalence.
PR3555_V180_GENERATED_PRESENTATION_EQUIVALENCE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationEndpointInvariantV1_80.lean": "7be90de61f5c05456de6fa74dd1f262430486d84",
}

# v1.81 exact original-name CodeAI quotient admission after independent strict Lean
# 37/37 declaration and standard-three axiom audit CI #44901601907, job 136838486395.
# Exact prior PR head 7890a37278509bda24c5f3c181ceeef051c46eff.
# This pins source integrity only, NOT standard-vs-canonical equivalence,
# arbitrary scaling endpoint RLP, or permission to merge the Draft PR.
PR3555_V181_GENERATED_PRESENTATION_QUOTIENT_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationQuotientInvariantV1_81.lean": "8ba7b0e6034a2e24b44587fb477c2192cffffeca",
}

# v1.82 adopted canonical endpoint epi-descent. Exact adopted original-name Lean
# source audited by pinned independent strict CI #44906589078,
# job 136853394307 at PR HEAD c800cc344c68e6a94c435976f46a350364ebde28:
# 12/12 public declarations, standard-three axioms only, no sorry/warnings/errors.
# This SHA records one reviewed formal source, not full PR certification or
# standard/canonical presentation equivalence.
PR3555_V182_CANONICAL_ENDPOINT_EPI_REVIEWED_BLOB = {
    "KUOS/DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82.lean": "a1acb5e5c4c5fc41229e595441e7ad826d3e9c31",
}

# v1.83 original-name posetal reflection, exact independently audited source.
# Candidate strict Lean/18-axiom CI #44941314882 and adopted-original strict
# Lean/18-axiom CI #44942055090 completed SUCCESS; only standard 3 axioms.
# Exact blob is source integrity, not proof of standard/canonical equality or
# authorization to merge the Draft PR. Frozen legacy/v5.291 bytes are untouched.
PR3555_V183_POSETAL_REFLECTION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationPosetalReflectionV1_83.lean": "3bc1f096876f8c7b799ae48f29419e6686e33c87",
}

# v1.84 generated-presentation order reflection, exact original-name source.
# Independent candidate #44950775715 and adopted-original #44951738535
# completed pinned Strict Lean and 13/13 axiom audits, standard three only.
# This hash is provenance, not full Governance or standard/canonical equality.
# Frozen legacy/v5.291 historical source remains immutable.
PR3555_V184_ORDER_REFLECTION_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationOrderReflectionV1_84.lean": "5c1f7e9dc8fbb12bb901f4c67f0aad99543d49b9",
}

# v1.85 generated presentation fixed-point order isomorphism, exact adopted source.
# Independently certified candidate CI #44954822314 and original-name CI
# #44955910257, strict fixed Lean 20/20 public axioms (standard three only).
# This is one source-integrity exception, NOT full PR approval nor a proof
# that standard/canonical presentations are equal. Frozen legacy untouched.
PR3555_V185_FIXED_POINT_ORDER_ISO_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationFixedPointOrderIsoV1_85.lean": "eff1b6d74800c4d3e1f37a6806ebf88ff8b6cd0e",
}

# v1.86 complete-lattice source exactly adopted from verified CodeAI.
# CI #44960553362 certified the candidate 21/21, and the original-name
# independent CI #44961419564 also completed pinned Strict Lean 21/21,
# only propext / Classical.choice / Quot.sound, no sorryAx/warnings/errors.
# This is exact source integrity, not full PR certification or a proof of
# equality of standard and canonical presentations.
PR3555_V186_COMPLETE_LATTICE_REVIEWED_BLOB = {
    "KUOS/DependentOriginationGeneratedPresentationCompleteLatticeV1_86.lean": "57e4436f389928864ebd75ef4b6a0a535b8d51c8",
}

# PR #3522 extraction: exact reviewed source repairs (v1.2–v1.5 only).
# These explicit blob values are integrity checks, not proof certification.
PR3522_FOCUSED_REPAIR_BLOBS = {
    "KUOS/DependentOriginationRefinementTransitivityV1_2.lean": "5247d279787292ee350d9c676ff76094ba4abc57",
    "KUOS/DependentOriginationDirectedCofinalSemanticsV1_3.lean": "7e448c6f56a3fca1a6fd4be18ec44ec0cefc05e3",
    "KUOS/DependentOriginationFilteredCofinalCategoryV1_4.lean": "45e6fd51b4881849819fc5513f3d9fa9f5e34dc4",
    "KUOS/DependentOriginationTwoCellCoherenceV1_5.lean": "42ad51fc7780c63e46ff9387a02d68b93bb27aab",
}


# v1.6 locally discrete bridge: exact independent correction, inherited theorem statement intact.
PR3548_V16_LOCALLY_DISCRETE_BLOB = {
    "KUOS/DependentOriginationBicategoricalCoherenceV1_6.lean": "c1d9cf1c6ed08b535ec5d0bb02bfca254bbb2ac0",
}


# v1.18 import-only provenance: the 2-Yoneda source no longer reexports v1.17 implicitly.
# Removing an import is not proof of global reverse-dependency compatibility.
PR3550_V118_DIRECT_IMPORT_BLOB = {
    "KUOS/DependentOriginationInfinityTwoYonedaV1_18.lean": "d525991b27475a78c7fb509be55dfaedaf654ac1",
}


# Minimal v1.19 class reducibility repair, byte-identical to archived reviewed correction.
# This source-integrity exception is not a Lean proof receipt.
PR3551_V119_CLASS_REDUCIBILITY_BLOB = {
    "KUOS/DependentOriginationNativeInfinityTwoScaledV1_19.lean": "d05efb10005d646752b8cca90f5fdcc11267c101",
}


# v1.20 exact Lean 4 class reducibility + typed inverse-equivalence repair.
# Git blob identity is provenance, not axiom-free proof certification.
PR3552_V120_SEGAL_BLOB = {
    "KUOS/DependentOriginationCompleteSegalInfinityTwoV1_20.lean": "835f9b5cec404f31d27b512dac56a6cef77791bb",
}


# Typed Lean4 Duskin v1.21–v1.25 reviewed exact source integrations only.
# All frozen v5.291 bytes remain unchanged. This check is not kernel certification.
PR3553_V121_V125_BOUNDED_BLOBS = {
    "KUOS/DependentOriginationGlobalDuskinScaledNerveV1_21.lean": "adf9f09aa122b1a6615c083f39815dcf8c36a0fe",
    "KUOS/DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.lean": "e560cd98ae0ca54d177347bc5b0043fe34a66fa7",
    "KUOS/DependentOriginationGlobalDuskinLocalMappingComparisonV1_23.lean": "215dd5d5831a481c466b4b6108954e2f1bf8e036",
    "KUOS/DependentOriginationGlobalDuskinLocalTwoCellComparisonV1_24.lean": "b38ac66a7d1751dc17cbce2dd1790aeef46f3f84",
    "KUOS/DependentOriginationPresentationIndependentInvariantV1_25.lean": "1df6dfa0b978cffd3cb0a9c1d51889b3d835ae07",
}


# v1.26 typed model-equivalence comparison uses explicit eqToHom endpoint transports.
# Historical theorem statements differ: this is recorded, NOT an unchanged-signature claim.
PR3554_V126_TYPED_TRANSPORT_BLOB = {
    "KUOS/DependentOriginationBiequivalencePresentationInvariantV1_26.lean": "60c17fbdefc29642889921e0002e055e9f36d046",
}


# Universe-safe v1.27-v1.29 typed repair: modified historical source blobs.
# Their theorem statements are intentionally typed via ULift, not asserted text-identical.
PR3555_V127_V129_ULIFT_REVIEWED_BLOBS = {
    "KUOS/DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27.lean": "36f9aef05ce8bc068856c28ccbbc2b7512b89112",
    "KUOS/DependentOriginationNormalizationChoiceInvariantV1_28.lean": "9078c15951561b85ecf5378e258adfc92789f823",
    "KUOS/DependentOriginationScaledDuskinHornTransportV1_29.lean": "3a1046a9a44cbb1ad466ef7a27a107122ea05aca",
}


def git_blob_sha(raw: bytes) -> str:
    """Reproduce the canonical git blob hash, including its type/length prefix."""
    header = b"blob " + str(len(raw)).encode("ascii") + b"\0"
    return hashlib.sha1(header + raw).hexdigest()

# Each allowed current-source change is an exact, reviewable lint-only edit of
# the frozen v5.291 bytes. All other historical theorem bytes must remain equal.
LINT_ONLY_SOURCE_EDITS = {
    "KUOS/DependentOriginationWeakCoherentTwoAxisObstructionV2_42.lean": (
        (("def HigherGlobalWeakStageIIIExistenceObstruction : Prop :=\n"
          "  ∃ (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))\n"
          "    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),\n"
          "    HigherWeakEssentialUniquenessObstruction (W := W) R").encode("utf-8"),
         ("def HigherGlobalWeakStageIIIExistenceObstruction : Prop :=\n"
          "  ∃ (R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context))\n"
          "    (_U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),\n"
          "    HigherWeakEssentialUniquenessObstruction (W := W) R").encode("utf-8")),
    ),
    "KUOS/DependentOriginationSingleDetectorObstructionEliminationV2_53.lean": (
        ("def StoredV2_18NaturalityDetectorTargetObject\n    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}\n    {H K : HigherLocalizationFactorization (W := W) R}\n    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=".encode("utf-8"), "def StoredV2_18NaturalityDetectorTargetObject\n    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}\n    {H K : HigherLocalizationFactorization (W := W) R}\n    (_alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=".encode("utf-8")),
    ),
    "KUOS/DependentOriginationDetectingFamilyObstructionEliminationV2_54.lean": (
        ("def StoredV2_18NaturalityDetectingTargetFamily\n    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}\n    {H K : HigherLocalizationFactorization (W := W) R}\n    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=".encode("utf-8"), "def StoredV2_18NaturalityDetectingTargetFamily\n    {R : RawHigherContextualSystem.{u, v, uH, vH} (Context := Context)}\n    {H K : HigherLocalizationFactorization (W := W) R}\n    (_alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=".encode("utf-8")),
    ),
    "KUOS/DependentOriginationPointwiseCoherenceEquationV2_30.lean": (
        ("  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    FactorComparisonArrowwiseCoherenceObstruction (W := W) H".encode("utf-8"), "  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    FactorComparisonArrowwiseCoherenceObstruction (W := W) H".encode("utf-8")),
    ),
    "KUOS/DependentOriginationPointwiseExtensionObstructionV2_29.lean": (
        ("  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    FactorComparisonCoherenceExtensionObstruction (W := W) H".encode("utf-8"), "  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    FactorComparisonCoherenceExtensionObstruction (W := W) H".encode("utf-8")),
    ),
    "KUOS/DependentOriginationComparisonAutomorphismSectionsV2_28.lean": (
        ("    simpa [factorComparisonAutomorphismComponentIso] using g.hom.as.naturality f.toLoc".encode("utf-8"), "    simp [factorComparisonAutomorphismComponentIso]".encode("utf-8")),
        ("  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    HasNontrivialFactorComparisonAutomorphismSection (W := W) H".encode("utf-8"), "  ∃ (H : HigherLocalizationFactorization (W := W) R)\n    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    HasNontrivialFactorComparisonAutomorphismSection (W := W) H".encode("utf-8")),
    ),
    "KUOS/DependentOriginationStoredTriangleCorrectionTorsorV2_27.lean": (
        ("  simp [storedTriangleCorrectionAct, Category.assoc]".encode("utf-8"), "  simp [storedTriangleCorrectionAct]".encode("utf-8")),
        ("  simp [storedTriangleCorrectionDifference, Category.assoc]".encode("utf-8"), "  simp [storedTriangleCorrectionDifference]".encode("utf-8")),
        ("  simp [storedTriangleCorrectionDifference, storedTriangleCorrectionAct,\n    Category.assoc]".encode("utf-8"), "  simp [storedTriangleCorrectionDifference, storedTriangleCorrectionAct]".encode("utf-8")),
        ("  simp [storedTriangleCorrectionAct, storedTriangleCorrectionDifference,\n    Category.assoc]".encode("utf-8"), "  simp [storedTriangleCorrectionAct, storedTriangleCorrectionDifference]".encode("utf-8")),
        ("    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    ¬ Subsingleton (H.comparison ≅ H.comparison)".encode("utf-8"), "    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),\n    ¬ Subsingleton (H.comparison ≅ H.comparison)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationStoredTriangleCorrectionV2_26.lean": (
        ("    (P : FactorModificationTrianglePresentation (W := W) alpha) :\n    factorModificationTrianglePresentationOfStoredCorrection\n        (W := W) (storedTriangleTargetCorrectionOfPresentation (W := W) P) = P := by\n  ext X\n  simp [factorModificationTrianglePresentationOfStoredCorrection,\n    storedTriangleTargetCorrectionOfPresentation, Category.assoc]".encode("utf-8"), "    (P : FactorModificationTrianglePresentation (W := W) alpha) :\n    factorModificationTrianglePresentationOfStoredCorrection\n        (W := W) (storedTriangleTargetCorrectionOfPresentation (W := W) P) = P := by\n  ext X\n  simp [factorModificationTrianglePresentationOfStoredCorrection,\n    storedTriangleTargetCorrectionOfPresentation]".encode("utf-8")),
        ("    (C : StoredTriangleTargetCorrection (W := W) alpha) :\n    storedTriangleTargetCorrectionOfPresentation\n        (W := W)\n        (factorModificationTrianglePresentationOfStoredCorrection (W := W) C) = C := by\n  ext X\n  simp [factorModificationTrianglePresentationOfStoredCorrection,\n    storedTriangleTargetCorrectionOfPresentation, Category.assoc]".encode("utf-8"), "    (C : StoredTriangleTargetCorrection (W := W) alpha) :\n    storedTriangleTargetCorrectionOfPresentation\n        (W := W)\n        (factorModificationTrianglePresentationOfStoredCorrection (W := W) C) = C := by\n  ext X\n  simp [factorModificationTrianglePresentationOfStoredCorrection,\n    storedTriangleTargetCorrectionOfPresentation]".encode("utf-8")),
    ),
    "KUOS/DependentOriginationCoherentWeakHigherLocalizationV2_19.lean": (
        ("    simpa [restrictHigherLocalizedSystem] using\n      alpha.naturality_naturality\n        ((higherPresentationUnitFunctor W).toPseudofunctor.map₂ η)".encode("utf-8"), "    simp [restrictHigherLocalizedSystem]".encode("utf-8")),
    ),
    "KUOS/DependentOriginationPointwiseEquivalenceTransportV2_17.lean": (
        ("  ∃ (G : Context ⥤ Cat.{vH, uH}) (hG : W.IsInvertedBy G),\n    Nonempty\n      (HigherPointwiseEquivalenceComparison\n        (strictRawHigherSystem G) R)".encode("utf-8"), "  ∃ (G : Context ⥤ Cat.{vH, uH}) (_hG : W.IsInvertedBy G),\n    Nonempty\n      (HigherPointwiseEquivalenceComparison\n        (strictRawHigherSystem G) R)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationStrictHigherUniversalityV2_13.lean": (
        ("      ∀ (E : LocalizedContext W ⥤ Cat.{vH, uH})\n        (hE : W.Q ⋙ E ≅ G),\n        Nonempty (E ≅ strictLocalizedFunctor W G hG) := by".encode("utf-8"), "      ∀ (E : LocalizedContext W ⥤ Cat.{vH, uH})\n        (_hE : W.Q ⋙ E ≅ G),\n        Nonempty (E ≅ strictLocalizedFunctor W G hG) := by".encode("utf-8")),
    ),
    "KUOS/DependentOriginationStrictHigherFactorizationV2_12.lean": (
        ("    simp [restrictHigherLocalizedSystem, strictLocalizedHigherSystem,\n      CategoryTheory.Pseudofunctor.comp,\n      CategoryTheory.Functor.toPseudofunctor,\n      CategoryTheory.Functor.toPseudofunctor',\n      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>\n      simp only [CategoryTheory.Cat.Hom.toNatTrans_comp,\n        CategoryTheory.Cat.Hom.toNatTrans_id,\n        CategoryTheory.Cat.whiskerRight_toNatTrans] <;>\n      ext X <;>\n      simp".encode("utf-8"),
         "    simp [restrictHigherLocalizedSystem, strictLocalizedHigherSystem,\n      CategoryTheory.Pseudofunctor.comp,\n      CategoryTheory.Functor.toPseudofunctor,\n      CategoryTheory.Functor.toPseudofunctor',\n      CategoryTheory.pseudofunctorOfIsLocallyDiscrete]".encode("utf-8")),
        ("      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>\n      ext Y <;>\n      simp".encode("utf-8"), "      CategoryTheory.pseudofunctorOfIsLocallyDiscrete]\n    ext Y\n    simp".encode("utf-8")),
        ("      CategoryTheory.pseudofunctorOfIsLocallyDiscrete] <;>\n      ext X <;>\n      simp".encode("utf-8"), "      CategoryTheory.pseudofunctorOfIsLocallyDiscrete]\n    ext X\n    simp".encode("utf-8")),
    ),
    "KUOS/DependentOriginationContextualCoreV1_0.lean": (
        ("    simpa using D.transport_id_apply X x".encode("utf-8"), "    simp".encode("utf-8")),
        ("    simpa using D.transport_id_apply Y y".encode("utf-8"), "    simp".encode("utf-8")),
    ),
    "KUOS/CodeAI/GeneratedPatchErrorBaselineReplayEvaluationV0_1.lean": (
        ("  simpa [hZero] using hPositive".encode("utf-8"), "  simp [hZero] at hPositive".encode("utf-8")),
    ),
    "KUOS/DependentOriginationFunctorialTransportV0_1.lean": (
        ("  simpa [transport] using congrFun (D.state.map_id X) x".encode("utf-8"), "  simp [transport]".encode("utf-8")),
        ("  simpa [transport] using congrFun (D.state.map_comp f g) x".encode("utf-8"), "  simp [transport]".encode("utf-8")),
    ),
    "KUOS/VerifyOS/MiddleWayConditionalContinuityVerificationV0_4.lean": (
        ("    (kind : certificate.transitionKind = .supersedeWithLineage)".encode("utf-8"), "    (_kind : certificate.transitionKind = .supersedeWithLineage)".encode("utf-8")),
        ("    (kind : certificate.transitionKind = .terminate)".encode("utf-8"), "    (_kind : certificate.transitionKind = .terminate)".encode("utf-8")),
    ),
    "KUOS/Architecture/QiWorldLicensedMultiCycleChainInductionV2_1.lean": (
        ("    simpa [w.target_is_immediate_successor]".encode("utf-8"), "    simp [w.target_is_immediate_successor]".encode("utf-8")),
    ),
    "KUOS/WORLD/KuuVacuumCentralReferenceStateBridgeV0_54.lean": (
        ("def centralReferenceState\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def centralReferenceState\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def excitationVector\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def excitationVector\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def vacuumRelativeEntropyLocal\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def vacuumRelativeEntropyLocal\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("def vacuumRelativeEntropyGlobal\n    (Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8"), "def vacuumRelativeEntropyGlobal\n    (_Central : WorldKuuVacuumCentralReferenceStateBridge K)".encode("utf-8")),
        ("    (nonzeroWeight : Central.vacuumTwoPoint creator creator ≠ 0)\n    (observable : B.A) : ℂ :=".encode("utf-8"), "    (_nonzeroWeight : Central.vacuumTwoPoint creator creator ≠ 0)\n    (observable : B.A) : ℂ :=".encode("utf-8")),
    ),
    "KUOS/WORLD/KuuVacuumInformationGeometryBridgeV0_55.lean": (
        ("def vacuumTangentExcitation\n    (Geom : WorldKuuVacuumInformationGeometryBridge Central)".encode("utf-8"), "def vacuumTangentExcitation\n    (_Geom : WorldKuuVacuumInformationGeometryBridge Central)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationLinearTransferConnectedReadoutV0_3.lean": (
        ("def centeredState\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def centeredState\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
        ("def connectedReadout\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def connectedReadout\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
        ("def connectedReadoutTwoStep\n    (L : D.LinearTransferRealization)".encode("utf-8"), "def connectedReadoutTwoStep\n    (_L : D.LinearTransferRealization)".encode("utf-8")),
    ),
    "KUOS/DependentOriginationFiniteTransferWordV0_4.lean": (
        (("/-- The decay product of a finite word is exactly the decay factor at total time. -/\n"
          "theorem wordDecayProduct_eq_totalTime").encode("utf-8"),
         ("-- The decay identity needs the normed additive structure, not an additional\n"
          "-- real vector-space instance. Keep it out of this theorem's implicit API.\n"
          "omit [NormedSpace ℝ State] in\n"
          "/-- The decay product of a finite word is exactly the decay factor at total time. -/\n"
          "theorem wordDecayProduct_eq_totalTime").encode("utf-8")),
    ),
}

class PublicRootRestorationTests(unittest.TestCase):
    def test_every_previous_public_root_remains_published(self):
        old = tomllib.loads((ROOT / 'legacy/v5.291/lakefile.toml').read_text())
        new = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        wanted = {r for lib in old['lean_lib'] for r in lib.get('roots', [])}
        actual = {r for lib in new['lean_lib'] for r in lib.get('roots', [])}
        self.assertEqual(wanted - actual, set(),
                         'Existing public proofs were blanket-excluded from the current Lake package')

class RestoredWiringTests(unittest.TestCase):
    def test_stage_iii_existence_keeps_coherent_witness_without_unused_name(self):
        source = (ROOT / 'formal/KUOS/DependentOriginationWeakCoherentTwoAxisObstructionV2_42.lean').read_text(
            encoding='utf-8')
        self.assertIn(
            "    (_U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),",
            source)
        self.assertIn(
            "    HigherWeakEssentialUniquenessObstruction (W := W) R",
            source)
        self.assertNotIn('set_option linter.unusedVariables false', source)

    def test_internal_kuu_module_is_built_with_one_public_target(self):
        config = tomllib.loads((ROOT / 'lakefile.toml').read_text())
        self.assertEqual(config['defaultTargets'], ['KuuOSFormal'])
        libraries = config['lean_lib']
        self.assertEqual(len(libraries), 1)
        self.assertEqual(libraries[0]['name'], 'KuuOSFormal')
        self.assertNotIn('KuuOSStrict', libraries[0]['roots'])
        self.assertNotIn('Kuu', libraries[0]['roots'])
        # A module can be local to a library through its globs without being
        # a published root; no distinct Lean library is introduced.
        self.assertEqual(libraries[0].get('needs', []), [])
        self.assertTrue(set(libraries[0]['roots']).issubset(set(libraries[0]['globs'])))
        self.assertIn('KuuOSStrict', libraries[0]['globs'])
        self.assertIn('Kuu.*', libraries[0]['globs'])
        workflow = (ROOT / '.github/workflows/kuu-independent-foundation.yml').read_text()
        self.assertIn('scripts/check_kuu_internal_foundation_lean.sh', workflow)
        compiler = (ROOT / 'scripts/check_kuu_internal_foundation_lean.sh').read_text()
        self.assertIn('lake build +KuuOSStrict:olean', compiler)
        self.assertNotIn('lake build KuuOSStrict', compiler)

    def test_publication_and_consumer_routes_are_restored(self):
        from scripts.check_public_proof_roots import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertEqual(report['previous_public_roots'], 107)

    def test_original_theorem_files_preserve_archived_bytes_or_exact_reviewed_integrations(self):
        # Keep every frozen historical source untouched. Only the exact
        # reviewed linter corrections listed above are accepted in current.
        before = ROOT / 'legacy/v5.291/formal'
        self.assertTrue(before.is_dir(), 'historical proof snapshot missing')
        archived = list(before.rglob('*.lean'))
        self.assertTrue(archived, 'historical proof snapshot empty')
        seen = set()
        pinned_seen = set()
        for old in archived:
            rel = old.relative_to(before)
            if rel.as_posix() == 'KuuOSFormal.lean':
                continue  # public import aggregate intentionally extends historical imports
            with self.subTest(path=rel.as_posix()):
                expected = old.read_bytes()
                edits = LINT_ONLY_SOURCE_EDITS.get(rel.as_posix(), ())
                if edits:
                    seen.add(rel.as_posix())
                for old_fragment, new_fragment in edits:
                    self.assertEqual(expected.count(old_fragment), 1,
                                     f'unique archived lint edit required: {rel}')
                    expected = expected.replace(old_fragment, new_fragment, 1)
                current = (ROOT / 'formal' / rel).read_bytes()
                fixed_sha = (PR2339_INTEGRATED_PROOF_BLOBS.get(rel.as_posix())
                             or PR3522_FOCUSED_REPAIR_BLOBS.get(rel.as_posix())
                             or PR3548_V16_LOCALLY_DISCRETE_BLOB.get(rel.as_posix())
                             or PR3550_V118_DIRECT_IMPORT_BLOB.get(rel.as_posix())
                             or PR3551_V119_CLASS_REDUCIBILITY_BLOB.get(rel.as_posix())
                             or PR3552_V120_SEGAL_BLOB.get(rel.as_posix())
                             or PR3553_V121_V125_BOUNDED_BLOBS.get(rel.as_posix())
                             or PR3554_V126_TYPED_TRANSPORT_BLOB.get(rel.as_posix())
                             or PR3555_V127_V129_ULIFT_REVIEWED_BLOBS.get(rel.as_posix())
                             or PR3555_V17_OPERADIC_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V18_V113_REVIEWED_BLOBS.get(rel.as_posix())
                             or PR3555_V114_V115_REVIEWED_BLOBS.get(rel.as_posix())
                             or PR3555_V117_TYPED_NERVE_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V125_CORESPINE_COMMENT_BLOB.get(rel.as_posix())
                             or PR3555_V130_LEGACY_TYPED_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V160_V161_UNIONPROD_REVIEWED_BLOBS.get(rel.as_posix())
                             or PR3555_V131_V132_LEGACY_TYPED_BRIDGE_BLOBS.get(rel.as_posix())
                             or PR3555_V133_V134_LIFTED_HOMOTOPY_REVIEWED_BLOBS.get(rel.as_posix())
                             or PR3555_V135_STRONG_CYLINDER_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V136_STRONG_UNCURRYING_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V137_CLASS_BRIDGED_HOMOTOPY_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V138_STRICTIFICATION_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V139_CYLINDER_EXTENSION_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V140_PUSHOUT_ATTACHMENT_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V141_TERMINAL_RLP_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V142_GENERATED_ANODYNE_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V143_CONDITIONAL_WFS_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V144_SMALL_OBJECT_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V145_COLIMITS_PRESENTABILITY_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V146_EXTERNAL_GENERATOR_COMPARISON_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V147_EXTERNAL_DUSKIN_FIBRANCY_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V148_SCALED_ATTACHMENT_FACTORIZATION_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V149_STANDARD_TYPE_A_REDUCIBLE_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V150_ENDPOINT_PUSHOUT_GENERATOR_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V151_NATIVE_LEIBNIZ_MATE_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V152_SCALED_CARTESIAN_INTERVAL_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V153_SOURCE_ENRICHMENT_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V154_GENERATED_LLP_DESCENT_REVIEWED_BLOB.get(rel.as_posix())
                             or PR3555_V155_SCALED_LEIBNIZ_PUSHOUT_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V156_TYPE_B_SCALING_PUSHOUT_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V157_TYPE_B_COLLAPSE_COMPLETION_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V158_TYPE_C_COLLAPSED_EDGE_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V159_ABC_LEIBNIZ_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V162_BOUNDARY_PRISM_SCALED_CELLS_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V163_PRISM_DIMENSION_DICHOTOMY_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V164_STAIRCASE_NORMAL_FORM_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V165_CELL_PUSHOUT_CRITERION_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V166_CELL_A_COMPATIBILITY_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V167_N2_MAXIMAL_FRONTIER_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V169_THREE_RESIDUAL_TABLE_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V170_CELLWISE_AB_CLASSIFICATION_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V171_SCALED_RANK_FILTRATION_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V172_RANKWISE_AB_CELLULARITY_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V173_RANKWISE_SCALED_PUSHOUT_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V174_SIMULTANEOUS_A_PHASE_REVIEWED_BLOB.get(rel.as_posix())
                              or PR3555_V175_SIMULTANEOUS_B_PHASE_REVIEWED_BLOB.get(rel.as_posix())
                               or PR3555_V176_ALTERNATING_RAW_PAIR_REVIEWED_BLOB.get(rel.as_posix())
                               or PR3555_V177_OPPOSITE_ENDPOINT_REVIEWED_BLOB.get(rel.as_posix())
                               or PR3555_V178_POST_ENDPOINT_COMPARISON_REVIEWED_BLOB.get(rel.as_posix())
                               or PR3555_V179_POSITIVE_RESIDUAL_REVIEWED_BLOB.get(rel.as_posix())
                                or PR3555_V180_GENERATED_PRESENTATION_EQUIVALENCE_REVIEWED_BLOB.get(rel.as_posix())
                                 or PR3555_V181_GENERATED_PRESENTATION_QUOTIENT_REVIEWED_BLOB.get(rel.as_posix())
                                  or PR3555_V182_CANONICAL_ENDPOINT_EPI_REVIEWED_BLOB.get(rel.as_posix())
                                  or PR3555_V183_POSETAL_REFLECTION_REVIEWED_BLOB.get(rel.as_posix())
                                   or PR3555_V184_ORDER_REFLECTION_REVIEWED_BLOB.get(rel.as_posix())
                                   or PR3555_V185_FIXED_POINT_ORDER_ISO_REVIEWED_BLOB.get(rel.as_posix())
                                   or PR3555_V186_COMPLETE_LATTICE_REVIEWED_BLOB.get(rel.as_posix()))
                if fixed_sha is not None:
                    pinned_seen.add(rel.as_posix())
                    self.assertEqual(git_blob_sha(current), fixed_sha,
                                     f'integrated proof source differs from exact main blob: {rel}')
                else:
                    self.assertEqual(current, expected,
                                     f'unreviewed theorem source change: {rel}')
        self.assertEqual(seen, set(LINT_ONLY_SOURCE_EDITS),
                         'reviewed lint edit targets must all exist in historical roots')
        self.assertEqual(pinned_seen, set(PR2339_INTEGRATED_PROOF_BLOBS) | set(PR3522_FOCUSED_REPAIR_BLOBS) | set(PR3548_V16_LOCALLY_DISCRETE_BLOB) | set(PR3550_V118_DIRECT_IMPORT_BLOB) | set(PR3551_V119_CLASS_REDUCIBILITY_BLOB) | set(PR3552_V120_SEGAL_BLOB) | set(PR3553_V121_V125_BOUNDED_BLOBS) | set(PR3554_V126_TYPED_TRANSPORT_BLOB) | set(PR3555_V127_V129_ULIFT_REVIEWED_BLOBS) | set(PR3555_V17_OPERADIC_REVIEWED_BLOB) | set(PR3555_V18_V113_REVIEWED_BLOBS) | set(PR3555_V114_V115_REVIEWED_BLOBS) | set(PR3555_V117_TYPED_NERVE_REVIEWED_BLOB) | set(PR3555_V125_CORESPINE_COMMENT_BLOB) | set(PR3555_V130_LEGACY_TYPED_REVIEWED_BLOB) | set(PR3555_V160_V161_UNIONPROD_REVIEWED_BLOBS) | set(PR3555_V131_V132_LEGACY_TYPED_BRIDGE_BLOBS) | set(PR3555_V133_V134_LIFTED_HOMOTOPY_REVIEWED_BLOBS) | set(PR3555_V135_STRONG_CYLINDER_REVIEWED_BLOB) | set(PR3555_V136_STRONG_UNCURRYING_REVIEWED_BLOB) | set(PR3555_V137_CLASS_BRIDGED_HOMOTOPY_REVIEWED_BLOB) | set(PR3555_V138_STRICTIFICATION_REVIEWED_BLOB) | set(PR3555_V139_CYLINDER_EXTENSION_REVIEWED_BLOB) | set(PR3555_V140_PUSHOUT_ATTACHMENT_REVIEWED_BLOB) | set(PR3555_V141_TERMINAL_RLP_REVIEWED_BLOB) | set(PR3555_V142_GENERATED_ANODYNE_REVIEWED_BLOB) | set(PR3555_V143_CONDITIONAL_WFS_REVIEWED_BLOB) | set(PR3555_V144_SMALL_OBJECT_REVIEWED_BLOB) | set(PR3555_V145_COLIMITS_PRESENTABILITY_REVIEWED_BLOB) | set(PR3555_V146_EXTERNAL_GENERATOR_COMPARISON_REVIEWED_BLOB) | set(PR3555_V147_EXTERNAL_DUSKIN_FIBRANCY_REVIEWED_BLOB) | set(PR3555_V148_SCALED_ATTACHMENT_FACTORIZATION_REVIEWED_BLOB) | set(PR3555_V149_STANDARD_TYPE_A_REDUCIBLE_REVIEWED_BLOB) | set(PR3555_V150_ENDPOINT_PUSHOUT_GENERATOR_REVIEWED_BLOB) | set(PR3555_V151_NATIVE_LEIBNIZ_MATE_REVIEWED_BLOB) | set(PR3555_V152_SCALED_CARTESIAN_INTERVAL_REVIEWED_BLOB) | set(PR3555_V153_SOURCE_ENRICHMENT_REVIEWED_BLOB) | set(PR3555_V154_GENERATED_LLP_DESCENT_REVIEWED_BLOB) | set(PR3555_V155_SCALED_LEIBNIZ_PUSHOUT_REVIEWED_BLOB) | set(PR3555_V156_TYPE_B_SCALING_PUSHOUT_REVIEWED_BLOB) | set(PR3555_V157_TYPE_B_COLLAPSE_COMPLETION_REVIEWED_BLOB) | set(PR3555_V158_TYPE_C_COLLAPSED_EDGE_REVIEWED_BLOB) | set(PR3555_V159_ABC_LEIBNIZ_REVIEWED_BLOB) | set(PR3555_V162_BOUNDARY_PRISM_SCALED_CELLS_REVIEWED_BLOB) | set(PR3555_V163_PRISM_DIMENSION_DICHOTOMY_REVIEWED_BLOB) | set(PR3555_V164_STAIRCASE_NORMAL_FORM_REVIEWED_BLOB) | set(PR3555_V165_CELL_PUSHOUT_CRITERION_REVIEWED_BLOB) | set(PR3555_V166_CELL_A_COMPATIBILITY_REVIEWED_BLOB) | set(PR3555_V167_N2_MAXIMAL_FRONTIER_REVIEWED_BLOB) | set(PR3555_V169_THREE_RESIDUAL_TABLE_REVIEWED_BLOB) | set(PR3555_V170_CELLWISE_AB_CLASSIFICATION_REVIEWED_BLOB) | set(PR3555_V171_SCALED_RANK_FILTRATION_REVIEWED_BLOB) | set(PR3555_V172_RANKWISE_AB_CELLULARITY_REVIEWED_BLOB) | set(PR3555_V173_RANKWISE_SCALED_PUSHOUT_REVIEWED_BLOB) | set(PR3555_V174_SIMULTANEOUS_A_PHASE_REVIEWED_BLOB) | set(PR3555_V175_SIMULTANEOUS_B_PHASE_REVIEWED_BLOB) | set(PR3555_V176_ALTERNATING_RAW_PAIR_REVIEWED_BLOB) | set(PR3555_V177_OPPOSITE_ENDPOINT_REVIEWED_BLOB) | set(PR3555_V178_POST_ENDPOINT_COMPARISON_REVIEWED_BLOB) | set(PR3555_V179_POSITIVE_RESIDUAL_REVIEWED_BLOB) | set(PR3555_V180_GENERATED_PRESENTATION_EQUIVALENCE_REVIEWED_BLOB) | set(PR3555_V181_GENERATED_PRESENTATION_QUOTIENT_REVIEWED_BLOB) | set(PR3555_V182_CANONICAL_ENDPOINT_EPI_REVIEWED_BLOB) | set(PR3555_V183_POSETAL_REFLECTION_REVIEWED_BLOB) | set(PR3555_V184_ORDER_REFLECTION_REVIEWED_BLOB) | set(PR3555_V185_FIXED_POINT_ORDER_ISO_REVIEWED_BLOB) | set(PR3555_V186_COMPLETE_LATTICE_REVIEWED_BLOB),
                         'every preexisting integrated proof exception is explicit and accounted for')

    def test_f55_path_functor_composition_has_actual_path_homs(self):
        # Regression for PR #2428: Paths V is a type synonym of V.
        # Bare category Hom notation can resolve to a raw Quiver.Hom
        # rather than the intended Quiver.Path. The Lean proof's
        # exact argument types must remain explicit at this boundary.
        source = (
            ROOT / 'formal/Kuu/F112/PolygonNativeF55StrictPathObserverP60.lean'
        ).read_text(encoding='utf-8')
        self.assertIn('theorem nativeF55RawPathsToShadow_mapTypedComp', source)
        typed = source.split(
            'theorem nativeF55RawPathsToShadow_mapTypedComp', 1
        )[1].split('/-- The COMPLETE independent nine-constructor', 1)[0]
        self.assertIn('(f : Quiver.Path', typed)
        self.assertIn('(g : Quiver.Path', typed)
        self.assertIn('nativeF55ThreeComp', typed)
        self.assertIn('.map_comp f g', typed)

    def test_v136_typed_uncurrying_helper_exact_blobs(self):
        # New helper roots have no frozen v5.291 counterpart.
        # Keep all four exact research fingerprints as independent provenance.
        for rel, expected in PR3555_V136_STRONG_UNCURRYING_HELPER_BLOBS.items():
            with self.subTest(path=rel):
                path = ROOT / "formal" / rel
                self.assertTrue(path.is_file(), f"missing typed v1.36 helper: {rel}")
                self.assertEqual(git_blob_sha(path.read_bytes()), expected,
                                 f"reviewed v1.36 helper differs from exact source: {rel}")

    def test_v135_normal_lax_universe_bridge_exact_blob(self):
        # The new ULift module is independently reviewed, not a historical overwrite.
        path = ROOT / "formal/KUOS/DependentOriginationNormalLaxUniverseLiftV1_35.lean"
        self.assertTrue(path.is_file(), "missing genuine v1.35 ULift bridge")
        self.assertEqual(git_blob_sha(path.read_bytes()),
                         "9f0f5f81109993bb791df655844c62de0729b681",
                         "v1.35 normal-lax ULift theorem bytes unreviewed")

    def test_v161_unionprod_pinned_source_port_exact_blobs(self):
        # Imported proof-port code, preserving its original Apache-2 attribution.
        # Source integrity is independent of Lean kernel type-checking.
        expected = {
            "PinnedMathlibUnionProdProofPortV1_61.lean": "ba703c0dd48e4e437cb968e077611fb50e5a154e",
            "PinnedMathlibUnionProdInnerPairingCoreV1_61.lean": "ece7c5a8291e6846d5c44c1e5e2f5d6ad546682d",
            "PinnedMathlibUnionProdWeakRankV1_61.lean": "131542e0a23efa80287655656f1805b5523acabf",
            "PinnedMathlibUnionProdOpSymmetryV1_61.lean": "6fa03ffd9b5e0bb084af47a303b275aaa27b7bda",
            "PinnedMathlibUnionProdFullPairingV1_61.lean": "da3cc7de1761081f15830dd0aecf9f3d23067e90",
        }
        for filename, sha in expected.items():
            with self.subTest(path=filename):
                file = ROOT / "formal" / "KUOS" / filename
                self.assertTrue(file.is_file(), f"missing pinned port: {filename}")
                self.assertEqual(git_blob_sha(file.read_bytes()), sha,
                                 f"pinned UnionProd proof port changed: {filename}")

    def test_v129_new_universe_lift_bridge_exact_blob(self):
        # New append-only source has no historical file to replace.
        # Source integrity is evidence, not a kernel typecheck.
        path = ROOT / 'formal/KUOS/DependentOriginationScaledDuskinUniverseLiftBridgeV1_29.lean'
        self.assertEqual(
            git_blob_sha(path.read_bytes()),
            '78b7d2d63dc8137a6143b93579ffcec6c910b06f',
            'v1.29 new ULift scaling bridge source changed without independent review'
        )

    def test_lean_mathlib_pins_are_unchanged(self):
        for name in ('lean-toolchain', 'lake-manifest.json'):
            self.assertEqual((ROOT / name).read_bytes(),
                             (ROOT / 'legacy/v5.291' / name).read_bytes())

    def test_retained_theorems_are_current_package_targets(self):
        from scripts.formal_package_boundary import validate_targets, CURRENT
        validate_targets(ROOT, CURRENT, [
            'KUOS.DependentOriginationContextualCoreV1_0',
            'KUOS.DependentOriginationAdmissibleNonfactorizationV4_01',
            'KuuOSCodeAIV0_1'])

    def test_gray_is_not_a_prerequisite_of_independent_core(self):
        from scripts.check_kuu_foundation import check
        report = check(ROOT)
        self.assertTrue(report['ok'], report['errors'])
        self.assertNotIn('KuuOSFormal', report['current_modules'])

if __name__ == '__main__':
    unittest.main()
