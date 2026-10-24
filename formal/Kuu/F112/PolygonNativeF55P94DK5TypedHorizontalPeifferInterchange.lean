import Kuu.F112.PolygonNativeF55P94DK5TypedFourCellPeifferWordBridge
import Mathlib.Tactic

/-!
# F112-P94D3X — typed horizontal four-cell pasting and Peiffer interchange

Take two composable, genuinely Type-valued P94D3V four-cells, including
the independent reoriented K5 pentagonator. Construct BOTH ordered
horizontal pastings from ACTUAL source witnesses, using distinct
vertical 3-cell whiskerings. Their 4-cell terms remain distinct.

Prove the two precise noncommutative Peiffer boundary formulas:
  R(alpha) + (boundary g) acting on R(beta)
  (boundary f) acting on R(beta) + R(alpha).
These agree, yielding Peiffer-level interchange for every pair of
source-typed four-cell terms. Show that the pentagonator participates,
and prove the integer-N obstruction to faithful old P94C2 descent.

This is NOT equality of the two Type-valued 4-cell proof terms and
does NOT construct a source 5-cell or assert strict 3/n or hyperdescent.
No Gray, sorry/admit, logical axiom, or change to C60 and public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Universal normal-kernel action is a group endomorphism in its
relation variable, with no assumed commutativity. -/
theorem nativeK5UniversalPeifferAct_add
    (w : NativeF55P94CWord)
    (r s : nativeK5UniversalPentagonatorKernel (D := D) (E := E)) :
    nativeK5UniversalPeifferAct w (r + s) =
      nativeK5UniversalPeifferAct w r +
        nativeK5UniversalPeifferAct w s := by
  apply Subtype.ext
  change w + ((r : NativeF55P94CWord) + (s : NativeF55P94CWord)) - w =
    (w + (r : NativeF55P94CWord) - w) +
      (w + (s : NativeF55P94CWord) - w)
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

/-- Nested genuine word whiskerings compose by their ORIGINAL
noncommutative concatenation. -/
theorem nativeK5UniversalPeifferAct_comp
    (w z : NativeF55P94CWord)
    (r : nativeK5UniversalPentagonatorKernel (D := D) (E := E)) :
    nativeK5UniversalPeifferAct (w + z) r =
      nativeK5UniversalPeifferAct w (nativeK5UniversalPeifferAct z r) := by
  apply Subtype.ext
  change (w + z) + (r : NativeF55P94CWord) - (w + z) =
    w + (z + (r : NativeF55P94CWord) - z) - w
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

section TypedHorizontal

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- First ACTUAL Type-valued horizontal 4-cell: right-whisker
alpha by h, then left-whisker beta by g. -/
def NativeK5StructuralFourCell.horizontalViaTarget
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFourCell p (.trans f h) (.trans g k) :=
  .trans (.postcompose alpha h) (.precompose g beta)

/-- The second ACTUAL Type-valued horizontal 4-cell: left-whisker
beta by f, then right-whisker alpha by k. These TWO proof terms
are NOT identified by the existing free four-cell grammar. -/
def NativeK5StructuralFourCell.horizontalViaSource
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFourCell p (.trans f h) (.trans g k) :=
  .trans (.precompose f beta) (.postcompose alpha k)

/-- First exact noncommutative Peiffer horizontal pasting formula.
The action uses the TARGET 3-cell word of alpha, not an
untyped commutative replacement. -/
theorem NativeK5StructuralFourCell.horizontalViaTarget_relator
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    (alpha.horizontalViaTarget beta).toUniversalPeifferRelator =
      alpha.toUniversalPeifferRelator +
        nativeK5UniversalPeifferAct g.p94cGroupWord
          beta.toUniversalPeifferRelator := by
  apply Subtype.ext
  change (f.p94cGroupWord + h.p94cGroupWord) -
      (g.p94cGroupWord + k.p94cGroupWord) =
    (f.p94cGroupWord - g.p94cGroupWord) +
      (g.p94cGroupWord + (h.p94cGroupWord - k.p94cGroupWord) -
        g.p94cGroupWord)
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

/-- Second Peiffer horizontal pasting formula, now transporting
beta by alpha's SOURCE 3-cell word. -/
theorem NativeK5StructuralFourCell.horizontalViaSource_relator
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    (alpha.horizontalViaSource beta).toUniversalPeifferRelator =
      nativeK5UniversalPeifferAct f.p94cGroupWord
          beta.toUniversalPeifferRelator +
        alpha.toUniversalPeifferRelator := by
  apply Subtype.ext
  change (f.p94cGroupWord + h.p94cGroupWord) -
      (g.p94cGroupWord + k.p94cGroupWord) =
    (f.p94cGroupWord + (h.p94cGroupWord - k.p94cGroupWord) -
      f.p94cGroupWord) +
      (f.p94cGroupWord - g.p94cGroupWord)
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

/-- Peiffer INTERCHANGE OF IMAGES of two genuinely source-typed
horizontal 4-cell composites. It does not assert equality of the
original four-cell proof terms. -/
theorem NativeK5StructuralFourCell.horizontalInterchange_peiffer
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    alpha.toUniversalPeifferRelator +
        nativeK5UniversalPeifferAct g.p94cGroupWord
          beta.toUniversalPeifferRelator =
      nativeK5UniversalPeifferAct f.p94cGroupWord
          beta.toUniversalPeifferRelator +
        alpha.toUniversalPeifferRelator := by
  calc
    _ = (alpha.horizontalViaTarget beta).toUniversalPeifferRelator :=
      (alpha.horizontalViaTarget_relator beta).symm
    _ = (alpha.horizontalViaSource beta).toUniversalPeifferRelator := rfl
    _ = _ := alpha.horizontalViaSource_relator beta

/-- Both distinct real source-typed horizontal composites have
exactly the same universal Peiffer image, not necessarily the
same Type-valued proof term. -/
theorem NativeK5StructuralFourCell.horizontalPeifferCoherence
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    (alpha.horizontalViaTarget beta).toUniversalPeifferRelator =
      (alpha.horizontalViaSource beta).toUniversalPeifferRelator := by
  rfl

end TypedHorizontal

section ReorientedPentagonator

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The actual independent five-stage pentagonator participates
in BOTH genuine Type-valued horizontal pastings. Their Peiffer
interchange is proved, not postulated as equality of higher cells. -/
theorem nativeK5IndependentPentagonator_horizontalPeiffer
    {h k : NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)}
    (beta : NativeK5StructuralFourCell p h k) :
    ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaTarget
      beta).toUniversalPeifferRelator =
    ((nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).horizontalViaSource
      beta).toUniversalPeifferRelator :=
  NativeK5StructuralFourCell.horizontalPeifferCoherence
    (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5) beta

/-- Any proposed descent of the NEW +3 pentagonator endpoints to
OLD P94C2 which preserves each full noncommutative word cannot
produce an old Type-valued 4-cell. The latter preserves INTEGER N.
This is an obstruction to faithful descent, not a no-go for all
higher presentations. -/
theorem nativeK5IndependentPentagonator_no_oldWordFaithfulFourCell
    (u v : NativeF55P92AssocComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0))
    (hu : u.p94cGroupWord =
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord)
    (hv : v.p94cGroupWord =
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5).p94cGroupWord) :
    ¬ Nonempty (NativeF55P94CGroupFourCell u v) := by
  rintro ⟨w⟩
  have hn : (3 : ℤ) = 0 := by
    calc
      (3 : ℤ) = nativeK5NaturalityCount u.p94cGroupWord := by
        rw [hu, nativeK5NineReorientedExtendedCycle_NCount_three]
      _ = nativeK5NaturalityCount v.p94cGroupWord := w.nCount_sound
      _ = 0 := by
        rw [hv]
        change nativeK5NaturalityCount (0 : NativeF55P94CWord) = 0
        exact map_zero nativeK5NaturalityCount
  exact (by decide : (3 : ℤ) ≠ 0) hn

end ReorientedPentagonator

#print axioms nativeK5UniversalPeifferAct_add
#print axioms nativeK5UniversalPeifferAct_comp
#print axioms NativeK5StructuralFourCell.horizontalViaTarget
#print axioms NativeK5StructuralFourCell.horizontalViaSource
#print axioms NativeK5StructuralFourCell.horizontalViaTarget_relator
#print axioms NativeK5StructuralFourCell.horizontalViaSource_relator
#print axioms NativeK5StructuralFourCell.horizontalInterchange_peiffer
#print axioms NativeK5StructuralFourCell.horizontalPeifferCoherence
#print axioms nativeK5IndependentPentagonator_horizontalPeiffer
#print axioms nativeK5IndependentPentagonator_no_oldWordFaithfulFourCell

end
end Kuu.F112.Physical
