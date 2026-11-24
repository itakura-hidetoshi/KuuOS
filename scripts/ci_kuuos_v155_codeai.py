#!/usr/bin/env python3
"""Source-bound v1.55 CodeAI experiments; no git/gh, paid API, or branch writes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import pathlib
import re
import subprocess
import tempfile

NS = 'KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55'
REL = 'formal/' + NS.replace('.', '/') + '.lean'
BASE = '659440d60913c2ff8455b823aca42cf4667fb779'
DEP = 'formal/KUOS/DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54.lean'
DEP_BLOB = '72d318ccb09a307251d7f204b9c0120e78bc7e26'
CORE_BLOB = '01ec93c4c3f3f6f77946fa0869fd895e15f2674f'
WORKFLOW = '.github/workflows/kuuos-v155-codeai-scaled-leibniz-real-mcp-v1.yml'
NAMES = ['standardTypeAEndpointSimplexEndpointObject',
 'standardTypeAEndpointHornIntervalObject',
 'standardTypeAEndpointCornerScaling',
 'standardTypeAEndpointCornerObject',
 'standardTypeAEndpointCornerToSimplexEndpoint',
 'standardTypeAEndpointCornerToHornInterval',
 'standardTypeAEndpointGeneratedInl',
 'standardTypeAEndpointGeneratedInr',
 'standardTypeAEndpointGeneratedPushout_commutes',
 'standardTypeAEndpointGeneratedPushout_compatibility_map',
 'standardTypeAEndpointGeneratedPushoutDescMap',
 'standardTypeAEndpointGeneratedPushoutDescMap_scaled',
 'standardTypeAEndpointGeneratedPushoutDesc',
 'standardTypeAEndpointGeneratedPushout_inl_desc',
 'standardTypeAEndpointGeneratedPushout_inr_desc',
 'standardTypeAEndpointGeneratedPushout_hom_ext',
 'standardTypeAEndpointGeneratedPushout_isPushout',
 'standardTypeAEndpointCylinder_is_scaledCartesianProduct',
 'standardTypeAEndpointSimplexEndpointToCylinder',
 'standardTypeAEndpointSimplexEndpointToCylinder_map',
 'standardTypeAEndpointHornIntervalToCylinder',
 'standardTypeAEndpointHornIntervalToCylinder_map',
 'standardTypeAEndpointCylinder_compatibility',
 'standardTypeAEndpointScaledLeibnizPushoutProductHom',
 'standardTypeAEndpointScaledLeibnizPushoutProductHom_eq_generated',
 'standardTypeAEndpointScaledLeibnizPushoutProductHom_map',
 'standardTypeAEndpointGeneratedPushoutProductHom_map_eq_induced',
 'standardTypeAEndpointScaledLeibnizPushoutProductHom_map_eq_native',
 'standardTypeAEndpointScaledLeibniz_underlying_hasLiftingProperty_iff',
 'standardTypeAScaledLeibnizPushoutProductGenerators',
 'standardTypeAScaledLeibnizPushoutProductGenerator_mem',
 'standardTypeAScaledLeibnizPushoutProductGenerators_eq_generated',
 'StandardTypeAScaledLeibnizPushoutProductStable',
 'StandardTypeAScaledLeibnizPushoutProductStable.toGenerated',
 'StandardTypeAScaledLeibnizPushoutProductStable.ofGenerated',
 'StandardTypeAExternalScaledLeibnizComparison',
 'StandardTypeAExternalScaledLeibnizComparison.toGeneratedPushoutComparison',
 'StandardTypeAExternalScaledLeibnizComparison.inducedTypeAAttachments_le_externalGenerated',
 'StandardTypeAExternalScaledLeibnizComparison.endpointPushoutProducts_le_externalGenerated']
EXPECTED = {'archived-reference': '12acfd38ff346c3b27e27fe652c401b9175140b4',
 'computability-only': '3c6fe0f2d1504d01ef08fbe38a2b7ea703d5bbfa',
 'explicit-comparison': 'be2fb30122c82a086304845cedc9a0964b524148'}
DEPENDENCIES = {'formal/KUOS/DependentOriginationScaledCartesianIntervalCylinderV1_52.lean': 'e12da806d1e8da9758c51b1c2139245b7f8e47b9',
 'formal/KUOS/DependentOriginationStandardTypeAEndpointPushoutProductV1_50.lean': '48ae0b637350ee8bfb63926327a4285d05b79af5',
 'formal/KUOS/DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54.lean': '72d318ccb09a307251d7f204b9c0120e78bc7e26',
 'formal/KUOS/DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51.lean': 'ed074ccd29f3b1ece21d5d4a1b5b136cf8a3400a',
 'formal/KUOS/DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53.lean': 'e1101bc30b4e30a00a43a0ca6125cb1165c79227'}
# Exact, reviewed reference transformations; never a source of certification.
# The compiler compares this reference against the current dependency world.
REFERENCE_EDITS = [['/-- The `Delta[n] x {epsilon}` leg, equipped with the restriction scaling from\n'
  'v1.53. -/\n'
  'def standardTypeAEndpointSimplexEndpointObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n',
  '/-- The `Delta[n] x {epsilon}` leg, equipped with the restriction scaling from\n'
  'v1.53. -/\n'
  'noncomputable def standardTypeAEndpointSimplexEndpointObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n'],
 ['/-- The `Lambda_i^n x Delta[1]` leg, equipped with the restriction scaling\n'
  'from v1.53. -/\n'
  'def standardTypeAEndpointHornIntervalObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n',
  '/-- The `Lambda_i^n x Delta[1]` leg, equipped with the restriction scaling\n'
  'from v1.53. -/\n'
  'noncomputable def standardTypeAEndpointHornIntervalObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n'],
 ['legs themselves are restrictions of the same induced source scaling, the\n'
  'second corner map will preserve this scaling as well. -/\n'
  'def standardTypeAEndpointCornerScaling\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    ScaledSimplicialSet\n',
  'legs themselves are restrictions of the same induced source scaling, the\n'
  'second corner map will preserve this scaling as well. -/\n'
  '@[reducible] noncomputable def standardTypeAEndpointCornerScaling\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    ScaledSimplicialSet\n'],
 ['\n'
  '/-- The scaled corner object of the endpoint Leibniz span. -/\n'
  'def standardTypeAEndpointCornerObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n',
  '\n'
  '/-- The scaled corner object of the endpoint Leibniz span. -/\n'
  'noncomputable def standardTypeAEndpointCornerObject\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=\n'
  '  ScaledSSet.of\n'],
 ['\n'
  '/-- The first canonical leg into the least-generated union-product source. -/\n'
  'def standardTypeAEndpointGeneratedInl\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointSimplexEndpointObject g ⟶\n',
  '\n'
  '/-- The first canonical leg into the least-generated union-product source. -/\n'
  'noncomputable def standardTypeAEndpointGeneratedInl\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointSimplexEndpointObject g ⟶\n'],
 ['\n'
  '/-- The second canonical leg into the least-generated union-product source. -/\n'
  'def standardTypeAEndpointGeneratedInr\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointHornIntervalObject g ⟶\n',
  '\n'
  '/-- The second canonical leg into the least-generated union-product source. -/\n'
  'noncomputable def standardTypeAEndpointGeneratedInr\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointHornIntervalObject g ⟶\n'],
 ['      (standardTypeAEndpointGeneratedPushoutDescMap g f h w) := by\n'
  '  intro t ht\n'
  '  dsimp [standardTypeAEndpointGeneratedPushoutScaling] at ht\n'
  '  rcases ht with\n'
  '    ⟨x, rfl⟩ | ⟨x, rfl⟩ | ⟨x, hx, rfl⟩ | ⟨x, hx, rfl⟩\n',
  '      (standardTypeAEndpointGeneratedPushoutDescMap g f h w) := by\n'
  '  intro t ht\n'
  '  rcases ht with\n'
  '    ⟨x, rfl⟩ | ⟨x, rfl⟩ | ⟨x, hx, rfl⟩ | ⟨x, hx, rfl⟩\n'],
 ['              (op ⦋2⦌) x) =\n'
  '        f.map.app (op ⦋2⦌) x := by\n'
  '      simpa [standardTypeAEndpointGeneratedPushoutDescMap] using\n'
  '        ConcreteCategory.congr_hom\n'
  '          (congr_app\n'
  '            ((standardTypeAEndpointPushoutSquare g).inl_desc\n'
  '              f.map h.map\n'
  '              (standardTypeAEndpointGeneratedPushout_compatibility_map\n'
  '                g f h w))\n'
  '            (op ⦋2⦌)) x\n'
  '    rw [hfac]\n'
  '    exact f.scaled x hx\n',
  '              (op ⦋2⦌) x) =\n'
  '        f.map.app (op ⦋2⦌) x := by\n'
  '      have heq := (standardTypeAEndpointPushoutSquare g).inl_desc\n'
  '        f.map h.map\n'
  '        (standardTypeAEndpointGeneratedPushout_compatibility_map g f h w)\n'
  '      have hcomponent := congrArg\n'
  '        (fun (η : ((Δ[g.n] : SSet.{u}) ⊗ (intervalEndpoint g.endpoint : SSet.{u})) ⟶ W.carrier) => η.app '
  '(op ⦋2⦌) x) heq\n'
  '      change\n'
  '        ((SSet.Subcomplex.unionProd.ι₁\n'
  '          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫\n'
  '            standardTypeAEndpointGeneratedPushoutDescMap g f h w).app\n'
  '            (op ⦋2⦌)) x = f.map.app (op ⦋2⦌) x\n'
  '      exact hcomponent\n'
  '    rw [hfac]\n'
  '    exact f.scaled x hx\n'],
 ['              (op ⦋2⦌) x) =\n'
  '        h.map.app (op ⦋2⦌) x := by\n'
  '      simpa [standardTypeAEndpointGeneratedPushoutDescMap] using\n'
  '        ConcreteCategory.congr_hom\n'
  '          (congr_app\n'
  '            ((standardTypeAEndpointPushoutSquare g).inr_desc\n'
  '              f.map h.map\n'
  '              (standardTypeAEndpointGeneratedPushout_compatibility_map\n'
  '                g f h w))\n'
  '            (op ⦋2⦌)) x\n'
  '    rw [hfac]\n'
  '    exact h.scaled x hx\n',
  '              (op ⦋2⦌) x) =\n'
  '        h.map.app (op ⦋2⦌) x := by\n'
  '      have heq := (standardTypeAEndpointPushoutSquare g).inr_desc\n'
  '        f.map h.map\n'
  '        (standardTypeAEndpointGeneratedPushout_compatibility_map g f h w)\n'
  '      have hcomponent := congrArg\n'
  '        (fun (η : ((SSet.horn g.n g.i : SSet.{u}) ⊗ (Δ[1] : SSet.{u})) ⟶ W.carrier) => η.app (op ⦋2⦌) x) '
  'heq\n'
  '      change\n'
  '        ((SSet.Subcomplex.unionProd.ι₂\n'
  '          (SSet.horn g.n g.i) (intervalEndpoint g.endpoint) ≫\n'
  '            standardTypeAEndpointGeneratedPushoutDescMap g f h w).app\n'
  '            (op ⦋2⦌)) x = h.map.app (op ⦋2⦌) x\n'
  '      exact hcomponent\n'
  '    rw [hfac]\n'
  '    exact h.scaled x hx\n'],
 ["    isColimit' := ⟨?_⟩\n"
  '  }\n'
  '  apply PushoutCocone.IsColimit.mk _\n'
  '  · intro s\n'
  '    exact standardTypeAEndpointGeneratedPushoutDesc\n'
  '      g s.inl s.inr s.condition\n'
  '  · intro s\n'
  '    exact standardTypeAEndpointGeneratedPushout_inl_desc\n'
  '      g s.inl s.inr s.condition\n'
  '  · intro s\n'
  '    exact standardTypeAEndpointGeneratedPushout_inr_desc\n'
  '      g s.inl s.inr s.condition\n'
  '  · intro s m hm₁ hm₂\n'
  '    apply standardTypeAEndpointGeneratedPushout_hom_ext g\n'
  '    · rw [hm₁, standardTypeAEndpointGeneratedPushout_inl_desc]\n'
  '    · rw [hm₂, standardTypeAEndpointGeneratedPushout_inr_desc]\n'
  '\n'
  '/-! ## The canonical scaled Leibniz comparison map -/\n',
  "    isColimit' := ⟨?_⟩\n"
  '  }\n'
  '  exact PushoutCocone.IsColimit.mk\n'
  '    (standardTypeAEndpointGeneratedPushout_commutes g)\n'
  '    (fun s => standardTypeAEndpointGeneratedPushoutDesc\n'
  '      g s.inl s.inr s.condition)\n'
  '    (fun s => standardTypeAEndpointGeneratedPushout_inl_desc\n'
  '      g s.inl s.inr s.condition)\n'
  '    (fun s => standardTypeAEndpointGeneratedPushout_inr_desc\n'
  '      g s.inl s.inr s.condition)\n'
  '    (by\n'
  '      intro s m hm₁ hm₂\n'
  '      apply standardTypeAEndpointGeneratedPushout_hom_ext g\n'
  '      · exact hm₁.trans\n'
  '          (standardTypeAEndpointGeneratedPushout_inl_desc\n'
  '            g s.inl s.inr s.condition).symm\n'
  '      · exact hm₂.trans\n'
  '          (standardTypeAEndpointGeneratedPushout_inr_desc\n'
  '            g s.inl s.inr s.condition).symm)\n'
  '\n'
  '/-! ## The canonical scaled Leibniz comparison map -/\n'],
 ['\n'
  '/-- The natural map from the simplex-endpoint leg to the scaled cylinder. -/\n'
  'def standardTypeAEndpointSimplexEndpointToCylinder\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointSimplexEndpointObject g ⟶\n',
  '\n'
  '/-- The natural map from the simplex-endpoint leg to the scaled cylinder. -/\n'
  'noncomputable def standardTypeAEndpointSimplexEndpointToCylinder\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointSimplexEndpointObject g ⟶\n'],
 ['    (standardTypeAEndpointSimplexEndpointToCylinder g).map =\n'
  '      (Δ[g.n] : SSet.{u}) ◁ (intervalEndpoint g.endpoint).ι := by\n'
  '  simp [standardTypeAEndpointSimplexEndpointToCylinder,\n'
  '    standardTypeAEndpointGeneratedInl,\n'
  '    standardTypeAEndpointGeneratedPushoutProductHom_map]\n'
  '\n'
  '/-- The natural map from the horn-interval leg to the scaled cylinder. -/\n'
  'def standardTypeAEndpointHornIntervalToCylinder\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointHornIntervalObject g ⟶\n',
  '    (standardTypeAEndpointSimplexEndpointToCylinder g).map =\n'
  '      (Δ[g.n] : SSet.{u}) ◁ (intervalEndpoint g.endpoint).ι := by\n'
  '  simpa only [standardTypeAEndpointSimplexEndpointToCylinder,\n'
  '    ScaledSSet.comp_map, standardTypeAEndpointGeneratedInl,\n'
  '    standardTypeAEndpointGeneratedPushoutProductHom_map] using\n'
  '    (SSet.Subcomplex.unionProd.ι₁_ι\n'
  '      (SSet.horn g.n g.i) (intervalEndpoint g.endpoint))\n'
  '\n'
  '/-- The natural map from the horn-interval leg to the scaled cylinder. -/\n'
  'noncomputable def standardTypeAEndpointHornIntervalToCylinder\n'
  '    (g : StandardTypeAHornAttachmentGeneratorIndex) :\n'
  '    standardTypeAEndpointHornIntervalObject g ⟶\n'],
 ['    (standardTypeAEndpointHornIntervalToCylinder g).map =\n'
  '      (SSet.horn g.n g.i).ι ▷ (Δ[1] : SSet.{u}) := by\n'
  '  simp [standardTypeAEndpointHornIntervalToCylinder,\n'
  '    standardTypeAEndpointGeneratedInr,\n'
  '    standardTypeAEndpointGeneratedPushoutProductHom_map]\n'
  '\n'
  '/-- The two product-leg maps into the cylinder agree on the corner. -/\n',
  '    (standardTypeAEndpointHornIntervalToCylinder g).map =\n'
  '      (SSet.horn g.n g.i).ι ▷ (Δ[1] : SSet.{u}) := by\n'
  '  simpa only [standardTypeAEndpointHornIntervalToCylinder,\n'
  '    ScaledSSet.comp_map, standardTypeAEndpointGeneratedInr,\n'
  '    standardTypeAEndpointGeneratedPushoutProductHom_map] using\n'
  '    (SSet.Subcomplex.unionProd.ι₂_ι\n'
  '      (SSet.horn g.n g.i) (intervalEndpoint g.endpoint))\n'
  '\n'
  '/-- The two product-leg maps into the cylinder agree on the corner. -/\n'],
 ['        standardTypeAEndpointHornIntervalToCylinder g := by\n'
  '  simp only [standardTypeAEndpointSimplexEndpointToCylinder,\n'
  '    standardTypeAEndpointHornIntervalToCylinder, Category.assoc]\n'
  '  rw [standardTypeAEndpointGeneratedPushout_commutes g]\n'
  '\n'
  '/-- The canonical scaled Leibniz pushout-product map obtained by the actual\n',
  '        standardTypeAEndpointHornIntervalToCylinder g := by\n'
  '  simp only [standardTypeAEndpointSimplexEndpointToCylinder,\n'
  '    standardTypeAEndpointHornIntervalToCylinder]\n'
  '  calc\n'
  '    _ = (standardTypeAEndpointCornerToSimplexEndpoint g ≫\n'
  '          standardTypeAEndpointGeneratedInl g) ≫\n'
  '          standardTypeAEndpointGeneratedPushoutProductHom g := by\n'
  '        rw [Category.assoc]\n'
  '    _ = (standardTypeAEndpointCornerToHornInterval g ≫\n'
  '          standardTypeAEndpointGeneratedInr g) ≫\n'
  '          standardTypeAEndpointGeneratedPushoutProductHom g :=\n'
  '        congrArg (fun k => k ≫ standardTypeAEndpointGeneratedPushoutProductHom g)\n'
  '          (standardTypeAEndpointGeneratedPushout_commutes g)\n'
  '    _ = _ := by rw [Category.assoc]\n'
  '\n'
  '/-- The canonical scaled Leibniz pushout-product map obtained by the actual\n'],
 ['      standardTypeAEndpointGeneratedPushoutProductHom g := by\n'
  '  apply (standardTypeAEndpointGeneratedPushout_isPushout g).hom_ext\n'
  '  · rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inl_desc]\n'
  '    rfl\n'
  '  · rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inr_desc]\n'
  '    rfl\n'
  '\n',
  '      standardTypeAEndpointGeneratedPushoutProductHom g := by\n'
  '  apply (standardTypeAEndpointGeneratedPushout_isPushout g).hom_ext\n'
  '  · unfold standardTypeAEndpointScaledLeibnizPushoutProductHom\n'
  '    rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inl_desc]\n'
  '    rfl\n'
  '  · unfold standardTypeAEndpointScaledLeibnizPushoutProductHom\n'
  '    rw [(standardTypeAEndpointGeneratedPushout_isPushout g).inr_desc]\n'
  '    rfl\n'
  '\n'],
 ['  pushoutProduct_mem :\n'
  '    ∀ g : StandardTypeAHornAttachmentGeneratorIndex,\n'
  '      L (standardTypeAScaledHornGeneratorHom g.toHornGenerator) →\n'
  '      L (standardTypeAEndpointScaledLeibnizPushoutProductHom g)\n'
  '\n',
  '  pushoutProduct_mem :\n'
  '    ∀ g : StandardTypeAHornAttachmentGeneratorIndex,\n'
  '      L (standardTypeAScaledHornGeneratorHom\n'
  '        (StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)) →\n'
  '      L (standardTypeAEndpointScaledLeibnizPushoutProductHom g)\n'
  '\n'],
 ['    (K : StandardTypeAExternalScaledLeibnizComparison E)\n'
  '\n'
  '/-- The categorical comparison data supplies the exact v1.54 comparison\n'
  'interface. -/\n',
  '    (K : StandardTypeAExternalScaledLeibnizComparison E)\n'
  '\n'
  'include K\n'
  '\n'
  '/-- The categorical comparison data supplies the exact v1.54 comparison\n'
  'interface. -/\n'],
 ['      MorphismProperty (ScaledSSet.{u})) ≤\n'
  '      externalGeneratedScaledAnodyne E :=\n'
  '  K.toGeneratedPushoutComparison\n'
  '    .inducedTypeAAttachments_le_externalGenerated\n'
  '\n'
  '/-- The v1.50 induced endpoint-pushout-product presentation is externally\n',
  '      MorphismProperty (ScaledSSet.{u})) ≤\n'
  '      externalGeneratedScaledAnodyne E :=\n'
  '  (K.toGeneratedPushoutComparison).inducedTypeAAttachments_le_externalGenerated\n'
  '\n'
  '/-- The v1.50 induced endpoint-pushout-product presentation is externally\n'],
 ['      MorphismProperty (ScaledSSet.{u})) ≤\n'
  '      externalGeneratedScaledAnodyne E :=\n'
  '  K.toGeneratedPushoutComparison\n'
  '    .endpointPushoutProducts_le_externalGenerated\n'
  '\n'
  'end StandardTypeAExternalScaledLeibnizComparison\n',
  '      MorphismProperty (ScaledSSet.{u})) ≤\n'
  '      externalGeneratedScaledAnodyne E :=\n'
  '  (K.toGeneratedPushoutComparison).endpointPushoutProducts_le_externalGenerated\n'
  '\n'
  'end StandardTypeAExternalScaledLeibnizComparison\n']]


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def candidates(baseline: str) -> dict[str, str]:
    assert blob(baseline.encode()) == BASE, 'baseline SHA mismatch'
    metadata = baseline
    for name in (
        'standardTypeAEndpointSimplexEndpointObject',
        'standardTypeAEndpointHornIntervalObject',
        'standardTypeAEndpointCornerScaling',
        'standardTypeAEndpointCornerObject',
        'standardTypeAEndpointGeneratedInl',
        'standardTypeAEndpointGeneratedInr',
        'standardTypeAEndpointSimplexEndpointToCylinder',
        'standardTypeAEndpointHornIntervalToCylinder',
    ):
        old = '\ndef ' + name + '\n'
        new = '\n' + ('@[reducible] ' if name == 'standardTypeAEndpointCornerScaling' else '')
        new += 'noncomputable def ' + name + '\n'
        assert metadata.count(old) == 1
        metadata = metadata.replace(old, new, 1)
    reference = baseline
    for old, new in REFERENCE_EDITS:
        assert reference.count(old) == 1, 'nonunique exact-reference edit'
        reference = reference.replace(old, new, 1)
    assert blob(reference.encode()) == '12acfd38ff346c3b27e27fe652c401b9175140b4'
    old = '(StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)'
    assert reference.count(old) == 1
    explicit = reference.replace(old,
        '(KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50.'
        'StandardTypeAHornAttachmentGeneratorIndex.toHornGenerator g)', 1)
    for name in ('inducedTypeAAttachments_le_externalGenerated',
                 'endpointPushoutProducts_le_externalGenerated'):
        old = '  (K.toGeneratedPushoutComparison).' + name
        assert explicit.count(old) == 1
        new = ('  KUOS.DependentOriginationStandardTypeAGeneratedPushoutLLPDescentV1_54.'
               'StandardTypeAExternalGeneratedPushoutComparison.' + name +
               '\n    (toGeneratedPushoutComparison K)')
        explicit = explicit.replace(old, new, 1)
    result = {'computability-only': metadata, 'archived-reference': reference,
              'explicit-comparison': explicit}
    pattern = (r'^(?:@\[[^\]]+\]\s*)?(?:noncomputable\s+)?'
               r'(?:def|theorem|lemma|structure|instance)\s+([^\s(:]+)')
    inventory = re.findall(pattern, baseline, re.M)
    assert inventory == [n.rsplit('.', 1)[-1] for n in NAMES]
    assert len(inventory) == 39
    for name, text in result.items():
        assert blob(text.encode()) == EXPECTED[name], ('candidate SHA mismatch', name)
        assert re.findall(pattern, text, re.M) == inventory
    return result


def pins(root: pathlib.Path) -> None:
    from scripts.check_kuuos_lean_lsp_mcp_compatibility_v7_17 import require_pins
    assert require_pins(root)['mathlib_sha'] == '5450b53e5ddc75d46418fabb605edbf36bd0beb6'
    assert blob((root / DEP).read_bytes()) == DEP_BLOB
    assert blob((root / 'scripts/kuuos_lean_mcp_repair_loop_v1.py').read_bytes()) == CORE_BLOB
    for path, expected in DEPENDENCIES.items():
        assert blob((root / path).read_bytes()) == expected, ('dependency changed', path)


def command(root: pathlib.Path, args: list[str], logfile: pathlib.Path, timeout: int = 600):
    p = subprocess.run(args, cwd=root, text=True, capture_output=True, timeout=timeout)
    logfile.write_text(p.stdout + '\n' + p.stderr, encoding='utf-8')
    print(p.stdout, p.stderr, flush=True)
    return p


def strict_build(root: pathlib.Path, out: pathlib.Path) -> None:
    p = command(root, ['lake', '-KleanArgs=-DwarningAsError=true',
        '-KleanArgs=-DsorryAsError=true', 'build', NS], out / 'strict-build.log', 3600)
    assert p.returncode == 0, 'strict dependency build failed'


def verify_mcp(receipt: dict, source: bytes) -> None:
    assert receipt['status'] == 'LOCAL_LEAN_GREEN_CANDIDATE_ONLY'
    assert receipt['candidate_sha256'] == hashlib.sha256(source).hexdigest()
    assert receipt['original_sha256'] == receipt['candidate_sha256']
    assert receipt['provider_calls'] == 0, 'MCP may verify only the directly successful source'
    assert receipt['source_restored'] and not receipt['git_write_performed']
    assert not receipt['independent_ci_success']
    assert len(receipt['rounds']) == 1
    r = receipt['rounds'][0]
    assert r['semantic_success'] and not r['partial'] and r['errors'] == 0
    assert r['source_sha256'] == receipt['candidate_sha256']
    assert not any(d.get('severity') in {'warning', 'error'} for d in r['diagnostics'])
    assert r['direct_lean']['exit_code'] == 0 and r['forbidden_final_count'] == 0


def direct(root: pathlib.Path, out: pathlib.Path) -> None:
    from scripts.kuuos_lean_mcp_repair_loop_v1 import run_loop, mcp_tactic_provider, mask_lean_comments, FORBIDDEN_NEW
    pins(root)
    target = root / REL
    original = target.read_bytes()
    assert blob(original) == os.environ['CHECKOUT_BLOB']
    assert blob(original) in {BASE, *EXPECTED.values()}
    baseline = (root / 'legacy/v5.291' / REL).read_text(encoding='utf-8')
    variants = candidates(baseline)
    rows = []
    manifest = None
    try:
        for name, text in [('baseline', baseline), *variants.items()]:
            assert not FORBIDDEN_NEW.findall(mask_lean_comments(text))
            target.write_text(text, encoding='utf-8')
            with tempfile.TemporaryDirectory(prefix='kuuos-v155-') as tmp:
                olean = pathlib.Path(tmp) / 'candidate.olean'
                p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
                    '-Dweak.sorryAsError=true', '-o', str(olean), REL], out / (name + '.log'))
                log = p.stdout + '\n' + p.stderr
                errors = re.findall(r'^.*\berror(?:\([^)]*\))?:.*$', log, re.M)
                row = {'candidate': name, 'blob': blob(text.encode()),
                    'source_sha256': hashlib.sha256(text.encode()).hexdigest(),
                    'head': os.environ['SOURCE_HEAD'], 'dependencies': DEPENDENCIES,
                    'lean': 'leanprover/lean4:v4.30.0-rc2',
                    'mathlib': '5450b53e5ddc75d46418fabb605edbf36bd0beb6',
                    'exit_code': p.returncode,
                    'errors': errors, 'success': p.returncode == 0 and olean.is_file() and not errors and 'sorryAx' not in log}
                rows.append(row)
                (out / 'candidates.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
                print('KUUOS_V155_DIRECT ' + json.dumps(row, ensure_ascii=False), flush=True)
        assert not rows[0]['success'] and 'Invalid field' in (out / 'baseline.log').read_text()
        selected = next((r for r in rows if r['candidate'] == 'explicit-comparison' and r['success']), None)
        if selected is None:
            selected = next((r for r in rows[1:] if r['success']), None)
        assert selected is not None, 'no directly verified candidate'
        source = variants[selected['candidate']].encode()
        target.write_bytes(source)
        strict_build(root, out)
        receipt = run_loop(root=root, rel_file=REL, output_dir=out / 'live-mcp',
            expected_sha256=hashlib.sha256(source).hexdigest(), provider=mcp_tactic_provider, max_iterations=1)
        (out / 'mcp.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2))
        verify_mcp(receipt, source)
        (out / 'source.lean').write_bytes(source)
        (out / 'public-root-test.py').write_bytes((root / 'tests/test_public_root_restoration.py').read_bytes())
        (out / 'workflow.yml').write_bytes((root / WORKFLOW).read_bytes())
        (out / 'candidate-script.py').write_bytes((root / 'scripts/ci_kuuos_v155_codeai.py').read_bytes())
        manifest = {'head': os.environ['SOURCE_HEAD'], 'checkout_blob': blob(original),
            'selected': selected, 'source_sha256': hashlib.sha256(source).hexdigest(),
            'dependencies': DEPENDENCIES, 'baseline_blob': BASE,
            'git_write_performed': False, 'independent_ci_success': False}
    finally:
        target.write_bytes(original)
    assert target.read_bytes() == original
    assert manifest is not None
    manifest['source_restored'] = True
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2))
    print('KUUOS_V155_DIRECT_AND_REAL_MCP_SUCCESS ' + json.dumps(manifest), flush=True)


def independent(root: pathlib.Path, out: pathlib.Path) -> None:
    pins(root)
    m = json.loads((out / 'manifest.json').read_text())
    receipt = json.loads((out / 'mcp.json').read_text())
    source = (out / 'source.lean').read_bytes()
    target = root / REL
    original = target.read_bytes()
    variants = candidates((root / 'legacy/v5.291' / REL).read_text(encoding='utf-8'))
    selected = m['selected']
    assert m['head'] == os.environ['SOURCE_HEAD']
    assert blob(original) == m['checkout_blob'] == os.environ['CHECKOUT_BLOB']
    assert m['dependencies'] == DEPENDENCIES and m['baseline_blob'] == BASE
    assert source == variants[selected['candidate']].encode()
    assert blob(source) == selected['blob'] == EXPECTED[selected['candidate']]
    assert hashlib.sha256(source).hexdigest() == m['source_sha256']
    assert selected['success'] and selected['exit_code'] == 0 and not selected['errors']
    assert m['source_restored'] and not m['git_write_performed'] and not m['independent_ci_success']
    assert (out / 'candidate-script.py').read_bytes() == (root / 'scripts/ci_kuuos_v155_codeai.py').read_bytes()
    assert (out / 'workflow.yml').read_bytes() == (root / WORKFLOW).read_bytes()
    assert (out / 'public-root-test.py').read_bytes() == (root / 'tests/test_public_root_restoration.py').read_bytes()
    verify_mcp(receipt, source)
    audit = root / 'formal/KUOS/DependentOriginationV155IndependentAudit.lean'
    assert not audit.exists()
    try:
        target.write_bytes(source)
        strict_build(root, out)
        audit.write_text('import ' + NS + '\n' + '\n'.join('#print axioms ' + NS + '.' + n for n in NAMES) + '\n')
        p = command(root, ['lake', 'env', 'lean', '-DwarningAsError=true',
            '-Dweak.sorryAsError=true', str(audit)], out / 'axioms.log')
        log = p.stdout + '\n' + p.stderr
        assert p.returncode == 0 and 'sorryAx' not in log and 'error:' not in log
        rows = re.findall(r"'([^']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)", log, re.S)
        assert len(rows) == len(NAMES) == 39
        assert {n for n, _ in rows} == {NS + '.' + n for n in NAMES}
        for _, axioms in rows:
            assert {x.strip() for x in axioms.split(',') if x.strip()} <= {'propext', 'Classical.choice', 'Quot.sound'}
        print('KUUOS_V155_INDEPENDENT_39_DECLARATIONS_STANDARD_AXIOMS_SUCCESS', flush=True)
    finally:
        target.write_bytes(original)
        audit.unlink(missing_ok=True)
    assert target.read_bytes() == original


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=['direct', 'independent', 'plan'])
    ap.add_argument('directory', type=pathlib.Path)
    args = ap.parse_args()
    if args.mode == 'plan':
        print(json.dumps({n: blob(s.encode()) for n, s in candidates(args.directory.read_text()).items()}, indent=2))
        return
    root = pathlib.Path('.').resolve()
    out = args.directory.resolve()
    assert not out.is_relative_to(root)
    out.mkdir(parents=True, exist_ok=True)
    (direct if args.mode == 'direct' else independent)(root, out)


if __name__ == '__main__':
    main()
