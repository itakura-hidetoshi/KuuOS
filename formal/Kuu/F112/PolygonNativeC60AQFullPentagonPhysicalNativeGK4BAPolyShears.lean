import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOriginalWord
import Mathlib.Tactic

/-!
F112-P94D3GK4BA stage 2a — isolated universal polynomial cyclic
shear group homomorphisms, source polynomial matrix action and
generator compatibility; original F54 path induction is downstream.
All definitions live in Z[X] × Z[X], keep original pinned mathlib.
No old source modified or assumptions widened.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 100000
-- Bound tactic search so its failure is reported by Lean at the actual location.
noncomputable section

abbrev NativeGK4BAPolyVector := Polynomial Int × Polynomial Int

def nativeGK4BAPolyUpperShear (n : Int) (z : NativeGK4BAPolyVector) :
    NativeGK4BAPolyVector :=
  (z.1 + Polynomial.C n * z.2, z.2)

def nativeGK4BAPolyLowerShear (n : Int) (z : NativeGK4BAPolyVector) :
    NativeGK4BAPolyVector :=
  (z.1, z.2 + Polynomial.C n * Polynomial.X * z.1)

def nativeGK4BAPolyUpperPerm (n : Int) : Equiv.Perm NativeGK4BAPolyVector where
  toFun := nativeGK4BAPolyUpperShear n
  invFun := nativeGK4BAPolyUpperShear (-n)
  left_inv := by
    intro ⟨x, y⟩
    apply Prod.ext
    · change x + Polynomial.C n * y + Polynomial.C (-n) * y = x
      simp only [map_neg, neg_mul]
      simp
    · rfl
  right_inv := by
    intro ⟨x, y⟩
    apply Prod.ext
    · change x + Polynomial.C (-n) * y + Polynomial.C n * y = x
      simp only [map_neg, neg_mul]
      simp
    · rfl

def nativeGK4BAPolyLowerPerm (n : Int) : Equiv.Perm NativeGK4BAPolyVector where
  toFun := nativeGK4BAPolyLowerShear n
  invFun := nativeGK4BAPolyLowerShear (-n)
  left_inv := by
    intro ⟨x, y⟩
    apply Prod.ext
    · rfl
    · change y + Polynomial.C n * Polynomial.X * x +
          Polynomial.C (-n) * Polynomial.X * x = y
      simp only [map_neg, neg_mul]
      simp
  right_inv := by
    intro ⟨x, y⟩
    apply Prod.ext
    · rfl
    · change y + Polynomial.C (-n) * Polynomial.X * x +
          Polynomial.C n * Polynomial.X * x = y
      simp only [map_neg, neg_mul]
      simp

/-- Upper polynomial shear as actual infinite-cyclic group hom. -/
def nativeGK4BAPolyUpperHom :
    Multiplicative Int →* Equiv.Perm NativeGK4BAPolyVector where
  toFun n := nativeGK4BAPolyUpperPerm (Multiplicative.toAdd n)
  map_one' := by
    apply Equiv.ext
    intro ⟨x, y⟩
    apply Prod.ext
    · change x + Polynomial.C (0 : Int) * y = x
      simp
    · rfl
  map_mul' m n := by
    apply Equiv.ext
    intro ⟨x, y⟩
    apply Prod.ext
    · change x + Polynomial.C
          (Multiplicative.toAdd m + Multiplicative.toAdd n) * y =
          x + Polynomial.C (Multiplicative.toAdd n) * y +
            Polynomial.C (Multiplicative.toAdd m) * y
      simp only [map_add, add_mul]
      abel
    · rfl

/-- Explicit scalar-addition law in Z[X]^2, separated from the
bundled permutation group-hom kernel proof. -/
theorem nativeGK4BAPolyLowerShear_add (m n : Int)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyLowerShear (m + n) z =
      nativeGK4BAPolyLowerShear m (nativeGK4BAPolyLowerShear n z) := by
  rcases z with ⟨x, y⟩
  apply Prod.ext
  · rfl
  · change y + Polynomial.C (m + n) * Polynomial.X * x =
      y + Polynomial.C n * Polynomial.X * x +
        Polynomial.C m * Polynomial.X * x
    rw [map_add]
    ring

/-- Lower polynomial shear as the second cyclic group hom. -/
def nativeGK4BAPolyLowerHom :
    Multiplicative Int →* Equiv.Perm NativeGK4BAPolyVector where
  toFun n := nativeGK4BAPolyLowerPerm (Multiplicative.toAdd n)
  map_one' := by
    apply Equiv.ext
    intro ⟨x, y⟩
    apply Prod.ext
    · rfl
    · change y + Polynomial.C (0 : Int) * Polynomial.X * x = y
      simp
  map_mul' m n := by
    apply Equiv.ext
    intro z
    change nativeGK4BAPolyLowerShear
        (Multiplicative.toAdd m + Multiplicative.toAdd n) z =
      nativeGK4BAPolyLowerShear (Multiplicative.toAdd m)
        (nativeGK4BAPolyLowerShear (Multiplicative.toAdd n) z)
    exact nativeGK4BAPolyLowerShear_add _ _ z


/-- Universal polynomial target attached to EXACTLY the prior
GK4AZ indexed two-cyclic free-product source. -/
def nativeGK4BAPolyFactors (i : Bool) :
    Multiplicative Int →* Equiv.Perm NativeGK4BAPolyVector :=
  if i then nativeGK4BAPolyLowerHom else nativeGK4BAPolyUpperHom

def nativeGK4BAPolyWordAction (w : NativeGK4BAWord) (z : NativeGK4BAPolyVector) :
    NativeGK4BAPolyVector :=
  (Monoid.CoprodI.lift nativeGK4BAPolyFactors w) z

theorem nativeGK4BAPolyWordAction_mul (u v : NativeGK4BAWord)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction (u * v) z =
      nativeGK4BAPolyWordAction u (nativeGK4BAPolyWordAction v z) := by
  simp only [nativeGK4BAPolyWordAction, map_mul]
  rfl

theorem nativeGK4BAPolyWordAction_one (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction 1 z = z := by
  simp [nativeGK4BAPolyWordAction]

/-- Matrix action of the ORIGINAL GK4AV polynomial pair-matrix. -/
def nativeGK4BAPolyMatAction (M : NativeGK4AVValue)
    (z : NativeGK4BAPolyVector) : NativeGK4BAPolyVector :=
  (M.1.1 * z.1 + M.1.2 * z.2,
    M.2.1 * z.1 + M.2.2 * z.2)

theorem nativeGK4BAPolyMatAction_mul (A B : NativeGK4AVValue)
    (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyMatAction (nativeGK4AVMul A B) z =
      nativeGK4BAPolyMatAction A (nativeGK4BAPolyMatAction B z) := by
  rcases A with ⟨⟨a, b⟩, ⟨c, d⟩⟩
  rcases B with ⟨⟨e, f⟩, ⟨g, h⟩⟩
  rcases z with ⟨x, y⟩
  apply Prod.ext
  · change (a*e+b*g)*x + (a*f+b*h)*y =
      a*(e*x+f*y) + b*(g*x+h*y)
    ring
  · change (c*e+d*g)*x + (c*f+d*h)*y =
      c*(e*x+f*y) + d*(g*x+h*y)
    ring

theorem nativeGK4BAPolyWordAction_cast (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction nativeGK4BAWordCast z =
      nativeGK4BAPolyMatAction nativeGK4AVCast z := by
  simp only [nativeGK4BAPolyWordAction, nativeGK4BAWordCast,
    Monoid.CoprodI.lift_of]
  rcases z with ⟨x,y⟩
  simp [nativeGK4BAPolyFactors, nativeGK4BAPolyUpperHom,
    nativeGK4BAPolyUpperPerm, nativeGK4BAPolyUpperShear,
    nativeGK4BAPolyMatAction, nativeGK4AVCast]

theorem nativeGK4BAPolyWordAction_forward (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction nativeGK4BAWordForward z =
      nativeGK4BAPolyMatAction nativeGK4AVForward z := by
  simp only [nativeGK4BAPolyWordAction, nativeGK4BAWordForward,
    Monoid.CoprodI.lift_of]
  rcases z with ⟨x,y⟩
  simp [nativeGK4BAPolyFactors, nativeGK4BAPolyUpperHom,
    nativeGK4BAPolyUpperPerm, nativeGK4BAPolyUpperShear,
    nativeGK4BAPolyMatAction, nativeGK4AVForward]

theorem nativeGK4BAPolyWordAction_backward (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction nativeGK4BAWordBackward z =
      nativeGK4BAPolyMatAction nativeGK4AVBackward z := by
  simp only [nativeGK4BAPolyWordAction, nativeGK4BAWordBackward,
    Monoid.CoprodI.lift_of]
  rcases z with ⟨x,y⟩
  simp [nativeGK4BAPolyFactors, nativeGK4BAPolyLowerHom,
    nativeGK4BAPolyLowerPerm, nativeGK4BAPolyLowerShear,
    nativeGK4BAPolyMatAction, nativeGK4AVBackward]

theorem nativeGK4BAPolyWordAction_unit (z : NativeGK4BAPolyVector) :
    nativeGK4BAPolyWordAction nativeGK4BAWordOne z =
      nativeGK4BAPolyMatAction nativeGK4AVOne z := by
  simp [nativeGK4BAWordOne, nativeGK4BAPolyWordAction_one,
    nativeGK4BAPolyMatAction, nativeGK4AVOne]

#print axioms nativeGK4BAPolyUpperShear
#print axioms nativeGK4BAPolyLowerShear
#print axioms nativeGK4BAPolyUpperPerm
#print axioms nativeGK4BAPolyLowerPerm
#print axioms nativeGK4BAPolyUpperHom
#print axioms nativeGK4BAPolyLowerShear_add
#print axioms nativeGK4BAPolyLowerHom
#print axioms nativeGK4BAPolyFactors
#print axioms nativeGK4BAPolyWordAction
#print axioms nativeGK4BAPolyWordAction_mul
#print axioms nativeGK4BAPolyWordAction_one
#print axioms nativeGK4BAPolyMatAction
#print axioms nativeGK4BAPolyMatAction_mul
#print axioms nativeGK4BAPolyWordAction_cast
#print axioms nativeGK4BAPolyWordAction_forward
#print axioms nativeGK4BAPolyWordAction_backward
#print axioms nativeGK4BAPolyWordAction_unit

end
end Kuu.F112.Physical
