import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAOriginalWord
import Mathlib.Tactic
/-!
GK4BA isolated cyclic polynomial shear group homomorphisms.
Stage2a1: no unproved original Type equality, no new axioms.
Pin Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only same root107. Copyright © 2026 Hidetoshi Itakura / 板倉英俊.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 100000
-- A bounded elaboration budget makes any expensive tactic fail locally
-- with its real source position rather than losing the runner to shutdown.
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
    intro ⟨x, y⟩
    apply Prod.ext
    · rfl
    · change y + Polynomial.C
          (Multiplicative.toAdd m + Multiplicative.toAdd n) *
          Polynomial.X * x =
          y + Polynomial.C (Multiplicative.toAdd n) * Polynomial.X * x +
            Polynomial.C (Multiplicative.toAdd m) * Polynomial.X * x
      simp only [map_add, add_mul]
      abel

#print axioms nativeGK4BAPolyUpperShear
#print axioms nativeGK4BAPolyLowerShear
#print axioms nativeGK4BAPolyUpperPerm
#print axioms nativeGK4BAPolyLowerPerm
#print axioms nativeGK4BAPolyUpperHom
#print axioms nativeGK4BAPolyLowerHom

end
end Kuu.F112.Physical
