import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ITypedStructuralCategoryFunctor
import Mathlib.Tactic

/-!
# F112-P94D3GK4J — no identity of ANY original P92B quotient class

GK4H proves the selected zero-edge F54 reflexivity route is NOT an
identity of the original P92B quotient with its TRUE source composition.
This alone does not rule out OTHER proposed identities: original F54
castDepths rfl rfl has zero original physical rotation count AND zero
GK4C unit-atom count.

Introduce a NEW original raw F54 witness invariant, its primitive
route-leaf count: BOTH genuine RotationChain and typed castDepths
contribute one atom, vertical composition adds counts, and original
contexts do not change the number. Every raw F54 route has strictly
positive leaf count.

All original F55 nine constructors preserve this atom count
CONDITIONALLY when the actual primitive physical rotation count is
zero. The pentagon 3-vs-2 and square 2-vs-2 generators cannot operate
at physical rotation zero; the newly added original P92B triple
associator-naturality source contains one genuine physical associator
edge, so cannot operate there either. The remaining P92B constructors
preserve the count by real dependent typed recursion. NO global
leaf-count invariance is assumed for positive-rotation pentagons.

If ANY original P92B endomorphism class e were a left identity on
true original F54 reflexivity route q, P92B comparison would identify
the raw route trans e q with q. GK4F forces trans e q to have ZERO
physical rotations, and the new conditional source proof then forces
leafCount(e)+1=1. This contradicts leafCount(e)>0 for every genuine
route. The symmetric argument rules out ANY right identity. Thus
the fixed original GK4H P92B binary operation admits NO identity
candidate at ANY inhabited original F45 stage; the distinct GK4I
structural quotient really forms a category only because it includes
the separately added genuine structural-seam witnesses.

The actual physical C60 north hexagon F45 triple witnesses
unconditional failure of ALL possible P92B units, not just selected
zero-chain units. A global choice of P92B units on all true F45 stages
cannot satisfy even the first category unit law.

Source and target retain independent D/E original category objects,
all four source Blocks, both Nat depths, every original F45 witness,
and every Type-valued F54 and P92B comparison constructor.
No different binary operation, P92B associativity or historically
typed P92B/F19/F28/F54/F55 equivalence is decided here.
No genuine 14D unconditional Countable, 19D filler, global strict n
or hyperdescent. No sorry/admit/new axioms or Gray.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root, 107 public roots, protect PR #1558.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section LeafCount
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Every original chain and typed depth cast is one primitive leaf,
unlike the earlier GK4C count of zero-edge RotationChain.refl. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4jLeafCount
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Nat := by
  induction route with
  | chain _ => exact 1
  | castDepths _ _ _ => exact 1
  | trans _ _ ihLeft ihRight => exact ihLeft + ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

/-- Every true original F54 route has at least one primitive leaf. -/
theorem nativeGK4J_leafCount_pos
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    0 < route.gk4jLeafCount := by
  induction route with
  | chain _ => decide
  | castDepths _ _ _ => decide
  | trans left right ihLeft ihRight =>
      change 0 < left.gk4jLeafCount + right.gk4jLeafCount
      omega
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

@[simp] theorem nativeGK4J_leafCount_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4jLeafCount =
      u.gk4jLeafCount + v.gk4jLeafCount := by
  rfl

@[simp] theorem nativeGK4J_leafCount_refl
    {n m : Nat}
    (t : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute.chain
      (KuuNativeF45Tree.RotationChain.refl t)).gk4jLeafCount = 1 := by
  rfl

@[simp] theorem nativeGK4J_leafCount_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4jLeafCount =
      route.gk4jLeafCount := by
  rfl

@[simp] theorem nativeGK4J_leafCount_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4jLeafCount =
      route.gk4jLeafCount := by
  rfl
end LeafCount

section ConditionalPreservation
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- All original F55 constructors preserve the original leaf count
on ZERO primitive physical rotation routes. Positive-rotation
pentagon/square boundaries cannot occur in this subfiber. -/
theorem nativeGK4JOriginal_zero_leafCount_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.rotationCount = 0 → r.gk4jLeafCount = s.gk4jLeafCount := by
  induction cell with
  | ident route =>
      intro _
      rfl
  | pentagon a b c d =>
      intro hzero
      change (3 : Nat) = 0 at hzero
      omega
  | disjointSquare left right =>
      intro hzero
      change (2 : Nat) = 0 at hzero
      omega
  | symm cell ih =>
      intro hzero
      exact (ih ((nativeGK4FOriginal_zero_rotation_iff cell).mpr hzero)).symm
  | trans left right ihLeft ihRight =>
      intro hzero
      exact (ihLeft hzero).trans
        (ihRight ((nativeGK4FOriginal_zero_rotation_iff left).mp hzero))
  | leftContext cell later ih =>
      intro hzero
      exact ih hzero
  | rightContext earlier cell ih =>
      intro hzero
      exact ih hzero
  | precompose prior cell ih =>
      intro hzero
      have hsub := ih (by
        change prior.rotationCount + _ = 0 at hzero
        omega)
      simpa only [nativeGK4J_leafCount_trans] using
        congrArg (fun k : Nat => prior.gk4jLeafCount + k) hsub
  | postcompose cell suffix ih =>
      intro hzero
      have hsub := ih (by
        change _ + suffix.rotationCount = 0 at hzero
        omega)
      simpa only [nativeGK4J_leafCount_trans] using
        congrArg (fun k : Nat => k + suffix.gk4jLeafCount) hsub

/-- All nine P92B constructors preserve the true F54 base-term count
ON ZERO physical-rotation routes. New associator-naturality contains
one real rotation, so its source cannot be in the zero subfiber.
NO incorrect global preservation across pentagon 3-vs-2 is claimed. -/
theorem nativeGK4JP92B_zero_leafCount_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.rotationCount = 0 → r.gk4jLeafCount = s.gk4jLeafCount := by
  induction cell with
  | original old => exact nativeGK4JOriginal_zero_leafCount_sound old
  | assocNaturality u v w =>
      intro hzero
      change (u.rotationCount + v.rotationCount + w.rotationCount) + 1 = 0 at hzero
      omega
  | refl route =>
      intro _
      rfl
  | symm cell ih =>
      intro hzero
      exact (ih ((nativeGK4FP92B_zero_rotation_iff cell).mpr hzero)).symm
  | trans left right ihLeft ihRight =>
      intro hzero
      exact (ihLeft hzero).trans
        (ihRight ((nativeGK4FP92B_zero_rotation_iff left).mp hzero))
  | leftContext cell later ih =>
      intro hzero
      exact ih hzero
  | rightContext earlier cell ih =>
      intro hzero
      exact ih hzero
  | precompose prior cell ih =>
      intro hzero
      have hsub := ih (by
        change prior.rotationCount + _ = 0 at hzero
        omega)
      simpa only [nativeGK4J_leafCount_trans] using
        congrArg (fun k : Nat => prior.gk4jLeafCount + k) hsub
  | postcompose cell suffix ih =>
      intro hzero
      have hsub := ih (by
        change _ + suffix.rotationCount = 0 at hzero
        omega)
      simpa only [nativeGK4J_leafCount_trans] using
        congrArg (fun k : Nat => k + suffix.gk4jLeafCount) hsub
end ConditionalPreservation

section UnitNoGo
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- No arbitrary original P92B endomorphism class is a left identity
for the GK4H full source-induced quotient composition, at any
inhabited original F45 tree. This includes typed casts. -/
theorem nativeGK4J_no_any_P92B_left_identity
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (e : NativeF55P92AssocRouteClasses tree tree) :
    ¬ (∀ q : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4H_p92Compose tree tree tree e q = q) := by
  refine _root_.Quotient.inductionOn e ?_
  intro rawE hunit
  let unit : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  have h := hunit (nativeF55P92AssocRouteClass tree tree unit)
  have heq :
      nativeF55P92AssocRouteClass tree tree (.trans rawE unit) =
        nativeF55P92AssocRouteClass tree tree unit := by
    simpa only [nativeGK4H_p92Compose_class] using h
  rcases (nativeF55P92AssocRouteClass_eq_iff tree tree
    (.trans rawE unit) unit).mp heq with ⟨cell⟩
  have hzero : (KuuNativeF45Tree.DepthRotationRoute.trans rawE unit).rotationCount =
      0 := (nativeGK4FP92B_zero_rotation_iff cell).mpr (by rfl)
  have hcount := nativeGK4JP92B_zero_leafCount_sound cell hzero
  have hpos := nativeGK4J_leafCount_pos rawE
  change rawE.gk4jLeafCount + 1 = 1 at hcount
  omega

/-- Symmetric no-go for ANY proposed right identity. -/
theorem nativeGK4J_no_any_P92B_right_identity
    (tree : KuuNativeF45Tree p n m ma pa mb pb)
    (e : NativeF55P92AssocRouteClasses tree tree) :
    ¬ (∀ q : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4H_p92Compose tree tree tree q e = q) := by
  refine _root_.Quotient.inductionOn e ?_
  intro rawE hunit
  let unit : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  have h := hunit (nativeF55P92AssocRouteClass tree tree unit)
  have heq :
      nativeF55P92AssocRouteClass tree tree (.trans unit rawE) =
        nativeF55P92AssocRouteClass tree tree unit := by
    simpa only [nativeGK4H_p92Compose_class] using h
  rcases (nativeF55P92AssocRouteClass_eq_iff tree tree
    (.trans unit rawE) unit).mp heq with ⟨cell⟩
  have hzero : (KuuNativeF45Tree.DepthRotationRoute.trans unit rawE).rotationCount =
      0 := (nativeGK4FP92B_zero_rotation_iff cell).mpr (by rfl)
  have hcount := nativeGK4JP92B_zero_leafCount_sound cell hzero
  have hpos := nativeGK4J_leafCount_pos rawE
  change 1 + rawE.gk4jLeafCount = 1 at hcount
  omega

theorem nativeGK4J_no_any_P92B_two_sided_identity
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ ∃ e : NativeF55P92AssocRouteClasses tree tree,
        (∀ q, nativeGK4H_p92Compose tree tree tree e q = q) ∧
        (∀ q, nativeGK4H_p92Compose tree tree tree q e = q) := by
  rintro ⟨e, hleft, _⟩
  exact nativeGK4J_no_any_P92B_left_identity tree e hleft
end UnitNoGo

section CategoryObstruction
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- No global choice of original P92B unit classes on all full
F45 stages can obey even the category LEFT unit law for the
fixed actual original GK4H quotient composition if a stage exists. -/
theorem nativeGK4J_no_P92B_global_unit_assignment
    (witness : NativeGK4IStage p ma mb pa pb) :
    ¬ ∃ (unit : ∀ X : NativeGK4IStage p ma mb pa pb,
          NativeF55P92AssocRouteClasses X.2.2 X.2.2),
        ∀ (X Y : NativeGK4IStage p ma mb pa pb)
          (q : NativeF55P92AssocRouteClasses X.2.2 Y.2.2),
          nativeGK4H_p92Compose X.2.2 X.2.2 Y.2.2 (unit X) q = q := by
  rintro ⟨unit, hleft⟩
  exact nativeGK4J_no_any_P92B_left_identity
    witness.2.2 (unit witness) (hleft witness witness)

/-- Genuine original C60 north hexagon F45 triple: unconditional
candidate-independent failure of both original P92B unit laws. -/
theorem nativeGK4J_physical_north_no_any_P92B_identity :
    (∀ e : NativeF55P92AssocRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      ¬ ∀ q : NativeF55P92AssocRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        nativeGK4H_p92Compose nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple e q = q) ∧
    (∀ e : NativeF55P92AssocRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      ¬ ∀ q : NativeF55P92AssocRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        nativeGK4H_p92Compose nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple q e = q) := by
  exact ⟨nativeGK4J_no_any_P92B_left_identity nativeGK4FPhysicalNorthTriple,
    nativeGK4J_no_any_P92B_right_identity nativeGK4FPhysicalNorthTriple⟩

/-- Independent GK4I STRUCTURAL quotient is actually unital in this
same original physical C60 fully dependent F45 context. -/
theorem nativeGK4J_physical_north_structural_unital_contrast :
    (∀ q : NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4H_structuralCompose
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple
        (nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple) q = q) ∧
    (∀ q : NativeGK4EStructuralRouteClasses
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4H_structuralCompose
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
        nativeGK4FPhysicalNorthTriple q
        (nativeGK4H_structuralUnit nativeGK4FPhysicalNorthTriple) = q) := by
  exact ⟨nativeGK4H_structuralCompose_leftUnit
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
    nativeGK4H_structuralCompose_rightUnit
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple⟩
end CategoryObstruction

#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4jLeafCount
#print axioms nativeGK4J_leafCount_pos
#print axioms nativeGK4J_leafCount_trans
#print axioms nativeGK4J_leafCount_refl
#print axioms nativeGK4J_leafCount_leftContext
#print axioms nativeGK4J_leafCount_rightContext
#print axioms nativeGK4JOriginal_zero_leafCount_sound
#print axioms nativeGK4JP92B_zero_leafCount_sound
#print axioms nativeGK4J_no_any_P92B_left_identity
#print axioms nativeGK4J_no_any_P92B_right_identity
#print axioms nativeGK4J_no_any_P92B_two_sided_identity
#print axioms nativeGK4J_no_P92B_global_unit_assignment
#print axioms nativeGK4J_physical_north_no_any_P92B_identity
#print axioms nativeGK4J_physical_north_structural_unital_contrast

end
end Kuu.F112.Physical
