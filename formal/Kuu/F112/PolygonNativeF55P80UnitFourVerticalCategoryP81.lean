import Kuu.F112.PolygonNativeF55P62RelativeUnitFourCellP80

/-!
# F112-P81 — genuine strict vertical category for the P62-relative P80 4-cell presentation

P79 proves a REAL no-go for the original P77 source 4-cell quotient:
original F55 horizontal composition fails to preserve the chosen
identity because its normalized proof path has length TWO rather than
ZERO. P80 addresses precisely that obstruction via a DIFFERENT,
explicit, proof-relevant presentation: preserve the original P77
4-cells, freely add source horizontal and both context unit
comparison constructors, and prove all certificates sound for P62's
independent syntax-generated unit-only path congruence.

We now equip EXACTLY the P80 source-witness quotient with a strict
LOCAL vertical Mathlib Category on the native F54 route objects.
Vertical composition descends by witnesses on BOTH input raw
representatives; vertical identity and associativity follow from
the ORIGINAL P77 raw unit/associator 4-cells embedded as actual
P80 Type-valued certificates. No observer equality is used to
construct any of these laws.

The original full native F55 (Int x Int) x ZMod 2 shadow still
factors and is exactly additive under the new vertical composition.
An explicit, representative-independent, surjective map carries
P77's old local 4-cell quotient to this DISTINCT P80 quotient,
commuting with identities, vertical composition and full shadow.

A genuinely physical C60 comparison shows this map is NOT
injective: the original north hexagon horizontal pair of raw
identity 3-proofs and its raw strict identity differ as P77
classes but coincide as P80 classes. Hence no readout from
the P80 quotient can equal the exact free P59 proof-labelled
path of EVERY original raw representative. This strengthens
the honesty boundary: P62-related paths, NOT P59 path equality,
are the correct observation layer for the new comparison data.

This proves ONE local strict VERTICAL category in a selected
presentation. Neither complete horizontal 3-composition nor
strict 3-interchange, global strict 3/n and hyperdescent is
claimed. The old P77 model and its P79 obstruction survive.
No Gray, new axioms, sorry, admit, or removed public roots.
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

/-- Two-sided SOURCE P80 four-cell witnesses make original
raw F55 vertical pasting compatible with the explicitly generated
P62-relative four-cell relation. -/
theorem nativeF55P80_comp_congr
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
    (hf : Nonempty (NativeF55P80UnitFourCell f f'))
    (hg : Nonempty (NativeF55P80UnitFourCell g g')) :
    Nonempty (NativeF55P80UnitFourCell
      (.trans f g) (.trans f' g')) := by
  rcases hf with ⟨wleft⟩
  rcases hg with ⟨wright⟩
  exact ⟨nativeF55P80UnitFour_comp_congr wleft wright⟩

/-- Well-defined total VERTICAL composition on exactly the
original P80 source-generated four-cell quotient. The two
quotient arguments are treated independently, each with genuine
Type-valued whiskered evidence of representative change. -/
def nativeF55P80VerticalComp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P80UnitFourClasses first last u v)
    (g : NativeF55P80UnitFourClasses first last v w) :
    NativeF55P80UnitFourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55P80UnitFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨NativeF55P80UnitFourCell.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨NativeF55P80UnitFourCell.rightWhisker witness right⟩)

/-- Original-shaped raw vertical pasting computes definitionally on
the P80 quotient of two actual source raw F55 3-proofs. -/
@[simp] theorem nativeF55P80VerticalComp_ofRaw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
    nativeF55P80VerticalComp first last
        (nativeF55P80UnitFourClass first last f)
        (nativeF55P80UnitFourClass first last g) =
      nativeF55P80UnitFourClass first last (.trans f g) := rfl

/-- Explicit and separately selected local CATEGORY with the P80
proof-relevant (not scalar-kernel) comparison classes as Homs.
No competing globally inferred Category instance is installed.
Original P77 associator/unit 4-cells provide the actual proofs. -/
@[reducible] def nativeF55P80VerticalCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55P80UnitFourClasses first last
  id route := nativeF55P80UnitFourClass first last (.ident route)
  comp f g := nativeF55P80VerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P80UnitFourClass first last (.trans (.ident X) raw) =
      nativeF55P80UnitFourClass first last raw
    exact Quot.sound ⟨NativeF55P80UnitFourCell.old
      (NativeF55RawVerticalFourCell.leftUnit raw)⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55P80UnitFourClass first last (.trans raw (.ident Y)) =
      nativeF55P80UnitFourClass first last raw
    exact Quot.sound ⟨NativeF55P80UnitFourCell.old
      (NativeF55RawVerticalFourCell.rightUnit raw)⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55P80UnitFourClass first last
        (.trans (.trans a b) c) =
      nativeF55P80UnitFourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55P80UnitFourCell.old
      (NativeF55RawVerticalFourCell.assoc a b c)⟩

/-- Full F55 chosen shadow survives the P80 VERTICAL composition
exactly, although the stronger P59 free-path equality does not
survive the horizontal-unit generator in the P80 relation. -/
theorem nativeF55P80VerticalShadow_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P80UnitFourClasses first last u v)
    (g : NativeF55P80UnitFourClasses first last v w) :
    nativeF55P80UnitFourToShadow first last u w
      (nativeF55P80VerticalComp first last f g) =
        nativeF55P80UnitFourToShadow first last u v f +
          nativeF55P80UnitFourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Raw F55 identities remain zero in ALL three full-shadow
coordinates after passage to the selected P80 comparison quotient. -/
theorem nativeF55P80VerticalShadow_id
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P80UnitFourToShadow first last u u
      (nativeF55P80UnitFourClass first last (.ident u)) =
        (0 : KuuNativeF55Shadow) := rfl

/-- Canonical map from the P77 source-generated VERTICAL 4-cell
quotient to the strictly enlarged P80 four-cell quotient. Every
old Type-valued source witness is visibly injected into P80
through the constructor NativeF55P80UnitFourCell.old.
This map does NOT claim to be injective. -/
def nativeF55P77ToP80
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v) :
    NativeF55P80UnitFourClasses first last u v :=
  Quot.liftOn f
    (fun raw => nativeF55P80UnitFourClass first last raw)
    (by
      intro left right h
      apply Quot.sound
      rcases h with ⟨witness⟩
      exact ⟨NativeF55P80UnitFourCell.old witness⟩)

/-- A represented original raw F55 proof maps to the class of the
SAME raw proof, without inspecting or changing its raw history. -/
@[simp] theorem nativeF55P77ToP80_ofRaw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P77ToP80 first last
      (nativeF55RawVerticalFourClass first last raw) =
      nativeF55P80UnitFourClass first last raw := rfl

/-- Every P80 quotient class comes from a P77 class, because
every P80 class has an ORIGINAL raw F55 3-cell representative.
This is surjectivity, not the false injectivity claim. -/
theorem nativeF55P77ToP80_surjective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Surjective
      (nativeF55P77ToP80 first last (u := u) (v := v)) := by
  intro g
  refine Quot.inductionOn g (fun raw => ?_)
  exact ⟨nativeF55RawVerticalFourClass first last raw, rfl⟩

/-- Canonical comparison preserves genuine source vertical pasting
from P77's original 4-cell quotient to P80's enlarged quotient. -/
theorem nativeF55P77ToP80_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v)
    (g : NativeF55RawVerticalFourClasses first last v w) :
    nativeF55P77ToP80 first last
      (nativeF55RawFourVerticalComp first last f g) =
    nativeF55P80VerticalComp first last
      (nativeF55P77ToP80 first last f)
      (nativeF55P77ToP80 first last g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Old-to-new vertical comparison preserves every originally
chosen signed integer charge and independent odd exchange phase. -/
theorem nativeF55P77ToP80_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v) :
    nativeF55P80UnitFourToShadow first last u v
      (nativeF55P77ToP80 first last f) =
    nativeF55RawVerticalFourToShadow first last u v f := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- THE PHYSICAL north C60 horizontal-identity counterexample:
the canonical map collapses two formerly DISTINCT original P77
classes. It is therefore not injective, with both unequal source
classes named explicitly (no fabricated numerical proxy). -/
theorem northHexagonNativeP77ToP80_notInjective :
    ¬ Function.Injective
      (nativeF55P77ToP80
        (u := nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute)
        (v := nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute) _ _) := by
  intro hinj
  apply northHexagonNativeHorizontalUnit_P77_class_ne
  apply hinj
  exact northHexagonNativeHorizontalUnit_P80_class_eq

/-- The P80 horizontal-unit generator also prevents an exact P59
proof-labelled free-path readout descending from ALL original
representatives. This is the P79 no-go transported to the
ACTUAL enlarged P80 source comparison quotient. The original
P62-relative path congruence and full shadow still descend. -/
theorem northHexagonNativeP80_noFreePathReadout :
    ¬ ∃ (readout :
      NativeF55P80UnitFourClasses _ _
        (nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute)
        (nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute) →
      Quiver.Path
        (⟨nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute⟩ :
          NativeF55RawRouteVertex _ _)
        (⟨nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute⟩ :
          NativeF55RawRouteVertex _ _)),
      ∀ raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell _
        (nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute)
        (nativeF55HorizontalUnitRoute
          northHexagonNativeLeftF54UnitRoute
          northHexagonNativeRightF54UnitRoute),
        readout (nativeF55P80UnitFourClass _ _ raw) =
          raw.toNativeStrictPath := by
  rintro ⟨readout, hread⟩
  have h :=
    congrArg readout northHexagonNativeHorizontalUnit_P80_class_eq
  have hPaths :
      northHexagonNativeHorizontalRawIdentityPair.toNativeStrictPath =
        northHexagonNativeHorizontalStrictIdentity.toNativeStrictPath := by
    exact (hread northHexagonNativeHorizontalRawIdentityPair).symm.trans
      (h.trans (hread northHexagonNativeHorizontalStrictIdentity))
  exact (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_not_normalized_unit
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute) hPaths

#print axioms nativeF55P80_comp_congr
#print axioms nativeF55P80VerticalComp
#print axioms nativeF55P80VerticalComp_ofRaw
#print axioms nativeF55P80VerticalCategory
#print axioms nativeF55P80VerticalShadow_comp
#print axioms nativeF55P80VerticalShadow_id
#print axioms nativeF55P77ToP80
#print axioms nativeF55P77ToP80_ofRaw
#print axioms nativeF55P77ToP80_surjective
#print axioms nativeF55P77ToP80_comp
#print axioms nativeF55P77ToP80_shadow
#print axioms northHexagonNativeP77ToP80_notInjective
#print axioms northHexagonNativeP80_noFreePathReadout

end
end Kuu.F112.Physical
