import KUOS.DependentOriginationCrossUniverseTypeAScalingV1_29

/-!
# Actual native type-(A) scaling invariance across independent universes

The represented simplex universe comparison preserves vertices and all
degeneracies. Consequently it preserves BOTH components of the standard
type-(A) thinness predicate: degenerate two-simplices and the distinguished
consecutive triangle. Naturality of the horn inclusion extends this to
the canonical pullback horn scaling.

This file DISCHARGES, rather than postulates, the two exact equalities
isolated in NativeTypeAUniverseScalingCompatibility. No inner-horn RLP,
scaled-anodyne generator equivalence, or unconditional Duskin fibrancy
is inferred.
-/

namespace KUOS.DependentOriginationNativeTypeAUniverseGeometryV1_29

open CategoryTheory Simplicial Opposite
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationULiftHornUniverseComparisonV1_29
open KUOS.DependentOriginationULiftScaledHornFillerForwardV1_29
open KUOS.DependentOriginationULiftScalingDescentV1_29
open KUOS.DependentOriginationULiftScalingRoundTripV1_29
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationCrossUniverseTypeAScalingV1_29

universe u v

/-- Every vertex of a represented 2-simplex is unchanged by the true
simplex universe comparison. This uses the pinned Yoneda order-hom API. -/
theorem typeAVertex_universe
    (n : Nat)
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    (j : Fin 3) :
    (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) j = t j := by
  have he := simplexUniverseEquiv_objEquiv.{u, v} n (op ⦋2⦌) t
  have hj := congrArg (fun f : ⦋2⦌ ⟶ ⦋n⦌ => f.toOrderHom j) he
  simpa only [SSet.stdSimplex.objEquiv_toOrderHom_apply] using hj

/-- The specified consecutive type-(A) triangle has exactly the same
vertex-index conditions at both independent universe levels. -/
theorem typeADistinguished_universe_iff
    {n : Nat} (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) :
    IsStandardTypeADistinguishedTriangle.{u} i t ↔
      IsStandardTypeADistinguishedTriangle.{max u v} i
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) := by
  simp only [IsStandardTypeADistinguishedTriangle,
    typeAVertex_universe.{u, v} n t]

/-- Minimal thinness (each of the two degeneracies of a 1-simplex) is
preserved and reflected by the actual natural represented simplex
equivalence. The backward direction uses its certified inverse. -/
theorem minimalScaling_universe_iff
    (n : Nat) (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) :
    (minimalScaling (Δ[n] : SSet.{u})).thin t ↔
      (minimalScaling (Δ[n] : SSet.{max u v})).thin
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) := by
  constructor
  · intro ht
    rcases ht with ⟨x, hx⟩ | ⟨x, hx⟩
    · left
      refine ⟨simplexUniverseEquiv.{u, v} n (op ⦋1⦌) x, ?_⟩
      change
        (Δ[n] : SSet.{max u v}).σ 0
            (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) x) =
          simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t
      rw [← simplexUniverseEquiv_natural.{u, v} n
        ((SimplexCategory.σ 0).op) x, hx]
    · right
      refine ⟨simplexUniverseEquiv.{u, v} n (op ⦋1⦌) x, ?_⟩
      change
        (Δ[n] : SSet.{max u v}).σ 1
            (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) x) =
          simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t
      rw [← simplexUniverseEquiv_natural.{u, v} n
        ((SimplexCategory.σ 1).op) x, hx]
  · intro ht
    rcases ht with ⟨x, hx⟩ | ⟨x, hx⟩
    · left
      let y := (simplexUniverseEquiv.{u, v} n (op ⦋1⦌)).symm x
      refine ⟨y, ?_⟩
      apply (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)).injective
      calc
        simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
            ((Δ[n] : SSet.{u}).σ 0 y) =
          (Δ[n] : SSet.{max u v}).σ 0
            (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) y) :=
          simplexUniverseEquiv_natural.{u, v} n
            ((SimplexCategory.σ 0).op) y
        _ = (Δ[n] : SSet.{max u v}).σ 0 x := by simp [y]
        _ = simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t := hx
    · right
      let y := (simplexUniverseEquiv.{u, v} n (op ⦋1⦌)).symm x
      refine ⟨y, ?_⟩
      apply (simplexUniverseEquiv.{u, v} n (op ⦋2⦌)).injective
      calc
        simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
            ((Δ[n] : SSet.{u}).σ 1 y) =
          (Δ[n] : SSet.{max u v}).σ 1
            (simplexUniverseEquiv.{u, v} n (op ⦋1⦌) y) :=
          simplexUniverseEquiv_natural.{u, v} n
            ((SimplexCategory.σ 1).op) y
        _ = (Δ[n] : SSet.{max u v}).σ 1 x := by simp [y]
        _ = simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t := hx

/-- Both genuinely geometric clauses of type-(A) thinness survive
and reflect across independent represented simplex universes. -/
theorem standardTypeASimplexScaling_universe_iff
    {n : Nat} (i : Fin (n + 1))
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) :
    (standardTypeASimplexScaling.{u} i).thin t ↔
      (standardTypeASimplexScaling.{max u v} i).thin
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) := by
  change
    ((minimalScaling (Δ[n] : SSet.{u})).thin t ∨
      IsStandardTypeADistinguishedTriangle.{u} i t) ↔
    ((minimalScaling (Δ[n] : SSet.{max u v})).thin
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) ∨
      IsStandardTypeADistinguishedTriangle.{max u v} i
        (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t))
  exact or_congr
    (minimalScaling_universe_iff.{u, v} n t)
    (typeADistinguished_universe_iff.{u, v} i t)

/-- Extensionality of actual scaled simplicial structures, with no
forgetting of the two thin-degeneracy proof fields. -/
private theorem scaling_eq_of_thin
    {X : SSet.{u}}
    (s t : ScaledSimplicialSet X)
    (h : ∀ x, s.thin x ↔ t.thin x) : s = t := by
  cases s with
  | mk thinS zeroS oneS =>
    cases t with
    | mk thinT zeroT oneT =>
      have hp : thinS = thinT := funext (fun x => propext (h x))
      cases hp
      rfl

/-- The NATIVE high-universe type-(A) simplex scaling un-lifts to
the ORIGINAL low-universe type-(A) scaling. -/
theorem unlift_nativeTypeASimplexScaling
    {n : Nat} (i : Fin (n + 1)) :
    unliftSimplexScaling.{u, v} n
      (standardTypeASimplexScaling.{max u v} i) =
        standardTypeASimplexScaling.{u} i := by
  apply scaling_eq_of_thin
  intro t
  change
    (standardTypeASimplexScaling.{max u v} i).thin
      (simplexUniverseEquiv.{u, v} n (op ⦋2⦌) t) ↔
    (standardTypeASimplexScaling.{u} i).thin t
  exact (standardTypeASimplexScaling_universe_iff.{u, v} i t).symm

/-- Naturality of the horn inclusion transports the exact type-(A)
pullback horn scaling. No independent horn thinness assumption remains. -/
theorem unlift_nativeTypeAHornScaling
    {n : Nat} (i : Fin (n + 1)) :
    unliftHornScaling.{u, v} n i
      (standardTypeAHornScaling.{max u v} i) =
        standardTypeAHornScaling.{u} i := by
  apply scaling_eq_of_thin
  intro t
  change
    (standardTypeASimplexScaling.{max u v} i).thin
      ((SSet.horn.{max u v} n i).ι.app (op ⦋2⦌)
        (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t)) ↔
    (standardTypeASimplexScaling.{u} i).thin
      ((SSet.horn.{u} n i).ι.app (op ⦋2⦌) t)
  have hIncl :
      (SSet.horn.{max u v} n i).ι.app (op ⦋2⦌)
          (hornUniverseEquiv.{u, v} n i (op ⦋2⦌) t) =
        simplexUniverseEquiv.{u, v} n (op ⦋2⦌)
          ((SSet.horn.{u} n i).ι.app (op ⦋2⦌) t) := rfl
  rw [hIncl]
  exact (standardTypeASimplexScaling_universe_iff.{u, v}
    i ((SSet.horn.{u} n i).ι.app (op ⦋2⦌) t)).symm

/-- CONSTRUCT the formerly external native high-universe type-(A)
scaling compatibility certificate from vertex, degeneracy and horn
naturality. Both exact structural equalities are now proved. -/
noncomputable def nativeTypeAUniverseScalingCompatibility :
    NativeTypeAUniverseScalingCompatibility.{u, v} where
  simplex := by
    intro n i
    have h := congrArg (liftedSimplexScaling.{u, v} n)
      (unlift_nativeTypeASimplexScaling.{u, v} i)
    rw [lift_unliftSimplexScaling.{u, v} n
      (standardTypeASimplexScaling.{max u v} i)] at h
    exact h.symm
  horn := by
    intro n i
    have h := congrArg (liftedHornScaling.{u, v} n i)
      (unlift_nativeTypeAHornScaling.{u, v} i)
    rw [lift_unliftHornScaling.{u, v} n i
      (standardTypeAHornScaling.{max u v} i)] at h
    exact h.symm

/-- Actual UNCONDITIONAL cross-universe comparison of the native type-(A)
families as fibrancy PREDICATES on a true ULift simplicial carrier.
This is a transport theorem, not an unconditional fibrancy proof. -/
theorem nativeTypeA_fibrancy_iff
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    HasScaledHornFillers X sX (standardTypeAScaledHornFamily X sX) ↔
      HasScaledHornFillers
        ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)
        (standardTypeAScaledHornFamily
          ((SSet.uliftFunctor.{v, u}).obj X) (uliftScaling.{u, v} sX)) :=
  nativeTypeA_fibrancy_iff_of_scaling_compatibility.{u, v}
    sX nativeTypeAUniverseScalingCompatibility

#print axioms typeAVertex_universe
#print axioms typeADistinguished_universe_iff
#print axioms minimalScaling_universe_iff
#print axioms standardTypeASimplexScaling_universe_iff
#print axioms unlift_nativeTypeASimplexScaling
#print axioms unlift_nativeTypeAHornScaling
#print axioms nativeTypeAUniverseScalingCompatibility
#print axioms nativeTypeA_fibrancy_iff

end KUOS.DependentOriginationNativeTypeAUniverseGeometryV1_29
