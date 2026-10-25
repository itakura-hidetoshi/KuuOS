import Kuu.F112.PolygonNativeF55P94DK5TypedFifteenNaturalityCoherenceBoundary
import Mathlib.Tactic

/-!
# F112-P94D3AV — finite-dimensional dependent globular presentation

Instead of ad hoc new files for geometric 16-, 17-, ...-cells, this
module represents every FINITE cutoff N simultaneously. Dimension 14
is the ORIGINAL dependent C60 raw 14-cell fiber. Dimension 15 is the
ACTUAL AQ Type-valued fifteen-cell syntax, carried together with its
two original dependent fourteen-cell endpoints.

Above dimension 15, an extension supplies up to N ADDITIONAL cell
types, explicit source/target maps, and globularity laws. Every such
extension is ASSUMED AS DATA, never inferred from the AS Peiffer kernel.
There are no cells above dimension 15+N in the bounded presentation.

The general finite scheme establishes:
  * typed boundaries, globularity, and parallelism of supplied fillers;
  * no phantom cells above the supplied finite cutoff;
  * boundary-respecting congruences and induced quotient boundaries;
  * necessary and sufficient observer descent at ALL finitely many
    levels, simultaneously, by a single parametrized theorem;
  * the genuine C60 15-cell embedding and the two AU naturality
    boundaries, without asserting the existence of a 16-cell.

The index in NativeConservativeTower measures closure depth, NOT
geometric dimension. The two are NOT conflated here. This file does
not prove a global strict 3/n-category or (infinity,3)-hyperdescent,
nor introduce Gray structures, new axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

/-- The finite globular carriers, counted RELATIVE TO GEOMETRIC 14D:
  0 = actual raw 14D proof;
  1 = the Sigma type of (two original 14D endpoints, actual 15D proof);
  k+2 = independently supplied (16+k)D data only for k < N.
Beyond the finite cutoff, the carrier is empty by construction.
The higher-level data are NOT automatically inhabited. -/
def NativeFiniteAVCell
    (A : Type u) (Edge : A → A → Type v)
    (N : Nat) (Higher : Fin N → Type (max u v)) :
    Nat → Type (max u v)
  | 0 => A
  | 1 => Σ endpoints : A × A, Edge endpoints.1 endpoints.2
  | Nat.succ (Nat.succ k) =>
      if h : k < N then Higher ⟨k, h⟩ else PEmpty

/-- Source map at 15D is an ACTUAL endpoint projection.
At higher dimensions it uses explicit, independently supplied data. -/
def nativeFiniteAVSource
    {A : Type u} {Edge : A → A → Type v}
    {N : Nat} {Higher : Fin N → Type (max u v)}
    (higherSource : ∀ k,
      NativeFiniteAVCell A Edge N Higher (k + 2) →
        NativeFiniteAVCell A Edge N Higher (k + 1)) :
    ∀ k, NativeFiniteAVCell A Edge N Higher (k + 1) →
      NativeFiniteAVCell A Edge N Higher k
  | 0, cell => cell.1.1
  | Nat.succ k, cell => higherSource k cell

/-- Target map at 15D is the other ORIGINAL typed endpoint.
All higher target maps must be independently supplied. -/
def nativeFiniteAVTarget
    {A : Type u} {Edge : A → A → Type v}
    {N : Nat} {Higher : Fin N → Type (max u v)}
    (higherTarget : ∀ k,
      NativeFiniteAVCell A Edge N Higher (k + 2) →
        NativeFiniteAVCell A Edge N Higher (k + 1)) :
    ∀ k, NativeFiniteAVCell A Edge N Higher (k + 1) →
      NativeFiniteAVCell A Edge N Higher k
  | 0, cell => cell.1.2
  | Nat.succ k, cell => higherTarget k cell

/-- A genuinely FINITE globular presentation above a FIXED, given
Type-valued 15D edge grammar. All higher cell sources and targets and
their globular equations are obligations, never automatically adjoined
coherence constructors. In particular, a nontrivial 16D cell is NOT
deduced from equality of two Peiffer defects. -/
structure NativeFiniteAVPresentation
    (A : Type u) (Edge : A → A → Type v) (N : Nat) where
  higher : Fin N → Type (max u v)
  higherSource : ∀ k,
    NativeFiniteAVCell A Edge N higher (k + 2) →
      NativeFiniteAVCell A Edge N higher (k + 1)
  higherTarget : ∀ k,
    NativeFiniteAVCell A Edge N higher (k + 2) →
      NativeFiniteAVCell A Edge N higher (k + 1)
  source_globular : ∀ k (cell : NativeFiniteAVCell A Edge N higher (k + 2)),
    nativeFiniteAVSource higherSource k (higherSource k cell) =
      nativeFiniteAVSource higherSource k (higherTarget k cell)
  target_globular : ∀ k (cell : NativeFiniteAVCell A Edge N higher (k + 2)),
    nativeFiniteAVTarget higherTarget k (higherSource k cell) =
      nativeFiniteAVTarget higherTarget k (higherTarget k cell)

namespace NativeFiniteAVPresentation

variable {A : Type u} {Edge : A → A → Type v} {N : Nat}

def Cell (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) : Type (max u v) :=
  NativeFiniteAVCell A Edge N T.higher k

def source (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) : T.Cell (k + 1) → T.Cell k :=
  nativeFiniteAVSource T.higherSource k

def target (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) : T.Cell (k + 1) → T.Cell k :=
  nativeFiniteAVTarget T.higherTarget k

/-- A genuine supplied (k+2)-cell has PARALLEL (k+1)-boundaries. -/
def Parallel (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (x y : T.Cell (k + 1)) : Prop :=
  T.source k x = T.source k y ∧ T.target k x = T.target k y

/-- Actual existence, NOT merely a shadow equality, of a higher
filler at the precise specified dependent boundary. -/
def HasFiller (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (x y : T.Cell (k + 1)) : Prop :=
  ∃ cell : T.Cell (k + 2),
    T.source (k + 1) cell = x ∧
      T.target (k + 1) cell = y

theorem source_globular_sound
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (cell : T.Cell (k + 2)) :
    T.source k (T.source (k + 1) cell) =
      T.source k (T.target (k + 1) cell) :=
  T.source_globular k cell

theorem target_globular_sound
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (cell : T.Cell (k + 2)) :
    T.target k (T.source (k + 1) cell) =
      T.target k (T.target (k + 1) cell) :=
  T.target_globular k cell

/-- Any actually supplied higher cell automatically respects the
two lower boundaries. This is necessary, NOT sufficient, for filling. -/
theorem filler_parallel
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) {x y : T.Cell (k + 1)}
    (h : T.HasFiller k x y) : T.Parallel k x y := by
  rcases h with ⟨cell, hs, ht⟩
  constructor
  · calc
      T.source k x = T.source k (T.source (k + 1) cell) :=
        congrArg (T.source k) hs.symm
      _ = T.source k (T.target (k + 1) cell) :=
        T.source_globular_sound k cell
      _ = T.source k y := congrArg (T.source k) ht
  · calc
      T.target k x = T.target k (T.source (k + 1) cell) :=
        congrArg (T.target k) hs.symm
      _ = T.target k (T.target (k + 1) cell) :=
        T.target_globular_sound k cell
      _ = T.target k y := congrArg (T.target k) ht

/-- For EVERY finite N, no (16+k)-cell with k >= N can exist.
This is a cutoff statement about a specified PRESENTATION, not a
geometric no-go in every possible richer extension. -/
theorem no_cell_beyond
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (hk : N ≤ k) :
    ¬ Nonempty (T.Cell (k + 2)) := by
  intro ⟨cell⟩
  have hn : ¬ k < N := Nat.not_lt.mpr hk
  have hfalse : PEmpty := by
    change (if h : k < N then T.higher ⟨k, h⟩ else PEmpty) at cell
    simpa only [dif_neg hn] using cell
  exact hfalse.elim

/-- No filler above the chosen finite cutoff, irrespective of
parallel endpoints or equality of scalar/group-valued observers. -/
theorem no_filler_beyond
    (T : NativeFiniteAVPresentation A Edge N)
    (k : Nat) (hk : N ≤ k)
    (x y : T.Cell (k + 1)) :
    ¬ T.HasFiller k x y := by
  rintro ⟨cell, _, _⟩
  exact T.no_cell_beyond k hk ⟨cell⟩

/-- The concrete Type-valued 15D generators always retain their
ORIGINAL two 14D endpoints at the bottom of any finite extension. -/
def mkFifteen
    (T : NativeFiniteAVPresentation A Edge N)
    {x y : A} (edge : Edge x y) : T.Cell 1 :=
  ⟨(x, y), edge⟩

theorem mkFifteen_source
    (T : NativeFiniteAVPresentation A Edge N)
    {x y : A} (edge : Edge x y) :
    T.source 0 (T.mkFifteen edge) = x := rfl

theorem mkFifteen_target
    (T : NativeFiniteAVPresentation A Edge N)
    {x y : A} (edge : Edge x y) :
    T.target 0 (T.mkFifteen edge) = y := rfl

/-- A parallel pair of explicit 15D proofs is a legitimate 16D
BOUNDARY, but the existence of its 16D filler remains a separate
inhabitation problem in the finite presentation. -/
theorem mkFifteen_parallel
    (T : NativeFiniteAVPresentation A Edge N)
    {x y : A} (f g : Edge x y) :
    T.Parallel 0 (T.mkFifteen f) (T.mkFifteen g) :=
  ⟨rfl, rfl⟩

end NativeFiniteAVPresentation

/-- A dimension-wise quotient congruence whose source and target
maps preserve the equivalence relations at ALL finite stages.
This is supplied data, rather than equality inferred from a shadow. -/
structure NativeFiniteAVCongruence
    {A : Type u} {Edge : A → A → Type v} {N : Nat}
    (T : NativeFiniteAVPresentation A Edge N) where
  relation : ∀ k, Setoid (T.Cell k)
  source_compatible :
    ∀ k {x y : T.Cell (k + 1)},
      (relation (k + 1)).r x y →
        (relation k).r (T.source k x) (T.source k y)
  target_compatible :
    ∀ k {x y : T.Cell (k + 1)},
      (relation (k + 1)).r x y →
        (relation k).r (T.target k x) (T.target k y)

namespace NativeFiniteAVCongruence

variable {A : Type u} {Edge : A → A → Type v} {N : Nat}
variable {T : NativeFiniteAVPresentation A Edge N}

def QuotCell (C : NativeFiniteAVCongruence T) (k : Nat) : Type (max u v) :=
  Quotient (C.relation k)

/-- Source descends because representative-independence is EXPLICIT. -/
def quotSource (C : NativeFiniteAVCongruence T) (k : Nat) :
    C.QuotCell (k + 1) → C.QuotCell k :=
  Quotient.lift
    (fun x => Quotient.mk (C.relation k) (T.source k x))
    (by
      intro x y h
      exact Quotient.sound (C.source_compatible k h))

/-- Target descends under the same independently justified congruence. -/
def quotTarget (C : NativeFiniteAVCongruence T) (k : Nat) :
    C.QuotCell (k + 1) → C.QuotCell k :=
  Quotient.lift
    (fun x => Quotient.mk (C.relation k) (T.target k x))
    (by
      intro x y h
      exact Quotient.sound (C.target_compatible k h))

theorem quotSource_mk (C : NativeFiniteAVCongruence T)
    (k : Nat) (x : T.Cell (k + 1)) :
    C.quotSource k (Quotient.mk (C.relation (k + 1)) x) =
      Quotient.mk (C.relation k) (T.source k x) := rfl

theorem quotTarget_mk (C : NativeFiniteAVCongruence T)
    (k : Nat) (x : T.Cell (k + 1)) :
    C.quotTarget k (Quotient.mk (C.relation (k + 1)) x) =
      Quotient.mk (C.relation k) (T.target k x) := rfl

/-- The quotient's globular source square commutes IN EVERY FINITE
DIMENSION, not just for one new 16D generator. -/
theorem quotSource_globular (C : NativeFiniteAVCongruence T)
    (k : Nat) (q : C.QuotCell (k + 2)) :
    C.quotSource k (C.quotSource (k + 1) q) =
      C.quotSource k (C.quotTarget (k + 1) q) := by
  refine Quotient.inductionOn q ?_
  intro x
  exact congrArg (Quotient.mk (C.relation k))
    (T.source_globular_sound k x)

/-- Likewise the quotient's globular target square commutes at
ALL available levels, without a global strict category claim. -/
theorem quotTarget_globular (C : NativeFiniteAVCongruence T)
    (k : Nat) (q : C.QuotCell (k + 2)) :
    C.quotTarget k (C.quotSource (k + 1) q) =
      C.quotTarget k (C.quotTarget (k + 1) q) := by
  refine Quotient.inductionOn q ?_
  intro x
  exact congrArg (Quotient.mk (C.relation k))
    (T.target_globular_sound k x)

/-- One UNIFORM theorem for observer descent across all finite
dimensions 14 through 15+N (indexed by Fin (N+2)).
No per-dimension theorem is needed: compatible observers descend
iff they preserve all supplied dimension-wise equivalences. -/
theorem finiteObserverDescent_iff
    (C : NativeFiniteAVCongruence T)
    (B : Fin (N + 2) → Type w)
    (obs : ∀ i : Fin (N + 2), T.Cell i.val → B i) :
    (∃ lift : ∀ i : Fin (N + 2), C.QuotCell i.val → B i,
      ∀ (i : Fin (N + 2)) (x : T.Cell i.val),
        lift i (Quotient.mk (C.relation i.val) x) = obs i x) ↔
      (∀ (i : Fin (N + 2)) (x y : T.Cell i.val),
        (C.relation i.val).r x y → obs i x = obs i y) := by
  constructor
  · rintro ⟨lift, hlift⟩ i x y h
    calc
      obs i x = lift i (Quotient.mk (C.relation i.val) x) :=
        (hlift i x).symm
      _ = lift i (Quotient.mk (C.relation i.val) y) :=
        congrArg (lift i) (Quotient.sound h)
      _ = obs i y := hlift i y
  · intro h
    refine ⟨fun i => Quotient.lift (obs i)
      (by intro x y hc; exact h i x y hc), ?_⟩
    intro i x
    rfl

end NativeFiniteAVCongruence

/-- The ORIGINAL SOURCE-DEPENDENT C60 physical carrier, specialized
WITHOUT a new cell constructor or erasure of its typed boundaries. -/
section C60PhysicalFinite

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

/-- Arbitrary FINITE cutoff N over the exactly original fourteen-cell
physical fiber and its TRUE AQ Type-valued fifteen-cell grammar. -/
abbrev NativeK5AVPhysicalFinitePresentation
    (W : NativeK5StructuralThirteenCell p U V) (N : Nat) :=
  NativeFiniteAVPresentation
    (NativeK5FifteenFourteenFiber W) (NativeK5AQFifteenCell W) N

/-- Every existing genuine AQ 15D proof enters an arbitrary finite
extension, as an edge whose two endpoints remain the original typed
14D proofs, independently of what higher cells may exist. -/
def nativeK5AVPhysicalFifteen
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) : T.Cell 1 :=
  T.mkFifteen cell

theorem nativeK5AVPhysicalFifteen_source
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    T.source 0 (nativeK5AVPhysicalFifteen W T cell) = R :=
  T.mkFifteen_source cell

theorem nativeK5AVPhysicalFifteen_target
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    T.target 0 (nativeK5AVPhysicalFifteen W T cell) = S :=
  T.mkFifteen_target cell

/-- AU supplies TWO ACTUAL 15D Type proofs of the same dependent
boundary. Their 16D parallel boundary is well typed for any finite N.
This explicitly DOES NOT construct its 16D filler. -/
theorem nativeK5AVNaturality_parallel
    (W : NativeK5StructuralThirteenCell p U V)
    {N : Nat} (T : NativeK5AVPhysicalFinitePresentation W N)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    T.Parallel 0
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaSource W cell))
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaTarget W cell)) :=
  T.mkFifteen_parallel _ _

/-- In the 15D-only cutoff N=0, no genuine 16D filler is provided for
AU's two 15D paths, even though AU proves equality of Peiffer defects.
This is ONLY relative to this cutoff, not a universal geometric no-go. -/
theorem nativeK5AVNaturality_noFiller_at_zero_cutoff
    (W : NativeK5StructuralThirteenCell p U V)
    (T : NativeK5AVPhysicalFinitePresentation W 0)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    ¬ T.HasFiller 0
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaSource W cell))
      (nativeK5AVPhysicalFifteen W T
        (nativeK5AUNaturalityViaTarget W cell)) :=
  T.no_filler_beyond 0 (Nat.le_refl 0) _ _

end C60PhysicalFinite

#print axioms NativeFiniteAVCell
#print axioms nativeFiniteAVSource
#print axioms nativeFiniteAVTarget
#print axioms NativeFiniteAVPresentation
#print axioms NativeFiniteAVPresentation.Cell
#print axioms NativeFiniteAVPresentation.source
#print axioms NativeFiniteAVPresentation.target
#print axioms NativeFiniteAVPresentation.Parallel
#print axioms NativeFiniteAVPresentation.HasFiller
#print axioms NativeFiniteAVPresentation.source_globular_sound
#print axioms NativeFiniteAVPresentation.target_globular_sound
#print axioms NativeFiniteAVPresentation.filler_parallel
#print axioms NativeFiniteAVPresentation.no_cell_beyond
#print axioms NativeFiniteAVPresentation.no_filler_beyond
#print axioms NativeFiniteAVPresentation.mkFifteen
#print axioms NativeFiniteAVPresentation.mkFifteen_source
#print axioms NativeFiniteAVPresentation.mkFifteen_target
#print axioms NativeFiniteAVPresentation.mkFifteen_parallel
#print axioms NativeFiniteAVCongruence
#print axioms NativeFiniteAVCongruence.QuotCell
#print axioms NativeFiniteAVCongruence.quotSource
#print axioms NativeFiniteAVCongruence.quotTarget
#print axioms NativeFiniteAVCongruence.quotSource_mk
#print axioms NativeFiniteAVCongruence.quotTarget_mk
#print axioms NativeFiniteAVCongruence.quotSource_globular
#print axioms NativeFiniteAVCongruence.quotTarget_globular
#print axioms NativeFiniteAVCongruence.finiteObserverDescent_iff
#print axioms NativeK5AVPhysicalFinitePresentation
#print axioms nativeK5AVPhysicalFifteen
#print axioms nativeK5AVPhysicalFifteen_source
#print axioms nativeK5AVPhysicalFifteen_target
#print axioms nativeK5AVNaturality_parallel
#print axioms nativeK5AVNaturality_noFiller_at_zero_cutoff

end
end Kuu.F112.Physical
