import KUOS.DependentOriginationDoubleDeloopingUniverseTransportV1_106_1

namespace KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeABV1_106_2

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationDoubleDeloopingUniverseTransportV1_106_1

universe u

noncomputable section

/-!
# Universe transport for standard type-(A)/(B) generators v1.106.2

The concrete B²ℕ separator is proved in universe zero.  Version v1.106.1
constructed the fully faithful pointwise `ULift` functor on scaled simplicial
sets together with the native standard-simplex and horn universe isomorphisms.

This file identifies the lifted low-universe standard type-(A) and type-(B)
generators with the native generators in an arbitrary universe.  The carrier
identifications are the v1.106.1 simplex/horn isomorphisms; the only remaining
work is to show that the standard scaling predicates are invariant under those
identifications.  We then package the commuting source/target isomorphisms as
isomorphisms in `Arrow ScaledSSet` and transport lifting properties with
Mathlib's `HasLiftingProperty.of_arrow_iso_left`.
-/

/-! ## Minimal standard-simplex scaling -/

/-- Minimal thinness on a low-universe standard simplex is equivalent to
minimal thinness on the native high-universe simplex under the canonical
simplex universe isomorphism. -/
theorem minimalStdSimplexUlift_iff
    {n : Nat}
    (t : ((SSet.uliftFunctor.{u, 0}).obj
      (Δ[n] : SSet.{0})).obj (op ⦋2⦌)) :
    (minimalScaling (Δ[n] : SSet.{0})).thin t.down ↔
      (minimalScaling (Δ[n] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} n).hom.app (op ⦋2⦌) t) := by
  constructor
  · intro ht
    have hLift :
        (minimalScaling
          ((SSet.uliftFunctor.{u, 0}).obj
            (Δ[n] : SSet.{0}))).thin t :=
      (uliftScaling_minimal_iff t).1 ht
    exact
      (minimalScaling_iso_iff (stdSimplexUliftIso.{u} n) t).1 hLift
  · intro ht
    have hLift :
        (minimalScaling
          ((SSet.uliftFunctor.{u, 0}).obj
            (Δ[n] : SSet.{0}))).thin t :=
      (minimalScaling_iso_iff (stdSimplexUliftIso.{u} n) t).2 ht
    exact (uliftScaling_minimal_iff t).2 hLift

/-! ## Type-(A) scaling and generator transport -/

/-- The standard type-(A) simplex scaling is preserved and reflected by the
canonical standard-simplex universe isomorphism. -/
theorem standardTypeASimplexScaling_ulift_iff
    {n : Nat}
    (i : Fin (n + 1))
    (t : ((SSet.uliftFunctor.{u, 0}).obj
      (Δ[n] : SSet.{0})).obj (op ⦋2⦌)) :
    (uliftScaling
      (standardTypeASimplexScaling i :
        ScaledSimplicialSet (Δ[n] : SSet.{0}))).thin t ↔
      (standardTypeASimplexScaling i :
        ScaledSimplicialSet (Δ[n] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} n).hom.app (op ⦋2⦌) t) := by
  change
    ((minimalScaling (Δ[n] : SSet.{0})).thin t.down ∨
      IsStandardTypeADistinguishedTriangle i t.down) ↔
    ((minimalScaling (Δ[n] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} n).hom.app (op ⦋2⦌) t) ∨
      IsStandardTypeADistinguishedTriangle i
        ((stdSimplexUliftIso.{u} n).hom.app (op ⦋2⦌) t))
  constructor
  · intro ht
    rcases ht with hmin | hdist
    · exact Or.inl ((minimalStdSimplexUlift_iff t).1 hmin)
    · exact Or.inr (by
        simpa only [IsStandardTypeADistinguishedTriangle,
          stdSimplexUliftIso_hom_apply] using hdist)
  · intro ht
    rcases ht with hmin | hdist
    · exact Or.inl ((minimalStdSimplexUlift_iff t).2 hmin)
    · exact Or.inr (by
        simpa only [IsStandardTypeADistinguishedTriangle,
          stdSimplexUliftIso_hom_apply] using hdist)

/-- The pullback type-(A) horn scaling is likewise invariant under the horn
universe isomorphism. -/
theorem standardTypeAHornScaling_ulift_iff
    {n : Nat}
    (i : Fin (n + 1))
    (t : ((SSet.uliftFunctor.{u, 0}).obj
      (Λ[n, i] : SSet.{0})).obj (op ⦋2⦌)) :
    (uliftScaling
      (standardTypeAHornScaling i :
        ScaledSimplicialSet (Λ[n, i] : SSet.{0}))).thin t ↔
      (standardTypeAHornScaling i :
        ScaledSimplicialSet (Λ[n, i] : SSet.{u})).thin
        ((hornUliftIso.{u} n i).hom.app (op ⦋2⦌) t) := by
  change
    (standardTypeASimplexScaling i :
      ScaledSimplicialSet (Δ[n] : SSet.{0})).thin t.down.1 ↔
    (standardTypeASimplexScaling i :
      ScaledSimplicialSet (Δ[n] : SSet.{u})).thin
      ((stdSimplexUliftIso.{u} n).hom.app (op ⦋2⦌)
        (ULift.up t.down.1))
  exact standardTypeASimplexScaling_ulift_iff i (ULift.up t.down.1)

/-- Lifted low-universe type-(A) simplex and native high-universe type-(A)
simplex are isomorphic as scaled simplicial sets. -/
def standardTypeAScaledSimplexUliftIso
    (g : StandardTypeAHornGeneratorIndex) :
    scaledUliftObj.{u} (standardTypeAScaledSimplex.{0} g) ≅
      standardTypeAScaledSimplex.{u} g := by
  refine scaledIsoOfCarrierIso (stdSimplexUliftIso.{u} g.n) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (standardTypeASimplexScaling g.i :
          ScaledSimplicialSet (Δ[g.n] : SSet.{0}))).thin t at ht
    change
      (standardTypeASimplexScaling g.i :
        ScaledSimplicialSet (Δ[g.n] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} g.n).hom.app (op ⦋2⦌) t)
    exact (standardTypeASimplexScaling_ulift_iff g.i t).1 ht
  · intro t ht
    change
      (standardTypeASimplexScaling g.i :
        ScaledSimplicialSet (Δ[g.n] : SSet.{u})).thin t at ht
    change
      (uliftScaling
        (standardTypeASimplexScaling g.i :
          ScaledSimplicialSet (Δ[g.n] : SSet.{0}))).thin
        ((stdSimplexUliftIso.{u} g.n).inv.app (op ⦋2⦌) t)
    apply (standardTypeASimplexScaling_ulift_iff g.i
      ((stdSimplexUliftIso.{u} g.n).inv.app (op ⦋2⦌) t)).2
    simpa using ht

/-- Lifted low-universe type-(A) horn and native high-universe type-(A) horn
are isomorphic as scaled simplicial sets. -/
def standardTypeAScaledHornUliftIso
    (g : StandardTypeAHornGeneratorIndex) :
    scaledUliftObj.{u} (standardTypeAScaledHorn.{0} g) ≅
      standardTypeAScaledHorn.{u} g := by
  refine scaledIsoOfCarrierIso (hornUliftIso.{u} g.n g.i) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (standardTypeAHornScaling g.i :
          ScaledSimplicialSet (Λ[g.n, g.i] : SSet.{0}))).thin t at ht
    change
      (standardTypeAHornScaling g.i :
        ScaledSimplicialSet (Λ[g.n, g.i] : SSet.{u})).thin
        ((hornUliftIso.{u} g.n g.i).hom.app (op ⦋2⦌) t)
    exact (standardTypeAHornScaling_ulift_iff g.i t).1 ht
  · intro t ht
    change
      (standardTypeAHornScaling g.i :
        ScaledSimplicialSet (Λ[g.n, g.i] : SSet.{u})).thin t at ht
    change
      (uliftScaling
        (standardTypeAHornScaling g.i :
          ScaledSimplicialSet (Λ[g.n, g.i] : SSet.{0}))).thin
        ((hornUliftIso.{u} g.n g.i).inv.app (op ⦋2⦌) t)
    apply (standardTypeAHornScaling_ulift_iff g.i
      ((hornUliftIso.{u} g.n g.i).inv.app (op ⦋2⦌) t)).2
    simpa using ht

/-- The lifted low-universe type-(A) generator is isomorphic, as an arrow, to
the native high-universe generator with the same index. -/
def standardTypeAGeneratorUliftArrowIso
    (g : StandardTypeAHornGeneratorIndex) :
    Arrow.mk
        ((scaledUliftFunctor.{u}).map
          (standardTypeAScaledHornGeneratorHom.{0} g)) ≅
      Arrow.mk (standardTypeAScaledHornGeneratorHom.{u} g) :=
  Arrow.isoMk'
    ((scaledUliftFunctor.{u}).map
      (standardTypeAScaledHornGeneratorHom.{0} g))
    (standardTypeAScaledHornGeneratorHom.{u} g)
    (standardTypeAScaledHornUliftIso.{u} g)
    (standardTypeAScaledSimplexUliftIso.{u} g)
    (by
      apply ScaledSSet.ScaledMap.ext
      exact hornUliftIso_hom_ι g.n g.i)

/-- Any low-universe lifting property against a type-(A) generator transports
to the native type-(A) generator in an arbitrary universe. -/
theorem hasLiftingProperty_standardTypeA_ulift
    (g : StandardTypeAHornGeneratorIndex)
    {P Q : ScaledSSet.{0}}
    (p : P ⟶ Q)
    (h : HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom.{0} g) p) :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom.{u} g)
      ((scaledUliftFunctor.{u}).map p) := by
  have hmap :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map
          (standardTypeAScaledHornGeneratorHom.{0} g))
        ((scaledUliftFunctor.{u}).map p) :=
    hasLiftingProperty_map_of_full_faithful
      (scaledUliftFunctor.{u}) h
  letI :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map
          (standardTypeAScaledHornGeneratorHom.{0} g))
        ((scaledUliftFunctor.{u}).map p) := hmap
  exact HasLiftingProperty.of_arrow_iso_left
    (standardTypeAGeneratorUliftArrowIso.{u} g)
    ((scaledUliftFunctor.{u}).map p)

/-! ## Type-(B) scaling and generator transport -/

/-- The five extra source triangles of type-(B) are preserved and reflected by
the standard-simplex universe isomorphism. -/
theorem standardTypeBSourceScaling_ulift_iff
    (t : ((SSet.uliftFunctor.{u, 0}).obj
      (Δ[4] : SSet.{0})).obj (op ⦋2⦌)) :
    (uliftScaling
      (standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin t ↔
      (standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t) := by
  change
    ((minimalScaling (Δ[4] : SSet.{0})).thin t.down ∨
      IsStandardTypeBSourceTriangle t.down) ↔
    ((minimalScaling (Δ[4] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t) ∨
      IsStandardTypeBSourceTriangle
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t))
  constructor
  · intro ht
    rcases ht with hmin | htri
    · exact Or.inl ((minimalStdSimplexUlift_iff t).1 hmin)
    · exact Or.inr (by
        simpa only [IsStandardTypeBSourceTriangle, IsStandardVertexTriangle,
          stdSimplexUliftIso_hom_apply] using htri)
  · intro ht
    rcases ht with hmin | htri
    · exact Or.inl ((minimalStdSimplexUlift_iff t).2 hmin)
    · exact Or.inr (by
        simpa only [IsStandardTypeBSourceTriangle, IsStandardVertexTriangle,
          stdSimplexUliftIso_hom_apply] using htri)

/-- The full type-(B) target scaling is preserved and reflected by the same
standard-simplex universe isomorphism. -/
theorem standardTypeBTargetScaling_ulift_iff
    (t : ((SSet.uliftFunctor.{u, 0}).obj
      (Δ[4] : SSet.{0})).obj (op ⦋2⦌)) :
    (uliftScaling
      (standardTypeBTargetScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin t ↔
      (standardTypeBTargetScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t) := by
  change
    ((standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{0})).thin t.down ∨
      IsStandardVertexTriangle (0 : Fin 5) 1 4 t.down ∨
      IsStandardVertexTriangle (0 : Fin 5) 3 4 t.down) ↔
    ((standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin
          ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t) ∨
      IsStandardVertexTriangle (0 : Fin 5) 1 4
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t) ∨
      IsStandardVertexTriangle (0 : Fin 5) 3 4
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t))
  constructor
  · intro ht
    rcases ht with hsrc | hrest
    · exact Or.inl ((standardTypeBSourceScaling_ulift_iff t).1 hsrc)
    · rcases hrest with h014 | h034
      · exact Or.inr (Or.inl (by
          simpa only [IsStandardVertexTriangle,
            stdSimplexUliftIso_hom_apply] using h014))
      · exact Or.inr (Or.inr (by
          simpa only [IsStandardVertexTriangle,
            stdSimplexUliftIso_hom_apply] using h034))
  · intro ht
    rcases ht with hsrc | hrest
    · exact Or.inl ((standardTypeBSourceScaling_ulift_iff t).2 hsrc)
    · rcases hrest with h014 | h034
      · exact Or.inr (Or.inl (by
          simpa only [IsStandardVertexTriangle,
            stdSimplexUliftIso_hom_apply] using h014))
      · exact Or.inr (Or.inr (by
          simpa only [IsStandardVertexTriangle,
            stdSimplexUliftIso_hom_apply] using h034))

/-- Lifted low-universe type-(B) source and native high-universe source are
isomorphic as scaled simplicial sets. -/
def standardTypeBSourceUliftIso :
    scaledUliftObj.{u} (standardTypeBSource.{0}) ≅
      standardTypeBSource.{u} := by
  refine scaledIsoOfCarrierIso (stdSimplexUliftIso.{u} 4) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (standardTypeBSourceScaling :
          ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin t at ht
    change
      (standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t)
    exact (standardTypeBSourceScaling_ulift_iff t).1 ht
  · intro t ht
    change
      (standardTypeBSourceScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin t at ht
    change
      (uliftScaling
        (standardTypeBSourceScaling :
          ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin
        ((stdSimplexUliftIso.{u} 4).inv.app (op ⦋2⦌) t)
    apply (standardTypeBSourceScaling_ulift_iff
      ((stdSimplexUliftIso.{u} 4).inv.app (op ⦋2⦌) t)).2
    simpa using ht

/-- Lifted low-universe type-(B) target and native high-universe target are
isomorphic as scaled simplicial sets. -/
def standardTypeBTargetUliftIso :
    scaledUliftObj.{u} (standardTypeBTarget.{0}) ≅
      standardTypeBTarget.{u} := by
  refine scaledIsoOfCarrierIso (stdSimplexUliftIso.{u} 4) ?_ ?_
  · intro t ht
    change
      (uliftScaling
        (standardTypeBTargetScaling :
          ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin t at ht
    change
      (standardTypeBTargetScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin
        ((stdSimplexUliftIso.{u} 4).hom.app (op ⦋2⦌) t)
    exact (standardTypeBTargetScaling_ulift_iff t).1 ht
  · intro t ht
    change
      (standardTypeBTargetScaling :
        ScaledSimplicialSet (Δ[4] : SSet.{u})).thin t at ht
    change
      (uliftScaling
        (standardTypeBTargetScaling :
          ScaledSimplicialSet (Δ[4] : SSet.{0}))).thin
        ((stdSimplexUliftIso.{u} 4).inv.app (op ⦋2⦌) t)
    apply (standardTypeBTargetScaling_ulift_iff
      ((stdSimplexUliftIso.{u} 4).inv.app (op ⦋2⦌) t)).2
    simpa using ht

/-- The lifted low-universe type-(B) generator is isomorphic, as an arrow, to
the native high-universe type-(B) generator. -/
def standardTypeBGeneratorUliftArrowIso :
    Arrow.mk
        ((scaledUliftFunctor.{u}).map standardTypeBGeneratorHom.{0}) ≅
      Arrow.mk standardTypeBGeneratorHom.{u} :=
  Arrow.isoMk'
    ((scaledUliftFunctor.{u}).map standardTypeBGeneratorHom.{0})
    standardTypeBGeneratorHom.{u}
    (standardTypeBSourceUliftIso.{u})
    (standardTypeBTargetUliftIso.{u})
    (by
      apply ScaledSSet.ScaledMap.ext
      change
        (stdSimplexUliftIso.{u} 4).hom ≫ 𝟙 (Δ[4] : SSet.{u}) =
          (SSet.uliftFunctor.{u, 0}).map (𝟙 (Δ[4] : SSet.{0})) ≫
            (stdSimplexUliftIso.{u} 4).hom
      simp)

/-- Any low-universe lifting property against the type-(B) generator transports
to the native type-(B) generator in an arbitrary universe. -/
theorem hasLiftingProperty_standardTypeB_ulift
    {P Q : ScaledSSet.{0}}
    (p : P ⟶ Q)
    (h : HasLiftingProperty standardTypeBGeneratorHom.{0} p) :
    HasLiftingProperty
      standardTypeBGeneratorHom.{u}
      ((scaledUliftFunctor.{u}).map p) := by
  have hmap :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map standardTypeBGeneratorHom.{0})
        ((scaledUliftFunctor.{u}).map p) :=
    hasLiftingProperty_map_of_full_faithful
      (scaledUliftFunctor.{u}) h
  letI :
      HasLiftingProperty
        ((scaledUliftFunctor.{u}).map standardTypeBGeneratorHom.{0})
        ((scaledUliftFunctor.{u}).map p) := hmap
  exact HasLiftingProperty.of_arrow_iso_left
    (standardTypeBGeneratorUliftArrowIso.{u})
    ((scaledUliftFunctor.{u}).map p)

end

end KUOS.DependentOriginationDoubleDeloopingUniverseTransportTypeABV1_106_2
