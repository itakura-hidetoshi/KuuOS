import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BAPolyCyclic
import Mathlib.Tactic

/-!
F112-P94D3GK4BA stage 2b: polynomial word-action matrix compatibility.
The already verified original cyclic shears and their group homomorphisms
are imported from GK4BA PolyCyclic PR #2842, not redeclared here.
This module proves the remaining genuine generator/word-action results.
No original Type-valued 3-cell is inferred from numerical equality.
Append-only / same public root107 / fixed Lean and mathlib.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/
namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 100000
noncomputable section

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
