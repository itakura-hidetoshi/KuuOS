import Kuu.F112.PolygonNativeF55RawVerticalFourCellP77

/-!
# F112-P78 — strict local vertical category on genuine raw F55 4-cell classes

P77 constructs eight genuine Type-valued source vertical 4-cell
constructors between two parallel ORIGINAL F55 raw 3-proofs and
proves independent source path and chosen shadow soundness. P77's
quotient kernel is defined by the existence of an actual 4-cell,
NOT by observer equality or by normalized path equality.

Here both raw F55 3-proof inputs are quotiented ONLY by P77's
source-generated relation, and we prove genuine vertical composition
is well-defined with either chosen source representative. This uses
actual source 4-cell left/right whiskering, not numerical readouts.

Then we define an EXPLICIT Mathlib Category structure on the actual
native F54 route objects using that 4-cell quotient. Raw identity and
raw vertical trans supply id and composition; exact strict unit and
associativity laws follow from P77's actual source 4-cell generators.
The new category is a separately selected local presentation, not a
replacement of the existing globally registered shadow-kernel category.

The strictly normalized P59 free-path and full signed F55 observer
commute with both the new vertical composition and identities.
Finally the genuine C60 north disjoint square remains unequal to its
unit-left composite as ORIGINAL source raw proof terms, while their
images in this new, precisely specified 4-cell quotient are equal.

This proves local strict VERTICAL 3-Hom composition in one presentation.
It does NOT prove horizontal bifunctoriality, strict 3-interchange,
a global strict 3/n, (infinity,3)-hyperdescent or source 4-cell
coherence-of-coherences. No Gray, new axiom, sorry or admit.
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

/-- Both-sided source-witness congruence: the P77 inductive 4-cells,
not shadow equality, establish that any two chosen raw trans pastings
belong to the SAME precisely specified 4-cell class. -/
theorem nativeF55RawFour_comp_congr
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
    (hf : Nonempty (NativeF55RawVerticalFourCell first last f f'))
    (hg : Nonempty (NativeF55RawVerticalFourCell first last g g')) :
    Nonempty (NativeF55RawVerticalFourCell first last
      (.trans f g) (.trans f' g')) := by
  rcases hf with ⟨wleft⟩
  rcases hg with ⟨wright⟩
  exact ⟨.trans (.rightWhisker wleft g) (.leftWhisker f' wright)⟩

/-- Total vertical composition on SOURCE-generated raw 4-cell
quotients, with representative-independence following from
left/right actual 4-cell witnesses rather than from grades. -/
def nativeF55RawFourVerticalComp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v)
    (g : NativeF55RawVerticalFourClasses first last v w) :
    NativeF55RawVerticalFourClasses first last u w :=
  Quot.liftOn₂ f g
    (fun left right =>
      nativeF55RawVerticalFourClass first last (.trans left right))
    (by
      intro left right₁ right₂ hr
      apply Quot.sound
      rcases hr with ⟨witness⟩
      exact ⟨.leftWhisker left witness⟩)
    (by
      intro left₁ left₂ right hl
      apply Quot.sound
      rcases hl with ⟨witness⟩
      exact ⟨.rightWhisker witness right⟩)

/-- On any pair of explicit ORIGINAL F55 source terms this
new composition is exactly the class of their original raw paste. -/
@[simp] theorem nativeF55RawFourVerticalComp_ofRaw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
    nativeF55RawFourVerticalComp first last
        (nativeF55RawVerticalFourClass first last f)
        (nativeF55RawVerticalFourClass first last g) =
      nativeF55RawVerticalFourClass first last (.trans f g) := rfl

/-- A SECOND and distinct local CATEGORY on genuine F54 route
objects, with proof-generated P77 4-cell classes as Homs. The
Category structure is explicit instead of a global instance, so
the existing E7P4/P64 presentations retain their independent
authority and remain usable without typeclass ambiguity. -/
def nativeF55RawFourVerticalCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55RawVerticalFourClasses first last
  id route := nativeF55RawVerticalFourClass first last (.ident route)
  comp f g := nativeF55RawFourVerticalComp first last f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55RawVerticalFourClass first last (.trans (.ident X) raw) =
      nativeF55RawVerticalFourClass first last raw
    exact Quot.sound ⟨NativeF55RawVerticalFourCell.leftUnit raw⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeF55RawVerticalFourClass first last (.trans raw (.ident Y)) =
      nativeF55RawVerticalFourClass first last raw
    exact Quot.sound ⟨NativeF55RawVerticalFourCell.rightUnit raw⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    change nativeF55RawVerticalFourClass first last
        (.trans (.trans a b) c) =
      nativeF55RawVerticalFourClass first last
        (.trans a (.trans b c))
    exact Quot.sound ⟨NativeF55RawVerticalFourCell.assoc a b c⟩

/-- The strictly normalized P59 free-path readout respects actual
P78 vertical composition on ALL chosen quotient classes. -/
theorem nativeF55RawFourVerticalPath_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v)
    (g : NativeF55RawVerticalFourClasses first last v w) :
    nativeF55RawVerticalFourToPath first last u w
      (nativeF55RawFourVerticalComp first last f g) =
        (nativeF55RawVerticalFourToPath first last u v f).comp
          (nativeF55RawVerticalFourToPath first last v w g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- The full selected signed charges and ZMod 2 exchange phase are
ALSO additively preserved by the genuine source-derived quotient
vertical composition. This is a separate observer factorization. -/
theorem nativeF55RawFourVerticalShadow_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55RawVerticalFourClasses first last u v)
    (g : NativeF55RawVerticalFourClasses first last v w) :
    nativeF55RawVerticalFourToShadow first last u w
      (nativeF55RawFourVerticalComp first last f g) =
        nativeF55RawVerticalFourToShadow first last u v f +
          nativeF55RawVerticalFourToShadow first last v w g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- Genuine raw three-cell identities become strict normalized path
identity on this selected source-4-cell quotient. -/
theorem nativeF55RawFourVerticalPath_id
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55RawVerticalFourToPath first last u u
      (nativeF55RawVerticalFourClass first last (.ident u)) =
        (Quiver.Path.nil :
          Quiver.Path
            (⟨u⟩ : NativeF55RawRouteVertex first last) ⟨u⟩) := rfl

/-- The genuinely original C60 square and its raw left-unit paste
belong to ONE explicitly specified source 4-cell class even though
the two source proofs are originally syntactically distinct. -/
theorem northHexagonNativeSquare_fourClass_unit_eq :
    nativeF55RawVerticalFourClass _ _
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northHexagonNativeSquareLeft)
        northHexagonNativeF55SquareCell) =
      nativeF55RawVerticalFourClass _ _ northHexagonNativeF55SquareCell := by
  exact (nativeF55RawVerticalFourClass_eq_iff _ _ _ _).2
    ⟨.leftUnit northHexagonNativeF55SquareCell⟩

#print axioms nativeF55RawFour_comp_congr
#print axioms nativeF55RawFourVerticalComp
#print axioms nativeF55RawFourVerticalComp_ofRaw
#print axioms nativeF55RawFourVerticalCategory
#print axioms nativeF55RawFourVerticalPath_comp
#print axioms nativeF55RawFourVerticalShadow_comp
#print axioms nativeF55RawFourVerticalPath_id
#print axioms northHexagonNativeSquare_fourClass_unit_eq

end
end Kuu.F112.Physical
