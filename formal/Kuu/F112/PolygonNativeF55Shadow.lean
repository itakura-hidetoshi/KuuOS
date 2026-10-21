import Kuu.F112.PolygonNativeF55Presented

/-!
# F112-E7P3 / independent native F55 full charge and braided-phase shadow

E7P2 reconstructs the genuine Type-valued NINE-CONSTRUCTOR F55 raw
higher-cell presentation over E7O's ACTUAL double-Nat-depth F45 native
Blocks and AxisTrace source; the pentagon/square 3-generators have
concrete, distinct original C60 F54 path boundaries.

We independently DEFINE and VERIFY a fully source-recursive additive
graded observation in (Int × Int) × ZMod 2. The pentagon generator
gets ((1,0),0), while the genuine disjoint-square generator gets
((0,1),1). These values coincide NUMERICALLY with the historical
original F58/F59 generator decorations but DO NOT establish a typed
old-to-new source equivalence, an original braided Gray target
equivalence, or any historical Δ curvature transfer.

All nine constructors are interpreted; inversion, pasting, both
independent native contexts and pre/post route whiskerings respect
the genuine additive target. Horizontal 3-cell pasting is DERIVED
from existing raw constructors, not introduced as an exchange axiom.

We prove phase = second integer charge mod 2 by FULL INDUCTION on
every raw F55 3-cell and the nonlift ((0,1),0). That obstruction is
only the new independent source shadow obstruction, not the
historical original F55/F77 Δ obstruction.

No old KUOS, Gray, F51/F77 imports and no new axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Three separately retained native coordinates: signed pentagon
charge, signed exchange-square charge, and odd exchange ZMod2 phase. -/
abbrev KuuNativeF55Shadow := (Int × Int) × ZMod 2

/-- The FULL chosen independent native F55 interpretation, defined
by recursion on every one of the NINE original-shaped source
constructors. No equality of different raw 3-proofs is imposed. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nativeShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    KuuNativeF55Shadow :=
  match cell with
  | .ident _ => 0
  | .pentagon _ _ _ _ => (((1 : Int), (0 : Int)), (0 : ZMod 2))
  | .disjointSquare _ _ => (((0 : Int), (1 : Int)), (1 : ZMod 2))
  | .symm c => -c.nativeShadow
  | .trans c d => c.nativeShadow + d.nativeShadow
  | .leftContext c _ => c.nativeShadow
  | .rightContext _ c => c.nativeShadow
  | .precompose _ c => c.nativeShadow
  | .postcompose c _ => c.nativeShadow

/-- On the actual north C60 native F45 four-sector 3-vs-2
rotation paths, the pentagon source higher-cell has charge one in
the FIRST integer coordinate and zero independent exchange phase. -/
theorem northNativeF55PentagonCell_shadow :
    northNativeF55PentagonCell.nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

/-- On the ACTUAL top C60 hexagon six-sector disjoint F54 square
of two categorical Blocks contexts, the independent SOURCE
interpretation has nontrivial square charge and odd ZMod2 phase. -/
theorem northHexagonNativeF55SquareCell_shadow :
    northHexagonNativeF55SquareCell.nativeShadow =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := rfl

theorem northHexagonNativeF55SquareCell_phase_nonzero :
    northHexagonNativeF55SquareCell.nativeShadow.2 ≠
      (0 : ZMod 2) := by
  decide

/-- A COMPLETE constructor-by-constructor proof that the chosen
native phase is exactly the parity of the SECOND signed generator
charge, for arbitrary raw pentagon/square pasting and all contexts.
No free phase cancellation or old F55 originality is assumed. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.phase_squareParity
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    ((cell.nativeShadow.1.2 : Int) : ZMod 2) =
      cell.nativeShadow.2 := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change ((-c.nativeShadow.1.2 : Int) : ZMod 2) =
        -c.nativeShadow.2
      simpa using congrArg (fun z : ZMod 2 => -z) ih
  | trans c d ihc ihd =>
      change ((c.nativeShadow.1.2 + d.nativeShadow.1.2 : Int) :
        ZMod 2) = c.nativeShadow.2 + d.nativeShadow.2
      simpa using congrArg₂ (fun z w : ZMod 2 => z + w) ihc ihd
  | leftContext c w ih => exact ih
  | rightContext w c ih => exact ih
  | precompose w c ih => exact ih
  | postcompose c w ih => exact ih

/-- The new native F55 source cannot present signed square charge
ONE together with zero phase in THIS chosen independent receiver.
This statement does NOT identify the frozen original F55 Δ obstruction. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.no_shadow_delta
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    cell.nativeShadow ≠
      (((0 : Int), (1 : Int)), (0 : ZMod 2)) := by
  intro h
  have hs := congrArg (fun z : KuuNativeF55Shadow => z.1.2) h
  have hp := congrArg (fun z : KuuNativeF55Shadow => z.2) h
  change cell.nativeShadow.1.2 = (1 : Int) at hs
  change cell.nativeShadow.2 = (0 : ZMod 2) at hp
  have hpar := cell.phase_squareParity
  rw [hs, hp] at hpar
  exact (by decide : (1 : ZMod 2) ≠ 0) hpar

/-- The REAL original-shaped horizontal 3-cell pasting is DERIVED
from left/right contexts and the two pre/post path pastings of the
nine-constructor raw source; it is NOT a freely assumed interchange. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal
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
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      (.trans (.leftContext u rightBefore) (.rightContext leftAfter v))
      (.trans (.leftContext u' rightBefore) (.rightContext leftAfter v')) :=
  .trans
    (.postcompose (.leftContext f rightBefore)
      (.rightContext leftAfter v))
    (.precompose (.leftContext u' rightBefore)
      (.rightContext leftAfter g))

/-- Derived horizontal composition preserves both signed generator
charges and nonzero ZMod2 phase EXACTLY, not just mod-2 total count. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow
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
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    (f.horizontal g).nativeShadow =
      f.nativeShadow + g.nativeShadow := by
  rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nativeShadow
#print axioms northNativeF55PentagonCell_shadow
#print axioms northHexagonNativeF55SquareCell_shadow
#print axioms northHexagonNativeF55SquareCell_phase_nonzero
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.phase_squareParity
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.no_shadow_delta
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow
end
end Kuu.F112.Physical
