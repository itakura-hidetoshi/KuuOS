import Kuu.F112.PolygonNativeF55P94DFiniteGlobularPresentation
import Mathlib.Tactic

/-!
# F112-P94D3AW — all-finite coherence obstruction and Peiffer boundary

Every finite cutoff N inherits AV's ORIGINAL source-dependent C60 14D
proof fiber and true AQ Type-valued 15D comparisons.

The new results do not merely append a 16D generator:
* For EVERY dimension below a chosen finite cutoff, define the typed
  parallel boundary of a genuine higher cell, and characterize complete
  filling by the surjectivity of ALL finite boundary maps.
* A receiver on any cell dimension that is conserved by ACTUAL higher
  generators obstructs filling whenever its two endpoint values differ.
* Give a CONCRETE empty-higher extension for EVERY finite N, without
  faking any 16D cell. This refutes the claim that formal finite
  globularity or equality of group invariants forces higher fillers.
* Specialize the obstruction at the original C60 15D naturality
  boundary to the noncommutative AS Peiffer kernel. Its shadow is
  equal on AU's two actual 15D paths, but this equality is demonstrably
  NOT sufficient for a genuine 16D filler in an arbitrary finite tower.

All higher structures and receiver-conservation laws are explicitly
data/assumptions, not consequences of an algebraic crossed module.
No sorry, admit, new axioms, Gray, strict global n-category, or
(infinity,3)-hyperdescent.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

/-- The true dependent pair of parallel (k+1)-cell boundaries.
Proof of parallelism is explicit and does not assert a (k+2)-filler. -/
structure NativeFiniteAWParallelBoundary
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N) (k : Nat) where
  left : T.Cell (k + 1)
  right : T.Cell (k + 1)
  parallel : T.Parallel k left right

/-- A real supplied higher cell determines its TWO source-typed
parallel boundaries at any geometric dimension, uniformly in N. -/
def nativeFiniteAWCellBoundary
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (z : T.Cell (k + 2)) :
    NativeFiniteAWParallelBoundary T k :=
  ⟨T.source (k + 1) z, T.target (k + 1) z,
    T.filler_parallel k ⟨z, rfl, rfl⟩⟩

/-- A finite presentation fills every parallel pair at every one
of its N explicitly enabled higher dimensions. No larger infinity
or implicit universal coherence is claimed. -/
def NativeFiniteAWComplete
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N) : Prop :=
  ∀ i : Fin N, ∀ x y : T.Cell (i.val + 1),
    T.Parallel i.val x y → T.HasFiller i.val x y

/-- A single universal finite-dimensional criterion:
a supplied tower is complete iff EACH of its N actual geometric
boundary maps is surjective ONTO THE TYPE OF PARALLEL PAIRS.
This does not claim the maps are surjective in arbitrary models. -/
theorem nativeFiniteAWComplete_iff_surjective
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N) :
    NativeFiniteAWComplete T ↔
      ∀ i : Fin N, Function.Surjective (nativeFiniteAWCellBoundary T i.val) := by
  constructor
  · intro h i pair
    rcases pair with ⟨x, y, hparallel⟩
    rcases h i x y hparallel with ⟨z, hs, ht⟩
    refine ⟨z, ?_⟩
    cases hs
    cases ht
    rfl
  · intro h i x y hparallel
    obtain ⟨z, hz⟩ := h i ⟨x, y, hparallel⟩
    refine ⟨z, ?_, ?_⟩
    · exact congrArg NativeFiniteAWParallelBoundary.left hz
    · exact congrArg NativeFiniteAWParallelBoundary.right hz

/-- A conserved higher-boundary observation is supplied and verified
at ONE arbitrary dimension. It need not be derived from a scalar
charge: any Type-valued receiver is allowed. -/
structure NativeFiniteAWBoundaryObserver
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (B : Type w) where
  observe : T.Cell (k + 1) → B
  preserves : ∀ z : T.Cell (k + 2),
    observe (T.source (k + 1) z) =
      observe (T.target (k + 1) z)

/-- Uniform obstruction theorem. Even if two endpoints are parallel,
NO actual higher cell with those boundaries can exist in a tower
whose prescribed cells conserve an observer separating the endpoints. -/
theorem nativeFiniteAWObserver_noFiller
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    {B : Type w} {k : Nat}
    (T : NativeFiniteAVPresentation A Edge N)
    (obs : NativeFiniteAWBoundaryObserver T k B)
    {x y : T.Cell (k + 1)}
    (hsep : obs.observe x ≠ obs.observe y) :
    ¬ T.HasFiller k x y := by
  rintro ⟨z, hs, ht⟩
  apply hsep
  calc
    obs.observe x = obs.observe (T.source (k + 1) z) :=
      congrArg obs.observe hs.symm
    _ = obs.observe (T.target (k + 1) z) := obs.preserves z
    _ = obs.observe y := congrArg obs.observe ht

/-- The SAME obstruction controls all finitely many enabled levels,
with separately supplied Type-valued receivers at each dimension.
This is not an assumption that every geometry admits such receivers. -/
theorem nativeFiniteAWObservers_noFiller
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N)
    (B : Fin N → Type w)
    (observers : ∀ i : Fin N,
      NativeFiniteAWBoundaryObserver T i.val (B i))
    (i : Fin N) {x y : T.Cell (i.val + 1)}
    (hsep : (observers i).observe x ≠ (observers i).observe y) :
    ¬ T.HasFiller i.val x y :=
  nativeFiniteAWObserver_noFiller T (observers i) hsep

/-- A canonical empty higher cell family is proof-theoretically
uninhabited at EACH finite layer, regardless of the cutoff N. -/
def nativeFiniteAWEmptyHigherElim
    {A : Type u} {Edge : A → A → Type v}
    (N k : Nat) :
    NativeFiniteAVCell A Edge N (fun _ => PEmpty) (k + 2) → PEmpty := by
  intro z
  change (if h : k < N then PEmpty else PEmpty) at z
  by_cases hk : k < N
  · simpa only [dif_pos hk] using z
  · simpa only [dif_neg hk] using z

/-- Every natural finite cutoff N has a completely explicit higher-
EMPTY presentation, with the original 14D/15D base unchanged.
This is a legitimate MODEL, not a proposed geometric construction. -/
def nativeFiniteAWEmptyPresentation
    (A : Type u) (Edge : A → A → Type v) (N : Nat) :
    NativeFiniteAVPresentation A Edge N where
  higher := fun _ => PEmpty
  higherSource := fun k z =>
    (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim
  higherTarget := fun k z =>
    (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim
  source_globular := fun k z =>
    (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim
  target_globular := fun k z =>
    (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim

/-- All candidate higher cells are absent in this PARTICULAR
explicit presentation, even for arbitrarily large finite N. -/
theorem nativeFiniteAWEmpty_noHigher
    (A : Type u) (Edge : A → A → Type v) (N k : Nat) :
    ¬ Nonempty ((nativeFiniteAWEmptyPresentation A Edge N).Cell (k + 2)) := by
  rintro ⟨z⟩
  exact (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim

theorem nativeFiniteAWEmpty_noFiller
    (A : Type u) (Edge : A → A → Type v) (N k : Nat)
    (x y : (nativeFiniteAWEmptyPresentation A Edge N).Cell (k + 1)) :
    ¬ (nativeFiniteAWEmptyPresentation A Edge N).HasFiller k x y := by
  rintro ⟨z, _, _⟩
  exact (nativeFiniteAWEmptyHigherElim (A := A) (Edge := Edge) N k z).elim

/-- If a genuine 15D cell exists, the empty extension fails complete
coherence even at the FIRST enabled higher dimension, uniformly for
all N+1. The original 15D cell is preserved, not erased. -/
theorem nativeFiniteAWEmpty_notComplete
    (A : Type u) (Edge : A → A → Type v) (N : Nat)
    {x y : A} (edge : Edge x y) :
    ¬ NativeFiniteAWComplete (nativeFiniteAWEmptyPresentation A Edge (N + 1)) := by
  intro h
  let T := nativeFiniteAWEmptyPresentation A Edge (N + 1)
  have hboundary : T.Parallel 0 (T.mkFifteen edge) (T.mkFifteen edge) :=
    T.mkFifteen_parallel edge edge
  have hf : T.HasFiller 0 (T.mkFifteen edge) (T.mkFifteen edge) :=
    h ⟨0, Nat.zero_lt_succ N⟩ _ _ hboundary
  exact (nativeFiniteAWEmpty_noFiller A Edge (N + 1) 0 _ _) hf

/-! Genuine C60 Peiffer boundary obstruction, with fully source-indexed data. -/

section PhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Read the TRUE AU/AT 15D noncommutative Peiffer-kernel defect
from a Sigma-packaged, originally source-typed 15D proof.
It is NOT an unrestricted 16D existence witness. -/
def nativeK5AWPeifferObserver
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N) :
    T.Cell 1 → NativeK5ASPeifferKernel W :=
  fun cell => nativeK5ATCellDefect W cell.2

/-- To use Peiffer as a 16D obstruction, preservation across every
ACTUAL 16D cell is a separate hypothesis, not inferred from the
crossed-module's group-level Peiffer identity. -/
structure NativeK5AWPeifferCompatible
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat) where
  presentation : NativeK5AVPhysicalFinitePresentation W N
  preserves : ∀ z : presentation.Cell 2,
    nativeK5AWPeifferObserver W presentation (presentation.source 1 z) =
      nativeK5AWPeifferObserver W presentation (presentation.target 1 z)

/-- Every separately supplied Peiffer-compatible 16D filler forces
equality of original noncommutative defects, for ANY finite cutoff. -/
theorem nativeK5AWPeiffer_filler_necessary
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (C : NativeK5AWPeifferCompatible W N)
    {x y : C.presentation.Cell 1}
    (h : C.presentation.HasFiller 0 x y) :
    nativeK5AWPeifferObserver W C.presentation x =
      nativeK5AWPeifferObserver W C.presentation y := by
  rcases h with ⟨z, hs, ht⟩
  calc
    nativeK5AWPeifferObserver W C.presentation x =
        nativeK5AWPeifferObserver W C.presentation (C.presentation.source 1 z) :=
          congrArg (nativeK5AWPeifferObserver W C.presentation) hs.symm
    _ = nativeK5AWPeifferObserver W C.presentation (C.presentation.target 1 z) :=
      C.preserves z
    _ = nativeK5AWPeifferObserver W C.presentation y :=
      congrArg (nativeK5AWPeifferObserver W C.presentation) ht

theorem nativeK5AWPeiffer_noFiller
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (C : NativeK5AWPeifferCompatible W N)
    {x y : C.presentation.Cell 1}
    (hsep : nativeK5AWPeifferObserver W C.presentation x ≠
      nativeK5AWPeifferObserver W C.presentation y) :
    ¬ C.presentation.HasFiller 0 x y := by
  intro hf
  exact hsep (nativeK5AWPeiffer_filler_necessary W C hf)

/-- This particular physical finite extension has NO 16D cells;
the ORIGINAL typed 14D fiber and all actual AQ 15D proofs remain. -/
def nativeK5AWPhysicalEmpty
    (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat) : NativeK5AVPhysicalFinitePresentation W N :=
  nativeFiniteAWEmptyPresentation _ _ N

/-- The two genuine AU 15D NATURALITY routes have equal Peiffer
defects in ANY finite physical presentation, as previously proved
at the original source-dependent boundary. -/
theorem nativeK5AWNaturality_Peiffer_equal
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AWPeifferObserver W T
        (nativeK5AVPhysicalFifteen W T
          (nativeK5AUNaturalityViaSource W cell)) =
      nativeK5AWPeifferObserver W T
        (nativeK5AVPhysicalFifteen W T
          (nativeK5AUNaturalityViaTarget W cell)) :=
  nativeK5AUNaturality_defect_eq W cell

/-- All finite empty-higher extensions simultaneously REFUTE the
false converse: even though the two genuinely typed AU naturality
15D paths have EXACTLY EQUAL Peiffer defects, no 16D filler exists
in this legitimate finite presentation. This is only a model-relative
no-go, NOT an absolute geometric obstruction. -/
theorem nativeK5AWNaturality_shadow_not_sufficient
    (W : NativeK5StructuralThirteenCell p U V)
    (N : Nat) {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    let T := nativeK5AWPhysicalEmpty W N
    (nativeK5AWPeifferObserver W T
        (nativeK5AVPhysicalFifteen W T
          (nativeK5AUNaturalityViaSource W cell)) =
      nativeK5AWPeifferObserver W T
        (nativeK5AVPhysicalFifteen W T
          (nativeK5AUNaturalityViaTarget W cell))) ∧
    ¬ T.HasFiller 0
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaSource W cell))
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaTarget W cell)) := by
  dsimp
  constructor
  · exact nativeK5AWNaturality_Peiffer_equal W
      (nativeK5AWPhysicalEmpty W N) cell
  · rintro ⟨z, _, _⟩
    exact (nativeFiniteAWEmptyHigherElim N 0 z).elim

end PhysicalC60

#print axioms NativeFiniteAWParallelBoundary
#print axioms nativeFiniteAWCellBoundary
#print axioms NativeFiniteAWComplete
#print axioms nativeFiniteAWComplete_iff_surjective
#print axioms NativeFiniteAWBoundaryObserver
#print axioms nativeFiniteAWObserver_noFiller
#print axioms nativeFiniteAWObservers_noFiller
#print axioms nativeFiniteAWEmptyHigherElim
#print axioms nativeFiniteAWEmptyPresentation
#print axioms nativeFiniteAWEmpty_noHigher
#print axioms nativeFiniteAWEmpty_noFiller
#print axioms nativeFiniteAWEmpty_notComplete
#print axioms nativeK5AWPeifferObserver
#print axioms NativeK5AWPeifferCompatible
#print axioms nativeK5AWPeiffer_filler_necessary
#print axioms nativeK5AWPeiffer_noFiller
#print axioms nativeK5AWPhysicalEmpty
#print axioms nativeK5AWNaturality_Peiffer_equal
#print axioms nativeK5AWNaturality_shadow_not_sufficient

end
end Kuu.F112.Physical
