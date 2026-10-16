import KUOS.DependentOriginationC60MediatedTensoratorChargeEvaluationV5_247
import KUOS.DependentOriginationC60StrictChargeGlobularCalculusV5_232
import KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244

namespace KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60StrictChargeGlobularCalculusV5_232
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationC60ExplicitChargeQuotientSectionV5_244
open KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239
open KUOS.DependentOriginationC60TensoratorComparisonObstructionV5_240
open KUOS.DependentOriginationC60MediatedTensoratorChargeEvaluationV5_247

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.248 / F94 — Kuu replaceability and strict interchange on the established quotient

No restoration of the original Gray exchange is attempted or needed.
The mathematical meaning of "kuu" in this file is PRESENTATION
REPLACEABILITY: two correctly typed original C60 source 3-arrows
may replace one another precisely when they determine the same
F77 quotient arrow.  Crucially, neither independent integer
charge is discarded.

We connect this equivalence relation to:
* the real F78 path-indexed strict globular semantics,
* vertical and horizontal original-source 3-arrow composition,
* F80's genuine middle-four quotient interchange,
* the F90 explicit canonical section (choice-independent substitution),
* F93's proven coherent transported/direct tensor comparison.

The F78 globular certificate is reused, not reconstructed.
There is no claim here of lifting the quotient equality back to
unequal original presentations, nor of resolving raw F55 higher descent.
-/

/-- Two original, boundary-typed F51 three-arrows are exchangeable
exactly when their images in the chosen Kuu/F77 category agree. -/
def c60F94Replaceable
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f g : X ⟶ Y) : Prop :=
  (c60F77OriginalSourceQuotient p q).map f =
    (c60F77OriginalSourceQuotient p q).map g

/-- The operative criterion for replacing presentations preserves
BOTH integer charges.  It does not demand phase equality. -/
theorem c60F94Replaceable_iff_charges
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f g : X ⟶ Y) :
    c60F94Replaceable f g ↔
      (c60F51Eval f).charge = (c60F51Eval g).charge :=
  c60F77OriginalSource_exactKernel f g

theorem c60F94Replaceable_refl
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F94Replaceable f f := rfl

theorem c60F94Replaceable_symm
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : c60F94Replaceable f g) :
    c60F94Replaceable g f :=
  h.symm

theorem c60F94Replaceable_trans
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    {f g h : X ⟶ Y}
    (hfg : c60F94Replaceable f g)
    (hgh : c60F94Replaceable g h) :
    c60F94Replaceable f h :=
  hfg.trans hgh

/-- Replaceability is compatible with the ACTUAL vertical
composition of original C60 source 3-arrows. -/
theorem c60F94Replaceable_vertical
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y Z : C60F51OriginalTwo p q}
    {f f' : X ⟶ Y} {g g' : Y ⟶ Z}
    (hf : c60F94Replaceable f f')
    (hg : c60F94Replaceable g g') :
    c60F94Replaceable (f ≫ g) (f' ≫ g') := by
  unfold c60F94Replaceable at hf hg ⊢
  simp only [Functor.map_comp, hf, hg]

/-- Under F78's original path-indexed strict globular semantics,
two presentations yield identical 3-arrows if and only if they
are Kuu-replaceable in the authentic F77 quotient. -/
theorem c60F94Replaceable_iff_F78
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f g : X ⟶ Y) :
    c60F94Replaceable f g ↔
      (c60F78OriginalSourceStrictFunctor p q).map f =
        (c60F78OriginalSourceStrictFunctor p q).map g := by
  unfold c60F94Replaceable
  constructor
  · intro h
    change
      c60F77QuotientToStrictCharge.map
        ((c60F77OriginalSourceQuotient p q).map f) =
      c60F77QuotientToStrictCharge.map
        ((c60F77OriginalSourceQuotient p q).map g)
    exact congrArg (fun z => c60F77QuotientToStrictCharge.map z) h
  · intro h
    change
      c60F77QuotientToStrictCharge.map
        ((c60F77OriginalSourceQuotient p q).map f) =
      c60F77QuotientToStrictCharge.map
        ((c60F77OriginalSourceQuotient p q).map g) at h
    exact c60F77QuotientToStrictCharge.map_injective h

/-- Replacing either ORIGINAL F51 factor leaves the true F80
horizontal quotient 3-arrow untouched at the original composed
C60 path boundary. -/
theorem c60F94Replaceable_horizontal
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    {f f' : X ⟶ X'} {g g' : Y ⟶ Y'}
    (hf : c60F94Replaceable f f')
    (hg : c60F94Replaceable g g') :
    c60F94Replaceable
      (c60F51HorizontalMap f g)
      (c60F51HorizontalMap f' g') := by
  unfold c60F94Replaceable at hf hg ⊢
  rw [c60F80OriginalF51_horizontal_quotient,
    c60F80OriginalF51_horizontal_quotient, hf, hg]

/-- Stronger than replacement compatibility: on arbitrary four
composable ORIGINAL F51 three-arrows, the quotient of the
horizontally pasted vertical composites equals the vertical
composite of the horizontally pasted originals. This is the
authentic F80 middle-four square at the original C60 boundaries. -/
theorem c60F94OriginalSource_horizontalMiddleFour
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' X'' : C60F51OriginalTwo p q}
    {Y Y' Y'' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (f' : X' ⟶ X'')
    (g : Y ⟶ Y') (g' : Y' ⟶ Y'') :
    (c60F77OriginalSourceQuotient (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap (f ≫ f') (g ≫ g')) =
    (c60F77OriginalSourceQuotient (p.comp r) (q.comp s)).map
        (c60F51HorizontalMap f g) ≫
      (c60F77OriginalSourceQuotient (p.comp r) (q.comp s)).map
        (c60F51HorizontalMap f' g') := by
  simp only [c60F80OriginalF51_horizontal_quotient, Functor.map_comp]
  exact c60F80QuotientThreeTensor_middleFour
    ((c60F77OriginalSourceQuotient p q).map f)
    ((c60F77OriginalSourceQuotient p q).map f')
    ((c60F77OriginalSourceQuotient r s).map g)
    ((c60F77OriginalSourceQuotient r s).map g')

/-- Emptying irrelevant presentation choices is constructive:
the F90 canonical section followed by F79 evaluation returns
EVERY actual F77 quotient 3-arrow, not merely its numerical charge. -/
theorem c60F94CanonicalReplacement
    {X Y : C60F77NativeQuotient} (f : X ⟶ Y) :
    c60F90ChargeToNativeQuotient.map
      (c60F77QuotientToStrictCharge.map f) = f :=
  c60F90Section_rightMap f

/-- Canonical choice of representative COMMUTES WITH horizontal
tensor on real F77 Hom-sets. Therefore changing a presentation
before or after horizontal composition yields the SAME arrow,
while retaining the independent Int × Int charges. -/
theorem c60F94CanonicalReplacement_horizontal
    {X X' Y Y' : C60F77NativeQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F90ChargeToNativeQuotient.map
      (c60F76StrictChargeThreeTensor
        (c60F77QuotientToStrictCharge.map f)
        (c60F77QuotientToStrictCharge.map g)) =
      c60F80QuotientThreeTensor f g := by
  rw [← c60F80QuotientTensor_chargeFunctor f g]
  exact c60F90Section_rightMap (c60F80QuotientThreeTensor f g)

/-- After F93, the two separately constructed tensor comparisons
have the SAME interchange naturality for EVERY real quotient
morphism. This uses the proven equality of tensorators; it is not
an assumed identity of the distinct transported/direct structures. -/
theorem c60F94CoherentTensorator_naturality
    {X X' Y Y' : C60F85TransportedQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F80QuotientThreeTensor f g ≫
        (c60F81TransportedVsOriginalQuotientTensorIso X' Y').inv =
      (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv ≫
        (f ⊗ₘ g) := by
  calc
    c60F80QuotientThreeTensor f g ≫
        (c60F81TransportedVsOriginalQuotientTensorIso X' Y').inv =
      c60F80QuotientThreeTensor f g ≫
        (c60F86F85IdentityTensoratorIso X' Y').hom := by
          rw [c60F93AllTensorators_agree X' Y']
    _ = (c60F86F85IdentityTensoratorIso X Y).hom ≫
          (f ⊗ₘ g) :=
        c60F86IdentityTensorator_natural f g
    _ = (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv ≫
          (f ⊗ₘ g) := by
            rw [c60F93AllTensorators_agree X Y]

/-- The existing F78 strict globular certificate, together with
F93's equality on all tensor comparison components, is a
verified, no-restoration input to all later C60 gluing. -/
theorem c60F94GlobularAndCoherentTensorCertificate :
    C60F78StrictGlobularCertificate ∧
    (∀ X Y : C60F77NativeQuotient,
      (c60F86F85IdentityTensoratorIso X Y).hom =
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv) :=
  ⟨c60F78StrictGlobularCertificate_proved,
    c60F93AllTensorators_agree⟩

#print axioms c60F94Replaceable_iff_charges
#print axioms c60F94Replaceable_refl
#print axioms c60F94Replaceable_symm
#print axioms c60F94Replaceable_trans
#print axioms c60F94Replaceable_vertical
#print axioms c60F94Replaceable_iff_F78
#print axioms c60F94Replaceable_horizontal
#print axioms c60F94OriginalSource_horizontalMiddleFour
#print axioms c60F94CanonicalReplacement
#print axioms c60F94CanonicalReplacement_horizontal
#print axioms c60F94CoherentTensorator_naturality
#print axioms c60F94GlobularAndCoherentTensorCertificate

end
end KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
