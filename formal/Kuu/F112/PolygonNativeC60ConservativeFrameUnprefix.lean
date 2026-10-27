import Kuu.F112.PolygonNativeC60OriginalTypedPairNormalization

/-!
# F112-P94D3CX — physical conservative finite-AQ generator unprefix

CW2 extracts complete original typed parallel-pair normal forms at every
genuine C60 conservative two-boundary sector. CX uses CT/CU's original
14D endpoint rigidity and CJ's exact finite-context word uniqueness to
prove that EVERY ORIGINAL framed parallel BC generator at the fixed
physical conservative endpoints is the actual shift of an ORIGINAL
unframed BC generator. Original AX primitive certificates, both 14D
endpoints, the underlying 15D Type-valued witnesses and finite words
remain unchanged.

The resulting exact pair-level finite-AQ free-word covariance connects
CW2's complete original signed normal form with CN's split decoder.
This is a theorem about the SELECTED no-extra-relations strict Kuu
presentation; it introduces no new geometric 16-cell, no Gray category,
no Peiffer or global n/∞-descent and no new axiom.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCX uD vD uE vE

section GenericPairFrames

variable {L : NativeC60AXLayer.{uCX}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- True finite context on each exact original 16D parallel-generator
pair. Each shifted generator still carries its full dependent witness. -/
def nativeC60CXFramePairs (outer : List Bool) {A B : L.Total}
    (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B)) :
    List ((nativeC60BCClosedSignature S F).Gen
      (nativeC60BCContextTotal F outer A)
      (nativeC60BCContextTotal F outer B) ×
      (nativeC60BCClosedSignature S F).Gen
      (nativeC60BCContextTotal F outer A)
      (nativeC60BCContextTotal F outer B)) :=
  pairs.map (fun gh =>
    (nativeC60BCShiftGen S F outer gh.1,
     nativeC60BCShiftGen S F outer gh.2))

/-- Noncommutative BW covariance for EVERY original typed finite pair
chain. No comparison is replaced with code data: code appears only in
the statement of its exact strict holonomy. -/
theorem nativeC60CXFramePairs_holonomy (outer : List Bool)
    {A B : L.Total}
    (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B)) :
    nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F
          (nativeC60CWPairChain S F (nativeC60CXFramePairs S F outer pairs))) =
      nativeC60BWFreePrefix S outer
        (nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F (nativeC60CWPairChain S F pairs))) := by
  induction pairs with
  | nil =>
      change (1 : FreeGroup (NativeC60BVGeneratorCode S)) =
        nativeC60BWFreePrefix S outer 1
      simp
  | cons gh rest ih =>
      rcases gh with ⟨g, h⟩
      simp only [nativeC60CXFramePairs, List.map_cons]
      rw [nativeC60CWPairChain_holonomy_cons S F
            (nativeC60BCShiftGen S F outer g)
            (nativeC60BCShiftGen S F outer h) _,
          nativeC60CWPairChain_holonomy_cons S F g h rest,
          map_mul, ih]
      simp only [nativeC60BVGeneratorCode_shift, nativeC60BWFreePrefix,
        FreeGroup.map.of, nativeC60BWCodePrefix, map_mul, map_inv]

/-- If every framed original 16D primitive has an original typed
unframed witness, finite lists of parallel pairs have a COMPLETE lift,
not merely a free-group code factorization. -/
theorem nativeC60CXFramePairs_surjective_of_generators
    (outer : List Bool) {A B : L.Total}
    (hlift : ∀ g : (nativeC60BCClosedSignature S F).Gen
        (nativeC60BCContextTotal F outer A)
        (nativeC60BCContextTotal F outer B),
      ∃ g0 : (nativeC60BCClosedSignature S F).Gen A B,
        nativeC60BCShiftGen S F outer g0 = g)
    (pairs : List ((nativeC60BCClosedSignature S F).Gen
        (nativeC60BCContextTotal F outer A)
        (nativeC60BCContextTotal F outer B) ×
      (nativeC60BCClosedSignature S F).Gen
        (nativeC60BCContextTotal F outer A)
        (nativeC60BCContextTotal F outer B))) :
    ∃ q : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B),
      nativeC60CXFramePairs S F outer q = pairs := by
  induction pairs with
  | nil => exact ⟨[], rfl⟩
  | cons gh rest ih =>
      rcases gh with ⟨g, h⟩
      obtain ⟨g0, hg0⟩ := hlift g
      obtain ⟨h0, hh0⟩ := hlift h
      obtain ⟨q, hq⟩ := ih
      refine ⟨(g0, h0) :: q, ?_⟩
      change
        (nativeC60BCShiftGen S F outer g0,
          nativeC60BCShiftGen S F outer h0) ::
          nativeC60CXFramePairs S F outer q = (g, h) :: rest
      rw [hg0, hh0, hq]

end GenericPairFrames

section PhysicalConservativeRecovery

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

/-- The actual positive conservative generator makes the two framed
fifteen-dimensional endpoints unequal: otherwise CJ's adjacent-positive
no-go would be violated by using that generator twice. -/
theorem nativeK5CXFramed_conservative_endpoints_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) ≠
      nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) := by
  intro h
  have g : (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :=
    h ▸ nativeK5CVFramedBase W R inner outer
  exact nativeK5CVFramed_no_outgoing_target W R inner outer g

/-- CORE GEOMETRIC LIFT. For ANY original positive BC generator between
the genuine outer-framed conservative source and target, recover an
UNFRAMED original generator with exactly the SAME independent AX
primitive certificate, original 14D boundaries, 15D raw witness and
finite inner AQ history. CT/CJ force the frame index to be outer++inner;
CT/CU preserve the source/target of the conservative input. -/
theorem nativeK5CXFramed_conservative_generator_unprefix
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (g : (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))) :
    ∃ g0 : (nativeK5BCSignature W).Gen
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)),
      nativeC60BCShiftGen (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer g0 = g := by
  rcases g with ⟨ys, a, b, ⟨gen, hxa, hyb⟩⟩
  rcases gen with ⟨R', S', other, hfrom, hto⟩
  have hsource :
      nativeK5CHSource W (outer ++ inner) (nativeK5CKConservativeRefl W R) =
        nativeK5CHSource W ys other := by
    calc
      _ = nativeK5BCContext W outer
            (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) :=
          (nativeK5CUPhysical_source_frame_append W inner outer
            (nativeK5CKConservativeRefl W R)).symm
      _ = nativeK5BCContext W ys a := hxa
      _ = nativeK5BCContext W ys
            (nativeK5AXPack W (nativeK5AUNaturalityViaSource W other)) :=
          congrArg (nativeK5BCContext W ys) hfrom
      _ = _ := rfl
  have hcon : nativeK5CHOuterConservative W other = true := by
    have h := nativeK5CTSource_eq_forces_outer W
      (outer ++ inner) ys (nativeK5CKConservativeRefl W R) other hsource
    exact h.symm
  obtain ⟨hw, hR, hS⟩ :=
    nativeK5CTSource_eq_forces_word_and_endpoints W
      (outer ++ inner) ys (nativeK5CKConservativeRefl W R) other hsource
  subst ys
  subst R'
  subst S'
  have ha0 :
      nativeK5CHSource W inner (nativeK5CKConservativeRefl W R) =
        nativeK5BCContext W inner a := by
    calc
      _ = nativeK5CHSource W inner other :=
        nativeK5CUConservative_source_independent W inner
          (nativeK5CKConservativeRefl W R) other (by rfl) hcon
      _ = nativeK5BCContext W inner
            (nativeK5AXPack W (nativeK5AUNaturalityViaSource W other)) := rfl
      _ = nativeK5BCContext W inner a :=
        congrArg (nativeK5BCContext W inner) hfrom.symm
  have hb0 :
      nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R) =
        nativeK5BCContext W inner b := by
    calc
      _ = nativeK5CHTarget W inner other :=
        nativeK5CTConservative_target_independent W inner
          (nativeK5CKConservativeRefl W R) other (by rfl) hcon
      _ = nativeK5BCContext W inner
            (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W other)) := rfl
      _ = nativeK5BCContext W inner b :=
        congrArg (nativeK5BCContext W inner) hto.symm
  let original : (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) :=
    ⟨inner, a, b, ⟨⟨R, R, other, hfrom, hto⟩, ha0, hb0⟩⟩
  refine ⟨original, ?_⟩
  apply nativeC60BVGeneratorCode_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
  rw [nativeC60BVGeneratorCode_shift]
  rfl

/-- True physical completeness of finite-AQ unprefix at this actual
conservative strict isotropy base. Proof witnesses first normalize by
CW2, then every individual primitive is genuinely unframed by CT/CU/CJ.
No scalar observer or graph surrogate is used. -/
theorem nativeK5CXPhysical_outer_pair_codes_complete
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    NativeC60CWOuterPairCodeComplete
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) := by
  intro path
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let cert := nativeK5CVAll_finite_signed_gauge_sector
    W R inner outer path (PSum.inl rfl)
  obtain ⟨framed, hframed⟩ :=
    cert.closedSource_pairs S F
      (nativeK5CXFramed_conservative_endpoints_ne W R inner outer)
  obtain ⟨original, horiginal⟩ :=
    nativeC60CXFramePairs_surjective_of_generators S F outer
      (fun g => nativeK5CXFramed_conservative_generator_unprefix W R inner outer g)
      framed
  refine ⟨original, ?_⟩
  calc
    FreeGroup.mk (nativeC60CAChainSignedCodes S F path) =
        nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F path) :=
      (nativeC60CAChain_holonomy S F path).symm
    _ = nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F
            (nativeC60CWPairChain S F
              (nativeC60CXFramePairs S F outer original))) := by
        rw [← hframed, horiginal]
    _ = nativeC60BWFreePrefix S outer
          (nativeC60BWFreeHolonomy S F
            (nativeC60CAChainStep S F (nativeC60CWPairChain S F original))) :=
      nativeC60CXFramePairs_holonomy S F outer original

/-- The actual CP kernel disappears at the conservative strict
isotropy sector in the SELECTED no-extra-relations presentation.
This follows from true Type-valued physical unprefix and CW's
noncommutative CN reconstruction; no identification with the BW kernel
or with any unconstructed geometric 16D quotient is performed. -/
theorem nativeK5CXPhysical_strict_kernel_trivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    ¬ ∃ k : NativeC60CPKernel
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner), k ≠ 1 :=
  nativeC60CWStrict_kernel_trivial_of_outer_pair_codes
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner)
    (nativeK5CXPhysical_outer_pair_codes_complete W R inner outer)

end PhysicalConservativeRecovery

#print axioms nativeC60CXFramePairs
#print axioms nativeC60CXFramePairs_holonomy
#print axioms nativeC60CXFramePairs_surjective_of_generators
#print axioms nativeK5CXFramed_conservative_endpoints_ne
#print axioms nativeK5CXFramed_conservative_generator_unprefix
#print axioms nativeK5CXPhysical_outer_pair_codes_complete
#print axioms nativeK5CXPhysical_strict_kernel_trivial

end
end Kuu.F112.Physical
