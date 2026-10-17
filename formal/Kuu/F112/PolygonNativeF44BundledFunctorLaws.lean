import Kuu.F112.PolygonNativeF45ExchangePacketFunctorLaws

/-!
# F112-E7Q5-F4-O6 — bundled F44 exchange and complete-history functor laws

The O4 laws compare dependent exchange-class fibers by HEq. Here we
retain all FOUR native Blocks indices together with the actual
exchange class, or with BOTH complete Type-valued histories. Thus the
same laws become ordinary equalities of entire dependent packets.

The old M3 historyEquiv lifts to an equivalence of these packets and
commutes with arbitrary independent category functors. No endpoint,
primitive evidence, or intra-axis execution history is forgotten.
This is still the independently generated adjacent-exchange quotient,
not an equivalence with frozen historical F19/F28 or Gray sources.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD uE vE uR vR
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {R : Type uR} [Category.{vR} R]

/-- Four indexed native block presentations and their genuine
adjacent-exchange class are one dependent datum. -/
structure KuuNativeF44BundledExchange (a b : A) (x y : B) (n m : Nat) where
  firstSource : KuuNativeBlocks a b
  firstTarget : KuuNativeBlocks a b
  secondSource : KuuNativeBlocks x y
  secondTarget : KuuNativeBlocks x y
  execution : KuuNativeF44ExchangeClass n m
    firstSource firstTarget secondSource secondTarget

/-- The same FOUR endpoints with two uncollapsed Type-valued
primitive histories. These are not Prop existence certificates. -/
structure KuuNativeF44BundledHistories (a b : A) (x y : B) (n m : Nat) where
  firstSource : KuuNativeBlocks a b
  firstTarget : KuuNativeBlocks a b
  secondSource : KuuNativeBlocks x y
  secondTarget : KuuNativeBlocks x y
  firstHistory : KuuNativeAxisTrace n firstSource firstTarget
  secondHistory : KuuNativeAxisTrace m secondSource secondTarget

/-- Equality of the packet requires the actual class witness,
not merely its four endpoint presentations. -/
theorem KuuNativeF44BundledExchange.ext
    {a b : A} {x y : B} {n m : Nat}
    {s t : KuuNativeF44BundledExchange a b x y n m}
    (h₁ : s.firstSource = t.firstSource)
    (h₂ : s.firstTarget = t.firstTarget)
    (h₃ : s.secondSource = t.secondSource)
    (h₄ : s.secondTarget = t.secondTarget)
    (hw : HEq s.execution t.execution) : s = t := by
  cases s
  cases t
  cases h₁
  cases h₂
  cases h₃
  cases h₄
  cases (eq_of_heq hw)
  rfl

/-- Both complete proof-relevant histories must agree to identify
two bundled history packets. -/
theorem KuuNativeF44BundledHistories.ext
    {a b : A} {x y : B} {n m : Nat}
    {s t : KuuNativeF44BundledHistories a b x y n m}
    (h₁ : s.firstSource = t.firstSource)
    (h₂ : s.firstTarget = t.firstTarget)
    (h₃ : s.secondSource = t.secondSource)
    (h₄ : s.secondTarget = t.secondTarget)
    (hf : HEq s.firstHistory t.firstHistory)
    (hs : HEq s.secondHistory t.secondHistory) : s = t := by
  cases s
  cases t
  cases h₁
  cases h₂
  cases h₃
  cases h₄
  cases (eq_of_heq hf)
  cases (eq_of_heq hs)
  rfl

/-- Transport all packet indices together with the actual class. -/
def KuuNativeF44BundledExchange.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    KuuNativeF44BundledExchange (F.obj a) (F.obj b)
      (G.obj x) (G.obj y) n m :=
  ⟨s.firstSource.map F, s.firstTarget.map F,
    s.secondSource.map G, s.secondTarget.map G, s.execution.mapAxes F G⟩

/-- Independently map the two complete Type-valued histories. -/
def KuuNativeF44BundledHistories.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    KuuNativeF44BundledHistories (F.obj a) (F.obj b)
      (G.obj x) (G.obj y) n m :=
  ⟨s.firstSource.map F, s.firstTarget.map F,
    s.secondSource.map G, s.secondTarget.map G,
    s.firstHistory.map F, s.secondHistory.map G⟩

/-- The heterogeneous fiber law becomes an ordinary equality of
complete packets without erasing any of their dependent indices. -/
theorem KuuNativeF44BundledExchange.mapAxes_id
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  apply KuuNativeF44BundledExchange.ext
  · exact KuuNativeBlocks.map_id s.firstSource
  · exact KuuNativeBlocks.map_id s.firstTarget
  · exact KuuNativeBlocks.map_id s.secondSource
  · exact KuuNativeBlocks.map_id s.secondTarget
  · exact KuuNativeF44ExchangeClass.mapAxes_id_heq s.execution

/-- Composition likewise holds as ordinary packet equality. -/
theorem KuuNativeF44BundledExchange.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  apply KuuNativeF44BundledExchange.ext
  · exact KuuNativeBlocks.map_comp F H s.firstSource
  · exact KuuNativeBlocks.map_comp F H s.firstTarget
  · exact KuuNativeBlocks.map_comp G I s.secondSource
  · exact KuuNativeBlocks.map_comp G I s.secondTarget
  · exact KuuNativeF44ExchangeClass.mapAxes_comp_heq F H G I s.execution

/-- Identity of complete history packets preserves primitive proof
terms, not merely their categorical composites or exact Nat lengths. -/
theorem KuuNativeF44BundledHistories.mapAxes_id
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  apply KuuNativeF44BundledHistories.ext
  · exact KuuNativeBlocks.map_id s.firstSource
  · exact KuuNativeBlocks.map_id s.firstTarget
  · exact KuuNativeBlocks.map_id s.secondSource
  · exact KuuNativeBlocks.map_id s.secondTarget
  · exact KuuNativeAxisTrace.map_id_heq s.firstHistory
  · exact KuuNativeAxisTrace.map_id_heq s.secondHistory

/-- Both independent primitive histories compose functorially as
whole dependent packets. -/
theorem KuuNativeF44BundledHistories.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  apply KuuNativeF44BundledHistories.ext
  · exact KuuNativeBlocks.map_comp F H s.firstSource
  · exact KuuNativeBlocks.map_comp F H s.firstTarget
  · exact KuuNativeBlocks.map_comp G I s.secondSource
  · exact KuuNativeBlocks.map_comp G I s.secondTarget
  · exact KuuNativeAxisTrace.map_comp_heq F H s.firstHistory
  · exact KuuNativeAxisTrace.map_comp_heq G I s.secondHistory

/-- Observe both exact histories while keeping their four indices. -/
def KuuNativeF44BundledExchange.histories
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    KuuNativeF44BundledHistories a b x y n m :=
  ⟨s.firstSource, s.firstTarget, s.secondSource, s.secondTarget,
    s.execution.histories.1, s.execution.histories.2⟩

/-- Reconstruct the actual generated class using the PROVED M3
inverse, not a choice of raw order asserted equal by endpoints. -/
def KuuNativeF44BundledHistories.toExchange
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    KuuNativeF44BundledExchange a b x y n m :=
  ⟨s.firstSource, s.firstTarget, s.secondSource, s.secondTarget,
    (KuuNativeF44ExchangeClass.historyEquiv s.firstSource s.firstTarget
      s.secondSource s.secondTarget).symm (s.firstHistory, s.secondHistory)⟩

/-- No extra quotient is introduced by bundling: recovering the
class from its full history packet is a left inverse. -/
theorem KuuNativeF44BundledExchange.histories_toExchange
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    s.histories.toExchange = s := by
  apply KuuNativeF44BundledExchange.ext rfl rfl rfl rfl
  exact heq_of_eq ((KuuNativeF44ExchangeClass.historyEquiv
    s.firstSource s.firstTarget s.secondSource s.secondTarget).symm_apply_apply s.execution)

/-- Both complete Type-valued histories are recovered, not just
their endpoints or existence. -/
theorem KuuNativeF44BundledHistories.toExchange_histories
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    s.toExchange.histories = s := by
  have h := (KuuNativeF44ExchangeClass.historyEquiv
    s.firstSource s.firstTarget s.secondSource s.secondTarget).apply_symm_apply
      (s.firstHistory, s.secondHistory)
  apply KuuNativeF44BundledHistories.ext rfl rfl rfl rfl
  · exact heq_of_eq (congrArg Prod.fst h)
  · exact heq_of_eq (congrArg Prod.snd h)

/-- The previously fiberwise classification is an equivalence of
entire indexed presentations, with ordinary inverse equations. -/
def kuuNativeF44BundledHistoryEquiv
    {a b : A} {x y : B} {n m : Nat} :
    KuuNativeF44BundledExchange a b x y n m ≃
      KuuNativeF44BundledHistories a b x y n m where
  toFun := KuuNativeF44BundledExchange.histories
  invFun := KuuNativeF44BundledHistories.toExchange
  left_inv := KuuNativeF44BundledExchange.histories_toExchange
  right_inv := KuuNativeF44BundledHistories.toExchange_histories

/-- The classification square commutes as ordinary equality of
complete history packets under arbitrary independent functors. -/
theorem KuuNativeF44BundledExchange.histories_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledExchange a b x y n m) :
    (s.mapAxes F G).histories = s.histories.mapAxes F G := by
  apply KuuNativeF44BundledHistories.ext rfl rfl rfl rfl
  · exact heq_of_eq (congrArg Prod.fst (s.execution.histories_mapAxes F G))
  · exact heq_of_eq (congrArg Prod.snd (s.execution.histories_mapAxes F G))

#print axioms KuuNativeF44BundledExchange.ext
#print axioms KuuNativeF44BundledHistories.ext
#print axioms KuuNativeF44BundledExchange.mapAxes_id
#print axioms KuuNativeF44BundledExchange.mapAxes_comp
#print axioms KuuNativeF44BundledHistories.mapAxes_id
#print axioms KuuNativeF44BundledHistories.mapAxes_comp
#print axioms kuuNativeF44BundledHistoryEquiv
#print axioms KuuNativeF44BundledExchange.histories_mapAxes
end
end Kuu.F112.Physical
