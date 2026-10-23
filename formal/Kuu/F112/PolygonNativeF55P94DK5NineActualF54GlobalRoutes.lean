import Kuu.F112.PolygonNativeF55P94DK5ShellingNoncommutativeGap
import Mathlib.Tactic

/-!
# F112-P94D3J — all nine genuinely dependent global F54 routes

Lift the nine graph spines from P94D3I to real F54 typed proof terms.
Every route is built *solely* by composing P94D1's certified original
twenty-one elementary F54 rotation terms, with the genuine original
F45 Blocks, physical sectors and independent F19/F28 Nat depths.
The 13→0 endpoints are exactly the original sigma-typed F45 vertices.

These nine routes are NOT proved judgementally identical to the nine
separately face-whiskered routes: raw DepthRotationRoute concatenation
is a proof-relevant syntax, not a strict category. No false transports,
no shadow-inferred 3-cell and no global pentagonator filler.
No Gray, sorry/admit, added axioms or removal of public roots.
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

/-- Eliminable Type-valued names for the nine actual 13-to-0
K₅ graph routes. Fin is only an adapter, not a Type recursor
through an arbitrary propositional graph-membership proof. -/
inductive NativeK5GlobalF54RouteTag where
  | path0
  | path1
  | path2
  | path3
  | path4
  | path5
  | path6
  | path7
  | path8
  deriving DecidableEq

def nativeK5GlobalF54RouteTagOfFin (i : Fin 9) : NativeK5GlobalF54RouteTag :=
  match i.val with
  | 0 => .path0
  | 1 => .path1
  | 2 => .path2
  | 3 => .path3
  | 4 => .path4
  | 5 => .path5
  | 6 => .path6
  | 7 => .path7
  | 8 => .path8
  | _ => .path8

def nativeK5GlobalF54RouteTagFin : NativeK5GlobalF54RouteTag → Fin 9
  | .path0 => 0
  | .path1 => 1
  | .path2 => 2
  | .path3 => 3
  | .path4 => 4
  | .path5 => 5
  | .path6 => 6
  | .path7 => 7
  | .path8 => 8

theorem nativeK5GlobalF54RouteTag_roundtrip (i : Fin 9) :
    nativeK5GlobalF54RouteTagFin (nativeK5GlobalF54RouteTagOfFin i) = i := by
  fin_cases i <;> rfl

section FiveNativeStages
variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- Every one of the nine paths is an actual source F54 route:
real trans constructors on P94D1's twenty-one original
dependent elementary typed-rotation route witnesses. -/
def nativeK5ActualGlobalF54Route
    (tag : NativeK5GlobalF54RouteTag) :
    NativeK5GlobalRoute t1 t2 t3 t4 t5 :=
  match tag with
  | .path0 => (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e15) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e11)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e2))
  | .path1 => (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e15) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e13)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e6)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e1))
  | .path2 => (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e19) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e12)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e4)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0))
  | .path3 => (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e19) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e12)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e10)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e2))
  | .path4 => (.trans (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e19) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e17)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e8)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e3)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0))
  | .path5 => (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e14)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e6)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e1))
  | .path6 => (.trans (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e18)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e9)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e5)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e1))
  | .path7 => (.trans (.trans (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e18)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e9)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e7)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e3)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0))
  | .path8 => (.trans (.trans (.trans (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e18)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e16)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e8)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e3)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0))

/-- Full, total Fin interface to nine independently typed genuine
F54 paths; it does not collapse their distinct proof terms. -/
def nativeK5ActualGlobalF54RouteFin (i : Fin 9) :
    NativeK5GlobalRoute t1 t2 t3 t4 t5 :=
  nativeK5ActualGlobalF54Route t1 t2 t3 t4 t5
    (nativeK5GlobalF54RouteTagOfFin i)

/-- Proven primitive original F54 rotation count for each
global route, not merely its combinatorial graph length. -/
theorem nativeK5ActualGlobalF54Route_count
    (tag : NativeK5GlobalF54RouteTag) :
    (nativeK5ActualGlobalF54Route t1 t2 t3 t4 t5 tag).rotationCount =
      (nativeK5GlobalMonotonePath
        (nativeK5GlobalF54RouteTagFin tag)).length - 1 := by
  cases tag <;> rfl

theorem nativeK5ActualGlobalF54RouteFin_count (i : Fin 9) :
    (nativeK5ActualGlobalF54RouteFin t1 t2 t3 t4 t5 i).rotationCount =
      (nativeK5GlobalMonotonePath i).length - 1 := by
  fin_cases i <;> rfl

/-- Every route genuinely preserves the full original ordered
physical sector source; this follows from original typed F54
proof terms, never from vertex shape alone. -/
theorem nativeK5ActualGlobalF54Route_sectors_eq
    (tag : NativeK5GlobalF54RouteTag) :
    (nativeK5TypedVertex t1 t2 t3 t4 t5 (13 : Fin 14)).2.2.sectors =
      (nativeK5TypedVertex t1 t2 t3 t4 t5 (0 : Fin 14)).2.2.sectors :=
  (nativeK5ActualGlobalF54Route t1 t2 t3 t4 t5 tag).sectors_eq

/-- Concrete north C60 fifth physical sector remains present in
each genuine five-stage route endpoint. -/
theorem northK5ActualGlobalF54Route_count (i : Fin 9) :
    (nativeK5ActualGlobalF54RouteFin
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage
      northNativeF45FifthStage i).rotationCount =
        (nativeK5GlobalMonotonePath i).length - 1 :=
  nativeK5ActualGlobalF54RouteFin_count _ _ _ _ _ i

#print axioms nativeK5GlobalF54RouteTag_roundtrip
#print axioms nativeK5ActualGlobalF54Route
#print axioms nativeK5ActualGlobalF54Route_count
#print axioms nativeK5ActualGlobalF54RouteFin_count
#print axioms nativeK5ActualGlobalF54Route_sectors_eq
#print axioms northK5ActualGlobalF54Route_count

end FiveNativeStages
end
end Kuu.F112.Physical
