import Kuu.F112.PolygonNativeF55P84HorizontalFourCellP85
import Mathlib.CategoryTheory.Quotient

/-!
# F112-P86A — P85-witness-closed contextual path presentation

P85 proves source Type-valued 4-cell soundness for the selected
P84 path congruence but does NOT prove the chosen P84 relation
is stable under all original F55 contexts and route operations.
Do not silently assert those missing path equalities.

We therefore keep P84 unchanged and introduce a DIFFERENT, explicitly
typed proof-generated P86 path congruence. In addition to an OLD
P84 comparison and the categorical equivalence/vertical composition
constructors, genuinely new rules apply an actual P85 Type-valued
4-cell witness through original left/right binary contexts, original
pre/post F54 route whiskering, and original left/right F55 horizontal
composition by a second raw proof. They do not equate same-shadow
histories by fiat. Original raw P59 paths remain available.

Every selected P86 path comparison preserves the exact ORIGINAL
F55 three-coordinate full shadow. A Mathlib Congruence, strict local
quotient Category, exact kernel and shadow factorization follow.
An explicit P84 quotient-to-P86 quotient comparison functor preserves
the original path images. This is a selected presentation, NOT a
completed 3-interchange or global strict 3/n-category.

No Gray, sorry/admit, new axioms, or removed old public roots.
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

/-- Genuine new typed path relation. The six action constructors
carry ACTUAL Type-valued P85 original-source 4-cell proof witnesses:
two contexts, two F54 route actions and two F55 horizontal whiskers. -/
inductive NativeF55P86ContextPathRel
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
      (witness : NativeF55P84HorizontalPathRel first last f g) :
      NativeF55P86ContextPathRel first last f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      (f : Quiver.Path r s) :
      NativeF55P86ContextPathRel first last f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g : Quiver.Path r s}
      (witness : NativeF55P86ContextPathRel first last f g) :
      NativeF55P86ContextPathRel first last g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g h : Quiver.Path r s}
      (fg : NativeF55P86ContextPathRel first last f g)
      (gh : NativeF55P86ContextPathRel first last g h) :
      NativeF55P86ContextPathRel first last f h
  | comp

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : NativeF55RawRouteVertex first last}
      {f f' : Quiver.Path r s}
      {g g' : Quiver.Path s t}
      (hf : NativeF55P86ContextPathRel first last f f')
      (hg : NativeF55P86ContextPathRel first last g g') :
      NativeF55P86ContextPathRel first last (f.comp g) (f'.comp g')
  | leftContext

      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P85HorizontalFourCell f g)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P86ContextPathRel
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later)
        (.leftContext f later).toNativeStrictPath
        (.leftContext g later).toNativeStrictPath
  | rightContext

      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (witness : NativeF55P85HorizontalFourCell f g) :
      NativeF55P86ContextPathRel
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last)
        (.rightContext earlier f).toNativeStrictPath
        (.rightContext earlier g).toNativeStrictPath
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
      (witness : NativeF55P85HorizontalFourCell f g) :
      NativeF55P86ContextPathRel first last
        (.precompose prior f).toNativeStrictPath
        (.precompose prior g).toNativeStrictPath
  | postcompose

      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
      {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
      {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (witness : NativeF55P85HorizontalFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
      NativeF55P86ContextPathRel first last
        (.postcompose f suffix).toNativeStrictPath
        (.postcompose g suffix).toNativeStrictPath
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
      (witness : NativeF55P85HorizontalFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P86ContextPathRel
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
      (witness : NativeF55P85HorizontalFourCell g g') :
      NativeF55P86ContextPathRel
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)
        (f.horizontal g).toNativeStrictPath
        (f.horizontal g').toNativeStrictPath

/-- Full original shadow preservation is a theorem about ALL
eleven P86 path rules. Neither P85 four-cell proof existence nor
P86 path comparison is DEFINED by numerical shadow equality. -/
theorem NativeF55P86ContextPathRel.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (h : NativeF55P86ContextPathRel first last f g) :
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
theorem nativeF55P86ContextPathRel_equivalence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : NativeF55RawRouteVertex first last) :
    Equivalence (NativeF55P86ContextPathRel first last (r := r) (s := s)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro f; exact .refl f
  · intro f g h; exact .symm h
  · intro f g h hfg hgh; exact .trans hfg hgh

/-- The P86 proof-generated relation, not a scalar-kernel proxy. -/
def nativeF55P86ContextHomRel
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    HomRel (NativeF55RawPathCategory first last) :=
  fun {_r _s} f g => NativeF55P86ContextPathRel first last f g

/-- Congruence on each original typed P59 path Hom, supplied
directly by actual P86 evidence on both vertical operands. -/
instance nativeF55P86ContextCongruence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    CategoryTheory.Congruence (nativeF55P86ContextHomRel first last) where
  equivalence := by
    intro r s
    exact nativeF55P86ContextPathRel_equivalence first last r s
  comp_left := by
    intro r s t f g g' h
    exact .comp (.refl f) h
  comp_right := by
    intro r s t f f' g h
    exact .comp h (.refl g)

/-- A strict LOCAL Mathlib category of the original F54 route
vertices, preserving original raw F55 proof-labelled free paths. -/
abbrev NativeF55P86ContextPathCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  CategoryTheory.Quotient (nativeF55P86ContextHomRel first last)

/-- Universal original-path projection into the precisely selected
P86 path quotient category, with all F54 route objects retained. -/
def nativeF55P86ContextQuotientFunctor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55RawPathCategory first last ⥤
      NativeF55P86ContextPathCategory first last :=
  CategoryTheory.Quotient.functor (nativeF55P86ContextHomRel first last)

/-- EXACT kernel: quotient equality IFF one original-source
P86 proof-generated path comparison exists. -/
theorem nativeF55P86ContextQuotient_map_eq_iff
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : NativeF55RawRouteVertex first last}
    (f g : Quiver.Path r s) :
    (nativeF55P86ContextQuotientFunctor first last).map f =
      (nativeF55P86ContextQuotientFunctor first last).map g ↔
      NativeF55P86ContextPathRel first last f g := by
  exact CategoryTheory.Quotient.functor_map_eq_iff
    (nativeF55P86ContextHomRel first last) f g

/-- Old full signed-charge and independent parity observer factors
through P86 exactly. This factorization is justified by proofs. -/
def nativeF55P86ContextToShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55P86ContextPathCategory first last ⥤
      (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  CategoryTheory.Quotient.lift
    (nativeF55P86ContextHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P86ContextPathRel.shadow_sound h)

/-- Exact commuting triangle original raw path -> P86 -> full shadow. -/
theorem nativeF55P86Context_shadow_factor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeF55P86ContextQuotientFunctor first last ⋙
      nativeF55P86ContextToShadow first last =
      nativeF55RawPathsToShadow first last := by
  exact CategoryTheory.Quotient.lift_spec
    (nativeF55P86ContextHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P86ContextPathRel.shadow_sound h)

/-- The old exact P84 path relation embeds without rewriting
any old path or erasing its witnesses. -/
theorem NativeF55P84HorizontalPathRel.toP86
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (witness : NativeF55P84HorizontalPathRel first last f g) :
    NativeF55P86ContextPathRel first last f g :=
  .old witness

/-- Exact functor on original objects: OLD P84 path quotient
to NEW P86 path quotient, justified by witness inclusion. -/
def nativeF55P84ToP86Context
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55P84HorizontalCategory first last ⥤
      NativeF55P86ContextPathCategory first last :=
  CategoryTheory.Quotient.lift
    (nativeF55P84HorizontalHomRel first last)
    (nativeF55P86ContextQuotientFunctor first last)
    (by
      intro r s f g h
      exact (nativeF55P86ContextQuotient_map_eq_iff first last f g).2
        (NativeF55P84HorizontalPathRel.toP86 h))

/-- Original source F55 raw paths commute strictly through the
P84-to-P86 selected quotient comparison functor. -/
theorem nativeF55P84ToP86Context_factor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeF55P84HorizontalQuotientFunctor first last ⋙
      nativeF55P84ToP86Context first last =
      nativeF55P86ContextQuotientFunctor first last := by
  exact CategoryTheory.Quotient.lift_spec
    (nativeF55P84HorizontalHomRel first last)
    (nativeF55P86ContextQuotientFunctor first last)
    (by
      intro r s f g h
      exact (nativeF55P86ContextQuotient_map_eq_iff first last f g).2
        (NativeF55P84HorizontalPathRel.toP86 h))

#print axioms NativeF55P86ContextPathRel
#print axioms NativeF55P86ContextPathRel.shadow_sound
#print axioms nativeF55P86ContextPathRel_equivalence
#print axioms nativeF55P86ContextHomRel
#print axioms nativeF55P86ContextCongruence
#print axioms NativeF55P86ContextPathCategory
#print axioms nativeF55P86ContextQuotientFunctor
#print axioms nativeF55P86ContextQuotient_map_eq_iff
#print axioms nativeF55P86ContextToShadow
#print axioms nativeF55P86Context_shadow_factor
#print axioms NativeF55P84HorizontalPathRel.toP86
#print axioms nativeF55P84ToP86Context
#print axioms nativeF55P84ToP86Context_factor

end
end Kuu.F112.Physical
