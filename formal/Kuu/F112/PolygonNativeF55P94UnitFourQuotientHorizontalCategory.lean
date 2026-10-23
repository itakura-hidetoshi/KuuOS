import Kuu.F112.PolygonNativeF55P94UnitFourCellPresentation
import Mathlib.Tactic

/-!
# F112-P94B — genuine P94A unit-four-quotient local horizontal unitality

P94A honestly adjoined three new source structural unit 4-generators
to a DISTINCT 4-cell presentation over ACTUAL P92B Type-valued 3-proofs.
All P93C four-cell evidence is included, with complete C60 odd phase
preserved and old P79 original path-sound no-go untouched.

Here construct, without numerical-shadow shortcuts:
  (1) full strict vertical Mathlib Category on original F54 routes
      with P94A four-proof classes as homs;
  (2) well-defined true two-sided F54 horizontal P92B four-classes;
  (3) strict four-class horizontal/vertical interchange;
  (4) honest horizontal preservation of BOTH identity 3-cells;
  (5) both original F45 left/right context operations and unit laws;
  (6) complete signed pentagon/square/odd-phase additive shadow,
      and compatibility with the old P93C four-quotient maps.

An actual north C60 six-sector instance records both new horizontal
unitality and the unchanged old P77 no-go: DIFFERENT presentations.
No proof of 4-dimensional associator pentagonator, full global strict
3/n-category or hyperdescent is asserted. No Gray or new logical axioms.
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

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55P92AssocComparison p u v}

def nativeF55P94VerticalComp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94UnitFourClasses first last u v)
    (g : NativeF55P94UnitFourClasses first last v w) :
    NativeF55P94UnitFourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P94UnitFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P94UnitFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P94UnitFourCell.rightWhisker witness right⟩)

/-- True local strict vertical Mathlib Category on ORIGINAL F54
route objects with P92B proof-relevant 3-homs modulo P93C 4-cells.
The unit/associator laws are witnesses in the NEW four-cell source. -/
@[reducible] def nativeF55P94VerticalCategory
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P94UnitFourClasses first last
  id route := nativeF55P94UnitFourClass first last (.refl route)
  comp f g := nativeF55P94VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94UnitFourClass first last (.trans (.refl X) raw) =
      nativeF55P94UnitFourClass first last raw
    exact Quot.sound ⟨NativeF55P94UnitFourCell.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P94UnitFourClass first last (.trans raw (.refl Y)) =
      nativeF55P94UnitFourClass first last raw
    exact Quot.sound ⟨NativeF55P94UnitFourCell.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P94UnitFourClass first last
        (.trans (.trans a b) c) =
      nativeF55P94UnitFourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P94UnitFourCell.verticalAssoc a b c⟩

/-- The new full shadow remains vertically additive on arbitrary
true P92B 4-class representatives. -/
theorem nativeF55P94VerticalShadow_comp
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P94UnitFourClasses first last r s)
    (g : NativeF55P94UnitFourClasses first last s t) :
    nativeF55P94UnitFourToShadow first last r t
      (nativeF55P94VerticalComp first last f g) =
    nativeF55P94UnitFourToShadow first last r s f +
      nativeF55P94UnitFourToShadow first last s t g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

def nativeF55P94Horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P94UnitFourClasses leftBefore leftAfter r r')
    (g : NativeF55P94UnitFourClasses rightBefore rightAfter s s') :
    NativeF55P94UnitFourClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (.trans (.leftContext r rightBefore) (.rightContext leftAfter s))
      (.trans (.leftContext r' rightBefore) (.rightContext leftAfter s')) :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P94UnitFourClass _ _ (left.horizontal right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨w⟩
      exact ⟨NativeF55P94UnitFourCell.horizontalRight left w⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨w⟩
      exact ⟨NativeF55P94UnitFourCell.horizontalLeft w right⟩)

/-- P92B×P92B→P93C binary operation computes on the SAME original
F54 route-typed NEW P92B 3-proofs, not a shadow replacement. -/
@[simp] theorem nativeF55P94Horizontal_raw
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p r r')
    (g : NativeF55P92AssocComparison p s s') :
    nativeF55P94Horizontal
      (nativeF55P94UnitFourClass leftBefore leftAfter f)
      (nativeF55P94UnitFourClass rightBefore rightAfter g) =
    nativeF55P94UnitFourClass _ _ (f.horizontal g) := rfl



/-- The complete signed F55 shadow of a two-sided horizontal
pasting computes additively on arbitrary NEW P94A quotient classes.
This is a preservation theorem, not proof of interchange. -/
theorem nativeF55P94Horizontal_shadow
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P94UnitFourClasses leftBefore leftAfter r r')
    (g : NativeF55P94UnitFourClasses rightBefore rightAfter s s') :
    nativeF55P94UnitFourToShadow _ _ _ _
      (nativeF55P94Horizontal f g) =
      nativeF55P94UnitFourToShadow _ _ _ _ f +
        nativeF55P94UnitFourToShadow _ _ _ _ g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Strict interchange for FOUR ARBITRARY typed P93C quotient classes:
horizontal preserves vertical pasting as equality in the SAME P94A
quotient. This is the strict bifunctoriality part of the local
higher structure, not yet the entire globular strict 3-category. -/
theorem nativeF55P94_interchange
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : NativeF55P94UnitFourClasses leftBefore leftAfter u₀ u₁)
    (f₂ : NativeF55P94UnitFourClasses leftBefore leftAfter u₁ u₂)
    (g₁ : NativeF55P94UnitFourClasses rightBefore rightAfter v₀ v₁)
    (g₂ : NativeF55P94UnitFourClasses rightBefore rightAfter v₁ v₂) :
    nativeF55P94Horizontal
      (nativeF55P94VerticalComp leftBefore leftAfter f₁ f₂)
      (nativeF55P94VerticalComp rightBefore rightAfter g₁ g₂) =
    nativeF55P94VerticalComp
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (nativeF55P94Horizontal f₁ g₁)
      (nativeF55P94Horizontal f₂ g₂) := by
  refine Quot.inductionOn f₁ (fun a => ?_)
  refine Quot.inductionOn f₂ (fun b => ?_)
  refine Quot.inductionOn g₁ (fun c => ?_)
  refine Quot.inductionOn g₂ (fun d => ?_)
  change nativeF55P94UnitFourClass _ _
      ((NativeF55P92AssocComparison.trans a b).horizontal
        (NativeF55P92AssocComparison.trans c d)) =
    nativeF55P94UnitFourClass _ _
      (NativeF55P92AssocComparison.trans
        (a.horizontal c) (b.horizontal d))
  exact Quot.sound ⟨NativeF55P94UnitFourCell.interchange a b c d⟩

/-- NEW four-class horizontal product maps actual identity
3-proofs to the genuine original F54 horizontal route's identity.
This is a quotient equality BY THE EXPLICIT P94A UNIT FOUR-CELL. -/
theorem nativeF55P94Horizontal_id
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last)
    (s : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55P94Horizontal
      (nativeF55P94UnitFourClass first last (.refl r))
      (nativeF55P94UnitFourClass rightBefore rightAfter (.refl s)) =
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (.refl (nativeF54P90HorizontalRoute r s)) :=
  nativeF55P94HorizontalUnit_new_class_eq r s

/-- Genuine F54 left tree context descends to the NEW P94A four-class
hom, with typed recursive P94A context evidence. -/
def nativeF55P94LeftContext
    {k l : Nat} {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (q : NativeF55P94UnitFourClasses first last r s) :
    NativeF55P94UnitFourClasses
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext r later) (.leftContext s later) :=
  Quot.liftOn q
    (fun raw => nativeF55P94UnitFourClass _ _ (.leftContext raw later))
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94UnitFourCell.leftContext w later⟩)

/-- Genuine F54 right binary context descends independently. -/
def nativeF55P94RightContext
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (fst : KuuNativeF45Tree p n m mb pb mc pc)
    (lst : KuuNativeF45Tree p n' m' mb pb mc pc)
    {r s : KuuNativeF45Tree.DepthRotationRoute p fst lst}
    (q : NativeF55P94UnitFourClasses fst lst r s) :
    NativeF55P94UnitFourClasses
      (KuuNativeF45Tree.node earlier fst)
      (KuuNativeF45Tree.node earlier lst)
      (.rightContext earlier r) (.rightContext earlier s) :=
  Quot.liftOn q
    (fun raw => nativeF55P94UnitFourClass _ _ (.rightContext earlier raw))
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeF55P94UnitFourCell.rightContext earlier w⟩)

/-- Left-context transport preserves true identity 3-cells
thanks to a chosen P94A source four-cell, never to a numeric charge. -/
theorem nativeF55P94LeftContext_id
    {k l : Nat} {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P94LeftContext later
      (nativeF55P94UnitFourClass first last (.refl r)) =
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.refl (.leftContext r later)) :=
  Quot.sound ⟨NativeF55P94UnitFourCell.leftContextUnit r later⟩

/-- Right-context transport also preserves true identity 3-cells,
using the independently typed new right-context unit witness. -/
theorem nativeF55P94RightContext_id
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (fst : KuuNativeF45Tree p n m mb pb mc pc)
    (lst : KuuNativeF45Tree p n' m' mb pb mc pc)
    (r : KuuNativeF45Tree.DepthRotationRoute p fst lst) :
    nativeF55P94RightContext earlier fst lst
      (nativeF55P94UnitFourClass fst lst (.refl r)) =
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.node earlier fst)
      (KuuNativeF45Tree.node earlier lst)
      (.refl (.rightContext earlier r)) :=
  Quot.sound ⟨NativeF55P94UnitFourCell.rightContextUnit earlier r⟩

/-- Original P93C four-proof embedding preserves genuine P92B
vertical pasting in the distinct NEW P94A quotient. -/
theorem nativeF55P94OldFour_toNew_comp
    (fst : KuuNativeF45Tree p n m ma pa mb pb)
    (lst : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : KuuNativeF45Tree.DepthRotationRoute p fst lst}
    (f : NativeF55P93AssocFourClasses fst lst r s)
    (g : NativeF55P93AssocFourClasses fst lst s t) :
    nativeF55P93ToP94UnitFour fst lst
      (nativeF55P93VerticalComp fst lst f g) =
    nativeF55P94VerticalComp fst lst
      (nativeF55P93ToP94UnitFour fst lst f)
      (nativeF55P93ToP94UnitFour fst lst g) := by
  refine Quot.inductionOn f (fun a => ?_)
  refine Quot.inductionOn g (fun b => ?_)
  rfl

/-- Original P93C shadow is faithfully retained by the new
P94A quotient map, including the C60 ZMod2 exchange phase. -/
theorem nativeF55P94OldFour_toNew_shadow
    (fst : KuuNativeF45Tree p n m ma pa mb pb)
    (lst : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p fst lst}
    (f : NativeF55P93AssocFourClasses fst lst r s) :
    nativeF55P94UnitFourToShadow fst lst r s
      (nativeF55P93ToP94UnitFour fst lst f) =
    nativeF55P93AssocFourToShadow fst lst r s f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- Original P93C horizontal pasting maps to genuine new
P94A horizontal pasting, because both use the same source P92B
Type-valued binary horizontal 3-cell, not a shadow proxy. -/
theorem nativeF55P94OldFour_toNew_horizontal
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p first last}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P93AssocFourClasses first last r r')
    (g : NativeF55P93AssocFourClasses rightBefore rightAfter s s') :
    nativeF55P93ToP94UnitFour _ _
      (nativeF55P93Horizontal f g) =
    nativeF55P94Horizontal
      (nativeF55P93ToP94UnitFour first last f)
      (nativeF55P93ToP94UnitFour rightBefore rightAfter g) := by
  refine Quot.inductionOn f (fun a => ?_)
  refine Quot.inductionOn g (fun b => ?_)
  rfl

/-- ACTUAL C60 six-sector horizontal identity is now valid in
the new P94A quotient but its original P77 strict path-sound
four-cell remains mathematically absent. Both statements hold. -/
theorem northHexagonNativeF55P94_horizontal_id_and_old_no_go :
    nativeF55P94Horizontal
      (nativeF55P94UnitFourClass _ _
        (NativeF55P92AssocComparison.refl northHexagonNativeLeftF54UnitRoute))
      (nativeF55P94UnitFourClass _ _
        (NativeF55P92AssocComparison.refl northHexagonNativeRightF54UnitRoute)) =
      nativeF55P94UnitFourClass _ _
        (NativeF55P92AssocComparison.refl
          (nativeF54P90HorizontalRoute
            northHexagonNativeLeftF54UnitRoute
            northHexagonNativeRightF54UnitRoute)) ∧
    ¬ Nonempty (NativeF55RawVerticalFourCell _ _
      northHexagonNativeHorizontalRawIdentityPair
      northHexagonNativeHorizontalStrictIdentity) := by
  constructor
  · exact nativeF55P94Horizontal_id
      northHexagonNativeLeftF54UnitRoute northHexagonNativeRightF54UnitRoute
  · exact northHexagonNativeHorizontalIdentity_noRawFourCell

#print axioms nativeF55P94VerticalComp
#print axioms nativeF55P94VerticalCategory
#print axioms nativeF55P94VerticalShadow_comp
#print axioms nativeF55P94Horizontal
#print axioms nativeF55P94Horizontal_raw
#print axioms nativeF55P94Horizontal_shadow
#print axioms nativeF55P94_interchange
#print axioms nativeF55P94Horizontal_id
#print axioms nativeF55P94LeftContext
#print axioms nativeF55P94RightContext
#print axioms nativeF55P94LeftContext_id
#print axioms nativeF55P94RightContext_id
#print axioms nativeF55P94OldFour_toNew_comp
#print axioms nativeF55P94OldFour_toNew_shadow
#print axioms nativeF55P94OldFour_toNew_horizontal
#print axioms northHexagonNativeF55P94_horizontal_id_and_old_no_go

end
end Kuu.F112.Physical
