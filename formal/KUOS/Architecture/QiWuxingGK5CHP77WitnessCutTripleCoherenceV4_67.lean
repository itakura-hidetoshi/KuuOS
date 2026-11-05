import KUOS.Architecture.QiWuxingGK5CHP77TypedPatchChainCutGluingV4_66
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.67 — ORIGINAL P77 TYPED WITNESS SPLITTING AND TRIPLE-CUT COHERENCE.

Qi v4.65 has true original F55/P77 finite typed patch chains,
source path witness Type and unique recovery. Qi v4.66 has the
original type-correct append of two chains, genuine GK5CG conservative
Type-valued five-cell compatibility iff, faithful source witness
gluing, and original P77 quotient vertical-composition coherence.

NEW: give an ACTUAL typed inverse at any specified finite-chain cut,
turning the full-chain proof-bearing source-path witness Type into
the PRODUCT of its two exact original source witness Types.
This is a genuine Type-level Equiv, not equality of signed charges.

For any THREE finite typed chains, prove that the left and right
parenthesized source witnesses agree after transporting through
the previously proved genuine chain associator. Their recovered
source free paths and original F55/P77 conservative quotient classes
agree strictly, respecting the original category composition and
the exact original Type-valued GK5CG evidence at each segment.

Do NOT infer global target fullness or arbitrary intermediate
reachability from an unrelated whole-target composite. No numeric
proxy, no new reverse source edge, no Gray or pentagonator. Original
F55/P77/P94A, north C60 physical gauge and CRT remain separate
authorities. Strict 空 is central; independent Kuu a presentation.

Append-only same-root, public root107, protected PR #1558 stays
Draft/open/unmerged. No new axioms, sorry, admit, native_decide.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

/-- Extract the TRUE two dependent original source-path witness
families from any witness of their appended original patch chain.
The cut carries the actual middle FivefoldPathVertex. -/
def fivefoldP77RawPatchChainSplitWitness
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right) →
      FivefoldP77RawPatchChainWitness f g h k left ×
        FivefoldP77RawPatchChainWitness f g h k right := by
  induction left with
  | nil vertex =>
      intro full
      exact (PUnit.unit, full)
  | cons block tail ih =>
      intro full
      let parts := ih right full.2
      exact ((full.1, parts.1), parts.2)

/-- Genuine TYPE-level equivalence of the whole original F55/P77
source-certified patch witness family with the product of the
original source-certified families of both cut pieces. -/
def fivefoldP77RawPatchChainCutWitnessEquiv
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right) ≃
      (FivefoldP77RawPatchChainWitness f g h k left ×
        FivefoldP77RawPatchChainWitness f g h k right) := by
  refine {
    toFun := fivefoldP77RawPatchChainSplitWitness f g h k left right
    invFun := fun pair =>
      fivefoldP77RawPatchChainAppendWitness f g h k left right
        pair.1 pair.2
    left_inv := ?_
    right_inv := ?_
  }
  · intro full
    letI : Subsingleton
        (FivefoldP77RawPatchChainWitness f g h k
          (fivefoldP77RawPatchChainAppend f g h k left right)) :=
      fivefoldP77RawPatchChain_witness_subsingleton f g h k _
    exact Subsingleton.elim _ _
  · intro pair
    letI : Subsingleton
        (FivefoldP77RawPatchChainWitness f g h k left) :=
      fivefoldP77RawPatchChain_witness_subsingleton f g h k left
    letI : Subsingleton
        (FivefoldP77RawPatchChainWitness f g h k right) :=
      fivefoldP77RawPatchChain_witness_subsingleton f g h k right
    exact Subsingleton.elim _ _

/-- An original P77 appended chain admits a genuine source-path
witness IFF both of its specified component chains do. No charge
criterion or illicit whole-target factorization is used. -/
theorem fivefoldP77RawPatchChainCutWitness_nonempty_iff
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w) :
    Nonempty (FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right)) ↔
    (Nonempty (FivefoldP77RawPatchChainWitness f g h k left) ∧
      Nonempty (FivefoldP77RawPatchChainWitness f g h k right)) := by
  constructor
  · rintro ⟨full⟩
    let pair := (fivefoldP77RawPatchChainCutWitnessEquiv
      f g h k left right).toFun full
    exact ⟨⟨pair.1⟩, ⟨pair.2⟩⟩
  · rintro ⟨⟨wLeft⟩, ⟨wRight⟩⟩
    exact ⟨fivefoldP77RawPatchChainAppendWitness
      f g h k left right wLeft wRight⟩

/-- Splitting and reassembling a true source-certified original
P77 finite patch chain does not change its ACTUAL typed source
finite path; it is EXACT original Quiver.Path composition. -/
theorem fivefoldP77RawPatchChainSplit_path
    {u v w : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (right : FivefoldP77RawPatchChain f g h k v w)
    (full : FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchChainAppend f g h k left right)) :
    fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right) full =
      (fivefoldP77RawPatchChainPath f g h k left
        (fivefoldP77RawPatchChainSplitWitness f g h k left right full).1).comp
      (fivefoldP77RawPatchChainPath f g h k right
        (fivefoldP77RawPatchChainSplitWitness f g h k left right full).2) := by
  let split := fivefoldP77RawPatchChainSplitWitness f g h k left right full
  have hRejoin :
      fivefoldP77RawPatchChainAppendWitness f g h k left right
          split.1 split.2 = full :=
    (fivefoldP77RawPatchChainCutWitnessEquiv
      f g h k left right).left_inv full
  calc
    fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right) full =
      fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k left right)
        (fivefoldP77RawPatchChainAppendWitness f g h k left right
          split.1 split.2) := by
      exact congrArg
        (fivefoldP77RawPatchChainPath f g h k
          (fivefoldP77RawPatchChainAppend f g h k left right))
        hRejoin.symm
    _ = (fivefoldP77RawPatchChainPath f g h k left split.1).comp
          (fivefoldP77RawPatchChainPath f g h k right split.2) :=
      fivefoldP77RawPatchChainAppend_path f g h k left right split.1 split.2

/-- Left association of three TRUE source-certified original P77
finite patch chains, keeping every source witness and typed cut. -/
def fivefoldP77RawPatchChainTripleLeftWitness
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wMiddle : FivefoldP77RawPatchChainWitness f g h k middle)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right) :=
  fivefoldP77RawPatchChainAppendWitness f g h k
    (fivefoldP77RawPatchChainAppend f g h k left middle) right
    (fivefoldP77RawPatchChainAppendWitness f g h k left middle
      wLeft wMiddle) wRight

/-- Right association of the same THREE original dependent typed
P77 patch-chain witnesses. -/
def fivefoldP77RawPatchChainTripleRightWitness
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wMiddle : FivefoldP77RawPatchChainWitness f g h k middle)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    FivefoldP77RawPatchChainWitness f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        left (fivefoldP77RawPatchChainAppend f g h k middle right)) :=
  fivefoldP77RawPatchChainAppendWitness f g h k left
    (fivefoldP77RawPatchChainAppend f g h k middle right)
    wLeft
    (fivefoldP77RawPatchChainAppendWitness f g h k middle right
      wMiddle wRight)

/-- Genuine TYPE-valued triple-cut coherence: the two original
source witness families agree after transporting along the
actual dependent patch-chain associator, not after a numerical
charge comparison or a fabricated higher cell. -/
theorem fivefoldP77RawPatchChainTriple_witness_transport
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wMiddle : FivefoldP77RawPatchChainWitness f g h k middle)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    Eq.mp
      (congrArg (FivefoldP77RawPatchChainWitness f g h k)
        (fivefoldP77RawPatchChainAppend_assoc f g h k left middle right))
      (fivefoldP77RawPatchChainTripleLeftWitness
        f g h k left middle right wLeft wMiddle wRight) =
      fivefoldP77RawPatchChainTripleRightWitness
        f g h k left middle right wLeft wMiddle wRight := by
  letI : Subsingleton
      (FivefoldP77RawPatchChainWitness f g h k
        (fivefoldP77RawPatchChainAppend f g h k
          left (fivefoldP77RawPatchChainAppend f g h k middle right))) :=
    fivefoldP77RawPatchChain_witness_subsingleton f g h k _
  exact Subsingleton.elim _ _

/-- ORIGINAL source finite free-path reconstruction is exactly
independent of all two parenthesizations of a three-way typed
F55/P77 patch-chain cut: (A ⋅ B) ⋅ C = A ⋅ (B ⋅ C). -/
theorem fivefoldP77RawPatchChainTriple_path_coherence
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wMiddle : FivefoldP77RawPatchChainWitness f g h k middle)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    fivefoldP77RawPatchChainPath f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right)
      (fivefoldP77RawPatchChainTripleLeftWitness
        f g h k left middle right wLeft wMiddle wRight) =
    fivefoldP77RawPatchChainPath f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        left (fivefoldP77RawPatchChainAppend f g h k middle right))
      (fivefoldP77RawPatchChainTripleRightWitness
        f g h k left middle right wLeft wMiddle wRight) := by
  let pathL := fivefoldP77RawPatchChainPath f g h k left wLeft
  let pathM := fivefoldP77RawPatchChainPath f g h k middle wMiddle
  let pathR := fivefoldP77RawPatchChainPath f g h k right wRight
  calc
    fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k
          (fivefoldP77RawPatchChainAppend f g h k left middle) right)
        (fivefoldP77RawPatchChainTripleLeftWitness
          f g h k left middle right wLeft wMiddle wRight) =
      (fivefoldP77RawPatchChainPath f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle)
        (fivefoldP77RawPatchChainAppendWitness f g h k left middle
          wLeft wMiddle)).comp pathR :=
      fivefoldP77RawPatchChainAppend_path f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right
        (fivefoldP77RawPatchChainAppendWitness f g h k left middle
          wLeft wMiddle) wRight
    _ = (pathL.comp pathM).comp pathR := by
      exact congrArg (fun q : Quiver.Path u w => q.comp pathR)
        (fivefoldP77RawPatchChainAppend_path f g h k
          left middle wLeft wMiddle)
    _ = pathL.comp (pathM.comp pathR) :=
      Quiver.Path.comp_assoc _ _ _
    _ = pathL.comp
          (fivefoldP77RawPatchChainPath f g h k
            (fivefoldP77RawPatchChainAppend f g h k middle right)
            (fivefoldP77RawPatchChainAppendWitness f g h k middle right
              wMiddle wRight)) := by
      exact congrArg (fun q : Quiver.Path v t => pathL.comp q)
        (fivefoldP77RawPatchChainAppend_path f g h k
          middle right wMiddle wRight).symm
    _ = fivefoldP77RawPatchChainPath f g h k
          (fivefoldP77RawPatchChainAppend f g h k
            left (fivefoldP77RawPatchChainAppend f g h k middle right))
          (fivefoldP77RawPatchChainTripleRightWitness
            f g h k left middle right wLeft wMiddle wRight) :=
      (fivefoldP77RawPatchChainAppend_path f g h k
        left (fivefoldP77RawPatchChainAppend f g h k middle right)
        wLeft (fivefoldP77RawPatchChainAppendWitness
          f g h k middle right wMiddle wRight)).symm

/-- The ORIGINAL GK5CG conservative 5-cell quotient values of
three genuinely typed raw patch chains are independent of the
two ways to parenthesize their actual typed concatenation. -/
theorem fivefoldP77RawPatchChainTriple_target_coherence
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t) :
    fivefoldP77RawPatchChainTarget f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right) =
    fivefoldP77RawPatchChainTarget f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        left (fivefoldP77RawPatchChainAppend f g h k middle right)) := by
  exact congrArg
    (fivefoldP77RawPatchChainTarget f g h k)
    (fivefoldP77RawPatchChainAppend_assoc f g h k left middle right)

/-- Strongest three-piece coherence: both parenthesizations
yield exactly the SAME original source-certified P77 conservative
Hom quotient element with its genuine reachability proof.
The equality is in the ACTUAL proof-bearing dependent Subtype. -/
theorem fivefoldP77RawPatchChainTriple_certified_coherence
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (wLeft : FivefoldP77RawPatchChainWitness f g h k left)
    (wMiddle : FivefoldP77RawPatchChainWitness f g h k middle)
    (wRight : FivefoldP77RawPatchChainWitness f g h k right) :
    fivefoldP77RawPatchChainCertified f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right)
      (fivefoldP77RawPatchChainTripleLeftWitness
        f g h k left middle right wLeft wMiddle wRight) =
    fivefoldP77RawPatchChainCertified f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        left (fivefoldP77RawPatchChainAppend f g h k middle right))
      (fivefoldP77RawPatchChainTripleRightWitness
        f g h k left middle right wLeft wMiddle wRight) := by
  letI := fivefoldP77ConservativeCategory f g h k
  apply Subtype.ext
  calc
    (fivefoldP77RawPatchChainCertified f g h k
        (fivefoldP77RawPatchChainAppend f g h k
          (fivefoldP77RawPatchChainAppend f g h k left middle) right)
        (fivefoldP77RawPatchChainTripleLeftWitness
          f g h k left middle right wLeft wMiddle wRight)).val =
      fivefoldP77RawPatchChainTarget f g h k
        (fivefoldP77RawPatchChainAppend f g h k
          (fivefoldP77RawPatchChainAppend f g h k left middle) right) :=
      fivefoldP77RawPatchChainCertified_val f g h k _ _
    _ = fivefoldP77RawPatchChainTarget f g h k
          (fivefoldP77RawPatchChainAppend f g h k
            left (fivefoldP77RawPatchChainAppend f g h k middle right)) :=
      fivefoldP77RawPatchChainTriple_target_coherence
        f g h k left middle right
    _ = (fivefoldP77RawPatchChainCertified f g h k
          (fivefoldP77RawPatchChainAppend f g h k
            left (fivefoldP77RawPatchChainAppend f g h k middle right))
          (fivefoldP77RawPatchChainTripleRightWitness
            f g h k left middle right wLeft wMiddle wRight)).val :=
      (fivefoldP77RawPatchChainCertified_val f g h k _ _).symm

/-- A missing Type-valued original source certificate of the
MIDDLE specified chain obstructs the entire designated three-piece
factorwise gluing, without asserting all-target cancellation. -/
theorem fivefoldP77RawPatchChainTriple_middle_obstruction
    {u v w t : FivefoldPathVertex}
    (left : FivefoldP77RawPatchChain f g h k u v)
    (middle : FivefoldP77RawPatchChain f g h k v w)
    (right : FivefoldP77RawPatchChain f g h k w t)
    (hmissing : ¬ fivefoldP77RawPatchChainCompatible f g h k middle) :
    ¬ fivefoldP77RawPatchChainCompatible f g h k
      (fivefoldP77RawPatchChainAppend f g h k
        (fivefoldP77RawPatchChainAppend f g h k left middle) right) := by
  apply fivefoldP77RawPatchChainAppend_left_obstruction
    f g h k (fivefoldP77RawPatchChainAppend f g h k left middle) right
  exact fivefoldP77RawPatchChainAppend_right_obstruction
    f g h k left middle hmissing

#print axioms fivefoldP77RawPatchChainSplitWitness
#print axioms fivefoldP77RawPatchChainCutWitnessEquiv
#print axioms fivefoldP77RawPatchChainCutWitness_nonempty_iff
#print axioms fivefoldP77RawPatchChainSplit_path
#print axioms fivefoldP77RawPatchChainTripleLeftWitness
#print axioms fivefoldP77RawPatchChainTripleRightWitness
#print axioms fivefoldP77RawPatchChainTriple_witness_transport
#print axioms fivefoldP77RawPatchChainTriple_path_coherence
#print axioms fivefoldP77RawPatchChainTriple_target_coherence
#print axioms fivefoldP77RawPatchChainTriple_certified_coherence
#print axioms fivefoldP77RawPatchChainTriple_middle_obstruction

end
end KUOS.Architecture.WuxingPentagonUnified
