import Kuu.F112.PolygonNativeF55P87ClosedFourCellCore
import Mathlib.CategoryTheory.Quotient

/-!
# F112-P87B — recursively source-witness-compatible typed path quotient

P87A's recursively closed genuine Type-valued source 4-cell syntax
has no assumed P86 path soundness. P86's existing path congruence
remains untouched.

We explicitly select a DISTINCT typed path congruence:
old P86 path witnesses, the five equivalence/category operations,
and SIX contextual, pre/post F54 and horizontal generators now
carrying genuinely recursive P87 source FOUR-CELL witnesses.
Every rule is independently sound for original F55 FULL shadow,
not merely a scalar charge. The strict local Mathlib quotient
category has the precise proof-generated relation as its
IF-AND-ONLY-IF source kernel. The original three-coordinate
observer factors exactly through it.

The old P86 quotient maps to the new P87 quotient by a functor
whose equality with direct original raw F55 path projection is
proved. No source 3-proof is erased, no old root discarded.

This does NOT prove original F55 strict interchange. In
particular all historical F54 route objects remain distinct
unless literally equal, even in the new selected quotient.
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

inductive NativeF55P87ClosedPathRel
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      (first : KuuNativeF45Tree p n m ma pa mb pb)
      (last : KuuNativeF45Tree p n' m' ma pa mb pb)
      {r s : NativeF55RawRouteVertex first last},
      Quiver.Path r s → Quiver.Path r s → Prop where
  | old

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g : Quiver.Path r s}
      (witness : NativeF55P86ContextPathRel first last f g) :
      NativeF55P87ClosedPathRel first last f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      (f : Quiver.Path r s) :
      NativeF55P87ClosedPathRel first last f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g : Quiver.Path r s}
      (witness : NativeF55P87ClosedPathRel first last f g) :
      NativeF55P87ClosedPathRel first last g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g h : Quiver.Path r s}
      (fg : NativeF55P87ClosedPathRel first last f g)
      (gh : NativeF55P87ClosedPathRel first last g h) :
      NativeF55P87ClosedPathRel first last f h
  | comp

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : NativeF55RawRouteVertex first last}
      {f f' : Quiver.Path r s}
      {g g' : Quiver.Path s t}
      (hf : NativeF55P87ClosedPathRel first last f f')
      (hg : NativeF55P87ClosedPathRel first last g g') :
      NativeF55P87ClosedPathRel first last (f.comp g) (f'.comp g')
  | leftContext

      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P87ClosedFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P87ClosedPathRel
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later)
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext f later).toNativeStrictPath
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext g later).toNativeStrictPath
  | rightContext

      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedPathRel
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last)
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext earlier f).toNativeStrictPath
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext earlier g).toNativeStrictPath
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
      (witness : NativeF55P87ClosedFourCell f g) :
      NativeF55P87ClosedPathRel first last
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.precompose prior f).toNativeStrictPath
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.precompose prior g).toNativeStrictPath
  | postcompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (witness : NativeF55P87ClosedFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P87ClosedPathRel first last
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.postcompose f suffix).toNativeStrictPath
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.postcompose g suffix).toNativeStrictPath
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
      (witness : NativeF55P87ClosedFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P87ClosedPathRel
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)
        (f.horizontal g).toNativeStrictPath
        (f'.horizontal g).toNativeStrictPath
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
      (witness : NativeF55P87ClosedFourCell g g') :
      NativeF55P87ClosedPathRel
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)
        (f.horizontal g).toNativeStrictPath
        (f.horizontal g').toNativeStrictPath

/-- Full original shadow preservation is a theorem about ALL
eleven P86 path rules. Neither P85 four-cell proof existence nor
P86 path comparison is DEFINED by numerical shadow equality. -/
theorem NativeF55P87ClosedPathRel.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (h : NativeF55P87ClosedPathRel first last f g) :
    (nativeF55RawPathsToShadow first last).map f =
      (nativeF55RawPathsToShadow first last).map g := by
  induction h with
  | old witness => exact witness.shadow_sound
  | refl path => rfl
  | symm witness ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | comp hf hg ihf ihg =>
      calc
        _ = nativeF55ThreeComp _ _ :=
          nativeF55RawPathsToShadow_mapTypedComp _ _ _ _
        _ = nativeF55ThreeComp _ _ := by rw [ihf, ihg]
        _ = _ := (nativeF55RawPathsToShadow_mapTypedComp _ _ _ _).symm
  | leftContext witness later =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      exact witness.shadow_sound
  | rightContext earlier witness =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      exact witness.shadow_sound
  | precompose prior witness =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      exact witness.shadow_sound
  | postcompose witness suffix =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      exact witness.shadow_sound
  | horizontalLeft witness g =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => z + g.nativeShadow)
          witness.shadow_sound
  | horizontalRight f witness =>
      apply nativeF55ThreeEval_injective
      rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval,
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval]
      simpa only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_nativeShadow] using
        congrArg (fun z : KuuNativeF55Shadow => f.nativeShadow + z)
          witness.shadow_sound

/-- The selected P86 path relation is a genuine equivalence on
each exact pair of dependent original F54 route vertices. -/
theorem nativeF55P87ClosedPathRel_equivalence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : NativeF55RawRouteVertex first last) :
    Equivalence (NativeF55P87ClosedPathRel first last (r := r) (s := s)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro f; exact .refl f
  · intro f g h; exact .symm h
  · intro f g h hfg hgh; exact .trans hfg hgh

/-- The P86 proof-generated relation, not a scalar-kernel proxy. -/
def nativeF55P87ClosedHomRel
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    HomRel (NativeF55RawPathCategory first last) :=
  fun {_r _s} f g => NativeF55P87ClosedPathRel first last f g

/-- Congruence on each original typed P59 path Hom, supplied
directly by actual P86 evidence on both vertical operands. -/
instance nativeF55P87ClosedCongruence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    CategoryTheory.Congruence (nativeF55P87ClosedHomRel first last) where
  equivalence := by
    intro r s
    exact nativeF55P87ClosedPathRel_equivalence first last r s
  comp_left := by
    intro r s t f g g' h
    exact .comp (.refl f) h
  comp_right := by
    intro r s t f f' g h
    exact .comp h (.refl g)

/-- A strict LOCAL Mathlib category of the original F54 route
vertices, preserving original raw F55 proof-labelled free paths. -/
abbrev NativeF55P87ClosedPathCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  CategoryTheory.Quotient (nativeF55P87ClosedHomRel first last)

/-- Universal original-path projection into the precisely selected
P86 path quotient category, with all F54 route objects retained. -/
def nativeF55P87ClosedQuotientFunctor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55RawPathCategory first last ⥤
      NativeF55P87ClosedPathCategory first last :=
  CategoryTheory.Quotient.functor (nativeF55P87ClosedHomRel first last)

/-- EXACT kernel: quotient equality IFF one original-source
P86 proof-generated path comparison exists. -/
theorem nativeF55P87ClosedQuotient_map_eq_iff
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : NativeF55RawRouteVertex first last}
    (f g : Quiver.Path r s) :
    (nativeF55P87ClosedQuotientFunctor first last).map f =
      (nativeF55P87ClosedQuotientFunctor first last).map g ↔
      NativeF55P87ClosedPathRel first last f g := by
  exact CategoryTheory.Quotient.functor_map_eq_iff
    (nativeF55P87ClosedHomRel first last) f g

/-- Old full signed-charge and independent parity observer factors
through P86 exactly. This factorization is justified by proofs. -/
def nativeF55P87ClosedToShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55P87ClosedPathCategory first last ⥤
      (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  CategoryTheory.Quotient.lift
    (nativeF55P87ClosedHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P87ClosedPathRel.shadow_sound h)

/-- Exact commuting triangle original raw path -> P86 -> full shadow. -/
theorem nativeF55P87Closed_shadow_factor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeF55P87ClosedQuotientFunctor first last ⋙
      nativeF55P87ClosedToShadow first last =
      nativeF55RawPathsToShadow first last := by
  exact CategoryTheory.Quotient.lift_spec
    (nativeF55P87ClosedHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P87ClosedPathRel.shadow_sound h)

/-- The old exact P84 path relation embeds without rewriting
any old path or erasing its witnesses. -/
theorem NativeF55P86ContextPathRel.toP87
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (witness : NativeF55P86ContextPathRel first last f g) :
    NativeF55P87ClosedPathRel first last f g :=
  .old witness

/-- Exact functor on original objects: OLD P84 path quotient
to NEW P86 path quotient, justified by witness inclusion. -/
def nativeF55P86ToP87ClosedPath
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55P86ContextPathCategory first last ⥤
      NativeF55P87ClosedPathCategory first last :=
  CategoryTheory.Quotient.lift
    (nativeF55P86ContextHomRel first last)
    (nativeF55P87ClosedQuotientFunctor first last)
    (by
      intro r s f g h
      exact (nativeF55P87ClosedQuotient_map_eq_iff first last f g).2
        (NativeF55P86ContextPathRel.toP87 h))

/-- Original source F55 raw paths commute strictly through the
P84-to-P86 selected quotient comparison functor. -/
theorem nativeF55P86ToP87ClosedPath_factor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeF55P86ContextQuotientFunctor first last ⋙
      nativeF55P86ToP87ClosedPath first last =
      nativeF55P87ClosedQuotientFunctor first last := by
  exact CategoryTheory.Quotient.lift_spec
    (nativeF55P86ContextHomRel first last)
    (nativeF55P87ClosedQuotientFunctor first last)
    (by
      intro r s f g h
      exact (nativeF55P87ClosedQuotient_map_eq_iff first last f g).2
        (NativeF55P86ContextPathRel.toP87 h))


/-- Original F54 route objects are not identified by taking
the selected P87 hom congruence. The quotient only modifies
the morphism comparisons, never original route objects. -/
theorem nativeF55P87ClosedQuotient_obj_injective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Injective
      (nativeF55P87ClosedQuotientFunctor first last).obj := by
  intro u v h
  exact congrArg
    (fun z : NativeF55P87ClosedPathCategory first last => z.as) h

#print axioms NativeF55P87ClosedPathRel
#print axioms NativeF55P87ClosedPathRel.shadow_sound
#print axioms nativeF55P87ClosedPathRel_equivalence
#print axioms nativeF55P87ClosedHomRel
#print axioms nativeF55P87ClosedCongruence
#print axioms NativeF55P87ClosedPathCategory
#print axioms nativeF55P87ClosedQuotientFunctor
#print axioms nativeF55P87ClosedQuotient_map_eq_iff
#print axioms nativeF55P87ClosedToShadow
#print axioms nativeF55P87Closed_shadow_factor
#print axioms NativeF55P86ContextPathRel.toP87
#print axioms nativeF55P86ToP87ClosedPath
#print axioms nativeF55P86ToP87ClosedPath_factor
#print axioms nativeF55P87ClosedQuotient_obj_injective

end
end Kuu.F112.Physical
