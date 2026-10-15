import KUOS.DependentOriginationCoherentBiadjunctionFiniteExchangeAssociativityV5_148

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F51-B / v5.148 — ARBITRARY finite serial ORIGINAL F45 refinements

This is an actual Type-valued finite-chain inductive, NOT a new
assumption or a Prop saying that some finite sequence might exist.
Each constructor records one more ORIGINAL F45 execution order and
its own exact n'/m' original F19/F28 refinement histories.
There is no bound on the number of stages and no fixed global
maximum of primitive operations.

The interpretation is genuinely composed in F44's generated quotient,
not a F26 comparison chain. We prove by structural induction that it
preserves BOTH entire proof-relevant original axis histories, and that
ANY entire finite run equals the ORIGINAL F45 route constructed from
their iterated concatenations in either original execution order.

This extends F50's *two-stage* original-path theorem to any finite
number of stages with exact source/target blocks and two depth indices.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A genuine arbitrary finite number of consecutive ORIGINAL F45
two-axis execution stages, with a separate F19/F28 primitive trace
and ACTUAL original F45 order choice recorded at EVERY stage. -/
inductive OriginalF45Stages :
    ∀ {a b : D} {x y : E}, Nat → Nat →
      Blocks a b → Blocks x y →
      Blocks a b → Blocks x y →
      Type (max (max uD uE) (max vD vE)) where
  | refl {a b : D} {x y : E}
      (mods : Blocks a b) (pq : Blocks x y) :
      OriginalF45Stages 0 0 mods pq mods pq
  | snoc {a b : D} {x y : E}
      {n m n' m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (prior : OriginalF45Stages n m ma pa mb pb)
      (order : OriginalF45Order)
      (hm : AxisTrace n' mb mc)
      (hc : AxisTrace m' pb pc) :
      OriginalF45Stages (n + n') (m + m') ma pa mc pc

/-- Full native F19/F28 proof-relevant operation histories of an
arbitrary number of actually executed old F45 stages. -/
def OriginalF45Stages.axisHistories
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    AxisTrace n ma mb × AxisTrace m pa pb := by
  induction stages with
  | refl mods pq =>
      exact (AxisTrace.refl mods, AxisTrace.refl pq)
  | snoc stages order hm hc ih =>
      exact (AxisTrace.append ih.1 hm, AxisTrace.append ih.2 hc)

/-- Interpret an arbitrary finite ORIGINAL F45 stage sequence in
the REAL F44 generated adjacent-exchange quotient using native
quotient concatenation at EVERY stage, preserving exact depths. -/
def OriginalF45Stages.toExchangeClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    ExchangeClass n m ma mb pa pb := by
  induction stages with
  | refl mods pq =>
      exact ExchangeClass.reflClass mods pq
  | snoc stages order hm hc ih =>
      exact ExchangeClass.append ih (AxisTrace.originalF45OrderClass order hm hc)

/-- Complete proof-relevant finite-stage induction invariant: EVERY
native F19/F28 primitive step remains in its ORIGINAL within-axis
order and the exact final depths after any finite sequence. -/
theorem OriginalF45Stages.toExchangeClass_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    stages.toExchangeClass.axisTraces = stages.axisHistories := by
  induction stages with
  | refl mods pq =>
      rfl
  | snoc stages order hm hc ih =>
      change
        (ExchangeClass.append stages.toExchangeClass
          (AxisTrace.originalF45OrderClass order hm hc)).axisTraces =
        (AxisTrace.append stages.axisHistories.1 hm,
         AxisTrace.append stages.axisHistories.2 hc)
      rw [ExchangeClass.axisTraces_append,
        AxisTrace.originalF45OrderClass_axisTraces, ih]

/-- F46 exact completeness: an ARBITRARY finite sequence of
ORIGINAL F45 order-selected execution stages has precisely the
single history-pair class, with every intermediate primitive stage
and every original within-axis operation order respected. -/
theorem OriginalF45Stages.toExchangeClass_eq_pair
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    stages.toExchangeClass = AxisTrace.pairToClass stages.axisHistories := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simp only [OriginalF45Stages.toExchangeClass_axisTraces,
    AxisTrace.pairToClass_axisTraces]

/-- A whole arbitrary finite serial run equals an ACTUAL OLD F45
F19-first OR F28-first route with exactly its complete total native
axis histories. The final original execution order is independent
of every stage's independently selected order. -/
theorem OriginalF45Stages.toExchangeClass_eq_originalF45
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb)
    (order : OriginalF45Order) :
    stages.toExchangeClass =
      AxisTrace.originalF45OrderClass order
        stages.axisHistories.1 stages.axisHistories.2 := by
  calc
    stages.toExchangeClass = AxisTrace.pairToClass stages.axisHistories :=
      OriginalF45Stages.toExchangeClass_eq_pair stages
    _ = AxisTrace.originalF45OrderClass order
          stages.axisHistories.1 stages.axisHistories.2 :=
      (AxisTrace.originalF45OrderClass_eq_pair order _ _).symm

/-- Any finite number of actual old F45 stages still gives the
unchanged ORIGINAL F43 Interleaving with exactly recorded depths. -/
theorem OriginalF45Stages.toInterleaving
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
      n m ma pa mb pb :=
  stages.toExchangeClass.toInterleaving

/-- Any finite number of ORIGINAL F45 stages preserves separately
the actual categorical Hom composites of the two ORIGINAL categories;
this does not identify their Hom carriers with one another. -/
theorem OriginalF45Stages.composites
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    ma.composite = mb.composite ∧ pa.composite = pb.composite :=
  stages.toExchangeClass.composites

/-- Map the ACTUAL entire finite stage sequence through independent
genuine functors on the two original categories, retaining every
original stage and its separate order choice and exact depth. -/
def OriginalF45Stages.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    OriginalF45Stages n m
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H ma)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pa)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H mb)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pb) := by
  induction stages with
  | refl mods pq =>
      exact OriginalF45Stages.refl
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H mods)
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pq)
  | snoc stages order hm hc ih =>
      exact OriginalF45Stages.snoc ih order
        (AxisTrace.mapBlocks H hm) (AxisTrace.mapBlocks K hc)

/-- Functorial transport of arbitrary finite sequences commutes with
extracting BOTH complete original proof-relevant F19/F28 histories. -/
theorem OriginalF45Stages.mapBoth_axisHistories
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    (OriginalF45Stages.mapBoth H K stages).axisHistories =
      (AxisTrace.mapBlocks H stages.axisHistories.1,
       AxisTrace.mapBlocks K stages.axisHistories.2) := by
  induction stages with
  | refl mods pq =>
      rfl
  | snoc stages order hm hc ih =>
      change
        (AxisTrace.append (OriginalF45Stages.mapBoth H K stages).axisHistories.1
            (AxisTrace.mapBlocks H hm),
         AxisTrace.append (OriginalF45Stages.mapBoth H K stages).axisHistories.2
            (AxisTrace.mapBlocks K hc)) =
        (AxisTrace.mapBlocks H
            (AxisTrace.append stages.axisHistories.1 hm),
         AxisTrace.mapBlocks K
            (AxisTrace.append stages.axisHistories.2 hc))
      rw [ih, AxisTrace.mapBlocks_append, AxisTrace.mapBlocks_append]

/-- Genuine naturality of an ARBITRARY finite number of ORIGINAL
F45 execution stages in the generated F44 quotient, for unrelated
independent functors. Nothing is inferred only from endpoint Hom. -/
theorem OriginalF45Stages.mapBoth_toExchangeClass
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    ExchangeClass.mapBoth H K stages.toExchangeClass =
      (OriginalF45Stages.mapBoth H K stages).toExchangeClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    (ExchangeClass.mapBoth H K stages.toExchangeClass).axisTraces =
        (AxisTrace.mapBlocks H stages.toExchangeClass.axisTraces.1,
         AxisTrace.mapBlocks K stages.toExchangeClass.axisTraces.2) :=
      ExchangeClass.axisTraces_mapBoth H K _
    _ = (AxisTrace.mapBlocks H stages.axisHistories.1,
         AxisTrace.mapBlocks K stages.axisHistories.2) := by
        rw [OriginalF45Stages.toExchangeClass_axisTraces]
    _ = (OriginalF45Stages.mapBoth H K stages).axisHistories :=
      (OriginalF45Stages.mapBoth_axisHistories H K stages).symm
    _ = (OriginalF45Stages.mapBoth H K stages).toExchangeClass.axisTraces :=
      (OriginalF45Stages.toExchangeClass_axisTraces _).symm

#print axioms OriginalF45Stages
#print axioms OriginalF45Stages.axisHistories
#print axioms OriginalF45Stages.toExchangeClass
#print axioms OriginalF45Stages.toExchangeClass_axisTraces
#print axioms OriginalF45Stages.toExchangeClass_eq_pair
#print axioms OriginalF45Stages.toExchangeClass_eq_originalF45
#print axioms OriginalF45Stages.toInterleaving
#print axioms OriginalF45Stages.composites
#print axioms OriginalF45Stages.mapBoth
#print axioms OriginalF45Stages.mapBoth_axisHistories
#print axioms OriginalF45Stages.mapBoth_toExchangeClass

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
