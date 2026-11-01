import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5FIndexRelabelingCoherence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5G — actual pointwise CATEGORY-EQUIVALENCE changes of
finite heterogeneous typed functor trees, genuine coherence and
chosen-inverse path naturality.

After GK5F's exact index relabeling of a fixed category family,
GK5G changes the actual categories: for each i : I, assume a REAL
Mathlib equivalence E i : C i ≌ D i. Genuine source functors R :
C i ⥤ C j transport to E_i.inverse ⋙ R ⋙ E_j.functor.
The equivalences are not assumed strict, so a binary composite is
related to the conjugate of its whole composite by an ACTUAL NatIso
built using E_j.unitIso.symm. Unit trees require E_i.counitIso.symm.

All finite words, binary trees, proof-relevant associator/unitor/
whiskering rewrite paths are transported constructively. The true
whole NatIso from recursively combining actual equivalence unit,
counit, associators and whiskering compares a transported tree to
the transported WHOLE original functor.

Original arbitrary chosen inverses Q and explicit P remain distinct,
linked by the genuine previously proved GK4BQ kappa. GK5E's whole
chosen-inverse target-NatTrans square applies to every explicitly
transported path. This does NOT assert an unsupported strict equality
of all conjugations, nor a whole naturality bridge across unrelated
chosen inverses at categories C_i and D_i.

Scope: fixed-universe-pair genuine Mathlib categories, specified
pointwise equivalences, and finite typed paths only. No arbitrary
changing-universe chain, original raw F54/F55/P92B Type high-cells,
Gray category or unrestricted higher hyperdescent.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC uD vD uE vE

section PointwiseEquivalenceTransport
variable {I : Type uI}
variable {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- Genuine pointwise category-change action on a typed functor:
a chosen quasi-inverse on the source, original F, and the
given genuine equivalence's forward functor on the target. -/
def nativeGK5GChangeAtom {i j : I} (R : C i ⥤ C j) : D i ⥤ D j :=
  (e i).inverse ⋙ R ⋙ (e j).functor

/-- A true natural transformation changes category through actual
Mathlib whiskering by both pointwise equivalence functors. -/
def nativeGK5GChangeNat {i j : I} {R S : C i ⥤ C j}
    (ρ : R ⟶ S) :
    nativeGK5GChangeAtom e R ⟶ nativeGK5GChangeAtom e S :=
  Functor.whiskerLeft (e i).inverse
    (Functor.whiskerRight ρ (e j).functor)

/-- Same construction for an ACTUAL whole Mathlib NatIso.
This is not a new raw source higher-cell or an equality postulate. -/
noncomputable def nativeGK5GChangeIso {i j : I} {R S : C i ⥤ C j}
    (α : R ≅ S) :
    nativeGK5GChangeAtom e R ≅ nativeGK5GChangeAtom e S :=
  Functor.isoWhiskerLeft (e i).inverse
    (Functor.isoWhiskerRight α (e j).functor)

/-- Retain every intermediate target category in a changed finite
dependent word, not a plain untyped list of functors. -/
def nativeGK5GChangeWord :
    ∀ {i j : I}, NativeGK5DTypedWord C i j → NativeGK5DTypedWord D i j
  | _, _, .empty i => .empty i
  | _, _, .cons R rs => .cons (nativeGK5GChangeAtom e R)
      (nativeGK5GChangeWord rs)

/-- Change EVERY category boundary in an actual finite typed tree.
Inserted identities remain genuine identities of the NEW categories. -/
def nativeGK5GChangeTree :
    ∀ {i j : I}, NativeGK5DTypedTree C i j → NativeGK5DTypedTree D i j
  | _, _, .unit i => .unit i
  | _, _, .atom R => .atom (nativeGK5GChangeAtom e R)
  | _, _, .paste left right =>
      .paste (nativeGK5GChangeTree left) (nativeGK5GChangeTree right)

/-- A pointwise equivalence transports every ACTUAL typed
associator/unitor/whiskering rewrite constructor. -/
def nativeGK5GChangeStep :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedStep C a b →
      NativeGK5DTypedStep D
        (nativeGK5GChangeTree e a) (nativeGK5GChangeTree e b)
  | _, _, _, _, .assoc a b c =>
      .assoc (nativeGK5GChangeTree e a)
        (nativeGK5GChangeTree e b) (nativeGK5GChangeTree e c)
  | _, _, _, _, .leftUnit a => .leftUnit (nativeGK5GChangeTree e a)
  | _, _, _, _, .rightUnit a => .rightUnit (nativeGK5GChangeTree e a)
  | _, _, _, _, .whiskerRight h c =>
      .whiskerRight (nativeGK5GChangeStep h) (nativeGK5GChangeTree e c)
  | _, _, _, _, .whiskerLeft a h =>
      .whiskerLeft (nativeGK5GChangeTree e a) (nativeGK5GChangeStep h)

/-- Transport full proof-relevant finite paths, retaining identity,
real basic steps, inverses and path concatenation. -/
def nativeGK5GChangePath :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j},
      NativeGK5DTypedPath C a b →
      NativeGK5DTypedPath D
        (nativeGK5GChangeTree e a) (nativeGK5GChangeTree e b)
  | _, _, _, _, .refl a => .refl (nativeGK5GChangeTree e a)
  | _, _, _, _, .basic h => .basic (nativeGK5GChangeStep e h)
  | _, _, _, _, .reverse q => .reverse (nativeGK5GChangePath q)
  | _, _, _, _, .trans q r =>
      .trans (nativeGK5GChangePath q) (nativeGK5GChangePath r)

/-- The changed full dependent leaf-word agrees with changing
each original genuine leaf, and preserves their entire order. -/
theorem nativeGK5GChangeWord_append
    {i j k : I} (xs : NativeGK5DTypedWord C i j)
    (ys : NativeGK5DTypedWord C j k) :
    nativeGK5GChangeWord e (nativeGK5DWordAppend xs ys) =
      nativeGK5DWordAppend
        (nativeGK5GChangeWord e xs) (nativeGK5GChangeWord e ys) := by
  induction xs with
  | empty _ => rfl
  | cons R xs ih =>
      change NativeGK5DTypedWord.cons (nativeGK5GChangeAtom e R)
          (nativeGK5GChangeWord e (nativeGK5DWordAppend xs ys)) =
        NativeGK5DTypedWord.cons (nativeGK5GChangeAtom e R)
          (nativeGK5DWordAppend (nativeGK5GChangeWord e xs)
            (nativeGK5GChangeWord e ys))
      rw [ih]

theorem nativeGK5GChangeTree_leaves
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5DTreeLeaves (nativeGK5GChangeTree e t) =
      nativeGK5GChangeWord e (nativeGK5DTreeLeaves t) := by
  induction t with
  | unit _ => rfl
  | atom _ => rfl
  | paste left right hl hr =>
      change nativeGK5DWordAppend
          (nativeGK5DTreeLeaves (nativeGK5GChangeTree e left))
          (nativeGK5DTreeLeaves (nativeGK5GChangeTree e right)) =
        nativeGK5GChangeWord e
          (nativeGK5DWordAppend (nativeGK5DTreeLeaves left)
            (nativeGK5DTreeLeaves right))
      rw [nativeGK5GChangeWord_append, hl, hr]

/-- ACTUAL counit of the category equivalence is required to
compare the new identity functor with the conjugate old identity.
Unlike GK5F this need NOT be equality of whole functors. -/
noncomputable def nativeGK5GChangeUnitIso (i : I) :
    (𝟭 (D i)) ≅ nativeGK5GChangeAtom e (𝟭 (C i)) :=
  (e i).counitIso.symm ≪≫
    eqToIso (congrArg
      (fun F : D i ⥤ C i => F ⋙ (e i).functor)
      (Functor.comp_id (e i).inverse).symm)

/-- Binary composition of genuine transported functors is
canonically NatIso to transport of the original composite.
The MIDDLE unitIso of the category equivalence is used
essentially; no false strict functor equality is asserted. -/
noncomputable def nativeGK5GChangeCompIso
    {i j k : I} (R : C i ⥤ C j) (S : C j ⥤ C k) :
    (nativeGK5GChangeAtom e R ⋙ nativeGK5GChangeAtom e S) ≅
      nativeGK5GChangeAtom e (R ⋙ S) := by
  let Gi : D i ⥤ C i := (e i).inverse
  let Fj : C j ⥤ D j := (e j).functor
  let Gj : D j ⥤ C j := (e j).inverse
  let Fk : C k ⥤ D k := (e k).functor
  let A : D i ⥤ C j := Gi ⋙ R
  let B : C j ⥤ D k := S ⋙ Fk
  have h₁ :
      (nativeGK5GChangeAtom e R ⋙ nativeGK5GChangeAtom e S) =
        A ⋙ ((Fj ⋙ Gj) ⋙ B) := by
    simp only [nativeGK5GChangeAtom, A, B, Gi, Fj, Gj, Fk, Functor.assoc]
  have h₂ : A ⋙ ((𝟭 (C j)) ⋙ B) =
      nativeGK5GChangeAtom e (R ⋙ S) := by
    simp only [A, B, Gi, Fk, nativeGK5GChangeAtom,
      Functor.id_comp, Functor.assoc]
  exact eqToIso h₁ ≪≫
    Functor.isoWhiskerLeft A
      (Functor.isoWhiskerRight (e j).unitIso.symm B) ≪≫
    eqToIso h₂

/-- MAIN CONSTRUCTIVE TREE COHERENCE under ACTUAL pointwise
category equivalences. The whole Mathlib NatIso is recursively
assembled using real counits at unit nodes, true middle unit
cancellations at paste nodes, and genuine iso whiskerings.
No objectwise inverse is assumed to commute strictly. -/
noncomputable def nativeGK5GChangeTreeIso :
    ∀ {i j : I} (t : NativeGK5DTypedTree C i j),
      nativeGK5DTreeComposite (nativeGK5GChangeTree e t) ≅
        nativeGK5GChangeAtom e (nativeGK5DTreeComposite t)
  | _, _, .unit i => nativeGK5GChangeUnitIso e i
  | _, _, .atom R => Iso.refl _
  | _, _, .paste left right =>
      (Functor.isoWhiskerRight (nativeGK5GChangeTreeIso left)
        (nativeGK5DTreeComposite (nativeGK5GChangeTree e right))) ≪≫
      (Functor.isoWhiskerLeft
        (nativeGK5GChangeAtom e (nativeGK5DTreeComposite left))
        (nativeGK5GChangeTreeIso right)) ≪≫
      nativeGK5GChangeCompIso e
        (nativeGK5DTreeComposite left) (nativeGK5DTreeComposite right)

/-- The actual finite path construction transports reachability
between the specified changed category families. -/
theorem nativeGK5GChangePath_reachable
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    Nonempty (NativeGK5DTypedPath D
      (nativeGK5GChangeTree e a) (nativeGK5GChangeTree e b)) :=
  ⟨nativeGK5GChangePath e q⟩

/-- GK5D constructive normalization provides an actual path
between any two identical typed ordered leaf words; transporting
it under specified pointwise equivalences remains nonvacuous. -/
theorem nativeGK5GChangeSameLeaves_reachable
    {i j : I} (a b : NativeGK5DTypedTree C i j)
    (h : nativeGK5DTreeLeaves a = nativeGK5DTreeLeaves b) :
    Nonempty (NativeGK5DTypedPath D
      (nativeGK5GChangeTree e a) (nativeGK5GChangeTree e b)) :=
  ⟨nativeGK5GChangePath e
    (nativeGK5DPathBetweenOfSameLeaves a b h)⟩

/-- Both source/target natural isomorphism boundaries in GK5D
remain actual whole NatIso values for the changed finite path. -/
theorem nativeGK5GChangedPathIso_eqToIso
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    nativeGK5DPathIso (nativeGK5GChangePath e q) =
      eqToIso (nativeGK5DPathEq (nativeGK5GChangePath e q)) :=
  nativeGK5DPathIso_eqToIso (nativeGK5GChangePath e q)

end PointwiseEquivalenceTransport

section ChosenInversePointwiseEquivalence
variable {I : Type uI}
variable {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)
variable {A : Type uD} [Category.{vD} A]
variable {B : Type uE} [Category.{vE} B]
variable {a b : A} {x y : B}

/-- Genuine GK5E recursively chosen whole NatIso remains the
direct GK4BT chosen-inverse comparison after the REAL pointwise
category-change, without identifying arbitrary Q with explicit P. -/
theorem nativeGK5GChangedChosenInverse_treeIso_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5GChangeTree e t) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb
        (nativeGK5DTreeComposite (nativeGK5GChangeTree e t)) :=
  nativeGK5EChosenInverse_treeIso_eq_direct p ma mb pa pb
    (nativeGK5GChangeTree e t)

/-- Genuine WHOLE target NatTrans modification square for every
actually transported finite associator/unitor/whiskering path.
GK5G does not claim unproved cross-family strictness of Q_i. -/
theorem nativeGK5GChangedChosenInverse_path_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} {left right : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C left right) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5GChangePath e q)).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := D j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5GChangeTree e right)).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb
      (nativeGK5GChangeTree e left)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := D i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso (nativeGK5GChangePath e q)).hom) :=
  nativeGK5EChosenInverse_rewritePath_square p ma mb pa pb
    (nativeGK5GChangePath e q)

/-- Actual GK5D normalization IN THE CHANGED FAMILY D also carries
the arbitrary-choice inverse whole target NatTrans square. This
retains genuine structural paths and all GK4BM choice boundaries. -/
theorem nativeGK5GChangedChosenInverse_normalization_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK5DPathIso
            (nativeGK5DNormalizePath (nativeGK5GChangeTree e t))).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := D j) p ma mb pa pb) ≫
      (nativeGK5EChosenInverse_treeIso p ma mb pa pb
        (nativeGK5DTreeOfWord
          (nativeGK5DTreeLeaves (nativeGK5GChangeTree e t)))).hom =
    (nativeGK5EChosenInverse_treeIso p ma mb pa pb
      (nativeGK5GChangeTree e t)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := D i) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK5DPathIso
            (nativeGK5DNormalizePath (nativeGK5GChangeTree e t))).hom) :=
  nativeGK5EChosenInverse_normalization_square p ma mb pa pb
    (nativeGK5GChangeTree e t)

end ChosenInversePointwiseEquivalence

#print axioms nativeGK5GChangeAtom
#print axioms nativeGK5GChangeNat
#print axioms nativeGK5GChangeIso
#print axioms nativeGK5GChangeWord
#print axioms nativeGK5GChangeTree
#print axioms nativeGK5GChangeStep
#print axioms nativeGK5GChangePath
#print axioms nativeGK5GChangeWord_append
#print axioms nativeGK5GChangeTree_leaves
#print axioms nativeGK5GChangeUnitIso
#print axioms nativeGK5GChangeCompIso
#print axioms nativeGK5GChangeTreeIso
#print axioms nativeGK5GChangePath_reachable
#print axioms nativeGK5GChangeSameLeaves_reachable
#print axioms nativeGK5GChangedPathIso_eqToIso
#print axioms nativeGK5GChangedChosenInverse_treeIso_eq_direct
#print axioms nativeGK5GChangedChosenInverse_path_square
#print axioms nativeGK5GChangedChosenInverse_normalization_square

end
end Kuu.F112.Physical
