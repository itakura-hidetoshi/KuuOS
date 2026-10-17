import Kuu.F112.PolygonNativeF44QuotientFunctorNaturality

/-!
# F112-E7Q5-F4-N3 — genuine C60 F45 packet and F44 exchange naturality

All independent F45 source constructors (true polygon sector leaf,
both actual Type-valued axis histories, their execution-order choice,
and arbitrary typed binary bracket nodes) are mapped by independent
ordinary categorical functors.

The physical polygon depth bracketing remains literally unchanged.
The source F44 raw execution may retain more constructor-level data
than the quotient, so the canonical functor-naturality assertion is
made for the EXACT generated adjacent-exchange quotient, and is
proved by the M3 historyEquiv's actual injectivity.  This is not
an identification of distinct raw F45 trees or historic Gray sources.

No historical KUOS, Gray, F51, F77 imports and no new axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- Functor transport of complete original-shaped Type-valued axis
histories strictly commutes with actual proof-relevant concatenation,
not merely the total Nat depth or categorical composite. -/
theorem KuuNativeAxisTrace.map_append
    (H : A ⥤ C)
    {a b : A} {n m : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    (h : KuuNativeAxisTrace n ma mb)
    (k : KuuNativeAxisTrace m mb mc) :
    (h.append k).map H = (h.map H).append (k.map H) := by
  induction k with
  | refl =>
      rfl
  | snoc k step ih =>
      change KuuNativeAxisTrace.snoc
          ((h.append k).map H) (step.map H) =
        KuuNativeAxisTrace.snoc
          ((h.map H).append (k.map H)) (step.map H)
      exact congrArg (fun z => KuuNativeAxisTrace.snoc z (step.map H)) (ih h)

/-- The old-F19/F28-shaped TWO COMPLETE Type-valued histories of
ANY genuinely C60-anchored and arbitrarily bracketed F45 tree
commute with arbitrary independent category functor transport. -/
theorem KuuNativeF45Tree.axisHistories_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).axisHistories =
      (tree.axisHistories.1.map F, tree.axisHistories.2.map G) := by
  induction tree with
  | refl i ma pa =>
      rfl
  | leaf i order firstAxis secondAxis =>
      rfl
  | node first second ihFirst ihSecond =>
      apply Prod.ext
      · change
          (first.mapAxes F G).axisHistories.1.append
            (second.mapAxes F G).axisHistories.1 =
          (first.axisHistories.1.append second.axisHistories.1).map F
        rw [KuuNativeAxisTrace.map_append]
        exact congrArg₂ (fun t s => t.append s)
          (congrArg (fun z => z.1) ihFirst)
          (congrArg (fun z => z.1) ihSecond)
      · change
          (first.mapAxes F G).axisHistories.2.append
            (second.mapAxes F G).axisHistories.2 =
          (first.axisHistories.2.append second.axisHistories.2).map G
        rw [KuuNativeAxisTrace.map_append]
        exact congrArg₂ (fun t s => t.append s)
          (congrArg (fun z => z.2) ihFirst)
          (congrArg (fun z => z.2) ihSecond)

/-- Map F45 then quotient F44 = quotient F44 then map two axes.
This is strict equality of ACTUAL generated exchange classes,
proved by the verified fully Type-valued history classification,
not by a guessed equality of F44 raw interleaving constructors. -/
theorem KuuNativeF45Tree.executeF44_class_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ((tree.mapAxes F G).executeF44).toExchangeClass =
      (tree.executeF44.toExchangeClass).mapAxes F G := by
  apply (KuuNativeF44ExchangeClass.historyEquiv
    (ma.map F) (mb.map F) (pa.map G) (pb.map G)).injective
  have ht : tree.executeF44.toExchangeClass.histories = tree.axisHistories :=
    (tree.executeF44.histories_toExchangeClass).trans
      tree.executeF44_histories
  calc
    ((tree.mapAxes F G).executeF44).toExchangeClass.histories =
        (tree.mapAxes F G).axisHistories :=
      (tree.mapAxes F G).executeF44.histories_toExchangeClass.trans
        (tree.mapAxes F G).executeF44_histories
    _ = (tree.axisHistories.1.map F, tree.axisHistories.2.map G) :=
      tree.axisHistories_mapAxes F G
    _ = (tree.executeF44.toExchangeClass.histories.1.map F,
         tree.executeF44.toExchangeClass.histories.2.map G) :=
      congrArg (fun h => (h.1.map F, h.2.map G)) ht.symm
    _ = (tree.executeF44.toExchangeClass.mapAxes F G).histories :=
      (tree.executeF44.toExchangeClass.histories_mapAxes F G).symm

/-- Full independent F45 execution PACKET naturality; the true
C60 physical bracketing is the first component, while the second
is the freely generated genuine F44 exchange quotient. -/
theorem KuuNativeF45Tree.exchangePacket_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).exchangePacket =
      (tree.exchangePacket.1, tree.exchangePacket.2.mapAxes F G) := by
  apply Prod.ext
  · exact tree.erasePhysical_mapAxes F G
  · exact tree.executeF44_class_mapAxes F G

/-- Every actual geometric C60 source sector stays in precisely
its original order across the chosen F44 exchange-quotient map. -/
theorem KuuNativeF45Tree.exchangePacket_mapAxes_sectors
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa pb) :
    (tree.mapAxes F G).exchangePacket.1.erase.leaves =
      tree.sectors := by
  calc
    _ = (tree.mapAxes F G).sectors :=
      (tree.mapAxes F G).exchangePacket_sectors
    _ = tree.sectors := tree.sectors_mapAxes F G

/-- The genuine source's complete Type-valued F19/F28 histories
also survive the F45-to-F44-quotient functorial execution square. -/
theorem KuuNativeF45Tree.exchangePacket_mapAxes_histories
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa pb) :
    (tree.mapAxes F G).exchangePacket.2.histories =
      (tree.axisHistories.1.map F, tree.axisHistories.2.map G) := by
  calc
    _ = (tree.mapAxes F G).axisHistories :=
      (tree.mapAxes F G).exchangePacket_histories
    _ = _ := tree.axisHistories_mapAxes F G

/-- The true physical north-C60-pentagon two-stage F45 source
instantiates both independent functor arrows without raw erasure. -/
theorem northNativeF45TwoStages_exchangePacket_mapAxes
    (F : Site ⥤ C) (G : Site ⥤ D) :
    (northNativeF45TwoStages.mapAxes F G).exchangePacket =
      (northNativeF45TwoStages.exchangePacket.1,
        northNativeF45TwoStages.exchangePacket.2.mapAxes F G) :=
  KuuNativeF45Tree.exchangePacket_mapAxes F G northNativeF45TwoStages

#print axioms KuuNativeAxisTrace.map_append
#print axioms KuuNativeF45Tree.axisHistories_mapAxes
#print axioms KuuNativeF45Tree.executeF44_class_mapAxes
#print axioms KuuNativeF45Tree.exchangePacket_mapAxes
#print axioms KuuNativeF45Tree.exchangePacket_mapAxes_sectors
#print axioms KuuNativeF45Tree.exchangePacket_mapAxes_histories
#print axioms northNativeF45TwoStages_exchangePacket_mapAxes
end
end Kuu.F112.Physical
