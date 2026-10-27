import Kuu.F112.PolygonNativeC60StrictCompositionFromFullCN

/-!
# F112-P94D3DN — arbitrary finite genuine C60 inner-AQ strict coherence

DM proves that the TRUE original strict inner-prefix isomorphism composes,
using all original CN letters, complete Type-valued 16D BV certificates,
and CY's whole free-isotropy theorem. DN extends this to EVERY FINITE
SEQUENCE of independently ordered C60 inner AQ prefixes, not just two.

A list of finite Bool context words records applications in chronological
order. Its exact ordered total word is defined by structural recursion:
the later context word is prepended on the LEFT, never commuted. We
define a genuine recursively iterated MulEquiv of the full strict
automorphism groups, retaining the exact original 14D fiber and the
dependent source/target 15D boundaries at every intermediate stage.

The normal form of this independently constructed finite strict action
is the existing ONE-STAGE original DF strict equivalence with its total
finite prefix. The proof is by induction using DM's actual whole-group
composition equality and explicit dependent List.append_assoc transport.
Consequently all signed noncommutative CN words, the full BW holonomy,
and the original strict composition law are coherent for arbitrary
finite length without postulating any additional geometric 16-cell.

Keep strict Kuu, independent Kuu as a presentation, no Gray, no erasure
of old no-go, no new axiom, sorry or admit, and unchanged 107 roots.
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

/-- Ordered accumulation of an arbitrary finite family of true inner AQ
prefixes; chronological s then t is the NONCOMMUTATIVE word t ++ s. -/
def nativeK5DNPrefixWord : List (List Bool) → List Bool
  | [] => []
  | shift :: rest => nativeK5DNPrefixWord rest ++ shift

theorem nativeK5DNPrefixWord_nil :
    nativeK5DNPrefixWord [] = [] := rfl

theorem nativeK5DNPrefixWord_cons
    (shift : List Bool) (rest : List (List Bool)) :
    nativeK5DNPrefixWord (shift :: rest) =
      nativeK5DNPrefixWord rest ++ shift := rfl

/-- Prefix aggregation reverses the order of chronological list
concatenation, not the internal order of any individual AQ word. -/
theorem nativeK5DNPrefixWord_append
    (steps more : List (List Bool)) :
    nativeK5DNPrefixWord (steps ++ more) =
      nativeK5DNPrefixWord more ++ nativeK5DNPrefixWord steps := by
  induction steps with
  | nil =>
      simp [nativeK5DNPrefixWord]
  | cons shift rest ih =>
      change nativeK5DNPrefixWord (rest ++ more) ++ shift =
        nativeK5DNPrefixWord more ++
          (nativeK5DNPrefixWord rest ++ shift)
      rw [ih, List.append_assoc]

section PhysicalFiniteAction

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

/-- The true DF whole-strict equivalence for the ordered accumulated
finite AQ word; does not impose any new original 16D relations. -/
def nativeK5DNDirectStrict
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (steps : List (List Bool)) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R (nativeK5DNPrefixWord steps ++ inner) outer :=
  nativeK5DFInnerPrefixStrictEquiv W R inner outer (nativeK5DNPrefixWord steps)

/-- The empty true inner AQ prefix acts as the identity on EVERY
original conservative strict automorphism. The result is derived from
DM's genuine whole-strict composition and injectivity, not assumed. -/
theorem nativeK5DNInnerPrefixStrict_nil
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DFInnerPrefixStrictEquiv W R inner outer [] =
      MulEquiv.refl _ := by
  apply MulEquiv.ext
  intro z
  let T := nativeK5DFInnerPrefixStrictEquiv W R inner outer []
  have hc := DFunLike.congr_fun
    (nativeK5DMInnerPrefixStrict_comp W R inner outer ([] : List Bool) []) z
  change T (T z) = T z at hc
  exact T.injective hc

/-- An actual identity transport for the empty finite context family. -/
theorem nativeK5DNDirectStrict_nil
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DNDirectStrict W R inner outer [] = MulEquiv.refl _ :=
  nativeK5DNInnerPrefixStrict_nil W R inner outer

/-- A single finite AQ context agrees with the original DF strict
equivalence, not merely its observed DC parity or quotient. -/
theorem nativeK5DNDirectStrict_singleton
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DNDirectStrict W R inner outer [shift] =
      nativeK5DFInnerPrefixStrictEquiv W R inner outer shift := by
  rfl

/-- Genuine physical one-step recursion on the full original strict
groups. The Type-valued target is transported along the exact
associator for the ordered finite AQ context word. -/
theorem nativeK5DNDirectStrict_cons
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) (rest : List (List Bool)) :
    ((List.append_assoc (nativeK5DNPrefixWord rest) shift inner).symm ▸
      ((nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).trans
        (nativeK5DNDirectStrict W R (shift ++ inner) outer rest))) =
      nativeK5DNDirectStrict W R inner outer (shift :: rest) := by
  change nativeK5DLTwoStageStrict W R inner outer shift
      (nativeK5DNPrefixWord rest) =
    nativeK5DLOneStageStrict W R inner outer shift
      (nativeK5DNPrefixWord rest)
  exact nativeK5DMInnerPrefixStrict_comp W R inner outer shift
    (nativeK5DNPrefixWord rest)

/-- INDEPENDENTLY RECURSIVE genuine finite strict action: first
apply the head real DF equivalence, then recursively transport through
every remaining actual AQ prefix. This is not defined by the one-stage
direct normal form, so the following theorem is substantive. -/
def nativeK5DNIteratedStrict
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (outer : List Bool) :
    (inner : List Bool) → (steps : List (List Bool)) →
      nativeK5DBIsotropy W R inner outer ≃*
        nativeK5DBIsotropy W R (nativeK5DNPrefixWord steps ++ inner) outer
  | inner, [] => MulEquiv.refl _
  | inner, shift :: rest => by
      let first := nativeK5DFInnerPrefixStrictEquiv W R inner outer shift
      let remaining := nativeK5DNIteratedStrict W R outer (shift ++ inner) rest
      exact (List.append_assoc (nativeK5DNPrefixWord rest) shift inner).symm ▸
        (first.trans remaining)

/-- MAIN DN induction: the genuine sequential full-strict action for
ANY finite ordered original AQ prefix family is EXACTLY the one-stage
strict transport with its correctly ordered accumulated prefix.
All intermediate 14D/15D dependent boundaries remain typed. -/
theorem nativeK5DNIteratedStrict_eq_direct
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (steps : List (List Bool)) :
    nativeK5DNIteratedStrict W R outer inner steps =
      nativeK5DNDirectStrict W R inner outer steps := by
  induction steps generalizing inner with
  | nil =>
      change MulEquiv.refl _ =
        nativeK5DFInnerPrefixStrictEquiv W R inner outer []
      exact (nativeK5DNInnerPrefixStrict_nil W R inner outer).symm
  | cons shift rest ih =>
      change
        ((List.append_assoc (nativeK5DNPrefixWord rest) shift inner).symm ▸
          ((nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).trans
            (nativeK5DNIteratedStrict W R outer (shift ++ inner) rest))) =
        nativeK5DNDirectStrict W R inner outer (shift :: rest)
      rw [ih (shift ++ inner)]
      exact nativeK5DNDirectStrict_cons W R inner outer shift rest

/-- Every genuinely constructed finite iterated strict equivalence
is bijective on all ORIGINAL strict automorphisms. -/
theorem nativeK5DNIteratedStrict_bijective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (steps : List (List Bool)) :
    Function.Bijective (nativeK5DNIteratedStrict W R outer inner steps) :=
  (nativeK5DNIteratedStrict W R outer inner steps).bijective

/-- Two successive independently finite true AQ prefix families act
as their one-stage combined ordered prefix on the ORIGINAL strict
group. Exact associator transport is the only reindexing performed. -/
theorem nativeK5DNIteratedStrict_append_direct
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (steps more : List (List Bool)) :
    ((List.append_assoc
        (nativeK5DNPrefixWord more) (nativeK5DNPrefixWord steps) inner).symm ▸
      ((nativeK5DNIteratedStrict W R outer inner steps).trans
        (nativeK5DNIteratedStrict W R outer
          (nativeK5DNPrefixWord steps ++ inner) more))) =
      nativeK5DFInnerPrefixStrictEquiv W R inner outer
        (nativeK5DNPrefixWord more ++ nativeK5DNPrefixWord steps) := by
  rw [nativeK5DNIteratedStrict_eq_direct W R inner outer steps,
    nativeK5DNIteratedStrict_eq_direct W R
      (nativeK5DNPrefixWord steps ++ inner) outer more]
  change nativeK5DLTwoStageStrict W R inner outer
      (nativeK5DNPrefixWord steps) (nativeK5DNPrefixWord more) =
    nativeK5DLOneStageStrict W R inner outer
      (nativeK5DNPrefixWord steps) (nativeK5DNPrefixWord more)
  exact nativeK5DMInnerPrefixStrict_comp W R inner outer
    (nativeK5DNPrefixWord steps) (nativeK5DNPrefixWord more)

end PhysicalFiniteAction

#print axioms nativeK5DNPrefixWord_nil
#print axioms nativeK5DNPrefixWord_cons
#print axioms nativeK5DNPrefixWord_append
#print axioms nativeK5DNDirectStrict
#print axioms nativeK5DNInnerPrefixStrict_nil
#print axioms nativeK5DNDirectStrict_nil
#print axioms nativeK5DNDirectStrict_singleton
#print axioms nativeK5DNDirectStrict_cons
#print axioms nativeK5DNIteratedStrict
#print axioms nativeK5DNIteratedStrict_eq_direct
#print axioms nativeK5DNIteratedStrict_bijective
#print axioms nativeK5DNIteratedStrict_append_direct

end
end Kuu.F112.Physical
