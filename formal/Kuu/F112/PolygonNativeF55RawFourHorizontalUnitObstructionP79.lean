import Kuu.F112.PolygonNativeF55RawFourVerticalCategoryP78

/-!
# F112-P79 — exact genuine horizontal unit obstruction in P77/P78 raw 4-cell quotient

P77 builds a source-generated Type-valued 4-cell relation on the
ORIGINAL nine-constructor F55 raw 3-cell proof trees. Its path_sound
theorem says every such witness preserves the P59 normalized STRICT
free proof-labelled path, not merely a selected integer charge.
P78 constructs strict LOCAL VERTICAL composition on that quotient.

P61 proved that original F55 horizontal composition of TWO RAW
identities has a two-edge normalized free path, while the intended
horizontal identity has the EMPTY free path. Thus it is IMPOSSIBLE
for P77's 4-cell relation to identify this horizontal identity
composite with the true raw identity. We prove the exact Type-level
nonexistence, unequal P77 quotient classes, and the necessary
no-go for ANY extension still sound for path equality.

The same two original raw cells DO have identical complete
F55 shadow, and their normalized paths ARE related by the
independently specified, SOURCE-GENERATED P62 unit-only path
congruence. That is a constructive lower-level repair candidate:
a prospective enlarged 4-cell presentation cannot preserve
P77's old strict path-equality soundness if it adds an actual
horizontal-unit 4-cell. It must instead use an honest weaker
path relation and independently prove its compatibility.

Moreover, contextual application of a raw identity carries
a one-edge P59 path, not the empty identity; this witnesses
LEFT and RIGHT contextual unit obstructions in the P77
4-cell relation, while the P62 structural-unit congruence
does relate those two source paths.

All results are uniform in both Nat axes and both independent
categorical sources. A separate specialization uses the TWO
ACTUAL disjoint north C60 six-sector local F54 associators,
not invented category objects or numerical shadow generators.

This is a positive/negative precise P79 boundary. We do NOT
claim strict 3-interchange, existence of a new 4-cell for all
pairs, global strict 3/n, or hyperdescent. No Gray, sorry,
admit, new axioms, or exclusion of 107 public root modules.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The ACTUAL F54 left-then-right route underlying raw F55
horizontal composition of two identities. No path equality is
introduced by this definition. -/
def nativeF55HorizontalUnitRoute
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    KuuNativeF45Tree.DepthRotationRoute p
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter) :=
  .trans (.leftContext u rightBefore) (.rightContext leftAfter v)

/-- Original raw horizontal identities are NOT related by ANY
P77 source-generated 4-cell to the genuine raw identity at the
same resultant F54 route: P61's free-path lengths are 2 vs 0,
and P77's actual 4-cell path_sound would equate the paths. -/
theorem nativeF55RawFour_horizontal_identity_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ¬ Nonempty (NativeF55RawVerticalFourCell
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute u v))) := by
  rintro ⟨w⟩
  exact (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_not_normalized_unit
    u v) w.path_sound

/-- This is an EXACT quotient no-go, not merely a failure to find
a chosen 4-cell: the P77 quotient kernel iff excludes equality.
The canonical SOURCE-horizontal choice fails strict identity on P78. -/
theorem nativeF55RawFour_horizontal_identity_class_ne
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55RawVerticalFourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v)) ≠
    nativeF55RawVerticalFourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute u v)) := by
  intro h
  apply nativeF55RawFour_horizontal_identity_noFourCell u v
  exact (nativeF55RawVerticalFourClass_eq_iff _ _ _ _).mp h

/-- POSITIVE but weaker repair: the two explicit source terms are
equivalent in the PREEXISTING P62 structural-unit PATH congruence,
without inventing a P77 4-cell or identifying any physical generator. -/
theorem nativeF55RawFour_horizontal_identity_unitPathRelated
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    NativeF55UnitPathRel
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v)).toNativeStrictPath
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute u v)).toNativeStrictPath := by
  exact KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_unit_related u v

/-- The horizontal unit defect is INvisible to the chosen FULL
three-coordinate F55 numerical shadow. Therefore numerical equality
alone cannot justify source proof-4-cell horizontal unit coherence. -/
theorem nativeF55RawFour_horizontal_identity_shadow_eq
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v)).nativeShadow =
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      (nativeF55HorizontalUnitRoute u v)).nativeShadow := by
  exact KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_ident_shadow_zero u v

/-- ANY proposed raw 4-cell relation that is sound for equality
of P59 proof-labelled free paths CANNOT identify the original F55
horizontal composite of identities with its intended unit.
This obstruction is independent of which 4-cell generating syntax
was chosen. It does not prohibit P62-relative 4-cell coherence. -/
theorem nativeF55RawFour_no_pathSound_horizontalUnitExtension
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter)
    (R : ∀ {a b : KuuNativeF45Tree.DepthRotationRoute p
                  (KuuNativeF45Tree.node leftBefore rightBefore)
                  (KuuNativeF45Tree.node leftAfter rightAfter)},
       KuuNativeF45Tree.DepthRotationRoute.PresentedCell p a b →
       KuuNativeF45Tree.DepthRotationRoute.PresentedCell p a b → Prop)
    (hPath : ∀ {a b} (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p a b),
       R f g → f.toNativeStrictPath = g.toNativeStrictPath)
    (hHorizontalUnit : R
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (nativeF55HorizontalUnitRoute u v))) : False := by
  exact (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.horizontal_identities_not_normalized_unit
    u v) (hPath _ _ hHorizontalUnit)

/-- Left F54 context changes a raw F55 identity into an ATOMIC
P59 singleton proof path; the identity at the resulting route has
the empty path. No P77 source 4-cell can bridge these two. -/
theorem nativeF55RawFour_leftContext_identity_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    ¬ Nonempty (NativeF55RawVerticalFourCell
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
        (.ident u) later)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (.leftContext u later))) := by
  rintro ⟨h⟩
  have hLength := congrArg Quiver.Path.length h.path_sound
  change (1 : Nat) = 0 at hLength
  exact (by decide : (1 : Nat) ≠ 0) hLength

/-- Right F54 context has the same genuine typed unit obstruction. -/
theorem nativeF55RawFour_rightContext_identity_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55RawVerticalFourCell
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
        earlier (.ident u))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (.rightContext earlier u))) := by
  rintro ⟨h⟩
  have hLength := congrArg Quiver.Path.length h.path_sound
  change (1 : Nat) = 0 at hLength
  exact (by decide : (1 : Nat) ≠ 0) hLength

/-- P62's independently specified SOURCE identity-only congruence
DOES relate the left-context source unit and empty path. It cannot
be substituted for a P77 raw 4-cell without enlarging that language. -/
theorem nativeF55RawFour_leftContext_identity_unitPathRelated
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    NativeF55UnitPathRel
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
        (.ident u) later).toNativeStrictPath
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (.leftContext u later)).toNativeStrictPath := by
  change NativeF55UnitPathRel
    (KuuNativeF45Tree.node first later)
    (KuuNativeF45Tree.node last later)
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
      (.ident u) later).toNativeStrictPath
    (Quiver.Path.nil : Quiver.Path
      (⟨KuuNativeF45Tree.DepthRotationRoute.leftContext u later⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node first later)
          (KuuNativeF45Tree.node last later))
      ⟨KuuNativeF45Tree.DepthRotationRoute.leftContext u later⟩)
  exact NativeF55UnitPathRel.structuralUnit
    (.leftContext u later) (.leftContext (.ident u) later) rfl

/-- Right-context unit is likewise related in P62's SOURCE-certified
structural-unit congruence, but not by the old P77 4-cells. -/
theorem nativeF55RawFour_rightContext_identity_unitPathRelated
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55UnitPathRel
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
        earlier (.ident u)).toNativeStrictPath
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (.rightContext earlier u)).toNativeStrictPath := by
  change NativeF55UnitPathRel
    (KuuNativeF45Tree.node earlier first)
    (KuuNativeF45Tree.node earlier last)
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
      earlier (.ident u)).toNativeStrictPath
    (Quiver.Path.nil : Quiver.Path
      (⟨KuuNativeF45Tree.DepthRotationRoute.rightContext earlier u⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node earlier first)
          (KuuNativeF45Tree.node earlier last))
      ⟨KuuNativeF45Tree.DepthRotationRoute.rightContext earlier u⟩)
  exact NativeF55UnitPathRel.structuralUnit
    (.rightContext earlier u) (.rightContext earlier (.ident u)) rfl

/-- The C60 north HEXAGON genuine left F54 associator, kept as a
physical two-axis raw route rather than a numerical label. -/
def northHexagonNativeLeftF54UnitRoute :=
  KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
    northHexagonNativeLeftRotation

/-- The independent right F54 physical associator on sectors 3-5. -/
def northHexagonNativeRightF54UnitRoute :=
  KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
    northHexagonNativeRightRotation

/-- Actual source-horizontal composition of the two distinct
six-sector physical C60 local F54 identity 3-cells. -/
def northHexagonNativeHorizontalRawIdentityPair :=
  (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
    northHexagonNativeLeftF54UnitRoute).horizontal
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northHexagonNativeRightF54UnitRoute)

/-- The TRUE raw 3-cell identity at the same physical
left-then-right F54 contextual route. -/
def northHexagonNativeHorizontalStrictIdentity :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
    (nativeF55HorizontalUnitRoute
      northHexagonNativeLeftF54UnitRoute
      northHexagonNativeRightF54UnitRoute)

/-- Genuine C60 six-sector specialization: P77 source 4-cells
CANNOT identify the horizontal pair of true F55 raw identities
with the strict identity at their contextual composite route. -/
theorem northHexagonNativeHorizontalIdentity_noRawFourCell :
    ¬ Nonempty (NativeF55RawVerticalFourCell _ _
      northHexagonNativeHorizontalRawIdentityPair
      northHexagonNativeHorizontalStrictIdentity) := by
  exact nativeF55RawFour_horizontal_identity_noFourCell
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute

/-- Nevertheless the same ACTUAL C60 pair is related by P62's
structural-unit path congruence, with both raw sources retained. -/
theorem northHexagonNativeHorizontalIdentity_P62_related :
    NativeF55UnitPathRel _ _
      northHexagonNativeHorizontalRawIdentityPair.toNativeStrictPath
      northHexagonNativeHorizontalStrictIdentity.toNativeStrictPath := by
  exact nativeF55RawFour_horizontal_identity_unitPathRelated
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute

/-- On actual original C60 physical categories all three
selected full-shadow observer coordinates agree, despite the
CERTIFIED nonexistence of a P77 raw 4-cell. -/
theorem northHexagonNativeHorizontalIdentity_fullShadow_eq :
    northHexagonNativeHorizontalRawIdentityPair.nativeShadow =
      northHexagonNativeHorizontalStrictIdentity.nativeShadow := by
  exact nativeF55RawFour_horizontal_identity_shadow_eq
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute

#print axioms nativeF55HorizontalUnitRoute
#print axioms nativeF55RawFour_horizontal_identity_noFourCell
#print axioms nativeF55RawFour_horizontal_identity_class_ne
#print axioms nativeF55RawFour_horizontal_identity_unitPathRelated
#print axioms nativeF55RawFour_horizontal_identity_shadow_eq
#print axioms nativeF55RawFour_no_pathSound_horizontalUnitExtension
#print axioms nativeF55RawFour_leftContext_identity_noFourCell
#print axioms nativeF55RawFour_rightContext_identity_noFourCell
#print axioms nativeF55RawFour_leftContext_identity_unitPathRelated
#print axioms nativeF55RawFour_rightContext_identity_unitPathRelated
#print axioms northHexagonNativeLeftF54UnitRoute
#print axioms northHexagonNativeRightF54UnitRoute
#print axioms northHexagonNativeHorizontalRawIdentityPair
#print axioms northHexagonNativeHorizontalStrictIdentity
#print axioms northHexagonNativeHorizontalIdentity_noRawFourCell
#print axioms northHexagonNativeHorizontalIdentity_P62_related
#print axioms northHexagonNativeHorizontalIdentity_fullShadow_eq

end
end Kuu.F112.Physical
