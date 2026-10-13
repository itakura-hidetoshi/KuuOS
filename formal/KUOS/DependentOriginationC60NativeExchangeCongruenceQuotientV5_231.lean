import KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
import Mathlib.CategoryTheory.Quotient

namespace KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.231 / F77 — the genuine Mathlib CATEGORY QUOTIENT by Gray exchange phase

F75 built the explicit integer-charge target and established that original
F42/F43 exchange has zero image. F76 proved the exact kernel and a strict
charge tensor with middle-four interchange. The present step constructs the
ACTUAL categorical quotient by the kernel congruence, rather than merely
naming the F75 target a quotient.

* The input is the original native GrayGrade CATEGORY of typed three-arrows.
* The congruence is equality of BOTH Int × Int charges, equivalently the
  kernel relation of the existing F75 phase-forgetting functor.
* Mathlib CategoryTheory.Quotient forms the generated congruence quotient.
  It comes with its FULL canonical projection and a UNIVERSAL LIFT.
* The independent phase-one generator at EVERY grade becomes an identity.
* Conversely, ANY functor killing those generators respects the COMPLETE
  charge congruence and factors UNIQUEly through this explicit quotient.
* The quotient maps to F75, is injective and surjective on all Hom-sets,
  and is surjective on degree-objects.
* The actual original F42/F43/F51 path-indexed source maps through the
  canonical quotient and then to F75, without changing its source theory.

Unlike a simple stipulation omega=1, this step supplies the categorical
universal property. The phase-killing quotient is a deliberate new theory:
the old north interchange still has nonzero phase before projection.
Independent Int × Int charge and north physical curvature are NOT killed.
The complete nondegenerate original F42/F54/F55 global strict 3-category
still requires further globular and mixed-boundary gluing.
-/

/-- Exact native congruence kernel of the phase-forgetting functor.
It is automatically a Mathlib Congruence: equivalence and both
composition-stability laws are obtained from an actual functor. -/
def c60F77ChargeKernel : HomRel GrayGrade :=
  c60F75ForgetGrayExchangePhase.homRel

/-- Explicit typeclass carrier: the kernel relation of a genuine
functor is a congruence, including stability under both compositions. -/
instance c60F77ChargeKernelCongruence : Congruence c60F77ChargeKernel := by
  change Congruence c60F75ForgetGrayExchangePhase.homRel
  infer_instance

/-- Relating two genuinely typed original native Gray three-arrows
in this congruence is EQUIVALENT to equality of BOTH integer charges. -/
theorem c60F77ChargeKernel_iff
    {X Y : GrayGrade} (f g : X ⟶ Y) :
    c60F77ChargeKernel f g ↔ f.charge = g.charge :=
  c60F76NativeQuotient_exactChargeKernel f g

/-- This is an ACTUAL Mathlib category quotient, whose Hom-sets are
quotients by the composition-compatible congruence closure, not a
hand-built charge-only category presented without a quotient. -/
abbrev C60F77NativeQuotient :=
  CategoryTheory.Quotient c60F77ChargeKernel

/-- Universally projecting the unmodified native Gray three-arrow
category into the genuine congruence quotient. -/
def c60F77Projection : GrayGrade ⥤ C60F77NativeQuotient :=
  CategoryTheory.Quotient.functor c60F77ChargeKernel

/-- No other native three-arrow equalities arise in the quotient:
the quotient identifies precisely the Int×Int kernel pairs. -/
theorem c60F77Projection_exactKernel
    {X Y : GrayGrade} (f g : X ⟶ Y) :
    c60F77Projection.map f = c60F77Projection.map g ↔
      f.charge = g.charge := by
  exact
    (CategoryTheory.Quotient.functor_map_eq_iff c60F77ChargeKernel f g).trans
      (c60F77ChargeKernel_iff f g)

/-- Full native phase generator at an exact ZMod2 boundary grade.
It changes NO integer charge and has the nonzero independent phase. -/
def c60F77PhaseGenerator (X : GrayGrade) : X ⟶ X :=
  ⟨rfl, (0 : Int × Int), (1 : ZMod 2)⟩

/-- Phase carrier with arbitrary ZMod2 value, used to prove a genuinely
universal quotient from the single nonidentity phase-one generator. -/
def c60F77PhaseArrow (X : GrayGrade) (p : ZMod 2) : X ⟶ X :=
  ⟨rfl, (0 : Int × Int), p⟩

/-- Removing ONLY the independent exchange phase keeps both original
integer coordinates and the exact typed source/target boundary. -/
def c60F77ErasePhase {X Y : GrayGrade} (f : X ⟶ Y) : X ⟶ Y :=
  ⟨f.gradeEq, f.charge, 0⟩

/-- Any native three-arrow factors into its charge-bearing phase-zero
part followed by the source's genuine extra phase at its target. -/
theorem c60F77PhaseFactorization
    {X Y : GrayGrade} (f : X ⟶ Y) :
    c60F77ErasePhase f ≫ c60F77PhaseArrow Y f.phase = f := by
  apply GradedThreeCell.ext
  · change f.charge + (0 : Int × Int) = f.charge
    exact add_zero _
  · change (0 : ZMod 2) + f.phase = f.phase
    exact zero_add _

/-- The generator is literally the ACTUAL odd/odd native braiding
in the original phase-rich Gray category, not a fresh formal symbol. -/
theorem c60F77OddBraiding_isPhaseGenerator :
    (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
      c60F77PhaseGenerator (GrayGrade.tensor GrayGrade.odd GrayGrade.odd) := by
  apply GradedThreeCell.ext
  · rfl
  · decide

/-- The native nonidentity exchange is IDENTIFIED WITH IDENTITY
only after the genuine categorical quotient projection. -/
theorem c60F77PhaseGenerator_collapses (X : GrayGrade) :
    c60F77Projection.map (c60F77PhaseGenerator X) =
      𝟙 (c60F77Projection.obj X) := by
  change
    (CategoryTheory.Quotient.functor c60F77ChargeKernel).map
        (c60F77PhaseGenerator X) =
      (CategoryTheory.Quotient.functor c60F77ChargeKernel).map (𝟙 X)
  apply CategoryTheory.Quotient.sound c60F77ChargeKernel
  exact (c60F77ChargeKernel_iff _ _).mpr rfl

/-- In particular, the original odd/odd nonidentity braiding becomes
the actual identity in the new quotient, not the original category. -/
theorem c60F77OddBraiding_collapses :
    c60F77Projection.map
        (BraidedCategory.braiding GrayGrade.odd GrayGrade.odd).hom =
      𝟙 (c60F77Projection.obj
        (GrayGrade.tensor GrayGrade.odd GrayGrade.odd)) := by
  rw [c60F77OddBraiding_isPhaseGenerator]
  exact c60F77PhaseGenerator_collapses _

/-- Recover the old charge-only target from the ACTUAL quotient by
Mathlib's UNIVERSAL lift, and no arbitrary second projection. -/
def c60F77QuotientToStrictCharge :
    C60F77NativeQuotient ⥤ C60F75StrictChargeGrade :=
  CategoryTheory.Quotient.lift c60F77ChargeKernel
    c60F75ForgetGrayExchangePhase (by
      intro X Y f g h
      exact h)

/-- The original F75 strictification factors through the real quotient
ON THE NOSE, as an equality of genuine Mathlib functors. -/
theorem c60F77QuotientToStrictCharge_factor :
    c60F77Projection ⋙ c60F77QuotientToStrictCharge =
      c60F75ForgetGrayExchangePhase :=
  CategoryTheory.Quotient.lift_spec c60F77ChargeKernel
    c60F75ForgetGrayExchangePhase (by
      intro X Y f g h
      exact h)

/-- All quotient morphisms have representatives: no 3-arrow was invented
by the quotient construction. -/
theorem c60F77Projection_full
    {X Y : C60F77NativeQuotient} (f : X ⟶ Y) :
    ∃ g : X.as ⟶ Y.as, c60F77Projection.map g = f :=
  (CategoryTheory.Quotient.full_functor c60F77ChargeKernel).map_surjective f

/-- The true quotient-to-charge functor is surjective on EVERY
strict 3-Hom: choose precisely the original native grade equality,
both integer charges, and zero phase. -/
theorem c60F77ToStrictCharge_map_surjective
    (X Y : C60F77NativeQuotient)
    (f : c60F77QuotientToStrictCharge.obj X ⟶
      c60F77QuotientToStrictCharge.obj Y) :
    ∃ g : X ⟶ Y, c60F77QuotientToStrictCharge.map g = f := by
  let g₀ : X.as ⟶ Y.as :=
    ⟨f.gradeEq, f.charge, 0⟩
  refine ⟨c60F77Projection.map g₀, ?_⟩
  apply C60F75StrictChargeThree.ext
  rfl

/-- The true quotient-to-charge functor is injective on EVERY
Hom-set because the CATEGORY congruence is precisely charge equality. -/
theorem c60F77ToStrictCharge_map_injective
    (X Y : C60F77NativeQuotient) (f g : X ⟶ Y)
    (h : c60F77QuotientToStrictCharge.map f =
      c60F77QuotientToStrictCharge.map g) : f = g := by
  revert h
  refine Quot.inductionOn f (fun f₀ => ?_)
  refine Quot.inductionOn g (fun g₀ => ?_)
  intro h₀
  apply CategoryTheory.Quotient.sound c60F77ChargeKernel
  apply (c60F77ChargeKernel_iff f₀ g₀).mpr
  exact congrArg C60F75StrictChargeThree.charge h₀

/-- Every strict charge-grade object is literally the image of a
true quotient object; no essential-surjectivity hypothesis is assumed. -/
theorem c60F77ToStrictCharge_obj_surjective
    (Y : C60F75StrictChargeGrade) :
    ∃ X : C60F77NativeQuotient,
      c60F77QuotientToStrictCharge.obj X = Y := by
  refine ⟨⟨⟨Y.degree⟩⟩, ?_⟩
  cases Y
  rfl

/-! ## Universal property generated by killing the actual exchange phase -/

universe u v
variable {D : Type u} [Category.{v} D]

/-- If a functor kills JUST the phase-one generator at every grade,
then it kills arbitrary ZMod2 phase arrows, including phase zero.
No assumption about any of the integer charges is needed. -/
theorem c60F77PhaseArrow_killed
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X))
    (X : GrayGrade) (p : ZMod 2) :
    F.map (c60F77PhaseArrow X p) = 𝟙 (F.obj X) := by
  have hp : p = (0 : ZMod 2) ∨ p = 1 := by
    have hv : p.val < 2 := ZMod.val_lt p
    have hv01 : p.val = 0 ∨ p.val = 1 := by omega
    rcases hv01 with h0 | h1
    · exact Or.inl ((ZMod.val_eq_zero p).mp h0)
    · exact Or.inr ((ZMod.val_eq_one (by decide : 1 < 2) p).mp h1)
  rcases hp with hp0 | hp1
  · rw [hp0]
    have hzero : c60F77PhaseArrow X 0 = 𝟙 X := by
      apply GradedThreeCell.ext <;> rfl
    rw [hzero]
    exact F.map_id X
  · rw [hp1]
    change F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X)
    exact hkill X

/-- THE KEY MINIMALITY RESULT. Any functor that kills the
nontrivial phase-one generator automatically respects ALL and ONLY
the native charge-kernel pairs, by the proved phase factorization. -/
theorem c60F77KillPhase_respectsKernel
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X)) :
    ∀ (X Y : GrayGrade) (f g : X ⟶ Y),
      c60F77ChargeKernel f g → F.map f = F.map g := by
  intro X Y f g hrel
  have hcharge : f.charge = g.charge :=
    (c60F77ChargeKernel_iff f g).mp hrel
  have hbase : c60F77ErasePhase f = c60F77ErasePhase g := by
    apply GradedThreeCell.ext
    · exact hcharge
    · rfl
  have hf : F.map f = F.map (c60F77ErasePhase f) := by
    calc
      F.map f =
          F.map (c60F77ErasePhase f ≫ c60F77PhaseArrow Y f.phase) := by
            rw [c60F77PhaseFactorization]
      _ = F.map (c60F77ErasePhase f) := by
            rw [F.map_comp, c60F77PhaseArrow_killed F hkill Y f.phase,
              Category.comp_id]
  have hg : F.map g = F.map (c60F77ErasePhase g) := by
    calc
      F.map g =
          F.map (c60F77ErasePhase g ≫ c60F77PhaseArrow Y g.phase) := by
            rw [c60F77PhaseFactorization]
      _ = F.map (c60F77ErasePhase g) := by
            rw [F.map_comp, c60F77PhaseArrow_killed F hkill Y g.phase,
              Category.comp_id]
  calc
    F.map f = F.map (c60F77ErasePhase f) := hf
    _ = F.map (c60F77ErasePhase g) := congrArg F.map hbase
    _ = F.map g := hg.symm

/-- The UNIVERSAL descended functor, for an ARBITRARY target category,
is actually constructed by Mathlib.Quotient.lift from the generator
identity and source category composition. -/
def c60F77UniversalLift
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X)) :
    C60F77NativeQuotient ⥤ D :=
  CategoryTheory.Quotient.lift c60F77ChargeKernel F
    (c60F77KillPhase_respectsKernel F hkill)

/-- This descended functor has the exact originally requested source
semantics: precomposing with the quotient projection gives F itself. -/
theorem c60F77UniversalLift_spec
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X)) :
    c60F77Projection ⋙ c60F77UniversalLift F hkill = F :=
  CategoryTheory.Quotient.lift_spec c60F77ChargeKernel F
    (c60F77KillPhase_respectsKernel F hkill)

/-- The factor is UNIQUE among all target functors: full universal
property of the actual quotient, not merely charge bookkeeping. -/
theorem c60F77UniversalLift_unique
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X))
    (G : C60F77NativeQuotient ⥤ D)
    (hG : c60F77Projection ⋙ G = F) :
    G = c60F77UniversalLift F hkill :=
  CategoryTheory.Quotient.lift_unique c60F77ChargeKernel F
    (c60F77KillPhase_respectsKernel F hkill) G hG

/-- Universal existence and uniqueness in standard mathematical form.
The precise relation generated by killing phase-one at each grade
is the charge congruence (not an unproven equation on raw F42 words). -/
theorem c60F77Universal_existsUnique
    (F : GrayGrade ⥤ D)
    (hkill : ∀ X : GrayGrade,
      F.map (c60F77PhaseGenerator X) = 𝟙 (F.obj X)) :
    ∃! G : C60F77NativeQuotient ⥤ D,
      c60F77Projection ⋙ G = F := by
  refine ⟨c60F77UniversalLift F hkill,
    c60F77UniversalLift_spec F hkill, ?_⟩
  intro G hG
  exact c60F77UniversalLift_unique F hkill G hG

/-! ## Original proof-relevant F42/F43/F51 source factorization -/

/-- The original F42/F43/F51 source three-Hom maps FIRST into the
genuine quotient, retaining real original 1-path boundaries and
original three-arrow composition; F75 is its subsequent evaluation. -/
def c60F77OriginalSourceQuotient
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F51OriginalTwo p q ⥤ C60F77NativeQuotient :=
  c60F51GrayFunctor p q ⋙ c60F77Projection

/-- Original F42/F43 source strictification genuinely FACTORS
through the actual quotient category, at EVERY true path boundary. -/
theorem c60F77OriginalSource_factor
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    c60F77OriginalSourceQuotient p q ⋙
        c60F77QuotientToStrictCharge =
      c60F75OriginalFaceStrictification p q := by
  simp only [c60F77OriginalSourceQuotient,
    c60F75OriginalFaceStrictification, Functor.assoc,
    c60F77QuotientToStrictCharge_factor]

/-- The resulting phase-erasure on original source three-arrows
identifies EXACTLY their two integer charges, without losing either
component or postulating equality of unquotiented F42 raw words. -/
theorem c60F77OriginalSource_exactKernel
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q} (f g : X ⟶ Y) :
    (c60F77OriginalSourceQuotient p q).map f =
        (c60F77OriginalSourceQuotient p q).map g ↔
      (c60F51Eval f).charge = (c60F51Eval g).charge := by
  exact c60F77Projection_exactKernel
    ((c60F51GrayFunctor p q).map f)
    ((c60F51GrayFunctor p q).map g)

#print axioms c60F77ChargeKernel_iff
#print axioms c60F77Projection_exactKernel
#print axioms c60F77PhaseFactorization
#print axioms c60F77OddBraiding_isPhaseGenerator
#print axioms c60F77PhaseGenerator_collapses
#print axioms c60F77OddBraiding_collapses
#print axioms c60F77QuotientToStrictCharge_factor
#print axioms c60F77Projection_full
#print axioms c60F77ToStrictCharge_map_surjective
#print axioms c60F77ToStrictCharge_map_injective
#print axioms c60F77ToStrictCharge_obj_surjective
#print axioms c60F77PhaseArrow_killed
#print axioms c60F77KillPhase_respectsKernel
#print axioms c60F77UniversalLift_spec
#print axioms c60F77UniversalLift_unique
#print axioms c60F77Universal_existsUnique
#print axioms c60F77OriginalSource_factor
#print axioms c60F77OriginalSource_exactKernel

end
end KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
