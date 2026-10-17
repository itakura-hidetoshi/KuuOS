import Mathlib.CategoryTheory.Category.Cat
import Mathlib.CategoryTheory.Products.Basic
import Mathlib.CategoryTheory.NatIso
import Kuu.F112.PolygonNativeF44BundledFunctorLaws

/-!
# F112-E7Q5-F4-O7 — genuine Cat-pair functors and natural history isomorphism

Bundle the category objects and both Nat depths as well as the O6
packets. The source is the ordinary product category Cat × Cat;
its morphisms are pairs of independently chosen ordinary functors.

The previously proved dependent laws now discharge actual Mathlib
Functor.map_id and Functor.map_comp fields. The complete-history
classification is a NatIso of these Type-valued functors. This
certifies the NEW generated F44 exchange quotient only, not frozen
historical F19/F28, a Gray reconstruction, or physical F47 descent.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD uE vE uR vR

/-- All categorical endpoint objects, exact depths and dependent
F44 exchange presentations, without dropping the four Blocks. -/
def KuuNativeF44TotalExchange (A : Type uA) [Category.{vA} A]
    (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B, Σ n : Nat, Σ m : Nat,
    KuuNativeF44BundledExchange a b x y n m

/-- The corresponding total space of BOTH full Type-valued
primitive histories and all their categorical indices. -/
def KuuNativeF44TotalHistories (A : Type uA) [Category.{vA} A]
    (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B, Σ n : Nat, Σ m : Nat,
    KuuNativeF44BundledHistories a b x y n m

variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {R : Type uR} [Category.{vR} R]

/-- Total source transport maps the actual endpoint objects too. -/
def KuuNativeF44TotalExchange.mapAxes (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF44TotalExchange A B) : KuuNativeF44TotalExchange C D :=
  match s with
  | ⟨a, b, x, y, n, m, w⟩ =>
      ⟨F.obj a, F.obj b, G.obj x, G.obj y, n, m, w.mapAxes F G⟩

/-- Transport all endpoint objects and both exact primitive histories. -/
def KuuNativeF44TotalHistories.mapAxes (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF44TotalHistories A B) : KuuNativeF44TotalHistories C D :=
  match s with
  | ⟨a, b, x, y, n, m, w⟩ =>
      ⟨F.obj a, F.obj b, G.obj x, G.obj y, n, m, w.mapAxes F G⟩

theorem KuuNativeF44TotalExchange.mapAxes_id
    (s : KuuNativeF44TotalExchange A B) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  rcases s with ⟨a, b, x, y, n, m, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledExchange a b x y n m =>
      (⟨a, b, x, y, n, m, z⟩ : KuuNativeF44TotalExchange A B))
    w.mapAxes_id

theorem KuuNativeF44TotalExchange.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    (s : KuuNativeF44TotalExchange A B) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  rcases s with ⟨a, b, x, y, n, m, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledExchange (H.obj (F.obj a)) (H.obj (F.obj b))
        (I.obj (G.obj x)) (I.obj (G.obj y)) n m =>
      (⟨H.obj (F.obj a), H.obj (F.obj b), I.obj (G.obj x),
        I.obj (G.obj y), n, m, z⟩ : KuuNativeF44TotalExchange E R))
    (w.mapAxes_comp F G H I)

theorem KuuNativeF44TotalHistories.mapAxes_id
    (s : KuuNativeF44TotalHistories A B) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  rcases s with ⟨a, b, x, y, n, m, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories a b x y n m =>
      (⟨a, b, x, y, n, m, z⟩ : KuuNativeF44TotalHistories A B))
    w.mapAxes_id

theorem KuuNativeF44TotalHistories.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    (s : KuuNativeF44TotalHistories A B) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  rcases s with ⟨a, b, x, y, n, m, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories (H.obj (F.obj a)) (H.obj (F.obj b))
        (I.obj (G.obj x)) (I.obj (G.obj y)) n m =>
      (⟨H.obj (F.obj a), H.obj (F.obj b), I.obj (G.obj x),
        I.obj (G.obj y), n, m, z⟩ : KuuNativeF44TotalHistories E R))
    (w.mapAxes_comp F G H I)

/-- The classification preserves ALL endpoint objects, Nat depths,
four Blocks and both Type-valued histories. -/
def kuuNativeF44TotalHistoryEquiv (A : Type uA) [Category.{vA} A]
    (B : Type uB) [Category.{vB} B] :
    KuuNativeF44TotalExchange A B ≃ KuuNativeF44TotalHistories A B where
  toFun := fun ⟨a, b, x, y, n, m, w⟩ => ⟨a, b, x, y, n, m, w.histories⟩
  invFun := fun ⟨a, b, x, y, n, m, w⟩ => ⟨a, b, x, y, n, m, w.toExchange⟩
  left_inv := by
    rintro ⟨a, b, x, y, n, m, w⟩
    exact congrArg
      (fun z : KuuNativeF44BundledExchange a b x y n m =>
        (⟨a, b, x, y, n, m, z⟩ : KuuNativeF44TotalExchange A B))
      w.histories_toExchange
  right_inv := by
    rintro ⟨a, b, x, y, n, m, w⟩
    exact congrArg
      (fun z : KuuNativeF44BundledHistories a b x y n m =>
        (⟨a, b, x, y, n, m, z⟩ : KuuNativeF44TotalHistories A B))
      w.toExchange_histories

/-- Ordinary equality of the complete total presentations in the
naturality square, not an equality after further information loss. -/
theorem kuuNativeF44TotalHistoryEquiv_naturality
    (F : A ⥤ C) (G : B ⥤ D) (s : KuuNativeF44TotalExchange A B) :
    kuuNativeF44TotalHistoryEquiv C D (s.mapAxes F G) =
      (kuuNativeF44TotalHistoryEquiv A B s).mapAxes F G := by
  rcases s with ⟨a, b, x, y, n, m, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories (F.obj a) (F.obj b)
        (G.obj x) (G.obj y) n m =>
      (⟨F.obj a, F.obj b, G.obj x, G.obj y, n, m, z⟩ :
        KuuNativeF44TotalHistories C D))
    (w.histories_mapAxes F G)

/-- An ACTUAL Mathlib functor on pairs of categories. Its map_id
and map_comp fields are proved from the original dependent witnesses. -/
def kuuNativeF44ExchangeTypeFunctor :
    (Cat.{vA, uA} × Cat.{vB, uB}) ⥤
      Type (max (max uA uB) (max vA vB)) where
  obj X := KuuNativeF44TotalExchange X.1 X.2
  map f := TypeCat.ofHom
    (KuuNativeF44TotalExchange.mapAxes f.1.toFunctor f.2.toFunctor)
  map_id X := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF44TotalExchange.mapAxes_id s
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF44TotalExchange.mapAxes_comp
      f.1.toFunctor f.2.toFunctor g.1.toFunctor g.2.toFunctor s

/-- An ACTUAL Mathlib functor carrying all endpoint data and the
two separate complete Type-valued primitive histories. -/
def kuuNativeF44HistoryTypeFunctor :
    (Cat.{vA, uA} × Cat.{vB, uB}) ⥤
      Type (max (max uA uB) (max vA vB)) where
  obj X := KuuNativeF44TotalHistories X.1 X.2
  map f := TypeCat.ofHom
    (KuuNativeF44TotalHistories.mapAxes f.1.toFunctor f.2.toFunctor)
  map_id X := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF44TotalHistories.mapAxes_id s
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF44TotalHistories.mapAxes_comp
      f.1.toFunctor f.2.toFunctor g.1.toFunctor g.2.toFunctor s

/-- Complete classification as a NATURAL ISOMORPHISM of the two
actual Cat-pair functors. This does not assert that an arbitrary
category functor is faithful on raw primitive evidence. -/
def kuuNativeF44HistoryNatIso :
    kuuNativeF44ExchangeTypeFunctor.{uA, vA, uB, vB} ≅
      kuuNativeF44HistoryTypeFunctor.{uA, vA, uB, vB} :=
  NatIso.ofComponents
    (fun X => (kuuNativeF44TotalHistoryEquiv X.1 X.2).toIso)
    (by
      intro X Y f
      apply ConcreteCategory.hom_ext
      intro s
      exact kuuNativeF44TotalHistoryEquiv_naturality
        f.1.toFunctor f.2.toFunctor s)

#print axioms KuuNativeF44TotalExchange.mapAxes_id
#print axioms KuuNativeF44TotalExchange.mapAxes_comp
#print axioms KuuNativeF44TotalHistories.mapAxes_id
#print axioms KuuNativeF44TotalHistories.mapAxes_comp
#print axioms kuuNativeF44TotalHistoryEquiv
#print axioms kuuNativeF44TotalHistoryEquiv_naturality
#print axioms kuuNativeF44ExchangeTypeFunctor
#print axioms kuuNativeF44HistoryTypeFunctor
#print axioms kuuNativeF44HistoryNatIso
end
end Kuu.F112.Physical
