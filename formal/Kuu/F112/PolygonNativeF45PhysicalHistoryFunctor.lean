import Kuu.F112.PolygonNativeF44TotalCategoryFunctor

/-!
# F112-E7Q5-F4-O8-A — physically bracketed complete-history natural isomorphism

For every actual C60 polygon and every pair of Nat depths, retain
its ENTIRE PolygonDepthTree alongside all four categorical endpoint
objects, four native Blocks, and the generated F44 exchange class.
The corresponding history presentation retains the SAME physical
tree and BOTH complete Type-valued primitive histories.

The equivalence acts identically on physical data and is natural in
arbitrary independent category functors. Forgetting the physical
component recovers the previously certified O7 total equivalence.
These are ambient typed packets; no raw F45 reconstruction or
surjectivity from raw F45 trees is asserted. No frozen KUOS imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD uE vE uR vR

/-- A genuine physical bracket and a full dependent exchange packet. -/
def KuuNativeF45PhysicalExchange (p : Polygon) (n m : Nat)
    (A : Type uA) [Category.{vA} A] (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B,
    PolygonDepthTree p n m × KuuNativeF44BundledExchange a b x y n m

/-- The same physical bracket with both complete primitive histories. -/
def KuuNativeF45PhysicalHistories (p : Polygon) (n m : Nat)
    (A : Type uA) [Category.{vA} A] (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B,
    PolygonDepthTree p n m × KuuNativeF44BundledHistories a b x y n m

variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {R : Type uR} [Category.{vR} R]
variable {p : Polygon} {n m : Nat}

def KuuNativeF45PhysicalExchange.mapAxes (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    KuuNativeF45PhysicalExchange p n m C D :=
  match s with
  | ⟨a, b, x, y, t, w⟩ =>
      ⟨F.obj a, F.obj b, G.obj x, G.obj y, t, w.mapAxes F G⟩

def KuuNativeF45PhysicalHistories.mapAxes (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    KuuNativeF45PhysicalHistories p n m C D :=
  match s with
  | ⟨a, b, x, y, t, w⟩ =>
      ⟨F.obj a, F.obj b, G.obj x, G.obj y, t, w.mapAxes F G⟩

def KuuNativeF45PhysicalExchange.physical
    (s : KuuNativeF45PhysicalExchange p n m A B) : PolygonDepthTree p n m :=
  match s with
  | ⟨_, _, _, _, t, _⟩ => t

def KuuNativeF45PhysicalHistories.physical
    (s : KuuNativeF45PhysicalHistories p n m A B) : PolygonDepthTree p n m :=
  match s with
  | ⟨_, _, _, _, t, _⟩ => t

theorem KuuNativeF45PhysicalExchange.physical_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    (s.mapAxes F G).physical = s.physical := by
  rcases s with ⟨a, b, x, y, t, w⟩
  rfl

theorem KuuNativeF45PhysicalExchange.mapAxes_id
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledExchange a b x y n m =>
      (⟨a, b, x, y, t, z⟩ : KuuNativeF45PhysicalExchange p n m A B))
    w.mapAxes_id

theorem KuuNativeF45PhysicalExchange.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledExchange (H.obj (F.obj a)) (H.obj (F.obj b))
        (I.obj (G.obj x)) (I.obj (G.obj y)) n m =>
      (⟨H.obj (F.obj a), H.obj (F.obj b), I.obj (G.obj x), I.obj (G.obj y), t, z⟩ :
        KuuNativeF45PhysicalExchange p n m E R))
    (w.mapAxes_comp F G H I)

theorem KuuNativeF45PhysicalHistories.mapAxes_id
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    s.mapAxes (𝟭 A) (𝟭 B) = s := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories a b x y n m =>
      (⟨a, b, x, y, t, z⟩ : KuuNativeF45PhysicalHistories p n m A B))
    w.mapAxes_id

theorem KuuNativeF45PhysicalHistories.mapAxes_comp
    (F : A ⥤ C) (G : B ⥤ D) (H : C ⥤ E) (I : D ⥤ R)
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    s.mapAxes (F ⋙ H) (G ⋙ I) = (s.mapAxes F G).mapAxes H I := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories (H.obj (F.obj a)) (H.obj (F.obj b))
        (I.obj (G.obj x)) (I.obj (G.obj y)) n m =>
      (⟨H.obj (F.obj a), H.obj (F.obj b), I.obj (G.obj x), I.obj (G.obj y), t, z⟩ :
        KuuNativeF45PhysicalHistories p n m E R))
    (w.mapAxes_comp F G H I)

/-- Fiberwise O6 classification with exactly the same physical bracket. -/
def kuuNativeF45PhysicalHistoryEquiv (p : Polygon) (n m : Nat)
    (A : Type uA) [Category.{vA} A] (B : Type uB) [Category.{vB} B] :
    KuuNativeF45PhysicalExchange p n m A B ≃
      KuuNativeF45PhysicalHistories p n m A B where
  toFun := fun ⟨a, b, x, y, t, w⟩ => ⟨a, b, x, y, t, w.histories⟩
  invFun := fun ⟨a, b, x, y, t, w⟩ => ⟨a, b, x, y, t, w.toExchange⟩
  left_inv := by
    rintro ⟨a, b, x, y, t, w⟩
    exact congrArg
      (fun z : KuuNativeF44BundledExchange a b x y n m =>
        (⟨a, b, x, y, t, z⟩ : KuuNativeF45PhysicalExchange p n m A B))
      w.histories_toExchange
  right_inv := by
    rintro ⟨a, b, x, y, t, w⟩
    exact congrArg
      (fun z : KuuNativeF44BundledHistories a b x y n m =>
        (⟨a, b, x, y, t, z⟩ : KuuNativeF45PhysicalHistories p n m A B))
      w.toExchange_histories

theorem kuuNativeF45PhysicalHistoryEquiv_physical
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    (kuuNativeF45PhysicalHistoryEquiv p n m A B s).physical = s.physical := by
  rcases s with ⟨a, b, x, y, t, w⟩
  rfl

theorem kuuNativeF45PhysicalHistoryEquiv_naturality
    (F : A ⥤ C) (G : B ⥤ D)
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    kuuNativeF45PhysicalHistoryEquiv p n m C D (s.mapAxes F G) =
      (kuuNativeF45PhysicalHistoryEquiv p n m A B s).mapAxes F G := by
  rcases s with ⟨a, b, x, y, t, w⟩
  exact congrArg
    (fun z : KuuNativeF44BundledHistories (F.obj a) (F.obj b)
        (G.obj x) (G.obj y) n m =>
      (⟨F.obj a, F.obj b, G.obj x, G.obj y, t, z⟩ :
        KuuNativeF45PhysicalHistories p n m C D))
    (w.histories_mapAxes F G)

/-- Forget only physical metadata, preserving every O7 categorical index. -/
def KuuNativeF45PhysicalExchange.forgetPhysical
    (s : KuuNativeF45PhysicalExchange p n m A B) : KuuNativeF44TotalExchange A B :=
  match s with
  | ⟨a, b, x, y, _, w⟩ => ⟨a, b, x, y, n, m, w⟩

def KuuNativeF45PhysicalHistories.forgetPhysical
    (s : KuuNativeF45PhysicalHistories p n m A B) : KuuNativeF44TotalHistories A B :=
  match s with
  | ⟨a, b, x, y, _, w⟩ => ⟨a, b, x, y, n, m, w⟩

/-- The physical extension recovers the exact O7 classification square. -/
theorem kuuNativeF45PhysicalHistoryEquiv_forget
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    (kuuNativeF45PhysicalHistoryEquiv p n m A B s).forgetPhysical =
      kuuNativeF44TotalHistoryEquiv A B s.forgetPhysical := by
  rcases s with ⟨a, b, x, y, t, w⟩
  rfl

/-- Actual Cat-pair functor with physical polygon brackets retained. -/
def kuuNativeF45PhysicalExchangeFunctor (p : Polygon) (n m : Nat) :
    (Cat.{vA, uA} × Cat.{vB, uB}) ⥤ Type (max (max uA uB) (max vA vB)) where
  obj X := KuuNativeF45PhysicalExchange p n m X.1 X.2
  map f := TypeCat.ofHom
    (KuuNativeF45PhysicalExchange.mapAxes f.1.toFunctor f.2.toFunctor)
  map_id X := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF45PhysicalExchange.mapAxes_id s
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF45PhysicalExchange.mapAxes_comp
      f.1.toFunctor f.2.toFunctor g.1.toFunctor g.2.toFunctor s

def kuuNativeF45PhysicalHistoryFunctor (p : Polygon) (n m : Nat) :
    (Cat.{vA, uA} × Cat.{vB, uB}) ⥤ Type (max (max uA uB) (max vA vB)) where
  obj X := KuuNativeF45PhysicalHistories p n m X.1 X.2
  map f := TypeCat.ofHom
    (KuuNativeF45PhysicalHistories.mapAxes f.1.toFunctor f.2.toFunctor)
  map_id X := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF45PhysicalHistories.mapAxes_id s
  map_comp f g := by
    apply ConcreteCategory.hom_ext
    intro s
    exact KuuNativeF45PhysicalHistories.mapAxes_comp
      f.1.toFunctor f.2.toFunctor g.1.toFunctor g.2.toFunctor s

/-- Natural isomorphism, identity on the actual physical bracket. -/
def kuuNativeF45PhysicalHistoryNatIso (p : Polygon) (n m : Nat) :
    kuuNativeF45PhysicalExchangeFunctor.{uA, vA, uB, vB} p n m ≅
      kuuNativeF45PhysicalHistoryFunctor.{uA, vA, uB, vB} p n m :=
  NatIso.ofComponents
    (fun X => (kuuNativeF45PhysicalHistoryEquiv p n m X.1 X.2).toIso)
    (by
      intro X Y f
      apply ConcreteCategory.hom_ext
      intro s
      exact kuuNativeF45PhysicalHistoryEquiv_naturality
        f.1.toFunctor f.2.toFunctor s)

#print axioms KuuNativeF45PhysicalExchange.physical_mapAxes
#print axioms KuuNativeF45PhysicalExchange.mapAxes_id
#print axioms KuuNativeF45PhysicalExchange.mapAxes_comp
#print axioms KuuNativeF45PhysicalHistories.mapAxes_id
#print axioms KuuNativeF45PhysicalHistories.mapAxes_comp
#print axioms kuuNativeF45PhysicalHistoryEquiv
#print axioms kuuNativeF45PhysicalHistoryEquiv_physical
#print axioms kuuNativeF45PhysicalHistoryEquiv_naturality
#print axioms kuuNativeF45PhysicalHistoryEquiv_forget
#print axioms kuuNativeF45PhysicalExchangeFunctor
#print axioms kuuNativeF45PhysicalHistoryFunctor
#print axioms kuuNativeF45PhysicalHistoryNatIso
end
end Kuu.F112.Physical
