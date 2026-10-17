import Kuu.F112.PolygonNativeF55Shadow

/-!
# F112-E7P4 / exact full-shadow 3-Hom category of native F55 sources

E7P2 constructs the genuine nine-constructor F55-SHAPED free raw
three-cell syntax on ACTUAL independent native F45/F54 double-Nat
Blocks and AxisTrace routes, including the typed concrete north C60
pentagon and top C60 hexagon square source generators.

E7P3 proves a full chosen (Int × Int) × ZMod 2 interpretation and
phase-square-parity for EVERY raw source three-cell, deriving an
independent shadow nonlift. The raw proof terms are NOT declared equal.

We quotient ONLY parallel raw three-cells with identical FULL shadow
values, retaining both signed integers and the independent ZMod2
exchange phase. We prove exact well-definedness of vertical and
horizontal quotient composition, a Mathlib Category on the typed
original-shaped F54 route objects, and a faithful shadow evaluator.

Finally prove vertical/horizontal interchange INSIDE THIS PARTICULAR
commutative additive shadow-kernel quotient using the full observer.
This does NOT prove a general raw Gray/tricategory interchange nor
transport the historical original F55/F47/F68/F77 obstructions.

No old KUOS.*, Gray, F51, F77 imports; no new axioms/sorry/admit.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Two truly parallel original-shaped F55 raw 3-proofs are related
ONLY if all chosen native signed charges AND odd phase agree. -/
def nativeF55ShadowRel
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) : Prop :=
  f.nativeShadow = g.nativeShadow

/-- A deliberately exact full-shadow QUOTIENT higher Hom, distinct
from the FREE old-F55-shaped source grammar and independent of Gray. -/
abbrev NativeF55ThreeHom
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) : Type :=
  Quot (nativeF55ShadowRel (u := u) (v := v))

/-- No shadow coercion creates a new raw three-cell: every quotient
arrow is explicitly represented by an ACTUAL free raw source proof. -/
def nativeF55ThreeOf
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55ThreeHom u v :=
  Quot.mk _ f

/-- Read all three native coordinates on an ACTUAL higher arrow.
Well-definedness is exactly the explicit source quotient relation. -/
def nativeF55ThreeEval
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) : KuuNativeF55Shadow :=
  Quot.liftOn f (fun raw => raw.nativeShadow) (by
    intro left right h
    exact h)

@[simp] theorem nativeF55ThreeEval_of
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55ThreeEval (nativeF55ThreeOf f) = f.nativeShadow := rfl

/-- Original native F55 VERTICAL pasting, descending to the explicit
quotient via separate proofs of both representatives' congruence. -/
def nativeF55ThreeComp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v)
    (g : NativeF55ThreeHom v w) :
    NativeF55ThreeHom u w :=
  Quot.liftOn₂ f g
    (fun left right => nativeF55ThreeOf (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.nativeShadow + right₁.nativeShadow =
        left.nativeShadow + right₂.nativeShadow
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.nativeShadow + right.nativeShadow =
        left₂.nativeShadow + right.nativeShadow
      rw [heq])

theorem nativeF55ThreeEval_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v)
    (g : NativeF55ThreeHom v w) :
    nativeF55ThreeEval (nativeF55ThreeComp f g) =
      nativeF55ThreeEval f + nativeF55ThreeEval g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- A TRUE Mathlib Category on the ACTUAL new original-shaped
two-axis F54 raw depth-route source. Identities/associativity are
proved only AFTER the chosen full-shadow quotient and NOT on
different unquotiented raw F55 free 3-cell proof trees. -/
instance nativeF55ThreeCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Category (KuuNativeF45Tree.DepthRotationRoute p first last) where
  Hom := NativeF55ThreeHom
  id r := nativeF55ThreeOf (.ident r)
  comp f g := nativeF55ThreeComp f g
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : KuuNativeF55Shadow) + raw.nativeShadow =
      raw.nativeShadow
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.nativeShadow + (0 : KuuNativeF55Shadow) =
      raw.nativeShadow
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun left => ?_)
    refine Quot.inductionOn g (fun middle => ?_)
    refine Quot.inductionOn h (fun right => ?_)
    apply Quot.sound
    change (left.nativeShadow + middle.nativeShadow) +
      right.nativeShadow =
      left.nativeShadow + (middle.nativeShadow + right.nativeShadow)
    exact add_assoc _ _ _

/-- FAITHFUL exact native observation on the newly defined quotient:
the complete signed charge and exchange phase determine its 3-arrow.
No faithfulness of the original unquotiented F55/Gray source claimed. -/
theorem nativeF55ThreeEval_injective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55ThreeHom u v}
    (h : nativeF55ThreeEval f = nativeF55ThreeEval g) :
    f = g := by
  revert h
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right h => ?_)
  exact Quot.sound h

/-- Horizontal pasting of ACTUAL higher arrows uses the derived
NINE-CONSTRUCTOR horizontal source 3-cell and checks each independent
quotient representative; no new exchange generator is postulated. -/
def nativeF55ThreeHorizontal
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
    (f : NativeF55ThreeHom u u')
    (g : NativeF55ThreeHom v v') :
    NativeF55ThreeHom
      (.trans (.leftContext u rightBefore) (.rightContext leftAfter v))
      (.trans (.leftContext u' rightBefore) (.rightContext leftAfter v')) :=
  Quot.liftOn₂ f g
    (fun left right => nativeF55ThreeOf (left.horizontal right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.nativeShadow + right₁.nativeShadow =
        left.nativeShadow + right₂.nativeShadow
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.nativeShadow + right.nativeShadow =
        left₂.nativeShadow + right.nativeShadow
      rw [heq])

theorem nativeF55ThreeEval_horizontal
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
    (f : NativeF55ThreeHom u u')
    (g : NativeF55ThreeHom v v') :
    nativeF55ThreeEval (nativeF55ThreeHorizontal f g) =
      nativeF55ThreeEval f + nativeF55ThreeEval g := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  exact KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow
    left right

/-- VERTICAL/HORIZONTAL interchange in the EXACT chosen native
commutative full-shadow quotient, PROVED from full observer
injectivity and additive commutativity. Neither the FREE raw F55
presentation nor original Gray exchange is declared strict. -/
theorem nativeF55Three_horizontal_vertical_interchange
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55ThreeHom u₀ u₁)
    (f' : NativeF55ThreeHom u₁ u₂)
    (g : NativeF55ThreeHom v₀ v₁)
    (g' : NativeF55ThreeHom v₁ v₂) :
    nativeF55ThreeHorizontal
        (nativeF55ThreeComp f f')
        (nativeF55ThreeComp g g') =
      nativeF55ThreeComp
        (nativeF55ThreeHorizontal f g)
        (nativeF55ThreeHorizontal f' g') := by
  apply nativeF55ThreeEval_injective
  simp only [nativeF55ThreeEval_horizontal,
    nativeF55ThreeEval_comp]
  exact add_add_add_comm _ _ _ _

/-- The independent native shadow nonlift extends from all raw
F55 presented 3-proofs to ALL ARROWS of the fully typed chosen
quotient category. Historical original F55 Δ remains unmigrated. -/
theorem NativeF55ThreeHom.no_shadow_delta
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) :
    nativeF55ThreeEval f ≠
      (((0 : Int), (1 : Int)), (0 : ZMod 2)) := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.no_shadow_delta

/-- A NONTRIVIAL quotient 3-arrow on the actual top C60 hexagon
E7P1 disjoint native-F45 Blocks source routes. -/
def northHexagonNativeF55ThreeSquare :
    NativeF55ThreeHom
      northHexagonNativeSquareLeft northHexagonNativeSquareRight :=
  nativeF55ThreeOf northHexagonNativeF55SquareCell

theorem northHexagonNativeF55ThreeSquare_phase_nonzero :
    (nativeF55ThreeEval northHexagonNativeF55ThreeSquare).2 ≠
      (0 : ZMod 2) := by
  decide

/-- The actual north C60 original-shaped 3-vs-2 F54 pentagon route
also yields a correctly typed independent quotient 3-arrow. -/
def northNativeF55PentagonThreeHom :
    NativeF55ThreeHom
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  nativeF55ThreeOf northNativeF55PentagonCell

theorem northNativeF55PentagonThreeHom_firstCharge :
    (nativeF55ThreeEval northNativeF55PentagonThreeHom).1.1 =
      (1 : Int) := by
  rfl

#print axioms nativeF55ThreeComp
#print axioms nativeF55ThreeEval_comp
#print axioms nativeF55ThreeCategory
#print axioms nativeF55ThreeEval_injective
#print axioms nativeF55ThreeHorizontal
#print axioms nativeF55ThreeEval_horizontal
#print axioms nativeF55Three_horizontal_vertical_interchange
#print axioms NativeF55ThreeHom.no_shadow_delta
#print axioms northHexagonNativeF55ThreeSquare_phase_nonzero
#print axioms northNativeF55PentagonThreeHom_firstCharge
end
end Kuu.F112.Physical
