import KUOS.DependentOriginationC60KuuFiniteContextCechDescentV5_258
import KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
import KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222

namespace KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuObservedContextPentagonV5_257
open KUOS.DependentOriginationC60KuuFiniteContextCechDescentV5_258
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.259 / F105 — conditional gluing of genuinely DIFFERENT C60 physical-edge patches

F104 proved finite Čech descent for many contexts on ONE common original
C60 path pair p,q. Here each chart instead has its OWN actual C60
physical edge, its OWN two distinct endpoint darts, and independently
chosen genuinely typed F51/F95 path presentations between those darts.

The overlap category `O` and the actual functorial RESTRICTION to each
physical patch must be GIVEN; no fictitious overlap functor or global
physical C60 cover is asserted to exist. Their F95-to-F77 observations
provide actual Mathlib functors, not synthetically assigned charges.

On any chosen common overlap, define the exact Int × Int comparison
defect for each original overlap morphism. This defect satisfies an
UNCONDITIONAL additive 1-cocycle identity, even if the local observers
do not agree. Its nonvanishing OBSTRUCTS every zero-additional-charge
observed natural isomorphism. Conversely, if the observed objects
are equal and the charge defect vanishes for ALL overlap morphisms,
a genuinely natural F77 isomorphism exists. Such comparisons are
unique, form strict Čech cocycles, and compose independently of an
arbitrarily long finite chart history.

Finally, the original F68/F69 actual signed pentagon/hexagon cellular
curvature is kept SEPARATE from F77 observed gluing. At every selected
real four-flag edge, physical face incidence and curvature invariance
are retained. In particular, even alongside a valid observed glue,
the real uncorrected north-pentagon second charge remains -5.
Nothing restores original Gray exchange, erases F55 curvature,
or proves unrestricted global physical hyperdescent.
-/

/-! ## I. Finite actual physical-edge patches, NOT one fixed path pair -/

/-- Each chart is pinned to ONE of the original ninety physical
C60 edges. Its original F95 path pair has exactly that edge's
two distinct real dart endpoints, never fabricated site labels. -/
structure C60F105PhysicalEdgePatchFamily (n : Nat) where
  edge : Fin n → TruncatedIcosahedralEdge
  p : (i : Fin n) →
    Quiver.Path (truncatedIcosahedralEdgeEndpoints (edge i)).1
      (truncatedIcosahedralEdgeEndpoints (edge i)).2
  q : (i : Fin n) →
    Quiver.Path (truncatedIcosahedralEdgeEndpoints (edge i)).1
      (truncatedIcosahedralEdgeEndpoints (edge i)).2

/-- Each physical edge has four authentic incidence flags:
two distinct C60 darts × two ACTUAL adjacent 5/6-gon faces. -/
def c60F105PhysicalPatchFace
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i : Fin n) (side : Bool) : TruncatedIcosahedralSeedFace :=
  (c60F46PhysicalFourFlagSquare (A.edge i)).face side

/-- The four incidence witnesses are inherited from the original
C60 geometric flag square, not an invented quadrilateral surface face. -/
theorem c60F105PhysicalPatch_fourIncidences
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i : Fin n) (endpoint side : Bool) :
    truncatedDartOnSeedFace
      ((c60F46PhysicalFourFlagSquare (A.edge i)).vertex endpoint)
      (c60F105PhysicalPatchFace A i side) :=
  c60F46PhysicalFourFlagSquare_allFourIncidences
    (A.edge i) endpoint side

/-- The two physical-edge endpoint darts really are distinct.
The F95 path pair above is not allowed to collapse the physical edge. -/
theorem c60F105PhysicalPatch_endpoints_ne
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i : Fin n) :
    (truncatedIcosahedralEdgeEndpoints (A.edge i)).1 ≠
      (truncatedIcosahedralEdgeEndpoints (A.edge i)).2 :=
  (c60F46PhysicalFourFlagSquare (A.edge i)).endpoints_ne

/-! ## II. Genuine restriction of different F95 categories to a common overlap -/

universe uO vO
variable {O : Type uO} [Category.{vO} O]

/-- The overlap O is a genuine category with GIVEN restriction
functors to the independently path-indexed F95 patch categories.
No map between different original F42 syntax is invented. -/
abbrev C60F105OverlapRestrictions
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n) :=
  (i : Fin n) →
    O ⥤ C60F95LocalKuuQuotient (A.p i) (A.q i)

/-- The authentic observed functor at the i-th original physical
patch: overlap restriction followed by its OWN F95-to-F77 quotient. -/
def c60F105PatchObserved
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i : Fin n) : O ⥤ C60F77NativeQuotient :=
  R i ⋙ c60F95DescendedToF77 (A.p i) (A.q i)

/-- Exact discrepancy between the TWO ORIGINAL integer-charge
coordinates on the common overlap, with NO object-gluing hypothesis.
A nonzero defect is retained as evidence, not quotiented away. -/
def c60F105OverlapChargeDefect
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n) {X Y : O} (f : X ⟶ Y) : Int × Int :=
  (c60F77QuotientToStrictCharge.map
    ((c60F105PatchObserved A R i).map f)).charge -
  (c60F77QuotientToStrictCharge.map
    ((c60F105PatchObserved A R j).map f)).charge

/-- The defect is antisymmetric without ANY flatness assumption. -/
theorem c60F105OverlapDefect_skew
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n) {X Y : O} (f : X ⟶ Y) :
    c60F105OverlapChargeDefect A R i j f =
      -c60F105OverlapChargeDefect A R j i f := by
  unfold c60F105OverlapChargeDefect
  abel

/-- The signed comparison defect forms an UNCONDITIONAL additive
1-cocycle for any THREE distinct physical patches. This holds even
when it is NONZERO and no comparison isomorphism exists. -/
theorem c60F105OverlapDefect_cocycle
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j k : Fin n) {X Y : O} (f : X ⟶ Y) :
    c60F105OverlapChargeDefect A R i j f +
      c60F105OverlapChargeDefect A R j k f =
        c60F105OverlapChargeDefect A R i k f := by
  unfold c60F105OverlapChargeDefect
  abel

/-- The exact endpoint charge defect vanishes if and only if both
integer-charge coordinates of the genuine observations agree. -/
theorem c60F105OverlapDefect_zero_iff
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n) {X Y : O} (f : X ⟶ Y) :
    c60F105OverlapChargeDefect A R i j f = (0 : Int × Int) ↔
      (c60F77QuotientToStrictCharge.map
        ((c60F105PatchObserved A R i).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F105PatchObserved A R j).map f)).charge := by
  exact sub_eq_zero

/-- NECESSITY: any zero-added-charge natural isomorphism across
two real patch observations forces the EXACT pairwise charge
defect to vanish on EVERY original overlap morphism. -/
theorem c60F105ZeroChargeIso_forces_defect_zero
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n)
    (θ : c60F105PatchObserved A R i ≅ c60F105PatchObserved A R j)
    (hθ : ∀ X : O,
      (c60F77QuotientToStrictCharge.map (θ.hom.app X)).charge =
        (0 : Int × Int))
    {X Y : O} (f : X ⟶ Y) :
    c60F105OverlapChargeDefect A R i j f = (0 : Int × Int) := by
  apply (c60F105OverlapDefect_zero_iff A R i j f).mpr
  have hn :=
    congrArg
      (fun g :
        (c60F105PatchObserved A R i).obj X ⟶
          (c60F105PatchObserved A R j).obj Y =>
        (c60F77QuotientToStrictCharge.map g).charge)
      (θ.hom.naturality f)
  simpa only [c60F80QuotientThree_comp_charge,
    hθ X, hθ Y, add_zero, zero_add] using hn

/-- NONZERO original overlap charge difference obstructs ANY
zero-added-charge NatIso. No fake descent is inferred from a
nonzero local defect. -/
theorem c60F105NonzeroOverlapDefect_obstruction
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n) {X Y : O} (f : X ⟶ Y)
    (hω : c60F105OverlapChargeDefect A R i j f ≠
      (0 : Int × Int)) :
    ¬ ∃ θ : c60F105PatchObserved A R i ≅
      c60F105PatchObserved A R j,
      ∀ Z : O,
        (c60F77QuotientToStrictCharge.map (θ.hom.app Z)).charge =
          (0 : Int × Int) := by
  rintro ⟨θ, hθ⟩
  exact hω (c60F105ZeroChargeIso_forces_defect_zero A R i j θ hθ f)

/-! ## III. Sufficiency under *explicit* observed object and Hom compatibility -/

/-- If the physical overlap restrictions ALSO give equality of
observed F77 objects and vanishing charge difference on ALL overlap
3-arrows, they induce an ACTUAL Mathlib NatIso of observations.
The original F42/F55 patch presentations are not identified. -/
def c60F105PairConditionalNatIso
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n)
    (hObj : ∀ X : O,
      (c60F105PatchObserved A R i).obj X =
        (c60F105PatchObserved A R j).obj X)
    (hDef : ∀ {X Y : O} (f : X ⟶ Y),
      c60F105OverlapChargeDefect A R i j f = (0 : Int × Int)) :
    c60F105PatchObserved A R i ≅ c60F105PatchObserved A R j :=
  NatIso.ofComponents
    (fun X => eqToIso (hObj X))
    (by
      intro X Y f
      change
        (c60F105PatchObserved A R i).map f ≫ eqToHom (hObj Y) =
          eqToHom (hObj X) ≫ (c60F105PatchObserved A R j).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact (c60F105OverlapDefect_zero_iff A R i j f).mp (hDef f))

/-- The actual comparison arrow has zero ADDITIONAL charge,
even when the input overlap morphism has nonzero Int × Int charge. -/
theorem c60F105PairConditionalNatIso_charge_zero
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n)
    (hObj : ∀ X : O,
      (c60F105PatchObserved A R i).obj X =
        (c60F105PatchObserved A R j).obj X)
    (hDef : ∀ {X Y : O} (f : X ⟶ Y),
      c60F105OverlapChargeDefect A R i j f = (0 : Int × Int))
    (X : O) :
    (c60F77QuotientToStrictCharge.map
      ((c60F105PairConditionalNatIso A R i j hObj hDef).hom.app X)).charge =
        (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map (eqToHom (hObj X))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-- For a given actual equality of observed objects on the shared
overlap, existence of a zero-added-charge NatIso is EQUIVALENT to
vanishing of all actual two-component charge differences. -/
theorem c60F105PairGluing_iff_zero_defect
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (i j : Fin n)
    (hObj : ∀ X : O,
      (c60F105PatchObserved A R i).obj X =
        (c60F105PatchObserved A R j).obj X) :
    (∀ {X Y : O} (f : X ⟶ Y),
      c60F105OverlapChargeDefect A R i j f = (0 : Int × Int)) ↔
      ∃ θ : c60F105PatchObserved A R i ≅
        c60F105PatchObserved A R j,
        ∀ X : O,
          (c60F77QuotientToStrictCharge.map (θ.hom.app X)).charge =
            (0 : Int × Int) := by
  constructor
  · intro hDef
    exact ⟨c60F105PairConditionalNatIso A R i j hObj hDef,
      c60F105PairConditionalNatIso_charge_zero A R i j hObj hDef⟩
  · rintro ⟨θ, hθ⟩
    intro X Y f
    exact c60F105ZeroChargeIso_forces_defect_zero A R i j θ hθ f

/-! ## IV. Conditional Čech gluing of any finite physical edge-patch family -/

/-- The ACTUAL proof obligations for a common overlap:
equality of F77 observed objects, and TWO INDEPENDENT integer
charge coordinates agreeing for every overlap three-arrow.
These are not silently inferred from incidence alone. -/
structure C60F105OverlapCompatibility
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A) : Prop where
  objects :
    ∀ (i j : Fin n) (X : O),
      (c60F105PatchObserved A R i).obj X =
        (c60F105PatchObserved A R j).obj X
  charges :
    ∀ (i j : Fin n) {X Y : O} (f : X ⟶ Y),
      c60F105OverlapChargeDefect A R i j f = (0 : Int × Int)

/-- Conditional REAL physical-patch Čech comparison: each i,j
may refer to distinct original C60 edges and distinct source
F95 local path-pair categories. -/
def c60F105PhysicalPatchTransition
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R) (i j : Fin n) :
    c60F105PatchObserved A R i ≅ c60F105PatchObserved A R j :=
  c60F105PairConditionalNatIso A R i j (h.objects i j) (h.charges i j)

/-- Actual F77 charge of each physical patch transition component
vanishes, while its source Hom charges remain arbitrary. -/
theorem c60F105PhysicalPatchTransition_charge_zero
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R) (i j : Fin n) (X : O) :
    (c60F77QuotientToStrictCharge.map
      ((c60F105PhysicalPatchTransition A R h i j).hom.app X)).charge =
        (0 : Int × Int) :=
  c60F105PairConditionalNatIso_charge_zero A R i j
    (h.objects i j) (h.charges i j) X

/-- Čech 1-cocycle on a FINITE SET OF DISTINCT REAL C60 EDGES:
the two paths of canonical zero-charge observed comparisons agree
as genuine Mathlib natural transformations. -/
theorem c60F105PhysicalPatchTransition_cocycle
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R)
    (i j k : Fin n) :
    (c60F105PhysicalPatchTransition A R h i j).hom ≫
      (c60F105PhysicalPatchTransition A R h j k).hom =
        (c60F105PhysicalPatchTransition A R h i k).hom := by
  apply c60F103ZeroChargeNatTrans_unique
  · intro X
    change
      (c60F77QuotientToStrictCharge.map
        (eqToHom (h.objects i j X) ≫
          eqToHom (h.objects j k X))).charge = (0 : Int × Int)
    simp only [c60F80QuotientThree_comp_charge,
      c60F82Quotient_eqToHom_charge_zero, zero_add]
  · intro X
    exact c60F105PhysicalPatchTransition_charge_zero A R h i k X

/-- A *finite* path of physically different C60 edge patches
is a properly typed natural transformation of their overlap
observers. No actual physical patch coverage has been assumed. -/
def c60F105PhysicalPatchTransitionChain
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R) (i j : Fin n) :
    List (Fin n) →
      (c60F105PatchObserved A R i ⟶ c60F105PatchObserved A R j)
  | [] => (c60F105PhysicalPatchTransition A R h i j).hom
  | k :: rest =>
      (c60F105PhysicalPatchTransition A R h i k).hom ≫
        c60F105PhysicalPatchTransitionChain A R h k j rest

/-- Conditional path independence for ALL finite genuine
physical-patch comparison histories, not merely charge labels. -/
theorem c60F105PhysicalPatchTransitionChain_eq_direct
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R) (i j : Fin n)
    (history : List (Fin n)) :
    c60F105PhysicalPatchTransitionChain A R h i j history =
      (c60F105PhysicalPatchTransition A R h i j).hom := by
  induction history generalizing i with
  | nil => rfl
  | cons k rest ih =>
      change
        (c60F105PhysicalPatchTransition A R h i k).hom ≫
          c60F105PhysicalPatchTransitionChain A R h k j rest =
            (c60F105PhysicalPatchTransition A R h i j).hom
      rw [ih k]
      exact c60F105PhysicalPatchTransition_cocycle A R h i k j

/-! ## V. Actual physical C60 2-cochain is NOT removed by observed gluing -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section PhysicalCurvaturePreserved
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- On an ACTUAL physical flag-square face selected at patch i,
the original signed C60 curvature is still invariant across arbitrary
90-edge face-choice atlases. This says nothing about its vanishing. -/
theorem c60F105PhysicalFaceCurvature_invariant
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (i : Fin n) (side : Bool)
    (sigma tau : C60F67Atlas) :
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
        (Finsupp.single (c60F105PhysicalPatchFace A i side) (1 : ℤ)) =
      c60F68PhysicalPatchCurvature t₁ t₂ left right tau
        (Finsupp.single (c60F105PhysicalPatchFace A i side) (1 : ℤ)) :=
  c60F68PhysicalPatchCurvature_evaluate_independent
    t₁ t₂ left right sigma tau _

/-- Both mathematical facts hold SIMULTANEOUSLY:
genuine F77 observed glue may carry zero added charge,
while the authentic original north pentagon has second integer
curvature -5. Thus observed descent does NOT erase F55 curvature. -/
theorem c60F105ObservedGlue_retainsNorthCurvature
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (R : C60F105OverlapRestrictions (O := O) A)
    (h : C60F105OverlapCompatibility A R) (i j : Fin n)
    (X : O) (sigma : C60F67Atlas) :
    (c60F77QuotientToStrictCharge.map
      ((c60F105PhysicalPatchTransition A R h i j).hom.app X)).charge =
        (0 : Int × Int) ∧
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) := by
  exact ⟨c60F105PhysicalPatchTransition_charge_zero A R h i j X,
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma⟩

end PhysicalCurvaturePreserved

#print axioms c60F105PhysicalPatch_fourIncidences
#print axioms c60F105PhysicalPatch_endpoints_ne
#print axioms c60F105OverlapDefect_skew
#print axioms c60F105OverlapDefect_cocycle
#print axioms c60F105OverlapDefect_zero_iff
#print axioms c60F105ZeroChargeIso_forces_defect_zero
#print axioms c60F105NonzeroOverlapDefect_obstruction
#print axioms c60F105PairConditionalNatIso
#print axioms c60F105PairConditionalNatIso_charge_zero
#print axioms c60F105PairGluing_iff_zero_defect
#print axioms c60F105PhysicalPatchTransition
#print axioms c60F105PhysicalPatchTransition_charge_zero
#print axioms c60F105PhysicalPatchTransition_cocycle
#print axioms c60F105PhysicalPatchTransitionChain_eq_direct
#print axioms c60F105PhysicalFaceCurvature_invariant
#print axioms c60F105ObservedGlue_retainsNorthCurvature

end
end KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
