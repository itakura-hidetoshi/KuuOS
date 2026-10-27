import Kuu.F112.PolygonNativeC60PartialGaugeDescentParity

/-!
# F112-P94D3DD — finite AQ transport and naturality of partial C60 gauge parity

DC constructs the original, non-injective parity quotient of the genuine
conservative strict 15D isotropy. DD keeps the original 14D/15D endpoints,
the complete BC/CN generator and BW sixteen-dimensional evidence, and
independent finite inner and outer AQ words.

On an UNCHANGED original inner 15D proof boundary, the genuine strict
isotropy groups for different finite outer AQ contexts are related by
the CANONICAL CY/CO transport through the entire original CN group.
The CY physical kernel-triviality theorem makes this an actual group
isomorphism on the selected no-extra-relations strict Kuu presentation,
not a newly postulated geometric 16-cell. We show:
* BF/BE strict full-arrow action composes in the correct AQ word order;
* BV/BW prefixing preserves the COMPLETE ordered noncommutative raw word;
* BX removes each finite prefix without erasing Type-valued provenance;
* the strict transport preserves all original CN coordinates and the
  nontrivial DC free-group Bool parity quotient, including arbitrary
  signed words and the CZ infinite native generator family;
* arbitrary inter-inner comparison has an explicit kernel obstruction
  and requires a separately supplied typed transport.

The selected partial quotient is not asserted to be a geometric gauge
quotient. No new Gray, geometric 16-cell, relation, axiom, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDD vDD wDD tDD uD vD uE vE

section AbstractTypedObstruction

variable {G : Type uDD} {Q : Type vDD}
variable {G' : Type wDD} {Q' : Type tDD}
variable [Group G] [Group Q] [Group G'] [Group Q']

/-- For ANY supplied group transport (in particular an independently
validated typed inner-boundary comparison), parity can move across a
surjective quotient exactly when the original kernel is respected.
This does not assert the existence of such an inter-inner transport. -/
theorem nativeC60DDTransport_descends_iff_kernel
    (q : G →* Q) (hq : Function.Surjective q)
    (q' : G' →* Q') (transport : G →* G') :
    (∃ induced : Q →* Q', induced.comp q = q'.comp transport) ↔
      q.ker ≤ (q'.comp transport).ker :=
  nativeC60DCPartial_descent_iff_kernel q hq (q'.comp transport)

end AbstractTypedObstruction

section CompleteFiniteAQCodes

variable {L : NativeC60AXLayer.{uDD}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Two actual finite AQ prefixes compose on the COMPLETE BV generator
code, including both dependent original endpoints and the primitive
16D witness. Concatenation order is deliberately noncommutative. -/
theorem nativeC60DDCodePrefix_append
    (more outer : List Bool) (code : NativeC60BVGeneratorCode S) :
    nativeC60BWCodePrefix S (more ++ outer) code =
      nativeC60BWCodePrefix S more
        (nativeC60BWCodePrefix S outer code) := by
  rcases code with ⟨word, evidence⟩
  change ((more ++ outer) ++ word, evidence) =
    (more ++ (outer ++ word), evidence)
  rw [List.append_assoc]

/-- Noncommutative free-group version of the true finite-AQ context
composition, on every signed reduced or unreduced 16D provenance word. -/
theorem nativeC60DDFreePrefix_append
    (more outer : List Bool) :
    (nativeC60BWFreePrefix S more).comp
        (nativeC60BWFreePrefix S outer) =
      nativeC60BWFreePrefix S (more ++ outer) := by
  apply FreeGroup.ext_hom
  intro code
  change FreeGroup.of
      (nativeC60BWCodePrefix S more
        (nativeC60BWCodePrefix S outer code)) =
    FreeGroup.of (nativeC60BWCodePrefix S (more ++ outer) code)
  exact congrArg FreeGroup.of
    (nativeC60DDCodePrefix_append S F more outer code).symm

/-- Original Type-valued raw sixteen-dimensional proof witnesses
obey exact two-context covariance of their ENTIRE BW free word. -/
theorem nativeC60DDRawHolonomy_two_prefix
    (more outer : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F (more ++ outer) c) =
      nativeC60BWFreePrefix S more
        (nativeC60BWFreePrefix S outer
          (nativeC60BWFreeHolonomy S F c)) := by
  rw [nativeC60BWFreeHolonomy_frame]
  exact (DFunLike.congr_fun
    (nativeC60DDFreePrefix_append S more outer)
    (nativeC60BWFreeHolonomy S F c)).symm

/-- BX really removes the two AQ contexts in reverse order: even a
noncommutative signed raw word is recovered with no loss of evidence. -/
theorem nativeC60DDRawHolonomy_two_unprefix
    (more outer : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BXFreeUnprefix S outer
        (nativeC60BXFreeUnprefix S more
          (nativeC60BWFreeHolonomy S F
            (nativeC60BCMapClosedStep S F (more ++ outer) c))) =
      nativeC60BWFreeHolonomy S F c := by
  rw [nativeC60DDRawHolonomy_two_prefix S F more outer c,
    nativeC60BXFreeUnprefix_prefix S more,
    nativeC60BXFreeUnprefix_prefix S outer]

/-- Full BF functorial transport is an action on original strict arrows,
not only on numerical or group-valued observations. -/
theorem nativeC60DDStrictContext_action
    (more outer : List Bool) (q : NativeC60BEStrictArrowBundle S F) :
    nativeC60BEArrowContext S F (more ++ outer) q =
      nativeC60BEArrowContext S F more
        (nativeC60BEArrowContext S F outer q) :=
  nativeC60BEArrowContext_append S F more outer q

/-- The corresponding equality holds as an equality of genuine
strict endofunctors, including every original dependent hom-set. -/
theorem nativeC60DDStrictContext_functor
    (more outer : List Bool) :
    nativeC60BDNoRelations_strictFunctor S F (more ++ outer) =
      nativeC60BDNoRelations_strictFunctor S F outer ⋙
        nativeC60BDNoRelations_strictFunctor S F more :=
  nativeC60BFStrictFunctor_append S F more outer

end CompleteFiniteAQCodes

section PhysicalFiniteAQNaturality

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

/-- ACTUAL strict-isotropy transport on a fixed original conservative
15D inner Type-valued boundary. It decodes in the ORIGINAL CN group
and re-embeds into the strictly transported OUTER context. CY proves
this reconstruction equals the whole original isotropy, not a subgroup
or an observer-quotient model. -/
def nativeK5DDOuterStrictTransport
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) :
    nativeK5DBIsotropy W R inner outer →*
      nativeK5DBIsotropy W R inner (more ++ outer) :=
  (nativeC60COEmbed (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) (more ++ outer)
    (nativeK5CKAtomGenerator W R inner)).comp
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer
      (nativeK5CKAtomGenerator W R inner))

/-- CN recovery is STRICTLY NATURAL for EVERY element of the true
conservative strict automorphism group, not just chosen CZ letters. -/
theorem nativeK5DDOuterStrictTransport_CN
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (more ++ outer)
        (nativeK5CKAtomGenerator W R inner)
        (nativeK5DDOuterStrictTransport W R inner outer more z) =
      nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner) z := by
  change nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner)
      (nativeC60COEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (more ++ outer)
        (nativeK5CKAtomGenerator W R inner)
        (nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CKAtomGenerator W R inner) z)) = _
  exact nativeC60CORetraction_embed (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) (more ++ outer)
    (nativeK5CKAtomGenerator W R inner) _

/-- The actual strictly transported source has zero kernel: the
original physical CX/CY theorem ensures injectivity of the transport. -/
theorem nativeK5DDOuterStrictTransport_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) :
    Function.Injective (nativeK5DDOuterStrictTransport W R inner outer more) := by
  intro z z' h
  apply nativeC60CYGenericRetraction_injective
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
    (nativeK5CYPhysicalKernel_eq_one W R inner outer)
  have hh := congrArg
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner)) h
  simpa only [nativeK5DDOuterStrictTransport_CN] using hh

/-- The target original strict automorphism is always represented by
its original CN term (CY), proving true outer-context surjectivity. -/
theorem nativeK5DDOuterStrictTransport_surjective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) :
    Function.Surjective (nativeK5DDOuterStrictTransport W R inner outer more) := by
  intro z
  refine ⟨nativeC60COEmbed (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner) z), ?_⟩
  change nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
        (nativeC60COEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) (more ++ outer)
            (nativeK5CKAtomGenerator W R inner) z))) = z
  rw [nativeC60CORetraction_embed]
  exact nativeK5CYPhysicalEvery_strict_loop_CN
    W R inner (more ++ outer) z

/-- On the selected original conservative strict presentation, every
finite outer AQ context induces a genuine group ISOMORPHISM. This is
theorem-derived from CX/CY, not assumed for arbitrary geometric higher
quotients or for changing the independent inner boundary. -/
def nativeK5DDOuterStrictEquiv
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R inner (more ++ outer) :=
  nativeC60DBBijectiveQuotientEquiv
    (nativeK5DDOuterStrictTransport W R inner outer more)
    (nativeK5DDOuterStrictTransport_surjective W R inner outer more)
    (nativeK5DDOuterStrictTransport_injective W R inner outer more)

/-- True full noncommutative BW holonomy transforms by the ORIGINAL
BV finite-prefix map. Neither the 14D/15D certificates nor the
noncommutative higher word are erased before this equality. -/
theorem nativeK5DDOuterStrictTransport_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (more ++ outer)
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
        (nativeK5DDOuterStrictTransport W R inner outer more z) =
      nativeC60BWFreePrefix (nativeK5AXKuuSignature W) more
        (nativeC60COHolonomy (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) z) := by
  let S := nativeK5AXKuuSignature W
  let F := nativeK5BCFrame W
  let base := nativeK5CKAtomGenerator W R inner
  let coord := nativeC60CORetraction S F outer base z
  change nativeC60COHolonomy S F (more ++ outer) _
      (nativeC60COEmbed S F (more ++ outer) base coord) =
    nativeC60BWFreePrefix S more
      (nativeC60COHolonomy S F outer _ z)
  rw [nativeC60COEmbed_holonomy_apply]
  have hz := congrArg (nativeC60COHolonomy S F outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    (nativeK5CYPhysicalEvery_strict_loop_CN W R inner outer z)
  change nativeC60COHolonomy S F outer _
      (nativeC60COEmbed S F outer base coord) =
    nativeC60COHolonomy S F outer _ z at hz
  rw [nativeC60COEmbed_holonomy_apply] at hz
  rw [← hz]
  exact (DFunLike.congr_fun
    (nativeC60DDFreePrefix_append S more outer)
    (nativeC60CNEmbed S F base coord)).symm

/-- Nontrivial parity is preserved NATURALLY on the WHOLE actual
strict conservative automorphism group under EVERY finite outer AQ
context. This is a commuting square of real group morphisms. -/
theorem nativeK5DDOuterStrictTransport_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R inner (more ++ outer)
        (nativeK5DDOuterStrictTransport W R inner outer more z) =
      nativeK5DCParityQuotient W R inner outer z := by
  change (FreeGroup.map (nativeK5DCLetterParity W R inner))
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (more ++ outer)
        (nativeK5CKAtomGenerator W R inner)
        (nativeK5DDOuterStrictTransport W R inner outer more z)) =
    (FreeGroup.map (nativeK5DCLetterParity W R inner))
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner) z)
  exact congrArg (FreeGroup.map (nativeK5DCLetterParity W R inner))
    (nativeK5DDOuterStrictTransport_CN W R inner outer more z)

/-- Exact naturality square as an equality of WHOLE group morphisms,
not merely of observations on a finite selection of generators. -/
theorem nativeK5DDOuterStrictTransport_parity_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) :
    (nativeK5DCParityQuotient W R inner (more ++ outer)).comp
        (nativeK5DDOuterStrictTransport W R inner outer more) =
      nativeK5DCParityQuotient W R inner outer := by
  apply MonoidHom.ext
  intro z
  exact nativeK5DDOuterStrictTransport_parity W R inner outer more z

/-- Original conservative symm-depth n, including its original proof
identity, is carried to the SAME original letter in the target strict
isotropy; no geometrical 16D filling is introduced. -/
theorem nativeK5DDOuterStrictTransport_CZ
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) (n : Nat) :
    nativeK5DDOuterStrictTransport W R inner outer more
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) =
      nativeK5CZFreeNatEmbed W R inner (more ++ outer) (FreeGroup.of n) := by
  change nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner)
        (nativeC60COEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CKAtomGenerator W R inner)
          (FreeGroup.map (nativeK5CZLetter W R inner) (FreeGroup.of n)))) =
    nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (more ++ outer)
      (nativeK5CKAtomGenerator W R inner)
      (FreeGroup.map (nativeK5CZLetter W R inner) (FreeGroup.of n))
  rw [nativeC60CORetraction_embed]

/-- Finite outer context transport is an exact identity on the coarse
Bool word of EVERY original natural-number symm-depth. -/
theorem nativeK5DDOuterStrictTransport_CZ_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool) (n : Nat) :
    nativeK5DCParityQuotient W R inner (more ++ outer)
      (nativeK5DDOuterStrictTransport W R inner outer more
        (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n))) =
      FreeGroup.of (decide (n % 2 = 1)) := by
  rw [nativeK5DDOuterStrictTransport_CZ]
  exact nativeK5DCParityQuotient_CZ W R inner (more ++ outer) n

/-- The partial quotient has EXACTLY transported fibers, including
the nontrivial double-symm identifications: context cannot turn a
partial decoder into the original FULL CN/BW decoder. -/
theorem nativeK5DDOuterStrictTransport_parity_fiber
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more : List Bool)
    (z z' : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R inner (more ++ outer)
        (nativeK5DDOuterStrictTransport W R inner outer more z) =
      nativeK5DCParityQuotient W R inner (more ++ outer)
        (nativeK5DDOuterStrictTransport W R inner outer more z') ↔
      nativeK5DCParityQuotient W R inner outer z =
        nativeK5DCParityQuotient W R inner outer z' := by
  rw [nativeK5DDOuterStrictTransport_parity,
    nativeK5DDOuterStrictTransport_parity]

/-- For an inner Type-valued boundary change, the mere existence of
two original AQ words is NOT sufficient. For any separately supplied
strict transport of the actual ORIGINAL groups, DD identifies the
necessary and sufficient obstruction to an induced parity comparison.
This asserts no unconstructed comparison of different 15D witnesses. -/
theorem nativeK5DDDifferentInner_descent_iff_kernel
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool)
    (transport : nativeK5DBIsotropy W R inner outer →*
      nativeK5DBIsotropy W R inner' outer') :
    (∃ induced : FreeGroup Bool →* FreeGroup Bool,
      induced.comp (nativeK5DCParityQuotient W R inner outer) =
        (nativeK5DCParityQuotient W R inner' outer').comp transport) ↔
      (nativeK5DCParityQuotient W R inner outer).ker ≤
        ((nativeK5DCParityQuotient W R inner' outer').comp transport).ker :=
  nativeC60DDTransport_descends_iff_kernel
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DCParityQuotient W R inner' outer') transport

end PhysicalFiniteAQNaturality

#print axioms nativeC60DDTransport_descends_iff_kernel
#print axioms nativeC60DDCodePrefix_append
#print axioms nativeC60DDFreePrefix_append
#print axioms nativeC60DDRawHolonomy_two_prefix
#print axioms nativeC60DDRawHolonomy_two_unprefix
#print axioms nativeC60DDStrictContext_action
#print axioms nativeC60DDStrictContext_functor
#print axioms nativeK5DDOuterStrictTransport
#print axioms nativeK5DDOuterStrictTransport_CN
#print axioms nativeK5DDOuterStrictTransport_injective
#print axioms nativeK5DDOuterStrictTransport_surjective
#print axioms nativeK5DDOuterStrictEquiv
#print axioms nativeK5DDOuterStrictTransport_BW
#print axioms nativeK5DDOuterStrictTransport_parity
#print axioms nativeK5DDOuterStrictTransport_parity_hom
#print axioms nativeK5DDOuterStrictTransport_CZ
#print axioms nativeK5DDOuterStrictTransport_CZ_parity
#print axioms nativeK5DDOuterStrictTransport_parity_fiber
#print axioms nativeK5DDDifferentInner_descent_iff_kernel

end
end Kuu.F112.Physical
