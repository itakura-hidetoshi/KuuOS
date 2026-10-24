import Kuu.F112.PolygonNativeF55P94DK5TypedPentagonatorBoundary
import Mathlib.Tactic

/-!
# F112-P94D3K: nine original Type-valued F54 routes

The nine K5 shelling paths have a common original dependent F45
source and target. Here ALL NINE paths are built as actual F54
DepthRotationRoute proof terms from the 21 genuine tagged edges.

The previous finite graph is used only to select which already-proved
Type-valued edge constructors to compose. No graph equality is
promoted into a higher cell. Nat depth transports and the original
F45 Blocks remain inside the actual F54 terms.

This discharges the ROUTE component of the former conditional
NativeK5TypedShellingDatum. Its P92B seam comparisons and independent
pentagonator/Peiffer 4-coherence are NOT assumed or inferred.
No Gray, sorry/admit, axioms, or public-root changes.
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

/-- Nine TRUE source-level F54 13-to-0 routes. Each selected
step is an existing original Type-valued tagged edge from P94D1.
The exact sequences of tags correspond to the nine monotonically
directed K5 finite spines, but no graph equality is used as a
route transport, 3-cell, or 4-cell.

0: 15-11-2; 1: 15-13-6-1; 2: 19-12-4-0;
3: 19-12-10-2; 4: 19-17-8-3-0; 5: 20-14-6-1;
6: 20-18-9-5-1; 7: 20-18-9-7-3-0;
8: 20-18-16-8-3-0. -/
def nativeK5TypedGlobalF54Route (i : Fin 9) :
    NativeK5GlobalRoute t1 t2 t3 t4 t5 := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  exact match i.val with
    | 0 => .trans (e .e15) (.trans (e .e11) (e .e2))
    | 1 => .trans (e .e15) (.trans (e .e13) (.trans (e .e6) (e .e1)))
    | 2 => .trans (e .e19) (.trans (e .e12) (.trans (e .e4) (e .e0)))
    | 3 => .trans (e .e19) (.trans (e .e12) (.trans (e .e10) (e .e2)))
    | 4 => .trans (e .e19) (.trans (e .e17)
        (.trans (e .e8) (.trans (e .e3) (e .e0))))
    | 5 => .trans (e .e20) (.trans (e .e14) (.trans (e .e6) (e .e1)))
    | 6 => .trans (e .e20) (.trans (e .e18)
        (.trans (e .e9) (.trans (e .e5) (e .e1))))
    | 7 => .trans (e .e20) (.trans (e .e18)
        (.trans (e .e9) (.trans (e .e7)
          (.trans (e .e3) (e .e0)))))
    | 8 => .trans (e .e20) (.trans (e .e18)
        (.trans (e .e16) (.trans (e .e8)
          (.trans (e .e3) (e .e0)))))
    | _ => .trans (e .e15) (.trans (e .e11) (e .e2))

/-- The canonical genuine Type-valued route family can now be
supplied unconditionally; only the typed seams remain open. -/
def nativeK5TypedGlobalF54Routes :
    Fin 9 → NativeK5GlobalRoute t1 t2 t3 t4 t5 :=
  nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5

#print axioms nativeK5TypedGlobalF54Route
#print axioms nativeK5TypedGlobalF54Routes

end FiveNativeStages
end
end Kuu.F112.Physical
