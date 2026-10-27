import Kuu.F112.PolygonNativeC60ConservativeFreeRank

/-!
# F112-P94D3DA — original C60 double-symmetry descent obstruction

CZ proves that the complete original fifteen-dimensional conservative
Type-valued certificates symm^(n)(refl R) are pairwise distinct, even
after their genuine dependent sixteen-dimensional BC encoding. CY
identifies the WHOLE selected conservative strict isotropy group with
CN's free group of complete original parallel-generator certificates.

DA tests one geometrically natural but NOT previously added relation:
identify the true strict loops associated to symm^(n+2)(refl R)
and symm^n(refl R), at a fixed actual conservative C60 14D fiber and
independently chosen inner/outer finite AQ contexts.

For ANY separately supplied group-valued quotient/readout q making
those two strict loops equal, exact descent of the original CN
retraction is impossible. Nor can the injective complete BW strict
holonomy descend through q. These are precise conditional obstructions,
NOT assertions that such an extra geometric 16-cell exists. Original
14D/15D boundary witnesses, finite AQ histories, strict Kuu,
independent Kuu presentation status and all earlier no-go results
remain unchanged.

No new geometric relation, Gray, Peiffer, axiom, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDA vDA wDA uD vD uE vE

section GeneralDescentObstructions

variable {G : Type uDA} {H : Type vDA} {Q : Type wDA}
variable [Group G] [Group H] [Group Q]

/-- A true split retraction cannot descend along a map identifying
two different embedded source elements. This is a group-level result
about the ORIGINAL retraction, not a group constructed from observers. -/
theorem nativeC60DASplit_no_decoder_of_identification
    (r : G →* H) (i : H →* G)
    (hsplit : ∀ h : H, r (i h) = h)
    (q : G →* Q)
    (x y : H) (hne : x ≠ y)
    (hidentify : q (i x) = q (i y)) :
    ¬ ∃ decoder : Q →* H, decoder.comp q = r := by
  rintro ⟨decoder, hdecoder⟩
  have hx := DFunLike.congr_fun hdecoder (i x)
  have hy := DFunLike.congr_fun hdecoder (i y)
  change decoder (q (i x)) = r (i x) at hx
  change decoder (q (i y)) = r (i y) at hy
  rw [hsplit x] at hx
  rw [hsplit y] at hy
  have hcollapsed := congrArg decoder hidentify
  exact hne (hx.symm.trans (hcollapsed.trans hy))

/-- Any exact factorization of an INJECTIVE complete strict-holonomy
readout must distinguish every pair that this readout distinguishes.
A quotient that kills such a pair has a genuine descent obstruction. -/
theorem nativeC60DAFaithful_no_descent_of_identification
    {T : Type uDA} [Group T]
    (obs : G →* T) (faithful : Function.Injective obs)
    (q : G →* Q) {x y : G}
    (hne : x ≠ y) (hidentify : q x = q y) :
    ¬ ∃ descended : Q →* T, descended.comp q = obs := by
  rintro ⟨descended, hdescended⟩
  have hx := DFunLike.congr_fun hdescended x
  have hy := DFunLike.congr_fun hdescended y
  change descended (q x) = obs x at hx
  change descended (q y) = obs y at hy
  have hsame : obs x = obs y :=
    hx.symm.trans ((congrArg descended hidentify).trans hy)
  exact hne (faithful hsame)

end GeneralDescentObstructions

section OriginalPhysicalC60

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

/-- Two adjacent DOUBLE-SYMMETRY counts are different ORIGINAL
15D conservative proof terms. There is no imposed 15D inverse-cancellation
equality on this Type-valued grammar. -/
theorem nativeK5DADouble_symm_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (k : Nat) :
    nativeK5CZCore W R (k + 2) ≠ nativeK5CZCore W R k := by
  intro heq
  have hindex := congrArg (nativeK5CZCoreIndex W) heq
  rw [nativeK5CZCoreIndex_core, nativeK5CZCoreIndex_core] at hindex
  have hnat := Option.some.inj hindex
  omega

/-- Distinctness persists at the ORIGINAL complete dependent BC
sixteen-dimensional generators, even at identical 14D/15D boundaries. -/
theorem nativeK5DADouble_symm_generator_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) (k : Nat) :
    nativeK5CZGenerator W R inner (k + 2) ≠
      nativeK5CZGenerator W R inner k := by
  intro heq
  have hnat := nativeK5CZGenerator_injective W R inner heq
  omega

/-- The ACTUAL strict C60 loops associated with n+2 and n are
different even after ANY original finite outer AQ frame.
This uses CY's isomorphism with the true strict automorphism group. -/
theorem nativeK5DADouble_symm_strict_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (k : Nat) :
    nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of (k + 2)) ≠
      nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of k) := by
  intro heq
  have hfree := nativeK5CZFreeNatEmbed_injective W R inner outer heq
  have hnat := FreeGroup.of_injective hfree
  omega

/-- The concrete free Nat letter is EXACTLY the original CO embedding
of its corresponding proof-relevant CN generator. -/
theorem nativeK5DAFreeNat_of_original_letter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (k : Nat) :
    nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of k) =
      nativeC60COEmbed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)
        (FreeGroup.of (nativeK5CZLetter W R inner k)) := by
  change nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
      ((FreeGroup.map (nativeK5CZLetter W R inner)) (FreeGroup.of k)) =
    nativeC60COEmbed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner)
      (FreeGroup.of (nativeK5CZLetter W R inner k))
  rw [FreeGroup.map.of]

/-- Any supplied quotient that identifies the two original double-symm
strict loops loses the ACTUAL full CN decoder. This does not assert
that the hypothetical geometric quotient is already constructed. -/
theorem nativeK5DADouble_symm_no_CN_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (k : Nat)
    {Q : Type wDA} [Group Q]
    (quotient : NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) →* Q)
    (hidentify :
      quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of (k + 2))) =
        quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of k))) :
    ¬ ∃ decoder : Q →* FreeGroup
        (NativeC60CNForkAlphabet (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)),
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) := by
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let base := nativeK5CKAtomGenerator W R inner
  have hletters :
      (FreeGroup.of (nativeK5CZLetter W R inner (k + 2)) :
        FreeGroup (NativeC60CNForkAlphabet S F base)) ≠
      FreeGroup.of (nativeK5CZLetter W R inner k) := by
    intro h
    have hletter := FreeGroup.of_injective h
    have hnat := nativeK5CZLetter_injective W R inner hletter
    omega
  have hshift :
      quotient (nativeC60COEmbed S F outer base
          (FreeGroup.of (nativeK5CZLetter W R inner (k + 2)))) =
        quotient (nativeC60COEmbed S F outer base
          (FreeGroup.of (nativeK5CZLetter W R inner k))) := by
    rw [← nativeK5DAFreeNat_of_original_letter W R inner outer (k + 2),
      ← nativeK5DAFreeNat_of_original_letter W R inner outer k]
    exact hidentify
  exact nativeC60DASplit_no_decoder_of_identification
    (nativeC60CORetraction S F outer base)
    (nativeC60COEmbed S F outer base)
    (nativeC60CORetraction_embed S F outer base)
    quotient _ _ hletters hshift

/-- Since BW is already faithful on the WHOLE original strict isotropy,
identifying double symm strict loops also prevents exact descent of
their COMPLETE noncommutative sixteen-dimensional BW holonomy. -/
theorem nativeK5DADouble_symm_no_BW_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (k : Nat)
    {Q : Type wDA} [Group Q]
    (quotient : NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) →* Q)
    (hidentify :
      quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of (k + 2))) =
        quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of k))) :
    ¬ ∃ descended : Q →*
        FreeGroup (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)),
      descended.comp quotient =
        nativeC60COHolonomy (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) := by
  exact nativeC60DAFaithful_no_descent_of_identification
    (nativeC60COHolonomy (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    (nativeC60COHolonomy_injective
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    quotient (nativeK5DADouble_symm_strict_ne W R inner outer k) hidentify

/-- Exact CN preservation forces separation of the two ORIGINAL
double-symmetry strict loops. This is a conditional necessary
compatibility criterion for any independently chosen geometric
quotient, not a newly supplied geometric 16-cell. -/
theorem nativeK5DA_CN_descent_requires_double_symm_separation
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (k : Nat)
    {Q : Type wDA} [Group Q]
    (quotient : NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) →* Q)
    (hdecoder : ∃ decoder : Q →* FreeGroup
        (NativeC60CNForkAlphabet (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)),
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)) :
      quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of (k + 2))) ≠
        quotient (nativeK5CZFreeNatEmbed W R inner outer
          (FreeGroup.of k)) := by
  intro hidentify
  exact nativeK5DADouble_symm_no_CN_descent
    W R inner outer k quotient hidentify hdecoder

end OriginalPhysicalC60

#print axioms nativeC60DASplit_no_decoder_of_identification
#print axioms nativeC60DAFaithful_no_descent_of_identification
#print axioms nativeK5DADouble_symm_raw_ne
#print axioms nativeK5DADouble_symm_generator_ne
#print axioms nativeK5DADouble_symm_strict_ne
#print axioms nativeK5DAFreeNat_of_original_letter
#print axioms nativeK5DADouble_symm_no_CN_descent
#print axioms nativeK5DADouble_symm_no_BW_descent
#print axioms nativeK5DA_CN_descent_requires_double_symm_separation

end
end Kuu.F112.Physical
