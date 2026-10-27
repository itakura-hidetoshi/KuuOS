import Kuu.F112.PolygonNativeC60MixedForkHolonomyObstruction

/-!
# F112-P94D3CL — framed signed fork normalization and selective geometric descent

CJ excludes any two consecutive positive original C60 BC primitives.
CK exhibits a truly typed nontrivial TWO-EDGE MIXED-SIGN 16D loop,
constructed from two distinct original conservative 15D proof certificates.

CL treats all finite original AQ contexts and the precise distinction
between safe typed cancellation and a forbidden geometric identification.

* Finite genuine frame transport of a mixed fork preserves and REFLECTS
  its full free-group nontriviality, its canonical reduced signed trace,
  and equality in the selected no-extra-relations strict Kuu quotient.
* The original two-edge mixed-sign path is constructed in CA's DEPENDENT
  signed-chain grammar. Its complete strict reduction to the empty chain
  is possible precisely if the two original BC generator certificates
  agree. Distinct generators cannot be reduced to nil by any finite
  sequence of the already declared CA typed cancellation moves. Every
  resulting typed reduced normal form remains nonempty.
* A candidate selective geometric relation includes existing CF
  structural triangles and ONLY specified mixed-fork contractions.
  The ORIGINAL complete free receiver descends iff every permitted
  mixed fork identifies the SAME original generator certificate.
  This equivalence holds in all finite physical AQ contexts.
* The actual original C60 CK conservative fork, under independently
  chosen inner and outer contexts, gives a concrete obstruction to
  any candidate policy that allows contracting that particular pair.

This is a theorem about the SELECTED optional BC presentation and the
complete free-group receiver; it is not a construction of a new original
geometric 16-cell, a proof of global Peiffer interchange, Gray, strict-n,
or infinity-hyperdescent. The original dependent 14D/15D data are retained.
No new axioms, sorry, admit, or public-root changes.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Actual transport of the full original two-edge mixed comparison
is another mixed comparison of the genuinely shifted BC generator codes.
No intermediate original fifteen-dimensional object is erased. -/
theorem nativeC60CLFork_frame_raw
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BCMapClosedStep S F word (nativeC60CKMixedFork S F g h) =
      nativeC60CKMixedFork S F
        (nativeC60BCShiftGen S F word g)
        (nativeC60BCShiftGen S F word h) := rfl

/-- The full framed free holonomy of a typed mixed fork vanishes
precisely when its ORIGINAL two positive BC certificates coincide. -/
theorem nativeC60CLFork_frame_free_one_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F word (nativeC60CKMixedFork S F g h)) =
        (1 : FreeGroup (NativeC60BVGeneratorCode S)) ↔ g = h := by
  constructor
  · intro hfree
    rw [nativeC60BWFreeHolonomy_frame S F word _] at hfree
    have hp :
        (nativeC60BWFreePrefix S word)
          (nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h)) =
        (nativeC60BWFreePrefix S word)
          (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
      simpa only [map_one] using hfree
    exact (nativeC60CKMixedFork_free_one_iff S F g h).mp
      ((nativeC60BWFreePrefix_injective S word) hp)
  · intro heq
    rw [nativeC60BWFreeHolonomy_frame S F word _]
    have hfree := (nativeC60CKMixedFork_free_one_iff S F g h).mpr heq
    rw [hfree]
    simp

/-- Canonical Church-Rosser signed trace is also a COMPLETE detector
of framed mixed-fork contraction at every original finite AQ context. -/
theorem nativeC60CLFork_frame_reduced_one_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BYReducedTrace S F
        (nativeC60BCMapClosedStep S F word (nativeC60CKMixedFork S F g h)) =
      nativeC60BYReducedTrace S F
        (nativeC60BCMapClosedStep S F word (.refl a)) ↔ g = h :=
  (nativeC60BYReducedTrace_frame_eq_iff S F word
    (nativeC60CKMixedFork S F g h) (.refl a)).trans
    ((nativeC60BYReducedTrace_eq_iff S F
      (nativeC60CKMixedFork S F g h) (.refl a)).trans
        (nativeC60CKMixedFork_free_one_iff S F g h))

/-- Even in the selected strict groupoid completion, EVERY contextual
mixed-fork contraction is exactly the old typed inverse cancellation,
and cannot equate two originally different generator certificates. -/
theorem nativeC60CLFork_frame_strict_one_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (nativeC60CKMixedFork S F g h)) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.refl a)) ↔ g = h :=
  (nativeC60CDAll_raw_free_eq_iff_strict S F word
    (nativeC60CKMixedFork S F g h) (.refl a)).symm.trans
      (nativeC60CKMixedFork_free_one_iff S F g h)

/-- The ACTUAL typed CA signed-chain interpretation, not an abstract
untyped/free-group word. It traverses a -> b -> a with two independently
recorded genuine original BC generators. -/
def nativeC60CLForkChain
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60CASignedChain S F a a :=
  .pos g (.neg h (.nil a))

/-- The complete ORIGINAL code and orientation of each dependent
16D edge remains in the CA signed-chain provenance. -/
theorem nativeC60CLForkChain_codes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CAChainSignedCodes S F (nativeC60CLForkChain S F g h) =
      [(nativeC60BVGeneratorCode S F g, true),
       (nativeC60BVGeneratorCode S F h, false)] := rfl

/-- A correctly typed signed path can be contracted to the empty
typed chain in ANY finite strict context precisely when its two
ORIGINAL BC generators agree, not merely their observer values.
The existing CC all-finite signed completeness is used directly. -/
theorem nativeC60CLForkChain_strict_nil_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CAChainStrictFrame S F word (nativeC60CLForkChain S F g h) =
      nativeC60CAChainStrictFrame S F word
        (NativeC60CASignedChain.nil a) ↔ g = h := by
  have hnorm :=
    (nativeC60CCAll_signed_free_eq_iff_strict S F word
      (nativeC60CLForkChain S F g h)
      (NativeC60CASignedChain.nil a)).symm
  have hfree :
      FreeGroup.mk (nativeC60CAChainSignedCodes S F
          (nativeC60CLForkChain S F g h)) =
        FreeGroup.mk (nativeC60CAChainSignedCodes S F
          (NativeC60CASignedChain.nil a)) ↔
      nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h) =
        (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
    rw [← nativeC60CAChain_holonomy S F
      (nativeC60CLForkChain S F g h)]
    rw [← nativeC60CAChain_holonomy S F
      (NativeC60CASignedChain.nil a)]
    change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
        ((FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ * 1) = 1 ↔
      FreeGroup.of (nativeC60BVGeneratorCode S F g) *
        (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ = 1
    simp only [mul_one]
  exact hnorm.trans (hfree.trans
    (nativeC60CKMixedFork_free_one_iff S F g h))

/-- Distinct BC generators give a genuinely IRREDUCIBLE OBSTRUCTION:
no finite sequence of the admitted CA typed adjacent inverse
cancellations, at any location in the original 15D skeleton, can
erase the signed two-edge loop to the empty original typed chain. -/
theorem nativeC60CLForkChain_no_cancel_to_nil
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (gauge : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    ¬ Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a a =>
        NativeC60CAElementaryCancel S F x y)
      (nativeC60CLForkChain S F g h)
      (NativeC60CASignedChain.nil a) := by
  intro hc
  have hs := nativeC60CAFiniteCancellation_sound S F gauge hc
  exact hne ((nativeC60CLForkChain_strict_nil_iff S F gauge g h).mp hs)

/-- CC normalizes ANY genuine typed signed chain. For the particular
mixed fork with distinct genuine BC generators, all such permitted
normalization processes must end at a NONEMPTY reduced typed chain. -/
theorem nativeC60CLForkChain_nonempty_normal_form
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    ∃ q : NativeC60CASignedChain S F a a,
      Relation.ReflTransGen
        (fun x y : NativeC60CASignedChain S F a a =>
          NativeC60CAElementaryCancel S F x y)
        (nativeC60CLForkChain S F g h) q ∧
      FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q) ∧
      q ≠ .nil a := by
  obtain ⟨q, hsteps, hred⟩ :=
    nativeC60CCEvery_signed_chain_normalizes S F
      (nativeC60CLForkChain S F g h)
  refine ⟨q, hsteps, hred, ?_⟩
  intro hnil
  cases hnil
  exact (nativeC60CLForkChain_no_cancel_to_nil S F [] g h hne) hsteps

/-- A SELECTIVE candidate higher comparison relation. The well-founded
old CF triangle/cancellation laws are always present. New mixed-fork
contractions are explicitly selected by a rule on genuine parallel
dependent BC generator certificates; no scalar equality manufactures
a 16D geometric filler. -/
inductive NativeC60CLSelectiveRelation
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (Allowed : ∀ {a b : L.Total},
      (nativeC60BCClosedSignature S F).Gen a b →
      (nativeC60BCClosedSignature S F).Gen a b → Prop) :
    {a b : L.Total} →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b → Prop where
  | triangle {a b : L.Total}
      {c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b}
      (h : NativeC60CFTriangleRelation S F c d) :
      NativeC60CLSelectiveRelation S F Allowed c d
  | fork {a b : L.Total}
      (g h : (nativeC60BCClosedSignature S F).Gen a b)
      (hallow : Allowed g h) :
      NativeC60CLSelectiveRelation S F Allowed
        (nativeC60CKMixedFork S F g h) (.refl a)

/-- SHARP NECESSARY AND SUFFICIENT TEST: a proposed selective geometric
comparison relation containing the existing genuine triangle laws can
preserve the complete C60 free receiver precisely if every ADDITIONAL
mixed-fork contraction already contracts the same typed BC generator. -/
theorem nativeC60CLSelective_compatible_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (Allowed : ∀ {a b : L.Total},
      (nativeC60BCClosedSignature S F).Gen a b →
      (nativeC60BCClosedSignature S F).Gen a b → Prop) :
    NativeC60CEGeometricCompatible S F
        (NativeC60CLSelectiveRelation S F Allowed) ↔
      ∀ {a b : L.Total}
        (g h : (nativeC60BCClosedSignature S F).Gen a b),
        Allowed g h → g = h := by
  constructor
  · intro hc a b g h hallowed
    have hfree := hc (nativeC60CKMixedFork S F g h)
      (NativeC60AXStep.refl a) (.fork g h hallowed)
    exact (nativeC60CKMixedFork_free_one_iff S F g h).mp hfree
  · intro hall a b c d h
    cases h with
    | triangle htriangle =>
        exact nativeC60CFTriangle_compatible S F _ _ htriangle
    | fork g h hallowed =>
        exact (nativeC60CKMixedFork_free_one_iff S F g h).mpr
          (hall g h hallowed)

/-- The COMPLETE free-group receiver descends through the proposed
geometric selective presentation if and ONLY if all separately allowed
mixed forks have the same original generator certificates. -/
theorem nativeC60CLSelective_factor_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (Allowed : ∀ {a b : L.Total},
      (nativeC60BCClosedSignature S F).Gen a b →
      (nativeC60BCClosedSignature S F).Gen a b → Prop) :
    (∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
          (NativeC60CLSelectiveRelation S F Allowed) ⥤
          SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
        nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
            (NativeC60CLSelectiveRelation S F Allowed) ⋙ G =
          nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
            (nativeC60BWFreeWeight S F)) ↔
      ∀ {a b : L.Total}
        (g h : (nativeC60BCClosedSignature S F).Gen a b),
        Allowed g h → g = h :=
  (nativeC60CECompatible_iff_holonomy_factor S F
    (NativeC60CLSelectiveRelation S F Allowed)).symm.trans
      (nativeC60CLSelective_compatible_iff S F Allowed)

/-- Equivalent strictly presentation-level criterion at EVERY finite
actual AQ context: no candidate mixed relation can become an extra
strict equality unless it already contracts identical BC generators. -/
theorem nativeC60CLSelective_all_frames_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (Allowed : ∀ {a b : L.Total},
      (nativeC60BCClosedSignature S F).Gen a b →
      (nativeC60BCClosedSignature S F).Gen a b → Prop) :
    (∀ (word : List Bool) {a b : L.Total}
      (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
      NativeC60CLSelectiveRelation S F Allowed c d →
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BCMapClosedStep S F word c) =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BCMapClosedStep S F word d)) ↔
      ∀ {a b : L.Total}
        (g h : (nativeC60BCClosedSignature S F).Gen a b),
        Allowed g h → g = h :=
  (nativeC60CECompatible_iff_all_frames S F
    (NativeC60CLSelectiveRelation S F Allowed)).symm.trans
      (nativeC60CLSelective_compatible_iff S F Allowed)

/-- Exact, generator-equality-only mixed contraction policy. -/
def nativeC60CLSameGeneratorAllowed
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∀ {a b : L.Total},
      (nativeC60BCClosedSignature S F).Gen a b →
      (nativeC60BCClosedSignature S F).Gen a b → Prop :=
  fun {_ _} g h => g = h

/-- The safe selective geometric relation genuinely has a receiver,
including the existing CF triangle laws; no new nontrivial mixed fork
is identified. -/
theorem nativeC60CLSame_generator_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
          (NativeC60CLSelectiveRelation S F
            (nativeC60CLSameGeneratorAllowed S F)) ⥤
          SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
        nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
            (NativeC60CLSelectiveRelation S F
              (nativeC60CLSameGeneratorAllowed S F)) ⋙ G =
          nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
            (nativeC60BWFreeWeight S F) :=
  (nativeC60CLSelective_factor_iff S F
    (nativeC60CLSameGeneratorAllowed S F)).mpr
      (by
        intro a b g h heq
        exact heq)

section OriginalC60

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

/-- Actual original C60 physical CK fork, under independently chosen
INNER and OUTER finite true AQ contexts, remains a nontrivial complete
free-group sixteen-dimensional word. -/
theorem nativeK5CLPhysical_all_contexts_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BCClosedContextStep W outer
        (nativeC60CKMixedFork (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)
          (nativeK5CKReflGenerator W R inner)
          (nativeK5CKAtomGenerator W R inner))) ≠
        (1 : FreeGroup
          (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W))) := by
  intro hfree
  exact (nativeC60CLFork_frame_free_one_iff
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
      (nativeK5CKReflGenerator W R inner)
      (nativeK5CKAtomGenerator W R inner)).mp hfree |>
        nativeK5CKPhysical_parallel_generators_ne W R inner

/-- The EXACT physical 15D comparison endpoints and the distinct
source-conservative witnesses also force a nontrivial STRICT 16D
mixed-sign loop under every pair of genuine finite original contexts. -/
theorem nativeK5CLPhysical_all_contexts_no_strict_collapse
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W outer
          (nativeC60CKMixedFork (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W)
            (nativeK5CKReflGenerator W R inner)
            (nativeK5CKAtomGenerator W R inner))) ≠
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W outer
          (.refl (nativeK5CHSource W inner
            (nativeK5CKConservativeRefl W R)))) := by
  exact nativeC60CKDistinct_fork_no_strict_identity
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
    (nativeK5CKReflGenerator W R inner)
    (nativeK5CKAtomGenerator W R inner)
    (nativeK5CKPhysical_parallel_generators_ne W R inner)

/-- A proposed mixed-fork policy that permits identifying this ONE
original physical conservative pair already blocks descent of the
complete free receiver, irrespective of any other permitted pairs. -/
theorem nativeK5CLPhysical_selective_no_compatibility
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    (Allowed : ∀ {a b : (nativeK5AXBaseLayer W).Total},
      (nativeK5BCSignature W).Gen a b →
      (nativeK5BCSignature W).Gen a b → Prop)
    (hallow : Allowed
      (nativeK5CKReflGenerator W R word)
      (nativeK5CKAtomGenerator W R word)) :
    ¬ NativeC60CEGeometricCompatible
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (NativeC60CLSelectiveRelation (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) Allowed) := by
  intro hc
  have hsafe :
      ∀ {a b : (nativeK5AXBaseLayer W).Total}
        (g h : (nativeK5BCSignature W).Gen a b),
          Allowed g h → g = h :=
    (nativeC60CLSelective_compatible_iff
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Allowed).mp hc
  exact nativeK5CKPhysical_parallel_generators_ne W R word
    (hsafe (nativeK5CKReflGenerator W R word)
      (nativeK5CKAtomGenerator W R word) hallow)

/-- The same concrete physical obstruction is a no-factor theorem:
no geometric strict quotient admitting that selected mixed fork has a
functor that extends the COMPLETE original BC free-group holonomy. -/
theorem nativeK5CLPhysical_selective_no_factor
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool)
    (Allowed : ∀ {a b : (nativeK5AXBaseLayer W).Total},
      (nativeK5BCSignature W).Gen a b →
      (nativeK5BCSignature W).Gen a b → Prop)
    (hallow : Allowed
      (nativeK5CKReflGenerator W R word)
      (nativeK5CKAtomGenerator W R word)) :
    ¬ ∃ G : NativeC60AZStrictSpace (nativeK5BCSignature W)
          (NativeC60CLSelectiveRelation (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) Allowed) ⥤
          SingleObj (FreeGroup
            (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)))ᵐᵒᵖ,
        nativeC60AZStrictProject (nativeK5BCSignature W)
            (NativeC60CLSelectiveRelation (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W) Allowed) ⋙ G =
          nativeC60AZRawHolonomy (nativeK5BCSignature W)
            (nativeC60BWFreeWeight (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W)) := by
  intro hfactor
  exact nativeK5CLPhysical_selective_no_compatibility W R word
    Allowed hallow
      ((nativeC60CECompatible_iff_holonomy_factor
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (NativeC60CLSelectiveRelation (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) Allowed)).mpr hfactor)

end OriginalC60

#print axioms nativeC60CLFork_frame_raw
#print axioms nativeC60CLFork_frame_free_one_iff
#print axioms nativeC60CLFork_frame_reduced_one_iff
#print axioms nativeC60CLFork_frame_strict_one_iff
#print axioms nativeC60CLForkChain_codes
#print axioms nativeC60CLForkChain_strict_nil_iff
#print axioms nativeC60CLForkChain_no_cancel_to_nil
#print axioms nativeC60CLForkChain_nonempty_normal_form
#print axioms nativeC60CLSelective_compatible_iff
#print axioms nativeC60CLSelective_factor_iff
#print axioms nativeC60CLSelective_all_frames_iff
#print axioms nativeC60CLSame_generator_factor
#print axioms nativeK5CLPhysical_all_contexts_nontrivial
#print axioms nativeK5CLPhysical_all_contexts_no_strict_collapse
#print axioms nativeK5CLPhysical_selective_no_compatibility
#print axioms nativeK5CLPhysical_selective_no_factor

end
end Kuu.F112.Physical
