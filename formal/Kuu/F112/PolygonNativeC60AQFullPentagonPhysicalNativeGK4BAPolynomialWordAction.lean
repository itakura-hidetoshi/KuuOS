import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolyShears
import Mathlib.Tactic

/-!
F112-P94D3GK4BA original F54 polynomial route action.
All true original Type-valued RotationEdge, RotationChain and
DepthRotationRoute constructors are retained in the induction below.
The polynomial cyclic group homs from PR #2842 and generator action
from PR #2841 are imported, NOT redeclared. Numeric equality
does not create source Type-valued 3-cells.
Append-only root107, Lean v4.30.0-rc2, pinned mathlib 5450b53...
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 100000
noncomputable section
universe uD vD uE vE

section OriginalF54PolyAction
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4BAPolyEdge_action
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction edge.gk4baWord z =
      nativeGK4BAPolyMatAction edge.gk4avPolynomial z := by
  cases edge with
  | forward _ => exact nativeGK4BAPolyWordAction_forward z
  | backward _ => exact nativeGK4BAPolyWordAction_backward z

theorem nativeGK4BAPolyChain_action
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction chain.gk4baWord z =
      nativeGK4BAPolyMatAction chain.gk4avPolynomial z := by
  induction chain generalizing z with
  | refl => exact nativeGK4BAPolyWordAction_unit z
  | snoc path edge ih =>
      change nativeGK4BAPolyWordAction (path.gk4baWord * edge.gk4baWord) z =
        nativeGK4BAPolyMatAction
          (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial) z
      calc
        _ = nativeGK4BAPolyWordAction path.gk4baWord
              (nativeGK4BAPolyWordAction edge.gk4baWord z) :=
            nativeGK4BAPolyWordAction_mul _ _ z
        _ = nativeGK4BAPolyWordAction path.gk4baWord
              (nativeGK4BAPolyMatAction edge.gk4avPolynomial z) := by
            rw [nativeGK4BAPolyEdge_action edge z]
        _ = nativeGK4BAPolyMatAction path.gk4avPolynomial
              (nativeGK4BAPolyMatAction edge.gk4avPolynomial z) := ih _
        _ = _ := (nativeGK4BAPolyMatAction_mul _ _ z).symm

theorem nativeGK4BAPolyRoute_action
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction route.gk4baWord z =
      nativeGK4BAPolyMatAction route.gk4avPolynomial z := by
  induction route generalizing z with
  | chain path => exact nativeGK4BAPolyChain_action path z
  | castDepths _ _ _ => exact nativeGK4BAPolyWordAction_cast z
  | trans u v ihu ihv =>
      change nativeGK4BAPolyWordAction (u.gk4baWord * v.gk4baWord) z =
        nativeGK4BAPolyMatAction
          (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial) z
      calc
        _ = nativeGK4BAPolyWordAction u.gk4baWord
              (nativeGK4BAPolyWordAction v.gk4baWord z) :=
            nativeGK4BAPolyWordAction_mul _ _ z
        _ = nativeGK4BAPolyWordAction u.gk4baWord
              (nativeGK4BAPolyMatAction v.gk4avPolynomial z) := by
            rw [ihv z]
        _ = nativeGK4BAPolyMatAction u.gk4avPolynomial
              (nativeGK4BAPolyMatAction v.gk4avPolynomial z) := ihu _
        _ = _ := (nativeGK4BAPolyMatAction_mul _ _ z).symm
  | leftContext _ _ ih => exact ih z
  | rightContext _ _ ih => exact ih z

/-- If two original dependent F54 histories have the SAME genuine
free-product word, their FULL polynomial matrix values agree.
No equality of original Type-valued paths is asserted. -/
theorem nativeGK4BAWord_eq_implies_polynomial
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last)
    (h : u.gk4baWord = v.gk4baWord) :
    u.gk4avPolynomial = v.gk4avPolynomial := by
  have h1 := congrArg
    (fun w : NativeGK4BAWord =>
      nativeGK4BAPolyWordAction w ((1 : Polynomial Int), 0)) h
  have h2 := congrArg
    (fun w : NativeGK4BAWord =>
      nativeGK4BAPolyWordAction w ((0 : Polynomial Int), 1)) h
  -- Lean4 keeps the congrArg application as an unreduced lambda
  -- application. Expose the exact observer applications before rewriting.
  change nativeGK4BAPolyWordAction u.gk4baWord
      ((1 : Polynomial Int), 0) =
    nativeGK4BAPolyWordAction v.gk4baWord
      ((1 : Polynomial Int), 0) at h1
  change nativeGK4BAPolyWordAction u.gk4baWord
      ((0 : Polynomial Int), 1) =
    nativeGK4BAPolyWordAction v.gk4baWord
      ((0 : Polynomial Int), 1) at h2
  rw [nativeGK4BAPolyRoute_action u, nativeGK4BAPolyRoute_action v] at h1 h2
  have h11 : u.gk4avPolynomial.1.1 = v.gk4avPolynomial.1.1 := by
    have ht := congrArg Prod.fst h1
    simpa [nativeGK4BAPolyMatAction] using ht
  have h21 : u.gk4avPolynomial.2.1 = v.gk4avPolynomial.2.1 := by
    have ht := congrArg Prod.snd h1
    simpa [nativeGK4BAPolyMatAction] using ht
  have h12 : u.gk4avPolynomial.1.2 = v.gk4avPolynomial.1.2 := by
    have ht := congrArg Prod.fst h2
    simpa [nativeGK4BAPolyMatAction] using ht
  have h22 : u.gk4avPolynomial.2.2 = v.gk4avPolynomial.2.2 := by
    have ht := congrArg Prod.snd h2
    simpa [nativeGK4BAPolyMatAction] using ht
  apply Prod.ext
  · exact Prod.ext h11 h12
  · exact Prod.ext h21 h22

end OriginalF54PolyAction

#print axioms nativeGK4BAPolyEdge_action
#print axioms nativeGK4BAPolyChain_action
#print axioms nativeGK4BAPolyRoute_action
#print axioms nativeGK4BAWord_eq_implies_polynomial

end
end Kuu.F112.Physical
