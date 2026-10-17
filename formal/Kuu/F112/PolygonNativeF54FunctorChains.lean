import Kuu.F112.PolygonNativeF45FunctorAxes
import Kuu.F112.PolygonNativeF54Chains

/-!
# F112-E7Q5-E1: genuinely typed F54 functorial rotation-source comparison

Extend independently proved E7Q5-C/D functor transport of both raw
categorical Blocks/F45 axes to original-shaped F54 LOCAL ROTATIONS
and arbitrary finite bidirectional Type-valued rotation chains.

No equality of different original raw F19/F28 histories is assumed.
All 5/6-sided C60 physical sector witnesses remain intact. Both
independent Nat.add_assoc depth casts are transported, rather than
deleted, and the forward/backward direction of each source rotation
is preserved. Proofs compare the actual constructors, not their
integer shadow/phase decorations.

This is a POSITIVE map inside the independent Kuu F112 source,
not a claimed isomorphism to the frozen legacy KUOS F54 grammar.
It imports neither original Gray nor F51/F77.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- Transport an ACTUAL original-shaped root associativity or either
contextual F54 rotation, preserving each source proof and both
independent Nat.add_assoc equalities of the root rotation. -/
def KuuNativeF45Tree.LocalRotation.mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    KuuNativeF45Tree.LocalRotation p
      (before.mapAxes F G) (after.mapAxes F G) := by
  induction step with
  | assoc first second third =>
      rw [KuuNativeF45Tree.mapAxes_castDepths]
      exact KuuNativeF45Tree.LocalRotation.assoc
        (first.mapAxes F G) (second.mapAxes F G)
        (third.mapAxes F G)
  | leftContext step later ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.LocalRotation.leftContext
          ih (later.mapAxes F G))
  | rightContext earlier step ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.LocalRotation.rightContext
          (earlier.mapAxes F G) ih)

/-- After transporting all originally typed raw data, the same
actual C60 physical sector boundary still witnesses this rotation. -/
theorem KuuNativeF45Tree.LocalRotation.mapAxes_sectors
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    (before.mapAxes F G).sectors = (after.mapAxes F G).sectors :=
  (step.mapAxes F G).sectors_eq

/-- Transport real FORWARD and BACKWARD edges without replacing a
backward source proof with a formal cell from a quotient. -/
def KuuNativeF45Tree.RotationEdge.mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    KuuNativeF45Tree.RotationEdge p
      (before.mapAxes F G) (after.mapAxes F G) := by
  cases edge with
  | forward step =>
      exact .forward (step.mapAxes F G)
  | backward step =>
      exact .backward (step.mapAxes F G)

/-- Reversing a SPECIFIC raw directed edge commutes with both genuine
category functors: orientation is never erased by this comparison. -/
theorem KuuNativeF45Tree.RotationEdge.mapAxes_reverse
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    (edge.reverse.mapAxes F G) = (edge.mapAxes F G).reverse := by
  cases edge <;> rfl

/-- Every arbitrary-length bidirectional rotation chain is
transported inductively with ALL its intermediate F45 source trees,
real orientation data and exact two-axis Nat depths. -/
def KuuNativeF45Tree.RotationChain.mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    KuuNativeF45Tree.RotationChain p
      (first.mapAxes F G) (last.mapAxes F G) := by
  induction chain with
  | refl =>
      exact .refl _
  | snoc prior edge ih =>
      exact .snoc ih (edge.mapAxes F G)

/-- The number of ACTUAL typed F54 rotation witnesses is identical
before/after any pair of independent source-category functors. -/
theorem KuuNativeF45Tree.RotationChain.length_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    (chain.mapAxes F G).length = chain.length := by
  induction chain with
  | refl =>
      rfl
  | snoc prior edge ih =>
      change (prior.mapAxes F G).length + 1 = prior.length + 1
      exact congrArg Nat.succ ih

/-- Finite F54 raw chain composition commutes EXACTLY with the
constructed typed two-category transport, not only after shadow. -/
theorem KuuNativeF45Tree.RotationChain.mapAxes_append
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first middle last : KuuNativeF45Tree p n m ma pa mb pb}
    (left : KuuNativeF45Tree.RotationChain p first middle)
    (right : KuuNativeF45Tree.RotationChain p middle last) :
    (left.append right).mapAxes F G =
      (left.mapAxes F G).append (right.mapAxes F G) := by
  induction right with
  | refl => rfl
  | snoc prior edge ih =>
      change KuuNativeF45Tree.RotationChain.snoc
          ((left.append prior).mapAxes F G) (edge.mapAxes F G) =
        KuuNativeF45Tree.RotationChain.snoc
          ((left.mapAxes F G).append (prior.mapAxes F G))
          (edge.mapAxes F G)
      exact congrArg
        (fun z => KuuNativeF45Tree.RotationChain.snoc
          z (edge.mapAxes F G)) ih

/-- Forward/backward path reversal also commutes with actual source
transport of the entire finite chain; backtracks remain nontrivial. -/
theorem KuuNativeF45Tree.RotationChain.mapAxes_reverse
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    (chain.reverse.mapAxes F G) = (chain.mapAxes F G).reverse := by
  induction chain with
  | refl => rfl
  | snoc prior edge ih =>
      change
        (((KuuNativeF45Tree.RotationChain.snoc (.refl _)
            edge.reverse).append prior.reverse).mapAxes F G) =
          ((KuuNativeF45Tree.RotationChain.snoc (.refl _)
              ((edge.mapAxes F G).reverse)).append
              (prior.mapAxes F G).reverse)
      calc
        (((KuuNativeF45Tree.RotationChain.snoc (.refl _)
            edge.reverse).append prior.reverse).mapAxes F G) =
            ((KuuNativeF45Tree.RotationChain.snoc (.refl _)
              edge.reverse).mapAxes F G).append
              (prior.reverse.mapAxes F G) :=
                KuuNativeF45Tree.RotationChain.mapAxes_append F G _ _
        _ = ((KuuNativeF45Tree.RotationChain.snoc (.refl _)
              ((edge.mapAxes F G).reverse)).append
              (prior.mapAxes F G).reverse) := by
                rw [ih]
                change
                  (KuuNativeF45Tree.RotationChain.snoc (.refl _)
                    (edge.reverse.mapAxes F G)).append
                      (prior.mapAxes F G).reverse =
                    (KuuNativeF45Tree.RotationChain.snoc (.refl _)
                      ((edge.mapAxes F G).reverse)).append
                      (prior.mapAxes F G).reverse
                rw [KuuNativeF45Tree.RotationEdge.mapAxes_reverse]

/-- The concrete north pentagon 2-step forward/backward return
retains precisely TWO genuine Type-valued F54 rotation steps under
arbitrary two-axis functors out of the original C60 Site. -/
theorem northNativeF45TripleBacktrack_mapAxes_length
    (F : Site ⥤ A₂) (G : Site ⥤ B₂) :
    (northNativeF45TripleBacktrack.mapAxes F G).length = 2 := by
  rw [KuuNativeF45Tree.RotationChain.length_mapAxes]
  exact northNativeF45TripleBacktrack_length

#print axioms KuuNativeF45Tree.LocalRotation.mapAxes
#print axioms KuuNativeF45Tree.LocalRotation.mapAxes_sectors
#print axioms KuuNativeF45Tree.RotationEdge.mapAxes
#print axioms KuuNativeF45Tree.RotationEdge.mapAxes_reverse
#print axioms KuuNativeF45Tree.RotationChain.mapAxes
#print axioms KuuNativeF45Tree.RotationChain.length_mapAxes
#print axioms KuuNativeF45Tree.RotationChain.mapAxes_append
#print axioms KuuNativeF45Tree.RotationChain.mapAxes_reverse
#print axioms northNativeF45TripleBacktrack_mapAxes_length
end
end Kuu.F112.Physical
