import Kuu.F112.PolygonNativeC60GlobalPositiveConnectivityObstruction

/-!
# F112-P94D3CK — physical mixed-sign two-edge holonomy obstruction

CJ excludes ALL consecutive positive 16D BC generators, including the
conservative-input case, in the selected C60 context-closed signature.
The reverse obstruction similarly excludes two consecutive negatives.
This leaves genuine mixed positive-negative and negative-positive paths.

The complete free-group receiver distinguishes the two-edge positive-
negative loop made from distinct, parallel BC generators: its free
holonomy is g*h⁻¹, which is trivial precisely when the ORIGINAL typed
generators themselves coincide.

In the ORIGINAL C60 15D conservative grammar, .refl R and .atom rfl rfl
are distinct proof-relevant conservative evidence for the same 14D
boundary. True AU naturality applies actual physical 14D whiskerings
to this evidence. The whiskering constructor deliberately replaces a
conservative proof tree by a single observer-conservative .atom; the
distinct original 15D input certificates therefore yield the SAME
concrete source-first and target-first AU naturality proof terms,
while the 16D BC generator codes still remember the different input
certificates.

This yields a genuinely physical pair of distinct, parallel positive
16D primitives, and hence a nontrivial mixed-sign 2-edge LOOP in the
selected strict Kuu quotient, even though no positive-positive or
negative-negative 2-edge path exists.

A proposed 'all mixed forks collapse' geometric 16D relation preserves
the original complete receiver iff ALL parallel BC generators are
equal. The physical pair defeats that condition and prevents the
complete free receiver from descending to such an extra relation.
The compatible triangle/cancellation relation from CF remains intact.

No new geometric 16D filler, equality of raw 15D evidence, scalar
Peiffer-only identification, global Peiffer interchange, Gray,
strict-n or infinity-hyperdescent is asserted. No axioms/sorry/admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A typed mixed-sign two-edge path across two genuine positive BC
generators sharing an exact original 15D source AND target. The path
is a raw loop, not an assumed higher-dimensional geometric filler. -/
def nativeC60CKMixedFork {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) a a :=
  .trans (.atom g) (.symm (.atom h))

/-- Complete 16D noncommutative holonomy detects EXACT equality of
the genuine original generator certificates, not merely Peiffer values. -/
theorem nativeC60CKMixedFork_free_one_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h) =
      (1 : FreeGroup (NativeC60BVGeneratorCode S)) ↔ g = h := by
  constructor
  · intro hfree
    have hmul :
        FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ = 1 := by
      exact hfree
    have heq :
        FreeGroup.of (nativeC60BVGeneratorCode S F g) =
          FreeGroup.of (nativeC60BVGeneratorCode S F h) := by
      calc
        FreeGroup.of (nativeC60BVGeneratorCode S F g) =
          (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
            (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) *
              FreeGroup.of (nativeC60BVGeneratorCode S F h) := by group
        _ = FreeGroup.of (nativeC60BVGeneratorCode S F h) := by rw [hmul]; simp
    exact nativeC60BVGeneratorCode_injective S F (FreeGroup.of_injective heq)
  · intro heq
    subst h
    change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F g))⁻¹ = 1
    exact mul_inv_cancel _

/-- A geometric proposal that contracts ANY two-edge mixed fork.
It is a RELATION CANDIDATE, not an asserted 17D or geometric 16D
coherence witness. All endpoints remain proof-relevant. -/
inductive NativeC60CKMixedForkRelation
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b → Prop where
  | fork {a b : L.Total}
      (g h : (nativeC60BCClosedSignature S F).Gen a b) :
      NativeC60CKMixedForkRelation S F
        (nativeC60CKMixedFork S F g h) (.refl a)

/-- Exact criterion for the mixed-fork contraction presentation to
retain the entire chosen free-group receiver: all genuine parallel
BC generators would have to be identical. -/
theorem nativeC60CKFork_relation_compatible_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60CEGeometricCompatible S F (NativeC60CKMixedForkRelation S F) ↔
      ∀ {a b : L.Total}
        (g h : (nativeC60BCClosedSignature S F).Gen a b), g = h := by
  constructor
  · intro hc a b g h
    have hfree := hc (nativeC60CKMixedFork S F g h)
      (NativeC60AXStep.refl a) (.fork g h)
    exact (nativeC60CKMixedFork_free_one_iff S F g h).mp hfree
  · intro hh a b p q rel
    cases rel with
    | fork g h =>
        have heq := hh g h
        subst h
        change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F g))⁻¹ = 1
        exact mul_inv_cancel _

/-- The physical obstruction to trying to contract a noncanceling
mixed-sign loop is already visible at the complete free-word level. -/
theorem nativeC60CKDistinct_fork_nontrivial
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h) ≠
      (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
  intro hf
  exact hne ((nativeC60CKMixedFork_free_one_iff S F g h).mp hf)

/-- Since the free receiver remains exact under EVERY finite context,
an irreducible physical mixed fork cannot be strictified to identity
in the selected no-extra-relations Kuu quotient. -/
theorem nativeC60CKDistinct_fork_no_strict_identity
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (nativeC60CKMixedFork S F g h)) ≠
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.refl a)) :=
  nativeC60CEHolonomyMismatch_all_frames S F
    (nativeC60CKMixedFork S F g h) (.refl a)
    (nativeC60CKDistinct_fork_nontrivial S F g h hne) word

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

/-- First genuine conservative 15D witness on the original proof
fiber. Its .refl constructor is retained as Type-valued evidence. -/
def nativeK5CKConservativeRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W R R :=
  .conservative (.refl R)

/-- Second, syntactically INDEPENDENT observer-conservative witness
at the exact same dependent lower boundary. -/
def nativeK5CKConservativeAtom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W R R :=
  .conservative (.atom rfl rfl)

/-- These two concrete original AQ proofs are NOT equal as raw
Type-valued 15D constructor trees. -/
theorem nativeK5CKConservatives_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5CKConservativeRefl W R ≠
      nativeK5CKConservativeAtom W R := by
  intro heq
  cases heq

/-- Both actual AU naturality routes have the same raw, typed proof
terms once their native 14D whiskerings have normalized the two
conservative cores. This does NOT identify the original inputs. -/
theorem nativeK5CKRefl_atom_source_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5CHSource W word (nativeK5CKConservativeRefl W R) =
      nativeK5CHSource W word (nativeK5CKConservativeAtom W R) := by
  rfl

theorem nativeK5CKRefl_atom_target_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5CHTarget W word (nativeK5CKConservativeRefl W R) =
      nativeK5CHTarget W word (nativeK5CKConservativeAtom W R) := by
  rfl

/-- Retain the TWO different original 15D witnesses as different
genuine 16D generator certificates, but with their exact same
contextual source and target 15D objects. -/
def nativeK5CKReflGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R)) :=
  nativeK5CHPositiveGenerator W word (nativeK5CKConservativeRefl W R)

def nativeK5CKAtomGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R)) := by
  rw [nativeK5CKRefl_atom_source_eq W R word,
    nativeK5CKRefl_atom_target_eq W R word]
  exact nativeK5CHPositiveGenerator W word (nativeK5CKConservativeAtom W R)

/-- The BC 16D generator codes still retain the ORIGINAL different
conservative proof constructors even when their AU route endpoints agree. -/
theorem nativeK5CKPhysical_parallel_generators_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5CKReflGenerator W R word ≠
      nativeK5CKAtomGenerator W R word := by
  intro h
  have hc := congrArg
    (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)) h
  have hinput :
      nativeK5CKConservativeRefl W R =
        nativeK5CKConservativeAtom W R := by
    cases hc
  exact nativeK5CKConservatives_raw_ne W R hinput

/-- An ACTUAL original C60 signed two-edge loop with TWO unequal
higher generator certificates and nonidentity free 16D holonomy.
Its 15D source and target are literally the same typed proof object. -/
theorem nativeK5CKPhysical_mixed_fork_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60CKMixedFork (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)
          (nativeK5CKReflGenerator W R word)
          (nativeK5CKAtomGenerator W R word)) ≠
      (1 : FreeGroup (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W))) :=
  nativeC60CKDistinct_fork_nontrivial
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5CKReflGenerator W R word)
    (nativeK5CKAtomGenerator W R word)
    (nativeK5CKPhysical_parallel_generators_ne W R word)

/-- No complete free-holonomy receiver descends through a relation
contracting ALL mixed forks for this original physical C60 signature. -/
theorem nativeK5CKPhysical_no_mixed_fork_receiver
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ NativeC60CEGeometricCompatible (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)
      (NativeC60CKMixedForkRelation (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)) := by
  intro hc
  let R := nativeK5FifteenCriticalLeft W
  have hparallel :
      ∀ {a b : (nativeK5AXBaseLayer W).Total}
        (g h : (nativeK5BCSignature W).Gen a b), g = h :=
    (nativeC60CKFork_relation_compatible_iff
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).mp hc
  exact nativeK5CKPhysical_parallel_generators_ne W R []
    (hparallel (nativeK5CKReflGenerator W R [])
      (nativeK5CKAtomGenerator W R []))

end OriginalC60

#print axioms nativeC60CKMixedFork_free_one_iff
#print axioms nativeC60CKFork_relation_compatible_iff
#print axioms nativeC60CKDistinct_fork_nontrivial
#print axioms nativeC60CKDistinct_fork_no_strict_identity
#print axioms nativeK5CKConservatives_raw_ne
#print axioms nativeK5CKRefl_atom_source_eq
#print axioms nativeK5CKRefl_atom_target_eq
#print axioms nativeK5CKPhysical_parallel_generators_ne
#print axioms nativeK5CKPhysical_mixed_fork_nontrivial
#print axioms nativeK5CKPhysical_no_mixed_fork_receiver

end
end Kuu.F112.Physical
