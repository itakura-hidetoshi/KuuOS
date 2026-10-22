import Kuu.F112.PolygonNativeF55P86ContextFourCell

/-!
# F112-P87A — recursively context- and horizontal-closed source 4-cells

P85/P86 prove genuine context and horizontal transport with successive
enlargements: old P85 witness -> new P86 witness. They do NOT give
endofunctorial horizontal transport on P86 quotient classes.

This file constructs a DIFFERENT freely generated genuine SOURCE
Type-valued 4-cell presentation, retaining every old P86 witness
and closing **recursively on its OWN certificates** under original
F55 left/right binary contexts, F54 pre/post route actions,
left/right horizontal whiskering by arbitrary original raw F55
3-proofs, and all vertical source witness operations.

All original F54 dependent types, original 9-constructor F55
raw proof endpoints, real C60 square and pentagon evidence are retained.
No relation is generated from mere equality of numeric shadows.

Every recursive constructor preserves all original full F55
signed charges and the independent ZMod2 exchange phase. The exact
path-soundness judgement will be separately given in P87B, relative
to a distinct witness-generated typed P87 path congruence.

No strict interchange, global strict 3/n-category or hyperdescent
is assumed. No Gray, sorry/admit, or new axioms.
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

/-- Twelve genuine Type-valued constructors, of which all six
context/route/horizontal actions act recursively on P87 itself.
Old P86 witnesses are only the original single base generator. -/
inductive NativeF55P87ClosedFourCell
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | old

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P86ContextFourCell f g) :
      NativeF55P87ClosedFourCell f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55P87ClosedFourCell f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedFourCell g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (fg : NativeF55P87ClosedFourCell f g)
      (gh : NativeF55P87ClosedFourCell g h) :
      NativeF55P87ClosedFourCell f h
  | leftWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (h : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedFourCell (.trans prior f) (.trans prior g)
  | rightWhisker

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P87ClosedFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55P87ClosedFourCell (.trans f suffix) (.trans g suffix)
  | leftContext

      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P87ClosedFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P87ClosedFourCell
        (.leftContext f later) (.leftContext g later)
  | rightContext

      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedFourCell
        (.rightContext earlier f) (.rightContext earlier g)
  | precompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
      {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedFourCell
        (.precompose prior f) (.precompose prior g)
  | postcompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (h : NativeF55P87ClosedFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P87ClosedFourCell
        (.postcompose f suffix) (.postcompose g suffix)
  | horizontalLeft

      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
      {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
      {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u'}
      (h : NativeF55P87ClosedFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P87ClosedFourCell
        (f.horizontal g) (f'.horizontal g)
  | horizontalRight

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
      {g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v'}
      (h : NativeF55P87ClosedFourCell g g') :
      NativeF55P87ClosedFourCell
        (f.horizontal g) (f.horizontal g')


variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- Independent source-recursive full shadow preservation. The
six contextual cases use the INDUCTION HYPOTHESIS for the P87
certificate; none is reduced to the narrower P86 generator rule. -/
theorem NativeF55P87ClosedFourCell.shadow_sound
    (h : NativeF55P87ClosedFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | old witness => exact witness.shadow_sound
  | refl raw => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior witness ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker witness suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | leftContext witness later ih => exact ih
  | rightContext earlier witness ih => exact ih
  | precompose prior witness ih => exact ih
  | postcompose witness suffix ih => exact ih
  | horizontalLeft witness g ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow) ih
  | horizontalRight f witness ih =>
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z) ih

/-- TWO P87 four-cell witnesses always paste horizontally to a
genuine P87 four-cell; no old-to-new shift or scalar equality. -/
def nativeF55P87Horizontal_twoSided
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {r r' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {s s' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r r'}
    {g g' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s s'}
    (hf : NativeF55P87ClosedFourCell f f')
    (hg : NativeF55P87ClosedFourCell g g') :
    NativeF55P87ClosedFourCell (f.horizontal g) (f'.horizontal g') :=
  .trans (.horizontalLeft hf g) (.horizontalRight f' hg)

#print axioms NativeF55P87ClosedFourCell
#print axioms NativeF55P87ClosedFourCell.shadow_sound
#print axioms nativeF55P87Horizontal_twoSided

end
end Kuu.F112.Physical
