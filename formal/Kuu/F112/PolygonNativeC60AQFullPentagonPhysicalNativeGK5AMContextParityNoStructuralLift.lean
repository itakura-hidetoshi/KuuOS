import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ALPrimitiveUnitObstruction
import Kuu.F112.PolygonNativeF55P93AssocQuotientHorizontalCoherence
import Mathlib.Tactic

/-!
F112-P94D3GK5AM — actual P93 structural non-descent of the
old P80 left/right context unit four-cell generators.

GK5AL proved that the complete original P87 and P89 structural
four-cell lift exists if and only if the three genuinely added P80
primitive unit families admit selected P93 four-cell images.
Here we exhibit a NEW finite, source-proof-sensitive ZMod 2
CONTEXT PARITY on the selected P92B three-cell presentation:
  - original F55 and new assocNaturality, identities -> 0;
  - left and right context constructor -> add 1 mod 2;
  - route whiskers -> unchanged, vertical composition -> add.

P92B horizontal pasting contains ONE left and ONE right context,
so context parity is additive modulo two. Every constructor of
P93's actual Type-valued four-cell presentation preserves it:
including inherited .old P89 four-cells, vertical units/assoc,
true F54 contexts/routes, both horizontal whiskers and
interchange. This is a NEW invariant separate from the existing
three-coordinate pentagon/square/odd-hexagon shadow.

The structural GK5AI image of an ORIGINAL P80 left-context-unit
generator has context parity 1 on its source, 0 on its target.
Likewise for the original P80 right-context-unit. Therefore
neither has any genuine selected P93 Type-valued four-cell:
the old P87 source unit is real, but it does NOT translate under
the structural phi into the existing selected P93 presentation.
The GK5AL obstruction implication now has an ACTUAL primitive
counterexample and hence no total structural P87/P89 lift
where a genuine typed context exists. We do NOT add imaginary
P93 unit certificates or conflate .original(f) with phi(f).

Keep the old P77/P80/P85/P86/P87/P89 Type-valued proof histories,
two Nat depth indices, full C60 shadow, strict 空 authority,
root107, append-only, and protected draft #1558.
No Gray, unrestricted higher filler/descent, sorry, native_decide,
or new axioms. Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Independently defined mod-2 count of selected P92B raw
left/right F54 context constructors, with original F55 and
the adjoined P92B associator naturality both counted as atoms. -/
def NativeF55P92AssocComparison.gk5amContextParity
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
  | rightContext earlier cell ih => exact ih + 1
  | precompose prior cell ih => exact ih
  | postcompose cell suffix ih => exact ih

/-- The TRUE selected P92B horizontal three-cell construction
adds context parity: its left and right context operations
cancel as 1+1=0 in ZMod2, with no proof history erased. -/
theorem NativeF55P92AssocComparison.gk5amHorizontal_contextParity
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
    (f.horizontal g).gk5amContextParity =
      f.gk5amContextParity + g.gk5amContextParity := by
  change (f.gk5amContextParity + 1) + (g.gk5amContextParity + 1) =
    f.gk5amContextParity + g.gk5amContextParity
  have htwo : (1 : ZMod 2) + 1 = 0 := by decide
  calc
    (f.gk5amContextParity + 1) + (g.gk5amContextParity + 1) =
        (f.gk5amContextParity + g.gk5amContextParity) + (1 + 1) := by abel
    _ = f.gk5amContextParity + g.gk5amContextParity := by simp [htwo]

/-- Definitional law for the actual P92B vertical 3-cell
constructor.  Keep this as a rewriting lemma rather than unfolding
the dependent primitive-recursion compiler inside P93 interchange. -/
theorem NativeF55P92AssocComparison.gk5amTrans_contextParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5amContextParity =
      f.gk5amContextParity + g.gk5amContextParity := rfl

/-- All SIXTEEN genuine selected P93 Type-valued four-cell rules
preserve context parity; this differs from numeric C60 shadow.
Most importantly the .old constructor compares two .original
sources and therefore does NOT give a comparison between
structurally recursive phi-images of original F55 cells. -/
theorem NativeF55P93AssocFourCell.gk5amContextParity_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5amContextParity = g.gk5amContextParity := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : ZMod 2) + f.gk5amContextParity = f.gk5amContextParity
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5amContextParity + (0 : ZMod 2) = f.gk5amContextParity
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5amContextParity + g.gk5amContextParity) +
        h.gk5amContextParity =
        f.gk5amContextParity + (g.gk5amContextParity + h.gk5amContextParity)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : ZMod 2 => prior.gk5amContextParity + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : ZMod 2 => z + suffix.gk5amContextParity) ih
  | leftContext w later ih =>
      exact congrArg (fun z : ZMod 2 => z + 1) ih
  | rightContext earlier w ih =>
      exact congrArg (fun z : ZMod 2 => z + 1) ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5amHorizontal_contextParity]
        using congrArg (fun z : ZMod 2 => z + other.gk5amContextParity) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5amHorizontal_contextParity]
        using congrArg (fun z : ZMod 2 => other.gk5amContextParity + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      -- Rewrite the two typed constructor laws independently.
      -- Unfolding the whole recursor here exposes opaque recursive
      -- terms to abel; it does not provide those constructor laws.
      simp only [NativeF55P92AssocComparison.gk5amHorizontal_contextParity,
        NativeF55P92AssocComparison.gk5amTrans_contextParity]
      abel

/-- ACTUAL counterexample, for EVERY correctly typed genuine
F54 pair: the original P80 left-context unit has no structural
image into the selected P93 four-cell presentation. -/
theorem nativeGK5AMLeftContextUnit_no_P93
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
          (.ident u) later))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.leftContext u later)))) := by
  rintro ⟨w⟩
  have h := w.gk5amContextParity_sound
  change (1 : ZMod 2) = 0 at h
  norm_num at h

/-- Symmetric ACTUAL obstruction for the genuinely original
P80 right-context unit, not inferred from shadow equality. -/
theorem nativeGK5AMRightContextUnit_no_P93
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
          earlier (.ident u)))
      (nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          (.rightContext earlier u)))) := by
  rintro ⟨w⟩
  have h := w.gk5amContextParity_sound
  change (1 : ZMod 2) = 0 at h
  norm_num at h

/-- The typed old P87 structural transport cannot exist globally
where any genuine original F54 left context exists, using the
actual source P80 primitive and its independently proven non-lift. -/
theorem nativeGK5AMP87_no_structural_lift_of_leftContext
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Nonempty (NativeGK5AKP87StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) :=
  nativeGK5ALP87_obstruction_of_primitive_missing
    (.leftContextUnit u later) (nativeGK5AMLeftContextUnit_no_P93 u later)

/-- Exact same concrete local non-lift obstructs every P89
thirteen-constructor structural lift. The P89 interchange
generator remains independently and unconditionally transportable. -/
theorem nativeGK5AMP89_no_structural_lift_of_leftContext
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Nonempty (NativeGK5AKP89StructuralBoundary
      (a := a) (b := b) (x := x) (y := y) p) :=
  nativeGK5ALP89_obstruction_of_primitive_missing
    (.leftContextUnit u later) (nativeGK5AMLeftContextUnit_no_P93 u later)

#print axioms NativeF55P92AssocComparison.gk5amContextParity
#print axioms NativeF55P92AssocComparison.gk5amHorizontal_contextParity
#print axioms NativeF55P93AssocFourCell.gk5amContextParity_sound
#print axioms nativeGK5AMLeftContextUnit_no_P93
#print axioms nativeGK5AMRightContextUnit_no_P93
#print axioms nativeGK5AMP87_no_structural_lift_of_leftContext
#print axioms nativeGK5AMP89_no_structural_lift_of_leftContext

end
end Kuu.F112.Physical
