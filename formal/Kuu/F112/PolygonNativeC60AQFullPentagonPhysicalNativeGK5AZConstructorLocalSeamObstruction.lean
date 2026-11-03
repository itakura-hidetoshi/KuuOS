import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AYOriginalStructuralPhiSeamGate
import Mathlib.Tactic

/-!
F112-P94D3GK5AZ — constructor-local, truly Type-valued seams from
raw P92B.original(F55) to GK5AI recursive structural phi.

The two source atoms pentagon/disjointSquare have unconditional
reflexive seams. For ident/symm/trans/context constructors the
raw whole-wrapper is NOT definitionally the recursive phi shape.
This file exposes the exact LOCAL higher-cell shell or inversion
compatibility that is needed, instead of assuming a universal seam.

A trans shell plus two child bridges yields a genuine seam by the
existing selected right/left whiskering operations. The four F45/F54
context shells similarly compose with existing chosen congruences.
For inversion P94A contains four-cell inversion but NO general
operation applying inversion to the endpoints of arbitrary four-cells;
two explicit local higher certificates are therefore kept distinct.

Given only two endpoint bridges, any actual raw P93C comparison is
transported to recursive phi endpoints; and any selected phi
comparison can be transported back to raw endpoints. GK5AX's
three source-indexed vertical primitives thereby admit raw P94A
comparisons ONLY when the corresponding local endpoint bridges
are supplied. Original P89 witnesses are not constructed.

GK5AW's eight original context-source reflection localization
lemmas remain independent: a supplied raw P93C witness with two
local endpoint bridges suffices to activate the left/right
whisker localization. No global seam, no universal normalized
P94A source proof, no unconditional nonfaithfulness is claimed.

Strict 空 / independent Kuu to Qi, same root107; original F54
two-Nat/two-category/Blocks history kept, #1558 Draft/open.
Lean 4.30.0-rc2 / pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; no Gray, sorry/admit/native_decide/new axioms.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- One genuinely selected, source-typed endpoint bridge.
It is a Type of 4-proofs, not an assertion of unconditional existence. -/
abbrev nativeGK5AZSeamAt
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :=
  NativeF55P94UnitFourCell
    (NativeF55P92AssocComparison.original f)
    (nativeGK5AIOriginalToP92Structural f)

/-- Real north C60 pentagon atom: original and recursive phi are
DEFINITIONALLY the same selected 3-proof for this source atom. -/
def nativeGK5AZNorthPentagonAtom :
    nativeGK5AZSeamAt northNativeF55PentagonCell :=
  .refl _

/-- Real north physical hexagon disjoint-square atom has the
same unconditional definitional seam, with its own original source. -/
def nativeGK5AZNorthDisjointSquareAtom :
    nativeGK5AZSeamAt northHexagonNativeF55SquareCell :=
  .refl _

/-- Inversion is different from inverting a 4-cell. To construct
the raw symmetric F55 seam one needs (1) a raw-unwrapping shell,
and (2) a 4-cell respecting inversion at the P92B 3-proof level.
Neither existence is silently inferred from the inner seam. -/
def nativeGK5AZSymm_of_two_gates
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.symm f))
      (.symm (NativeF55P92AssocComparison.original f)))
    (respect : NativeF55P94UnitFourCell
      (.symm (NativeF55P92AssocComparison.original f))
      (.symm (nativeGK5AIOriginalToP92Structural f))) :
    nativeGK5AZSeamAt (.symm f) :=
  .trans unwrap respect

/-- Genuine F55 composition: only the raw WHOLE-composite to
composition-of-raw shell is additional. The two subterm seams
are then glued using existing P94A right/left whiskering. -/
def nativeGK5AZTrans_of_shell
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f g))
      (.trans (NativeF55P92AssocComparison.original f)
        (NativeF55P92AssocComparison.original g)))
    (firstBridge : nativeGK5AZSeamAt f)
    (secondBridge : nativeGK5AZSeamAt g) :
    nativeGK5AZSeamAt (.trans f g) :=
  .trans unwrap
    (.trans
      (.rightWhisker firstBridge
        (NativeF55P92AssocComparison.original g))
      (.leftWhisker (nativeGK5AIOriginalToP92Structural f)
        secondBridge))

/-- Exact trans-shell obstruction. This does NOT claim such an
obstruction is populated at any concrete original F55 cell. -/
def nativeGK5AZTransShellHole
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    Prop :=
  ¬ Nonempty (NativeF55P94UnitFourCell
    (NativeF55P92AssocComparison.original (.trans f g))
    (.trans (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)))

/-- With two true child seams, either the composite has been
constructed as a true 4-cell, or the precise raw-composition
shell is unavailable. This is an exact CONDITIONAL gate, not a
claim that either particular branch actually occurs. -/
theorem nativeGK5AZTrans_seam_or_shellHole
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (hf : Nonempty (nativeGK5AZSeamAt f))
    (hg : Nonempty (nativeGK5AZSeamAt g)) :
    Nonempty (nativeGK5AZSeamAt (.trans f g)) ∨
      nativeGK5AZTransShellHole f g := by
  classical
  by_cases missing : nativeGK5AZTransShellHole f g
  · exact Or.inr missing
  · have shell : Nonempty (NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.trans f g))
        (.trans (NativeF55P92AssocComparison.original f)
          (NativeF55P92AssocComparison.original g))) :=
      Classical.byContradiction missing
    exact Or.inl ⟨nativeGK5AZTrans_of_shell f g
      (Classical.choice shell) (Classical.choice hf) (Classical.choice hg)⟩

/-- Left F45 context: raw wrapper to wrapped-original inner term
is the only new shell; the actual P94A leftContext transports
the child seam inside its genuine binary context. -/
def nativeGK5AZLeftContext_of_shell
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.leftContext f later))
      (.leftContext (NativeF55P92AssocComparison.original f) later))
    (inner : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.leftContext f later) :=
  .trans unwrap (.leftContext inner later)

/-- Right F45 binary context with independently typed original
Blocks and target category context. -/
def nativeGK5AZRightContext_of_shell
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l mc pc ma pa)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.rightContext earlier f))
      (.rightContext earlier (NativeF55P92AssocComparison.original f)))
    (inner : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.rightContext earlier f) :=
  .trans unwrap (.rightContext earlier inner)

/-- Precomposing the ORIGINAL F54 route requires one raw outer
shell. The true selected precompose 4-cell lifts the inner seam. -/
def nativeGK5AZPrecompose_of_shell
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {k l : Nat}
    (before : KuuNativeF45Tree p k l ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p before first)
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.precompose prior f))
      (.precompose prior (NativeF55P92AssocComparison.original f)))
    (inner : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.precompose prior f) :=
  .trans unwrap (.precompose prior inner)

/-- Postcomposition preserves distinct genuine original F54
source/target routes, with a separate local outer shell. -/
def nativeGK5AZPostcompose_of_shell
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {k l : Nat}
    (after : KuuNativeF45Tree p k l ma pa mb pb)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p last after)
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.postcompose f suffix))
      (.postcompose (NativeF55P92AssocComparison.original f) suffix))
    (inner : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.postcompose f suffix) :=
  .trans unwrap (.postcompose inner suffix)

/-- Two LOCAL bridges suffice to transport an ACTUAL raw P93C
four-proof to recursive phi endpoints; a global GK5AY seam
record is NOT a prerequisite for this restricted source slot. -/
def nativeGK5AZRawP93_to_phi
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) :=
  .trans (.trans (.symm bf) (.old raw)) bg

/-- Conversely, two local endpoint bridges lift any actual
selected phi comparison to a true RAW ORIGINAL endpoint 4-cell,
without creating an original P89 comparison. -/
def nativeGK5AZPhi_to_raw
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g) :=
  .trans (.trans bf selected) (.symm bg)

/-- Source-indexed GK5AX selected LEFT VERTICAL UNIT gives a true
raw original endpoint comparison, conditional only on the two
local 4-cell bridges. No original P89 unit is manufactured. -/
def nativeGK5AZRawLeftVerticalUnit
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bComp : nativeGK5AZSeamAt (.trans (.ident r) f))
    (bF : nativeGK5AZSeamAt f) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans (.ident r) f))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5AZPhi_to_raw bComp bF (nativeGK5AXSelectedLeftUnit f)

/-- The analogous actual original endpoint lift of GK5AX right
unit, again not an original P89 four-cell. -/
def nativeGK5AZRawRightVerticalUnit
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bComp : nativeGK5AZSeamAt (.trans f (.ident s)))
    (bF : nativeGK5AZSeamAt f) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f (.ident s)))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5AZPhi_to_raw bComp bF (nativeGK5AXSelectedRightUnit f)

/-- Actual GK5AX selected associativity at three genuine F55
sources, transported to raw P92B.original three-proof endpoints. -/
def nativeGK5AZRawVerticalAssoc
    {r s t z : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t z)
    (bLeft : nativeGK5AZSeamAt (.trans (.trans f g) h))
    (bRight : nativeGK5AZSeamAt (.trans f (.trans g h))) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans (.trans f g) h))
      (NativeF55P92AssocComparison.original (.trans f (.trans g h))) :=
  nativeGK5AZPhi_to_raw bLeft bRight
    (nativeGK5AXSelectedVerticalAssoc f g h)

/-- Source-local GK5AW LEFT WHISKER obstruction transfer needs
only the two actual endpoint seams and a raw P93C comparison.
No universal seam is used to localize a genuine BadPair. -/
theorem nativeGK5AZLeftWhisker_raw_bad_localizes
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair first last
      (.trans prior f) (.trans prior g)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWLeftWhisker_bad_localizes prior
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- Dual right-whisker localization: only a genuine original
suffix, a raw selected comparison, and two local seams are used. -/
theorem nativeGK5AZRightWhisker_raw_bad_localizes
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair first last
      (.trans f suffix) (.trans g suffix)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWRightWhisker_bad_localizes suffix
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- If every individual source endpoint seam has been genuinely
constructed, it can be assembled into the GK5AY dependent
record; this theorem does NOT populate that forall-condition. -/
def nativeGK5AZAssemblePointwise
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (all : ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
      nativeGK5AZSeamAt f) :
    NativeGK5AYOriginalPhiSeam first last :=
  ⟨fun f => all f⟩


/-- Every genuine original pentagon atom, not merely the north
example, has a definitional raw-original to phi bridge. -/
def nativeGK5AZPentagonAtom
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.pentagon
        t₁ t₂ t₃ t₄) :=
  .refl _

/-- Every ORIGINAL disjoint rotation square atom has a real
reflexive seam before P92B quotienting, in all physical sectors. -/
def nativeGK5AZDisjointSquareAtom
    {n₀ m₀ n₁ m₁ : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter :
      KuuNativeF45Tree p n₀ m₀ p₀ q₀ p₁ q₁}
    {rightBefore rightAfter :
      KuuNativeF45Tree p n₁ m₁ p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
        left right) :=
  .refl _

/-- Unlike the two atomic generators, the ORIGINAL F55
identity wrapper and selected P92B refl are not equal as raw
Type-valued inductive proof constructors for ANY original route.
This proves no nonexistence of a connecting higher 4-cell. -/
theorem nativeGK5AZIdent_raw_ne_phi
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (NativeF55P92AssocComparison.original
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)) ≠
      nativeGK5AIOriginalToP92Structural
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route) := by
  intro h
  cases h

/-- The ident constructor has a precise independent raw-to-refl
higher 4-cell gate. It is NOT derivable from raw witness equality:
the latter is refuted by the theorem above. -/
def nativeGK5AZIdent_of_gate
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (rawToRefl : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route))
      (NativeF55P92AssocComparison.refl route)) :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route) :=
  rawToRefl

/-- The selected P94A left-context unit supplies an EXTRA
higher reduction, after the two independent local original
ident and context-shell gates have been explicitly given. -/
def nativeGK5AZLeftContextIdentity_normalize
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route))
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (.leftContext
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)
          later))
      (.leftContext
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route))
        later)) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (.leftContext
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)
          later))
      (NativeF55P92AssocComparison.refl
        (.leftContext route later)) :=
  .trans
    (nativeGK5AZLeftContext_of_shell
      (.ident route) later unwrap identBridge)
    (.leftContextUnit route later)

/-- Dual right-context selected unit, retaining the explicit
original identity seam and outer raw unwrapping gate. -/
def nativeGK5AZRightContextIdentity_normalize
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l mc pc ma pa)
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route))
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (.rightContext earlier
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)))
      (.rightContext earlier
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)))) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (.rightContext earlier
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route)))
      (NativeF55P92AssocComparison.refl
        (.rightContext earlier route)) :=
  .trans
    (nativeGK5AZRightContext_of_shell
      earlier (.ident route) unwrap identBridge)
    (.rightContextUnit earlier route)

/-- Original-context LEFT reflection obstruction localized with
only the two local endpoint seams and one real raw P93C witness.
The context itself does not manufacture a P89 4-cell. -/
theorem nativeGK5AZLeftContext_raw_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext f later) (.leftContext g later)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWLeftContext_bad_localizes later
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- Original-context RIGHT reflection obstruction localized
without a global seam and without identifying independent Blocks. -/
theorem nativeGK5AZRightContext_raw_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l mc pc ma pa)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (.rightContext earlier f) (.rightContext earlier g)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWRightContext_bad_localizes earlier
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- Source-typed F54 precomposition with actual old raw P93C
comparison, local seams and the GK5AW source gate. -/
theorem nativeGK5AZPrecompose_raw_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    (before : KuuNativeF45Tree p k l ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p before first)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair before last
      (.precompose prior f) (.precompose prior g)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWPrecompose_bad_localizes before prior
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- Source-typed F54 postcomposition transfers a parent bad
pair to an actual original subcomparison with only local seams. -/
theorem nativeGK5AZPostcompose_raw_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    (after : KuuNativeF45Tree p k l ma pa mb pb)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p last after)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair first after
      (.postcompose f suffix) (.postcompose g suffix)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWPostcompose_bad_localizes after suffix
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- The genuine original horizontal LEFT context with original
F55 right input also localizes any selected BadPair using only
the two local raw-phi seam endpoints. -/
theorem nativeGK5AZHorizontalLeft_raw_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (other : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (f.horizontal other) (g.horizontal other)) :
    nativeGK5AQBadPair first last f g :=
  nativeGK5AWHorizontalLeft_bad_localizes other
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- The genuine original horizontal RIGHT context is source-
typed; no shadow or selected source without an F55 preimage is used. -/
theorem nativeGK5AZHorizontalRight_raw_bad_localizes
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (other : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bf : nativeGK5AZSeamAt f)
    (bg : nativeGK5AZSeamAt g)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (other.horizontal f) (other.horizontal g)) :
    nativeGK5AQBadPair rightBefore rightAfter f g :=
  nativeGK5AWHorizontalRight_bad_localizes other
    (nativeGK5AZRawP93_to_phi bf bg raw) parentBad

/-- Exact raw original left unit from three separately named
sources of proof: F55 ident seam, raw trans shell, and seam of f.
The chosen vertical primitive supplies the remaining 4-cell. -/
def nativeGK5AZRawLeftUnit_from_local_gates
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r))
    (fBridge : nativeGK5AZSeamAt f)
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans (.ident r) f))
      (.trans
        (NativeF55P92AssocComparison.original (.ident r))
        (NativeF55P92AssocComparison.original f))) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans (.ident r) f))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5AZRawLeftVerticalUnit f
    (nativeGK5AZTrans_of_shell (.ident r) f unwrap identBridge fBridge)
    fBridge

/-- Exact raw original right unit from the symmetric local
identity seam at the F54 target route and a raw trans shell. -/
def nativeGK5AZRawRightUnit_from_local_gates
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (fBridge : nativeGK5AZSeamAt f)
    (identBridge : nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident s))
    (unwrap : NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f (.ident s)))
      (.trans
        (NativeF55P92AssocComparison.original f)
        (NativeF55P92AssocComparison.original (.ident s)))) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f (.ident s)))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5AZRawRightVerticalUnit f
    (nativeGK5AZTrans_of_shell f (.ident s) unwrap fBridge identBridge)
    fBridge

#print axioms nativeGK5AZPentagonAtom
#print axioms nativeGK5AZDisjointSquareAtom
#print axioms nativeGK5AZIdent_raw_ne_phi
#print axioms nativeGK5AZIdent_of_gate
#print axioms nativeGK5AZLeftContextIdentity_normalize
#print axioms nativeGK5AZRightContextIdentity_normalize
#print axioms nativeGK5AZLeftContext_raw_bad_localizes
#print axioms nativeGK5AZRightContext_raw_bad_localizes
#print axioms nativeGK5AZPrecompose_raw_bad_localizes
#print axioms nativeGK5AZPostcompose_raw_bad_localizes
#print axioms nativeGK5AZHorizontalLeft_raw_bad_localizes
#print axioms nativeGK5AZHorizontalRight_raw_bad_localizes
#print axioms nativeGK5AZRawLeftUnit_from_local_gates
#print axioms nativeGK5AZRawRightUnit_from_local_gates
#print axioms nativeGK5AZNorthPentagonAtom
#print axioms nativeGK5AZNorthDisjointSquareAtom
#print axioms nativeGK5AZSymm_of_two_gates
#print axioms nativeGK5AZTrans_of_shell
#print axioms nativeGK5AZTransShellHole
#print axioms nativeGK5AZTrans_seam_or_shellHole
#print axioms nativeGK5AZLeftContext_of_shell
#print axioms nativeGK5AZRightContext_of_shell
#print axioms nativeGK5AZPrecompose_of_shell
#print axioms nativeGK5AZPostcompose_of_shell
#print axioms nativeGK5AZRawP93_to_phi
#print axioms nativeGK5AZPhi_to_raw
#print axioms nativeGK5AZRawLeftVerticalUnit
#print axioms nativeGK5AZRawRightVerticalUnit
#print axioms nativeGK5AZRawVerticalAssoc
#print axioms nativeGK5AZLeftWhisker_raw_bad_localizes
#print axioms nativeGK5AZRightWhisker_raw_bad_localizes
#print axioms nativeGK5AZAssemblePointwise

end
end Kuu.F112.Physical
