import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AZShearFreeProduct
import Mathlib.GroupTheory.CoprodI
import Mathlib.Tactic

/-!
F112-P94D3GK4BA — original dependent F54 histories carry a genuine
two-cyclic-factor free-product word. This is a SOURCE construction,
not an assumption of any new Type-valued comparison 3-cell.

The first factor represents the original double-Nat cast C and actual
forward LocalRotation F=C^{-1}. The second factor represents the
actual original backward LocalRotation R(X). Composition preserves
the noncommutative order; all original F54 typed constructors
(chain/refl/snoc/castDepths/trans/leftContext/rightContext) are handled.

The object is the *free product of groups*, not a synthetic F54
replacement. We neither impose nor infer original source equality
from equality of these words, and make no assertion that Q is a
category or the polynomial family descends through existing K_AI.

Append-only, tighten-only, root107 unchanged. No Gray.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/OPEN/unmerged.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- Exactly the two independent infinite-cyclic factors used by GK4AZ. -/
abbrev NativeGK4BAWord :=
  Monoid.CoprodI (fun _ : Bool => Multiplicative Int)

/-- Source double-Nat cast is positive first cyclic generator. -/
def nativeGK4BAWordCast : NativeGK4BAWord :=
  Monoid.CoprodI.of (i := false) (Multiplicative.ofAdd (1 : Int))

/-- Source physical forward rotation is its NEGATIVE first generator. -/
def nativeGK4BAWordForward : NativeGK4BAWord :=
  Monoid.CoprodI.of (i := false) (Multiplicative.ofAdd (-1 : Int))

/-- Source physical backward rotation is positive second generator. -/
def nativeGK4BAWordBackward : NativeGK4BAWord :=
  Monoid.CoprodI.of (i := true) (Multiplicative.ofAdd (1 : Int))

/-- A unit is a word-unit, but not a claim about equality of F54
Type-valued proof objects. -/
def nativeGK4BAWordOne : NativeGK4BAWord := 1

section OriginalDependentWord
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

def KuuNativeF45Tree.RotationEdge.gk4baWord
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) : NativeGK4BAWord :=
  match edge with
  | .forward _ => nativeGK4BAWordForward
  | .backward _ => nativeGK4BAWordBackward

def KuuNativeF45Tree.RotationChain.gk4baWord
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4BAWord
  | .refl _ => nativeGK4BAWordOne
  | .snoc path edge => path.gk4baWord * edge.gk4baWord

/-- A full original F54 dependent route, including both Nat depths
and actual source/target F45 tree objects. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4baWord
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGK4BAWord := by
  induction route with
  | chain path => exact path.gk4baWord
  | castDepths _ _ _ => exact nativeGK4BAWordCast
  | trans _ _ ihU ihV => exact ihU * ihV
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4BAWord_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4baWord =
      u.gk4baWord * v.gk4baWord := rfl

@[simp] theorem nativeGK4BAWord_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4baWord =
      route.gk4baWord := rfl

@[simp] theorem nativeGK4BAWord_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4baWord =
      route.gk4baWord := rfl

end OriginalDependentWord

/-- The ACTION ON INTEGER VECTORS is precisely the already verified
GK4AZ faithful free-product action, not a separate unproved model. -/
def nativeGK4BAIntegerWordAction (w : NativeGK4BAWord) (z : Int × Int) :
    Int × Int :=
  (Monoid.CoprodI.lift nativeGK4AZFactors w) z

theorem nativeGK4BAIntegerWordAction_mul
    (w v : NativeGK4BAWord) (z : Int × Int) :
    nativeGK4BAIntegerWordAction (w * v) z =
      nativeGK4BAIntegerWordAction w
        (nativeGK4BAIntegerWordAction v z) := by
  simp only [nativeGK4BAIntegerWordAction, map_mul]
  rfl

/-- The existing exact GK4AZ theorem directly makes our indexed
original source words distinguishable by their integer actions.
This is NOT a claim of injectivity from original Type-valued paths. -/
theorem nativeGK4BAIntegerWordAction_injective
    (u v : NativeGK4BAWord)
    (h : ∀ z : Int × Int, nativeGK4BAIntegerWordAction u z =
      nativeGK4BAIntegerWordAction v z) : u = v := by
  apply nativeGK4AZFreeProduct_injective
  apply Equiv.ext
  intro z
  exact h z

#print axioms NativeGK4BAWord
#print axioms nativeGK4BAWordCast
#print axioms nativeGK4BAWordForward
#print axioms nativeGK4BAWordBackward
#print axioms nativeGK4BAWordOne
#print axioms KuuNativeF45Tree.RotationEdge.gk4baWord
#print axioms KuuNativeF45Tree.RotationChain.gk4baWord
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4baWord
#print axioms nativeGK4BAWord_trans
#print axioms nativeGK4BAWord_leftContext
#print axioms nativeGK4BAWord_rightContext
#print axioms nativeGK4BAIntegerWordAction
#print axioms nativeGK4BAIntegerWordAction_mul
#print axioms nativeGK4BAIntegerWordAction_injective

end
end Kuu.F112.Physical
