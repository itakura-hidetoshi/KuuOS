import Kuu.F112.PolygonNativeC60AQFullPentagonFullDependentWhiskerReflection

/-!
# F112-P94D3FM — actual alternative AQ 17D context and full 18D faithfulness

FK defines a SEPARATE constructor-preserving 15D Type-valued whiskering
on the SAME original physical K5 14D fiber. FL proves its injection on
every fixed dependent 15D Hom fiber, all finite AQ words, and the new
base frame onCell. Here we combine the actual lower onObj and onCell
proofs, reflect every raw16D constructor of the true 17D context
closure, and apply FI's already proved exact 17D/18D/FreeGroup criterion.

This is not the OLD FJ selected AQ transport: FJ's actual
noninjectivity and universal two-letter kernel survive intact.
All object pairs, original 15D evidence, raw16D intermediate witnesses,
exact closed-generator provenance and 18D recursive generator codes
are preserved; no graph or Peiffer observer replaces their Type values.

No assertion about original geometric 19D filling, arbitrary physical
presentations, strict global n-categories or hyperdescent. No Gray,
axioms, sorry or admit. Append-only/tighten-only/same-root; existing
107 public roots. Apache-2.0. Copyright 板倉英俊 / Hidetoshi Itakura.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Genuine closed 16D raw syntax reflects all four constructors
under any original finite context whose COMPLETE lower 15D
proof-bearing object action is injective. Exact composite intermediate
boundary is recovered through dependent Sigma syntax. The atom case
uses the independently proved injective FULL provenance prefix,
not a quotient or the noncommutative BV shadow. -/
theorem nativeK5FMClosedStep_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (F : Bool → NativeC60BCFrame L)
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal F word)) :
    ∀ {a b : L.Total},
      Function.Injective
        (fun c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b =>
          nativeC60BCMapClosedStep S F word c) := by
  intro a b p q heq
  induction p with
  | atom g =>
      cases q with
      | atom h =>
          have hg : g = h := by
            apply nativeC60BVShiftGen_injective S F word
            injection heq
          cases hg
          rfl
      | refl _ => cases heq
      | symm _ => cases heq
      | trans _ _ => cases heq
  | refl _ =>
      cases q with
      | atom _ => cases heq
      | refl _ => rfl
      | symm _ => cases heq
      | trans _ _ => cases heq
  | symm p ih =>
      cases q with
      | atom _ => cases heq
      | refl _ => cases heq
      | symm q =>
          have hp : nativeC60BCMapClosedStep S F word p =
              nativeC60BCMapClosedStep S F word q := by
            injection heq
          have hraw : p = q := ih hp
          cases hraw
          rfl
      | trans _ _ => cases heq
  | trans p t ihp iht =>
      cases q with
      | atom _ => cases heq
      | refl _ => cases heq
      | symm _ => cases heq
      | trans q r =>
          have hleftSigma := Option.some.inj
            (congrArg
              (nativeC60FFTransLeftCode (nativeC60BCClosedSignature S F))
              heq)
          have hrightSigma := Option.some.inj
            (congrArg
              (nativeC60FFTransRightCode (nativeC60BCClosedSignature S F))
              heq)
          have hmid := hctx (congrArg Sigma.fst hleftSigma)
          cases hmid
          have hl : nativeC60BCMapClosedStep S F word p =
              nativeC60BCMapClosedStep S F word q :=
            eq_of_heq (Sigma.mk.inj hleftSigma).2
          have hr : nativeC60BCMapClosedStep S F word t =
              nativeC60BCMapClosedStep S F word r :=
            eq_of_heq (Sigma.mk.inj hrightSigma).2
          have hp : p = q := ihp hl
          have ht : t = r := iht hr
          cases hp
          cases ht
          rfl

section ActualAlternativePhysicalFidelity

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

/-- The FK alternative 15D base frame onObj preserves the entire
original raw14D boundary; it is individually injective. -/
theorem nativeK5FMBCFrame_onObj_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    Function.Injective (nativeK5FKBCFrame W side).onObj := by
  intro a b heq
  apply ULift.down_injective
  apply nativeK5FKRawFourteenWhisker_injective W side
  exact congrArg ULift.down heq

/-- Combine FK actual physical 14D onObj and FL full dependent
15D onCell to reflect the ENTIRE original proof-carrying AX Total.
Both source/target endpoints are retained by the FE Sigma proof. -/
theorem nativeK5FMBCFrame_mapTotal_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    Function.Injective (nativeK5FKBCFrame W side).mapTotal := by
  apply nativeC60FEFrame_mapTotal_injective
    (nativeK5FKBCFrame W side)
    (nativeK5FMBCFrame_onObj_injective W side)
  intro a b
  exact nativeK5FLBCFrame_onCell_injective W side a b

/-- Every chronological finite AQ context is injective on the
alternative complete 15D base AX Total, not just each Hom fiber. -/
theorem nativeK5FMBCContext_injective
    (W : NativeK5StructuralThirteenCell p U V) :
    ∀ word : List Bool,
      Function.Injective
        (nativeC60BCContextTotal (nativeK5FKBCFrame W) word) := by
  intro word
  induction word with
  | nil =>
      intro x y hxy
      exact hxy
  | cons side rest ih =>
      intro x y hxy
      apply ih
      exact nativeK5FMBCFrame_mapTotal_injective W side hxy

/-- The TRUE DR 17D singleton frame onObj is the faithful
complete 15D context action. No original FJ frame is used. -/
theorem nativeK5FMSeventeenFrame_onObj_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    Function.Injective
      (nativeC60DRSeventeenFrame
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) side).onObj := by
  exact nativeK5FMBCContext_injective W [side]

/-- Every original typed raw16D Hom path is reflected by the
alternative DR singleton 17D onCell. The indexed BC closure stores
complete original generator provenance. -/
theorem nativeK5FMSeventeenFrame_onCell_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {a b : (nativeC60DQSeventeenLayer
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)).Obj} :
    Function.Injective (fun h :
      (nativeC60DQSeventeenLayer
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)).Hom a b =>
      (nativeC60DRSeventeenFrame
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) side).onCell h) := by
  apply nativeK5FMClosedStep_injective
    (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) [side]
  exact nativeK5FMBCContext_injective W [side]

/-- The genuine new DR 17D frame is injective on its complete
proof-bearing Total: exact raw16D endpoints and paths are reflected. -/
theorem nativeK5FMSeventeenFrame_mapTotal_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    Function.Injective
      (nativeC60DRSeventeenFrame
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) side).mapTotal := by
  apply nativeC60FEFrame_mapTotal_injective
    (nativeC60DRSeventeenFrame
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) side)
    (nativeK5FMSeventeenFrame_onObj_injective W side)
  intro a b
  exact nativeK5FMSeventeenFrame_onCell_injective W side

/-- EVERY finite actual alternative 17D context word is injective
on complete proof-bearing original 17D Total. -/
theorem nativeK5FMAllSeventeenContexts_injective
    (W : NativeK5StructuralThirteenCell p U V) :
    ∀ word : List Bool,
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame
          (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W)) word) := by
  intro word
  induction word with
  | nil =>
      intro x y hxy
      exact hxy
  | cons side rest ih =>
      intro x y hxy
      apply ih
      exact nativeK5FMSeventeenFrame_mapTotal_injective W side hxy

/-- FI's exact GENERATOR-level converse now applies to the real
constructor-preserving K5 alternative. Unquotiented dependent
18D COMPLETE CODE injectivity holds for every finite AQ word. -/
theorem nativeK5FMCompleteEighteenCode_injective
    (W : NativeK5StructuralThirteenCell p U V) (word : List Bool) :
    Function.Injective
      (nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word) := by
  apply (nativeC60FICompleteCode_injective_iff_context
    (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word).mpr
  exact nativeK5FMAllSeventeenContexts_injective W word

/-- The full NONCOMMUTATIVE original 18D FreeGroup transport
is injective in the newly selected alternative Type-valued frame
for every finite physical AQ word. The old FJ frame remains
provably noninjective for every NONEMPTY word. -/
theorem nativeK5FMFullFree_injective
    (W : NativeK5StructuralThirteenCell p U V) (word : List Bool) :
    Function.Injective
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word) := by
  apply (nativeC60FIFullFree_injective_iff_context
    (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word).mpr
  exact nativeK5FMAllSeventeenContexts_injective W word

/-- The newly selected full noncommutative free-word map has NO
nonidentity kernel element at any finite AQ word. This does not
alter the old FJ common two-letter kernel witness. -/
theorem nativeK5FMFullFree_kernel_trivial
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (z : NativeC60DTFullFree
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W))
    (hz : (nativeC60DVFullWordTransport
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word) z = 1) :
    z = 1 := by
  apply nativeK5FMFullFree_injective W word
  simpa only [map_one] using hz

end ActualAlternativePhysicalFidelity

#print axioms nativeK5FMClosedStep_injective
#print axioms nativeK5FMBCFrame_onObj_injective
#print axioms nativeK5FMBCFrame_mapTotal_injective
#print axioms nativeK5FMBCContext_injective
#print axioms nativeK5FMSeventeenFrame_onObj_injective
#print axioms nativeK5FMSeventeenFrame_onCell_injective
#print axioms nativeK5FMSeventeenFrame_mapTotal_injective
#print axioms nativeK5FMAllSeventeenContexts_injective
#print axioms nativeK5FMCompleteEighteenCode_injective
#print axioms nativeK5FMFullFree_injective
#print axioms nativeK5FMFullFree_kernel_trivial

end
end Kuu.F112.Physical
