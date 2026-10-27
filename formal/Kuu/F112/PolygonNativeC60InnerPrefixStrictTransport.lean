import Kuu.F112.PolygonNativeC60TypedInnerBFParityNaturality

/-!
# F112-P94D3DF — original type-valued inner-prefix strict isotropy transfer

DE establishes genuine BF functor covariance and a common original typed
CZ sector for independently chosen finite inner contexts. DF treats the
strictly stronger *comparable* case of an ACTUAL additional inner AQ
prefix. It does not conflate the noncommuting outer and inner context words.

CU's two original AU naturality routes retain the 14D/15D boundaries and
give typed endpoint equalities for (outer ++ shift) ++ inner versus
outer ++ (shift ++ inner). The resulting equality of ORIGINAL strict
objects reindexes actual automorphism groups; no scalar equality
replaces this step. Separately CY, based on CX's genuine generator
unprefix, gives a canonical equivalence between any two outer-framed
strict automorphism groups at the same original inner 15D boundary.
Composition of these two *proven* equivalences constructs a genuine,
whole-group inner-prefix strict equivalence at arbitrary outer frame.

The exact noncommutative BW provenance of all source strict loops is
retained by that transport, with its original CN code and precisely
ordered outer/inner prefixes. We keep the question of equality of
whole-group DC parity maps separate from equality on the DE original
CZ subfamily: DD's kernel inclusion is the exact descent obstruction.
No geometric 16-cell, Gray structure, independent replacement of
strict Kuu, new axioms, sorry, or admit is introduced.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDF vDF wDF uD vD uE vE

section GenericStrictObjectReindex

/-- Exact equality of original CATEGORY OBJECTS, not an equality of
their group-valued receivers, reindexes the genuine opposite Aut group. -/
def nativeC60DFReindexAut
    {C : Type uDF} [Category.{vDF} C] {X Y : C}
    (h : X = Y) : (Aut X)ᵐᵒᵖ ≃* (Aut Y)ᵐᵒᵖ := by
  cases h
  exact MulEquiv.refl _

/-- Reindexing is the identity when the original strict objects agree
definitionally. No automorphism is discarded or collapsed. -/
theorem nativeC60DFReindexAut_rfl
    {C : Type uDF} [Category.{vDF} C] (X : C)
    (z : (Aut X)ᵐᵒᵖ) :
    nativeC60DFReindexAut (C := C) (X := X) rfl z = z := by
  rfl

/-- Any original free holonomy evaluates identically on genuinely
equal strict objects after exact Aut reindexing. -/
theorem nativeC60DFReindexAut_holonomy
    {C : Type uDF} [Category.{vDF} C]
    {G : Type wDF} [Group G] {X Y : C}
    (h : X = Y) (obs : C ⥤ SingleObj (Gᵐᵒᵖ))
    (z : (Aut X)ᵐᵒᵖ) :
    MulOpposite.unop
      (obs.map ((nativeC60DFReindexAut h z).unop.hom)) =
    MulOpposite.unop (obs.map z.unop.hom) := by
  cases h
  rfl

end GenericStrictObjectReindex

section GenuinePhysicalInnerPrefix

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

/-- Exact source 15D equality across two TRUE context presentations,
using the genuine conserved 14D fiber R and CU original boundary map.
No commutativity of outer and inner prefix is assumed. -/
theorem nativeK5DFInnerPrefix_source_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5BCContext W (outer ++ shift)
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) =
      nativeK5BCContext W outer
        (nativeK5CHSource W (shift ++ inner)
          (nativeK5CKConservativeRefl W R)) := by
  calc
    _ = nativeK5CHSource W ((outer ++ shift) ++ inner)
        (nativeK5CKConservativeRefl W R) :=
      nativeK5CUPhysical_source_frame_append W inner (outer ++ shift) _
    _ = nativeK5CHSource W (outer ++ (shift ++ inner))
        (nativeK5CKConservativeRefl W R) := by rw [List.append_assoc]
    _ = _ := (nativeK5CUPhysical_source_frame_append
      W (shift ++ inner) outer (nativeK5CKConservativeRefl W R)).symm

/-- The independent target-first 15D witness has the same exact
boundary rebracketing. This prevents covertly dropping the second
Type-valued original boundary. -/
theorem nativeK5DFInnerPrefix_target_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5BCContext W (outer ++ shift)
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) =
      nativeK5BCContext W outer
        (nativeK5CHTarget W (shift ++ inner)
          (nativeK5CKConservativeRefl W R)) := by
  calc
    _ = nativeK5CHTarget W ((outer ++ shift) ++ inner)
        (nativeK5CKConservativeRefl W R) :=
      nativeK5CUPhysical_target_frame_append W inner (outer ++ shift) _
    _ = nativeK5CHTarget W (outer ++ (shift ++ inner))
        (nativeK5CKConservativeRefl W R) := by rw [List.append_assoc]
    _ = _ := (nativeK5CUPhysical_target_frame_append
      W (shift ++ inner) outer (nativeK5CKConservativeRefl W R)).symm

/-- ACTUAL strict object equality induced by original dependent
source 15D boundary, rather than selected parity observational value. -/
theorem nativeK5DFInnerPrefix_strict_object
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeC60COObject (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (outer ++ shift)
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) =
      nativeC60COObject (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W (shift ++ inner)
          (nativeK5CKConservativeRefl W R)) := by
  exact congrArg
    (fun a : (nativeK5AXBaseLayer W).Total =>
      (nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj ⟨a⟩)
    (nativeK5DFInnerPrefix_source_boundary W R inner outer shift)

/-- Genuine strict group equivalence for ANY TWO finite outer frames,
using CY's actual physical kernel-triviality and the original CN
free group, never an observed quotient or an abstract new isotropy. -/
def nativeK5DFOuterReframeEquiv
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer targetOuter : List Bool) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R inner targetOuter :=
  (nativeK5CYPhysicalFreeIsotropy W R inner outer).symm.trans
    (nativeK5CYPhysicalFreeIsotropy W R inner targetOuter)

/-- Reindex the two genuinely equal strict objects without
identifying the original distinct inner Type-valued histories. -/
def nativeK5DFInnerPrefixReindex
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DBIsotropy W R inner (outer ++ shift) ≃*
      nativeK5DBIsotropy W R (shift ++ inner) outer :=
  nativeC60DFReindexAut
    (nativeK5DFInnerPrefix_strict_object W R inner outer shift)

/-- MAIN DF construction. A genuinely added INNER finite AQ context
induces an equivalence of the WHOLE ORIGINAL proof-bearing C60 strict
automorphism groups. The first factor uses CX/CY's original true typed
outer-unprefix theorem; the second is the genuine CU strict object
equality, not equality of Peiffer/holonomy receiver values. -/
def nativeK5DFInnerPrefixStrictEquiv
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R (shift ++ inner) outer :=
  (nativeK5DFOuterReframeEquiv W R inner outer (outer ++ shift)).trans
    (nativeK5DFInnerPrefixReindex W R inner outer shift)

/-- The FULL original CN word coordinates survive an arbitrary change
of outer framing; statement is on every TRUE strict automorphism. -/
theorem nativeK5DFOuterReframe_CN
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer targetOuter : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) targetOuter
        (nativeK5CKAtomGenerator W R inner)
        (nativeK5DFOuterReframeEquiv W R inner outer targetOuter z) =
      nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner) z := by
  change nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) targetOuter (nativeK5CKAtomGenerator W R inner)
      (nativeC60COEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) targetOuter (nativeK5CKAtomGenerator W R inner)
        (nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) z)) = _
  exact nativeC60CORetraction_embed
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    targetOuter (nativeK5CKAtomGenerator W R inner) _

/-- A true reframe retains its complete original noncommutative
16D provenance, including the two original dependent 15D boundaries. -/
theorem nativeK5DFOuterReframe_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer targetOuter : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) targetOuter
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
        (nativeK5DFOuterReframeEquiv W R inner outer targetOuter z) =
      nativeC60BWFreePrefix (nativeK5AXKuuSignature W) targetOuter
        (nativeC60CNEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) outer
            (nativeK5CKAtomGenerator W R inner) z)) := by
  change nativeC60COHolonomy (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) targetOuter _
      (nativeC60COEmbed (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) targetOuter (nativeK5CKAtomGenerator W R inner)
        (nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) z)) = _
  exact nativeC60COEmbed_holonomy_apply
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    targetOuter (nativeK5CKAtomGenerator W R inner) _

/-- The STRICT-O-BJECT reindex is exactly holonomy invariant:
no observer-kernel equivalence has been used to identify arrows. -/
theorem nativeK5DFInnerPrefixReindex_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (z : nativeK5DBIsotropy W R inner (outer ++ shift)) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W (shift ++ inner)
          (nativeK5CKConservativeRefl W R))
        (nativeK5DFInnerPrefixReindex W R inner outer shift z) =
      nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (outer ++ shift)
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) z := by
  change MulOpposite.unop
      ((nativeC60BWFreeStrictHolonomy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).map
        ((nativeC60DFReindexAut
          (nativeK5DFInnerPrefix_strict_object W R inner outer shift) z).unop.hom)) =
    MulOpposite.unop
      ((nativeC60BWFreeStrictHolonomy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).map z.unop.hom)
  exact nativeC60DFReindexAut_holonomy
    (nativeK5DFInnerPrefix_strict_object W R inner outer shift)
    (nativeC60BWFreeStrictHolonomy
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) z

/-- WHOLE-GROUP exact noncommutative BW code of the newly constructed
inner-prefix strict equivalence; the value is expressed in original
CN coordinates, with the correct (outer ++ shift) word ORDER. -/
theorem nativeK5DFInnerPrefixStrictEquiv_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W (shift ++ inner)
          (nativeK5CKConservativeRefl W R))
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z) =
      nativeC60BWFreePrefix (nativeK5AXKuuSignature W)
        (outer ++ shift)
        (nativeC60CNEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) outer
            (nativeK5CKAtomGenerator W R inner) z)) := by
  change nativeC60COHolonomy (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer _
      (nativeK5DFInnerPrefixReindex W R inner outer shift
        (nativeK5DFOuterReframeEquiv W R inner outer (outer ++ shift) z)) = _
  rw [nativeK5DFInnerPrefixReindex_BW]
  exact nativeK5DFOuterReframe_BW W R inner outer (outer ++ shift) z

/-- The strict inner-prefix transfer is an actual invertible group map.
This does NOT assert a new geometric 16-cell relation. -/
theorem nativeK5DFInnerPrefixStrictEquiv_bijective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    Function.Bijective (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift) :=
  (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).bijective

/-- Exact obstruction to the PARTIAL parity quotient following the
new ACTUAL whole-group inner-prefix equivalence: no unproved kernel
inclusion is silently introduced. The two quotient maps are the
ORIGINAL DC maps, not a new geometry or raw Type equality. -/
theorem nativeK5DFInnerPrefix_parity_descent_iff_kernel
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    (∃ descended : FreeGroup Bool →* FreeGroup Bool,
      descended.comp (nativeK5DCParityQuotient W R inner outer) =
        (nativeK5DCParityQuotient W R (shift ++ inner) outer).comp
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom) ↔
      (nativeK5DCParityQuotient W R inner outer).ker ≤
        ((nativeK5DCParityQuotient W R (shift ++ inner) outer).comp
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom).ker :=
  nativeK5DDDifferentInner_descent_iff_kernel W R inner outer
    (shift ++ inner) outer
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift).toMonoidHom

end GenuinePhysicalInnerPrefix

#print axioms nativeC60DFReindexAut
#print axioms nativeC60DFReindexAut_rfl
#print axioms nativeC60DFReindexAut_holonomy
#print axioms nativeK5DFInnerPrefix_source_boundary
#print axioms nativeK5DFInnerPrefix_target_boundary
#print axioms nativeK5DFInnerPrefix_strict_object
#print axioms nativeK5DFOuterReframeEquiv
#print axioms nativeK5DFInnerPrefixReindex
#print axioms nativeK5DFInnerPrefixStrictEquiv
#print axioms nativeK5DFOuterReframe_CN
#print axioms nativeK5DFOuterReframe_BW
#print axioms nativeK5DFInnerPrefixReindex_BW
#print axioms nativeK5DFInnerPrefixStrictEquiv_BW
#print axioms nativeK5DFInnerPrefixStrictEquiv_bijective
#print axioms nativeK5DFInnerPrefix_parity_descent_iff_kernel

end
end Kuu.F112.Physical
