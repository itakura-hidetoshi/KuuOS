import Kuu.F112.PolygonNativeC60ExactCNBWDescentClassification

/-!
# F112-P94D3DC — exact partial gauge descent and a genuine coarse C60 quotient

DB proves complete CN/BW decoding descends through a surjective strict
group quotient iff that quotient is injective. DC distinguishes this
FULL information from genuine PARTIAL group-valued invariants.

First, for ANY surjective group homomorphism q : G →* Q, an ORIGINAL
group-valued invariant f : G →* T descends to Q iff it is constant
on exact q-fibers, iff ker q ≤ ker f. No new observational equivalence
is built into the ORIGINAL strict category.

Second, at every original conservative C60 proof-bearing 15D object
with independent finite inner/outer AQ histories, the fully retained
original BC generator code permits a COARSE parity presentation of the
actual original symm-depth. Mapping every genuine CN generator to
its Bool parity extends to an actual surjective group homomorphism
from the WHOLE strict isotropy into FreeGroup Bool.

This is a nontrivial free rank-two group-valued PARTIAL observable:
it separates the genuine original n=0 and n=1 strict loops but
identifies n with n+2. It therefore cannot retain the ORIGINAL FULL
CN retraction or BW holonomy (DA/DB), although its OWN coarse phase
descends. It is a selected strict/presentation-level quotient, NOT
a claimed physical geometric 16-cell or a quotient of the original
14D/15D Type-valued proof witnesses.

Keep strict Kuu, independent Kuu as one presentation, full original
history/authority boundaries, no Gray, new geometric relations,
new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDC vDC wDC tDC uD vD uE vE

section GenericPartialDescent

variable {G : Type uDC} {Q : Type vDC} {T : Type wDC}
variable [Group G] [Group Q] [Group T]

/-- A faithful distinction is not necessary for PARTIAL descent:
the exact condition is equality of f-values along every q-fiber. -/
def NativeC60DCFiberCompatible (q : G →* Q) (f : G →* T) : Prop :=
  ∀ x y : G, q x = q y → f x = f y

/-- Even without surjectivity, a genuinely descended original
observable is necessarily constant on every actual quotient fiber. -/
theorem nativeC60DCDescent_implies_fiber
    (q : G →* Q) (f : G →* T)
    (hdesc : ∃ descended : Q →* T, descended.comp q = f) :
    NativeC60DCFiberCompatible q f := by
  obtain ⟨descended, hdescended⟩ := hdesc
  intro x y hq
  have hx := DFunLike.congr_fun hdescended x
  have hy := DFunLike.congr_fun hdescended y
  change descended (q x) = f x at hx
  change descended (q y) = f y at hy
  exact hx.symm.trans ((congrArg descended hq).trans hy)

/-- Exact q-fiber compatibility has the ORIGINAL group-kernel criterion,
without forgetting any original strict arrows or postulating a quotient. -/
theorem nativeC60DCFiber_iff_kernel_le
    (q : G →* Q) (f : G →* T) :
    NativeC60DCFiberCompatible q f ↔ q.ker ≤ f.ker := by
  constructor
  · intro h z hz
    apply (MonoidHom.mem_ker).mpr
    have hq : q z = q (1 : G) := by
      simpa only [map_one] using (MonoidHom.mem_ker).mp hz
    have hf := h z 1 hq
    simpa only [map_one] using hf
  · intro h x y hxy
    have hmem : x * y⁻¹ ∈ q.ker := by
      apply (MonoidHom.mem_ker).mpr
      rw [map_mul, map_inv, hxy, mul_inv_cancel]
    have hf : f x * (f y)⁻¹ = 1 := by
      have hzero := (MonoidHom.mem_ker).mp (h hmem)
      simpa only [map_mul, map_inv] using hzero
    calc
      f x = (f x * (f y)⁻¹) * f y := by group
      _ = 1 * f y := by rw [hf]
      _ = f y := one_mul _

/-- Surjectivity makes compatibility SUFFICIENT: choose one genuine
preimage in the existing group, and prove the resulting function
respects unit and multiplication by original fiber compatibility. -/
def nativeC60DCFiberDecoder
    (q : G →* Q) (hq : Function.Surjective q)
    (f : G →* T) (h : NativeC60DCFiberCompatible q f) :
    Q →* T := by
  classical
  let rep : Q → G := fun z => Classical.choose (hq z)
  have hrep (z : Q) : q (rep z) = z :=
    Classical.choose_spec (hq z)
  exact {
    toFun := fun z => f (rep z)
    map_one' := by
      have hh : q (rep 1) = q (1 : G) := by
        calc
          q (rep 1) = 1 := hrep 1
          _ = q (1 : G) := (map_one q).symm
      exact (h _ _ hh).trans (map_one f)
    map_mul' := by
      intro x y
      have hh : q (rep (x * y)) = q (rep x * rep y) := by
        calc
          q (rep (x * y)) = x * y := hrep (x * y)
          _ = q (rep x) * q (rep y) := by rw [hrep x, hrep y]
          _ = q (rep x * rep y) := (map_mul q _ _).symm
      calc
        f (rep (x * y)) = f (rep x * rep y) := h _ _ hh
        _ = f (rep x) * f (rep y) := map_mul f _ _
  }

/-- The constructed PARTIAL decoder exactly reproduces the original
observable on every actual strict group element. -/
theorem nativeC60DCFiberDecoder_comp
    (q : G →* Q) (hq : Function.Surjective q)
    (f : G →* T) (h : NativeC60DCFiberCompatible q f) :
    (nativeC60DCFiberDecoder q hq f h).comp q = f := by
  classical
  apply MonoidHom.ext
  intro x
  change f (Classical.choose (hq (q x))) = f x
  apply h
  exact Classical.choose_spec (hq (q x))

/-- MAIN DC CLASSIFICATION. For a surjective strict group quotient,
the possible partial invariants are EXACTLY those whose original
kernel contains the quotient kernel. No demand that f be faithful. -/
theorem nativeC60DCPartial_descent_iff_kernel
    (q : G →* Q) (hq : Function.Surjective q) (f : G →* T) :
    (∃ descended : Q →* T, descended.comp q = f) ↔
      q.ker ≤ f.ker := by
  constructor
  · intro hdesc
    exact (nativeC60DCFiber_iff_kernel_le q f).mp
      (nativeC60DCDescent_implies_fiber q f hdesc)
  · intro hker
    have hcompat : NativeC60DCFiberCompatible q f :=
      (nativeC60DCFiber_iff_kernel_le q f).mpr hker
    exact ⟨nativeC60DCFiberDecoder q hq f hcompat,
      nativeC60DCFiberDecoder_comp q hq f hcompat⟩

/-- A surjective quotient has a unique decoder of a chosen PARTIAL
invariant when one exists. In particular the descended invariant is
not a choice of geometric 16D filler. -/
theorem nativeC60DCPartial_decoder_unique
    (q : G →* Q) (hq : Function.Surjective q)
    (f : G →* T)
    (d e : Q →* T)
    (hd : d.comp q = f) (he : e.comp q = f) : d = e :=
  nativeC60DBSurjective_decoder_unique f q hq d e hd he

end GenericPartialDescent

section PhysicalParityQuotient

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- A PARTIAL two-valued classification of ORIGINAL conservative
symm-depth from its COMPLETE original sixteen-dimensional code.
All other ORIGINAL proof certificates go to false. This is a
presentation-level function, not a quotient equality of 15D proofs. -/
def nativeK5DCLetterParity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner : List Bool) :
    NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner) → Bool :=
  fun i =>
    match nativeK5CZCodeIndex W
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) i.val) with
    | some n => decide (n % 2 = 1)
    | none => false

/-- Exact original proof-provenance parity for every infinitely many
CZ generators; no use of integer charge or Peiffer shadows. -/
theorem nativeK5DCLetterParity_CZ
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner : List Bool)
    (n : Nat) :
    nativeK5DCLetterParity W R inner (nativeK5CZLetter W R inner n) =
      decide (n % 2 = 1) := by
  change
    (match nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CZGenerator W R inner n)) with
      | some k => decide (k % 2 = 1)
      | none => false) = decide (n % 2 = 1)
  rw [nativeK5CZCodeIndex_generator]

/-- The two coarse parity classes both have ACTUAL original C60
proof-bearing generator representatives. -/
theorem nativeK5DCLetterParity_surjective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner : List Bool) :
    Function.Surjective (nativeK5DCLetterParity W R inner) := by
  intro b
  cases b with
  | false =>
      refine ⟨nativeK5CZLetter W R inner 0, ?_⟩
      simpa using nativeK5DCLetterParity_CZ W R inner 0
  | true =>
      refine ⟨nativeK5CZLetter W R inner 1, ?_⟩
      simpa using nativeK5DCLetterParity_CZ W R inner 1

/-- A REAL group-valued coarse readout of the WHOLE original strict
C60 conservative isotropy. The target is the FREE NONCOMMUTATIVE group
on two letters, rather than a commutative charge or a newly declared
geometric 16D category. -/
def nativeK5DCParityQuotient
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DBIsotropy W R inner outer →* FreeGroup Bool :=
  (FreeGroup.map (nativeK5DCLetterParity W R inner)).comp
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))

/-- Exact coarse gauge value of EVERY original countable conservative
strict generator, preserving its inner/outer original AQ histories
until the final explicitly declared projection. -/
theorem nativeK5DCParityQuotient_CZ
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (n : Nat) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) =
      FreeGroup.of (decide (n % 2 = 1)) := by
  rw [nativeK5DAFreeNat_of_original_letter W R inner outer n]
  change
    (FreeGroup.map (nativeK5DCLetterParity W R inner))
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
        (nativeC60COEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
          (FreeGroup.of (nativeK5CZLetter W R inner n)))) =
      FreeGroup.of (decide (n % 2 = 1))
  rw [nativeC60CORetraction_embed, FreeGroup.map.of,
    nativeK5DCLetterParity_CZ]

/-- Both true and false gauge-sector letters survive: q is SURJECTIVE
onto the full noncommutative two-letter free group. -/
theorem nativeK5DCParityQuotient_surjective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    Function.Surjective (nativeK5DCParityQuotient W R inner outer) := by
  intro y
  obtain ⟨x, hx⟩ :=
    (FreeGroup.map_surjective (nativeK5DCLetterParity_surjective W R inner)) y
  refine ⟨nativeC60COEmbed (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) x, ?_⟩
  change
    FreeGroup.map (nativeK5DCLetterParity W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
        (nativeC60COEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) x)) = y
  rw [nativeC60CORetraction_embed]
  exact hx

/-- Distinct 15D proof certificates of symm-depth n and n+2 have
the SAME deliberately coarse free-group parity image. -/
theorem nativeK5DCParityQuotient_double_symm_equal
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (n : Nat) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of (n + 2))) =
      nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) := by
  rw [nativeK5DCParityQuotient_CZ, nativeK5DCParityQuotient_CZ]
  have h : (n + 2) % 2 = n % 2 := by omega
  rw [h]

/-- This is an actual PROPER strict GROUP quotient: its two-loop
identification is witnessed by original, provably distinct full
C60 proof-bearing strict automorphisms. -/
theorem nativeK5DCParityQuotient_not_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    ¬ Function.Injective (nativeK5DCParityQuotient W R inner outer) := by
  intro hinj
  exact nativeK5DADouble_symm_strict_ne W R inner outer 0
    (hinj (nativeK5DCParityQuotient_double_symm_equal W R inner outer 0))

/-- Nevertheless the n=0 and n=1 independent original strict
generators remain distinguishable after the partial projection. -/
theorem nativeK5DCParityQuotient_separates_0_1
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 0)) ≠
      nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of 1)) := by
  intro h
  rw [nativeK5DCParityQuotient_CZ, nativeK5DCParityQuotient_CZ] at h
  have hb : (false : Bool) = true := FreeGroup.of_injective h
  cases hb

/-- This chosen PARTIAL gauge observable genuinely descends across
its own strict group quotient. The full original CN decoder does not. -/
theorem nativeK5DCParity_observable_descends
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    ∃ descended : FreeGroup Bool →* FreeGroup Bool,
      descended.comp (nativeK5DCParityQuotient W R inner outer) =
        nativeK5DCParityQuotient W R inner outer := by
  refine ⟨MonoidHom.id (FreeGroup Bool), ?_⟩
  apply MonoidHom.ext
  intro x
  rfl

/-- DB/DA give the precise cost of this ACTUAL non-injective coarse
group projection: the full ORIGINAL CN retraction cannot descend. -/
theorem nativeK5DCParity_no_full_CN_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    ¬ ∃ decoder : FreeGroup Bool →* nativeK5DBForkFree W R inner,
      decoder.comp (nativeK5DCParityQuotient W R inner outer) =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) := by
  intro hdesc
  exact nativeK5DCParityQuotient_not_injective W R inner outer
    ((nativeK5DBPhysical_CN_descent_iff_injective W R inner outer
      (nativeK5DCParityQuotient W R inner outer)
      (nativeK5DCParityQuotient_surjective W R inner outer)).mp hdesc)

/-- The original COMPLETE noncommutative BW provenance also cannot
descend through the SAME partial parity projection. No comparison
between the CN-kernel and a separately chosen BW observer kernel is
silently asserted. -/
theorem nativeK5DCParity_no_full_BW_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    ¬ ∃ descended : FreeGroup Bool →*
        FreeGroup (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)),
      descended.comp (nativeK5DCParityQuotient W R inner outer) =
        nativeC60COHolonomy (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) := by
  intro hdesc
  exact nativeK5DCParityQuotient_not_injective W R inner outer
    ((nativeK5DBPhysical_BW_descent_iff_injective W R inner outer
      (nativeK5DCParityQuotient W R inner outer)
      (nativeK5DCParityQuotient_surjective W R inner outer)).mp hdesc)

end PhysicalParityQuotient

#print axioms NativeC60DCFiberCompatible
#print axioms nativeC60DCDescent_implies_fiber
#print axioms nativeC60DCFiber_iff_kernel_le
#print axioms nativeC60DCFiberDecoder
#print axioms nativeC60DCFiberDecoder_comp
#print axioms nativeC60DCPartial_descent_iff_kernel
#print axioms nativeC60DCPartial_decoder_unique
#print axioms nativeK5DCLetterParity
#print axioms nativeK5DCLetterParity_CZ
#print axioms nativeK5DCLetterParity_surjective
#print axioms nativeK5DCParityQuotient
#print axioms nativeK5DCParityQuotient_CZ
#print axioms nativeK5DCParityQuotient_surjective
#print axioms nativeK5DCParityQuotient_double_symm_equal
#print axioms nativeK5DCParityQuotient_not_injective
#print axioms nativeK5DCParityQuotient_separates_0_1
#print axioms nativeK5DCParity_observable_descends
#print axioms nativeK5DCParity_no_full_CN_descent
#print axioms nativeK5DCParity_no_full_BW_descent

end
end Kuu.F112.Physical
