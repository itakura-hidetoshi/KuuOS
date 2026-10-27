import Kuu.F112.PolygonNativeC60ConservativeTargetSourceRigidity

/-!
# F112-P94D3CV — arbitrary finite ORIGINAL signed C60 gauge sector

CU proves both ends of the original conservative C60 BC base are rigid.
CV now considers every length of genuinely dependent signed 16D paths
starting at either original 15D endpoint, including the arbitrary
outer AQ strict-isotropy framing.

The physical base is an ACTUAL shifted 16D generator. The proved
incidence laws force every positive generator from its source, and
every positive generator into its target, to be parallel to the same
two original 15D objects. CJ excludes incoming positives at the
source and outgoing positives at the target.

An inductively constructed TYPE-VALUED signed gauge-sector certificate
therefore exists for EVERY original finite signed path from those
endpoints. Its positive and negative constructors retain the entire
original BC primitive certificate and the exact intermediate 15D
objects; only their strict ordering is classified. The complete
noncommutative BW word is recovered from the original primitive
code trace, not a graph, an abelianization, or a quotient projection.

No assertion that all original framed codes have a CN unprefix lift,
that the CO kernel is trivial, that the actual free group action is
trivial, or that all higher geometric coherence descends. This stage
does NOT equate distinct 15D or 16D proof terms. No Gray, axioms,
sorry/admit, new public roots, or modifications of protected #1558.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCV uD vD uE vE

section GenericGaugeSector

/-- A TYPE-valued certificate that each signed step carries one
actual, original 16D generator with exact 15D endpoints A/B.
No raw comparison term or independent generator is manufactured. -/
inductive NativeC60CVSignedGaugeSector {L : NativeC60AXLayer.{uCV}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (A B : L.Total) :
    {x y : L.Total} → NativeC60CASignedChain S F x y → Type uCV where
  | nilSource :
      NativeC60CVSignedGaugeSector S F A B (.nil A)
  | nilTarget :
      NativeC60CVSignedGaugeSector S F A B (.nil B)
  | positive {y : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen A B)
      (tail : NativeC60CASignedChain S F B y)
      (htail : NativeC60CVSignedGaugeSector S F A B tail) :
      NativeC60CVSignedGaugeSector S F A B (.pos g tail)
  | negative {y : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen A B)
      (tail : NativeC60CASignedChain S F A y)
      (htail : NativeC60CVSignedGaugeSector S F A B tail) :
      NativeC60CVSignedGaugeSector S F A B (.neg g tail)

/-- The four exact incidence laws suffice for the entire finite signed
language, including arbitrary intermediate ORIGINAL 15D Types. -/
theorem nativeC60CVSignedGaugeSector_of_incidence
    {L : NativeC60AXLayer.{uCV}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (A B : L.Total)
    (houtA : ∀ {z : L.Total},
      (nativeC60BCClosedSignature S F).Gen A z → z = B)
    (hinB : ∀ {z : L.Total},
      (nativeC60BCClosedSignature S F).Gen z B → z = A)
    (hnoOutB : ∀ {z : L.Total},
      (nativeC60BCClosedSignature S F).Gen B z → False)
    (hnoInA : ∀ {z : L.Total},
      (nativeC60BCClosedSignature S F).Gen z A → False) :
    ∀ {x y : L.Total} (p : NativeC60CASignedChain S F x y),
      (x = A ∨ x = B) → NativeC60CVSignedGaugeSector S F A B p := by
  intro x y path
  induction path with
  | nil x =>
      intro hx
      rcases hx with hA | hB
      · subst x
        exact .nilSource
      · subst x
        exact .nilTarget
  | pos g tail ih =>
      intro hx
      rcases hx with hA | hB
      · subst x
        have hmiddle := houtA g
        cases hmiddle
        exact .positive g tail (ih (Or.inr rfl))
      · subst x
        exact False.elim (hnoOutB g)
  | neg g tail ih =>
      intro hx
      rcases hx with hA | hB
      · subst x
        exact False.elim (hnoInA g)
      · subst x
        have hmiddle := hinB g
        cases hmiddle
        exact .negative g tail (ih (Or.inl rfl))

/-- Every sector certificate records the exact original final 15D
endpoint as one of the two endpoints; no third proof object arises. -/
theorem NativeC60CVSignedGaugeSector.target_two_endpoints
    {L : NativeC60AXLayer.{uCV}}
    {S : NativeC60AXSignature L} {F : Bool → NativeC60BCFrame L}
    {A B : L.Total} {x y : L.Total}
    {p : NativeC60CASignedChain S F x y}
    (certificate : NativeC60CVSignedGaugeSector S F A B p) :
    y = A ∨ y = B := by
  induction certificate with
  | nilSource => exact Or.inl rfl
  | nilTarget => exact Or.inr rfl
  | positive _ _ _ ih => exact ih
  | negative _ _ _ ih => exact ih

/-- Extract a COMPLETE signed original BC generator word from an
independent Type-valued gauge-sector certificate. Each letter still
carries its original dependent 15D A/B boundaries and 16D witness. -/
def NativeC60CVSignedGaugeSector.originalLetters
    {L : NativeC60AXLayer.{uCV}}
    {S : NativeC60AXSignature L} {F : Bool → NativeC60BCFrame L}
    {A B : L.Total} {x y : L.Total}
    {p : NativeC60CASignedChain S F x y}
    (certificate : NativeC60CVSignedGaugeSector S F A B p) :
    List ((nativeC60BCClosedSignature S F).Gen A B × Bool) :=
  match certificate with
  | .nilSource => []
  | .nilTarget => []
  | .positive g _ htail => (g, true) :: htail.originalLetters
  | .negative g _ htail => (g, false) :: htail.originalLetters

/-- The extracted sector word reproduces the entire TRUE signed
provenance code, not merely its source, charge, or decoded shadow. -/
theorem NativeC60CVSignedGaugeSector.originalLetters_codes
    {L : NativeC60AXLayer.{uCV}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {A B : L.Total} {x y : L.Total}
    {p : NativeC60CASignedChain S F x y}
    (certificate : NativeC60CVSignedGaugeSector S F A B p) :
    (certificate.originalLetters.map
      (fun entry => (nativeC60BVGeneratorCode S F entry.1, entry.2))) =
      nativeC60CAChainSignedCodes S F p := by
  induction certificate with
  | nilSource => rfl
  | nilTarget => rfl
  | positive g tail htail ih =>
      simp only [originalLetters, List.map_cons, nativeC60CAChainSignedCodes,
        ih]
  | negative g tail htail ih =>
      simp only [originalLetters, List.map_cons, nativeC60CAChainSignedCodes,
        ih]

/-- The complete original free noncommutative 16D holonomy can be read
directly from the sector's generator list without changing proofs. -/
theorem NativeC60CVSignedGaugeSector.full_holonomy
    {L : NativeC60AXLayer.{uCV}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {A B : L.Total} {x y : L.Total}
    {p : NativeC60CASignedChain S F x y}
    (certificate : NativeC60CVSignedGaugeSector S F A B p) :
    nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F p) =
      FreeGroup.mk (certificate.originalLetters.map
        (fun entry => (nativeC60BVGeneratorCode S F entry.1, entry.2))) := by
  rw [nativeC60CAChain_holonomy, certificate.originalLetters_codes]

end GenericGaugeSector

section PhysicalC60

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

/-- Actual framed base certificate at the SAME proof-bearing strict
isotropy object of CO/CP/CQ/CR, for independent inner/outer AQ words. -/
def nativeK5CVFramedBase
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :=
  nativeC60BCShiftGen (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)

/-- The ACTUAL original endpoint A has no incoming positive 16D
comparison. No free group/homology observation is involved. -/
theorem nativeK5CVFramed_no_incoming_source
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {z : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen z
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))) :
    False :=
  nativeK5CSNo_adjacent_positive W g (nativeK5CVFramedBase W R inner outer)

/-- The ACTUAL original endpoint B has no outgoing positive 16D
comparison, so no genuine positive-positive two-step exists. -/
theorem nativeK5CVFramed_no_outgoing_target
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {z : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) z) :
    False :=
  nativeK5CSNo_adjacent_positive W (nativeK5CVFramedBase W R inner outer) g

/-- CT's genuine conservative outgoing rigidity at the actual physical
outer-framed original fifteen-dimensional source. -/
theorem nativeK5CVFramed_outgoing_unique_target
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {z : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) z) :
    z = nativeK5BCContext W outer
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) :=
  (nativeK5CUPhysical_framed_incidence_parallel W R inner outer
    g (nativeK5CVFramedBase W R inner outer)).1

/-- CU's dual incoming rigidity at the ACTUAL same physical original
fifteen-dimensional terminal object, for all independent contexts. -/
theorem nativeK5CVFramed_incoming_unique_source
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {z : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen z
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))) :
    z = nativeK5BCContext W outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) :=
  (nativeK5CUPhysical_framed_incidence_parallel W R inner outer
    (nativeK5CVFramedBase W R inner outer) g).2

/-- For EVERY finite genuinely typed signed 16D path starting in
either framed original physical 15D endpoint, one constructs a
complete Type-valued two-boundary gauge-sector certificate. -/
theorem nativeK5CVAll_finite_signed_gauge_sector
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {x y : (nativeK5AXBaseLayer W).Total}
    (path : NativeC60CASignedChain (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) x y)
    (hstart : x = nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) ∨
      x = nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :
    NativeC60CVSignedGaugeSector
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
      (nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))
      path := by
  exact nativeC60CVSignedGaugeSector_of_incidence
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5BCContext W outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    (nativeK5BCContext W outer
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)))
    (fun {_} g => nativeK5CVFramed_outgoing_unique_target W R inner outer g)
    (fun {_} g => nativeK5CVFramed_incoming_unique_source W R inner outer g)
    (fun {_} g => nativeK5CVFramed_no_outgoing_target W R inner outer g)
    (fun {_} g => nativeK5CVFramed_no_incoming_source W R inner outer g)
    path hstart

/-- The original 15D endpoint reached by ANY finite signed physical
C60 path in the genuine conservative isotropy sector is necessarily
one of the two ACTUAL framed boundary proofs. -/
theorem nativeK5CVAll_finite_signed_endpoint_two
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {x y : (nativeK5AXBaseLayer W).Total}
    (path : NativeC60CASignedChain (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) x y)
    (hstart : x = nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) ∨
      x = nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) :
    y = nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) ∨
      y = nativeK5BCContext W outer
        (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) :=
  (nativeK5CVAll_finite_signed_gauge_sector W R inner outer path hstart).target_two_endpoints

/-- The BW free-group holonomy of ANY genuine original finite signed
loop based at the CO strict isotropy object is supported entirely on
the original parallel BC certificates of the SAME physical endpoints.
This is a literal signed-list equality, not a quotient-level analogy. -/
theorem nativeK5CVOriginal_signed_loop_complete_code
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (path : NativeC60CASignedChain (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
      (nativeK5BCContext W outer
        (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))) :
    ∃ xs : List
      ((nativeK5BCSignature W).Gen
        (nativeK5BCContext W outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
        (nativeK5BCContext W outer
          (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R))) × Bool),
      nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeC60CAChainStep (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) path) =
      FreeGroup.mk (xs.map (fun entry =>
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) entry.1, entry.2))) := by
  let cert := nativeK5CVAll_finite_signed_gauge_sector
    W R inner outer path (Or.inl rfl)
  exact ⟨cert.originalLetters, cert.full_holonomy
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)⟩

end PhysicalC60

#print axioms nativeC60CVSignedGaugeSector_of_incidence
#print axioms NativeC60CVSignedGaugeSector.target_two_endpoints
#print axioms NativeC60CVSignedGaugeSector.originalLetters
#print axioms NativeC60CVSignedGaugeSector.originalLetters_codes
#print axioms NativeC60CVSignedGaugeSector.full_holonomy
#print axioms nativeK5CVFramedBase
#print axioms nativeK5CVFramed_no_incoming_source
#print axioms nativeK5CVFramed_no_outgoing_target
#print axioms nativeK5CVFramed_outgoing_unique_target
#print axioms nativeK5CVFramed_incoming_unique_source
#print axioms nativeK5CVAll_finite_signed_gauge_sector
#print axioms nativeK5CVAll_finite_signed_endpoint_two
#print axioms nativeK5CVOriginal_signed_loop_complete_code

end
end Kuu.F112.Physical
