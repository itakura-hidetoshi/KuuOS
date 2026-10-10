import Mathlib.Logic.Relation
import KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140

set_option autoImplicit false
noncomputable section

/-!
# F44-A / v5.141 — proof-relevant primitive shuffle and generated quotient

F43's Interleaving lives in Prop: quotienting its proofs directly would
erase all shuffle-order information by proof irrelevance. We therefore
construct a companion Type-valued native derivation, retaining each
intermediate F19/F28 Blocks presentation and its genuine OneStep.

The ONLY generating exchange is the adjacent square between one F19
modification move and one independent F28 quotient-category move,
together with congruence under subsequent moves. Its equivalence
closure is Relation.EqvGen; the corresponding quotient is Quot Swap.
No two distinct same-axis steps are declared exchangeable, and no
composite-equality relation is silently added to the quotient.

All constructions stay in two independently typed original categories.
-/

namespace Grid

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid
open KUOS.DependentOriginationCoherentBiadjunctionFunctorialPrimitiveRefinementV5_140.Grid

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A proof-relevant F43 shuffle. Unlike the F43 Prop, this Type
retains the two possible syntactic orders of independently typed
primitive refinement operations. -/
inductive OrderedInterleaving :
    ∀ {a b : D} {x y : E}, Nat → Nat →
      Blocks a b → Blocks x y →
      Blocks a b → Blocks x y → Type (max uD uE vD vE) where
  | refl {a b : D} {x y : E}
      (mods : Blocks a b) (pq : Blocks x y) :
      OrderedInterleaving 0 0 mods pq mods pq
  | modification {a b : D} {x y : E}
      {n m : Nat}
      {ma mb mc : Blocks a b} {pa pb : Blocks x y}
      (h : OrderedInterleaving n m ma pa mb pb)
      (step : OneStep mb mc) :
      OrderedInterleaving (n + 1) m ma pa mc pb
  | comparison {a b : D} {x y : E}
      {n m : Nat}
      {ma mb : Blocks a b} {pa pb pc : Blocks x y}
      (h : OrderedInterleaving n m ma pa mb pb)
      (step : OneStep pb pc) :
      OrderedInterleaving n (m + 1) ma pa mb pc

/-- The new Type-valued route proves the unchanged original F43 Prop. -/
theorem OrderedInterleaving.toInterleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    Interleaving n m ma pa mb pb := by
  induction h with
  | refl mods pq =>
      exact Interleaving.refl mods pq
  | modification h step ih =>
      exact Interleaving.modification ih step
  | comparison h step ih =>
      exact Interleaving.comparison ih step

/-- Each original F43 Prop certificate has a proof-relevant
representative, although proof irrelevance supplies no CANONICAL
choice of its original syntactic presentation. -/
theorem OrderedInterleaving.nonempty_of_interleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : Interleaving n m ma pa mb pb) :
    Nonempty (OrderedInterleaving n m ma pa mb pb) := by
  induction h with
  | refl mods pq =>
      exact ⟨OrderedInterleaving.refl mods pq⟩
  | modification h step ih =>
      rcases ih with ⟨route⟩
      exact ⟨OrderedInterleaving.modification route step⟩
  | comparison h step ih =>
      rcases ih with ⟨route⟩
      exact ⟨OrderedInterleaving.comparison route step⟩

/-- Independently functorial transport of the actual ordered
Type-level route, not merely its endpoint composite or F43 Prop. -/
def OrderedInterleaving.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (h : OrderedInterleaving n m ma pa mb pb) :
    OrderedInterleaving n m
      (mapBlocks H ma) (mapBlocks K pa)
      (mapBlocks H mb) (mapBlocks K pb) := by
  induction h with
  | refl mods pq =>
      exact OrderedInterleaving.refl (mapBlocks H mods) (mapBlocks K pq)
  | modification h step ih =>
      exact OrderedInterleaving.modification ih (oneStep_mapBlocks H step)
  | comparison h step ih =>
      exact OrderedInterleaving.comparison ih (oneStep_mapBlocks K step)

/-- Adjacent interchange only of one genuine F19 step with one
INDEPENDENT genuine F28 step, closed under right-hand path context. -/
inductive AdjacentSwap :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y},
      OrderedInterleaving n m ma pa mb pb →
      OrderedInterleaving n m ma pa mb pb → Prop where
  | square {a b : D} {x y : E}
      {n m : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (prefix : OrderedInterleaving n m ma pa mb pb)
      (hm : OneStep mb mc) (hp : OneStep pb pc) :
      AdjacentSwap
        (OrderedInterleaving.comparison
          (OrderedInterleaving.modification prefix hm) hp)
        (OrderedInterleaving.modification
          (OrderedInterleaving.comparison prefix hp) hm)
  | afterModification {a b : D} {x y : E}
      {n m : Nat}
      {ma mb mc : Blocks a b} {pa pb : Blocks x y}
      {p q : OrderedInterleaving n m ma pa mb pb}
      (h : AdjacentSwap p q) (step : OneStep mb mc) :
      AdjacentSwap (OrderedInterleaving.modification p step)
        (OrderedInterleaving.modification q step)
  | afterComparison {a b : D} {x y : E}
      {n m : Nat}
      {ma mb : Blocks a b} {pa pb pc : Blocks x y}
      {p q : OrderedInterleaving n m ma pa mb pb}
      (h : AdjacentSwap p q) (step : OneStep pb pc) :
      AdjacentSwap (OrderedInterleaving.comparison p step)
        (OrderedInterleaving.comparison q step)

/-- The equivalence relation is GENERATED from the genuine local
exchange rules, rather than inferred from equality of final arrows. -/
def ExchangeEqv
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p q : OrderedInterleaving n m ma pa mb pb) : Prop :=
  Relation.EqvGen (fun r s => AdjacentSwap r s) p q

/-- Reflexivity, symmetry and transitivity are consequences of
equivalence generation, not additional primitive exchange rules. -/
theorem exchangeEqv_equivalence
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y} :
    Equivalence (ExchangeEqv (D := D) (E := E) (ma := ma) (mb := mb)
      (pa := pa) (pb := pb) (n := n) (m := m)) :=
  Relation.EqvGen.is_equivalence _

/-- Every raw adjacent exchange transports through both real
functors and remains a genuine adjacent exchange with exact counts. -/
theorem AdjacentSwap.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {p q : OrderedInterleaving n m ma pa mb pb}
    (h : AdjacentSwap p q) :
    AdjacentSwap (OrderedInterleaving.mapBoth H K p)
      (OrderedInterleaving.mapBoth H K q) := by
  induction h with
  | square prefix hm hp =>
      exact AdjacentSwap.square
        (OrderedInterleaving.mapBoth H K prefix)
        (oneStep_mapBlocks H hm) (oneStep_mapBlocks K hp)
  | afterModification h step ih =>
      exact AdjacentSwap.afterModification ih (oneStep_mapBlocks H step)
  | afterComparison h step ih =>
      exact AdjacentSwap.afterComparison ih (oneStep_mapBlocks K step)

/-- Genuine Type-level path quotient by the adjacent exchange rule.
Its equality is exactly the reflexive/symmetric/transitive closure
of AdjacentSwap, because Quot forms that generated congruence. -/
def ExchangeClass
    {a b : D} {x y : E} (n m : Nat)
    (ma mb : Blocks a b) (pa pb : Blocks x y) :
    Type (max uD uE vD vE) :=
  Quot (fun p q : OrderedInterleaving n m ma pa mb pb => AdjacentSwap p q)

/-- Put a concrete ordered path into the genuine exchange quotient. -/
def OrderedInterleaving.toClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p : OrderedInterleaving n m ma pa mb pb) :
    ExchangeClass n m ma mb pa pb :=
  Quot.mk _ p

/-- Exact quotient characterization: no additional identifications
besides the equivalence closure of the primitive adjacent exchanges. -/
theorem exchangeEqv_iff_class_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (p q : OrderedInterleaving n m ma pa mb pb) :
    ExchangeEqv p q ↔
      OrderedInterleaving.toClass p = OrderedInterleaving.toClass q := by
  constructor
  · exact Quot.eqvGen_sound
  · exact Quot.eqvGen_exact

/-- Every exchange class retains the REAL F43 finite two-axis
derivation, rather than only equality of evaluated composites. -/
theorem ExchangeClass.toInterleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    Interleaving n m ma pa mb pb := by
  refine Quot.ind ?_ c
  intro route
  exact OrderedInterleaving.toInterleaving route

/-- Both unchanged original categorical Hom composites remain equal
after descent to the generated exchange quotient. -/
theorem ExchangeClass.composites
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ma.composite = mb.composite ∧ pa.composite = pb.composite :=
  (ExchangeClass.toInterleaving c).composites

/-- Transport a genuine EXCHANGE CLASS through both original functors;
the quotient lift is justified by transporting the primitive square
and its congruence, not by equating mapped endpoint arrows. -/
def ExchangeClass.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ExchangeClass n m
      (mapBlocks H ma) (mapBlocks H mb)
      (mapBlocks K pa) (mapBlocks K pb) :=
  Quot.liftOn c
    (fun p => OrderedInterleaving.toClass (OrderedInterleaving.mapBoth H K p))
    (by
      intro p q hpq
      exact Quot.sound (AdjacentSwap.mapBoth H K hpq))

/-- The genuine mapped quotient class preserves both evaluated
Hom equalities in the two potentially unrelated original categories. -/
theorem ExchangeClass.mapBoth_composites
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ((mapBlocks H ma).composite = (mapBlocks H mb).composite) ∧
      ((mapBlocks K pa).composite = (mapBlocks K pb).composite) :=
  (ExchangeClass.mapBoth H K c).composites

#print axioms OrderedInterleaving
#print axioms OrderedInterleaving.toInterleaving
#print axioms OrderedInterleaving.nonempty_of_interleaving
#print axioms OrderedInterleaving.mapBoth
#print axioms AdjacentSwap
#print axioms AdjacentSwap.mapBoth
#print axioms ExchangeEqv
#print axioms exchangeEqv_equivalence
#print axioms ExchangeClass
#print axioms OrderedInterleaving.toClass
#print axioms exchangeEqv_iff_class_eq
#print axioms ExchangeClass.toInterleaving
#print axioms ExchangeClass.composites
#print axioms ExchangeClass.mapBoth
#print axioms ExchangeClass.mapBoth_composites

end Grid
end

end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141
