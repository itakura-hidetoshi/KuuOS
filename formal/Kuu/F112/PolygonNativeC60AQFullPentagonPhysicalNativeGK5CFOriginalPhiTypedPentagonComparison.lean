import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CEFourSegmentPentagonCRT
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFDoubleInversionWeightObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5CF — TRUE ORIGINAL F55 SOURCE PENTAGON AND THE
BOUNDARY BETWEEN GK5CE STRICT RINGHOM EQUALITY AND P94A HIGHER SEAMS.

GK5CE establishes the genuine five-parenthesization pentagon for
heterogeneous MvPolynomial Int RingHoms, including the entire noncoprime
finite CRT descent. This independent theorem adds the SECOND, proof-relevant
presentation: five ACTUAL differently parenthesized four-part original F55
Type-valued source 3-cells, with five ACTUAL P77 four-cell edges built from
original associativity and left/right whiskering.

The two actual source pentagon routes give two parallel raw P77 four-cell
certificates and two parallel P94A FOUR-cell certificates after the existing
seven historical inclusions. These are witnesses, NOT an equality of
four-cell proofs, a five-cell pentagonator, a new P92B associator,
or an unconditional original-to-recursive-phi seam.

Direct original→phi seam EXISTENCE transports around the entire original
P77 pentagon by GK5BC, so a chosen local seed glues all five original
parenthesizations. This necessary local Type-valued seed cannot be inferred
from any numerical RingHom pentagon: the genuine same-F54-Hom north
primitive is locally seam-positive but its original DOUBLE INVERSE
is seam-negative, despite passing BOTH old unsigned/signed source gates.
The GK5BF inverse-depth weight is an actual higher obstruction.
The universal GK5AY seam is already impossible by GK5BB.

Strict 空, independent Kuu→Qi; original F54 two-Nat/two-category/Blocks
and F55 source Type proofs intact. No numerical CRT equality is converted
into a source/phi structural seam. Root107, pinned Lean v4.30.0-rc2 and
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected #1558 remains Draft/open/unmerged. Append-only; no
sorry, admit, axiom, native_decide, Gray, or GK5BA shell kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE
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

/-- Genuine original F55 three-cell (((f·g)·h)·k). -/
def nativeGK5CFOriginalLeftLeftLeft
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  .trans (.trans (.trans f g) h) k

/-- Genuine original F55 three-cell ((f·(g·h))·k). -/
def nativeGK5CFOriginalLeftMiddle
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  .trans (.trans f (.trans g h)) k

/-- Genuine original F55 three-cell ((f·g)·(h·k)). -/
def nativeGK5CFOriginalMiddle
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  .trans (.trans f g) (.trans h k)

/-- Genuine original F55 three-cell (f·((g·h)·k)). -/
def nativeGK5CFOriginalRightMiddle
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  .trans f (.trans (.trans g h) k)

/-- Genuine original F55 three-cell (f·(g·(h·k))). -/
def nativeGK5CFOriginalRightRight
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  .trans f (.trans g (.trans h k))

/-- Original P77 4-cell: LLL → LM, true right whiskering of assoc(f,g,h). -/
def nativeGK5CFP77Edge01
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftLeftLeft f g h k)
      (nativeGK5CFOriginalLeftMiddle f g h k) :=
  .rightWhisker (.assoc f g h) k

/-- Original P77 4-cell: LM → RM, genuine original assoc(f,g·h,k). -/
def nativeGK5CFP77Edge12
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftMiddle f g h k)
      (nativeGK5CFOriginalRightMiddle f g h k) :=
  .assoc f (.trans g h) k

/-- Original P77 4-cell: RM → RR, true left whiskering of assoc(g,h,k). -/
def nativeGK5CFP77Edge23
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalRightMiddle f g h k)
      (nativeGK5CFOriginalRightRight f g h k) :=
  .leftWhisker f (.assoc g h k)

/-- Original P77 4-cell: RR → M, true inverse of assoc(f,g,h·k). -/
def nativeGK5CFP77Edge34
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalRightRight f g h k)
      (nativeGK5CFOriginalMiddle f g h k) :=
  .symm (.assoc f g (.trans h k))

/-- Original P77 4-cell: M → LLL, true inverse assoc(f·g,h,k). -/
def nativeGK5CFP77Edge40
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalMiddle f g h k)
      (nativeGK5CFOriginalLeftLeftLeft f g h k) :=
  .symm (.assoc (.trans f g) h k)

/-- The length-three route of genuine source 4-proofs, LLL→LM→RM→RR. -/
def nativeGK5CFP77UpperPath
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftLeftLeft f g h k)
      (nativeGK5CFOriginalRightRight f g h k) :=
  .trans (.trans (nativeGK5CFP77Edge01 f g h k)
    (nativeGK5CFP77Edge12 f g h k))
    (nativeGK5CFP77Edge23 f g h k)

/-- The length-two source 4-proof route LLL→M→RR: a second genuine
P77 certificate at exactly the same dependent source and target.
No 5-cell equality between the two route proofs is asserted. -/
def nativeGK5CFP77LowerPath
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftLeftLeft f g h k)
      (nativeGK5CFOriginalRightRight f g h k) :=
  .trans (.symm (nativeGK5CFP77Edge40 f g h k))
    (.symm (nativeGK5CFP77Edge34 f g h k))

/-- Genuine, distinct P77-proof presentations both map into the
existing P94A Type-valued FOUR-cell language with RAW original
F55 wrappers. This is not a seam from raw to recursive phi. -/
def nativeGK5CFUpperRawP94
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalLeftLeftLeft f g h k))
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalRightRight f g h k)) :=
  nativeGK5BCP77_to_rawP94 (nativeGK5CFP77UpperPath f g h k)

/-- The second genuine P94A RAW four-cell witnesses the lower
pentagon route at the same original endpoints, without equation
between the two higher proof terms. -/
def nativeGK5CFLowerRawP94
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalLeftLeftLeft f g h k))
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalRightRight f g h k)) :=
  nativeGK5BCP77_to_rawP94 (nativeGK5CFP77LowerPath f g h k)

/-- All five ACTUAL original source 4-cell edges exist for every
composable F55 four-tuple; no extra four-cell hypotheses. -/
theorem nativeGK5CFOriginalFiveEdges_exist
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    Nonempty (NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftLeftLeft f g h k)
      (nativeGK5CFOriginalLeftMiddle f g h k)) ∧
    Nonempty (NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalLeftMiddle f g h k)
      (nativeGK5CFOriginalRightMiddle f g h k)) ∧
    Nonempty (NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalRightMiddle f g h k)
      (nativeGK5CFOriginalRightRight f g h k)) ∧
    Nonempty (NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalRightRight f g h k)
      (nativeGK5CFOriginalMiddle f g h k)) ∧
    Nonempty (NativeF55RawVerticalFourCell first last
      (nativeGK5CFOriginalMiddle f g h k)
      (nativeGK5CFOriginalLeftLeftLeft f g h k)) :=
  ⟨⟨nativeGK5CFP77Edge01 f g h k⟩,
   ⟨nativeGK5CFP77Edge12 f g h k⟩,
   ⟨nativeGK5CFP77Edge23 f g h k⟩,
   ⟨nativeGK5CFP77Edge34 f g h k⟩,
   ⟨nativeGK5CFP77Edge40 f g h k⟩⟩

/-- The five TRUE original P77 four-proofs induce the five
bidirectional local ORIGINAL→PHI P94A seam-existence transports.
This is a Prop-level descent statement derived from Type values,
not equality of the actual selected 4-cell proof terms. -/
theorem nativeGK5CFOriginalSeamPentagon_cycle
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftLeftLeft f g h k)) ↔
      Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftMiddle f g h k))) ∧
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftMiddle f g h k)) ↔
      Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightMiddle f g h k))) ∧
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightMiddle f g h k)) ↔
      Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightRight f g h k))) ∧
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightRight f g h k)) ↔
      Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalMiddle f g h k))) ∧
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalMiddle f g h k)) ↔
      Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftLeftLeft f g h k))) :=
  ⟨nativeGK5BCSeam_nonempty_iff_P77 (nativeGK5CFP77Edge01 f g h k),
   nativeGK5BCSeam_nonempty_iff_P77 (nativeGK5CFP77Edge12 f g h k),
   nativeGK5BCSeam_nonempty_iff_P77 (nativeGK5CFP77Edge23 f g h k),
   nativeGK5BCSeam_nonempty_iff_P77 (nativeGK5CFP77Edge34 f g h k),
   nativeGK5BCSeam_nonempty_iff_P77 (nativeGK5CFP77Edge40 f g h k)⟩

/-- Exact local-to-all-five original source pentagon descent:
the extra original→phi bridge at ONE original F55 3-proof
is necessary and sufficient for seam existence at EVERY vertex.
No numerical RingHom equality is used in this proof. -/
theorem nativeGK5CFOriginalSeamPentagon_glue_iff
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftLeftLeft f g h k)) ↔
    (Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalLeftMiddle f g h k)) ∧
     Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightMiddle f g h k)) ∧
     Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalRightRight f g h k)) ∧
     Nonempty (nativeGK5AZSeamAt (nativeGK5CFOriginalMiddle f g h k))) := by
  have h01 := nativeGK5BCSeam_nonempty_iff_P77
    (nativeGK5CFP77Edge01 f g h k)
  have h12 := nativeGK5BCSeam_nonempty_iff_P77
    (nativeGK5CFP77Edge12 f g h k)
  have h23 := nativeGK5BCSeam_nonempty_iff_P77
    (nativeGK5CFP77Edge23 f g h k)
  have h34 := nativeGK5BCSeam_nonempty_iff_P77
    (nativeGK5CFP77Edge34 f g h k)
  constructor
  · intro seed
    have h1 := h01.mp seed
    have h2 := h12.mp h1
    have h3 := h23.mp h2
    exact ⟨h1, h2, h3, h34.mp h3⟩
  · intro all
    exact h01.mpr all.1

/-- The PRECISE additional gate for comparing a true heterogeneous
GK5CE RingHom pentagon to a chosen actual original F55 source: a
P94A four-cell between its raw wrapper and recursive structural phi.
The gate never treats numerical equality as this higher witness. -/
def nativeGK5CFPentagonHigherComparison
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (src : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) : Prop :=
  nativeGK5CEFourPentagon_boundary steps start a b c d ∧
  Nonempty (nativeGK5AZSeamAt src)

/-- Sharp conditional descent: since the numerical RingHom
pentagon is proved for ALL actual typed polynomial chains,
a joint comparison exists EXACTLY when the independent original
F55 Type-valued local seam exists. -/
theorem nativeGK5CFPentagonHigherComparison_iff
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (src : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5CFPentagonHigherComparison steps start a b c d src ↔
      Nonempty (nativeGK5AZSeamAt src) := by
  constructor
  · intro h
    exact h.2
  · intro h
    exact ⟨nativeGK5CEFourPentagon_boundary steps start a b c d, h⟩

/-- Genuine SAME-F54-HOM north original pentagon primitive:
numerical RingHom pentagon and the real reflexive P94A local seam
coexist, for ALL variable types, substitutions and segment lengths. -/
theorem nativeGK5CFNorthPrimitiveComparison_positive
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CFPentagonHigherComparison steps start a b c d
      nativeGK5AGNorthOriginalCell :=
  ⟨nativeGK5CEFourPentagon_boundary steps start a b c d,
   ⟨NativeF55P94UnitFourCell.refl _⟩⟩

/-- The TRUE SAME-F54-HOM north DOUBLE INVERSE original source
has NO direct raw→structural-phi four-cell even when ALL five
heterogeneous polynomial RingHoms are equal: N=S=1 is inadequate
and the original inversion-depth invariant obstructs the lift. -/
theorem nativeGK5CFNorthDoubleInverseComparison_no
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    ¬ nativeGK5CFPentagonHigherComparison steps start a b c d
      nativeGK5BFNorthDoubleInverse := by
  intro h
  exact nativeGK5BFNorthDoubleInverse_no_seam h.2

/-- Explicit no-go for any unconditional reconstruction rule
RingHom pentagon equality → a source-typed P94A original→phi seam,
using the existing actual north double-inverse obstruction. -/
theorem nativeGK5CFNoNumericalPentagonToSourceSeam
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    ¬ (nativeGK5CEFourPentagon_boundary steps start a b c d →
      Nonempty (nativeGK5AZSeamAt nativeGK5BFNorthDoubleInverse)) := by
  intro lift
  exact nativeGK5BFNorthDoubleInverse_no_seam
    (lift (nativeGK5CEFourPentagon_boundary steps start a b c d))

/-- An explicit original north same-fiber counterexample: both
original source classes satisfy the established unsigned/signed
necessary gates, the same arbitrary GK5CE numerical RingHom
pentagon remains true, but exactly the primitive source lifts.
Thus a numerical CRT pentagon, even together with N=S=1,
does not determine structural original→phi descent. -/
theorem nativeGK5CFNorthNumericGate_sameFiber_split
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat) :
    nativeGK5CEFourPentagon_boundary steps start a b c d ∧
    nativeGK5BFCountSignedGate nativeGK5AGNorthOriginalCell ∧
    nativeGK5BFCountSignedGate nativeGK5BFNorthDoubleInverse ∧
    nativeGK5CFPentagonHigherComparison steps start a b c d
      nativeGK5AGNorthOriginalCell ∧
    ¬ nativeGK5CFPentagonHigherComparison steps start a b c d
      nativeGK5BFNorthDoubleInverse := by
  obtain ⟨hN₁, hS₁, _, hN₂, hS₂, _⟩ :=
    nativeGK5BFNorthSameFiber_joint_gate_not_sufficient
  exact ⟨nativeGK5CEFourPentagon_boundary steps start a b c d,
    ⟨hN₁, hS₁⟩, ⟨hN₂, hS₂⟩,
    nativeGK5CFNorthPrimitiveComparison_positive steps start a b c d,
    nativeGK5CFNorthDoubleInverseComparison_no steps start a b c d⟩

#print axioms nativeGK5CFOriginalLeftLeftLeft
#print axioms nativeGK5CFOriginalLeftMiddle
#print axioms nativeGK5CFOriginalMiddle
#print axioms nativeGK5CFOriginalRightMiddle
#print axioms nativeGK5CFOriginalRightRight
#print axioms nativeGK5CFP77Edge01
#print axioms nativeGK5CFP77Edge12
#print axioms nativeGK5CFP77Edge23
#print axioms nativeGK5CFP77Edge34
#print axioms nativeGK5CFP77Edge40
#print axioms nativeGK5CFP77UpperPath
#print axioms nativeGK5CFP77LowerPath
#print axioms nativeGK5CFUpperRawP94
#print axioms nativeGK5CFLowerRawP94
#print axioms nativeGK5CFOriginalFiveEdges_exist
#print axioms nativeGK5CFOriginalSeamPentagon_cycle
#print axioms nativeGK5CFOriginalSeamPentagon_glue_iff
#print axioms nativeGK5CFPentagonHigherComparison
#print axioms nativeGK5CFPentagonHigherComparison_iff
#print axioms nativeGK5CFNorthPrimitiveComparison_positive
#print axioms nativeGK5CFNorthDoubleInverseComparison_no
#print axioms nativeGK5CFNoNumericalPentagonToSourceSeam
#print axioms nativeGK5CFNorthNumericGate_sameFiber_split

end
end Kuu.F112.Physical
