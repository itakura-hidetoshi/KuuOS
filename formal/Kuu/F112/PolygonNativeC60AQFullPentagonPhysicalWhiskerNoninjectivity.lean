import Kuu.F112.PolygonNativeC60AQFullPentagonRecursiveGeneratorReflection

/-!
# F112-P94D3FJ — an actual original Type-valued singleton whiskering collision

The genuine K5 AQ physical fifteen-cell grammar distinguishes
a conservative reflexivity certificate from an observer-compatible
conservative atom, even at identical original fourteen-cell endpoints.
The actual nativeK5AQWhiskerCell operation maps BOTH to the SAME
conservative atom: it does not preserve which core constructor
produced that equality. We prove this as an explicit nontrivial
collision of original Type-valued proof terms, not a quotient,
charge, parity or graph observer.

The collision is lifted into the TRUE proof-bearing base AX total
and then into the TRUE DR 17D singleton context action. By the
already merged FI (#2676) exact code/free-group/context injection
criterion, this would obstruct unconditional DV full-word
faithfulness at the corresponding genuine physical singleton.
The construction does not assert a 19D filler or a classification
of the full kernel; DS no-go and earlier strict/independent Kuu
presentations, 107 public roots and no Gray are preserved.

Append-only / tighten-only / same root. No sorry, admit or new axiom.
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

section ActualPhysicalSingletonCollision

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

/-- A genuine source proof of original fifteen-cell reflexivity. -/
def nativeK5FJConservativeRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W R R :=
  .conservative (.refl R)

/-- A different genuine source proof of the SAME original observer
equality, but using the primitive conservative atom constructor. -/
def nativeK5FJConservativeAtom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W R R :=
  .conservative (.atom rfl rfl)

/-- Both source raw Type-valued proofs are different as CONSTRUCTORS.
Their common endpoints and observer equalities do not identify them. -/
theorem nativeK5FJConservativeRefl_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5FJConservativeRefl W R ≠
      nativeK5FJConservativeAtom W R := by
  intro heq
  cases heq

/-- IMPORTANT actual physical obstruction. The genuine K5
whiskering maps both distinct source proofs to a conservative
observer-compatible ATOM, forgetting whether the original core
proof was a reflexive constructor or an observer atom. The
equality is in the target Type-valued fifteen-cell grammar,
not after quotient or abelianization. -/
theorem nativeK5FJWhisker_conservative_collision
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    nativeK5AQWhiskerCell W side (nativeK5FJConservativeRefl W R) =
      nativeK5AQWhiskerCell W side (nativeK5FJConservativeAtom W R) := by
  rfl

/-- The full genuine fifteen-cell whiskering function is
NOT injective even on this single original, endpoint-fixed
dependent Hom fiber. No original boundary is discarded. -/
theorem nativeK5FJWhiskerCell_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    ¬ Function.Injective
      (fun cell : NativeK5AQFifteenCell W R R =>
        nativeK5AQWhiskerCell W side cell) := by
  intro hinj
  exact (nativeK5FJConservativeRefl_ne_atom W R)
    (hinj (nativeK5FJWhisker_conservative_collision W R side))

/-- Embed the original differing fifteen-cell proofs into the
complete proof-bearing original base fifteen-dimensional AX total. -/
def nativeK5FJBaseRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W (nativeK5FJConservativeRefl W R)

def nativeK5FJBaseAtom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W (nativeK5FJConservativeAtom W R)

/-- Complete original lower proof-bearing AX source objects differ;
this is not merely a difference of spellings of a shadow. -/
theorem nativeK5FJBaseRefl_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5FJBaseRefl W R ≠ nativeK5FJBaseAtom W R := by
  intro heq
  apply nativeK5FJConservativeRefl_ne_atom W R
  exact congrArg
    (fun o : (nativeK5AXBaseLayer W).Total => o.2.down) heq

/-- Both distinct true source AX totals have equal images under
the original genuine C60 one-letter physical base frame. -/
theorem nativeK5FJBaseFrame_collision
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    (nativeK5BCFrame W side).mapTotal (nativeK5FJBaseRefl W R) =
      (nativeK5BCFrame W side).mapTotal (nativeK5FJBaseAtom W R) := by
  change
    nativeK5AXPack W
        (nativeK5AQWhiskerCell W side (nativeK5FJConservativeRefl W R)) =
      nativeK5AXPack W
        (nativeK5AQWhiskerCell W side (nativeK5FJConservativeAtom W R))
  exact congrArg (nativeK5AXPack W)
    (nativeK5FJWhisker_conservative_collision W R side)

/-- Unlike generic abstract frame models, the ACTUAL physical
base singleton mapTotal has an explicit Type-valued collision. -/
theorem nativeK5FJBaseFrame_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    ¬ Function.Injective ((nativeK5BCFrame W side).mapTotal) := by
  intro hinj
  exact nativeK5FJBaseRefl_ne_atom W R
    (hinj (nativeK5FJBaseFrame_collision W R side))

/-- Lift each original lower source into the complete original
dependent 17D layer via its actual REFLEXIVE raw16D proof.
No extra 17D generator is introduced. -/
def nativeK5FJSeventeenRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)).Total :=
  ⟨(nativeK5FJBaseRefl W R, nativeK5FJBaseRefl W R),
    .refl (nativeK5FJBaseRefl W R)⟩

def nativeK5FJSeventeenAtom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)).Total :=
  ⟨(nativeK5FJBaseAtom W R, nativeK5FJBaseAtom W R),
    .refl (nativeK5FJBaseAtom W R)⟩

/-- Distinct source 15D proofs remain distinct when fully stored
as original 17D Type-valued identity comparison objects. -/
theorem nativeK5FJSeventeenRefl_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5FJSeventeenRefl W R ≠
      nativeK5FJSeventeenAtom W R := by
  intro heq
  exact nativeK5FJBaseRefl_ne_atom W R
    (congrArg
      (fun t : (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)).Total => t.1.1) heq)

/-- An explicit collision in the ACTUAL genuine DR singleton 17D
frame, with all original 15D and raw16D endpoints retained. -/
theorem nativeK5FJSeventeenFrame_collision
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) side).mapTotal
        (nativeK5FJSeventeenRefl W R) =
      (nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) side).mapTotal
          (nativeK5FJSeventeenAtom W R) := by
  have hbase := nativeK5FJBaseFrame_collision W R side
  change
    (⟨((nativeK5BCFrame W side).mapTotal (nativeK5FJBaseRefl W R),
        (nativeK5BCFrame W side).mapTotal (nativeK5FJBaseRefl W R)),
        NativeC60AXStep.refl _⟩ :
        (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)).Total) =
      ⟨((nativeK5BCFrame W side).mapTotal (nativeK5FJBaseAtom W R),
        (nativeK5BCFrame W side).mapTotal (nativeK5FJBaseAtom W R)),
        NativeC60AXStep.refl _⟩
  exact congrArg
    (fun t : (nativeK5AXBaseLayer W).Total =>
      (⟨(t, t), NativeC60AXStep.refl t⟩ :
        (nativeC60DQSeventeenLayer (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)).Total)) hbase

/-- Thus the actual 17D singleton frame mapTotal is
NONINJECTIVE. The hypothesis in FI #2676 fails for this
specific original physical AQ presentation, not merely abstractly. -/
theorem nativeK5FJSeventeenFrame_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    ¬ Function.Injective
      ((nativeC60DRSeventeenFrame (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) side).mapTotal) := by
  intro hinj
  exact nativeK5FJSeventeenRefl_ne_atom W R
    (hinj (nativeK5FJSeventeenFrame_collision W R side))

/-- The real physical singleton fails the exact FI whole original
18D noncommutative FreeGroup faithfulness gate. This does NOT
assert any geometric 19D filler or equality of the original
distinct 18D evidence before the context is applied. -/
theorem nativeK5FJPhysicalSingleton_fullWord_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (side : Bool) :
    ¬ Function.Injective
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [side]) := by
  intro hfull
  have hctx := (nativeC60FIFullFree_injective_iff_context
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [side]).mp hfull
  exact nativeK5FJSeventeenRefl_ne_atom W R
    (hctx (nativeK5FJSeventeenFrame_collision W R side))

end ActualPhysicalSingletonCollision

#print axioms nativeK5FJConservativeRefl_ne_atom
#print axioms nativeK5FJWhisker_conservative_collision
#print axioms nativeK5FJWhiskerCell_not_injective
#print axioms nativeK5FJBaseRefl_ne_atom
#print axioms nativeK5FJBaseFrame_collision
#print axioms nativeK5FJBaseFrame_not_injective
#print axioms nativeK5FJSeventeenRefl_ne_atom
#print axioms nativeK5FJSeventeenFrame_collision
#print axioms nativeK5FJSeventeenFrame_not_injective
#print axioms nativeK5FJPhysicalSingleton_fullWord_not_injective

end
end Kuu.F112.Physical
