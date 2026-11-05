import KUOS.Architecture.QiWuxingGK5CHP77TwoSegmentLocalTypeDescentV4_64
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.65 — ORIGINAL P77 ARBITRARY FINITE TYPED PATCH-CHAIN DESCENT.

An indexed original F55/P77 raw four-proof patch FAMILY at each
genuinely typed source boundary is kept as a dependent block,
with its genuine GK5CG conservative Type-valued five-cell overlaps
and one original evaluated source-path five-cell anchor as the
precise, necessary-and-sufficient local certificate.

A new dependent inductive chain (empty or a block followed by
another chain) supports ARBITRARY FINITE numbers of patches,
not merely v4.64's two stages. The proof-bearing space of
factorwise typed finite source paths is inhabited exactly when
ALL the original GK5CG Type-valued patch descent conditions hold.
When inhabited, this proof-bearing space is a Subsingleton:
the original faithful P77 functor makes all typed source
segment paths unique, rather than merely charge-equivalent.

The chosen segment paths concatenate to an ACTUAL original typed
FivefoldEdge free path. Its evaluation is precisely the ordered
original P77 conservative-quotient composition of the underlying
raw patch classes; the v4.62 certified partial recovery returns the
WHOLE original typed path, with original charge equal to its length.
This result includes empty chains and arbitrary finite nonempty
chains while retaining each raw patch family and its history.

NO unproved inference from a whole target composite to an
arbitrary missing intermediate source path, no global recovery on
the entire original P77 target, no general sheaf claim.
No numerical proxies, fabricated reverse source edges,
new pentagonator or Gray. Genuine F55/P77/P94A, physical C60
and north C60 CRT retain distinct authorities.

Append-only same-root, public root107, strict 空 central;
independent Kuu remains one presentation. No new axioms,
sorry, admit or native_decide. Protected validation-only #1558
Draft/open/unmerged. Lean v4.30.0-rc2, pinned mathlib
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

/-- One actual original P77 patch family at a fixed TYPED Hom.
No overlap/anchor assumption is baked into its data. -/
structure FivefoldP77RawPatchBlock
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    (u v : FivefoldPathVertex) where
  Index : Type
  nonempty : Nonempty Index
  raw : Index → FivefoldP77LocalRaw f g h k u v

/-- Genuine necessary and sufficient local descent evidence of a
block, with real original GK5CG Type-valued five-cell witnesses. -/
def fivefoldP77RawPatchBlockCompatible
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) : Prop :=
  (∀ i j : block.Index,
    Nonempty (NativeGK5CGConservativeFiveCell first last
      (block.raw i) (block.raw j))) ∧
  (∃ i : block.Index, ∃ path : Quiver.Path u v,
    Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k path) (block.raw i)))

/-- Actual TYPE of a source path realizing EVERY original P77
patch quotient class in one block. The proof remains a PROP in
the dependent subtype, while the source path is a real Type value. -/
abbrev FivefoldP77RawPatchBlockWitness
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :=
  {path : Quiver.Path u v //
    ∀ i : block.Index,
      (fivefoldP77ConservativeFunctor f g h k).map path =
        fivefoldP77ConservativeClass f g h k (block.raw i)}

/-- Blockwise local Type-valued descent if and only if the
proof-bearing original source path subtype is inhabited. -/
theorem fivefoldP77RawPatchBlock_witness_iff
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    Nonempty (FivefoldP77RawPatchBlockWitness f g h k block) ↔
      fivefoldP77RawPatchBlockCompatible f g h k block := by
  letI : Nonempty block.Index := block.nonempty
  constructor
  · rintro ⟨⟨path, hpath⟩⟩
    exact (fivefoldP77LocalTypeDescent_iff f g h k block.raw).1
      ⟨path, hpath⟩
  · intro hlocal
    obtain ⟨path, hpath⟩ :=
      (fivefoldP77LocalTypeDescent_iff f g h k block.raw).2 hlocal
    exact ⟨⟨path, hpath⟩⟩

/-- Original P77 faithfulness reflects equality of genuine typed
source paths. Thus a block has AT MOST ONE source path witness. -/
theorem fivefoldP77RawPatchBlock_witness_subsingleton
    {u v : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v) :
    Subsingleton (FivefoldP77RawPatchBlockWitness f g h k block) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  intro a b
  apply Subtype.ext
  let i₀ : block.Index := Classical.choice block.nonempty
  apply (fivefoldP77ConservativeFunctor_faithful_genuine
    f g h k).map_injective
  exact (a.property i₀).trans (b.property i₀).symm

/-- Arbitrary FINITE typed chains of original F55/P77 raw patch
families. Unlike a list of integers, dependent intermediate source
and target vertices are kept by each constructor. -/
inductive FivefoldP77RawPatchChain
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    FivefoldPathVertex → FivefoldPathVertex →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil (u : FivefoldPathVertex) :
      FivefoldP77RawPatchChain f g h k u u
  | cons {u v w : FivefoldPathVertex}
      (block : FivefoldP77RawPatchBlock f g h k u v)
      (tail : FivefoldP77RawPatchChain f g h k v w) :
      FivefoldP77RawPatchChain f g h k u w

/-- Exactly the conjunction of actual Type-valued block
certificates, recursively over all dependent source endpoints. -/
def fivefoldP77RawPatchChainCompatible
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) : Prop :=
  match chain with
  | .nil _ => True
  | .cons block tail =>
      fivefoldP77RawPatchBlockCompatible f g h k block ∧
        fivefoldP77RawPatchChainCompatible f g h k tail

/-- TYPE of genuine segmentwise typed source paths for an
arbitrary finite original patch chain. Retains every local
quotient-class evaluation and original typed intermediate boundary. -/
def FivefoldP77RawPatchChainWitness
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) : Type :=
  match chain with
  | .nil _ => PUnit
  | .cons block tail =>
      FivefoldP77RawPatchBlockWitness f g h k block ×
        FivefoldP77RawPatchChainWitness f g h k tail

/-- FINITE-CHAIN DESCENT IFF: full original Type-valued
compatibility at EVERY segment is equivalent to existence of a
genuine dependent TYPE of source-path witnesses. -/
theorem fivefoldP77RawPatchChain_witness_iff
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    Nonempty (FivefoldP77RawPatchChainWitness f g h k chain) ↔
      fivefoldP77RawPatchChainCompatible f g h k chain := by
  induction chain with
  | nil u =>
      change Nonempty PUnit ↔ True
      constructor
      · intro _
        trivial
      · intro _
        exact ⟨PUnit.unit⟩
  | cons block tail ih =>
      change
        Nonempty (FivefoldP77RawPatchBlockWitness f g h k block ×
          FivefoldP77RawPatchChainWitness f g h k tail) ↔
        (fivefoldP77RawPatchBlockCompatible f g h k block ∧
          fivefoldP77RawPatchChainCompatible f g h k tail)
      constructor
      · rintro ⟨⟨wBlock, wTail⟩⟩
        exact ⟨
          (fivefoldP77RawPatchBlock_witness_iff f g h k block).1
            ⟨wBlock⟩,
          ih.mp ⟨wTail⟩⟩
      · rintro ⟨hBlock, hTail⟩
        obtain ⟨wBlock⟩ :=
          (fivefoldP77RawPatchBlock_witness_iff f g h k block).2 hBlock
        obtain ⟨wTail⟩ := ih.mpr hTail
        exact ⟨(wBlock, wTail)⟩

/-- FINITE-CHAIN uniqueness: genuine original F55/P77 Type-valued
certificates determine EACH segment path uniquely by original
faithfulness; hence the whole dependent path witness is subsingleton. -/
theorem fivefoldP77RawPatchChain_witness_subsingleton
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    Subsingleton (FivefoldP77RawPatchChainWitness f g h k chain) := by
  induction chain with
  | nil u =>
      change Subsingleton PUnit
      infer_instance
  | cons block tail ih =>
      change Subsingleton
        (FivefoldP77RawPatchBlockWitness f g h k block ×
          FivefoldP77RawPatchChainWitness f g h k tail)
      letI : Subsingleton (FivefoldP77RawPatchBlockWitness f g h k block) :=
        fivefoldP77RawPatchBlock_witness_subsingleton f g h k block
      letI : Subsingleton (FivefoldP77RawPatchChainWitness f g h k tail) := ih
      infer_instance

/-- Every compatible finite raw patch chain has EXACTLY ONE
Type-valued family of original typed source path witnesses.
This is not mere uniqueness of their signed charges. -/
theorem fivefoldP77RawPatchChain_witness_unique
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (hcompatible : fivefoldP77RawPatchChainCompatible f g h k chain) :
    ∃! witness : FivefoldP77RawPatchChainWitness f g h k chain,
      True := by
  have hex : Nonempty (FivefoldP77RawPatchChainWitness f g h k chain) :=
    (fivefoldP77RawPatchChain_witness_iff f g h k chain).2 hcompatible
  letI : Subsingleton (FivefoldP77RawPatchChainWitness f g h k chain) :=
    fivefoldP77RawPatchChain_witness_subsingleton f g h k chain
  refine ⟨Classical.choice hex, trivial, ?_⟩
  intro other _
  exact Subsingleton.elim other (Classical.choice hex)

/-- Concatenate the genuine typed source paths from all
original P77 patch blocks in their dependency-preserving order. -/
def fivefoldP77RawPatchChainPath
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    FivefoldP77RawPatchChainWitness f g h k chain →
      Quiver.Path u v := by
  induction chain with
  | nil vertex =>
      intro _
      exact Quiver.Path.nil
  | cons block tail ih =>
      intro witness
      exact witness.1.val.comp (ih witness.2)

/-- Evaluate an arbitrary finite source patch chain in the
ORIGINAL P77 conservative quotient, composing original raw
four-proof classes in dependent boundary order. The chosen local
patch indices only pick genuine raw representatives; compatibility
will prove the value is the source image. -/
def fivefoldP77RawPatchChainTarget
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
      FivefoldP77ConservativeClasses f g h k u v :=
  match chain with
  | .nil vertex =>
      fivefoldP77ConservativeClass f g h k
        (.refl (fivefoldF55OriginalAt f g h k vertex.phase))
  | .cons block tail =>
      fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeClass f g h k
          (block.raw (Classical.choice block.nonempty)))
        (fivefoldP77RawPatchChainTarget f g h k tail)

/-- ARBITRARY FINITE COMPOSITION COHERENCE: evaluation of the
concatenated GENUINE source finite path is EXACTLY the iterated
vertical composition of original P77 quotient four-proof patches. -/
theorem fivefoldP77RawPatchChainPath_eval
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v) :
    ∀ witness : FivefoldP77RawPatchChainWitness f g h k chain,
      (fivefoldP77ConservativeFunctor f g h k).map
          (fivefoldP77RawPatchChainPath f g h k chain witness) =
        fivefoldP77RawPatchChainTarget f g h k chain := by
  letI := fivefoldP77ConservativeCategory f g h k
  induction chain with
  | nil vertex =>
      intro _
      change
        (fivefoldP77ConservativeFunctor f g h k).map
          (Quiver.Path.nil : Quiver.Path vertex vertex) =
          fivefoldP77ConservativeClass f g h k
            (.refl (fivefoldF55OriginalAt f g h k vertex.phase))
      exact (fivefoldP77ConservativeFunctor f g h k).map_id vertex
  | cons block tail ih =>
      intro witness
      rcases witness with ⟨head, rest⟩
      let i₀ : block.Index := Classical.choice block.nonempty
      change
        (fivefoldP77ConservativeFunctor f g h k).map
          (head.val.comp (fivefoldP77RawPatchChainPath f g h k tail rest)) =
        fivefoldP77ConservativeCompose f g h k
          (fivefoldP77ConservativeClass f g h k (block.raw i₀))
          (fivefoldP77RawPatchChainTarget f g h k tail)
      calc
        (fivefoldP77ConservativeFunctor f g h k).map
            (head.val.comp
              (fivefoldP77RawPatchChainPath f g h k tail rest)) =
          (fivefoldP77ConservativeFunctor f g h k).map head.val ≫
            (fivefoldP77ConservativeFunctor f g h k).map
              (fivefoldP77RawPatchChainPath f g h k tail rest) :=
          (fivefoldP77ConservativeFunctor f g h k).map_comp _ _
        _ = fivefoldP77ConservativeCompose f g h k
              (fivefoldP77ConservativeClass f g h k (block.raw i₀))
              (fivefoldP77RawPatchChainTarget f g h k tail) := by
          rw [head.property i₀, ih rest]
          rfl

/-- Actual original P77 conservative quotient class together
with proof of a genuinely typed source preimage for the WHOLE
finite chain, never a charge-defined synthetic class. -/
def fivefoldP77RawPatchChainCertified
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    FivefoldP77PartialDomain f g h k u v := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageFactor f g h k).map
    (fivefoldP77RawPatchChainPath f g h k chain witness)

/-- True source-certified original target composite has EXACT
original F55/P77 Type-valued quotient value of the full raw chain. -/
theorem fivefoldP77RawPatchChainCertified_val
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    (fivefoldP77RawPatchChainCertified f g h k chain witness).val =
      fivefoldP77RawPatchChainTarget f g h k chain := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  change
    (fivefoldP77ConservativeFunctor f g h k).map
        (fivefoldP77RawPatchChainPath f g h k chain witness) =
      fivefoldP77RawPatchChainTarget f g h k chain
  exact fivefoldP77RawPatchChainPath_eval f g h k chain witness

/-- Exact v4.62 partial recovery of the ENTIRE genuine finite
path chain returns its actual typed source concatenation. -/
theorem fivefoldP77RawPatchChainCertified_recover
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77RawPatchChainCertified f g h k chain witness) =
      fivefoldP77RawPatchChainPath f g h k chain witness := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  change fivefoldP77PartialRecoverPath f g h k
    ((fivefoldP77ImageFactor f g h k).map
      (fivefoldP77RawPatchChainPath f g h k chain witness)) =
      fivefoldP77RawPatchChainPath f g h k chain witness
  exact fivefoldP77PartialRecoverPath_of_factor f g h k
    (fivefoldP77RawPatchChainPath f g h k chain witness)

/-- Original P77 associator charge is the length of the
RECOVERED typed free source path only after genuine finite-chain
Type-valued descent. It is not an image-membership test. -/
theorem fivefoldP77RawPatchChainCertified_charge_length
    {u v : FivefoldPathVertex}
    (chain : FivefoldP77RawPatchChain f g h k u v)
    (witness : FivefoldP77RawPatchChainWitness f g h k chain) :
    fivefoldP77ConservativeCharge f g h k
        (fivefoldP77RawPatchChainCertified f g h k chain witness).val =
      ((fivefoldP77RawPatchChainPath f g h k chain witness).length : ℤ) := by
  calc
    fivefoldP77ConservativeCharge f g h k
        (fivefoldP77RawPatchChainCertified f g h k chain witness).val =
      ((fivefoldP77PartialRecoverPath f g h k
          (fivefoldP77RawPatchChainCertified f g h k chain witness)).length : ℤ) :=
        fivefoldP77PartialRecoverPath_charge_length f g h k _
    _ = ((fivefoldP77RawPatchChainPath f g h k chain witness).length : ℤ) := by
      rw [fivefoldP77RawPatchChainCertified_recover]

/-- Failure of one genuinely typed segment's source certificate
blocks a full segmentwise realization of the WHOLE finite chain.
No assertion that a different global P77 target factorization
is impossible follows from this. -/
theorem fivefoldP77RawPatchChain_cons_typeGap
    {u v w : FivefoldPathVertex}
    (block : FivefoldP77RawPatchBlock f g h k u v)
    (tail : FivefoldP77RawPatchChain f g h k v w)
    (hno : ¬ fivefoldP77RawPatchBlockCompatible f g h k block) :
    ¬ Nonempty
        (FivefoldP77RawPatchChainWitness f g h k
          (.cons block tail)) := by
  intro hw
  have hcompat :=
    (fivefoldP77RawPatchChain_witness_iff f g h k
      (.cons block tail)).1 hw
  exact hno hcompat.1

#print axioms FivefoldP77RawPatchBlock
#print axioms fivefoldP77RawPatchBlockCompatible
#print axioms FivefoldP77RawPatchBlockWitness
#print axioms fivefoldP77RawPatchBlock_witness_iff
#print axioms fivefoldP77RawPatchBlock_witness_subsingleton
#print axioms FivefoldP77RawPatchChain
#print axioms fivefoldP77RawPatchChainCompatible
#print axioms FivefoldP77RawPatchChainWitness
#print axioms fivefoldP77RawPatchChain_witness_iff
#print axioms fivefoldP77RawPatchChain_witness_subsingleton
#print axioms fivefoldP77RawPatchChain_witness_unique
#print axioms fivefoldP77RawPatchChainPath
#print axioms fivefoldP77RawPatchChainTarget
#print axioms fivefoldP77RawPatchChainPath_eval
#print axioms fivefoldP77RawPatchChainCertified
#print axioms fivefoldP77RawPatchChainCertified_val
#print axioms fivefoldP77RawPatchChainCertified_recover
#print axioms fivefoldP77RawPatchChainCertified_charge_length
#print axioms fivefoldP77RawPatchChain_cons_typeGap

end
end KUOS.Architecture.WuxingPentagonUnified
