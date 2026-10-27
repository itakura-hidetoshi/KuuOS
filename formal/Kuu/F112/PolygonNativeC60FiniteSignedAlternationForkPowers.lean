import Kuu.F112.PolygonNativeC60SelectiveMixedForkDescent

/-!
# F112-P94D3CM — finite alternating physical 16D paths and powers of a genuine fork

CJ proves that no two genuine positively oriented BC primitives can
compose anywhere in the ACTUAL C60 dependent 15D object fiber. The
same theorem, applied in the reverse order, prohibits two successive
negative-oriented primitives.

CM gives a structural description of EVERY finite proof-bearing signed
16D chain in the native selected BC presentation: its sequence of
orientations alternates strictly. This is not a restriction assumed on
paths or deduced from a scalar observer. It follows from actual typed
nonexistence of the middle positive/positive (or negative/negative)
15D endpoint.

The CC normalization theorem therefore provides a genuinely dependent
alternating reduced normal form for EVERY finite signed chain, retaining
the exact original 15D beginning/end and arbitrary intermediate evidence.

CK's physical pair of distinct parallel genuine BC generators yields
an actual based, alternating, signed fork loop. We build its iteration
of every finite length in CA's dependent path grammar. A homomorphism
from the complete noncommutative free group to Multiplicative Int,
counting one fixed ORIGINAL generator certificate, proves that the
nontrivial fork has infinite order. Every nonempty finite iterate
remains nontrivial after EVERY finite AQ context, and no permitted
finite typed inverse-cancellation chain can erase it.

This does not assert a new geometric 16D filler, global strict
horizontal Peiffer, Gray, P92B descent, or strict n/infinity
hyperdescent; the already selected optional BC presentation and
its complete free receiver are fixed. No axioms or sorry/admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- The actual list of signs of a dependent signed path. This is
extracted from the WHOLE typed 16D chain and not supplied as an
unrelated graph-level walk. -/
def nativeC60CMSignWord {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} → NativeC60CASignedChain S F a b → List Bool
  | _, _, .nil _ => []
  | _, _, .pos _ tail => true :: nativeC60CMSignWord S F tail
  | _, _, .neg _ tail => false :: nativeC60CMSignWord S F tail

/-- Strictly alternating signs of an arbitrary finite length. Unlike
List.Pairwise, only ADJACENT orientations must be different. -/
def NativeC60CMAlternating : List Bool → Prop
  | [] => True
  | _ :: [] => True
  | x :: y :: tail => x ≠ y ∧ NativeC60CMAlternating (y :: tail)

/-- The physical BC signature contains no two successive inversely
oriented (negative/negative) genuine generators. Their original
positive arrows would compose in the reverse order, contrary to CJ. -/
theorem nativeK5CMNo_negative_negative
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    {U V : NativeK5StructuralTwelveCell p H K}
    (W : NativeK5StructuralThirteenCell p U V)
    {a₀ b₀ c₀ : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen b₀ a₀)
    (h : (nativeK5BCSignature W).Gen c₀ b₀) : False :=
  nativeK5CJNo_composable_positive_generators W h ⟨g⟩

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

/-- Every arbitrarily long genuine dependent signed 16D chain must
alternate in sign. In particular this checks *every* intermediate
original fifteen-dimensional object, not merely its endpoints. -/
theorem nativeK5CMAll_signed_chains_alternate
    (W : NativeK5StructuralThirteenCell p U V) :
    ∀ {a b : (nativeK5AXBaseLayer W).Total}
      (chain : NativeC60CASignedChain
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) a b),
      NativeC60CMAlternating
        (nativeC60CMSignWord (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) chain) := by
  intro a b chain
  induction chain with
  | nil x =>
      trivial
  | pos g tail ih =>
      cases tail with
      | nil _ =>
          trivial
      | pos h rest =>
          exact False.elim (nativeK5CJNo_composable_positive_generators W g ⟨h⟩)
      | neg h rest =>
          exact ⟨by decide, ih⟩
  | neg g tail ih =>
      cases tail with
      | nil _ =>
          trivial
      | neg h rest =>
          exact False.elim (nativeK5CMNo_negative_negative W g h)
      | pos h rest =>
          exact ⟨by decide, ih⟩

/-- CC's unconditional all-finite normalization can be sharpened for
the TRUE native C60 BC signature: the reduced typed path is also
strictly alternating, without a separate graph or quotient model. -/
theorem nativeK5CMEvery_signed_chain_normalizes_alternating
    (W : NativeK5StructuralThirteenCell p U V)
    {a b : (nativeK5AXBaseLayer W).Total}
    (chain : NativeC60CASignedChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) a b) :
    ∃ reduced : NativeC60CASignedChain
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) a b,
      Relation.ReflTransGen
        (fun x y : NativeC60CASignedChain
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) a b =>
            NativeC60CAElementaryCancel
              (nativeK5AXKuuSignature W) (nativeK5BCFrame W) x y)
        chain reduced ∧
      FreeGroup.IsReduced (nativeC60CAChainSignedCodes
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) reduced) ∧
      NativeC60CMAlternating (nativeC60CMSignWord
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) reduced) := by
  obtain ⟨q, hsteps, hred⟩ :=
    nativeC60CCEvery_signed_chain_normalizes
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) chain
  exact ⟨q, hsteps, hred, nativeK5CMAll_signed_chains_alternate W q⟩

end OriginalC60

/-- A genuine, arbitrary-length iteration of the original CK
two-edge fork in the DEPENDENT CA signed 16D path syntax.
It is a based loop at the same proof-relevant original 15D object. -/
def nativeC60CMForkIter
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    Nat → NativeC60CASignedChain S F a a
  | 0 => .nil a
  | n + 1 => .pos g (.neg h (nativeC60CMForkIter S F g h n))

/-- Every finite CK iteration records exactly the two SIGNED full
generator codes followed by the complete original typed tail. -/
theorem nativeC60CMForkIter_codes_succ
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (n : Nat) :
    nativeC60CAChainSignedCodes S F
        (nativeC60CMForkIter S F g h (n + 1)) =
      (nativeC60BVGeneratorCode S F g, true) ::
        (nativeC60BVGeneratorCode S F h, false) ::
          nativeC60CAChainSignedCodes S F
            (nativeC60CMForkIter S F g h n) := rfl

/-- The entire original typed iterated CK path has free holonomy the
natural-number power of its original noncommutative mixed-fork word. -/
theorem nativeC60CMForkIter_holonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (n : Nat) :
    nativeC60BWFreeHolonomy S F
      (nativeC60CAChainStep S F (nativeC60CMForkIter S F g h n)) =
      (nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h)) ^ n := by
  induction n with
  | zero =>
      rfl
  | succ n ih =>
      change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          ((FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ *
            nativeC60BWFreeHolonomy S F
              (nativeC60CAChainStep S F (nativeC60CMForkIter S F g h n))) =
        (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) ^ (n + 1)
      rw [ih, pow_succ']
      group

/-- A character of the complete ORIGINAL 16D noncommutative free group.
It counts the distinguished FULL higher generator certificate, without
collapsing unrelated original 15D proof constructors by fiat. -/
noncomputable def nativeC60CMCountCertificate
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (code : NativeC60BVGeneratorCode S) :
    FreeGroup (NativeC60BVGeneratorCode S) →* Multiplicative ℤ := by
  classical
  exact FreeGroup.lift
    (fun x => if x = code then Multiplicative.ofAdd (1 : ℤ) else 1)

/-- A fork built from two DISTINCT actual BC generator certificates
has nonzero exponent of the chosen first generator: +1, not zero. -/
theorem nativeC60CMCountCertificate_fork
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) :
    nativeC60CMCountCertificate S (nativeC60BVGeneratorCode S F g)
      (nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h)) =
        Multiplicative.ofAdd (1 : ℤ) := by
  classical
  have hcode : nativeC60BVGeneratorCode S F h ≠
      nativeC60BVGeneratorCode S F g := by
    intro eqcode
    exact hne (nativeC60BVGeneratorCode_injective S F eqcode.symm)
  change nativeC60CMCountCertificate S (nativeC60BVGeneratorCode S F g)
    (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) =
        Multiplicative.ofAdd (1 : ℤ)
  rw [map_mul, map_inv]
  simp [nativeC60CMCountCertificate, hcode]

/-- A nontrivial original mixed fork has infinite order. The proof
does NOT just assume torsion-freeness: the full original generator
certificate is evaluated by a genuine FreeGroup.lift into integers. -/
theorem nativeC60CMFork_power_ne_one
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) (n : Nat) (hn : 0 < n) :
    (nativeC60BWFreeHolonomy S F (nativeC60CKMixedFork S F g h)) ^ n ≠
      (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
  intro heq
  have hm := congrArg
    (nativeC60CMCountCertificate S (nativeC60BVGeneratorCode S F g)) heq
  rw [map_pow, map_one, nativeC60CMCountCertificate_fork S F g h hne] at hm
  have hp :
      ∀ k : Nat,
        Multiplicative.toAdd ((Multiplicative.ofAdd (1 : ℤ)) ^ k) =
          (k : ℤ) := by
    intro k
    induction k with
    | zero => rfl
    | succ k ih =>
        rw [pow_succ]
        change Multiplicative.toAdd
            ((Multiplicative.ofAdd (1 : ℤ)) ^ k) + 1 =
          (Nat.succ k : ℤ)
        omega
  have hzero := congrArg Multiplicative.toAdd hm
  rw [hp n] at hzero
  have hzero' : (n : ℤ) = 0 := by simpa using hzero
  omega

/-- Every POSITIVE finite iteration of a genuine mixed fork has
nontrivial complete free 16D holonomy, with ALL intermediate 15D
proof objects still carried by the original typed CA chain. -/
theorem nativeC60CMForkIter_nontrivial
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) (n : Nat) (hn : 0 < n) :
    nativeC60BWFreeHolonomy S F
      (nativeC60CAChainStep S F (nativeC60CMForkIter S F g h n)) ≠
        (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
  rw [nativeC60CMForkIter_holonomy S F g h n]
  exact nativeC60CMFork_power_ne_one S F g h hne n hn

/-- No nonempty positive iteration of the CK fork can become an
identity in the selected strict Kuu Hom, at ANY genuine finite
physical context. This follows from CC's actual finite signed
path strict/free faithfulness and the exponent obstruction. -/
theorem nativeC60CMForkIter_no_strict_nil
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) (n : Nat) (hn : 0 < n) :
    nativeC60CAChainStrictFrame S F word (nativeC60CMForkIter S F g h n) ≠
      nativeC60CAChainStrictFrame S F word (.nil a) := by
  intro hstrict
  have hfree :=
    (nativeC60CCAll_signed_free_eq_iff_strict S F word
      (nativeC60CMForkIter S F g h n) (.nil a)).mpr hstrict
  have hh : nativeC60BWFreeHolonomy S F
      (nativeC60CAChainStep S F (nativeC60CMForkIter S F g h n)) =
      (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
    calc
      _ = FreeGroup.mk (nativeC60CAChainSignedCodes S F
          (nativeC60CMForkIter S F g h n)) :=
        (nativeC60CAChain_holonomy S F _).symm
      _ = FreeGroup.mk (nativeC60CAChainSignedCodes S F
          (NativeC60CASignedChain.nil a)) := hfree
      _ = 1 := rfl
  exact nativeC60CMForkIter_nontrivial S F g h hne n hn hh

/-- EVERY allowed finite typed cancellation-normalization of a
positive iterate must retain a NONEMPTY canonical reduced chain.
This combines the genuinely typed CC normal form, CA cancellation
soundness and the new full free-group exponent obstruction. -/
theorem nativeC60CMForkIter_nonempty_normal_form
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b)
    (hne : g ≠ h) (n : Nat) (hn : 0 < n) :
    ∃ q : NativeC60CASignedChain S F a a,
      Relation.ReflTransGen
        (fun x y : NativeC60CASignedChain S F a a =>
          NativeC60CAElementaryCancel S F x y)
        (nativeC60CMForkIter S F g h n) q ∧
      FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q) ∧
      q ≠ .nil a := by
  obtain ⟨q, hsteps, hred⟩ :=
    nativeC60CCEvery_signed_chain_normalizes S F
      (nativeC60CMForkIter S F g h n)
  refine ⟨q, hsteps, hred, ?_⟩
  intro hnileq
  cases hnileq
  have hstrict := nativeC60CAFiniteCancellation_sound S F [] hsteps
  exact (nativeC60CMForkIter_no_strict_nil S F [] g h hne n hn) hstrict

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

/-- The actual physical CK conservative-generator fork has nontrivial
free-group power for EVERY positive n, independently of inner and
outer finite genuine original C60 AQ contexts. -/
theorem nativeK5CMPhysical_all_fork_powers_strict_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (n : Nat) (hn : 0 < n) :
    nativeC60CAChainStrictFrame
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeC60CMForkIter (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W)
          (nativeK5CKReflGenerator W R inner)
          (nativeK5CKAtomGenerator W R inner) n) ≠
      nativeC60CAChainStrictFrame
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (.nil (nativeK5CHSource W inner
          (nativeK5CKConservativeRefl W R))) :=
  nativeC60CMForkIter_no_strict_nil
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
    (nativeK5CKReflGenerator W R inner)
    (nativeK5CKAtomGenerator W R inner)
    (nativeK5CKPhysical_parallel_generators_ne W R inner) n hn

end PhysicalC60

#print axioms nativeK5CMNo_negative_negative
#print axioms nativeK5CMAll_signed_chains_alternate
#print axioms nativeK5CMEvery_signed_chain_normalizes_alternating
#print axioms nativeC60CMForkIter_codes_succ
#print axioms nativeC60CMForkIter_holonomy
#print axioms nativeC60CMCountCertificate_fork
#print axioms nativeC60CMFork_power_ne_one
#print axioms nativeC60CMForkIter_nontrivial
#print axioms nativeC60CMForkIter_no_strict_nil
#print axioms nativeC60CMForkIter_nonempty_normal_form
#print axioms nativeK5CMPhysical_all_fork_powers_strict_nontrivial

end
end Kuu.F112.Physical
