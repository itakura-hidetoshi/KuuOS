import Kuu.F112.PolygonNativeF55P94DK5SixCellSquareProvenance
import Mathlib.Tactic

/-!
# F112-P94D3AD — conservative seven-cell grammar and 6D provenance obstruction

An actual source-typed 7D relation between SIX-cell proof witnesses.
Its conservative constructors include:
  reflexivity/inverse/composition, 6D associativity/units/inverse,
  left/right 6D vertical congruence, congruence under original 5D
  vertical left/right composition and 5D inverse, and both original
  typed F54 3-cell whiskerings.

This grammar deliberately does NOT identify primitive and derived
six-cell horizontal squares. Both original 6D square-generator
provenance coordinates are invariant under every 7D constructor.

Consequently a direct 6D target/source square proof and its
P94D3AC-derived counterpart have NO 7D filler in this core, even
though both share EXACT original 5D boundaries and genuine 6D
proof witnesses already exist. The theorem is RELATIVE to the
explicitly defined conservative 7D syntax, not an absolute no-go.
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

/-- A completely source-dependent conservative SEVEN-cell syntax
relating parallel genuine P94D3Z six-cell proof terms. -/
inductive NativeK5CoreSevenCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta},
      NativeK5StructuralSixCell p w z →
      NativeK5StructuralSixCell p w z →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5CoreSevenCell p u u
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p v u
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v q : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v)
      (k : NativeK5CoreSevenCell p v q) :
      NativeK5CoreSevenCell p u q
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z t : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v)
      (q : NativeK5StructuralSixCell p z t) :
      NativeK5CoreSevenCell p (.trans u q) (.trans v q)
  | verticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z t : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p z t}
      (q : NativeK5StructuralSixCell p w z)
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p (.trans q u) (.trans q v)
  | verticalAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q t : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z)
      (v : NativeK5StructuralSixCell p z q)
      (h : NativeK5StructuralSixCell p q t) :
      NativeK5CoreSevenCell p
        (.trans (.trans u v) h) (.trans u (.trans v h))
  | verticalLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5CoreSevenCell p (.trans (.refl w) u) u
  | verticalRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5CoreSevenCell p (.trans u (.refl z)) u
  | inverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5CoreSevenCell p (.trans u (.symm u)) (.refl w)
  | inverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5CoreSevenCell p (.trans (.symm u) u) (.refl z)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p (.symm u) (.symm v)
  | fiveVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v)
      (suffix : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5CoreSevenCell p
        (.verticalLeft u suffix) (.verticalLeft v suffix)
  | fiveVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      (lead : NativeK5StructuralFiveCell p alpha beta)
      {w z : NativeK5StructuralFiveCell p beta gamma}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p
        (.verticalRight lead u) (.verticalRight lead v)
  | fiveInverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p
        (.inverseRespect u) (.inverseRespect v)
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
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v) :
      NativeK5CoreSevenCell p
        (.precompose prior u) (.precompose prior v)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      (h : NativeK5CoreSevenCell p u v)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5CoreSevenCell p
        (.postcompose u suffix) (.postcompose v suffix)


/-- The two independent signed SIX-cell square-provenance axes
are invariant under ALL conservative source-typed 7D generators,
including 5D inverse, 6D inverse, F54 whiskering and pasting. -/
theorem NativeK5CoreSevenCell.squareProvenance_sound
    (selectTarget : Bool)
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5CoreSevenCell p u v) :
    u.squareProvenance selectTarget = v.squareProvenance selectTarget := by
  induction h with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralSixCell.squareProvenance] using
        congrArg (fun t : ℤ => t + suffix.squareProvenance selectTarget) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralSixCell.squareProvenance] using
        congrArg (fun t : ℤ => lead.squareProvenance selectTarget + t) ih
  | verticalAssoc u v h =>
      change (u.squareProvenance selectTarget + v.squareProvenance selectTarget) +
        h.squareProvenance selectTarget =
        u.squareProvenance selectTarget +
          (v.squareProvenance selectTarget + h.squareProvenance selectTarget)
      exact add_assoc _ _ _
  | verticalLeftUnit _ => simp [NativeK5StructuralSixCell.squareProvenance]
  | verticalRightUnit _ => simp [NativeK5StructuralSixCell.squareProvenance]
  | inverseLeft _ => simp [NativeK5StructuralSixCell.squareProvenance]
  | inverseRight _ => simp [NativeK5StructuralSixCell.squareProvenance]
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralSixCell.squareProvenance] using
        congrArg (fun t : ℤ => -t) ih
  | fiveVerticalLeft witness suffix ih => exact ih
  | fiveVerticalRight lead witness ih => exact ih
  | fiveInverseRespect witness ih =>
      simpa only [NativeK5StructuralSixCell.squareProvenance] using
        congrArg (fun t : ℤ => -t) ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih

/-- No conservative 7D witness between the two ACTUAL parallel
target-square six-cell proofs: target-square 6D generator
provenance is 1 vs 0, even though their 5D boundaries coincide. -/
theorem nativeK5TargetSquare_noCoreSevenCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5SixTargetSquareDirect w v)
      (nativeK5SixTargetSquareViaSource w v)) := by
  rintro ⟨h⟩
  have hc := h.squareProvenance_sound true
  change (1 : ℤ) = 0 at hc
  norm_num at hc

/-- Complementary source-square non-derivability in the SAME
conservative 7D grammar, by the independent source-axis count. -/
theorem nativeK5SourceSquare_noCoreSevenCell
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5SixSourceSquareDirect w v)
      (nativeK5SixSourceSquareViaTarget w v)) := by
  rintro ⟨h⟩
  have hc := h.squareProvenance_sound false
  change (1 : ℤ) = 0 at hc
  norm_num at hc

#print axioms NativeK5CoreSevenCell
#print axioms NativeK5CoreSevenCell.squareProvenance_sound
#print axioms nativeK5TargetSquare_noCoreSevenCell
#print axioms nativeK5SourceSquare_noCoreSevenCell

end
end Kuu.F112.Physical
