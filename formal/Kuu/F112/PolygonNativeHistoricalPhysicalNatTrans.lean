import Kuu.F112.PolygonNativeHistoricalEvidenceFunctorNaturality
import Kuu.F112.PolygonNativeF45PhysicalHistoryFunctor

/-!
# F112-E7Q5-F4-P2-B — two-category natural transformation of C60 packets

For every genuine C60 polygon and arbitrary independent Nat depths,
we transport the historical-shaped Prop-step, Type-history packet
along TWO unrelated ordinary category functors.

All four category endpoints, four native Blocks, full binary C60
bracket/sector leaves and each intermediate Type-valued history survive.

The O8 complete-history functor and this historical-shaped functor
are actual Mathlib functors on Cat × Cat. Proof-evidence erasure is
a true NatTrans between them, never a claimed NatIso: P1 already
certifies native split/insertNil noninjectivity. Chosen raw lifts
commute with category transport only AFTER observed evidence erasure;
no unsupported raw choice naturality is assumed.

No historical KUOS or Gray imported; no F19/F28 ambient equivalence.
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
variable {p : Polygon} {n m : Nat}

/-- The four native endpoint Blocks and complete historical-shaped
Type-valued histories are each transported in their own category. -/
def KuuNativeHistoricalF44Histories.mapAxes (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeHistoricalF44Histories a b x y n m) :
    KuuNativeHistoricalF44Histories (F.obj a) (F.obj b)
      (G.obj x) (G.obj y) n m :=
  ⟨s.firstSource.map F, s.firstTarget.map F,
    s.secondSource.map G, s.secondTarget.map G,
    s.firstHistory.map F, s.secondHistory.map G⟩

/-- The ORIGINAL indices must be equal before comparing dependent
histories; proof irrelevance is applied ONLY to Prop elementary steps. -/
theorem KuuNativeHistoricalF44Histories.ext
    {a b : A} {x y : B} {n m : Nat}
    {s t : KuuNativeHistoricalF44Histories a b x y n m}
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

theorem KuuNativeHistoricalF44Histories.mapAxes_id
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeHistoricalF44Histories a b x y n m) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  apply KuuNativeHistoricalF44Histories.ext
  · exact KuuNativeBlocks.map_id s.firstSource
  · exact KuuNativeBlocks.map_id s.firstTarget
  · exact KuuNativeBlocks.map_id s.secondSource
  · exact KuuNativeBlocks.map_id s.secondTarget
  · exact KuuNativeHistoricalAxisTrace.map_id_heq s.firstHistory
  · exact KuuNativeHistoricalAxisTrace.map_id_heq s.secondHistory

theorem KuuNativeHistoricalF44Histories.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeHistoricalF44Histories a b x y n m) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  apply KuuNativeHistoricalF44Histories.ext
  · exact KuuNativeBlocks.map_comp F H s.firstSource
  · exact KuuNativeBlocks.map_comp F H s.firstTarget
  · exact KuuNativeBlocks.map_comp G I s.secondSource
  · exact KuuNativeBlocks.map_comp G I s.secondTarget
  · exact KuuNativeHistoricalAxisTrace.map_comp_heq F H s.firstHistory
  · exact KuuNativeHistoricalAxisTrace.map_comp_heq G I s.secondHistory

/-- Forget native Type primitive evidence but retain ALL four
dependent Blocks and both Type-valued history shells. -/
def KuuNativeF44BundledHistories.toHistorical
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    KuuNativeHistoricalF44Histories a b x y n m :=
  ⟨s.firstSource, s.firstTarget, s.secondSource, s.secondTarget,
    s.firstHistory.toHistorical, s.secondHistory.toHistorical⟩

/-- The F41 elementary-erasure square is lifted to BOTH category
axes of the exact four-Blocks F44 history bundle. -/
theorem KuuNativeF44BundledHistories.toHistorical_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {a b : A} {x y : B} {n m : Nat}
    (s : KuuNativeF44BundledHistories a b x y n m) :
    (s.mapAxes F G).toHistorical = (s.toHistorical).mapAxes F G := by
  apply KuuNativeHistoricalF44Histories.ext
    (s := (s.mapAxes F G).toHistorical)
    (t := s.toHistorical.mapAxes F G) rfl rfl rfl rfl
  · exact heq_of_eq (KuuNativeAxisTrace.map_toHistorical F s.firstHistory)
  · exact heq_of_eq (KuuNativeAxisTrace.map_toHistorical G s.secondHistory)

/-- Genuine polygon sector/leaf/bracket stays literally the same;
only the four endpoints and their dependent witness packet move. -/
def KuuNativeHistoricalF45PhysicalHistories.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    KuuNativeHistoricalF45PhysicalHistories p n m C D :=
  match s with
  | ⟨a, b, x, y, t, w⟩ =>
      ⟨F.obj a, F.obj b, G.obj x, G.obj y, t, w.mapAxes F G⟩

theorem KuuNativeHistoricalF45PhysicalHistories.mapAxes_id
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeHistoricalF44Histories a b x y n m =>
      (⟨a, b, x, y, t, z⟩ :
        KuuNativeHistoricalF45PhysicalHistories p n m A B))
    w.mapAxes_id

theorem KuuNativeHistoricalF45PhysicalHistories.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    s.mapAxes (F ⋙ H) (G ⋙ I) =
      (s.mapAxes F G).mapAxes H I := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeHistoricalF44Histories
        (H.obj (F.obj a)) (H.obj (F.obj b))
        (I.obj (G.obj x)) (I.obj (G.obj y)) n m =>
      (⟨H.obj (F.obj a), H.obj (F.obj b),
        I.obj (G.obj x), I.obj (G.obj y), t, z⟩ :
        KuuNativeHistoricalF45PhysicalHistories p n m E R))
    (w.mapAxes_comp F G H I)

/-- The map from genuine O8 complete Type-valued physical histories
to old-shaped Type-valued physical histories is two-axis natural. -/
theorem KuuNativeF45PhysicalHistories.toHistorical_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    (s.mapAxes F G).toHistorical =
      (s.toHistorical).mapAxes F G := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeHistoricalF44Histories
        (F.obj a) (F.obj b) (G.obj x) (G.obj y) n m =>
      (⟨F.obj a, F.obj b, G.obj x, G.obj y, t, z⟩ :
        KuuNativeHistoricalF45PhysicalHistories p n m C D))
    (w.toHistorical_mapAxes F G)

/-- Historical C60 physical packet transports under ANY pair of
ordinary category functors, and its original physical tree is fixed. -/
theorem KuuNativeHistoricalF45PhysicalHistories.physical_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    (s.mapAxes F G).2.2.2.2.1 = s.2.2.2.2.1 := by
  rcases s with ⟨a, b, x, y, t, w⟩
  rfl

/-- After old-shaped observation, two arbitrary primitive-evidence
choices map equally, even though their raw Type witnesses need NOT
be equal before erasure. -/
theorem KuuNativeHistoricalF45PhysicalHistories.chooseNative_map_observed
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    (s.chooseNative.mapAxes F G).toHistorical =
      (s.mapAxes F G).chooseNative.toHistorical := by
  calc
    (s.chooseNative.mapAxes F G).toHistorical =
      (s.chooseNative.toHistorical).mapAxes F G :=
        s.chooseNative.toHistorical_mapAxes F G
    _ = s.mapAxes F G :=
      congrArg (KuuNativeHistoricalF45PhysicalHistories.mapAxes F G)
        s.toHistorical_chooseNative
    _ = (s.mapAxes F G).chooseNative.toHistorical :=
      ((s.mapAxes F G).toHistorical_chooseNative).symm

/-- A REAL Mathlib Cat-pair functor, not an identity on shadow grades. -/
def kuuNativeHistoricalF45PhysicalHistoryFunctor (p : Polygon) (n m : Nat) :
    (Cat.{vA, uA} × Cat.{vB, uB}) ⥤
      Type (max (max uA uB) (max vA vB)) where
  obj X := KuuNativeHistoricalF45PhysicalHistories p n m X.1 X.2
  map f := TypeCat.ofHom
    (KuuNativeHistoricalF45PhysicalHistories.mapAxes
      f.1.toFunctor f.2.toFunctor)
  map_id X := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeHistoricalF45PhysicalHistories.mapAxes_id s
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeHistoricalF45PhysicalHistories.mapAxes_comp
      f.1.toFunctor f.2.toFunctor g.1.toFunctor g.2.toFunctor s

/-- The exact primitive-evidence erasure is an ACTUAL Mathlib
natural transformation between the O8 genuine physical Type-history
functor and the historical-shaped Prop-step Type-history functor.
It is not an isomorphism by P1's noninjectivity theorem. -/
def kuuNativeF45HistoricalErasureNatTrans (p : Polygon) (n m : Nat) :
    kuuNativeF45PhysicalHistoryFunctor.{uA, vA, uB, vB} p n m ⟶
      kuuNativeHistoricalF45PhysicalHistoryFunctor.{uA, vA, uB, vB} p n m where
  app X := TypeCat.ofHom KuuNativeF45PhysicalHistories.toHistorical
  naturality X Y f := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF45PhysicalHistories.toHistorical_mapAxes
      f.1.toFunctor f.2.toFunctor s

#print axioms KuuNativeHistoricalF44Histories.mapAxes_id
#print axioms KuuNativeHistoricalF44Histories.mapAxes_comp
#print axioms KuuNativeF44BundledHistories.toHistorical_mapAxes
#print axioms KuuNativeHistoricalF45PhysicalHistories.mapAxes_id
#print axioms KuuNativeHistoricalF45PhysicalHistories.mapAxes_comp
#print axioms KuuNativeF45PhysicalHistories.toHistorical_mapAxes
#print axioms KuuNativeHistoricalF45PhysicalHistories.chooseNative_map_observed
#print axioms kuuNativeHistoricalF45PhysicalHistoryFunctor
#print axioms kuuNativeF45HistoricalErasureNatTrans
end
end Kuu.F112.Physical
