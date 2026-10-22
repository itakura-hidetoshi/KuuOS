import Kuu.F112.PolygonNativeF55P62HorizontalContextObstructionP83
import Mathlib.CategoryTheory.Quotient

/-!
# F112-P84 — a distinct horizontal-source-witness path-congruence presentation

P82 certifies that original F55 horizontal composition does NOT descend
to P80's original selected Type-valued 4-cell quotient. P83 further
certifies that the missing comparison fails P62's original unit-only
free-path relation. Neither theorem is erased.

We now construct a NEW, separately labelled relation on the ORIGINAL
typed P59 F55 free paths. Its generating syntax is:
* actual old P62 path witnesses, explicitly embedded;
* reflexivity, symmetry, transitivity and vertical path compatibility;
* one-step left/right horizontal application of ANY genuine Type-valued
  P80 4-cell witness against any original parallel F55 raw 3-proof.

Unlike defining equality by numerical shadow agreement, the extra
generators carry the ACTUAL P80 source four-cell proof as a constructor
argument. Original raw proof histories and old P62/P80 syntax survive.

We prove the selected full F55 shadow is preserved by EVERY rule,
construct the strict local Mathlib quotient CATEGORY with its EXACT
source-witness kernel and source-to-shadow factorization, and show the
chosen new relation is STRICTLY more permissive than P62 on an actual
north C60 pentagon. This precisely repairs P83's necessary path-level
obstruction without falsely claiming that existing P62 permitted it.

We do NOT yet construct a new Type-valued 4-cell category, full
horizontal bifunctoriality, interchange, context transport coherence,
global strict 3/n or (∞,3)-hyperdescent. No Gray, sorry, admit or
new axioms; 107 legacy public roots and the pre-C60 general theory stay.
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

/-- The LEAST explicitly generated typed path relation extending
P62 by horizontal whiskering of GENUINE P80 source 4-cell evidence.
No arbitrary same-shadow path pair is an elementary constructor. -/
inductive NativeF55P84HorizontalPathRel
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
      (h : NativeF55UnitPathRel first last f g) :
      NativeF55P84HorizontalPathRel first last f g
  | refl

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      (f : Quiver.Path r s) :
      NativeF55P84HorizontalPathRel first last f f
  | symm

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g : Quiver.Path r s}
      (h : NativeF55P84HorizontalPathRel first last f g) :
      NativeF55P84HorizontalPathRel first last g f
  | trans

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : NativeF55RawRouteVertex first last}
      {f g h : Quiver.Path r s}
      (hfg : NativeF55P84HorizontalPathRel first last f g)
      (hgh : NativeF55P84HorizontalPathRel first last g h) :
      NativeF55P84HorizontalPathRel first last f h
  | comp

      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : NativeF55RawRouteVertex first last}
      {f f' : Quiver.Path r s}
      {g g' : Quiver.Path s t}
      (hf : NativeF55P84HorizontalPathRel first last f f')
      (hg : NativeF55P84HorizontalPathRel first last g g') :
      NativeF55P84HorizontalPathRel first last
        (f.comp g) (f'.comp g')
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
      (witness : NativeF55P80UnitFourCell f f')
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
      NativeF55P84HorizontalPathRel
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
      (witness : NativeF55P80UnitFourCell g g') :
      NativeF55P84HorizontalPathRel
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)
        (f.horizontal g).toNativeStrictPath
        (f.horizontal g').toNativeStrictPath

/-- This is a genuine equivalence on every dependent raw free-path
Hom, using exactly the generators of the displayed syntax. -/
theorem nativeF55P84HorizontalPathRel_equivalence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : NativeF55RawRouteVertex first last) :
    Equivalence (NativeF55P84HorizontalPathRel first last
      (r := r) (s := s)) := by
  refine ⟨?_, ?_, ?_⟩
  · intro f
    exact .refl f
  · intro f g h
    exact .symm h
  · intro f g h hfg hgh
    exact .trans hfg hgh

/-- Every proof of equality in P62's OLD independently generated
structural-unit relation yields a chosen NEW P84 witness. -/
theorem NativeF55UnitPathRel.toP84
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (h : NativeF55UnitPathRel first last f g) :
    NativeF55P84HorizontalPathRel first last f g :=
  .old h

/-- Full chosen (Int × Int) × ZMod 2 F55 shadow is preserved by
ALL seven constructors of the distinctly selected P84 path relation.
The two horizontal cases are justified by actual Type-valued P80
source witnesses and source shadow additivity, NOT shadow kernels. -/
theorem NativeF55P84HorizontalPathRel.shadow_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (h : NativeF55P84HorizontalPathRel first last f g) :
    (nativeF55RawPathsToShadow first last).map f =
      (nativeF55RawPathsToShadow first last).map g := by
  induction h with
  | old witness => exact witness.shadow_sound
  | refl path => rfl
  | symm witness ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | comp hf hg ihf ihg =>
      calc
        _ = nativeF55ThreeComp _ _ :=
          nativeF55RawPathsToShadow_mapTypedComp _ _ _ _
        _ = nativeF55ThreeComp _ _ := by rw [ihf, ihg]
        _ = _ :=
          (nativeF55RawPathsToShadow_mapTypedComp _ _ _ _).symm
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

/-- Mathlib HomRel for EXACTLY the new proof-generated P84 path
relation, not equality of selected numerical receiver values. -/
def nativeF55P84HorizontalHomRel
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    HomRel (NativeF55RawPathCategory first last) :=
  fun {_r _s} f g => NativeF55P84HorizontalPathRel first last f g

/-- The explicit selected P84 relation is a categorical congruence:
P62 inclusion and horizontal four-cell generators respect the
vertical-category associativity and both whiskerings. -/
instance nativeF55P84HorizontalCongruence
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    CategoryTheory.Congruence (nativeF55P84HorizontalHomRel first last) where
  equivalence := by
    intro r s
    exact nativeF55P84HorizontalPathRel_equivalence first last r s
  comp_left := by
    intro r s t f g g' h
    exact .comp (.refl f) h
  comp_right := by
    intro r s t f f' g h
    exact .comp h (.refl g)

/-- A strict local Mathlib quotient category on the SAME original
F54 objects and original F55 proof-labelled free paths, but with
the NEW P84 horizontal-evidence relation as its exact Hom kernel. -/
abbrev NativeF55P84HorizontalCategory
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  CategoryTheory.Quotient (nativeF55P84HorizontalHomRel first last)

/-- The new quotient functor keeps the original typed F54 objects
unchanged and carries every raw proof-labelled F55 path to its class. -/
def nativeF55P84HorizontalQuotientFunctor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55RawPathCategory first last ⥤
      NativeF55P84HorizontalCategory first last :=
  CategoryTheory.Quotient.functor (nativeF55P84HorizontalHomRel first last)

/-- EXACT source-witness kernel: P84 quotient equality holds IFF
there is a recursively generated typed P84 path comparison.
A mere coincidence of full F55 shadows is insufficient. -/
theorem nativeF55P84HorizontalQuotient_map_eq_iff
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : NativeF55RawRouteVertex first last}
    (f g : Quiver.Path r s) :
    (nativeF55P84HorizontalQuotientFunctor first last).map f =
      (nativeF55P84HorizontalQuotientFunctor first last).map g ↔
      NativeF55P84HorizontalPathRel first last f g := by
  exact CategoryTheory.Quotient.functor_map_eq_iff
    (nativeF55P84HorizontalHomRel first last) f g

/-- The previously chosen FULL native F55 charge/phase observer
factors constructively through the new P84 path quotient, with the
actual new witness-preservation theorem as its descent evidence. -/
def nativeF55P84HorizontalToShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55P84HorizontalCategory first last ⥤
      (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  CategoryTheory.Quotient.lift
    (nativeF55P84HorizontalHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P84HorizontalPathRel.shadow_sound h)

/-- The original shadow functor factors on ALL typed raw paths.
No previously proved strict path equality is retroactively changed. -/
theorem nativeF55P84Horizontal_shadow_factor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeF55P84HorizontalQuotientFunctor first last ⋙
      nativeF55P84HorizontalToShadow first last =
      nativeF55RawPathsToShadow first last := by
  exact CategoryTheory.Quotient.lift_spec
    (nativeF55P84HorizontalHomRel first last)
    (nativeF55RawPathsToShadow first last)
    (by
      intro r s f g h
      exact NativeF55P84HorizontalPathRel.shadow_sound h)

/-- Every chosen genuine P80 four-cell certificate is now respected
as an ACTUAL new P84 path-level comparison after horizontal
application to any independent original raw 3-proof. -/
theorem nativeF55P84_horizontalLeft_related
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
    {f f' : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u'}
    (witness : NativeF55P80UnitFourCell f f')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    NativeF55P84HorizontalPathRel
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (f.horizontal g).toNativeStrictPath
      (f'.horizontal g).toNativeStrictPath :=
  .horizontalLeft witness g

/-- In particular the exact P83 counterexample becomes
related in THIS NEW presentation by the original P80 Type-valued
left-unit witness, while P83's proof of OLD-P62 nonrelatedness stands. -/
theorem nativeF55P84_oldLeftUnit_horizontal_related
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    NativeF55P84HorizontalPathRel
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident u) f).horizontal (.ident v)).toNativeStrictPath
      (f.horizontal (.ident v)).toNativeStrictPath := by
  rcases nativeF55P82_oldLeftUnit_witness f with ⟨h⟩
  exact .horizontalLeft h (.ident v)

/-- PHYSICAL north C60 specialization: a genuinely new P84 path
witness exists exactly where P83 proved that NO old P62 witness
can exist. This is strict enlargement of the selected presentation,
not elimination of the earlier obstruction theorem. -/
theorem northNativeP84_horizontal_related_but_not_P62 :
    NativeF55P84HorizontalPathRel
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon0
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon3
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath ∧
    ¬ NativeF55UnitPathRel
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon0
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon3
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath := by
  constructor
  · exact nativeF55P84_oldLeftUnit_horizontal_related
      northNativeF55PentagonCell northNativeP82RightUnitRoute
  · exact northNativeP83_horizontal_oldLeftUnit_not_P62

#print axioms NativeF55P84HorizontalPathRel
#print axioms nativeF55P84HorizontalPathRel_equivalence
#print axioms NativeF55UnitPathRel.toP84
#print axioms NativeF55P84HorizontalPathRel.shadow_sound
#print axioms nativeF55P84HorizontalHomRel
#print axioms nativeF55P84HorizontalCongruence
#print axioms NativeF55P84HorizontalCategory
#print axioms nativeF55P84HorizontalQuotientFunctor
#print axioms nativeF55P84HorizontalQuotient_map_eq_iff
#print axioms nativeF55P84HorizontalToShadow
#print axioms nativeF55P84Horizontal_shadow_factor
#print axioms nativeF55P84_horizontalLeft_related
#print axioms nativeF55P84_oldLeftUnit_horizontal_related
#print axioms northNativeP84_horizontal_related_but_not_P62

end
end Kuu.F112.Physical
