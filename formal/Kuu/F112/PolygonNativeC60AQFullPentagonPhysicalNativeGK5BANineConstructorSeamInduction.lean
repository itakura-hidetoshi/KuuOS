import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AZConstructorLocalSeamObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5BA — complete dependent induction for the nine
genuine ORIGINAL F55 three-proof constructors, assembling
constructor-local Type-valued P94A seams into a global original→phi
four-cell comparison without postulating the global GK5AY seam.

The required local shell is indexed by the REAL original F55
proof term, preserving all F54 two-Nat/category/Blocks histories.
The two atoms pentagon/disjointSquare require PUnit (their seam
is reflexive). Ident requires an actual raw-to-refl four-cell.
Symm requires a raw inversion unwrap AND a map transporting
genuinely supplied child seams under three-cell inversion.
Trans requires a raw composition split shell; the child bridges
are assembled by existing P94A right/left whiskering.
Four original F45/F54 contexts need exact outer raw split shells,
while their inner seams are transported by existing selected
four-cell congruences.

The kit is a CONDITION of a coherent family of local shells,
not a theorem that every such shell exists. Its Nonempty is
equivalent to the pointwise Nonempty family by classical choice,
and the constructor recursion then produces a genuine global
GK5AY seam record at EVERY fixed original source slot. This
is sufficiency, NOT the converse (a global seam alone need not
supply each stronger raw factorization shell).

Any actual raw P93C witness at fixed original endpoints therefore
reflects to an original P89 four-cell OR a true GK5AQ BadPair
under the kit; source noninjectivity still requires a REAL
raw obstruction. No unconditional seam, P89 faithfulness,
P89 nonfaithfulness, or normalization of all 19 P94A constructors.

Strict 空 / independent Kuu→Qi; same public root107,
original F54 type history and authority unchanged, PR #1558
Draft/open preserved. Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, no Gray, new axioms, sorry/admit/native_decide.
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

/-- The EXACT constructor-local missing shell at a real original
F55 proof term. This uses a dependent Type, not a Boolean flag,
quotient class, or shadow equality. The two atomic cases are PUnit;
the other seven syntax cases carry their own genuinely typed
higher-cell requirements, including the separate symm action. -/
def nativeGK5BARequiredShell
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    Type (max (max uD uE) (max vD vE)) :=
  match f with
  | .ident route =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route))
        (NativeF55P92AssocComparison.refl route)
  | .pentagon _ _ _ _ => PUnit
  | .disjointSquare _ _ => PUnit
  | .symm cell =>
      (NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.symm cell))
        (.symm (NativeF55P92AssocComparison.original cell))) ×
      (NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original cell)
        (nativeGK5AIOriginalToP92Structural cell) →
        NativeF55P94UnitFourCell
          (.symm (NativeF55P92AssocComparison.original cell))
          (.symm (nativeGK5AIOriginalToP92Structural cell)))
  | .trans left right =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.trans left right))
        (.trans (NativeF55P92AssocComparison.original left)
          (NativeF55P92AssocComparison.original right))
  | .leftContext cell later =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.leftContext cell later))
        (.leftContext (NativeF55P92AssocComparison.original cell) later)
  | .rightContext earlier cell =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.rightContext earlier cell))
        (.rightContext earlier (NativeF55P92AssocComparison.original cell))
  | .precompose prior cell =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.precompose prior cell))
        (.precompose prior (NativeF55P92AssocComparison.original cell))
  | .postcompose cell suffix =>
      NativeF55P94UnitFourCell
        (NativeF55P92AssocComparison.original (.postcompose cell suffix))
        (.postcompose (NativeF55P92AssocComparison.original cell) suffix)

/-- A single dependent witness family across ALL original F54
source/target histories and both original category block axes.
It requires only constructor-specific local shells; neither
a global seam nor unconditional local existence is a field. -/
structure NativeGK5BAConstructorShellKit
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) where
  shell :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
      nativeGK5BARequiredShell f

/-- The ACTUAL 9-constructor dependent induction. Each recursive
source term has a selected four-cell, provided ONLY its local
constructor shell and (where needed) the recursively constructed
child seams. No reflection of raw evidence into P89 is inferred. -/
def NativeGK5BAConstructorShellKit.bridge
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (kit : NativeGK5BAConstructorShellKit p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original f)
      (nativeGK5AIOriginalToP92Structural f) := by
  induction f with
  | ident route =>
      exact kit.shell (.ident route)
  | pentagon t₁ t₂ t₃ t₄ =>
      exact nativeGK5AZPentagonAtom t₁ t₂ t₃ t₄
  | disjointSquare left right =>
      exact nativeGK5AZDisjointSquareAtom left right
  | symm cell ih =>
      let gates := kit.shell (.symm cell)
      exact nativeGK5AZSymm_of_two_gates cell gates.1 (gates.2 ih)
  | trans left right ihLeft ihRight =>
      exact nativeGK5AZTrans_of_shell left right
        (kit.shell (.trans left right)) ihLeft ihRight
  | leftContext cell later ih =>
      exact nativeGK5AZLeftContext_of_shell cell later
        (kit.shell (.leftContext cell later)) ih
  | rightContext earlier cell ih =>
      exact nativeGK5AZRightContext_of_shell earlier cell
        (kit.shell (.rightContext earlier cell)) ih
  | precompose prior cell ih =>
      exact nativeGK5AZPrecompose_of_shell _ prior cell
        (kit.shell (.precompose prior cell)) ih
  | postcompose cell suffix ih =>
      exact nativeGK5AZPostcompose_of_shell _ suffix cell
        (kit.shell (.postcompose cell suffix)) ih

/-- Assemble the complete global constructor induction into the
PREVIOUS GK5AY dependent seam record for ANY exact original F54
source/target slot. The kit is never silently instantiated. -/
def NativeGK5BAConstructorShellKit.toGK5AY
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (kit : NativeGK5BAConstructorShellKit p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeGK5AYOriginalPhiSeam first last :=
  ⟨fun f => kit.bridge f⟩

/-- Pointwise existence of EACH local constructor shell, at all
original F54 slots; this is still a HYPOTHESIS, not a global
automatic existence claim. -/
def nativeGK5BAAllLocalShells
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] : Prop :=
  ∀ {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
    Nonempty (nativeGK5BARequiredShell f)

/-- This is the EXACT equivalence at the level of the
constructor-shell KIT, not a false equivalence between arbitrary
global seams and stronger local raw factorization shells.
Choice is used only to select already assumed local witnesses. -/
theorem nativeGK5BAKit_nonempty_iff_allLocal
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Nonempty (NativeGK5BAConstructorShellKit p D E) ↔
      nativeGK5BAAllLocalShells p D E := by
  classical
  constructor
  · rintro ⟨kit⟩
    intro a b x y n n' m m' ma mb pa pb first last r s f
    exact ⟨kit.shell f⟩
  · intro h
    refine ⟨{ shell := ?_ }⟩
    intro a b x y n n' m m' ma mb pa pb first last r s f
    exact Classical.choice (h f)

/-- Pointwise local shell EXISTENCE across all source histories
implies the existence of a true GK5AY seam at any concrete
source. It is NOT a proof of the local shell hypothesis itself. -/
theorem nativeGK5BAAllLocal_constructs_GK5AY
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E]
    (h : nativeGK5BAAllLocalShells p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Nonempty (NativeGK5AYOriginalPhiSeam first last) := by
  obtain ⟨kit⟩ := (nativeGK5BAKit_nonempty_iff_allLocal p D E).2 h
  exact ⟨kit.toGK5AY first last⟩

/-- The EXACT constructor-shell obstruction is the negation of
inhabiting the required local shell family. It is not the
unconditional negation of arbitrary GK5AY seams. -/
def nativeGK5BAConstructorShellObstruction
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] : Prop :=
  ¬ nativeGK5BAAllLocalShells p D E

/-- No complete constructor shell KIT iff the precise local
shell requirement is obstructed; no existence is inferred. -/
theorem nativeGK5BAKit_obstructed_iff
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    (¬ Nonempty (NativeGK5BAConstructorShellKit p D E)) ↔
      nativeGK5BAConstructorShellObstruction p D E := by
  exact not_congr (nativeGK5BAKit_nonempty_iff_allLocal p D E)

/-- Under the genuine constructor KIT, a real raw P93C witness
at genuine ORIGINAL F55 endpoints either reflects to an ORIGINAL
P89 four-cell or yields a true GK5AQ BadPair. This uses the
actual constructor recursion, not a separately assumed seam. -/
theorem nativeGK5BARawP93_reflect_or_bad
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (kit : NativeGK5BAConstructorShellKit p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      nativeGK5AQBadPair first last f g := by
  classical
  by_cases h : Nonempty (NativeF55P89InterchangeFourCell f g)
  · exact Or.inl h
  · exact Or.inr ⟨⟨nativeGK5AZRawP93_to_phi
      (kit.bridge f) (kit.bridge g) raw⟩, h⟩

/-- A real raw source P93C/P89 obstruction, in the presence
of the constructor kit, forces noninjectivity at some exact
original F54 route slot. No obstruction witness is constructed. -/
theorem nativeGK5BARawObstruction_forces_noninjective
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (kit : NativeGK5BAConstructorShellKit p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (h : nativeGK5AYRawP93Obstruction first last) :
    ∃ (r s : KuuNativeF45Tree.DepthRotationRoute p first last),
      ¬ Function.Injective
        (nativeGK5ANP89ToP94FourClassMap first last r s) :=
  nativeGK5AYRawObstruction_forces_noninjective
    (kit.toGK5AY first last) h

/-- Conversely the true original source class-map injectivity,
if separately supplied at a fixed F54 route slot, produces raw
P93C reflection using only the constructor kit as seam evidence. -/
theorem nativeGK5BARawReflects_of_injective
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (kit : NativeGK5BAConstructorShellKit p D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (hinj : Function.Injective
      (nativeGK5ANP89ToP94FourClassMap first last r s))
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (raw : NativeF55P93AssocFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g)) :
    Nonempty (NativeF55P89InterchangeFourCell f g) :=
  nativeGK5AYRawReflects_of_injective
    (kit.toGK5AY first last) hinj f g raw

#print axioms nativeGK5BARequiredShell
#print axioms NativeGK5BAConstructorShellKit
#print axioms NativeGK5BAConstructorShellKit.bridge
#print axioms NativeGK5BAConstructorShellKit.toGK5AY
#print axioms nativeGK5BAAllLocalShells
#print axioms nativeGK5BAKit_nonempty_iff_allLocal
#print axioms nativeGK5BAAllLocal_constructs_GK5AY
#print axioms nativeGK5BAConstructorShellObstruction
#print axioms nativeGK5BAKit_obstructed_iff
#print axioms nativeGK5BARawP93_reflect_or_bad
#print axioms nativeGK5BARawObstruction_forces_noninjective
#print axioms nativeGK5BARawReflects_of_injective

end
end Kuu.F112.Physical
