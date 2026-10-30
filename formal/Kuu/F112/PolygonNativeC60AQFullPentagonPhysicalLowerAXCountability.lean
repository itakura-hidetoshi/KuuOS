import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalRecursiveGenCountability

/-!
# F112-P94D3GC — countability of the actual LOWER physical AX evidence

GA and GB establish countability of the original 16D/17D/18D
dependent Type-valued syntax from Countable of the lower physical
AX base total and primitive AX Gen fibers.

For the ACTUAL original K5 Kuu signature, each primitive Gen is
a dependent source/target equality-constrained occurrence of an
ORIGINAL 15D proof. Forgetting only the Prop-valued endpoint
equations gives an injective map to the actual original AX base
total. Thus the primitive Gen Countable hypothesis is redundant
once the complete base Total is Countable.

We also isolate precise sufficient 14D/15D conditions for the
base Total, without asserting that arbitrary categorical Hom
or original 14D proof families are automatically countable.
All original proof witnesses and free-group generators remain
unmodified. This is not a quotient or a new presentation.

Strict Kuu primary, independent Kuu preserved, no Gray or
invented 19D filler, append-only and 107 published roots.
Lean v4.30.0-rc2; pinned mathlib. Copyright Hidetoshi Itakura.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section ActualLowerPhysicalAX

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Every original 15D comparison with its exact 14D endpoints
is stored in the original AX base total. The extra source/target
equations that define the physical primitive Gen are propositions,
not new independent Type-valued evidence. Forget only those
equations; NO original 14D or 15D proof is forgotten. -/
theorem nativeK5GCPrimitiveGen_countable_of_baseTotal
    (W : NativeK5StructuralThirteenCell p U V)
    (hbase : Countable (nativeK5AXBaseLayer W).Total)
    (x y : (nativeK5AXBaseLayer W).Total) :
    Countable ((nativeK5AXKuuSignature W).Gen x y) := by
  letI : Countable (nativeK5AXBaseLayer W).Total := hbase
  let includeEvidence :
      (nativeK5AXKuuSignature W).Gen x y →
        (nativeK5AXBaseLayer W).Total :=
    fun g => nativeK5AXPack W g.2.2.1
  have hinj : Function.Injective includeEvidence := by
    rintro ⟨R, S, ⟨c, hx, hy⟩⟩
      ⟨R', S', ⟨d, hx', hy'⟩⟩ heq
    have hR : R = R' :=
      congrArg
        (fun z : (nativeK5AXBaseLayer W).Total => z.1.1.down) heq
    have hS : S = S' :=
      congrArg
        (fun z : (nativeK5AXBaseLayer W).Total => z.1.2.down) heq
    subst R'
    subst S'
    have hcd : c = d := by
      have hproof : HEq (ULift.up c) (ULift.up d) :=
        (Sigma.mk.inj heq).2
      exact congrArg ULift.down (eq_of_heq hproof)
    subst d
    rfl
  exact hinj.countable

/-- The TRUE original physical 18D source is Countable from
ONLY the original lower AX base Total Countable. The separate
primitive Gen-fiber gate in GB is derived from that very Total. -/
theorem nativeK5GCPhysicalOriginal18_countable_of_baseTotal
    (W : NativeK5StructuralThirteenCell p U V)
    (hbase : Countable (nativeK5AXBaseLayer W).Total) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :=
  nativeK5GBPhysicalOriginal18_countable_of_lower_primitive
    W hbase (nativeK5GCPrimitiveGen_countable_of_baseTotal W hbase)

/-- For every genuine nonempty finite C60 AQ word, the precise
minimal normal-generator cardinality of the old physical full
noncommutative DV kernel is aleph-null from ONE lower AX total
Countable premise, rather than TWO primitive gates. -/
theorem nativeK5GCPhysical_exactAleph0NormalRank_of_baseTotal
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hbase : Countable (nativeK5AXBaseLayer W).Total) :
    (∀ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R → ℵ₀ ≤ #R) ∧
    (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R ∧ #R = ℵ₀) :=
  nativeK5FYPhysical_fullDV_exactAleph0NormalRank_of_sourceCountable
    W word hne
    (nativeK5GCPhysicalOriginal18_countable_of_baseTotal W hbase)

/-- An exact lower-level sufficient condition: countability of
the original 14D proof fiber together with countability of each
ORIGINAL dependent 15D comparison proof fiber yields countability
of the whole original proof-bearing AX base total. No original
Type-valued evidence is quotiented, shortened or scalarized. -/
theorem nativeK5GCBaseTotal_countable_of_fourteen_fifteen
    (W : NativeK5StructuralThirteenCell p U V)
    (h14 : Countable (NativeK5FifteenFourteenFiber W))
    (h15 : ∀ R S : NativeK5FifteenFourteenFiber W,
      Countable (NativeK5AQFifteenCell W R S)) :
    Countable (nativeK5AXBaseLayer W).Total := by
  letI : Countable (NativeK5FifteenFourteenFiber W) := h14
  letI : ∀ R S : NativeK5FifteenFourteenFiber W,
      Countable (NativeK5AQFifteenCell W R S) := h15
  dsimp [NativeC60AXLayer.Total, nativeK5AXBaseLayer, nativeC60AXLayerOf]
  infer_instance

/-- The physical aleph-null rank follows from explicit exact
original 14D/15D witness-cardinality hypotheses. The stronger
reduction of actual 15D syntax to 14D and of actual 14D to
categorical Hom smallness is the remaining GC frontier. -/
theorem nativeK5GCPhysical_exactAleph0NormalRank_of_fourteen_fifteen
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (h14 : Countable (NativeK5FifteenFourteenFiber W))
    (h15 : ∀ R S : NativeK5FifteenFourteenFiber W,
      Countable (NativeK5AQFifteenCell W R S)) :
    (∀ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R → ℵ₀ ≤ #R) ∧
    (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R ∧ #R = ℵ₀) :=
  nativeK5GCPhysical_exactAleph0NormalRank_of_baseTotal
    W word hne
    (nativeK5GCBaseTotal_countable_of_fourteen_fifteen W h14 h15)

end ActualLowerPhysicalAX

#print axioms nativeK5GCPrimitiveGen_countable_of_baseTotal
#print axioms nativeK5GCPhysicalOriginal18_countable_of_baseTotal
#print axioms nativeK5GCPhysical_exactAleph0NormalRank_of_baseTotal
#print axioms nativeK5GCBaseTotal_countable_of_fourteen_fifteen
#print axioms nativeK5GCPhysical_exactAleph0NormalRank_of_fourteen_fifteen

end
end Kuu.F112.Physical
