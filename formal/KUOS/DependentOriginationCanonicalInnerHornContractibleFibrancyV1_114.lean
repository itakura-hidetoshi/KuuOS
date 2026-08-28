import KUOS.DependentOriginationCanonicalTypeATerminalSourceSplitTransferV1_113
import KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
import Mathlib.AlgebraicTopology.SimplicialSet.Homotopy

namespace KUOS.DependentOriginationCanonicalInnerHornContractibleFibrancyV1_114

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationCanonicalTypeATerminalSourceSplitTransferV1_113

universe u

noncomputable section

/-!
# Canonical inner-horn contractibility and object-level fibrancy v1.114

Version v1.113 isolated a one-sided source-split route from canonical terminal
RLP to standard type-(A) terminal horn filling.  That route remains a valid
sufficient geometric criterion.  At object level, however, the v1.37--v1.42
strictification spine permits a still weaker argument.

Every horn of dimension at least two is simplicially contractible to its
central vertex in homotopy class.  We use the pointwise maximum endomap

```text
x |-> max(x,i)
```

on `Lambda[n,i]`.  It admits two literal simplicial prisms

```text
id       ~ max(-,i)
const_i  ~ max(-,i).
```

Both prisms stay inside the horn because every output vertex is either an
original vertex of the simplex or `i`; hence any vertex missing from
`range(x) union {i}` remains missing.  After postcomposition, every horn map is
therefore homotopic in Mathlib's `RelativeMorphism.HomotopyClass` to a constant
horn map.

A constant horn map extends over the full simplex.  For an attachment-fibrant
target, v1.91 already proves that the target scaling is maximal, so this
constant simplex extension is automatically scaled.  Thus every inner horn
problem has a homotopy-class scaled filler.  The canonical terminal RLP of
v1.42 then strictifies it.

Consequently canonical attachment fibrancy implies strict filling for every
chosen inner scaled-horn family, and in particular standard type-(A) terminal
RLP, with no higher source-split hypothesis.

This is strictly an object-level statement.  It does not prove that standard
type-(A) generators lie in the canonical generated left class.  The
presentation-level reverse comparison remains separate, and the v1.112
obstruction to one-lower-cylinder full arrow retracts remains relevant there.
-/

/-! ## A range lemma keeping pointwise horn deformations inside the horn -/

/-- If every vertex of a simplex is either the corresponding vertex of a horn
simplex or the distinguished horn vertex, then the new simplex is still in the
horn. -/
private theorem horn_mem_of_pointwise_eq_or_index
    (m : Nat)
    (i : Fin (m + 3))
    {d : Nat}
    (x : (Λ[m + 2, i] : SSet.{u}) _⦋d⦌)
    (y : (Δ[m + 2] : SSet.{u}) _⦋d⦌)
    (hy : ∀ k : Fin (d + 1), y k = x.val k ∨ y k = i) :
    y ∈ (SSet.horn (m + 2) i).obj (op ⦋d⦌) := by
  rw [SSet.mem_horn_iff_notMem_range]
  rcases
      (SSet.mem_horn_iff_notMem_range x.val i).1 x.property with
    ⟨missing, hmissing_ne, hmissing⟩
  refine ⟨missing, hmissing_ne, ?_⟩
  rintro ⟨k, hk⟩
  rcases hy k with hyx | hyi
  · apply hmissing
    exact ⟨k, hyx.symm.trans hk⟩
  · exact hmissing_ne (hyi.symm.trans hk).symm

/-! ## The central constant map and pointwise maximum endomap -/

/-- The distinguished horn vertex, as a vertex of the horn itself. -/
def innerHornCenter
    (m : Nat)
    (i : Fin (m + 3)) :
    (Λ[m + 2, i] : SSet.{u}) _⦋0⦌ :=
  SSet.horn.const m i i (op ⦋0⦌)

/-- Constant endomap at the distinguished horn vertex. -/
def innerHornConstMap
    (m : Nat)
    (i : Fin (m + 3)) :
    (Λ[m + 2, i] : SSet.{u}) ⟶ (Λ[m + 2, i] : SSet.{u}) :=
  SSet.const (innerHornCenter m i)

/-- Pointwise maximum with the distinguished horn vertex. -/
def innerHornMaxMap
    (m : Nat)
    (i : Fin (m + 3)) :
    (Λ[m + 2, i] : SSet.{u}) ⟶ (Λ[m + 2, i] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun x =>
    ⟨SSet.stdSimplex.objMk
      { toFun := fun j => max (x.val j) i
        monotone' := by
          intro a b hab
          exact max_le_max
            (SSet.stdSimplex.monotone_apply x.val hab) le_rfl },
      horn_mem_of_pointwise_eq_or_index m i x _ (by
        intro k
        by_cases h : i ≤ x.val k
        · exact Or.inl (max_eq_left h)
        · exact Or.inr (max_eq_right (le_of_lt (lt_of_not_ge h))))⟩
  naturality := by
    intro d e f
    ext x j
    rfl

/-! ## Literal prisms id ~ max and const ~ max -/

/-- Prism from the identity horn endomap to pointwise maximum with `i`. -/
def innerHornIdToMaxPrism
    (m : Nat)
    (i : Fin (m + 3)) :
    ((Λ[m + 2, i] : SSet.{u}) ⊗ Δ[1]) ⟶
      (Λ[m + 2, i] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    ⟨SSet.stdSimplex.objMk
      { toFun := fun j =>
          if z.2 j = 0 then z.1.val j else max (z.1.val j) i
        monotone' := by
          intro a b hab
          have hx := SSet.stdSimplex.monotone_apply z.1.val hab
          have ht := SSet.stdSimplex.monotone_apply z.2 hab
          by_cases ha : z.2 a = 0
          · by_cases hb : z.2 b = 0
            · simpa [ha, hb] using hx
            · simp only [ha, if_pos, hb, if_neg]
              exact hx.trans (le_max_left _ _)
          · have hb : z.2 b ≠ 0 := by
              intro hb
              have hz : z.2 a ≤ 0 := by simpa [hb] using ht
              have : z.2 a = 0 := le_antisymm hz (Fin.zero_le _)
              exact ha this
            simp only [ha, if_neg, hb]
            exact max_le_max hx le_rfl },
      horn_mem_of_pointwise_eq_or_index m i z.1 _ (by
        intro k
        by_cases hk : z.2 k = 0
        · exact Or.inl (by simp [hk])
        · simp only [hk, if_neg]
          by_cases h : i ≤ z.1.val k
          · exact Or.inl (max_eq_left h)
          · exact Or.inr
              (max_eq_right (le_of_lt (lt_of_not_ge h))))⟩
  naturality := by
    intro d e f
    ext z j
    rfl

/-- Prism from the constant endomap at `i` to pointwise maximum with `i`. -/
def innerHornConstToMaxPrism
    (m : Nat)
    (i : Fin (m + 3)) :
    ((Λ[m + 2, i] : SSet.{u}) ⊗ Δ[1]) ⟶
      (Λ[m + 2, i] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    ⟨SSet.stdSimplex.objMk
      { toFun := fun j =>
          if z.2 j = 0 then i else max (z.1.val j) i
        monotone' := by
          intro a b hab
          have hx := SSet.stdSimplex.monotone_apply z.1.val hab
          have ht := SSet.stdSimplex.monotone_apply z.2 hab
          by_cases ha : z.2 a = 0
          · by_cases hb : z.2 b = 0
            · simp [ha, hb]
            · simp only [ha, if_pos, hb, if_neg]
              exact le_max_right _ _
          · have hb : z.2 b ≠ 0 := by
              intro hb
              have hz : z.2 a ≤ 0 := by simpa [hb] using ht
              have : z.2 a = 0 := le_antisymm hz (Fin.zero_le _)
              exact ha this
            simp only [ha, if_neg, hb]
            exact max_le_max hx le_rfl },
      horn_mem_of_pointwise_eq_or_index m i z.1 _ (by
        intro k
        by_cases hk : z.2 k = 0
        · exact Or.inr (by simp [hk])
        · simp only [hk, if_neg]
          by_cases h : i ≤ z.1.val k
          · exact Or.inl (max_eq_left h)
          · exact Or.inr
              (max_eq_right (le_of_lt (lt_of_not_ge h))))⟩
  naturality := by
    intro d e f
    ext z j
    rfl

/-- The first prism is a literal simplicial homotopy `id ~ max(-,i)`. -/
def innerHornIdToMaxHomotopy
    (m : Nat)
    (i : Fin (m + 3)) :
    SSet.Homotopy
      (𝟙 (Λ[m + 2, i] : SSet.{u}))
      (innerHornMaxMap m i) where
  h := innerHornIdToMaxPrism m i
  h₀ := by
    apply SSet.hom_ext
    intro d
    ext x j
    rfl
  h₁ := by
    apply SSet.hom_ext
    intro d
    ext x j
    rfl

/-- The second prism is a literal simplicial homotopy `const_i ~ max(-,i)`. -/
def innerHornConstToMaxHomotopy
    (m : Nat)
    (i : Fin (m + 3)) :
    SSet.Homotopy
      (innerHornConstMap m i)
      (innerHornMaxMap m i) where
  h := innerHornConstToMaxPrism m i
  h₀ := by
    apply SSet.hom_ext
    intro d
    ext x j
    rfl
  h₁ := by
    apply SSet.hom_ext
    intro d
    ext x j
    rfl

/-! ## Postcomposition and contractibility of horn mapping classes -/

/-- A simplicial homotopy remains a simplicial homotopy after postcomposition. -/
def postcomposeSSetHomotopy
    {A B C : SSet.{u}}
    {f g : A ⟶ B}
    (H : SSet.Homotopy f g)
    (k : B ⟶ C) :
    SSet.Homotopy (f ≫ k) (g ≫ k) where
  h := H.h ≫ k
  h₀ := by simp
  h₁ := by simp

/-- Every map out of a horn of dimension at least two has the same simplicial
homotopy class as the constant map at its value on the distinguished vertex. -/
theorem innerHornMap_homotopyClass_eq_const
    (m : Nat)
    (i : Fin (m + 3))
    {X : SSet.{u}}
    (f : (Λ[m + 2, i] : SSet.{u}) ⟶ X) :
    homotopyClassOfMap f =
      homotopyClassOfMap
        (SSet.const
          (f.app (op ⦋0⦌) (innerHornCenter m i))) := by
  have hId :
      homotopyClassOfMap
          ((𝟙 (Λ[m + 2, i] : SSet.{u})) ≫ f) =
        homotopyClassOfMap (innerHornMaxMap m i ≫ f) :=
    homotopyClassOfMap_eq_of_homotopy
      (postcomposeSSetHomotopy (innerHornIdToMaxHomotopy m i) f)
  have hConst :
      homotopyClassOfMap (innerHornConstMap m i ≫ f) =
        homotopyClassOfMap (innerHornMaxMap m i ≫ f) :=
    homotopyClassOfMap_eq_of_homotopy
      (postcomposeSSetHomotopy (innerHornConstToMaxHomotopy m i) f)
  calc
    homotopyClassOfMap f =
        homotopyClassOfMap (innerHornMaxMap m i ≫ f) := by
      simpa using hId
    _ = homotopyClassOfMap (innerHornConstMap m i ≫ f) :=
      hConst.symm
    _ = homotopyClassOfMap
        (SSet.const
          (f.app (op ⦋0⦌) (innerHornCenter m i))) := by
      rw [innerHornConstMap, SSet.const_comp]

/-! ## Universal homotopy-class filler under maximal target scaling -/

/-- Under maximal target scaling, every scaled horn problem in dimension at
least two has a homotopy-class filler: use the constant simplex extension and
horn contractibility. -/
noncomputable def innerHornHomotopyClassFillerOfMaximalScaling
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (m : Nat)
    (i : Fin (m + 3))
    (P : ScaledHornExtensionProblem X sX (m + 2) i)
    (hmax : sX = ScaledSimplicialSet.maximal X) :
    HomotopyClassScaledHornFiller P where
  simplexMap :=
    SSet.const
      (P.hornMap.app (op ⦋0⦌) (innerHornCenter m i))
  boundary_class_eq := by
    rw [SSet.comp_const]
    exact (innerHornMap_homotopyClass_eq_const m i P.hornMap).symm
  simplexMap_scaled := by
    rw [hmax]
    intro t ht
    exact ScaledSimplicialSet.maximal_thin X _

/-! ## Attachment fibrancy gives every strict inner horn filler -/

/-- Canonical attachment fibrancy gives a strict filler for every inner scaled
horn problem.  The family selecting the problem is irrelevant. -/
theorem attachmentFibrant_innerHornFiller
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (hX : IsAttachmentFibrant (ScaledSSet.of X sX))
    {n : Nat}
    {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i)
    (h0 : 0 < i)
    (hi : i < Fin.last n) :
    Nonempty (ScaledHornFiller P) := by
  have hn2 : 2 ≤ n := by
    have h0' := h0
    have hi' := hi
    change 0 < i.val at h0'
    change i.val < n at hi'
    omega
  obtain ⟨m, hm⟩ : ∃ m : Nat, n = m + 2 :=
    ⟨n - 2, by omega⟩
  subst n
  let Q : HomotopyClassScaledHornFiller P :=
    innerHornHomotopyClassFillerOfMaximalScaling
      m i P (attachmentFibrant_scaling_eq_maximal hX)
  exact (problemTerminalRLPOfAttachmentFibrant hX P).strictify Q

/-- Hence an attachment-fibrant target fills every inner horn selected by any
scaled horn family. -/
noncomputable def hasScaledHornFillersOfAttachmentFibrant
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (hX : IsAttachmentFibrant (ScaledSSet.of X sX))
    (F : ScaledHornFamily X sX) :
    HasScaledHornFillers X sX F where
  fill := by
    intro n i P _ h0 hi
    exact attachmentFibrant_innerHornFiller hX P h0 hi

/-- The same universal inner-horn fibrancy follows from fibrancy for any
compatible canonical scaled-anodyne presentation. -/
noncomputable def hasScaledHornFillersOfPresentationFibrant
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (A : ScaledAnodynePresentation.{u})
    (hX : IsFibrantForPresentation A (ScaledSSet.of X sX))
    (F : ScaledHornFamily X sX) :
    HasScaledHornFillers X sX F :=
  hasScaledHornFillersOfAttachmentFibrant
    ((isFibrantForPresentation_iff_attachmentFibrant A _).mp hX) F

/-! ## Standard type-(A) object-level frontier closes unconditionally -/

/-- Attachment fibrancy gives standard type-(A) terminal RLP in every
admissible dimension, with no higher source-split certificate. -/
theorem attachmentFibrant_hasStandardTypeATerminalRLP_unconditional
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    HasStandardTypeATerminalRLP X := by
  intro g
  apply
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (standardTypeAScaledHornGeneratorHom g)).2
  intro f
  let P : ScaledHornExtensionProblem
      X.carrier X.scaling g.n g.i :=
    { hornScaling := standardTypeAHornScaling g.i
      simplexScaling := standardTypeASimplexScaling g.i
      inclusion_scaled := standardTypeAHornInclusion_scaled g.i
      hornMap := f.map
      hornMap_scaled := f.scaled }
  rcases
      attachmentFibrant_innerHornFiller
        hX P g.inner_left g.inner_right with
    ⟨Q⟩
  let l : standardTypeAScaledSimplex g ⟶ X :=
    { map := Q.simplexMap
      scaled := Q.simplexMap_scaled }
  refine ⟨l, ?_⟩
  apply ScaledSSet.ScaledMap.ext
  change
    (Λ[g.n, g.i].ι :
        (Λ[g.n, g.i] : SSet.{u}) ⟶ (Δ[g.n] : SSet.{u})) ≫
      Q.simplexMap = f.map
  exact Q.extends_horn.symm

/-!
The object-level PlanOS branch is now closed conceptually:

```text
inner horn Lambda[n,i]
  -> id ~ max(-,i) ~ const_i in simplicial homotopy class
  -> every horn map is class-equal to a constant horn map

attachment fibrancy
  -> maximal target scaling                         -- v1.91
  -> constant simplex extension is scaled
  -> homotopy-class filler exists
  -> canonical two-sided terminal RLP               -- v1.42
  -> strict filler
  -> HasScaledHornFillers for every chosen family
  -> standard type-(A) terminal RLP, unconditionally.
```

What is *not* closed is the presentation-level reverse comparison
`standardGeneratedScaledAnodyneABC <= canonicalGeneratedScaledAnodyne`.
That statement still requires left-class geometry, and v1.112 still rules out
one-lower-cylinder full target retracts in dimensions at least three.  Thus
v1.114 cleanly separates object fibrancy from presentation comparison rather
than weakening either notion.
-/

end KUOS.DependentOriginationCanonicalInnerHornContractibleFibrancyV1_114
