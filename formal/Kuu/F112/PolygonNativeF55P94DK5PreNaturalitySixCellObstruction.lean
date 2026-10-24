import Kuu.F112.PolygonNativeF55P94DK5FiveCellShapeCharge
import Mathlib.Tactic

/-!
# F112-P94D3AA — exact necessity of independent 6D naturality cells

An explicitly defined source-typed six-cell CORE, containing:
  reflexivity, symmetry, transitivity,
  vertical congruences, associativity, units, inverses,
  inverse-respect and both typed 3-cell whiskerings,
but EXCLUDING all four independent P94D3Z naturality/square
six-cell generator families.

This core embeds constructor-by-constructor in P94D3Z's FULL
six-cell grammar. The two strictly finer interchanger SHAPE
observers from P94D3AA are invariant under EVERY core constructor.

For the precise OLD 5-cell left/right naturality boundaries
of a genuine unit-reduction source, those observers are 0 vs 1.
Hence NO composite of core six-cells fills those boundaries.
P94D3Z's new naturality generator DOES fill them. This gives
a genuine relative independence/obstruction theorem, not a
claim of absolute non-existence in all imaginable extensions.

No Gray, sorry/admit, new axioms, or loss of C60/107 roots.
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

/-- The pre-naturality six-dimensional core has NO independent
interchanger-naturality or horizontal-square generators. Each
retained constructor uses exactly the original typed boundaries
from the FULL source six-cell grammar. -/
inductive NativeK5PrenaturalitySixCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g},
      NativeK5StructuralFiveCell p alpha beta →
      NativeK5StructuralFiveCell p alpha beta →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5PrenaturalitySixCell p w w
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z) :
      NativeK5PrenaturalitySixCell p z w
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z)
      (v : NativeK5PrenaturalitySixCell p z q) :
      NativeK5PrenaturalitySixCell p w q
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z)
      (v : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5PrenaturalitySixCell p (.trans w v) (.trans z v)
  | verticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      {v z : NativeK5StructuralFiveCell p beta gamma}
      (u : NativeK5PrenaturalitySixCell p v z) :
      NativeK5PrenaturalitySixCell p (.trans w v) (.trans w z)
  | verticalAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma delta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      (v : NativeK5StructuralFiveCell p beta gamma)
      (z : NativeK5StructuralFiveCell p gamma delta) :
      NativeK5PrenaturalitySixCell p
        (.trans (.trans w v) z) (.trans w (.trans v z))
  | verticalLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5PrenaturalitySixCell p (.trans (.refl alpha) w) w
  | verticalRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5PrenaturalitySixCell p (.trans w (.refl beta)) w
  | inverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5PrenaturalitySixCell p (.trans w (.symm w)) (.refl alpha)
  | inverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5PrenaturalitySixCell p (.trans (.symm w) w) (.refl beta)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z) :
      NativeK5PrenaturalitySixCell p (.symm w) (.symm z)
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55StructuralComparison p r s)
      {f g : NativeF55StructuralComparison p s t}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z) :
      NativeK5PrenaturalitySixCell p (.precompose prior w) (.precompose prior z)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5PrenaturalitySixCell p (.postcompose w suffix) (.postcompose z suffix)


/-- Every core witness faithfully maps to the complete P94D3Z
six-cell syntax, by the *same* source-dependent constructor.
No NEW filler is manufactured by this map. -/
def NativeK5PrenaturalitySixCell.toFull
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5PrenaturalitySixCell p w z) :
    NativeK5StructuralSixCell p w z := by
  induction u with
  | refl w => exact .refl w
  | symm _ ih => exact .symm ih
  | trans _ _ ihu ihv => exact .trans ihu ihv
  | verticalLeft witness suffix ih => exact .verticalLeft ih suffix
  | verticalRight lead witness ih => exact .verticalRight lead ih
  | verticalAssoc a b c => exact .verticalAssoc a b c
  | verticalLeftUnit w => exact .verticalLeftUnit w
  | verticalRightUnit w => exact .verticalRightUnit w
  | inverseLeft w => exact .inverseLeft w
  | inverseRight w => exact .inverseRight w
  | inverseRespect witness ih => exact .inverseRespect ih
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix

/-- Every constructor of the conservative, genuinely typed 6D
core preserves BOTH independently selectable interchanger
source-shape charges. Unlike the coarser total signed charge,
this invariant is violated by the NEW D3Z naturality generators. -/
theorem NativeK5PrenaturalitySixCell.shapeCharge_sound
    (selectFirst : Bool)
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5PrenaturalitySixCell p w z) :
    w.shapeCharge selectFirst = z.shapeCharge selectFirst := by
  induction u with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralFiveCell.shapeCharge] using
        congrArg (fun t : ℤ => t + suffix.shapeCharge selectFirst) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralFiveCell.shapeCharge] using
        congrArg (fun t : ℤ => lead.shapeCharge selectFirst + t) ih
  | verticalAssoc a b c =>
      change (a.shapeCharge selectFirst + b.shapeCharge selectFirst) +
        c.shapeCharge selectFirst =
        a.shapeCharge selectFirst +
          (b.shapeCharge selectFirst + c.shapeCharge selectFirst)
      exact add_assoc _ _ _
  | verticalLeftUnit _ => simp [NativeK5StructuralFiveCell.shapeCharge]
  | verticalRightUnit _ => simp [NativeK5StructuralFiveCell.shapeCharge]
  | inverseLeft _ => simp [NativeK5StructuralFiveCell.shapeCharge]
  | inverseRight _ => simp [NativeK5StructuralFiveCell.shapeCharge]
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralFiveCell.shapeCharge] using
        congrArg (fun t : ℤ => -t) ih
  | precompose _ witness ih => exact ih
  | postcompose witness _ ih => exact ih

/-- A concrete OLD five-cell left-naturalization boundary has
NO six-cell in the conservative six-dimensional core. Its
coarse total signed interchanger charge is nevertheless equal. -/
theorem nativeK5LeftNaturality_noCoreSixCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    {h k : NativeF55StructuralComparison p s t}
    (beta : NativeK5StructuralFourCell p h k) :
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta)
      (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta)) := by
  rintro ⟨u⟩
  have h := u.shapeCharge_sound true
  change (0 : ℤ) = 1 at h
  norm_num at h

/-- Independent second coordinate: right-naturality cannot be
derived from the same conservative six-dimensional core. -/
theorem nativeK5RightNaturality_noCoreSixCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g)
    (h : NativeF55StructuralComparison p s t) :
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerRightPathTarget
        alpha (nativeK5UnitFiveReduction h))
      (NativeK5StructuralFiveCell.interchangerRightPathSource
        alpha (nativeK5UnitFiveReduction h))) := by
  rintro ⟨u⟩
  have hv := u.shapeCharge_sound false
  change (0 : ℤ) = 1 at hv
  norm_num at hv

/-- The NEW full P94D3Z grammar does fill the genuine left
naturality boundary that no core-only composite can fill.
The added generator is provably independent from that core. -/
theorem nativeK5LeftNaturality_newGeneratorEssential
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55StructuralComparison p r s)
    {h k : NativeF55StructuralComparison p s t}
    (beta : NativeK5StructuralFourCell p h k) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta)
      (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta)) ∧
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerLeftPathTarget
        (nativeK5UnitFiveReduction f) beta)
      (NativeK5StructuralFiveCell.interchangerLeftPathSource
        (nativeK5UnitFiveReduction f) beta)) := by
  exact ⟨⟨.interchangerLeftNaturality (nativeK5UnitFiveReduction f) beta⟩,
    nativeK5LeftNaturality_noCoreSixCell f beta⟩

/-- Likewise the NEW right-naturality generator is not expressible
by any composite of the OLD conservative 6D core constructors. -/
theorem nativeK5RightNaturality_newGeneratorEssential
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g)
    (h : NativeF55StructuralComparison p s t) :
    Nonempty (NativeK5StructuralSixCell p
      (NativeK5StructuralFiveCell.interchangerRightPathTarget
        alpha (nativeK5UnitFiveReduction h))
      (NativeK5StructuralFiveCell.interchangerRightPathSource
        alpha (nativeK5UnitFiveReduction h))) ∧
    ¬ Nonempty (NativeK5PrenaturalitySixCell p
      (NativeK5StructuralFiveCell.interchangerRightPathTarget
        alpha (nativeK5UnitFiveReduction h))
      (NativeK5StructuralFiveCell.interchangerRightPathSource
        alpha (nativeK5UnitFiveReduction h))) := by
  exact ⟨⟨.interchangerRightNaturality alpha (nativeK5UnitFiveReduction h)⟩,
    nativeK5RightNaturality_noCoreSixCell alpha h⟩

#print axioms NativeK5PrenaturalitySixCell
#print axioms NativeK5PrenaturalitySixCell.toFull
#print axioms NativeK5PrenaturalitySixCell.shapeCharge_sound
#print axioms nativeK5LeftNaturality_noCoreSixCell
#print axioms nativeK5RightNaturality_noCoreSixCell
#print axioms nativeK5LeftNaturality_newGeneratorEssential
#print axioms nativeK5RightNaturality_newGeneratorEssential

end
end Kuu.F112.Physical
