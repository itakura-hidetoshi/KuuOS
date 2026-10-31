import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolynomialWordAction
import Mathlib.Tactic

/-!
F112-P94D3GK4BA — exact rescaled INTEGER action of the SAME original
dependent F54 free-product word at t=4.

The action of the existing, GK4AZ-faithful free product permutation
on (2x,y) agrees with the rescaled original GK4AV polynomial
matrix evaluated at 4, for every genuine F54 rotation edge, chain,
original double-Nat cast, composition and both contexts.
The word action is additive on Z². Its restriction to the even
horizontal sublattice uniquely determines the action everywhere.

This is proved from existing GK4AZ hom and GK4AV evaluations;
no abstract Sanov faithfulness assumption or new original Type-
valued comparison proof is introduced. Append-only/root107.
Lean 4.30.0-rc2 / pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect #1558 Draft/OPEN/unmerged. Copyright © 2026
Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 100000
-- Tight, local elaboration budget for precise Lean failure diagnostics.
noncomputable section
universe uD vD uE vE

def nativeGK4BAIntVec (M : NativeGK4AHMatrix) (x y : Int) : Int × Int :=
  (M.1.1 * x + M.1.2 * y, M.2.1 * x + M.2.2 * y)

/-- Integer coordinate change: original (x,y) becomes (2x,y). -/
def nativeGK4BARescaledVec (M : NativeGK4AHMatrix) (x y : Int) :
    Int × Int :=
  (2 * (nativeGK4BAIntVec M x y).1, (nativeGK4BAIntVec M x y).2)

theorem nativeGK4BARescaledVec_mul (A B : NativeGK4AHMatrix)
    (x y : Int) :
    nativeGK4BARescaledVec (nativeGK4AHMul A B) x y =
      nativeGK4BARescaledVec A (nativeGK4BAIntVec B x y).1
        (nativeGK4BAIntVec B x y).2 := by
  rcases A with ⟨⟨a, b⟩, ⟨c, d⟩⟩
  rcases B with ⟨⟨e, f⟩, ⟨g, h⟩⟩
  apply Prod.ext
  · change 2 * ((a*e+b*g)*x+(a*f+b*h)*y) =
        2 * (a*(e*x+f*y)+b*(g*x+h*y))
    ring
  · change (c*e+d*g)*x+(c*f+d*h)*y =
        c*(e*x+f*y)+d*(g*x+h*y)
    ring

theorem nativeGK4BAIntegerWordAction_one (z : Int × Int) :
    nativeGK4BAIntegerWordAction 1 z = z := by
  simp [nativeGK4BAIntegerWordAction]

theorem nativeGK4BAIntegerWordAction_cast (x y : Int) :
    nativeGK4BAIntegerWordAction nativeGK4BAWordCast (2*x,y) =
      nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVCast) x y := by
  simp only [nativeGK4BAIntegerWordAction, nativeGK4BAWordCast,
    Monoid.CoprodI.lift_of]
  change nativeGK4AYUpperShear 1 (2*x,y) =
    nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVCast) x y
  simp [nativeGK4AYUpperShear, nativeGK4BARescaledVec,
    nativeGK4BAIntVec, nativeGK4AVPolyEval, nativeGK4AVCast]
  <;> ring

theorem nativeGK4BAIntegerWordAction_forward (x y : Int) :
    nativeGK4BAIntegerWordAction nativeGK4BAWordForward (2*x,y) =
      nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVForward) x y := by
  simp only [nativeGK4BAIntegerWordAction, nativeGK4BAWordForward,
    Monoid.CoprodI.lift_of]
  change nativeGK4AYUpperShear (-1) (2*x,y) =
    nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVForward) x y
  simp [nativeGK4AYUpperShear, nativeGK4BARescaledVec,
    nativeGK4BAIntVec, nativeGK4AVPolyEval, nativeGK4AVForward]
  <;> ring

theorem nativeGK4BAIntegerWordAction_backward (x y : Int) :
    nativeGK4BAIntegerWordAction nativeGK4BAWordBackward (2*x,y) =
      nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVBackward) x y := by
  simp only [nativeGK4BAIntegerWordAction, nativeGK4BAWordBackward,
    Monoid.CoprodI.lift_of]
  change nativeGK4AYLowerShear 1 (2*x,y) =
    nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVBackward) x y
  simp [nativeGK4AYLowerShear, nativeGK4BARescaledVec,
    nativeGK4BAIntVec, nativeGK4AVPolyEval, nativeGK4AVBackward]
  <;> ring

theorem nativeGK4BAIntegerWordAction_unit (x y : Int) :
    nativeGK4BAIntegerWordAction nativeGK4BAWordOne (2*x,y) =
      nativeGK4BARescaledVec (nativeGK4AVPolyEval 4 nativeGK4AVOne) x y := by
  simp [nativeGK4BAWordOne, nativeGK4BAIntegerWordAction_one,
    nativeGK4BARescaledVec, nativeGK4BAIntVec,
    nativeGK4AVPolyEval, nativeGK4AVOne]

section ActualOriginalRoute
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4BAIntegerEdge_action
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after)
    (x y : Int) :
    nativeGK4BAIntegerWordAction edge.gk4baWord (2*x,y) =
      nativeGK4BARescaledVec
        (nativeGK4AVPolyEval 4 edge.gk4avPolynomial) x y := by
  cases edge with
  | forward _ => exact nativeGK4BAIntegerWordAction_forward x y
  | backward _ => exact nativeGK4BAIntegerWordAction_backward x y

theorem nativeGK4BAIntegerChain_action
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after)
    (x y : Int) :
    nativeGK4BAIntegerWordAction chain.gk4baWord (2*x,y) =
      nativeGK4BARescaledVec
        (nativeGK4AVPolyEval 4 chain.gk4avPolynomial) x y := by
  induction chain generalizing x y with
  | refl => exact nativeGK4BAIntegerWordAction_unit x y
  | snoc path edge ih =>
      change nativeGK4BAIntegerWordAction (path.gk4baWord * edge.gk4baWord)
        (2*x,y) =
        nativeGK4BARescaledVec
          (nativeGK4AVPolyEval 4
            (nativeGK4AVMul path.gk4avPolynomial edge.gk4avPolynomial)) x y
      let B := nativeGK4AVPolyEval 4 edge.gk4avPolynomial
      let A := nativeGK4AVPolyEval 4 path.gk4avPolynomial
      calc
        _ = nativeGK4BAIntegerWordAction path.gk4baWord
              (nativeGK4BAIntegerWordAction edge.gk4baWord (2*x,y)) :=
            nativeGK4BAIntegerWordAction_mul _ _ _
        _ = nativeGK4BAIntegerWordAction path.gk4baWord
              (nativeGK4BARescaledVec B x y) := by
            rw [nativeGK4BAIntegerEdge_action edge x y]
        _ = nativeGK4BAIntegerWordAction path.gk4baWord
              (2*(nativeGK4BAIntVec B x y).1,
                (nativeGK4BAIntVec B x y).2) := rfl
        _ = nativeGK4BARescaledVec A
              (nativeGK4BAIntVec B x y).1
              (nativeGK4BAIntVec B x y).2 := ih _ _
        _ = nativeGK4BARescaledVec (nativeGK4AHMul A B) x y :=
            (nativeGK4BARescaledVec_mul A B x y).symm
        _ = _ := by
            rw [nativeGK4AVPolyEval_mul]

theorem nativeGK4BAIntegerRoute_action
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (x y : Int) :
    nativeGK4BAIntegerWordAction route.gk4baWord (2*x,y) =
      nativeGK4BARescaledVec
        (nativeGK4AVPolyEval 4 route.gk4avPolynomial) x y := by
  induction route generalizing x y with
  | chain path => exact nativeGK4BAIntegerChain_action path x y
  | castDepths _ _ _ => exact nativeGK4BAIntegerWordAction_cast x y
  | trans u v ihu ihv =>
      change nativeGK4BAIntegerWordAction (u.gk4baWord * v.gk4baWord)
        (2*x,y) =
        nativeGK4BARescaledVec
          (nativeGK4AVPolyEval 4
            (nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial)) x y
      let B := nativeGK4AVPolyEval 4 v.gk4avPolynomial
      let A := nativeGK4AVPolyEval 4 u.gk4avPolynomial
      calc
        _ = nativeGK4BAIntegerWordAction u.gk4baWord
              (nativeGK4BAIntegerWordAction v.gk4baWord (2*x,y)) :=
            nativeGK4BAIntegerWordAction_mul _ _ _
        _ = nativeGK4BAIntegerWordAction u.gk4baWord
              (nativeGK4BARescaledVec B x y) := by
            rw [ihv x y]
        _ = nativeGK4BAIntegerWordAction u.gk4baWord
              (2*(nativeGK4BAIntVec B x y).1,
                (nativeGK4BAIntVec B x y).2) := rfl
        _ = nativeGK4BARescaledVec A
              (nativeGK4BAIntVec B x y).1
              (nativeGK4BAIntVec B x y).2 := ihu _ _
        _ = nativeGK4BARescaledVec (nativeGK4AHMul A B) x y :=
            (nativeGK4BARescaledVec_mul A B x y).symm
        _ = _ := by
            rw [nativeGK4AVPolyEval_mul]
  | leftContext _ _ ih => exact ih x y
  | rightContext _ _ ih => exact ih x y

end ActualOriginalRoute

/-- Vector addition, to establish that equality on the even first
coordinate sublattice determines these specific linear permutations. -/
def nativeGK4BAIntAdd (z t : Int × Int) : Int × Int :=
  (z.1 + t.1, z.2 + t.2)

theorem nativeGK4BAIntegerWordAction_add
    (w : NativeGK4BAWord) (z t : Int × Int) :
    nativeGK4BAIntegerWordAction w (nativeGK4BAIntAdd z t) =
      nativeGK4BAIntAdd
        (nativeGK4BAIntegerWordAction w z)
        (nativeGK4BAIntegerWordAction w t) := by
  induction w using Monoid.CoprodI.induction_on generalizing z t with
  | one =>
      simp [nativeGK4BAIntegerWordAction_one, nativeGK4BAIntAdd]
  | of i m =>
      simp only [nativeGK4BAIntegerWordAction, Monoid.CoprodI.lift_of]
      cases i with
      | false =>
          change nativeGK4AYUpperShear (Multiplicative.toAdd m)
            (nativeGK4BAIntAdd z t) =
            nativeGK4BAIntAdd (nativeGK4AYUpperShear (Multiplicative.toAdd m) z)
              (nativeGK4AYUpperShear (Multiplicative.toAdd m) t)
          rcases z with ⟨x,y⟩
          rcases t with ⟨a,b⟩
          apply Prod.ext
          · change x+a+2*Multiplicative.toAdd m*(y+b) =
              (x+2*Multiplicative.toAdd m*y)+(a+2*Multiplicative.toAdd m*b)
            ring
          · rfl
      | true =>
          change nativeGK4AYLowerShear (Multiplicative.toAdd m)
            (nativeGK4BAIntAdd z t) =
            nativeGK4BAIntAdd (nativeGK4AYLowerShear (Multiplicative.toAdd m) z)
              (nativeGK4AYLowerShear (Multiplicative.toAdd m) t)
          rcases z with ⟨x,y⟩
          rcases t with ⟨a,b⟩
          apply Prod.ext
          · rfl
          · change y+b+2*Multiplicative.toAdd m*(x+a) =
              (y+2*Multiplicative.toAdd m*x)+(b+2*Multiplicative.toAdd m*a)
            ring
  | mul a b ha hb =>
      calc
        nativeGK4BAIntegerWordAction (a*b) (nativeGK4BAIntAdd z t) =
            nativeGK4BAIntegerWordAction a
              (nativeGK4BAIntegerWordAction b (nativeGK4BAIntAdd z t)) :=
          nativeGK4BAIntegerWordAction_mul a b _
        _ = nativeGK4BAIntegerWordAction a
              (nativeGK4BAIntAdd (nativeGK4BAIntegerWordAction b z)
                (nativeGK4BAIntegerWordAction b t)) := by rw [hb]
        _ = nativeGK4BAIntAdd
              (nativeGK4BAIntegerWordAction a (nativeGK4BAIntegerWordAction b z))
              (nativeGK4BAIntegerWordAction a (nativeGK4BAIntegerWordAction b t)) :=
          ha _ _
        _ = nativeGK4BAIntAdd (nativeGK4BAIntegerWordAction (a*b) z)
              (nativeGK4BAIntegerWordAction (a*b) t) := by
          rw [nativeGK4BAIntegerWordAction_mul,
            nativeGK4BAIntegerWordAction_mul]

theorem nativeGK4BAIntegerWordAction_double
    (w : NativeGK4BAWord) (z : Int × Int) :
    nativeGK4BAIntegerWordAction w (2*z.1,2*z.2) =
      (2*(nativeGK4BAIntegerWordAction w z).1,
        2*(nativeGK4BAIntegerWordAction w z).2) := by
  have h := nativeGK4BAIntegerWordAction_add w z z
  simpa [nativeGK4BAIntAdd, two_mul] using h

#print axioms nativeGK4BAIntVec
#print axioms nativeGK4BARescaledVec
#print axioms nativeGK4BARescaledVec_mul
#print axioms nativeGK4BAIntegerWordAction_one
#print axioms nativeGK4BAIntegerWordAction_cast
#print axioms nativeGK4BAIntegerWordAction_forward
#print axioms nativeGK4BAIntegerWordAction_backward
#print axioms nativeGK4BAIntegerWordAction_unit
#print axioms nativeGK4BAIntegerEdge_action
#print axioms nativeGK4BAIntegerChain_action
#print axioms nativeGK4BAIntegerRoute_action
#print axioms nativeGK4BAIntAdd
#print axioms nativeGK4BAIntegerWordAction_add
#print axioms nativeGK4BAIntegerWordAction_double

end
end Kuu.F112.Physical
