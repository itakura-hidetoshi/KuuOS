import Kuu.F112.PolygonNativeC60FiniteSignedAlternationForkPowers

/-!
# F112-P94D3CM — canonical fork powers, closed provenance, and faithful finite exponents

The earlier CM implementation in PolygonNativeC60FiniteSignedAlternationForkPowers
was merged as PR #2597. In particular it already proves genuine dependent
mixed-fork iteration, exact free-group holonomy, infinite order by a full
generator-certificate counting character, and physical nontriviality.

This module REFERS to that canonical implementation rather than creating
an independent second recursion or repeating its proof. It contributes:

* an explicit arbitrary-length closed formula for the COMPLETE ordered
  positive/negative generator-code list (not merely a successor equation);
* equality of the full typed path with the canonical earlier CM iteration;
* injectivity of the natural-number fork exponent into the original
  noncommutative free-group holonomy and into EVERY finite-context selected
  strict Hom, not just nonidentity for positive exponents;
* a necessary-and-sufficient zero-power identity criterion;
* an actual physical C60 specialization using CK's distinct original
  conservative-15D generator certificates at the SAME typed boundaries.

No new geometric filler, no extra equality of original 15D proof objects,
no Gray reintroduction, no axioms, sorry/admit, or changes to published roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Keep the preexisting PR #2598 interface but use #2597's UNIQUE
canonical original-boundary-dependent CA signed fork iteration. -/
abbrev nativeC60CMForkPowerChain {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    Nat → NativeC60CASignedChain S F a a :=
  nativeC60CMForkIter S F g h

/-- No duplicate path syntax or additional quotient is introduced:
the earlier finite-power name is exactly the canonical typed CM chain. -/
theorem nativeC60CMForkPower_eq_canonical
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (n : Nat) :
    nativeC60CMForkPowerChain S F g h n =
      nativeC60CMForkIter S F g h n := rfl

/-- NEW closed code formula for ALL finite genuine typed repetitions.
The original 16D generator certificates and BOTH signs are recorded;
no generic scalar Peiffer observer has replaced them. -/
theorem nativeC60CMForkPower_codes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    ∀ n : Nat,
      nativeC60CAChainSignedCodes S F
        (nativeC60CMForkPowerChain S F g h n) =
      (List.replicate n
        [(nativeC60BVGeneratorCode S F g, true),
         (nativeC60BVGeneratorCode S F h, false)]).flatten := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
      change
        (nativeC60BVGeneratorCode S F g, true) ::
          (nativeC60BVGeneratorCode S F h, false) ::
            nativeC60CAChainSignedCodes S F
              (nativeC60CMForkPowerChain S F g h n) =
        [(nativeC60BVGeneratorCode S F g, true),
         (nativeC60BVGeneratorCode S F h, false)] ++
          (List.replicate n
            [(nativeC60BVGeneratorCode S F g, true),
             (nativeC60BVGeneratorCode S F h, false)]).flatten
      rw [ih]
      rfl

/-- Reuse the earlier EXACT proof with the correct left-handed
group-power convention (pow_succ'); no competing induction needed. -/
theorem nativeC60CMForkPower_holonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    ∀ n : Nat,
      nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F
          (nativeC60CMForkPowerChain S F g h n)) =
        (nativeC60BWFreeHolonomy S F
          (nativeC60CKMixedFork S F g h)) ^ n := by
  intro n
  exact nativeC60CMForkIter_holonomy S F g h n

/-- Reusable Lean4 normalization of the canonical multiplicative
integer character; this is an integer identity, not torsion-freeness
postulated as an axiom. -/
theorem nativeC60CMForkPower_integer_character (n : Nat) :
    Multiplicative.toAdd ((Multiplicative.ofAdd (1 : ℤ)) ^ n) =
      (n : ℤ) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      rw [pow_succ]
      change Multiplicative.toAdd
          ((Multiplicative.ofAdd (1 : ℤ)) ^ n) + 1 =
        (Nat.succ n : ℤ)
      omega

/-- STRONGER THAN infinite order: any two nonnegative powers of the
actual mixed fork have equal complete free words iff their exponents
coincide. Uses #2597's original generator-certificate character. -/
theorem nativeC60CMForkPower_holonomy_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    Function.Injective (fun n : Nat =>
      nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F
          (nativeC60CMForkPowerChain S F g h n))) := by
  intro m n heq
  rw [nativeC60CMForkPower_holonomy S F g h m,
      nativeC60CMForkPower_holonomy S F g h n] at heq
  have hc := congrArg
    (nativeC60CMCountCertificate S (nativeC60BVGeneratorCode S F g)) heq
  simp only [map_pow, nativeC60CMCountCertificate_fork S F g h hne] at hc
  have hz := congrArg Multiplicative.toAdd hc
  rw [nativeC60CMForkPower_integer_character m,
      nativeC60CMForkPower_integer_character n] at hz
  exact_mod_cast hz

/-- The same exponent uniqueness is visible in the ACTUAL strict
groupoid Hom after ANY finite AQ frame, with no restriction on the
typed intermediate fifteen-dimensional witness sequence. -/
theorem nativeC60CMForkPower_strict_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    Function.Injective (fun n : Nat =>
      nativeC60CAChainStrictFrame S F word
        (nativeC60CMForkPowerChain S F g h n)) := by
  intro m n heq
  have hfree :=
    (nativeC60CCAll_signed_free_eq_iff_strict S F word
      (nativeC60CMForkPowerChain S F g h m)
      (nativeC60CMForkPowerChain S F g h n)).mpr heq
  have hhol :
      nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F
            (nativeC60CMForkPowerChain S F g h m)) =
        nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F
            (nativeC60CMForkPowerChain S F g h n)) := by
    calc
      _ = FreeGroup.mk (nativeC60CAChainSignedCodes S F
            (nativeC60CMForkPowerChain S F g h m)) :=
          nativeC60CAChain_holonomy S F
            (nativeC60CMForkPowerChain S F g h m)
      _ = FreeGroup.mk (nativeC60CAChainSignedCodes S F
            (nativeC60CMForkPowerChain S F g h n)) := hfree
      _ = _ := (nativeC60CAChain_holonomy S F
        (nativeC60CMForkPowerChain S F g h n)).symm
  exact nativeC60CMForkPower_holonomy_injective S F g h hne hhol

/-- In particular, an iterated mixed fork is a strict identity exactly
for exponent zero. This strengthens the old one-way n > 0 obstruction. -/
theorem nativeC60CMForkPower_strict_nil_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) (n : Nat) :
    nativeC60CAChainStrictFrame S F word
        (nativeC60CMForkPowerChain S F g h n) =
      nativeC60CAChainStrictFrame S F word
        (NativeC60CASignedChain.nil a) ↔ n = 0 := by
  constructor
  · intro heq
    cases n with
    | zero => rfl
    | succ n =>
        exact False.elim
          ((nativeC60CMForkIter_no_strict_nil S F word
            g h hne (n + 1) (Nat.zero_lt_succ n)) heq)
  · intro hzero
    cases hzero
    rfl

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

/-- The PR #2598 physical name is definitionally the original,
already-certified C60 based signed fork from canonical CM. -/
def nativeK5CMPhysicalForkPower
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (n : Nat) :
    NativeC60CASignedChain (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R))
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R)) :=
  nativeC60CMForkPowerChain
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5CKReflGenerator W R word)
    (nativeK5CKAtomGenerator W R word) n

theorem nativeK5CMPhysicalForkPower_holonomy
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (n : Nat) :
    nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)
      (nativeC60CAChainStep (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CMPhysicalForkPower W R word n)) =
      (nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeC60CKMixedFork (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)
          (nativeK5CKReflGenerator W R word)
          (nativeK5CKAtomGenerator W R word))) ^ n :=
  nativeC60CMForkPower_holonomy
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5CKReflGenerator W R word)
    (nativeK5CKAtomGenerator W R word) n

/-- Actual original C60 witnesses distinguish EVERY pair of finite
mixed-fork powers in EVERY further physical AQ context. -/
theorem nativeK5CMPhysicalForkPower_strict_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    Function.Injective (fun n : Nat =>
      nativeC60CAChainStrictFrame
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeK5CMPhysicalForkPower W R inner n)) :=
  nativeC60CMForkPower_strict_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
    (nativeK5CKReflGenerator W R inner)
    (nativeK5CKAtomGenerator W R inner)
    (nativeK5CKPhysical_parallel_generators_ne W R inner)

end PhysicalC60

#print axioms nativeC60CMForkPower_eq_canonical
#print axioms nativeC60CMForkPower_codes
#print axioms nativeC60CMForkPower_holonomy
#print axioms nativeC60CMForkPower_integer_character
#print axioms nativeC60CMForkPower_holonomy_injective
#print axioms nativeC60CMForkPower_strict_injective
#print axioms nativeC60CMForkPower_strict_nil_iff
#print axioms nativeK5CMPhysicalForkPower_holonomy
#print axioms nativeK5CMPhysicalForkPower_strict_injective

end
end Kuu.F112.Physical
