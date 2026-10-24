import Kuu.F112.PolygonNativeF55P94DK5CoreSevenCellProvenanceObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AD — independently generated genuine seven-cell square comparison

P94D3AC supplies TWO genuinely distinct six-cell proofs of every
target/source square boundary. Their old free six-cell proof terms
are NOT equal, and conservative 7D structural rules cannot connect
them (P94D3AD source-dependent provenance obstruction).

This file ADJOINS two independent Type-valued seven-cell comparison
GENERATOR families at those exact old source-typed six-cell proof
boundaries, closes them under inverses, vertical composition,
whiskering and original 5D congruences.

It proves a coarse TOTAL 6D horizontal-square provenance survives
every new seven-cell constructor, while the finer two coordinates
do not survive the new comparison generators. This is a model for
a NEW higher presentation, not a claim of old P92B descent or
a uniqueness/coherence theorem for arbitrary 7D pastings.
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

/-- The sum forgets WHICH of the two independent 6D square
constructor families was used but retains the signed total. -/
def NativeK5StructuralSixCell.totalSquareProvenance
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) : ℤ :=
  u.squareProvenance true + u.squareProvenance false

/-- Additivity under original source-dependent 6D vertical pasting. -/
theorem NativeK5StructuralSixCell.totalSquareProvenance_trans
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z q : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z)
    (v : NativeK5StructuralSixCell p z q) :
    (NativeK5StructuralSixCell.trans u v).totalSquareProvenance =
      u.totalSquareProvenance + v.totalSquareProvenance := by
  change (u.squareProvenance true + v.squareProvenance true) +
      (u.squareProvenance false + v.squareProvenance false) =
    (u.squareProvenance true + u.squareProvenance false) +
      (v.squareProvenance true + v.squareProvenance false)
  abel

/-- Reversing a genuine 6D proof negates its total 6D provenance. -/
theorem NativeK5StructuralSixCell.totalSquareProvenance_symm
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) :
    (NativeK5StructuralSixCell.symm u).totalSquareProvenance =
      -u.totalSquareProvenance := by
  change (-u.squareProvenance true) + (-u.squareProvenance false) =
    -(u.squareProvenance true + u.squareProvenance false)
  abel

/-- Original 5D inversion congruence also negates 6D square
provenance. No extensional equality of 5D proofs is assumed. -/
theorem NativeK5StructuralSixCell.totalSquareProvenance_fiveInverse
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) :
    (NativeK5StructuralSixCell.inverseRespect u).totalSquareProvenance =
      -u.totalSquareProvenance := by
  change (-u.squareProvenance true) + (-u.squareProvenance false) =
    -(u.squareProvenance true + u.squareProvenance false)
  abel

/-- Independently specified typed 7D grammar of genuine 6D
proof-term comparisons, not just an integer-level quotient. -/
inductive NativeK5StructuralSevenCell (p : Polygon) :
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
  | core
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
      NativeK5StructuralSevenCell p u v
  | targetComparison
      {a b : D} {x y : E} {n n' m m' : Nat}
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
      NativeK5StructuralSevenCell p
        (nativeK5SixTargetSquareDirect w v)
        (nativeK5SixTargetSquareViaSource w v)
  | sourceComparison
      {a b : D} {x y : E} {n n' m m' : Nat}
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
      NativeK5StructuralSevenCell p
        (nativeK5SixSourceSquareDirect w v)
        (nativeK5SixSourceSquareViaTarget w v)
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p v u
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
      (h : NativeK5StructuralSevenCell p u v)
      (k : NativeK5StructuralSevenCell p v q) :
      NativeK5StructuralSevenCell p u q
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
      (h : NativeK5StructuralSevenCell p u v)
      (q : NativeK5StructuralSixCell p z t) :
      NativeK5StructuralSevenCell p (.trans u q) (.trans v q)
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p (.trans q u) (.trans q v)
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p (.symm u) (.symm v)
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
      (h : NativeK5StructuralSevenCell p u v)
      (suffix : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5StructuralSevenCell p
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p
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
      (h : NativeK5StructuralSevenCell p u v) :
      NativeK5StructuralSevenCell p
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
      (h : NativeK5StructuralSevenCell p u v)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5StructuralSevenCell p
        (.postcompose u suffix) (.postcompose v suffix)


/-- The NEW 7D square comparison proof preserves the COARSE
total 6D square-generator number, though not either fine axis.
Complete induction over every 7D source-dependent generator. -/
theorem NativeK5StructuralSevenCell.totalSquareProvenance_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    (h : NativeK5StructuralSevenCell p u v) :
    u.totalSquareProvenance = v.totalSquareProvenance := by
  induction h with
  | core witness =>
      unfold NativeK5StructuralSixCell.totalSquareProvenance
      rw [witness.squareProvenance_sound true,
        witness.squareProvenance_sound false]
  | targetComparison w v =>
      change (1 : ℤ) + 0 = 0 + 1
      norm_num
  | sourceComparison w v =>
      change (0 : ℤ) + 1 = 1 + 0
      norm_num
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralSixCell.totalSquareProvenance_trans] using
        congrArg (fun t : ℤ => t + suffix.totalSquareProvenance) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralSixCell.totalSquareProvenance_trans] using
        congrArg (fun t : ℤ => lead.totalSquareProvenance + t) ih
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralSixCell.totalSquareProvenance_symm] using
        congrArg (fun t : ℤ => -t) ih
  | fiveVerticalLeft witness suffix ih => exact ih
  | fiveVerticalRight lead witness ih => exact ih
  | fiveInverseRespect witness ih =>
      simpa only [NativeK5StructuralSixCell.totalSquareProvenance_fiveInverse] using
        congrArg (fun t : ℤ => -t) ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih

/-- Relative 7D necessity: the *new independent* target comparison
fills precisely the source-typed 6D boundary obstructed in
the conservative 7D grammar. -/
theorem nativeK5TargetComparison_newSevenGeneratorEssential
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
    Nonempty (NativeK5StructuralSevenCell p
      (nativeK5SixTargetSquareDirect w v)
      (nativeK5SixTargetSquareViaSource w v)) ∧
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5SixTargetSquareDirect w v)
      (nativeK5SixTargetSquareViaSource w v)) := by
  exact ⟨⟨.targetComparison w v⟩,
    nativeK5TargetSquare_noCoreSevenCell w v⟩

/-- Relative necessity on the independent SOURCE square family. -/
theorem nativeK5SourceComparison_newSevenGeneratorEssential
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
    Nonempty (NativeK5StructuralSevenCell p
      (nativeK5SixSourceSquareDirect w v)
      (nativeK5SixSourceSquareViaTarget w v)) ∧
    ¬ Nonempty (NativeK5CoreSevenCell p
      (nativeK5SixSourceSquareDirect w v)
      (nativeK5SixSourceSquareViaTarget w v)) := by
  exact ⟨⟨.sourceComparison w v⟩,
    nativeK5SourceSquare_noCoreSevenCell w v⟩

#print axioms NativeK5StructuralSixCell.totalSquareProvenance
#print axioms NativeK5StructuralSixCell.totalSquareProvenance_trans
#print axioms NativeK5StructuralSixCell.totalSquareProvenance_symm
#print axioms NativeK5StructuralSixCell.totalSquareProvenance_fiveInverse
#print axioms NativeK5StructuralSevenCell
#print axioms NativeK5StructuralSevenCell.totalSquareProvenance_sound
#print axioms nativeK5TargetComparison_newSevenGeneratorEssential
#print axioms nativeK5SourceComparison_newSevenGeneratorEssential

end
end Kuu.F112.Physical
