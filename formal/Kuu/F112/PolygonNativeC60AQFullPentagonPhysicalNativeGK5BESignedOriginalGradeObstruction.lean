import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BDP77ClassLocalSeamDescent
import Mathlib.Tactic

/-!
F112-P94D3GK5BE — signed ORIGINAL-wrapper grade and a real
COUNTEREXAMPLE to the sufficiency of GK5BB unsigned count one
for local P94A raw-original → recursive-phi seams.

GK5BB counts original P92B wrappers without signs. We introduce
an independent Int-valued invariant: original=+1, refl=0,
assocNaturality=0, trans=addition, symm=integer NEGATION,
and all contexts preserve the grade. Both true P92B horizontal
composition and all sixteen P93C and nineteen P94A Type-valued
four-cell constructors preserve this integer grade.

Consequently original(F55.symm f) has grade +1, while recursive
phi(F55.symm f) has grade -1 whenever original f is a primitive
pentagon or disjointSquare. The two endpoints have the SAME
unsigned wrapper count ONE yet cannot be joined by ANY chosen
P94A four-cell. This is a strictly sharper obstruction than
the GK5BB unsigned count test, not a failure of search.

An ordinary original primitive pentagon has a direct reflexive
seam; its genuine original inverse has none even though its
two proposed P92B endpoints both carry one original wrapper.
For each genuine F54 source pair, the count-and-signed
necessity of a local seam descends as a positive/negative
property on actual P77 equivalence classes by GK5BD.

We do NOT assert that the combination (count=1,signed=1)
is sufficient, any global original→phi seam, constructor shell
kit, unconditional original-P89 class-map reflection, source
image hole elimination, or Gray reconstruction.

Strict 空 authority, independent Kuu→Qi, original F54
two-Nat/two-category/Blocks histories intact, append-only,
public root107, protected PR #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, admit, native_decide, or new axioms.
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

/-- Count the exact P92B ORIGINAL F55 wrapper constructor inside
the FULL Type-valued P92B three-proof, weighted by inversion.
An original wrapper has +1, an inverted subtree changes sign,
vertical and horizontal composition add, and F45/F54 contexts
preserve the integer. This is NOT the unsigned GK5BB count. -/
def NativeF55P92AssocComparison.gk5beSignedCount
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) : Int := by
  induction f with
  | original old => exact 1
  | assocNaturality u v w => exact 0
  | refl r => exact 0
  | symm f ih => exact -ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Exact vertical 3-proof computation; using the named lemma
avoids unfolding the dependent recursor inside interchange. -/
theorem NativeF55P92AssocComparison.gk5beTrans_count
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5beSignedCount =
      f.gk5beSignedCount + g.gk5beSignedCount := rfl

/-- Exact genuine P92B horizontal pasting: the signed original-wrapper grade
is additive in genuine dependent P92B horizontal composition. -/
theorem NativeF55P92AssocComparison.gk5beHorizontal_count
    {n₁ n₁' m₁ m₁' n₂ n₂' m₂ m₂' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5beSignedCount =
      f.gk5beSignedCount + g.gk5beSignedCount := rfl

/-- ALL SIXTEEN P93C constructors preserve the signed integer
original-wrapper grade. Old P89 compares two +1 original wrappers,
regardless of the internal F55 proof syntax. Interchange is
compatible because addition in Int is commutative. -/
theorem NativeF55P93AssocFourCell.gk5beSignedCount_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5beSignedCount = g.gk5beSignedCount := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Int) + f.gk5beSignedCount = f.gk5beSignedCount
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5beSignedCount + (0 : Int) = f.gk5beSignedCount
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5beSignedCount + g.gk5beSignedCount) +
        h.gk5beSignedCount =
        f.gk5beSignedCount + (g.gk5beSignedCount + h.gk5beSignedCount)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Int => prior.gk5beSignedCount + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Int => z + suffix.gk5beSignedCount) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5beHorizontal_count] using
        congrArg (fun z : Int => z + other.gk5beSignedCount) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5beHorizontal_count] using
        congrArg (fun z : Int => other.gk5beSignedCount + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5beHorizontal_count,
        NativeF55P92AssocComparison.gk5beTrans_count]
      omega

/-- ALL NINETEEN chosen P94A four-cell constructors preserve this
SIGNED grade, including horizontalUnit and both contextUnit
additions. This is independent of GK5BB's unsigned count. -/
theorem NativeF55P94UnitFourCell.gk5beSignedCount_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5beSignedCount = g.gk5beSignedCount := by
  induction w with
  | old w => exact w.gk5beSignedCount_sound
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Int) + f.gk5beSignedCount = f.gk5beSignedCount
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5beSignedCount + (0 : Int) = f.gk5beSignedCount
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5beSignedCount + g.gk5beSignedCount) +
        h.gk5beSignedCount =
        f.gk5beSignedCount + (g.gk5beSignedCount + h.gk5beSignedCount)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Int => prior.gk5beSignedCount + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Int => z + suffix.gk5beSignedCount) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5beHorizontal_count] using
        congrArg (fun z : Int => z + other.gk5beSignedCount) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5beHorizontal_count] using
        congrArg (fun z : Int => other.gk5beSignedCount + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5beHorizontal_count,
        NativeF55P92AssocComparison.gk5beTrans_count]
      omega
  | horizontalUnit u v =>
      change (0 : Int) + 0 = 0
      omega
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl


/-- A raw original F55 three-proof always has signed grade +1,
regardless of the internal source constructor or orientation. -/
theorem nativeGK5BEOriginal_signed_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (NativeF55P92AssocComparison.original f).gk5beSignedCount = 1 := rfl

/-- P92B inversion negates the signed ORIGINAL grade. -/
theorem NativeF55P92AssocComparison.gk5beSymm_signed
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (NativeF55P92AssocComparison.symm f).gk5beSignedCount =
      - f.gk5beSignedCount := rfl

/-- Recursive phi commutes DEFINITIONALLY with original F55
three-proof inversion, preserving the dependent F54 endpoints. -/
theorem nativeGK5BEPhiSymm_signed
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeGK5AIOriginalToP92Structural (.symm f)).gk5beSignedCount =
      -(nativeGK5AIOriginalToP92Structural f).gk5beSignedCount := rfl

/-- Any actual local original→recursive-phi P94A seam must have
BOTH unsigned count 1 and SIGNED count +1 at the chosen phi
endpoint. This implication uses full Type-valued 4-cell soundness. -/
theorem nativeGK5BENecessary_unsigned_and_signed
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount = 1 := by
  have hu := bridge.gk5bbOriginalCount_sound
  have hs := bridge.gk5beSignedCount_sound
  change (1 : Nat) = _ at hu
  change (1 : Int) = _ at hs
  exact ⟨hu.symm, hs.symm⟩

/-- New obstruction, independent of unsigned wrapper count:
phi's signed grade different from +1 refutes every P94A
direct local seam, without using a missing trans shell. -/
theorem nativeGK5BENoSeam_if_signed_ne_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (hole : (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount ≠ 1) :
    ¬ Nonempty (nativeGK5AZSeamAt f) := by
  rintro ⟨bridge⟩
  exact hole (nativeGK5BENecessary_unsigned_and_signed f bridge).2

/-- An arbitrary original F55 source whose phi grade equals
+1 has a reverse original source with phi grade -1.
Hence its inverse has NO local original→phi P94A seam,
without requiring any special constructor shell. -/
theorem nativeGK5BEInverse_of_positive_phi_no_seam
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (hphi : (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount = 1) :
    ¬ Nonempty (nativeGK5AZSeamAt (.symm f)) := by
  apply nativeGK5BENoSeam_if_signed_ne_one (.symm f)
  rw [nativeGK5BEPhiSymm_signed f, hphi]
  omega

/-- Genuine original north-C60 pentagon has raw grade +1,
whereas the selected phi of its INVERSE has signed grade -1. -/
theorem nativeGK5BENorthInverse_signed_split :
    ((NativeF55P92AssocComparison.original
      (.symm nativeGK5AGNorthOriginalCell)).gk5beSignedCount = 1) ∧
    ((nativeGK5AIOriginalToP92Structural
      (.symm nativeGK5AGNorthOriginalCell)).gk5beSignedCount = -1) := by
  constructor <;> rfl

/-- But BOTH endpoints of the actual north pentagon-inverse
direct seam candidate have the SAME GK5BB unsigned count one.
This is an equality of observations, not an actual seam. -/
theorem nativeGK5BENorthInverse_unsigned_equal :
    (NativeF55P92AssocComparison.original
      (.symm nativeGK5AGNorthOriginalCell)).gk5bbOriginalCount =
    (nativeGK5AIOriginalToP92Structural
      (.symm nativeGK5AGNorthOriginalCell)).gk5bbOriginalCount := rfl

/-- A REAL counterexample: BOTH raw/phi endpoints carry ONE
original wrapper, but a chosen P94A seam is IMPOSSIBLE because
the stronger signed original-wrapper grade is +1 vs -1. -/
theorem nativeGK5BENorthInverse_count_one_but_no_seam :
    ((NativeF55P92AssocComparison.original
      (.symm nativeGK5AGNorthOriginalCell)).gk5bbOriginalCount =
    (nativeGK5AIOriginalToP92Structural
      (.symm nativeGK5AGNorthOriginalCell)).gk5bbOriginalCount) ∧
    ¬ Nonempty (nativeGK5AZSeamAt (.symm nativeGK5AGNorthOriginalCell)) :=
  ⟨nativeGK5BENorthInverse_unsigned_equal,
    nativeGK5BENoSeam_if_signed_ne_one _
      (by
        change (-1 : Int) ≠ 1
        omega)⟩

/-- This confirms that GK5BB's unsigned necessary condition is
STRICTLY weaker than a genuine local seam: its converse fails
at one actual nontrivial north C60 original F55 inverse. -/
theorem nativeGK5BEUnsigned_one_not_sufficient :
    ¬ (∀ {r s : KuuNativeF45Tree.DepthRotationRoute
          (.pentagon .north)
          (KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
            northNativeF45SecondStage northNativeF45ThirdStage
            northNativeF45FourthStage)
          (KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
            northNativeF45SecondStage northNativeF45ThirdStage
            northNativeF45FourthStage)},
        (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
          (.pentagon .north) r s) →
        (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount = 1 →
        Nonempty (nativeGK5AZSeamAt f)) := by
  intro h
  have hw : (nativeGK5AIOriginalToP92Structural
      (.symm nativeGK5AGNorthOriginalCell)).gk5bbOriginalCount = 1 := rfl
  exact nativeGK5BENorthInverse_count_one_but_no_seam.2
    (h (.symm nativeGK5AGNorthOriginalCell) hw)

/-- The entire genuine P77 finite orbit of the actual north
inverse is negative, even though the unsigned wrapper counts
at its seed are equal. This uses GK5BD's finite-word proof
transport, not a shadow equality. -/
theorem nativeGK5BENorthInverseP77Word_no_seam
    {target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) northNativeF45PentagonShort northNativeF45PentagonLong}
    (w : NativeGK5BDP77Word
      (KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (.symm nativeGK5AGNorthOriginalCell) target) :
    ¬ Nonempty (nativeGK5AZSeamAt target) := by
  rintro ⟨bridge⟩
  exact nativeGK5BENorthInverse_count_one_but_no_seam.2
    ⟨nativeGK5BCSeam_transport_P77 w.toP77 bridge⟩

#print axioms NativeF55P92AssocComparison.gk5beSignedCount
#print axioms NativeF55P92AssocComparison.gk5beTrans_count
#print axioms NativeF55P92AssocComparison.gk5beHorizontal_count
#print axioms NativeF55P93AssocFourCell.gk5beSignedCount_sound
#print axioms NativeF55P94UnitFourCell.gk5beSignedCount_sound
#print axioms nativeGK5BEOriginal_signed_one
#print axioms NativeF55P92AssocComparison.gk5beSymm_signed
#print axioms nativeGK5BEPhiSymm_signed
#print axioms nativeGK5BENecessary_unsigned_and_signed
#print axioms nativeGK5BENoSeam_if_signed_ne_one
#print axioms nativeGK5BEInverse_of_positive_phi_no_seam
#print axioms nativeGK5BENorthInverse_signed_split
#print axioms nativeGK5BENorthInverse_unsigned_equal
#print axioms nativeGK5BENorthInverse_count_one_but_no_seam
#print axioms nativeGK5BEUnsigned_one_not_sufficient
#print axioms nativeGK5BENorthInverseP77Word_no_seam

end
end Kuu.F112.Physical
