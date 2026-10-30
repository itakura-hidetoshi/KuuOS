import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4StructuralP92ReturnGate

/-!
# F112-P94D3GK4B — unconditional original constructor / structural seam obstruction

GK4 gave the exact existence condition for a typed StructuralComparison
return to the ORIGINAL P92B presentation: each truly typed F54 seam
must first be realized by an original P92B proof. Here we establish a
strictly stronger, independent equality-reflection obstruction.

The ORIGINAL P92B constructor and the genuinely ADDED F54 structural
seam constructor are disjoint Type-valued evidence, even when their
F45/F54 boundaries coincide. The old P92B inclusion is therefore
not surjective in ANY original F54 route's reflexive fiber.

More importantly, for any typed return fixing every original P92B
proof, injectivity is impossible. This obstruction applies in
particular to every return constructed from GK4 seam realizations.
It does NOT assert arbitrary unrelated Type equivalences impossible;
it rules out the specific extension-compatible, original-preserving
inverse/equality-reflection required for historical presentation
identification. No quotient, observer, numeric shadow or new axiom.

Append-only / same-root; Lean v4.30.0-rc2, pinned mathlib;
no sorry, no Gray, no modification of 107 public roots.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

universe uD vD uE vE

section OriginalStructuralObstruction

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- Constructor disjointness is at the ORIGINAL dependent Type-valued
witness level; no shadow or Setoid equality has been introduced. -/
theorem nativeGK4B_original_ne_structural
    (old : NativeF55P92AssocComparison p r s)
    (seam : NativeF54StructuralSeam p r s) :
    NativeF55StructuralComparison.original old ≠
      NativeF55StructuralComparison.structural seam := by
  intro heq
  cases heq

/-- At every genuine F54 route, the original P92B injection misses
the tagged structural reflexivity seam, with the same typed endpoints. -/
theorem nativeGK4B_original_not_surjective
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Function.Surjective
      (fun old : NativeF55P92AssocComparison p route route =>
        (NativeF55StructuralComparison.original old :
          NativeF55StructuralComparison p route route)) := by
  intro hsurj
  obtain ⟨old, heq⟩ := hsurj
    (NativeF55StructuralComparison.structural (NativeF54StructuralSeam.refl route))
  exact (nativeGK4B_original_ne_structural old (.refl route)) heq

/-- Exact constructor-tag obstruction. Any return of genuine original
StructuralComparison evidence to original P92B which fixes ALL original
P92B witnesses must identify two different original Type constructors.
Consequently such a return can never be injective. -/
theorem nativeGK4B_no_injective_original_preserving_return
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (ret : NativeF55StructuralComparison p route route →
      NativeF55P92AssocComparison p route route)
    (hOriginal : ∀ old : NativeF55P92AssocComparison p route route,
      ret (.original old) = old) :
    ¬ Function.Injective ret := by
  intro hinj
  let seam : NativeF54StructuralSeam p route route := .refl route
  have heq :
      ret (.original (ret (.structural seam))) =
        ret (.structural seam) :=
    hOriginal _
  have hsame := hinj heq
  exact (nativeGK4B_original_ne_structural (ret (.structural seam)) seam) hsame

/-- Even if EVERY original structural F54 seam admits a chosen P92B
realization (GK4's sufficient condition), the resulting typed return
cannot reflect all equality in any reflexive F54 route fiber. -/
theorem nativeGK4B_interpret_noninjective
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (h : NativeGK4SeamP92Realization p D E) :
    ¬ Function.Injective
      (fun cell : NativeF55StructuralComparison p route route =>
        nativeGK4InterpretStructural h cell) := by
  apply nativeGK4B_no_injective_original_preserving_return route
  intro old
  exact nativeGK4InterpretStructural_original h old

end OriginalStructuralObstruction

#print axioms nativeGK4B_original_ne_structural
#print axioms nativeGK4B_original_not_surjective
#print axioms nativeGK4B_no_injective_original_preserving_return
#print axioms nativeGK4B_interpret_noninjective

end Kuu.F112.Physical
