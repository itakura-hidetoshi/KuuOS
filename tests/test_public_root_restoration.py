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


# Reviewed Lean4 source repairs (v1.2 calc and v1.3 parser): frozen legacy stays unchanged.
# The original full source and both proof transitions are preserved in Git history.
# Explicit SHA enrollment is a review gate, never proof of Lean correctness.
REVIEWED_REFINEMENT_TRANSITIVITY_V1_2_BLOBS = {
    "KUOS/DependentOriginationRefinementTransitivityV1_2.lean": "5247d279787292ee350d9c676ff76094ba4abc57",
    "KUOS/DependentOriginationDirectedCofinalSemanticsV1_3.lean": "7e448c6f56a3fca1a6fd4be18ec44ec0cefc05e3",
    "KUOS/DependentOriginationTwoCellCoherenceV1_5.lean": "42ad51fc7780c63e46ff9387a02d68b93bb27aab",
    "KUOS/GaugeInvariantDependentOriginationDenseDescentV0_1.lean": "122b97a2962b30862fbb98d110f04f74af235ba0",
    "KUOS/DependentOriginationBicategoricalCoherenceV1_6.lean": "c1d9cf1c6ed08b535ec5d0bb02bfca254bbb2ac0",
    "KUOS/GaugeInvariantDependentOriginationOrbitQuotientV0_1.lean": "48b6667b350db1853c55645c3b8a919fab159b58",
    "KUOS/DependentOriginationOperadicMultiConditionV1_7.lean": "92350cbc0ff050ddfc011b6841f0ef582b9ca5b4",
    "KUOS/GaugeInvariantDependentOriginationActionGroupoidV0_1.lean": "b02d86014b734012b201f53b33dac173fa1a8376",
    "KUOS/DependentOriginationHigherMulticategoryCoherenceV1_8.lean": "36ab51f8eefe18584c7c4e56e79cd8399aeaa961",
    "KUOS/DependentOriginationCausalMonoidalProcessV1_10.lean": "51657eed7ef67efd71c80e6c6c33f4b1efd62c35",
    "KUOS/DependentOriginationMarginalNoSignallingV1_11.lean": "f63ca5a22952520e6d2d7e551a4c2bb0a7bc24cf",
    "KUOS/DependentOriginationJointCausalFactorizationV1_12.lean": "dd732790976af821c1c4c7b806cb099d7cc1e048",
    "KUOS/DependentOriginationEnrichedContextV1_13.lean": "7daa0119c4c8eef35a861ba7b925bf6524fc84b3",
    "KUOS/DependentOriginationStackDescentV1_14.lean": "d57177de97b58f77049cddf22fdfe53d16ea1c6b",
    "KUOS/DependentOriginationInfinityCoherenceV1_15.lean": "db66456d5d497bcdcae089ce74e5046a4a1c5146",
    "KUOS/DependentOriginationContextualGaugeTheoryV0_1.lean": "cf4b5dc9c4b61f64416489ab50b4233c440bc098",
    "KUOS/DependentOriginationFilteredCofinalCategoryV1_4.lean": "45e6fd51b4881849819fc5513f3d9fa9f5e34dc4",
    "KUOS/DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.lean": "e560cd98ae0ca54d177347bc5b0043fe34a66fa7",
    "KUOS/DependentOriginationGlobalDuskinScaledNerveV1_21.lean": "adf9f09aa122b1a6615c083f39815dcf8c36a0fe",
    "KUOS/DependentOriginationContextualGaugeCoreFactorizationV0_3.lean": "4fdd0e81a57ec768b1241fb3f2e65d1907c4fbc6",
    "KUOS/DependentOriginationCompleteSegalInfinityTwoV1_20.lean": "835f9b5cec404f31d27b512dac56a6cef77791bb",
    "KUOS/DependentOriginationNativeInfinityTwoScaledV1_19.lean": "d05efb10005d646752b8cca90f5fdcc11267c101",
    "KUOS/DependentOriginationContextualGaugeEquivalenceV0_2.lean": "bf36c2c8b4209e60a763f59552f1cb379c58d057",
    "KUOS/DependentOriginationGlobularNerveComparisonV1_17.lean": "714411f14ff3efe16dcc4b7c3a8973dd261b840e",
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
                fixed_sha = PR2339_INTEGRATED_PROOF_BLOBS.get(rel.as_posix())
                if fixed_sha is None:
                    fixed_sha = REVIEWED_REFINEMENT_TRANSITIVITY_V1_2_BLOBS.get(rel.as_posix())
                if fixed_sha is not None:
                    pinned_seen.add(rel.as_posix())
                    self.assertEqual(git_blob_sha(current), fixed_sha,
                                     f'integrated proof source differs from exact main blob: {rel}')
                else:
                    self.assertEqual(current, expected,
                                     f'unreviewed theorem source change: {rel}')
        self.assertEqual(seen, set(LINT_ONLY_SOURCE_EDITS),
                         'reviewed lint edit targets must all exist in historical roots')
        self.assertEqual(pinned_seen,
                         set(PR2339_INTEGRATED_PROOF_BLOBS) |
                         set(REVIEWED_REFINEMENT_TRANSITIVITY_V1_2_BLOBS),
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
