import KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
import KUOS.DependentOriginationFunctorialTransportV0_1
import Mathlib.CategoryTheory.Bicategory.Coherence
import Mathlib.CategoryTheory.Bicategory.LocallyDiscrete
import Mathlib.CategoryTheory.CodiscreteCategory
import Mathlib.CategoryTheory.Bicategory.Functor.LocallyDiscrete

namespace KUOS.DependentOriginationGrayC60WangBiNativeBicategoryV5_171

open CategoryTheory
open scoped CategoryTheory.Bicategory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F23 / v5.171: native bicategory of Wang Bi's contextual six-Yao chart changes

SOURCE: original C60 32 signed pentagon/hexagon faces, Wang Bi six-Yao
codes and temporal readings (F59-F22). A chart is an ACTUAL
equivalence between those 32 geometric faces and five-bit
patterns, never an intrinsic King Wen/Fu Xi hexagram assignment.

The genuine MATHLIB CODISCRETE CATEGORY on these charts has a
specified 1-arrow from every chart to every other chart. The
transition acts on six-Yao symbols by the original theorem-bearing
C60 equiv; temporal context is transported unchanged, so we
preserve the important Wang Bi separation of hexagram-as-time
and Yao-as-contextual-change.

A real Type-valued FUNCTOR is constructed and checked against
category identity/composition. Mathlib's native
Bicategory on LocallyDiscrete source provides genuine
associator/unitor two-cells, whiskering, pentagon and triangle.
The old KuuOS v1.6 transport architecture is preserved in its
v0.1 functorial core without forcing a full legacy recompilation.

We ALSO build a genuine Cat-valued native PSEUDOFUNCTOR
(L.o.c.a.l.l.y D.i.s.c.r.e.t.e source → Cat) from this
constructed ordinary functor, rather than asserting coherence
for an arbitrary hypothetical higher system.

Meaning is not encoded in the geometric 64 choices: the user's
Wang Bi time-dependent interpreter is independently supplied
and shown invariant under ALL chart 1-arrows and all native
bicategorical 2-cells, including reassociation.

This is a rigorous set-truncated sector, not an assertion
that nontrivial original F55 3-cells are just equalities.
An independent braided Cat 2-cell refinement is constructed
in the companion file using F59-C Gray category.
-/

universe uT uM

/-- Real native category on all face↔five-bit chart choices.
It remembers that geometric 32-face coding is not canonical. -/
abbrev C60WangBiChartContext :=
  Codiscrete C60WangBiFaceChart

/-- Actual chart change on six-Yao codes. Each chart has
all 32 ORIGINAL C60 face objects and two physical sides. -/
def c60NativeChartCodeTransport
    (a b : C60WangBiFaceChart) :
    WangBiSixYao ≃ WangBiSixYao :=
  c60WangBiChangeHexagramChart a b

theorem c60NativeChartCodeTransport_identity
    (a : C60WangBiFaceChart) (x : WangBiSixYao) :
    c60NativeChartCodeTransport a a x = x := by
  simp [c60NativeChartCodeTransport, c60WangBiChangeHexagramChart]

/-- Strict pasting of three ORIGINAL chart reencodings
is independent of a chosen intermediate presentation. -/
theorem c60NativeChartCodeTransport_comp
    (a b c : C60WangBiFaceChart) (x : WangBiSixYao) :
    c60NativeChartCodeTransport b c
      (c60NativeChartCodeTransport a b x) =
        c60NativeChartCodeTransport a c x :=
  c60WangBiChartChange_compose a b c x

theorem c60NativeChartCodeTransport_inverse
    (a b : C60WangBiFaceChart) (x : WangBiSixYao) :
    c60NativeChartCodeTransport b a
      (c60NativeChartCodeTransport a b x) = x := by
  rw [c60NativeChartCodeTransport_comp, c60NativeChartCodeTransport_identity]

/-- True state functor on the chart-change CATEGORY, not a
standalone diagrammatic metaphor. Time remains fixed while
a six-Yao symbol changes under an arbitrary original face chart. -/
def c60WangBiContextStateFunctor
    (Time : Type uT) :
    C60WangBiChartContext ⥤ Type uT where
  obj _ := WangBiSixYao × Time
  map := fun {X Y} (_ : X ⟶ Y) =>
    TypeCat.ofHom (fun pair : WangBiSixYao × Time =>
      (c60NativeChartCodeTransport X.as Y.as pair.1, pair.2))
  map_id := by
    intro X
    apply TypeCat.homEquiv.injective
    funext ⟨code, time⟩
    exact congrArg (fun code => (code, time))
      (c60NativeChartCodeTransport_identity X.as code)
  map_comp := by
    intro X Y Z f g
    apply TypeCat.homEquiv.injective
    funext ⟨code, time⟩
    exact congrArg (fun code => (code, time))
      (c60NativeChartCodeTransport_comp X.as Y.as Z.as code).symm

/-- The ORIGINAL KuuOS v0.1 functorial transport interface is
realized concretely on the REAL C60 Wang Bi chart category. -/
def c60WangBiContextTransport
    (Time : Type uT) :
    FunctorialTransportSystem C60WangBiChartContext where
  state := c60WangBiContextStateFunctor Time

/-- The Cat-valued representation is an ACTUAL functor
into the Category of Categories, using Mathlib's canonical
codiscrete fiber functor to Cat. -/
def c60WangBiCatValuedFunctor
    (Time : Type uT) :
    C60WangBiChartContext ⥤ Cat.{0, uT} :=
  (c60WangBiContextStateFunctor Time) ⋙
    Codiscrete.functorToCat

/-- A real NATIVE Mathlib pseudofunctor on the locally discrete
chart bicategory, valued in the bicategory of small categories.
All pseudofunctor mapId/mapComp two-cell data are supplied
by the pinned Mathlib promotion, not postulated. -/
def c60WangBiCatPseudofunctor
    (Time : Type uT) :
    LocallyDiscrete C60WangBiChartContext ⥤ᵖ Cat.{0, uT} :=
  (c60WangBiCatValuedFunctor Time).toPseudofunctor'

/-- Native bicategorical version of the ordinary Cat functor:
the source has actual bicategorical associators, unitors,
two-cell whiskerings, pentagon and triangle. This is an
honest Mathlib Pseudofunctor, not an informal equivalence. -/
def c60WangBiNativeBicategoricalTransport (Time : Type uT) :
    LocallyDiscrete C60WangBiChartContext ⥤ᵖ Cat.{0,uT} :=
  c60WangBiCatPseudofunctor Time

/--王弼: interpret a transported symbol at its ORIGINAL time.
The meaning interpreter is independent of the chosen C60 chart. -/
def c60WangBiTemporalInvariantReadout
    {Time : Type uT} {Meaning : Type uM}
    (origin : C60WangBiFaceChart)
    (reading : WangBiTemporalReading Time Meaning) :
    FunctorialTransportSystem.InvariantReadout
      (c60WangBiContextTransport Time) Meaning where
  readout := fun X pair =>
    (c60WangBiTransportReading origin X.as reading).interpret
      pair.1 pair.2
  transport_invariant := by
    intro X Y f pair
    rcases pair with ⟨code, time⟩
    change
      (c60WangBiTransportReading origin Y.as reading).interpret
        (c60NativeChartCodeTransport X.as Y.as code) time =
      (c60WangBiTransportReading origin X.as reading).interpret
        code time
    simp [c60WangBiTransportReading,
      c60NativeChartCodeTransport, c60WangBiChangeHexagramChart]

/-- A genuine native two-cell between reencoding 1-arrows
does not disturb the original time-dependent Wang Bi reading
at any REAL C60 face symbol. A LocallyDiscrete 2-cell gives
the necessary equality of underlying arrows, not a postulate. -/
theorem c60WangBiNativeTwoCell_preservesMeaning
    {Time : Type uT} {Meaning : Type uM}
    (origin : C60WangBiFaceChart)
    (reading : WangBiTemporalReading Time Meaning)
    {X Y : LocallyDiscrete C60WangBiChartContext}
    {f g : X ⟶ Y} (η : f ⟶ g)
    (state : WangBiSixYao × Time) :
    (c60WangBiTemporalInvariantReadout origin reading).readout Y.as
      ((c60WangBiContextStateFunctor Time).map f.as state) =
    (c60WangBiTemporalInvariantReadout origin reading).readout Y.as
      ((c60WangBiContextStateFunctor Time).map g.as state) := by
  have h : f = g := LocallyDiscrete.eq_of_hom η
  subst g
  rfl

/-- The native bicategory associator 2-isomorphism compares
the two genuinely differently parenthesized chart-change 1-arrows;
our transported six-Yao/time state is invariant. -/
theorem c60WangBiNativeAssociator_preservesState
    (Time : Type uT)
    {X Y Z W : LocallyDiscrete C60WangBiChartContext}
    (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ W)
    (state : WangBiSixYao × Time) :
    (c60WangBiContextStateFunctor Time).map
        (((f ≫ g) ≫ h).as) state =
      (c60WangBiContextStateFunctor Time).map
        ((f ≫ (g ≫ h)).as) state := by
  have hh : (f ≫ g) ≫ h = f ≫ (g ≫ h) :=
    LocallyDiscrete.eq_of_hom (Bicategory.associator f g h).hom
  rw [hh]

/-- Native bicategorical pentagon, including explicit
whiskering and the two genuinely different 2-cell pasting
paths. This coherence is inherited from a BUILT instance. -/
theorem c60WangBiNativePentagon
    {a b c d e : LocallyDiscrete C60WangBiChartContext}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d) (i : d ⟶ e) :
    Bicategory.whiskerRight (Bicategory.associator f g h).hom i ≫
      (Bicategory.associator f (g ≫ h) i).hom ≫
        Bicategory.whiskerLeft f (Bicategory.associator g h i).hom =
      (Bicategory.associator (f ≫ g) h i).hom ≫
        (Bicategory.associator f g (h ≫ i)).hom :=
  Bicategory.pentagon f g h i

theorem c60WangBiNativeTriangle
    {a b c : LocallyDiscrete C60WangBiChartContext}
    (f : a ⟶ b) (g : b ⟶ c) :
    (Bicategory.associator f (𝟙 b) g).hom ≫
        Bicategory.whiskerLeft f (Bicategory.leftUnitor g).hom =
      Bicategory.whiskerRight (Bicategory.rightUnitor f).hom g :=
  Bicategory.triangle f g

#print axioms c60NativeChartCodeTransport_identity
#print axioms c60NativeChartCodeTransport_comp
#print axioms c60NativeChartCodeTransport_inverse
#print axioms c60WangBiContextStateFunctor
#print axioms c60WangBiNativeBicategoricalTransport
#print axioms c60WangBiCatPseudofunctor
#print axioms c60WangBiTemporalInvariantReadout
#print axioms c60WangBiNativeTwoCell_preservesMeaning
#print axioms c60WangBiNativeAssociator_preservesState
#print axioms c60WangBiNativePentagon
#print axioms c60WangBiNativeTriangle

end
end KUOS.DependentOriginationGrayC60WangBiNativeBicategoryV5_171
