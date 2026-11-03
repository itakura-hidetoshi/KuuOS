import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AWContextGeneratorReflectionGate
import Mathlib.Tactic

/-!
F112-P94D3GK5AX — ORIGINAL F55 source-indexed selected P94A
vertical primitive reflection gates and finite typed source-word descent.

GK5AU recursively audited all 19 genuine P94A and 16 embedded P93C
four-cell constructors for original F55 phi-source-image holes.
GK5AV built true original source-vertex comparison chains from a
source-saturated vertical trans. GK5AW localized BadPair obstructions
through eight real P89 source context operations.

The selected P93C/P94A grammar additionally CHOOSES 3 primitive
vertical 4-cells (left unit, right unit, associativity). None is
silently attributed to the original P89 13-constructor grammar.
Here these primitives are restricted to GENUINE original F55
proof-indexed source histories and their structurally translated
P92B phi-images. The selected P94A 4-cell is truly CONSTRUCTED,
and its failure to reflect to original P89 is equivalent to an
ACTUAL GK5AQ BadPair for the same genuine source endpoints.

The exact additional original P89 reflection evidence required by
the three primitives is bundled in a Type-valued dependent record,
not declared inhabited. A separate proof-relevant finite vertical
source-word grammar is interpreted unconditionally in selected
P94A and, CONDITIONALLY on that original record, in genuine P89.
The precise iff with absence of primitive BadPairs explains the
remaining obstruction. It does not infer global P89/P94A
faithfulness, nor normalize an arbitrary selected P94A proof word.

The original P93C .old generator uses SELECTED P92B.original proof
terms, not by definition GK5AI's recursively computed phi-image;
the two proof-authority boundaries remain distinct. Independent
Kuu -> Qi, strict 空 authority, append-only same public root 107,
protected #1558 Draft/open. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or global gluing.
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
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- TRUE P94A left vertical unit comparison indexed by an ORIGINAL
F55 three-proof, not a generic selected P92B proof. The original
left endpoint is an actual original F55 trans with ident. -/
def nativeGK5AXSelectedLeftUnit
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural (.trans (.ident r) f))
      (nativeGK5AIOriginalToP92Structural f) :=
  .verticalLeftUnit (nativeGK5AIOriginalToP92Structural f)

/-- TRUE P94A right vertical unit, with a genuine ORIGINAL
F55 identity at the original target route. -/
def nativeGK5AXSelectedRightUnit
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural (.trans f (.ident s)))
      (nativeGK5AIOriginalToP92Structural f) :=
  .verticalRightUnit (nativeGK5AIOriginalToP92Structural f)

/-- The new selected associativity 4-cell has a genuine ORIGINAL
F55 typed source triple and exactly translated P92B 3-cell endpoints.
This does NOT itself construct any original P89 associativity proof. -/
def nativeGK5AXSelectedVerticalAssoc
    {t z : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t z) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural (.trans (.trans f g) h))
      (nativeGK5AIOriginalToP92Structural (.trans f (.trans g h))) :=
  .verticalAssoc
    (nativeGK5AIOriginalToP92Structural f)
    (nativeGK5AIOriginalToP92Structural g)
    (nativeGK5AIOriginalToP92Structural h)

/-- Source-indexed left unit failure is EXACTLY a GK5AQ BadPair
because the selected P94A witness is explicitly available.
No failed original P89 witness is asserted to exist. -/
theorem nativeGK5AXLeftUnit_bad_iff_noP89
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AQBadPair first last (.trans (.ident r) f) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans (.ident r) f) f) := by
  constructor
  · exact fun bad => bad.2
  · exact fun missing => ⟨⟨nativeGK5AXSelectedLeftUnit f⟩, missing⟩

/-- Source-indexed right unit failure is an EXACT original P89
reflection obstruction, not a numeric C60 shadow discrepancy. -/
theorem nativeGK5AXRightUnit_bad_iff_noP89
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AQBadPair first last (.trans f (.ident s)) f ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans f (.ident s)) f) := by
  constructor
  · exact fun bad => bad.2
  · exact fun missing => ⟨⟨nativeGK5AXSelectedRightUnit f⟩, missing⟩

/-- Source-indexed vertical associativity has a TRUE selected
P94A four-proof, and exactly requires an ORIGINAL P89 four-proof
to exclude a genuine GK5AQ BadPair. -/
theorem nativeGK5AXAssoc_bad_iff_noP89
    {t z : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t z) :
    nativeGK5AQBadPair first last
      (.trans (.trans f g) h) (.trans f (.trans g h)) ↔
      ¬ Nonempty (NativeF55P89InterchangeFourCell
        (.trans (.trans f g) h) (.trans f (.trans g h))) := by
  constructor
  · exact fun bad => bad.2
  · exact fun missing =>
      ⟨⟨nativeGK5AXSelectedVerticalAssoc f g h⟩, missing⟩

/-- Additional TRUE, proof-relevant ORIGINAL P89 four-cell
certificates for ALL three selected primitive vertical families.
This is a CONDITION, not an asserted construction. Its fields
retain the original F54 two-Nat, two-category and proof history. -/
structure NativeGK5AXVerticalPrimitiveCertificates
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Type (max (max uD uE) (max vD vE)) where
  leftUnit :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v),
      NativeF55P89InterchangeFourCell (.trans (.ident u) f) f
  rightUnit :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v),
      NativeF55P89InterchangeFourCell (.trans f (.ident v)) f
  assoc :
    ∀ {u v w z : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
      (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p w z),
      NativeF55P89InterchangeFourCell
        (.trans (.trans f g) h) (.trans f (.trans g h))

/-- A typed ORIGINAL-source finite vertical four-proof grammar.
It is a SUBPRESENTATION with genuine original F55 endpoints.
It is not the full 19-constructor selected P94A syntax. -/
inductive NativeGK5AXSourceVerticalWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) →
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) →
    Type (max (max uD uE) (max vD vE)) where
  | refl (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
      NativeGK5AXSourceVerticalWord f f
  | symm
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeGK5AXSourceVerticalWord f g) :
      NativeGK5AXSourceVerticalWord g f
  | trans
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (fg : NativeGK5AXSourceVerticalWord f g)
      (gh : NativeGK5AXSourceVerticalWord g h) :
      NativeGK5AXSourceVerticalWord f h
  | leftUnit (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
      NativeGK5AXSourceVerticalWord (.trans (.ident r) f) f
  | rightUnit (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
      NativeGK5AXSourceVerticalWord (.trans f (.ident s)) f
  | assoc
      {t u : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r t)
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t u)
      (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u s) :
      NativeGK5AXSourceVerticalWord
        (.trans (.trans f g) h) (.trans f (.trans g h))

/-- EVERY finite source-vertical word has an ACTUAL selected P94A
four-cell interpretation; no original P89 reflection data needed.
All original F55 history endpoints are structurally phi-translated. -/
def NativeGK5AXSourceVerticalWord.toSelected
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5AXSourceVerticalWord f g) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) := by
  induction w with
  | refl f => exact .refl _
  | symm inner ih => exact .symm ih
  | trans left right ihLeft ihRight => exact .trans ihLeft ihRight
  | leftUnit f => exact nativeGK5AXSelectedLeftUnit f
  | rightUnit f => exact nativeGK5AXSelectedRightUnit f
  | assoc f g h => exact nativeGK5AXSelectedVerticalAssoc f g h

/-- Given exactly the three ORIGINAL primitive P89 certificates,
every finite source-vertical word descends to a GENUINE source
four-cell by an actual Type-valued word induction. -/
def NativeGK5AXSourceVerticalWord.toOriginal
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (data : NativeGK5AXVerticalPrimitiveCertificates first last)
    (w : NativeGK5AXSourceVerticalWord f g) :
    NativeF55P89InterchangeFourCell f g := by
  induction w with
  | refl f => exact .refl f
  | symm inner ih => exact .symm ih
  | trans left right ihLeft ihRight => exact .trans ihLeft ihRight
  | leftUnit f => exact data.leftUnit f
  | rightUnit f => exact data.rightUnit f
  | assoc f g h => exact data.assoc f g h

/-- The three selected vertical primitive families are all
P89-reflectable EXACTLY when there are no original-source
GK5AQ BadPairs among their actual source-typed generator pairs.
Backward direction chooses source witnesses; it does NOT assert
that the absence condition holds unconditionally. -/
theorem nativeGK5AXVerticalCertificates_iff_noPrimitiveBad
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Nonempty (NativeGK5AXVerticalPrimitiveCertificates first last) ↔
      (∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
        (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v),
        ¬ nativeGK5AQBadPair first last (.trans (.ident u) f) f) ∧
      (∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
        (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v),
        ¬ nativeGK5AQBadPair first last (.trans f (.ident v)) f) ∧
      (∀ {u v w z : KuuNativeF45Tree.DepthRotationRoute p first last}
        (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
        (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
        (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p w z),
        ¬ nativeGK5AQBadPair first last
          (.trans (.trans f g) h) (.trans f (.trans g h))) := by
  classical
  constructor
  · rintro ⟨cert⟩
    constructor
    · intro u v f bad
      exact bad.2 ⟨cert.leftUnit f⟩
    constructor
    · intro u v f bad
      exact bad.2 ⟨cert.rightUnit f⟩
    · intro u v w z f g h bad
      exact bad.2 ⟨cert.assoc f g h⟩
  · rintro ⟨hL, hR, hA⟩
    refine ⟨{
      leftUnit := ?_
      rightUnit := ?_
      assoc := ?_
    }⟩
    · intro u v f
      apply Classical.choice
      by_contra missing
      exact hL f ((nativeGK5AXLeftUnit_bad_iff_noP89 f).2 missing)
    · intro u v f
      apply Classical.choice
      by_contra missing
      exact hR f ((nativeGK5AXRightUnit_bad_iff_noP89 f).2 missing)
    · intro u v w z f g h
      apply Classical.choice
      by_contra missing
      exact hA f g h ((nativeGK5AXAssoc_bad_iff_noP89 f g h).2 missing)

/-- A genuine original vertical certificate record gives BOTH
the original P89 witness and the independently selected P94A
witness for each finite source-vertical four-proof word. -/
theorem NativeGK5AXSourceVerticalWord.both_witnesses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (data : NativeGK5AXVerticalPrimitiveCertificates first last)
    (w : NativeGK5AXSourceVerticalWord f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∧
    Nonempty (NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)) :=
  ⟨⟨w.toOriginal data⟩, ⟨w.toSelected⟩⟩

/-- In the restricted source-vertical word grammar, any original
P89 primitive reflection data precludes a GK5AQ BadPair. This
does not establish faithfulness of the full selected P94A syntax. -/
theorem NativeGK5AXSourceVerticalWord.not_bad
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (data : NativeGK5AXVerticalPrimitiveCertificates first last)
    (w : NativeGK5AXSourceVerticalWord f g) :
    ¬ nativeGK5AQBadPair first last f g := by
  intro bad
  exact bad.2 ⟨w.toOriginal data⟩

#print axioms nativeGK5AXSelectedLeftUnit
#print axioms nativeGK5AXSelectedRightUnit
#print axioms nativeGK5AXSelectedVerticalAssoc
#print axioms nativeGK5AXLeftUnit_bad_iff_noP89
#print axioms nativeGK5AXRightUnit_bad_iff_noP89
#print axioms nativeGK5AXAssoc_bad_iff_noP89
#print axioms NativeGK5AXVerticalPrimitiveCertificates
#print axioms NativeGK5AXSourceVerticalWord
#print axioms NativeGK5AXSourceVerticalWord.toSelected
#print axioms NativeGK5AXSourceVerticalWord.toOriginal
#print axioms nativeGK5AXVerticalCertificates_iff_noPrimitiveBad
#print axioms NativeGK5AXSourceVerticalWord.both_witnesses
#print axioms NativeGK5AXSourceVerticalWord.not_bad

end
end Kuu.F112.Physical
