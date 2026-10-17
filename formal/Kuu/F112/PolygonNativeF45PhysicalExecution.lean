import Kuu.F112.PolygonNativeF45PhysicalHistoryFunctor

/-!
# F112-E7Q5-F4-O8-B — actual F45 execution and its exact information boundary

Execute an ACTUAL independently defined F45 tree into the O8
physically bracketed exchange/history presentations. Its real
PolygonDepthTree, categorical endpoint objects, four Blocks and
complete Type-valued per-axis histories survive, and the O8 natural
isomorphism commutes with this execution.

The map is deliberately NOT called a raw-source equivalence.
Opposite F45 leaf orders are distinct raw constructors but have the
same physical exchange packet, even at positive depths (1,1).
A zero-depth refl and leaf are also distinct and have the same packet.
No inverse of the positive-depth raw observation exists. Neither
ambient-packet realizability nor historical source equivalence is
inferred from this classification. No frozen KUOS/Gray import.
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
variable {p : Polygon} {a b : A} {x y : B} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- Actual F44 execution with all four dependent Blocks bundled. -/
def KuuNativeF45Tree.bundledExecution
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF44BundledExchange a b x y n m :=
  ⟨ma, mb, pa, pb, tree.executeF44.toExchangeClass⟩

/-- Preserve the complete physical bracket alongside the actual class. -/
def KuuNativeF45Tree.physicalExchange
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45PhysicalExchange p n m A B :=
  ⟨a, b, x, y, tree.erasePhysical, tree.bundledExecution⟩

/-- The directly observed complete histories and the SAME physical tree. -/
def KuuNativeF45Tree.physicalHistories
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45PhysicalHistories p n m A B :=
  ⟨a, b, x, y, tree.erasePhysical,
    ⟨ma, mb, pa, pb, tree.axisHistories.1, tree.axisHistories.2⟩⟩

/-- Executing and then classifying is exactly direct history observation. -/
theorem KuuNativeF45Tree.physicalHistoryEquiv_execution
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    kuuNativeF45PhysicalHistoryEquiv p n m A B tree.physicalExchange =
      tree.physicalHistories := by
  exact congrArg
    (fun h : KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb =>
      (⟨a, b, x, y, tree.erasePhysical, ⟨ma, mb, pa, pb, h.1, h.2⟩⟩ :
        KuuNativeF45PhysicalHistories p n m A B))
    tree.executeF44_histories

/-- No physical sector or parenthesis is reconstructed from a scalar. -/
theorem KuuNativeF45Tree.physicalExchange_physical
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.physicalExchange.physical = tree.erasePhysical := rfl

theorem KuuNativeF45Tree.bundledExecution_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).bundledExecution = tree.bundledExecution.mapAxes F G := by
  apply KuuNativeF44BundledExchange.ext
  · rfl
  · rfl
  · rfl
  · rfl
  · exact heq_of_eq (tree.executeF44_class_mapAxes F G)

/-- Strict naturality of actual F45 execution into physical packets. -/
theorem KuuNativeF45Tree.physicalExchange_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).physicalExchange = tree.physicalExchange.mapAxes F G := by
  exact congrArg
    (fun z : PolygonDepthTree p n m ×
        KuuNativeF44BundledExchange (F.obj a) (F.obj b) (G.obj x) (G.obj y) n m =>
      (⟨F.obj a, F.obj b, G.obj x, G.obj y, z⟩ :
        KuuNativeF45PhysicalExchange p n m C D))
    (Prod.ext (tree.erasePhysical_mapAxes F G) (tree.bundledExecution_mapAxes F G))

/-- The direct physical/history observation has the matching naturality. -/
theorem KuuNativeF45Tree.physicalHistories_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (tree.mapAxes F G).physicalHistories = tree.physicalHistories.mapAxes F G := by
  calc
    _ = kuuNativeF45PhysicalHistoryEquiv p n m C D
        (tree.mapAxes F G).physicalExchange :=
      (tree.mapAxes F G).physicalHistoryEquiv_execution.symm
    _ = kuuNativeF45PhysicalHistoryEquiv p n m C D
        (tree.physicalExchange.mapAxes F G) :=
      congrArg (kuuNativeF45PhysicalHistoryEquiv p n m C D)
        (tree.physicalExchange_mapAxes F G)
    _ = (kuuNativeF45PhysicalHistoryEquiv p n m A B
        tree.physicalExchange).mapAxes F G :=
      kuuNativeF45PhysicalHistoryEquiv_naturality F G tree.physicalExchange
    _ = _ := congrArg (KuuNativeF45PhysicalHistories.mapAxes F G)
      tree.physicalHistoryEquiv_execution

/-- Actual physical equality AND equality of both complete histories
suffice for packet equality. This does not claim raw tree equality. -/
theorem KuuNativeF45Tree.physicalExchange_eq_of_observations
    (s t : KuuNativeF45Tree p n m ma pa mb pb)
    (hphysical : s.erasePhysical = t.erasePhysical)
    (hhistories : s.axisHistories = t.axisHistories) :
    s.physicalExchange = t.physicalExchange := by
  apply (kuuNativeF45PhysicalHistoryEquiv p n m A B).injective
  rw [s.physicalHistoryEquiv_execution, t.physicalHistoryEquiv_execution]
  exact congrArg₂
    (fun (phys : PolygonDepthTree p n m)
        (h : KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb) =>
      (⟨a, b, x, y, phys, ⟨ma, mb, pa, pb, h.1, h.2⟩⟩ :
        KuuNativeF45PhysicalHistories p n m A B)) hphysical hhistories

/-- A discriminator used ONLY to prove raw inequality, never to
replace the complete source by a scalar classification. -/
def KuuNativeF45Tree.rootKind
    (tree : KuuNativeF45Tree p n m ma pa mb pb) : Nat := by
  cases tree with
  | refl => exact 0
  | leaf i order h₁ h₂ =>
      cases order with
      | firstAxisFirst => exact 1
      | secondAxisFirst => exact 2
  | node => exact 3

/-- Opposite actual leaf orders remain different in the raw source. -/
theorem nativeF45LeafOrders_raw_ne
    (i : PolygonBoundarySector p)
    (h₁ : KuuNativeAxisTrace n ma mb) (h₂ : KuuNativeAxisTrace m pa pb) :
    KuuNativeF45Tree.leaf i .firstAxisFirst h₁ h₂ ≠
      KuuNativeF45Tree.leaf i .secondAxisFirst h₁ h₂ := by
  intro h
  have hk := congrArg KuuNativeF45Tree.rootKind h
  change (1 : Nat) = 2 at hk
  cases hk

/-- The physical bracket and BOTH Type-valued histories are unchanged
by selecting the other leaf order, so this specific packet forgets it. -/
theorem nativeF45LeafOrders_physicalExchange_eq
    (i : PolygonBoundarySector p)
    (h₁ : KuuNativeAxisTrace n ma mb) (h₂ : KuuNativeAxisTrace m pa pb) :
    (KuuNativeF45Tree.leaf i .firstAxisFirst h₁ h₂).physicalExchange =
      (KuuNativeF45Tree.leaf i .secondAxisFirst h₁ h₂).physicalExchange :=
  KuuNativeF45Tree.physicalExchange_eq_of_observations _ _ rfl rfl

/-- Zero-depth reflexivity is also distinct from an explicitly
constructed zero-depth leaf, although their packets coincide. -/
theorem nativeF45Refl_leaf_information_loss
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    KuuNativeF45Tree.refl i ma pa ≠
        KuuNativeF45Tree.leaf i .firstAxisFirst (.refl ma) (.refl pa) ∧
      (KuuNativeF45Tree.refl i ma pa).physicalExchange =
        (KuuNativeF45Tree.leaf i .firstAxisFirst (.refl ma) (.refl pa)).physicalExchange := by
  constructor
  · intro h
    cases h
  · exact KuuNativeF45Tree.physicalExchange_eq_of_observations _ _ rfl rfl

/-- Even at strictly positive depths on BOTH axes, the full physical
packet is NOT injective on actual raw F45 source trees. -/
theorem nativeF45PhysicalExchange_not_injective
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun t : KuuNativeF45Tree p 1 1 ma pa
        (.snoc ma (.nil b)) (.snoc pa (.nil y)) => t.physicalExchange) := by
  intro hinj
  apply nativeF45LeafOrders_raw_ne i
    (KuuNativeAxisTrace.insertNilOnce ma) (KuuNativeAxisTrace.insertNilOnce pa)
  apply hinj
  exact nativeF45LeafOrders_physicalExchange_eq i
    (KuuNativeAxisTrace.insertNilOnce ma) (KuuNativeAxisTrace.insertNilOnce pa)

/-- No raw reconstruction map can be a left inverse of this observation. -/
theorem nativeF45PhysicalExchange_no_leftInverse
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    ¬ ∃ recover : KuuNativeF45PhysicalExchange p 1 1 A B →
        KuuNativeF45Tree p 1 1 ma pa (.snoc ma (.nil b)) (.snoc pa (.nil y)),
      Function.LeftInverse recover (fun t => t.physicalExchange) := by
  rintro ⟨recover, hrecover⟩
  exact nativeF45PhysicalExchange_not_injective i ma pa hrecover.injective

/-- The real north pentagon two-stage source enters the same classification. -/
theorem northNativeF45TwoStages_physical_history_comparison :
    kuuNativeF45PhysicalHistoryEquiv (.pentagon .north) 2 2 Site Site
      northNativeF45TwoStages.physicalExchange =
        northNativeF45TwoStages.physicalHistories :=
  northNativeF45TwoStages.physicalHistoryEquiv_execution

#print axioms KuuNativeF45Tree.physicalHistoryEquiv_execution
#print axioms KuuNativeF45Tree.physicalExchange_physical
#print axioms KuuNativeF45Tree.physicalExchange_mapAxes
#print axioms KuuNativeF45Tree.physicalHistories_mapAxes
#print axioms KuuNativeF45Tree.physicalExchange_eq_of_observations
#print axioms nativeF45LeafOrders_raw_ne
#print axioms nativeF45LeafOrders_physicalExchange_eq
#print axioms nativeF45Refl_leaf_information_loss
#print axioms nativeF45PhysicalExchange_not_injective
#print axioms nativeF45PhysicalExchange_no_leftInverse
#print axioms northNativeF45TwoStages_physical_history_comparison
end
end Kuu.F112.Physical
