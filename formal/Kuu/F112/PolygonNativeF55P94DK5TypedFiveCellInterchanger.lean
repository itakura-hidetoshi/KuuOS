import Kuu.F112.PolygonNativeF55P94DK5TypedHorizontalPeifferInterchange
import Mathlib.Tactic

/-!
# F112-P94D3Y — source-typed five-cell interchanger presentation

The D3X pair of genuinely typed four-cell horizontal pastings have
identical Peiffer images but are DISTINCT proof terms. It is unsound
to infer a five-cell from the Peiffer equality alone.

Here we freely ADJOIN, as an explicitly NEW Type-valued presentation,
an interchanger whose endpoints are those ACTUAL four-cell proof terms.
Reversal, vertical 5-cell pasting, four-cell vertical congruence,
unit/associativity/inversion five-cells and both three-cell
whiskerings are independently source typed. This new presentation
supports a strict LOCAL groupoid of genuine four-cell proofs modulo
five-cell evidence; none of its chosen generators is asserted to
have been derivable in the PREVIOUS P94D3V free grammar.

The new 5-dimensional witness is a chosen GENERATOR, not a theorem
of old P92B or a proof of unrestricted strict 3/n coherence.
No Gray, sorry, admit, new logical axioms, or changes to the
107 public roots, physical C60, or previous obstruction results.
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

/-- A genuinely Type-valued FREE five-cell evidence grammar
between original source-typed four-cell proof terms at EXACTLY
the same F54/3-cell boundaries. In particular, interchanger
is a NEW independent generator, not a consequence of equality
in the universal Peiffer quotient. -/
inductive NativeK5StructuralFiveCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s},
      NativeK5StructuralFourCell p f g →
      NativeK5StructuralFourCell p f g →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFiveCell p alpha alpha
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralFiveCell p beta alpha
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      (ab : NativeK5StructuralFiveCell p alpha beta)
      (bc : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5StructuralFiveCell p alpha gamma
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55StructuralComparison p r s}
      {alpha alpha' : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (beta : NativeK5StructuralFourCell p g h) :
      NativeK5StructuralFiveCell p (.trans alpha beta) (.trans alpha' beta)
  | verticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g)
      {beta beta' : NativeK5StructuralFourCell p g h}
      (w : NativeK5StructuralFiveCell p beta beta') :
      NativeK5StructuralFiveCell p (.trans alpha beta) (.trans alpha beta')
  | verticalAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h k : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g)
      (beta : NativeK5StructuralFourCell p g h)
      (gamma : NativeK5StructuralFourCell p h k) :
      NativeK5StructuralFiveCell p
        (.trans (.trans alpha beta) gamma)
        (.trans alpha (.trans beta gamma))
  | verticalLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFiveCell p (.trans (.refl f) alpha) alpha
  | verticalRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFiveCell p (.trans alpha (.refl g)) alpha
  | inverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFiveCell p
        (.trans alpha (.symm alpha)) (.refl f)
  | inverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (alpha : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFiveCell p
        (.trans (.symm alpha) alpha) (.refl g)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralFiveCell p (.symm alpha) (.symm beta)
  | interchanger
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      (alpha : NativeK5StructuralFourCell p f g)
      (beta : NativeK5StructuralFourCell p h k) :
      NativeK5StructuralFiveCell p
        (alpha.horizontalViaTarget beta)
        (alpha.horizontalViaSource beta)
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55StructuralComparison p r s)
      {f g : NativeF55StructuralComparison p s t}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralFiveCell p
        (.precompose prior alpha) (.precompose prior beta)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5StructuralFiveCell p
        (.postcompose alpha suffix) (.postcompose beta suffix)

/-- A free interchanger has the ACTUAL D3X four-term boundaries.
This is an EXPLICIT constructor of the new presentation. -/
def nativeK5TypedInterchanger
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha.horizontalViaSource beta) :=
  .interchanger alpha beta

/-- The new five-cell relation is proof relevant before truncation;
the Setoid truncates ONLY existence of chosen five-cell evidence,
never the equality of Peiffer images by itself. -/
def NativeK5StructuralFiveCell.setoid
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s} :
    Setoid (NativeK5StructuralFourCell p f g) where
  r := fun alpha beta => Nonempty (NativeK5StructuralFiveCell p alpha beta)
  iseqv := ⟨
    (fun alpha => ⟨.refl alpha⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- Genuine 4-cell proofs modulo ONLY the freely adjoined typed
5-cell grammar, not modulo a numerical/kernel equality test. -/
abbrev NativeK5FiveCellFourClasses
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : NativeF55StructuralComparison p r s) :=
  Quotient (NativeK5StructuralFiveCell.setoid (f := f) (g := g))

def nativeK5FiveCellFourClass
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5StructuralFourCell p f g) :
    NativeK5FiveCellFourClasses f g :=
  Quotient.mk _ alpha

/-- Vertical composition of ACTUAL 4-cell proof classes respects
both separate source-typed five-cell congruence operations. -/
def nativeK5FiveCellFourVerticalComp
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g h : NativeF55StructuralComparison p r s}
    (alpha : NativeK5FiveCellFourClasses f g)
    (beta : NativeK5FiveCellFourClasses g h) :
    NativeK5FiveCellFourClasses f h :=
  Quot.liftOn₂ alpha beta
    (fun a b => nativeK5FiveCellFourClass (.trans a b))
    (by
      intro a b b' h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeK5StructuralFiveCell.verticalRight a w⟩)
    (by
      intro a a' b h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeK5StructuralFiveCell.verticalLeft w b⟩)

/-- Four-cell reversal is compatible with EVERY five-cell generator
through the freely specified inversion-respect 5-constructor. -/
def nativeK5FiveCellFourInverse
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha : NativeK5FiveCellFourClasses f g) :
    NativeK5FiveCellFourClasses g f :=
  Quot.liftOn alpha
    (fun a => nativeK5FiveCellFourClass (.symm a))
    (by
      intro a b h
      rcases h with ⟨w⟩
      exact Quot.sound ⟨NativeK5StructuralFiveCell.inverseRespect w⟩)

/-- A strict LOCAL vertical groupoid of 3-cell terms with
four-cell morphisms modulo ACTUAL NEW 5-cell proof terms.
This is not a global strict 3/n category. -/
@[reducible] def nativeK5FiveCellFourVerticalGroupoid
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Groupoid (NativeF55StructuralComparison p r s) where
  Hom := fun f g => NativeK5FiveCellFourClasses f g
  id f := nativeK5FiveCellFourClass (.refl f)
  comp f g := nativeK5FiveCellFourVerticalComp f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeK5FiveCellFourClass (.trans (.refl X) raw) =
      nativeK5FiveCellFourClass raw
    exact Quot.sound ⟨NativeK5StructuralFiveCell.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeK5FiveCellFourClass (.trans raw (.refl Y)) =
      nativeK5FiveCellFourClass raw
    exact Quot.sound ⟨NativeK5StructuralFiveCell.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun alpha => ?_)
    refine Quot.inductionOn g (fun beta => ?_)
    refine Quot.inductionOn h (fun gamma => ?_)
    change nativeK5FiveCellFourClass (.trans (.trans alpha beta) gamma) =
      nativeK5FiveCellFourClass (.trans alpha (.trans beta gamma))
    exact Quot.sound ⟨NativeK5StructuralFiveCell.verticalAssoc alpha beta gamma⟩
  inv := fun {X Y} f => nativeK5FiveCellFourInverse f
  inv_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeK5FiveCellFourClass (.trans (.symm raw) raw) =
      nativeK5FiveCellFourClass (.refl Y)
    exact Quot.sound ⟨NativeK5StructuralFiveCell.inverseRight raw⟩
  comp_inv := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    change nativeK5FiveCellFourClass (.trans raw (.symm raw)) =
      nativeK5FiveCellFourClass (.refl X)
    exact Quot.sound ⟨NativeK5StructuralFiveCell.inverseLeft raw⟩

/-- The universal noncommutative Peiffer witness descends through
the chosen five-cell quotient. Because it depends on the common
3-cell endpoints, this is a NECESSARY check, not a completeness
or faithfulness theorem for the higher coherence presentation. -/
def nativeK5FiveCellFourToPeiffer
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s} :
    NativeK5FiveCellFourClasses f g →
      nativeK5UniversalPentagonatorKernel (D := D) (E := E) :=
  Quotient.lift
    (fun alpha : NativeK5StructuralFourCell p f g =>
      alpha.toUniversalPeifferRelator)
    (by
      intro alpha beta h
      apply Subtype.ext
      rfl)

#print axioms NativeK5StructuralFiveCell
#print axioms nativeK5TypedInterchanger
#print axioms NativeK5StructuralFiveCell.setoid
#print axioms NativeK5FiveCellFourClasses
#print axioms nativeK5FiveCellFourClass
#print axioms nativeK5FiveCellFourVerticalComp
#print axioms nativeK5FiveCellFourInverse
#print axioms nativeK5FiveCellFourVerticalGroupoid
#print axioms nativeK5FiveCellFourToPeiffer

end
end Kuu.F112.Physical
