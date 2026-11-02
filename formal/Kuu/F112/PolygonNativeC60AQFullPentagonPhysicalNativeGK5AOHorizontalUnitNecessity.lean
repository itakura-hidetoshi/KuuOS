import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ANStructuralP89ToP94A
import Kuu.F112.PolygonNativeF55P94UnitFourCellPresentation
import Mathlib.Tactic

/-!
F112-P94D3GK5AO — a genuine Boolean invariant proving the ORIGINAL
P80 horizontal-unit four-cell is INDEPENDENT of P93 plus both
P94A context-unit four-cell generators (within the actual P94A
free Type-valued presentation).

GK5AM constructed a ZMod2 context-constructor parity witnessing
the failure to lift the original P80 left/right context-unit four-
cells into P93C. GK5AN then used the already existing P94A
presentation with three explicitly chosen primitive units to
construct a full original P89→P94A structural four-cell lift.

The remaining issue is whether P94A's horizontalUnit 4-generator
is redundant given its leftContextUnit and rightContextUnit.

Construct a DIFFERENT Bool invariant on raw selected P92B 3-proofs:
- original F55 / added assocNaturality / refl are false,
- symm preserves, trans uses Bool.or,
- left/right context preserves,
- precompose and postcompose of an arbitrary 3-proof are TRUE.
The actual P92B horizontal 3-proof operation contains precisely
one precompose and one postcompose, and so its Boolean flag is
ALWAYS true, even on both source identities.

All SIXTEEN true P93 four-cell rules preserve this invariant.
So do P94A's new leftContextUnit and rightContextUnit. But the
new P94A horizontalUnit has source flag TRUE and target FALSE.
A recursive natural-number count of occurrences of the explicit
P94A horizontalUnit generator in any genuine Type-valued 4-cell
certificate now proves: a P94A witness with count ZERO must
preserve the Bool invariant, hence EVERY horizontal-unit
four-cell certificate between the actual typed source and target
uses the horizontalUnit primitive AT LEAST ONCE. The old P93
presentation itself has no such four-cell.

This proves the exact non-redundancy of the third generator
relative to the original P93 and both context units (including
their full closure operations). It is not a universal assertion
about every other possible higher presentation. No original
F54/F55 proof history, physical C60 Edge, source signatures or
actual P94A generator was erased/rewritten. No numerical shadow
equality was promoted to a four-cell. Independent Kuu -> Qi only,
strict 空 authority; append-only/tighten-only, root107.
Protect PR #1558 Draft/open/unmerged; pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide, new axioms, Gray or global gluing.
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

/-- Actual P92B three-proof Boolean observer. Pre/post F54 route
actions on proof terms are distinguished from BOTH true context
constructors and original (atomic) three-proof histories. -/
def NativeF55P92AssocComparison.gk5aoRouteActionFlag
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) : Bool := by
  induction cell with
  | original old => exact false
  | assocNaturality u v w => exact false
  | refl route => exact false
  | symm cell ih => exact ih
  | trans f g ihf ihg => exact ihf || ihg
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih => exact true
  | postcompose cell suffix ih => exact true

/-- Vertical source three-cell pasting uses Boolean disjunction. -/
theorem NativeF55P92AssocComparison.gk5aoTrans_flag
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5aoRouteActionFlag =
      (f.gk5aoRouteActionFlag || g.gk5aoRouteActionFlag) := rfl

/-- The TRUE P92B horizontal composition has an explicit pre- and
post-F54-route action, hence is always flagged. This is a
definitional property of the actual proof term, not an axiom. -/
theorem NativeF55P92AssocComparison.gk5aoHorizontal_flag
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
    (f.horizontal g).gk5aoRouteActionFlag = true := rfl

/-- ALL genuine P93 four-cells preserve the new flag, even
interchange, original P89 witnesses, both whiskers, context
actions and vertical units/associativity. -/
theorem NativeF55P93AssocFourCell.gk5aoRouteActionFlag_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5aoRouteActionFlag = g.gk5aoRouteActionFlag := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f => rfl
  | verticalRightUnit f =>
      change (f.gk5aoRouteActionFlag || false) = f.gk5aoRouteActionFlag
      cases f.gk5aoRouteActionFlag <;> rfl
  | verticalAssoc f g h =>
      change (f.gk5aoRouteActionFlag || g.gk5aoRouteActionFlag) ||
        h.gk5aoRouteActionFlag =
        f.gk5aoRouteActionFlag ||
          (g.gk5aoRouteActionFlag || h.gk5aoRouteActionFlag)
      cases f.gk5aoRouteActionFlag <;>
        cases g.gk5aoRouteActionFlag <;>
          cases h.gk5aoRouteActionFlag <;> rfl
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Bool => prior.gk5aoRouteActionFlag || z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Bool => z || suffix.gk5aoRouteActionFlag) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => rfl
  | postcompose w suffix ih => rfl
  | horizontalLeft w other ih => rfl
  | horizontalRight other w ih => rfl
  | interchange f₁ f₂ g₁ g₂ => rfl

/-- A source-local proof of P93's inability to normalize genuine
horizontal P92B identities. This is independent of GK5AM's
different left/right CONTEXT parity obstruction. -/
theorem nativeGK5AOP93HorizontalUnit_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ¬ Nonempty (NativeF55P93AssocFourCell
      ((NativeF55P92AssocComparison.refl u).horizontal
        (NativeF55P92AssocComparison.refl v))
      (NativeF55P92AssocComparison.refl
        (nativeF54P90HorizontalRoute u v))) := by
  rintro ⟨w⟩
  have h := w.gk5aoRouteActionFlag_sound
  change true = false at h
  cases h

/-- EXACT source-provenance measure: number of explicit
horizontalUnit generator occurrences in a genuine P94A 4-cell
derivation, retaining ALL 19 constructors and nested histories. -/
def NativeF55P94UnitFourCell.gk5aoHorizontalUnitCount
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
  | horizontalUnit u v => exact 1
  | leftContextUnit u later => exact 0
  | rightContextUnit earlier u => exact 0

/-- A genuine P94A derivation with ZERO horizontalUnit generators
cannot change the Bool flag: this includes every historical P93
four-cell and any left/right context-unit proof, with their full
repeated vertical/horizontal/route/context closure. -/
theorem NativeF55P94UnitFourCell.gk5aoZeroHorizontal_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g)
    (hz : w.gk5aoHorizontalUnitCount = 0) :
    f.gk5aoRouteActionFlag = g.gk5aoRouteActionFlag := by
  induction w with
  | old w => exact w.gk5aoRouteActionFlag_sound
  | refl f => rfl
  | symm w ih => exact (ih hz).symm
  | trans fg gh ihfg ihgh =>
      have hfg : fg.gk5aoHorizontalUnitCount = 0 := by
        change fg.gk5aoHorizontalUnitCount + gh.gk5aoHorizontalUnitCount = 0 at hz
        omega
      have hgh : gh.gk5aoHorizontalUnitCount = 0 := by
        change fg.gk5aoHorizontalUnitCount + gh.gk5aoHorizontalUnitCount = 0 at hz
        omega
      exact (ihfg hfg).trans (ihgh hgh)
  | verticalLeftUnit f => rfl
  | verticalRightUnit f =>
      change (f.gk5aoRouteActionFlag || false) = f.gk5aoRouteActionFlag
      cases f.gk5aoRouteActionFlag <;> rfl
  | verticalAssoc f g h =>
      change (f.gk5aoRouteActionFlag || g.gk5aoRouteActionFlag) ||
        h.gk5aoRouteActionFlag =
        f.gk5aoRouteActionFlag ||
          (g.gk5aoRouteActionFlag || h.gk5aoRouteActionFlag)
      cases f.gk5aoRouteActionFlag <;>
        cases g.gk5aoRouteActionFlag <;>
          cases h.gk5aoRouteActionFlag <;> rfl
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Bool => prior.gk5aoRouteActionFlag || z) (ih hz)
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Bool => z || suffix.gk5aoRouteActionFlag) (ih hz)
  | leftContext w later ih => exact ih hz
  | rightContext earlier w ih => exact ih hz
  | precompose prior w ih => rfl
  | postcompose w suffix ih => rfl
  | horizontalLeft w other ih => rfl
  | horizontalRight other w ih => rfl
  | interchange f₁ f₂ g₁ g₂ => rfl
  | horizontalUnit u v =>
      change (1 : Nat) = 0 at hz
      omega
  | leftContextUnit u later => rfl
  | rightContextUnit earlier u => rfl

/-- Exact positive count lower bound: EVERY actual P94A four-cell
normalizing a horizontal pair of raw P92B identities to the
horizontal identity must use its NEW horizontalUnit generator
at least once. Left/right context units cannot replace it. -/
theorem nativeGK5AOHorizontalUnit_requires_primitive
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
    0 < w.gk5aoHorizontalUnitCount := by
  by_contra h
  have hz : w.gk5aoHorizontalUnitCount = 0 := by omega
  have heq := w.gk5aoZeroHorizontal_sound hz
  change true = false at heq
  cases heq

/-- One actual primitive horizontalUnit four-cell is sufficient,
and the source-provenance count of that explicit constructor is
exactly ONE. Together with the previous lower bound, this is an
exact minimum certificate count in the chosen P94A presentation. -/
theorem nativeGK5AOHorizontalUnit_minimal_count
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (NativeF55P94UnitFourCell.horizontalUnit u v).gk5aoHorizontalUnitCount = 1
      ∧ (∀ w : NativeF55P94UnitFourCell
          ((NativeF55P92AssocComparison.refl u).horizontal
            (NativeF55P92AssocComparison.refl v))
          (NativeF55P92AssocComparison.refl
            (nativeF54P90HorizontalRoute u v)),
          1 ≤ w.gk5aoHorizontalUnitCount) := by
  constructor
  · rfl
  · intro w
    exact nativeGK5AOHorizontalUnit_requires_primitive u v w

#print axioms NativeF55P92AssocComparison.gk5aoRouteActionFlag
#print axioms NativeF55P92AssocComparison.gk5aoTrans_flag
#print axioms NativeF55P92AssocComparison.gk5aoHorizontal_flag
#print axioms NativeF55P93AssocFourCell.gk5aoRouteActionFlag_sound
#print axioms nativeGK5AOP93HorizontalUnit_noFourCell
#print axioms NativeF55P94UnitFourCell.gk5aoHorizontalUnitCount
#print axioms NativeF55P94UnitFourCell.gk5aoZeroHorizontal_sound
#print axioms nativeGK5AOHorizontalUnit_requires_primitive
#print axioms nativeGK5AOHorizontalUnit_minimal_count

end
end Kuu.F112.Physical
