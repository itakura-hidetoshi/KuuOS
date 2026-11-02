import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AOHorizontalUnitNecessity
import Mathlib.Tactic

/-!
F112-P94D3GK5AP — exact independence of BOTH P94A context-unit
4-generators, even allowing the opposite context unit AND the
genuine P94A horizontal unit, with all 19 original constructors.

The two independent ZMod 2 observers on raw P92B proof HISTORY are:
  LeftParity:  leftContext + precompose, all else except trans/symm 0;
  RightParity: rightContext + postcompose, all else except trans/symm 0.
Each chosen horizontal proof contains exactly one of EACH of the
four actions, so BOTH observers are horizontally additive (the two
added 1s cancel modulo 2), even for raw identity proofs.

Every one of 16 P93 four-cell rules preserves both observers.
A leftContextUnit generator changes ONLY LeftParity; a
rightContextUnit changes ONLY RightParity; horizontalUnit changes
NEITHER. Counting the relevant primitive among ALL 19 P94A
four-cell constructors proves its exact minimum is ONE for
any context-identity normalization. This is source proof history,
not a shadow-level quotient substitution or a universal no-go for
all possible higher presentations.

Independent Kuu -> Qi only. Original P93/P94A unchanged.
Append-only, strict 空 authority, public root107 unchanged.
Pinned Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide, added axioms, Gray or global gluing.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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

/-- Left context/route-action mod-two observer on actual P92B proof terms. -/
def NativeF55P92AssocComparison.gk5apLeftParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) : ZMod 2 := by
  induction cell with
  | original old => exact 0
  | assocNaturality u v w => exact 0
  | refl route => exact 0
  | symm cell ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext cell later ih => exact ih + 1
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih => exact ih + 1
  | postcompose cell suffix ih => exact ih

/-- Definitional vertical 3-composition law; used before interchange normalization. -/
theorem NativeF55P92AssocComparison.gk5apLeftTrans_parity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5apLeftParity =
      f.gk5apLeftParity + g.gk5apLeftParity := rfl

/-- Horizontal P92B inserts paired leftContext/precompose
actions, which cancel in ZMod 2. -/
theorem NativeF55P92AssocComparison.gk5apLeftHorizontal_parity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5apLeftParity = f.gk5apLeftParity + g.gk5apLeftParity := by
  change (f.gk5apLeftParity + 1) + (g.gk5apLeftParity + 1) =
    f.gk5apLeftParity + g.gk5apLeftParity
  have htwo : (1 : ZMod 2) + 1 = 0 := by decide
  calc
    _ = (f.gk5apLeftParity + g.gk5apLeftParity) + (1 + 1) := by abel
    _ = f.gk5apLeftParity + g.gk5apLeftParity := by simp [htwo]

/-- All SIXTEEN P93 constructors preserve the Left observer. -/
theorem NativeF55P93AssocFourCell.gk5apLeftParity_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5apLeftParity = g.gk5apLeftParity := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : ZMod 2) + f.gk5apLeftParity = f.gk5apLeftParity
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5apLeftParity + (0 : ZMod 2) = f.gk5apLeftParity
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5apLeftParity + g.gk5apLeftParity) + h.gk5apLeftParity =
        f.gk5apLeftParity + (g.gk5apLeftParity + h.gk5apLeftParity)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : ZMod 2 => prior.gk5apLeftParity + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : ZMod 2 => z + suffix.gk5apLeftParity) ih
  | leftContext w later ih => exact congrArg (fun z : ZMod 2 => z + 1) ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact congrArg (fun z : ZMod 2 => z + 1) ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity] using
        congrArg (fun z : ZMod 2 => z + other.gk5apLeftParity) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity] using
        congrArg (fun z : ZMod 2 => other.gk5apLeftParity + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity,
        NativeF55P92AssocComparison.gk5apLeftTrans_parity]
      abel

/-- Genuine P93 cannot normalize the Left context identity. -/
theorem nativeGK5APP93LeftContextUnit_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.leftContext (.refl u) later)
      (NativeF55P92AssocComparison.refl (.leftContext u later))) := by
  rintro ⟨w⟩
  have h := w.gk5apLeftParity_sound
  change (1 : ZMod 2) = 0 at h
  norm_num at h

/-- Exact occurrence count of leftContextUnit in all 19 P94A constructors. -/
def NativeF55P94UnitFourCell.gk5apLeftUnitCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) : Nat := by
  induction w with
  | old w => exact 0
  | refl f => exact 0
  | symm w ih => exact ih
  | trans fg gh ihfg ihgh => exact ihfg + ihgh
  | verticalLeftUnit f => exact 0
  | verticalRightUnit f => exact 0
  | verticalAssoc f g h => exact 0
  | leftWhisker prior w ih => exact ih
  | rightWhisker w suffix ih => exact ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih => exact ih
  | horizontalRight other w ih => exact ih
  | interchange f₁ f₂ g₁ g₂ => exact 0
  | horizontalUnit u v => exact 0
  | leftContextUnit u later => exact 1
  | rightContextUnit earlier u => exact 0

/-- Zero count of Left unit implies preservation, despite arbitrary
horizontalUnit and opposite contextUnit generators and closures. -/
theorem NativeF55P94UnitFourCell.gk5apZeroLeft_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g)
    (hz : w.gk5apLeftUnitCount = 0) :
    f.gk5apLeftParity = g.gk5apLeftParity := by
  induction w with
  | old w => exact w.gk5apLeftParity_sound
  | refl f => rfl
  | symm w ih => exact (ih hz).symm
  | trans fg gh ihfg ihgh =>
      have hfg : fg.gk5apLeftUnitCount = 0 := by
        change fg.gk5apLeftUnitCount + gh.gk5apLeftUnitCount = 0 at hz
        omega
      have hgh : gh.gk5apLeftUnitCount = 0 := by
        change fg.gk5apLeftUnitCount + gh.gk5apLeftUnitCount = 0 at hz
        omega
      exact (ihfg hfg).trans (ihgh hgh)
  | verticalLeftUnit f =>
      change (0 : ZMod 2) + f.gk5apLeftParity = f.gk5apLeftParity
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5apLeftParity + (0 : ZMod 2) = f.gk5apLeftParity
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5apLeftParity + g.gk5apLeftParity) + h.gk5apLeftParity =
        f.gk5apLeftParity + (g.gk5apLeftParity + h.gk5apLeftParity)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : ZMod 2 => prior.gk5apLeftParity + z) (ih hz)
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : ZMod 2 => z + suffix.gk5apLeftParity) (ih hz)
  | leftContext w later ih => exact congrArg (fun z : ZMod 2 => z + 1) (ih hz)
  | rightContext earlier w ih => exact ih hz
  | precompose prior w ih => exact congrArg (fun z : ZMod 2 => z + 1) (ih hz)
  | postcompose w suffix ih => exact ih hz
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity] using
        congrArg (fun z : ZMod 2 => z + other.gk5apLeftParity) (ih hz)
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity] using
        congrArg (fun z : ZMod 2 => other.gk5apLeftParity + z) (ih hz)
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity,
        NativeF55P92AssocComparison.gk5apLeftTrans_parity]
      abel
  | horizontalUnit u v =>
      have h := NativeF55P92AssocComparison.gk5apLeftHorizontal_parity
        (NativeF55P92AssocComparison.refl u)
        (NativeF55P92AssocComparison.refl v)
      simpa [NativeF55P92AssocComparison.gk5apLeftParity] using h
  | leftContextUnit u later =>
      change (1 : Nat) = 0 at hz
      omega
  | rightContextUnit earlier u =>
      rfl

/-- Each actual left context identity normalization necessarily
uses this exact left-context generator at least once. -/
theorem nativeGK5APLeftContextUnit_requires_primitive
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (w : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.leftContext (.refl u) later)
      (NativeF55P92AssocComparison.refl (.leftContext u later))) :
    0 < w.gk5apLeftUnitCount := by
  by_contra h
  have hz : w.gk5apLeftUnitCount = 0 := by omega
  have heq := w.gk5apZeroLeft_sound hz
  change (1 : ZMod 2) = 0 at heq
  norm_num at heq

/-- Exactly one generator suffices, and none can avoid it. -/
theorem nativeGK5APLeftContextUnit_minimal_count
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (NativeF55P94UnitFourCell.leftContextUnit u later).gk5apLeftUnitCount = 1
      ∧ (∀ w : NativeF55P94UnitFourCell
          (NativeF55P92AssocComparison.leftContext (.refl u) later)
          (NativeF55P92AssocComparison.refl (.leftContext u later)),
          1 ≤ w.gk5apLeftUnitCount) := by
  constructor
  · rfl
  · intro w
    exact nativeGK5APLeftContextUnit_requires_primitive u later w

#print axioms NativeF55P92AssocComparison.gk5apLeftParity
#print axioms NativeF55P92AssocComparison.gk5apLeftTrans_parity
#print axioms NativeF55P92AssocComparison.gk5apLeftHorizontal_parity
#print axioms NativeF55P93AssocFourCell.gk5apLeftParity_sound
#print axioms nativeGK5APP93LeftContextUnit_noFourCell
#print axioms NativeF55P94UnitFourCell.gk5apLeftUnitCount
#print axioms NativeF55P94UnitFourCell.gk5apZeroLeft_sound
#print axioms nativeGK5APLeftContextUnit_requires_primitive
#print axioms nativeGK5APLeftContextUnit_minimal_count

/-- Right context/route-action mod-two observer on actual P92B proof terms. -/
def NativeF55P92AssocComparison.gk5apRightParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) : ZMod 2 := by
  induction cell with
  | original old => exact 0
  | assocNaturality u v w => exact 0
  | refl route => exact 0
  | symm cell ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih + 1
  | precompose prior cell ih => exact ih
  | postcompose cell suffix ih => exact ih + 1

/-- Definitional vertical 3-composition law; used before interchange normalization. -/
theorem NativeF55P92AssocComparison.gk5apRightTrans_parity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5apRightParity =
      f.gk5apRightParity + g.gk5apRightParity := rfl

/-- Horizontal P92B inserts paired rightContext/postcompose
actions, which cancel in ZMod 2. -/
theorem NativeF55P92AssocComparison.gk5apRightHorizontal_parity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5apRightParity = f.gk5apRightParity + g.gk5apRightParity := by
  change (f.gk5apRightParity + 1) + (g.gk5apRightParity + 1) =
    f.gk5apRightParity + g.gk5apRightParity
  have htwo : (1 : ZMod 2) + 1 = 0 := by decide
  calc
    _ = (f.gk5apRightParity + g.gk5apRightParity) + (1 + 1) := by abel
    _ = f.gk5apRightParity + g.gk5apRightParity := by simp [htwo]

/-- All SIXTEEN P93 constructors preserve the Right observer. -/
theorem NativeF55P93AssocFourCell.gk5apRightParity_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5apRightParity = g.gk5apRightParity := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : ZMod 2) + f.gk5apRightParity = f.gk5apRightParity
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5apRightParity + (0 : ZMod 2) = f.gk5apRightParity
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5apRightParity + g.gk5apRightParity) + h.gk5apRightParity =
        f.gk5apRightParity + (g.gk5apRightParity + h.gk5apRightParity)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : ZMod 2 => prior.gk5apRightParity + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : ZMod 2 => z + suffix.gk5apRightParity) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact congrArg (fun z : ZMod 2 => z + 1) ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact congrArg (fun z : ZMod 2 => z + 1) ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity] using
        congrArg (fun z : ZMod 2 => z + other.gk5apRightParity) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity] using
        congrArg (fun z : ZMod 2 => other.gk5apRightParity + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity,
        NativeF55P92AssocComparison.gk5apRightTrans_parity]
      abel

/-- Genuine P93 cannot normalize the Right context identity. -/
theorem nativeGK5APP93RightContextUnit_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.rightContext earlier (.refl u))
      (NativeF55P92AssocComparison.refl (.rightContext earlier u))) := by
  rintro ⟨w⟩
  have h := w.gk5apRightParity_sound
  change (1 : ZMod 2) = 0 at h
  norm_num at h

/-- Exact occurrence count of rightContextUnit in all 19 P94A constructors. -/
def NativeF55P94UnitFourCell.gk5apRightUnitCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) : Nat := by
  induction w with
  | old w => exact 0
  | refl f => exact 0
  | symm w ih => exact ih
  | trans fg gh ihfg ihgh => exact ihfg + ihgh
  | verticalLeftUnit f => exact 0
  | verticalRightUnit f => exact 0
  | verticalAssoc f g h => exact 0
  | leftWhisker prior w ih => exact ih
  | rightWhisker w suffix ih => exact ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih => exact ih
  | horizontalRight other w ih => exact ih
  | interchange f₁ f₂ g₁ g₂ => exact 0
  | horizontalUnit u v => exact 0
  | leftContextUnit u later => exact 0
  | rightContextUnit earlier u => exact 1

/-- Zero count of Right unit implies preservation, despite arbitrary
horizontalUnit and opposite contextUnit generators and closures. -/
theorem NativeF55P94UnitFourCell.gk5apZeroRight_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g)
    (hz : w.gk5apRightUnitCount = 0) :
    f.gk5apRightParity = g.gk5apRightParity := by
  induction w with
  | old w => exact w.gk5apRightParity_sound
  | refl f => rfl
  | symm w ih => exact (ih hz).symm
  | trans fg gh ihfg ihgh =>
      have hfg : fg.gk5apRightUnitCount = 0 := by
        change fg.gk5apRightUnitCount + gh.gk5apRightUnitCount = 0 at hz
        omega
      have hgh : gh.gk5apRightUnitCount = 0 := by
        change fg.gk5apRightUnitCount + gh.gk5apRightUnitCount = 0 at hz
        omega
      exact (ihfg hfg).trans (ihgh hgh)
  | verticalLeftUnit f =>
      change (0 : ZMod 2) + f.gk5apRightParity = f.gk5apRightParity
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5apRightParity + (0 : ZMod 2) = f.gk5apRightParity
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5apRightParity + g.gk5apRightParity) + h.gk5apRightParity =
        f.gk5apRightParity + (g.gk5apRightParity + h.gk5apRightParity)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : ZMod 2 => prior.gk5apRightParity + z) (ih hz)
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : ZMod 2 => z + suffix.gk5apRightParity) (ih hz)
  | leftContext w later ih => exact ih hz
  | rightContext earlier w ih => exact congrArg (fun z : ZMod 2 => z + 1) (ih hz)
  | precompose prior w ih => exact ih hz
  | postcompose w suffix ih => exact congrArg (fun z : ZMod 2 => z + 1) (ih hz)
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity] using
        congrArg (fun z : ZMod 2 => z + other.gk5apRightParity) (ih hz)
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity] using
        congrArg (fun z : ZMod 2 => other.gk5apRightParity + z) (ih hz)
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity,
        NativeF55P92AssocComparison.gk5apRightTrans_parity]
      abel
  | horizontalUnit u v =>
      have h := NativeF55P92AssocComparison.gk5apRightHorizontal_parity
        (NativeF55P92AssocComparison.refl u)
        (NativeF55P92AssocComparison.refl v)
      simpa [NativeF55P92AssocComparison.gk5apRightParity] using h
  | leftContextUnit u later =>
      rfl
  | rightContextUnit earlier u =>
      change (1 : Nat) = 0 at hz
      omega

/-- Each actual right context identity normalization necessarily
uses this exact right-context generator at least once. -/
theorem nativeGK5APRightContextUnit_requires_primitive
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (w : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.rightContext earlier (.refl u))
      (NativeF55P92AssocComparison.refl (.rightContext earlier u))) :
    0 < w.gk5apRightUnitCount := by
  by_contra h
  have hz : w.gk5apRightUnitCount = 0 := by omega
  have heq := w.gk5apZeroRight_sound hz
  change (1 : ZMod 2) = 0 at heq
  norm_num at heq

/-- Exactly one generator suffices, and none can avoid it. -/
theorem nativeGK5APRightContextUnit_minimal_count
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (NativeF55P94UnitFourCell.rightContextUnit earlier u).gk5apRightUnitCount = 1
      ∧ (∀ w : NativeF55P94UnitFourCell
          (NativeF55P92AssocComparison.rightContext earlier (.refl u))
          (NativeF55P92AssocComparison.refl (.rightContext earlier u)),
          1 ≤ w.gk5apRightUnitCount) := by
  constructor
  · rfl
  · intro w
    exact nativeGK5APRightContextUnit_requires_primitive earlier u w

#print axioms NativeF55P92AssocComparison.gk5apRightParity
#print axioms NativeF55P92AssocComparison.gk5apRightTrans_parity
#print axioms NativeF55P92AssocComparison.gk5apRightHorizontal_parity
#print axioms NativeF55P93AssocFourCell.gk5apRightParity_sound
#print axioms nativeGK5APP93RightContextUnit_noFourCell
#print axioms NativeF55P94UnitFourCell.gk5apRightUnitCount
#print axioms NativeF55P94UnitFourCell.gk5apZeroRight_sound
#print axioms nativeGK5APRightContextUnit_requires_primitive
#print axioms nativeGK5APRightContextUnit_minimal_count

end
end Kuu.F112.Physical
