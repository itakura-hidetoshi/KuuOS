import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BFiniteTreeRewritePathCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5C — actual proof-relevant normalization REACHABILITY
for every finite endofunctor tree, by genuine Mathlib associator,
left/right unitor and typed whiskering rewrite paths.

GK5B established equality of genuine whole Mathlib NatIso values for
already existing paths. GK5C now CONSTRUCTS such a path from EACH
finite tree to GK5A's right-associated canonical leaf-word tree, with
real intermediate typed rewrites and no new primitive source high cells.

A recursive list-append path uses real associators and left unitors.
A recursive tree normalization uses right unitors for atomic leaves,
whiskering on both subtrees, and the append path. We prove actual
normalization Iso agrees, after the true eqToIso transport at its
canonical target, with the GK5B finite-word normalization NatIso.

Equal ordered leaf words are NECESSARY AND SUFFICIENT for existence
of a typed finite real rewrite path. Thus genuine rewrite-path
independence from GK5B is non-vacuous for any two tree presentations
of the same ordered leaves. GK5A/GK4BU chosen-inverse naturality
and both-end eqToIso transport apply to the explicitly constructed path.

Scope: finite endofunctor trees of one fixed genuine Mathlib target
category. NOT arbitrary many-category dependent chains, unconditional
original F45 source faithfulness, source-Q category axioms, raw
F54/F55/P92B Type-valued higher cells, ambient integer-matrix
attainability, Gray category reconstruction, or hyperdescent.
GK4BM's arbitrary chosen Q and GK4BP explicit P remain different
presentations connected by GK4BQ's genuine NatIso, not definitionally
equal. Strict 空 center, independent Kuu one presentation.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

section FiniteTreeNormalization
variable {T : Type uT} [Category.{vT} T]

/-- Genuine path-level left whiskering, recursively retaining
all original associator/unitor steps and their path composition. -/
def nativeGK5CPathWhiskerLeft (fixed : NativeGK5AFiniteTargetTree T) :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewritePath T a b →
      NativeGK5BRewritePath T (.paste fixed a) (.paste fixed b)
  | _, _, .refl _ => .refl _
  | _, _, .basic h => .basic (.whiskerLeft fixed h)
  | _, _, .reverse p => .reverse (nativeGK5CPathWhiskerLeft fixed p)
  | _, _, .trans p q =>
      .trans (nativeGK5CPathWhiskerLeft fixed p)
        (nativeGK5CPathWhiskerLeft fixed q)

/-- Genuine path-level right whiskering, preserving all
intermediate actual Mathlib structural steps. -/
def nativeGK5CPathWhiskerRight :
    ∀ {a b : NativeGK5AFiniteTargetTree T},
      NativeGK5BRewritePath T a b →
      (fixed : NativeGK5AFiniteTargetTree T) →
      NativeGK5BRewritePath T (.paste a fixed) (.paste b fixed)
  | _, _, .refl _, _ => .refl _
  | _, _, .basic h, fixed => .basic (.whiskerRight h fixed)
  | _, _, .reverse p, fixed => .reverse (nativeGK5CPathWhiskerRight p fixed)
  | _, _, .trans p q, fixed =>
      .trans (nativeGK5CPathWhiskerRight p fixed)
        (nativeGK5CPathWhiskerRight q fixed)

/-- The recursively constructed REAL rewrite path for appending
two right-associated canonical finite-list trees. A nonempty
left word genuinely reassociates and then rewrites under a
left whisker; the empty left word uses the true left unitor. -/
def nativeGK5CAppendPath :
    (xs ys : List (T ⥤ T)) →
      NativeGK5BRewritePath T
        (.paste (nativeGK5ATreeOfList xs) (nativeGK5ATreeOfList ys))
        (nativeGK5ATreeOfList (xs ++ ys))
  | [], ys => .basic (.leftUnit (nativeGK5ATreeOfList ys))
  | R :: xs, ys =>
      .trans
        (.basic (.assoc (.atom R)
          (nativeGK5ATreeOfList xs) (nativeGK5ATreeOfList ys)))
        (nativeGK5CPathWhiskerLeft (.atom R)
          (nativeGK5CAppendPath xs ys))

/-- CONSTRUCTIVE FINITE NORMALIZATION. For each tree t, produce
a genuine finite typed sequence of Mathlib associators/unitors
and whiskerings from t to the canonical right-associated
treeOfList(leaves t), retaining all intermediate rewrite evidence. -/
def nativeGK5CNormalizePath :
    (t : NativeGK5AFiniteTargetTree T) →
      NativeGK5BRewritePath T t
        (nativeGK5ATreeOfList (nativeGK5ATreeLeaves t))
  | .unit => .refl _
  | .atom R => .reverse (.basic (.rightUnit (.atom R)))
  | .paste left right =>
      .trans
        (nativeGK5CPathWhiskerRight (nativeGK5CNormalizePath left) right)
        (.trans
          (nativeGK5CPathWhiskerLeft
            (nativeGK5ATreeOfList (nativeGK5ATreeLeaves left))
            (nativeGK5CNormalizePath right))
          (nativeGK5CAppendPath
            (nativeGK5ATreeLeaves left) (nativeGK5ATreeLeaves right)))

/-- The canonical right-associated true finite tree has EXACTLY
the given ordered list of genuine non-unit endofunctor leaves. -/
theorem nativeGK5CTreeOfList_leaves (rs : List (T ⥤ T)) :
    nativeGK5ATreeLeaves (nativeGK5ATreeOfList rs) = rs := by
  induction rs with
  | nil => rfl
  | cons R rs ih =>
      simp [nativeGK5ATreeOfList, nativeGK5ATreeLeaves, ih]

/-- The actual normalization path preserves ALL ordered leaf
functors, and its target really is the canonical list tree. -/
theorem nativeGK5CNormalizePath_leaves
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5ATreeLeaves t =
      nativeGK5ATreeLeaves
        (nativeGK5ATreeOfList (nativeGK5ATreeLeaves t)) :=
  nativeGK5BPathLeaves (nativeGK5CNormalizePath t)

/-- The WHOLE Mathlib NatIso of the actually constructed normalization
path followed by the true GK5A terminal whole-functor eqToIso is
EXACTLY GK5B's canonical normalization Iso; no informal identification
of different dependent target types is made. -/
theorem nativeGK5CNormalizePath_iso_eq_canonical
    (t : NativeGK5AFiniteTargetTree T) :
    nativeGK5BPathIso (nativeGK5CNormalizePath t) ≪≫
      eqToIso (nativeGK5ATreeOfList_eval
        (nativeGK5ATreeLeaves t)) =
    nativeGK5BTreeNormalization t := by
  simp only [nativeGK5BPathIso_eqToIso,
    nativeGK5BTreeNormalization, eqToIso_trans]

/-- Any two presentations of the SAME ordered genuine leaves
are connected by a CONSTRUCTED finite REAL rewrite path:
normalize the first, then reverse normalization of the second.
This does not assume arbitrary raw high-cell reachability. -/
def nativeGK5CPathBetweenOfSameLeaves
    (left right : NativeGK5AFiniteTargetTree T)
    (h : nativeGK5ATreeLeaves left = nativeGK5ATreeLeaves right) :
    NativeGK5BRewritePath T left right := by
  have q : NativeGK5BRewritePath T right
      (nativeGK5ATreeOfList (nativeGK5ATreeLeaves left)) := by
    simpa only [h] using (nativeGK5CNormalizePath right)
  exact .trans (nativeGK5CNormalizePath left) (.reverse q)

/-- EXACT reachability criterion for the actual finite-tree
associator/unitor rewrite system: same ordered leaves if and only
if there EXISTS a correctly typed concrete rewrite path. -/
theorem nativeGK5CReachable_iff_sameLeaves
    (left right : NativeGK5AFiniteTargetTree T) :
    Nonempty (NativeGK5BRewritePath T left right) ↔
      nativeGK5ATreeLeaves left = nativeGK5ATreeLeaves right := by
  constructor
  · rintro ⟨p⟩
    exact nativeGK5BPathLeaves p
  · intro h
    exact ⟨nativeGK5CPathBetweenOfSameLeaves left right h⟩

/-- NONVACUOUS path independence: any genuine rewrite path between
two tree presentations is whole-NatIso equal to the concretely
constructed normalize/reverse-normalize comparison path. -/
theorem nativeGK5CPath_eq_canonical_of_path
    {left right : NativeGK5AFiniteTargetTree T}
    (path : NativeGK5BRewritePath T left right) :
    nativeGK5BPathIso path =
      nativeGK5BPathIso
        (nativeGK5CPathBetweenOfSameLeaves left right
          (nativeGK5BPathLeaves path)) :=
  nativeGK5BPath_independent path
    (nativeGK5CPathBetweenOfSameLeaves left right
      (nativeGK5BPathLeaves path))

end FiniteTreeNormalization

section ChosenInverseFiniteNormalization
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- The genuine GK4BU whole target-NatTrans modification holds
ALONG the ACTUAL constructive tree-to-canonical normalization path,
not merely for an existential or postulated transport. -/
theorem nativeGK5CChosenInverse_normalization_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5BPathIso (nativeGK5CNormalizePath t)).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb
        (nativeGK5ATreeOfList (nativeGK5ATreeLeaves t))).hom =
    (nativeGK5AChosenInverse_treeIso p ma mb pa pb t).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5BPathIso (nativeGK5CNormalizePath t)).hom) :=
  nativeGK5BChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5CNormalizePath t)

/-- The full chosen-inverse whole NatIso comparison is transported
along the ACTUAL constructive normalization path using both real
boundary eqToIso morphisms. All previous GK5A/GK5B choice boundaries
are retained; this is not a definitional equation Q_T=P_T. -/
theorem nativeGK5CChosenInverse_normalization_transport
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (t : NativeGK5AFiniteTargetTree T) :
    eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BNPostcompCompatible p ma mb pa pb K ⋙
            nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK5BPathEq (nativeGK5CNormalizePath t))) ≪≫
      nativeGK5AChosenInverse_treeIso p ma mb pa pb
        (nativeGK5ATreeOfList (nativeGK5ATreeLeaves t)) ≪≫
      eqToIso (congrArg
        (fun K : T ⥤ T =>
          nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
            nativeGK4BNPostcompAttained p ma mb pa pb K)
        (nativeGK5BPathEq (nativeGK5CNormalizePath t)).symm) =
    nativeGK5AChosenInverse_treeIso p ma mb pa pb t :=
  nativeGK5BChosenInverse_rewritePath_transport p ma mb pa pb
    (nativeGK5CNormalizePath t)

/-- Any same-leaf pair has not just a canonical rewrite path but
a concrete whole chosen-inverse target modification square along it. -/
theorem nativeGK5CChosenInverse_sameLeaves_canonical_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (left right : NativeGK5AFiniteTargetTree T)
    (h : nativeGK5ATreeLeaves left = nativeGK5ATreeLeaves right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5BPathIso
            (nativeGK5CPathBetweenOfSameLeaves left right h)).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb) ≫
      (nativeGK5AChosenInverse_treeIso p ma mb pa pb right).hom =
    (nativeGK5AChosenInverse_treeIso p ma mb pa pb left).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5BPathIso
            (nativeGK5CPathBetweenOfSameLeaves left right h)).hom) :=
  nativeGK5BChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5CPathBetweenOfSameLeaves left right h)

end ChosenInverseFiniteNormalization

#print axioms nativeGK5CPathWhiskerLeft
#print axioms nativeGK5CPathWhiskerRight
#print axioms nativeGK5CAppendPath
#print axioms nativeGK5CNormalizePath
#print axioms nativeGK5CTreeOfList_leaves
#print axioms nativeGK5CNormalizePath_leaves
#print axioms nativeGK5CNormalizePath_iso_eq_canonical
#print axioms nativeGK5CPathBetweenOfSameLeaves
#print axioms nativeGK5CReachable_iff_sameLeaves
#print axioms nativeGK5CPath_eq_canonical_of_path
#print axioms nativeGK5CChosenInverse_normalization_square
#print axioms nativeGK5CChosenInverse_normalization_transport
#print axioms nativeGK5CChosenInverse_sameLeaves_canonical_square

end
end Kuu.F112.Physical
