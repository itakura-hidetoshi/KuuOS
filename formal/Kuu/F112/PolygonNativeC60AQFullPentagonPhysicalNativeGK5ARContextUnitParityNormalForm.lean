import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AQP89P94ReflectionObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5AR — exact ZMod2 two-context-unit provenance normal
form across all NINETEEN genuine P94A four-cell constructors.

GK5AP proved that both left/right context unit generators
are individually indispensable. GK5AQ isolated actual P89→P94A
nonfaithfulness as an unconstructed source-typed bad pair.
Here prove, for EVERY selected P94A 4-cell derivation w,
  (countL(w),countR(w)) mod 2
  = (I_L(target)-I_L(source), I_R(target)-I_R(source)).
Thus ANY TWO proofs with the same Type-valued endpoints have
identical context-unit count parities. Left normalization is
(odd,even), right is (even,odd), and horizontal unit has
(even,even) context count. This is more precise than a positive
lower bound but does not construct a unique 4-cell normal form.

All original P89/P93/P94A, Type-valued F55 and C60 evidence
retained without rewrite. No sorry/admit/native_decide, new
axioms, Gray or global gluing. Independent Kuu → Qi only,
strict 空 authority, public root107 unchanged.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/open/unmerged.
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

private theorem nativeGK5ARTwice_zero (z : ZMod 2) : z + z = 0 := by
  have htwo : (2 : ZMod 2) = 0 := by decide
  calc
    z + z = (2 : ZMod 2) * z := by ring
    _ = 0 := by simp [htwo]

theorem NativeF55P94UnitFourCell.gk5arLeftParity_grade
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5apLeftParity + ((w.gk5apLeftUnitCount : Nat) : ZMod 2) = g.gk5apLeftParity := by
  induction w with
  | old w =>
      change _ + (0 : ZMod 2) = _
      simpa only [add_zero] using w.gk5apLeftParity_sound
  | refl f =>
      change f.gk5apLeftParity + (0 : ZMod 2) = f.gk5apLeftParity
      exact add_zero _
  | symm w ih =>
      change _ + (w.gk5apLeftUnitCount : ZMod 2) = _
      rw [← ih, add_assoc, nativeGK5ARTwice_zero, add_zero]
  | trans fg gh ihfg ihgh =>
      change _ + ((fg.gk5apLeftUnitCount + gh.gk5apLeftUnitCount : Nat) : ZMod 2) = _
      rw [Nat.cast_add, ← add_assoc, ihfg, ihgh]
  | verticalLeftUnit f =>
      change ((0 : ZMod 2) + f.gk5apLeftParity) + 0 = f.gk5apLeftParity
      simp
  | verticalRightUnit f =>
      change (f.gk5apLeftParity + (0 : ZMod 2)) + 0 = f.gk5apLeftParity
      simp
  | verticalAssoc f g h =>
      change ((f.gk5apLeftParity + g.gk5apLeftParity) + h.gk5apLeftParity) + 0 =
        f.gk5apLeftParity + (g.gk5apLeftParity + h.gk5apLeftParity)
      simp only [add_zero, add_assoc]
  | leftWhisker prior w ih =>
      change (prior.gk5apLeftParity + _) + (w.gk5apLeftUnitCount : ZMod 2) = prior.gk5apLeftParity + _
      rw [add_assoc, ih]
  | rightWhisker w suffix ih =>
      change (_ + suffix.gk5apLeftParity) + (w.gk5apLeftUnitCount : ZMod 2) = _ + suffix.gk5apLeftParity
      rw [← ih]
      abel
  | leftContext w later ih =>
      change (_ + (1 : ZMod 2)) + (w.gk5apLeftUnitCount : ZMod 2) = _ + 1
      rw [← ih]
      abel
  | rightContext earlier w ih =>
      exact ih
  | precompose prior w ih =>
      change (_ + (1 : ZMod 2)) + (w.gk5apLeftUnitCount : ZMod 2) = _ + 1
      rw [← ih]
      abel
  | postcompose w suffix ih =>
      exact ih
  | horizontalLeft w other ih =>
      simp only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity]
      rw [← ih]
      abel
  | horizontalRight other w ih =>
      simp only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity]
      rw [← ih]
      abel
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity,
        NativeF55P92AssocComparison.gk5apLeftTrans_parity]
      abel
  | horizontalUnit u v =>
      change ((NativeF55P92AssocComparison.refl u).horizontal
          (NativeF55P92AssocComparison.refl v)).gk5apLeftParity + 0 = 0
      rw [NativeF55P92AssocComparison.gk5apLeftHorizontal_parity]
      norm_num [NativeF55P92AssocComparison.gk5apLeftParity]
  | leftContextUnit u later =>
      change (1 : ZMod 2) + 1 = 0
      decide
  | rightContextUnit earlier u =>
      change (0 : ZMod 2) + 0 = 0
      rfl

/-- Two genuine P94A certificates with identical typed endpoints
have exactly the same Left context-unit count parity. -/
theorem NativeF55P94UnitFourCell.gk5arLeftCountParity_rigid
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w₁ w₂ : NativeF55P94UnitFourCell f g) :
    ((w₁.gk5apLeftUnitCount : Nat) : ZMod 2) =
      ((w₂.gk5apLeftUnitCount : Nat) : ZMod 2) := by
  have h₁ := w₁.gk5arLeftParity_grade
  have h₂ := w₂.gk5arLeftParity_grade
  exact add_left_cancel (h₁.trans h₂.symm)

theorem NativeF55P94UnitFourCell.gk5arRightParity_grade
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5apRightParity + ((w.gk5apRightUnitCount : Nat) : ZMod 2) = g.gk5apRightParity := by
  induction w with
  | old w =>
      change _ + (0 : ZMod 2) = _
      simpa only [add_zero] using w.gk5apRightParity_sound
  | refl f =>
      change f.gk5apRightParity + (0 : ZMod 2) = f.gk5apRightParity
      exact add_zero _
  | symm w ih =>
      change _ + (w.gk5apRightUnitCount : ZMod 2) = _
      rw [← ih, add_assoc, nativeGK5ARTwice_zero, add_zero]
  | trans fg gh ihfg ihgh =>
      change _ + ((fg.gk5apRightUnitCount + gh.gk5apRightUnitCount : Nat) : ZMod 2) = _
      rw [Nat.cast_add, ← add_assoc, ihfg, ihgh]
  | verticalLeftUnit f =>
      change ((0 : ZMod 2) + f.gk5apRightParity) + 0 = f.gk5apRightParity
      simp
  | verticalRightUnit f =>
      change (f.gk5apRightParity + (0 : ZMod 2)) + 0 = f.gk5apRightParity
      simp
  | verticalAssoc f g h =>
      change ((f.gk5apRightParity + g.gk5apRightParity) + h.gk5apRightParity) + 0 =
        f.gk5apRightParity + (g.gk5apRightParity + h.gk5apRightParity)
      simp only [add_zero, add_assoc]
  | leftWhisker prior w ih =>
      change (prior.gk5apRightParity + _) + (w.gk5apRightUnitCount : ZMod 2) = prior.gk5apRightParity + _
      rw [add_assoc, ih]
  | rightWhisker w suffix ih =>
      change (_ + suffix.gk5apRightParity) + (w.gk5apRightUnitCount : ZMod 2) = _ + suffix.gk5apRightParity
      rw [← ih]
      abel
  | leftContext w later ih =>
      exact ih
  | rightContext earlier w ih =>
      change (_ + (1 : ZMod 2)) + (w.gk5apRightUnitCount : ZMod 2) = _ + 1
      rw [← ih]
      abel
  | precompose prior w ih =>
      exact ih
  | postcompose w suffix ih =>
      change (_ + (1 : ZMod 2)) + (w.gk5apRightUnitCount : ZMod 2) = _ + 1
      rw [← ih]
      abel
  | horizontalLeft w other ih =>
      simp only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity]
      rw [← ih]
      abel
  | horizontalRight other w ih =>
      simp only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity]
      rw [← ih]
      abel
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5apRightHorizontal_parity,
        NativeF55P92AssocComparison.gk5apRightTrans_parity]
      abel
  | horizontalUnit u v =>
      change ((NativeF55P92AssocComparison.refl u).horizontal
          (NativeF55P92AssocComparison.refl v)).gk5apRightParity + 0 = 0
      rw [NativeF55P92AssocComparison.gk5apRightHorizontal_parity]
      norm_num [NativeF55P92AssocComparison.gk5apRightParity]
  | leftContextUnit u later =>
      change (0 : ZMod 2) + 0 = 0
      rfl
  | rightContextUnit earlier u =>
      change (1 : ZMod 2) + 1 = 0
      decide

/-- Two genuine P94A certificates with identical typed endpoints
have exactly the same Right context-unit count parity. -/
theorem NativeF55P94UnitFourCell.gk5arRightCountParity_rigid
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w₁ w₂ : NativeF55P94UnitFourCell f g) :
    ((w₁.gk5apRightUnitCount : Nat) : ZMod 2) =
      ((w₂.gk5apRightUnitCount : Nat) : ZMod 2) := by
  have h₁ := w₁.gk5arRightParity_grade
  have h₂ := w₂.gk5arRightParity_grade
  exact add_left_cancel (h₁.trans h₂.symm)

/-- For EVERY P94A four-cell the entire left/right
primitive parity vector is determined by the two raw endpoints. -/
theorem NativeF55P94UnitFourCell.gk5arContextParity_normalForm
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2),
      ((w.gk5apRightUnitCount : Nat) : ZMod 2)) =
      (g.gk5apLeftParity - f.gk5apLeftParity,
       g.gk5apRightParity - f.gk5apRightParity) := by
  apply Prod.ext
  · calc
      ((w.gk5apLeftUnitCount : Nat) : ZMod 2) =
          (f.gk5apLeftParity +
            ((w.gk5apLeftUnitCount : Nat) : ZMod 2)) -
            f.gk5apLeftParity := by abel
      _ = g.gk5apLeftParity - f.gk5apLeftParity := by
        rw [w.gk5arLeftParity_grade]
  · calc
      ((w.gk5apRightUnitCount : Nat) : ZMod 2) =
          (f.gk5apRightParity +
            ((w.gk5apRightUnitCount : Nat) : ZMod 2)) -
            f.gk5apRightParity := by abel
      _ = g.gk5apRightParity - f.gk5apRightParity := by
        rw [w.gk5arRightParity_grade]

/-- Proof history may differ but its two-component count parity
cannot differ for fixed P94A source and target evidence. -/
theorem NativeF55P94UnitFourCell.gk5arContextParity_rigid
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w₁ w₂ : NativeF55P94UnitFourCell f g) :
    (((w₁.gk5apLeftUnitCount : Nat) : ZMod 2),
      ((w₁.gk5apRightUnitCount : Nat) : ZMod 2)) =
    (((w₂.gk5apLeftUnitCount : Nat) : ZMod 2),
      ((w₂.gk5apRightUnitCount : Nat) : ZMod 2)) :=
  Prod.ext (w₁.gk5arLeftCountParity_rigid w₂)
    (w₁.gk5arRightCountParity_rigid w₂)

/-- Every genuine Left context normalization has
exact odd left/even right primitive counts. -/
theorem nativeGK5ARLeftContextUnit_exactParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (w : NativeF55P94UnitFourCell (NativeF55P92AssocComparison.leftContext (.refl u) later) (NativeF55P92AssocComparison.refl (.leftContext u later))) :
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 1) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  have h := w.gk5arContextParity_rigid (NativeF55P94UnitFourCell.leftContextUnit u later)
  exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩

/-- Every genuine Right context normalization has
exact even left/odd right primitive counts. -/
theorem nativeGK5ARRightContextUnit_exactParity
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (w : NativeF55P94UnitFourCell (NativeF55P92AssocComparison.rightContext earlier (.refl u)) (NativeF55P92AssocComparison.refl (.rightContext earlier u))) :
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 1) := by
  have h := w.gk5arContextParity_rigid (NativeF55P94UnitFourCell.rightContextUnit earlier u)
  exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩

/-- A genuine horizontal identity normalization has even
counts of BOTH context unit primitives. HorizontalUnit has a
separate GK5AO minimal count but no asserted mod-two rigidity. -/
theorem nativeGK5ARHorizontalUnit_contextParity_even
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter)
    (w : NativeF55P94UnitFourCell
      ((NativeF55P92AssocComparison.refl u).horizontal
        (NativeF55P92AssocComparison.refl v))
      (NativeF55P92AssocComparison.refl
        (nativeF54P90HorizontalRoute u v))) :
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  have h := w.gk5arContextParity_rigid
    (NativeF55P94UnitFourCell.horizontalUnit u v)
  exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩

#print axioms NativeF55P94UnitFourCell.gk5arLeftParity_grade
#print axioms NativeF55P94UnitFourCell.gk5arRightParity_grade
#print axioms NativeF55P94UnitFourCell.gk5arLeftCountParity_rigid
#print axioms NativeF55P94UnitFourCell.gk5arRightCountParity_rigid
#print axioms NativeF55P94UnitFourCell.gk5arContextParity_normalForm
#print axioms NativeF55P94UnitFourCell.gk5arContextParity_rigid
#print axioms nativeGK5ARLeftContextUnit_exactParity
#print axioms nativeGK5ARRightContextUnit_exactParity
#print axioms nativeGK5ARHorizontalUnit_contextParity_even

end
end Kuu.F112.Physical
