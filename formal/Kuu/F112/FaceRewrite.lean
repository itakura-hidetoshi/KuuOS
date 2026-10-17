import Kuu.F112.Overlap

/-!
# F112-A / independent proof-relevant physical face reductions

This is a NEW, boundary-typed, Type-valued presentation of actual C60
vertex-edge-polygon triangular reductions. A face generator replaces the
two genuine raw F69 incidence legs by their original direct diagonal.
Whiskering, inverse and vertical pasting are *proof terms*, not equations.

Their soundness is proved into the exact Kuu incidence-localization kernel,
rather than postulated by a Gray, charge or phase evaluator. The unquotiented
raw two-leg and diagonal paths remain provably distinct. This is a
physically grounded first higher-source layer; it is not the old F42
polygon-loop grammar or a finished original F54/F55 proof 3-category.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false

/-- Genuine Type-valued face-pasting witnesses between *parallel* raw
physical zigzags. Endpoint and compositional compatibility are enforced by
dependent indices, not checked by an observation/grade after construction. -/
inductive FaceRewrite :
    {s t : Site} → Zigzag s t → Zigzag s t → Type where
  | ident {s t : Site} (p : Zigzag s t) : FaceRewrite p p
  | physicalFlag (e : Edge) (i j : Bool) :
      FaceRewrite (flagRawTwoStep e i j) (flagRawDiagonal e i j)
  | inverse {s t : Site} {p q : Zigzag s t}
      (c : FaceRewrite p q) : FaceRewrite q p
  | vertical {s t : Site} {p q r : Zigzag s t}
      (c : FaceRewrite p q) (d : FaceRewrite q r) : FaceRewrite p r
  | leftContext {r s t : Site} (h : Zigzag r s)
      {p q : Zigzag s t} (c : FaceRewrite p q) :
      FaceRewrite (append h p) (append h q)
  | rightContext {r s t : Site}
      {p q : Zigzag r s} (c : FaceRewrite p q) (h : Zigzag s t) :
      FaceRewrite (append p h) (append q h)

/-- Every freely presented face reduction has a *proved* interpretation in
the genuine F69 localization, with both original endpoint sites fixed.
None of the higher-source rewrite constructors is silently identified. -/
theorem FaceRewrite.localized_sound
    {s t : Site} {p q : Zigzag s t} (c : FaceRewrite p q) :
    zigzagToLocalization p = zigzagToLocalization q := by
  induction c with
  | ident p => rfl
  | physicalFlag e i j => exact physicalFlagTwoStep_localized e i j
  | inverse c ih => exact ih.symm
  | vertical c d ihc ihd => exact ihc.trans ihd
  | leftContext h c ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => zigzagToLocalization h ≫ x) ih
  | rightContext c h ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => x ≫ zigzagToLocalization h) ih

/-- Source 2-cell reductions are sound even after the *exact*, previously
proved localization-kernel quotient, not just after a chosen evaluator. -/
theorem FaceRewrite.kernel_sound
    {s t : Site} {p q : Zigzag s t} (c : FaceRewrite p q) :
    zigzagKernelQ.map p = zigzagKernelQ.map q :=
  (zigzagKernel_exact p q).2 c.localized_sound

/-- Each of the 360 actual C60 endpoint/edge/face flags is a primitive,
correctly typed proof-relevant source face reduction. -/
def flagFaceRewrite (e : Edge) (i j : Bool) :
    FaceRewrite (flagRawTwoStep e i j) (flagRawDiagonal e i j) :=
  .physicalFlag e i j

/-- A different, nontrivial proof tree over precisely the same original
physical source/target. No proof irrelevance is imposed on the raw syntax. -/
def flagFaceRewriteWithUnit (e : Edge) (i j : Bool) :
    FaceRewrite (flagRawTwoStep e i j) (flagRawDiagonal e i j) :=
  .vertical (.ident (flagRawTwoStep e i j)) (.physicalFlag e i j)

/-- Proof relevance is REAL: adding a source identity before the genuine
physical face reduction changes the raw witness, despite equal endpoints. -/
theorem flagFaceRewrite_ne_withUnit (e : Edge) (i j : Bool) :
    flagFaceRewrite e i j ≠ flagFaceRewriteWithUnit e i j := by
  intro h
  cases h

/-- The primitive C60 physical rewrite is NOT an equality of raw paths;
the two different source expressions survive outside their *explicit* kernel. -/
theorem flagFaceRewrite_raw_paths_distinct (e : Edge) (i j : Bool) :
    flagRawTwoStep e i j ≠ flagRawDiagonal e i j :=
  flagRawTwoStep_ne_diagonal e i j

/-- A concrete NEW 2-cell anchored at the actual north C60 pentagon,
using an original around-vertex edge and its real polygon site. -/
def northPentagonFlagRewrite :
    FaceRewrite
      (flagRawTwoStep (.around ⟨.north, .s0⟩) false false)
      (flagRawDiagonal (.around ⟨.north, .s0⟩) false false) :=
  .physicalFlag (.around ⟨.north, .s0⟩) false false

theorem northPentagonFlagRewrite_kernel :
    zigzagKernelQ.map
      (flagRawTwoStep (.around ⟨.north, .s0⟩) false false) =
    zigzagKernelQ.map
      (flagRawDiagonal (.around ⟨.north, .s0⟩) false false) :=
  northPentagonFlagRewrite.kernel_sound

#print axioms FaceRewrite.localized_sound
#print axioms FaceRewrite.kernel_sound
#print axioms flagFaceRewrite_ne_withUnit
#print axioms flagFaceRewrite_raw_paths_distinct
#print axioms northPentagonFlagRewrite_kernel
end Kuu.F112.Physical
