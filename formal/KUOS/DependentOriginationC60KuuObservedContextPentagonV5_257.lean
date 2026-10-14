import KUOS.DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256

namespace KUOS.DependentOriginationC60KuuObservedContextPentagonV5_257

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252
open KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253
open KUOS.DependentOriginationC60KuuTwoSidedContextCoherenceV5_254
open KUOS.DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255
open KUOS.DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.257 / F103 — Kuu observed context pentagon and higher coherence

No Gray restoration. We preserve genuine typed C60 paths, genuine F95
local quotient Hom categories, and both independent Int × Int charges.

The first result is a universal, proof-relevant criterion: in the TRUE
F77 quotient, between two fixed observable functors there is AT MOST
ONE natural transformation with zero *additional* integer charge at
every source object. We use this not as an assumption that source
charges vanish, but as a theorem from F77 quotient Hom extensionality.

We then construct actual F99 context-observation comparison NatIsos
for arbitrarily different C60 prefix paths with the SAME typed ends.
These comparisons are transitive as actual natural transformations.

Four real successive C60 contexts have five actual path brackets,
forming Mac Lane's pentagon. The two perimeter composites of the
five genuine observation NatIsos agree in the functor category.
We also prove true three-step sequential F99 whiskering is naturally
equivalent, after F77 observation, to single bundled path whiskering.

Finally, the F102 four-input context/interchange square has a
higher universal property: ANY zero-additional-charge natural
transformation between its opposite observed corners agrees with
BOTH existing F102 exchange/context routes.

These are observer-side coherence theorems, NOT unquotiented F42
presentation equalities, F55 curvature cancellation, or unrestricted
finite-atlas global descent.
-/

/-! ## I. Uniqueness of zero-charge comparison 2-cells in F77 -/

universe u v

/-- F77 local Hom extensionality makes every zero-additional-charge
natural transformation UNIQUE for a fixed source and target FUNCTOR.
This is a genuine functor-category theorem for arbitrary source C. -/
theorem c60F103ZeroChargeNatTrans_unique
    {C : Type u} [Category.{v} C]
    {F G : C ⥤ C60F77NativeQuotient}
    (α β : F ⟶ G)
    (hα : ∀ X, (c60F77QuotientToStrictCharge.map (α.app X)).charge =
      (0 : Int × Int))
    (hβ : ∀ X, (c60F77QuotientToStrictCharge.map (β.app X)).charge =
      (0 : Int × Int)) :
    α = β := by
  ext X
  apply c60F80QuotientThree_ext
  exact (hα X).trans (hβ X).symm

/-! ## II. Genuine original C60 path contexts and their observer comparison -/

/-- Actual left whiskering on the true F95 local quotient category,
followed by its correctly path-indexed F77 observation. -/
def c60F103LeftObserved
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    (p q : Quiver.Path b c) :
    C60F95LocalKuuQuotient p q ⥤ C60F77NativeQuotient :=
  c60F99LeftWhiskerFunctor prior ⋙
    c60F95DescendedToF77 (prior.comp p) (prior.comp q)

theorem c60F103LeftObserved_object
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q) :
    (c60F103LeftObserved prior p q).obj X =
      (c60F95DescendedToF77 p q).obj X :=
  c60F99LeftWhisker_object_obs prior X

theorem c60F103LeftObserved_charge
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F103LeftObserved prior p q).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge :=
  c60F99LeftWhisker_charge_obs prior f

/-- Two possibly DIFFERENT original C60 context paths with the same
typed endpoints give the same F77 observable object. Raw original
F42 whiskered objects are NOT asserted equal. -/
theorem c60F103LeftCompare_object
    {a b c : IcosahedralDart}
    (prior₁ prior₂ : Quiver.Path a b)
    (p q : Quiver.Path b c)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F103LeftObserved prior₁ p q).obj X =
      (c60F103LeftObserved prior₂ p q).obj X := by
  exact (c60F103LeftObserved_object prior₁ X).trans
    (c60F103LeftObserved_object prior₂ X).symm

theorem c60F103LeftCompare_charge
    {a b c : IcosahedralDart}
    (prior₁ prior₂ : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F103LeftObserved prior₁ p q).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F103LeftObserved prior₂ p q).map f)).charge := by
  exact (c60F103LeftObserved_charge prior₁ f).trans
    (c60F103LeftObserved_charge prior₂ f).symm

/-- Genuine Mathlib NatIso of differently presented original C60
left-whiskering contexts, defined after the F95-to-F77 descent. -/
def c60F103LeftContextCompare
    {a b c : IcosahedralDart}
    (prior₁ prior₂ : Quiver.Path a b)
    (p q : Quiver.Path b c) :
    c60F103LeftObserved prior₁ p q ≅
      c60F103LeftObserved prior₂ p q :=
  NatIso.ofComponents
    (fun X => eqToIso (c60F103LeftCompare_object prior₁ prior₂ p q X))
    (by
      intro X Y f
      change
        (c60F103LeftObserved prior₁ p q).map f ≫
            eqToHom (c60F103LeftCompare_object prior₁ prior₂ p q Y) =
          eqToHom (c60F103LeftCompare_object prior₁ prior₂ p q X) ≫
            (c60F103LeftObserved prior₂ p q).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F103LeftCompare_charge prior₁ prior₂ f)

/-- In a Kuu observation comparison the ADDED charge is zero,
but the input source morphism charges are arbitrary. -/
theorem c60F103LeftContextCompare_charge_zero
    {a b c : IcosahedralDart}
    (prior₁ prior₂ : Quiver.Path a b)
    (p q : Quiver.Path b c)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F77QuotientToStrictCharge.map
      ((c60F103LeftContextCompare prior₁ prior₂ p q).hom.app X)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F103LeftCompare_object prior₁ prior₂ p q X))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-- Higher composition law: choosing an intermediate C60
presentation/path does not change the natural comparison.
The equality is IN the functor category, not of raw F42 words. -/
theorem c60F103LeftContextCompare_trans
    {a b c : IcosahedralDart}
    (prior₁ prior₂ prior₃ : Quiver.Path a b)
    (p q : Quiver.Path b c) :
    (c60F103LeftContextCompare prior₁ prior₂ p q).hom ≫
      (c60F103LeftContextCompare prior₂ prior₃ p q).hom =
        (c60F103LeftContextCompare prior₁ prior₃ p q).hom := by
  apply c60F103ZeroChargeNatTrans_unique
  · intro X
    change
      (c60F77QuotientToStrictCharge.map
        (eqToHom (c60F103LeftCompare_object prior₁ prior₂ p q X) ≫
         eqToHom (c60F103LeftCompare_object prior₂ prior₃ p q X))).charge =
        (0 : Int × Int)
    simp only [c60F80QuotientThree_comp_charge,
      c60F82Quotient_eqToHom_charge_zero, zero_add]
  · intro X
    exact c60F103LeftContextCompare_charge_zero prior₁ prior₃ p q X

/-! ## III. Real C60 four-path bracketings and observed pentagon -/

/-- (((A·B)·C)·D), the first authentic C60 path bracketing. -/
def c60F103PentagonPath0
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    Quiver.Path a e := ((A.comp B).comp C).comp D

/-- ((A·(B·C))·D), second genuine path bracketing. -/
def c60F103PentagonPath1
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    Quiver.Path a e := (A.comp (B.comp C)).comp D

/-- A·((B·C)·D), third genuine path bracketing. -/
def c60F103PentagonPath2
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    Quiver.Path a e := A.comp ((B.comp C).comp D)

/-- A·(B·(C·D)), fourth genuine path bracketing. -/
def c60F103PentagonPath3
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    Quiver.Path a e := A.comp (B.comp (C.comp D))

/-- (A·B)·(C·D), fifth genuine path bracketing. -/
def c60F103PentagonPath4
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    Quiver.Path a e := (A.comp B).comp (C.comp D)

/-- The REAL C60 path boundaries themselves are associative.
This never asserts equality of corresponding original F42 objects. -/
theorem c60F103PentagonPath_assoc
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e) :
    c60F103PentagonPath0 A B C D =
      c60F103PentagonPath3 A B C D := by
  unfold c60F103PentagonPath0 c60F103PentagonPath3
  simp only [Quiver.Path.comp_assoc]

/-- The three-edge upper route through four of the five actual
C60 path presentations, as a true natural transformation in F77. -/
def c60F103ObservedPentagonUpper
    {a b c d e f : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e)
    (p q : Quiver.Path e f) :
    c60F103LeftObserved (c60F103PentagonPath0 A B C D) p q ⟶
      c60F103LeftObserved (c60F103PentagonPath3 A B C D) p q :=
  ((c60F103LeftContextCompare
      (c60F103PentagonPath0 A B C D)
      (c60F103PentagonPath1 A B C D) p q).hom ≫
    (c60F103LeftContextCompare
      (c60F103PentagonPath1 A B C D)
      (c60F103PentagonPath2 A B C D) p q).hom) ≫
    (c60F103LeftContextCompare
      (c60F103PentagonPath2 A B C D)
      (c60F103PentagonPath3 A B C D) p q).hom

/-- Two-edge lower route through the remaining real C60
bracketing, also an actual F77 natural transformation. -/
def c60F103ObservedPentagonLower
    {a b c d e f : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e)
    (p q : Quiver.Path e f) :
    c60F103LeftObserved (c60F103PentagonPath0 A B C D) p q ⟶
      c60F103LeftObserved (c60F103PentagonPath3 A B C D) p q :=
  (c60F103LeftContextCompare
    (c60F103PentagonPath0 A B C D)
    (c60F103PentagonPath4 A B C D) p q).hom ≫
    (c60F103LeftContextCompare
      (c60F103PentagonPath4 A B C D)
      (c60F103PentagonPath3 A B C D) p q).hom

/-- THE OBSERVED PENTAGON: both actual C60 path-associator
comparison routes AGREE AS MATHLIB NATURAL TRANSFORMATIONS.
The result is a coherence of F77 observations, not a lifting
claim for all original F42/Gray associators. -/
theorem c60F103ObservedPentagon_natTrans
    {a b c d e f : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (D : Quiver.Path d e)
    (p q : Quiver.Path e f) :
    c60F103ObservedPentagonUpper A B C D p q =
      c60F103ObservedPentagonLower A B C D p q := by
  unfold c60F103ObservedPentagonUpper c60F103ObservedPentagonLower
  rw [c60F103LeftContextCompare_trans
    (c60F103PentagonPath0 A B C D)
    (c60F103PentagonPath1 A B C D)
    (c60F103PentagonPath2 A B C D) p q]
  rw [c60F103LeftContextCompare_trans
    (c60F103PentagonPath0 A B C D)
    (c60F103PentagonPath2 A B C D)
    (c60F103PentagonPath3 A B C D) p q]
  exact (c60F103LeftContextCompare_trans
    (c60F103PentagonPath0 A B C D)
    (c60F103PentagonPath4 A B C D)
    (c60F103PentagonPath3 A B C D) p q).symm

/-! ## IV. Actual three-step original quotient whiskering -/

/-- Three SUCCESSIVE genuine F99 C60 path contexts, not a single
unmotivated grade reassignment. Each functor acts on full F95 Hom. -/
def c60F103TripleSequentialObserved
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (p q : Quiver.Path d e) :
    C60F95LocalKuuQuotient p q ⥤ C60F77NativeQuotient :=
  ((c60F99LeftWhiskerFunctor C ⋙
      c60F99LeftWhiskerFunctor B) ⋙
      c60F99LeftWhiskerFunctor A) ⋙
      c60F95DescendedToF77
        (A.comp (B.comp (C.comp p)))
        (A.comp (B.comp (C.comp q)))

/-- A single bundled original C60 path, with an alternative
proof-relevant F42 whiskering presentation. -/
def c60F103TripleBundledObserved
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (p q : Quiver.Path d e) :
    C60F95LocalKuuQuotient p q ⥤ C60F77NativeQuotient :=
  c60F103LeftObserved ((A.comp B).comp C) p q

theorem c60F103TripleSequential_object
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d)
    {p q : Quiver.Path d e}
    (X : C60F95LocalKuuQuotient p q) :
    (c60F103TripleSequentialObserved A B C p q).obj X =
      (c60F95DescendedToF77 p q).obj X := by
  change
    (c60F95DescendedToF77
      (A.comp (B.comp (C.comp p)))
      (A.comp (B.comp (C.comp q)))).obj
      ((c60F99LeftWhiskerFunctor A).obj
        ((c60F99LeftWhiskerFunctor B).obj
          ((c60F99LeftWhiskerFunctor C).obj X))) =
      (c60F95DescendedToF77 p q).obj X
  exact
    (c60F99LeftWhisker_object_obs A
      ((c60F99LeftWhiskerFunctor B).obj
        ((c60F99LeftWhiskerFunctor C).obj X))).trans
      ((c60F99LeftWhisker_object_obs B
        ((c60F99LeftWhiskerFunctor C).obj X)).trans
        (c60F99LeftWhisker_object_obs C X))

theorem c60F103TripleSequential_charge
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d)
    {p q : Quiver.Path d e}
    {X Y : C60F95LocalKuuQuotient p q} (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F103TripleSequentialObserved A B C p q).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77
        (A.comp (B.comp (C.comp p)))
        (A.comp (B.comp (C.comp q)))).map
        ((c60F99LeftWhiskerFunctor A).map
          ((c60F99LeftWhiskerFunctor B).map
            ((c60F99LeftWhiskerFunctor C).map f))))).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge
  exact
    (c60F99LeftWhisker_charge_obs A
      ((c60F99LeftWhiskerFunctor B).map
        ((c60F99LeftWhiskerFunctor C).map f))).trans
      ((c60F99LeftWhisker_charge_obs B
        ((c60F99LeftWhiskerFunctor C).map f)).trans
        (c60F99LeftWhisker_charge_obs C f))

/-- Observable triple-context associativity of ACTUAL sequential
F95 quotient functors versus one bundled path context. -/
def c60F103TripleSequentialBundledNatIso
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (p q : Quiver.Path d e) :
    c60F103TripleSequentialObserved A B C p q ≅
      c60F103TripleBundledObserved A B C p q :=
  NatIso.ofComponents
    (fun X => eqToIso
      ((c60F103TripleSequential_object A B C X).trans
        (c60F103LeftObserved_object ((A.comp B).comp C) X).symm))
    (by
      intro X Y f
      change
        (c60F103TripleSequentialObserved A B C p q).map f ≫
          eqToHom
            ((c60F103TripleSequential_object A B C Y).trans
              (c60F103LeftObserved_object ((A.comp B).comp C) Y).symm) =
        eqToHom
            ((c60F103TripleSequential_object A B C X).trans
              (c60F103LeftObserved_object ((A.comp B).comp C) X).symm) ≫
          (c60F103TripleBundledObserved A B C p q).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero]
      change
        (c60F77QuotientToStrictCharge.map
          ((c60F103TripleSequentialObserved A B C p q).map f)).charge =
        (c60F77QuotientToStrictCharge.map
          ((c60F103LeftObserved ((A.comp B).comp C) p q).map f)).charge
      exact (c60F103TripleSequential_charge A B C f).trans
        (c60F103LeftObserved_charge ((A.comp B).comp C) f).symm)

/-- Comparing three successive contexts to one bundled context
introduces no added integer charge at any original F95 object. -/
theorem c60F103TripleSequentialBundledNatIso_charge_zero
    {a b c d e : IcosahedralDart}
    (A : Quiver.Path a b) (B : Quiver.Path b c)
    (C : Quiver.Path c d) (p q : Quiver.Path d e)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F77QuotientToStrictCharge.map
      ((c60F103TripleSequentialBundledNatIso A B C p q).hom.app X)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom
        ((c60F103TripleSequential_object A B C X).trans
          (c60F103LeftObserved_object ((A.comp B).comp C) X).symm))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-! ## V. F102 four-input exchange square: higher uniqueness -/

/-- F102's H-after-V context-order comparison is itself a genuine
zero-additional-charge F77 morphism for every four-input object. -/
theorem c60F103F102HVOrder_charge_zero
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F77QuotientToStrictCharge.map
      ((c60F102HVOrderNatIso
        prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom
        (c60F102HVOrder_object_eq
          prior p q r bridgeOut bridgeIn s t u suffix Z))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-- Universal F102 higher-coherence certificate: every conceivable
ADDITIONAL zero-charge natural comparison from LR-HV to RL-VH is
already the verified F102 two-edge route. The criterion is
conditional on the given comparison having zero added charge. -/
theorem c60F103F102ZeroChargeRoute_unique
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (θ :
      c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix ⟶
        c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix)
    (hθ : ∀ Z,
      (c60F77QuotientToStrictCharge.map (θ.app Z)).charge =
        (0 : Int × Int)) :
    θ =
      (c60F102HVOrderNatIso
        prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
        (c60F102RLMixedNatIso
          prior p q r bridgeOut bridgeIn s t u suffix).hom := by
  apply c60F103ZeroChargeNatTrans_unique θ _
  · exact hθ
  · intro Z
    change
      (c60F77QuotientToStrictCharge.map
        ((c60F102HVOrderNatIso
          prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z ≫
          (c60F102RLMixedNatIso
            prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z)).charge =
        (0 : Int × Int)
    simp only [c60F80QuotientThree_comp_charge,
      c60F103F102HVOrder_charge_zero,
      c60F102RLMixedNatIso_charge_zero, zero_add]

/-- The same arbitrary zero-added-charge comparison must ALSO
coincide with the other F102 route, by its independently proved
mixed-exchange/context-order natural-transformation square. -/
theorem c60F103F102ZeroChargeRoute_second
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (θ :
      c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix ⟶
        c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix)
    (hθ : ∀ Z,
      (c60F77QuotientToStrictCharge.map (θ.app Z)).charge =
        (0 : Int × Int)) :
    θ =
      (c60F102LRMixedNatIso
        prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
        (c60F102VHOrderNatIso
          prior p q r bridgeOut bridgeIn s t u suffix).hom := by
  calc
    θ =
        (c60F102HVOrderNatIso
          prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
          (c60F102RLMixedNatIso
            prior p q r bridgeOut bridgeIn s t u suffix).hom :=
      c60F103F102ZeroChargeRoute_unique
        prior p q r bridgeOut bridgeIn s t u suffix θ hθ
    _ =
        (c60F102LRMixedNatIso
          prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
          (c60F102VHOrderNatIso
            prior p q r bridgeOut bridgeIn s t u suffix).hom :=
      c60F102OrderMixedSquare_natTrans
        prior p q r bridgeOut bridgeIn s t u suffix

#print axioms c60F103ZeroChargeNatTrans_unique
#print axioms c60F103LeftContextCompare
#print axioms c60F103LeftContextCompare_charge_zero
#print axioms c60F103LeftContextCompare_trans
#print axioms c60F103PentagonPath_assoc
#print axioms c60F103ObservedPentagonUpper
#print axioms c60F103ObservedPentagonLower
#print axioms c60F103ObservedPentagon_natTrans
#print axioms c60F103TripleSequential_object
#print axioms c60F103TripleSequential_charge
#print axioms c60F103TripleSequentialBundledNatIso
#print axioms c60F103TripleSequentialBundledNatIso_charge_zero
#print axioms c60F103F102HVOrder_charge_zero
#print axioms c60F103F102ZeroChargeRoute_unique
#print axioms c60F103F102ZeroChargeRoute_second

end
end KUOS.DependentOriginationC60KuuObservedContextPentagonV5_257
