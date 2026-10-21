import Kuu.F112.PolygonNativeF55StrictPathObserverP60
import Kuu.F112.PolygonNativeF55RawPathNormalizerFunctorP60

/-!
# F112-P61 — horizontal / vertical strict-path boundary on independent F55

The independent genuine Type-valued F55 source has NINE raw constructors.
P59 strictly normalizes *vertical* identity and pasting to Mathlib
free paths, while the OTHER seven raw constructors remain singleton
proof-relevant generators. P60 proves factorization through ONE chosen
shadow quotient. Here we inspect derived horizontal pasting itself.

Positive: the native derived horizontal 3-cell is, after P59
normalization, EXACTLY a two-edge composite (both whiskered proof
witnesses are retained); its selected complete shadow is the sum of
the true left and right raw shadows.

Obstruction: even if both horizontal arguments are raw identities,
the resulting native horizontal syntax normalizes to a TWO-edge path,
NOT the empty path. Native left/right context applied to raw identities
likewise normalize to singleton paths. This is a genuine obstruction to
claiming the current vertical normalizer is already a STRICTLY UNIT-PRESERVING
horizontal path functor, and not a global no-go theorem.

No equality of raw proofs is derived from numerical shadow equality.
No imported historical KUOS higher source, Gray, braiding or new axioms.
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

/-- P59's vertical normalization of true horizontal pasting has
TWO actual generators: source-ordered left-context post-whiskering
and right-context pre-whiskering. Neither is erased by declaration. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_normalized_length
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
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    (f.horizontal g).toNativeStrictPath.length = 2 := by
  rfl

/-- Positive horizontal compatibility *through the chosen observer*:
both the signed charges and the independently chosen parity coordinate
are conserved by genuine two-edge horizontal paste. This uses
the independently typed source proof and actual free path functor. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_normalized_shadow
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
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    nativeF55ThreeEval
      ((nativeF55RawPathsToShadow
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)).map
        (f.horizontal g).toNativeStrictPath) =
      f.nativeShadow + g.nativeShadow := by
  calc
    _ = (f.horizontal g).nativeShadow :=
      (f.horizontal g).toNativeStrictPath_shadow_eval
    _ = f.nativeShadow + g.nativeShadow :=
      f.horizontal_nativeShadow g

/-- Left contextual whiskering of a RAW unit is a genuine singleton
edge under P59, not a strict path identity. The context generator
retains its own Type-valued proof history. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext_ident_normalized_length
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
       (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u)
       later).toNativeStrictPath.length = 1 := by
  rfl

/-- The analogous right contextual whiskering also records a
singleton proof generator, rather than being silently erased. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext_ident_normalized_length
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
       earlier (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u)
      ).toNativeStrictPath.length = 1 := by
  rfl

/-- Source-ordered horizontal pasting of TWO literal raw identity
cells has length TWO, whereas the strict vertical-normalized
identity at that SAME route has length ZERO. This counterexample is
uniform over both Nat axes and all independent source categories. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_not_normalized_unit
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
       (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v)
      ).toNativeStrictPath ≠
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (KuuNativeF45Tree.DepthRotationRoute.trans
          (.leftContext u rightBefore)
          (.rightContext leftAfter v))).toNativeStrictPath := by
  intro h
  have hl := congrArg Quiver.Path.length h
  change (2 : Nat) = 0 at hl
  exact (by decide : (2 : Nat) ≠ 0) hl

/-- The same TWO identity-input horizontal composite has
ZERO selected signed charge and selected exchange parity.
This DOES NOT imply equality in the free strict path category. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_ident_shadow_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v)).nativeShadow =
        (0 : KuuNativeF55Shadow) := by
  rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow]
  rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_normalized_length
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_normalized_shadow
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext_ident_normalized_length
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext_ident_normalized_length
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_not_normalized_unit
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_ident_shadow_zero

end
end Kuu.F112.Physical
