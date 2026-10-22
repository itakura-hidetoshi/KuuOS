import Kuu.F112.PolygonNativeF55GradedTransportCoherenceP75
import Kuu.F112.PolygonNativeF55RawVerticalNormalizationP59
import Mathlib.Tactic.Abel

/-!
# F112-P76 — actual square-only bridge/transport compatibility

P70's chosen F55 representative transport and bridge composition are
operations on ACTUAL Type-valued raw proof cells. P75 adds a Type-valued
graded transport history but only establishes coherence of its three
selected shadow coordinates, not raw 4-dimensional equations.

Here we first vertically compose ORIGINAL square-only F55 comparison
witnesses, preserving the real raw proof syntax. We prove coherent
two-stage representative transport at BOTH the original full F55
shadow and the strictly normalized free-path levels. This does NOT
claim the two raw proof histories are equal.

Next compare two legitimate constructions of the same outer higher-Hom
endpoints:
  A. Compose two raw F55 higher arrows along an old chosen bridge, then
     transport their outer representatives.
  B. Transport each higher arrow (also at its internal endpoints),
     then compose along a NEW chosen middle bridge.
Their exact original full-shadow defect is
  rightF + newBridge + leftG - oldBridge.
Thus graded readout equality follows only with the EXPLICIT
bridge compatibility equation. A stronger, separately specified
equation between the actual NORMALIZED bridge proof paths yields
equality between the two normalized full composites.

Finally the GENUINE north C60 square and the original raw term
"identity; square" have equal normalized paths and equal full
shadows, but distinct original F55 proof trees. This is a concrete
obstruction to confusing a path-coherence theorem with raw strict
interchange. No Gray, sorry, admit, new axiom or deleted legacy roots.
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

/-- Compose TWO real square-only comparisons in their original
Type-valued F55 syntax, not merely by quotient equality or grade. -/
def NativeF55SquareOnlyCell.vcomp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell (p := p) (u := u) (v := v))
    (right : NativeF55SquareOnlyCell (p := p) (u := v) (v := w)) :
    NativeF55SquareOnlyCell (p := p) (u := u) (v := w) :=
  ⟨.trans left.1 right.1, by
    simp only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.squareOnly,
      left.2, right.2]
    rfl⟩

/-- Genuine source comparison proof-tree concatenation adds its
full chosen F55 shadow (both integer charges and odd parity). -/
theorem NativeF55SquareOnlyCell.vcomp_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell (p := p) (u := u) (v := v))
    (right : NativeF55SquareOnlyCell (p := p) (u := v) (v := w)) :
    (left.vcomp right).1.nativeShadow =
      left.1.nativeShadow + right.1.nativeShadow := rfl

/-- Its STRICT path normalization is a genuine composition of
actual proof-labelled free path edges. -/
theorem NativeF55SquareOnlyCell.vcomp_path
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell (p := p) (u := u) (v := v))
    (right : NativeF55SquareOnlyCell (p := p) (u := v) (v := w)) :
    (left.vcomp right).1.toNativeStrictPath =
      left.1.toNativeStrictPath.comp right.1.toNativeStrictPath := rfl

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Two sequential ACTUAL representative transports normalize to
the one-step transport using the VERTICALLY COMPOSED original
square-only proofs. Equality is only in the honest free path model. -/
theorem NativeF55HigherArrowOverClasses.transport_twice_path
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {u₁ v₁ u₂ v₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left₁ : NativeF55SquareOnlyCell
      (p := p) (u := u₁) (v := arrow.before))
    (right₁ : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := v₁))
    (left₂ : NativeF55SquareOnlyCell (p := p) (u := u₂) (v := u₁))
    (right₂ : NativeF55SquareOnlyCell (p := p) (u := v₁) (v := v₂)) :
    ((arrow.changeRepresentatives left₁ right₁).changeRepresentatives
      left₂ right₂).raw.toNativeStrictPath =
      (arrow.changeRepresentatives (left₂.vcomp left₁)
        (right₁.vcomp right₂)).raw.toNativeStrictPath := by
  change
    left₂.1.toNativeStrictPath.comp
      ((left₁.1.toNativeStrictPath.comp
        (arrow.raw.toNativeStrictPath.comp right₁.1.toNativeStrictPath)).comp
          right₂.1.toNativeStrictPath) =
    (left₂.1.toNativeStrictPath.comp left₁.1.toNativeStrictPath).comp
      (arrow.raw.toNativeStrictPath.comp
        (right₁.1.toNativeStrictPath.comp right₂.1.toNativeStrictPath))
  simp only [Quiver.Path.comp_assoc]

/-- Two-stage and composed single-stage representative transports
have EXACTLY the same full selected F55 shadow. This is a direct
theorem about actual raw proof terms, NOT equality of those terms. -/
theorem NativeF55HigherArrowOverClasses.transport_twice_shadow
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {u₁ v₁ u₂ v₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left₁ : NativeF55SquareOnlyCell
      (p := p) (u := u₁) (v := arrow.before))
    (right₁ : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := v₁))
    (left₂ : NativeF55SquareOnlyCell (p := p) (u := u₂) (v := u₁))
    (right₂ : NativeF55SquareOnlyCell (p := p) (u := v₁) (v := v₂)) :
    ((arrow.changeRepresentatives left₁ right₁).changeRepresentatives
      left₂ right₂).raw.nativeShadow =
      (arrow.changeRepresentatives (left₂.vcomp left₁)
        (right₁.vcomp right₂)).raw.nativeShadow := by
  have h :
      left₂.1.nativeShadow +
        (left₁.1.nativeShadow +
          (arrow.raw.nativeShadow +
            (right₁.1.nativeShadow + right₂.1.nativeShadow))) =
      left₁.1.nativeShadow +
        (arrow.raw.nativeShadow +
          (right₁.1.nativeShadow +
            (left₂.1.nativeShadow + right₂.1.nativeShadow))) := by
    calc
    left₂.1.nativeShadow +
        (left₁.1.nativeShadow +
          (arrow.raw.nativeShadow +
            (right₁.1.nativeShadow + right₂.1.nativeShadow))) =
      left₁.1.nativeShadow +
        (left₂.1.nativeShadow +
          (arrow.raw.nativeShadow +
            (right₁.1.nativeShadow + right₂.1.nativeShadow))) :=
      add_left_comm _ _ _
    _ = left₁.1.nativeShadow +
        (arrow.raw.nativeShadow +
          (left₂.1.nativeShadow +
            (right₁.1.nativeShadow + right₂.1.nativeShadow))) :=
      congrArg (fun z : KuuNativeF55Shadow => left₁.1.nativeShadow + z)
        (add_left_comm _ _ _)
    _ = left₁.1.nativeShadow +
        (arrow.raw.nativeShadow +
          (right₁.1.nativeShadow +
            (left₂.1.nativeShadow + right₂.1.nativeShadow))) :=
      congrArg (fun z : KuuNativeF55Shadow =>
        left₁.1.nativeShadow + (arrow.raw.nativeShadow + z))
        (add_left_comm _ _ _)
  first
  | simpa only [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow,
      NativeF55SquareOnlyCell.vcomp_shadow, add_assoc] using h
  | simpa only [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow,
      NativeF55SquareOnlyCell.vcomp_shadow, add_assoc] using h.symm

/-- Additive cancellation for the genuine full F55 shadow group,
with the old bridge term retained and canceled explicitly. -/
private theorem nativeF55_bridge_group_cancel
    (a b c h : KuuNativeF55Shadow) :
    a + (b + c) = a + (h + (c + (b - h))) := by
  rw [sub_eq_add_neg]
  calc
    a + (b + c) = a + ((h + -h) + (b + c)) := by simp
    _ = a + (h + (-h + (b + c))) := by simp only [add_assoc] <;> rfl
    _ = a + (h + ((b + c) + -h)) := by
      rw [add_comm (-h) (b + c)]
    _ = a + (h + ((c + b) + -h)) := by
      rw [add_comm b c]
    _ = a + (h + (c + (b + -h))) := by simp only [add_assoc] <;> rfl

/-- EXACT full selected-shadow DEFECT of the two ways of
transporting a genuine P70 bridge composite. It records all four
original square-only witnesses and the chosen old/new bridge.
No source F55 4-cell, or equality between raw proof histories, is
invented by this numerical identity. -/
theorem NativeF55HigherArrowOverClasses.bridgeTransport_shadow_defect
    {source middle target : NativeF55ContextSquareRouteClasses first last}
    (f : NativeF55HigherArrowOverClasses first last source middle)
    (g : NativeF55HigherArrowOverClasses first last middle target)
    (oldBridge : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := g.before))
    {outerBefore outerAfter midLeft midRight :
      KuuNativeF45Tree.DepthRotationRoute p first last}
    (outerLeft : NativeF55SquareOnlyCell
      (p := p) (u := outerBefore) (v := f.before))
    (outerRight : NativeF55SquareOnlyCell
      (p := p) (u := g.after) (v := outerAfter))
    (rightF : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := midLeft))
    (leftG : NativeF55SquareOnlyCell
      (p := p) (u := midRight) (v := g.before))
    (newBridge : NativeF55SquareOnlyCell
      (p := p) (u := midLeft) (v := midRight)) :
    ((f.changeRepresentatives outerLeft rightF).composeWithBridge
      (g.changeRepresentatives leftG outerRight) newBridge).raw.nativeShadow =
      ((f.composeWithBridge g oldBridge).changeRepresentatives
        outerLeft outerRight).raw.nativeShadow +
          (rightF.1.nativeShadow +
            (newBridge.1.nativeShadow + leftG.1.nativeShadow) -
              oldBridge.1.nativeShadow) := by
  simp only [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow,
    NativeF55HigherArrowOverClasses.composeWithBridge_shadow]
  calc
    _ = (outerLeft.1.nativeShadow + f.raw.nativeShadow) +
      ((rightF.1.nativeShadow +
        (newBridge.1.nativeShadow + leftG.1.nativeShadow)) +
          (g.raw.nativeShadow + outerRight.1.nativeShadow)) := by
      simp only [add_assoc] <;> rfl
    _ = (outerLeft.1.nativeShadow + f.raw.nativeShadow) +
      (oldBridge.1.nativeShadow +
        ((g.raw.nativeShadow + outerRight.1.nativeShadow) +
          ((rightF.1.nativeShadow +
            (newBridge.1.nativeShadow + leftG.1.nativeShadow)) -
              oldBridge.1.nativeShadow))) :=
      nativeF55_bridge_group_cancel _ _ _ _
    _ = _ := by simp only [add_assoc] <;> rfl

/-- If the newly chosen genuine middle square comparison WITNESSES
have the same full F55 shadow as the old bridge, the two complete
pasted higher arrows agree in shadow. A raw proof-term equality or
P71 transport equivalence does NOT follow from this equation. -/
theorem NativeF55HigherArrowOverClasses.bridgeTransport_shadow_of_compat
    {source middle target : NativeF55ContextSquareRouteClasses first last}
    (f : NativeF55HigherArrowOverClasses first last source middle)
    (g : NativeF55HigherArrowOverClasses first last middle target)
    (oldBridge : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := g.before))
    {outerBefore outerAfter midLeft midRight :
      KuuNativeF45Tree.DepthRotationRoute p first last}
    (outerLeft : NativeF55SquareOnlyCell
      (p := p) (u := outerBefore) (v := f.before))
    (outerRight : NativeF55SquareOnlyCell
      (p := p) (u := g.after) (v := outerAfter))
    (rightF : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := midLeft))
    (leftG : NativeF55SquareOnlyCell
      (p := p) (u := midRight) (v := g.before))
    (newBridge : NativeF55SquareOnlyCell
      (p := p) (u := midLeft) (v := midRight))
    (hBridge :
      rightF.1.nativeShadow +
        (newBridge.1.nativeShadow + leftG.1.nativeShadow) =
          oldBridge.1.nativeShadow) :
    ((f.changeRepresentatives outerLeft rightF).composeWithBridge
      (g.changeRepresentatives leftG outerRight) newBridge).raw.nativeShadow =
      ((f.composeWithBridge g oldBridge).changeRepresentatives
        outerLeft outerRight).raw.nativeShadow := by
  have h := f.bridgeTransport_shadow_defect g oldBridge
    outerLeft outerRight rightF leftG newBridge
  rw [hBridge, sub_self, add_zero] at h
  exact h

/-- A strictly stronger, explicitly GIVEN bridge PATH compatibility
witness proves interchange at the native free-path normalization
level. This is a conditional mathematical theorem: no equality
of distinct F55 proof histories is asserted or obtained. -/
theorem NativeF55HigherArrowOverClasses.bridgeTransport_path_of_compat
    {source middle target : NativeF55ContextSquareRouteClasses first last}
    (f : NativeF55HigherArrowOverClasses first last source middle)
    (g : NativeF55HigherArrowOverClasses first last middle target)
    (oldBridge : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := g.before))
    {outerBefore outerAfter midLeft midRight :
      KuuNativeF45Tree.DepthRotationRoute p first last}
    (outerLeft : NativeF55SquareOnlyCell
      (p := p) (u := outerBefore) (v := f.before))
    (outerRight : NativeF55SquareOnlyCell
      (p := p) (u := g.after) (v := outerAfter))
    (rightF : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := midLeft))
    (leftG : NativeF55SquareOnlyCell
      (p := p) (u := midRight) (v := g.before))
    (newBridge : NativeF55SquareOnlyCell
      (p := p) (u := midLeft) (v := midRight))
    (hBridge :
      oldBridge.1.toNativeStrictPath =
        rightF.1.toNativeStrictPath.comp
          (newBridge.1.toNativeStrictPath.comp
            leftG.1.toNativeStrictPath)) :
    ((f.changeRepresentatives outerLeft rightF).composeWithBridge
      (g.changeRepresentatives leftG outerRight) newBridge).raw.toNativeStrictPath =
      ((f.composeWithBridge g oldBridge).changeRepresentatives
        outerLeft outerRight).raw.toNativeStrictPath := by
  change
    (outerLeft.1.toNativeStrictPath.comp
      (f.raw.toNativeStrictPath.comp rightF.1.toNativeStrictPath)).comp
      (newBridge.1.toNativeStrictPath.comp
        (leftG.1.toNativeStrictPath.comp
          (g.raw.toNativeStrictPath.comp outerRight.1.toNativeStrictPath))) =
    outerLeft.1.toNativeStrictPath.comp
      ((f.raw.toNativeStrictPath.comp
        (oldBridge.1.toNativeStrictPath.comp g.raw.toNativeStrictPath)).comp
          outerRight.1.toNativeStrictPath)
  rw [hBridge]
  simp only [Quiver.Path.comp_assoc]

/-- The physical north C60 original disjoint square is DIFFERENT,
as a Type-valued source proof tree, from its unit-left-pasted
version. Hence path coherence is not raw 4-dimensional equality. -/
theorem northHexagonNativeF55Square_ne_leftUnit :
    northHexagonNativeF55SquareCell ≠
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
          northHexagonNativeSquareLeft)
        northHexagonNativeF55SquareCell) := by
  intro heq
  have hshape := congrArg
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag heq
  change (2 : Nat) = 4 at hshape
  exact (by decide : (2 : Nat) ≠ 4) hshape

/-- Nevertheless those two distinct genuine C60 F55 source
histories have EXACTLY equal normalized proof-labelled paths. -/
theorem northHexagonNativeF55Square_leftUnit_path :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northHexagonNativeSquareLeft)
      northHexagonNativeF55SquareCell).toNativeStrictPath =
        northHexagonNativeF55SquareCell.toNativeStrictPath :=
  northHexagonNativeF55SquareCell.toNativeStrictPath_leftUnit

/-- Both C60 raw terms also have the same full chosen F55 observer,
despite the certified raw inequality. This is not a raw proof-cell
or transport equivalence between them. -/
theorem northHexagonNativeF55Square_leftUnit_shadow :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        northHexagonNativeSquareLeft)
      northHexagonNativeF55SquareCell).nativeShadow =
        northHexagonNativeF55SquareCell.nativeShadow := by
  change (0 : KuuNativeF55Shadow) +
    northHexagonNativeF55SquareCell.nativeShadow =
      northHexagonNativeF55SquareCell.nativeShadow
  simp

#print axioms NativeF55SquareOnlyCell.vcomp
#print axioms NativeF55SquareOnlyCell.vcomp_shadow
#print axioms NativeF55SquareOnlyCell.vcomp_path
#print axioms NativeF55HigherArrowOverClasses.transport_twice_path
#print axioms NativeF55HigherArrowOverClasses.transport_twice_shadow
#print axioms NativeF55HigherArrowOverClasses.bridgeTransport_shadow_defect
#print axioms NativeF55HigherArrowOverClasses.bridgeTransport_shadow_of_compat
#print axioms NativeF55HigherArrowOverClasses.bridgeTransport_path_of_compat
#print axioms northHexagonNativeF55Square_ne_leftUnit
#print axioms northHexagonNativeF55Square_leftUnit_path
#print axioms northHexagonNativeF55Square_leftUnit_shadow

end
end Kuu.F112.Physical
