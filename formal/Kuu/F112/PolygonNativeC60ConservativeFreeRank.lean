import Kuu.F112.PolygonNativeC60PhysicalFreeIsotropy

/-!
# F112-P94D3CZ — actual conservative C60 has unbounded free rank

CY identifies the FULL original conservative strict isotropy group with
the free group of ORIGINAL typed parallel BC certificates, after any
independently chosen finite inner/outer AQ context.

Here a countably indexed family of different ORIGINAL conservative
15D certificates is constructed at ONE fixed original 14D fiber R:
the unquotiented proof terms symm^n(refl R) have different syntactic
depths. They retain EXACT original 14D boundaries, and their 16D BC
generator codes preserve the full proof trees. None equals the selected
conservative-atom base certificate.

Their distinct CN letters give an injective FreeGroup Nat homomorphism
to the ACTUAL strict isotropy group. Restriction to Fin n gives every
finite free rank with original typed witnesses. This is unbounded
PRESENTATION rank, NOT an infinite number of physical C60 vertices,
new geometric 16-cells or a claim of exact cardinality/rank of ALL
raw certificates. No extra relations, Peiffer, Gray, axioms or sorry.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

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

/-- A countably infinite sequence of ORIGINAL conservative raw 15D
cores. Each term remains a complete original 14D-to-14D proof, without
quotienting out inverse-of-inverse steps or filling higher coherence. -/
def nativeK5CZCore
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (n : Nat) → NativeObserverCoreFifteenCell
      (nativeK5FifteenHistoryObserver W)
      (nativeK5FifteenChargeObserver W) R R
  | 0 => .refl R
  | n + 1 => .symm (nativeK5CZCore W R n)

/-- An independent structural fingerprint of ORIGINAL conservative
proof syntax. There is no descent to a geometric 15D quotient. -/
def nativeK5CZCoreIndex
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} :
    NativeObserverCoreFifteenCell
      (nativeK5FifteenHistoryObserver W)
      (nativeK5FifteenChargeObserver W) R S → Option Nat
  | .refl _ => some 0
  | .atom _ _ => none
  | .symm c => (nativeK5CZCoreIndex W c).map Nat.succ
  | .trans _ _ => none

theorem nativeK5CZCoreIndex_core
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (n : Nat) :
    nativeK5CZCoreIndex W (nativeK5CZCore W R n) = some n := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change (nativeK5CZCoreIndex W (nativeK5CZCore W R n)).map Nat.succ =
        some (n + 1)
      rw [ih]
      rfl

/-- The original 15D term, conserving the same actual 14D endpoints. -/
def nativeK5CZCell
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (n : Nat) :
    NativeK5AQFifteenCell W R R :=
  .conservative (nativeK5CZCore W R n)

/-- The COMPLETE original BW 16D code contains the original 15D core.
Unlike a scalar charge, this readout distinguishes every symm-depth. -/
def nativeK5CZCodeIndex
    (W : NativeK5StructuralThirteenCell p U V)
    (code : NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)) : Option Nat :=
  match code.2.2.2.2.2.val with
  | .conservative core => nativeK5CZCoreIndex W core
  | _ => none

/-- Genuine, dependent, parallel physical BC generator for every n;
all 14D/15D endpoints coincide with the ORIGINAL conservative refl
boundary. Only the raw Type-valued certificate differs. -/
def nativeK5CZGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) (n : Nat) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W inner (nativeK5CKConservativeRefl W R)) :=
  nativeK5CHPositiveGenerator W inner (nativeK5CZCell W R n)

/-- The complete original 16D provenance differentiates every n. -/
theorem nativeK5CZCodeIndex_generator
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) (n : Nat) :
    nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CZGenerator W R inner n)) =
      some n := by
  change nativeK5CZCoreIndex W (nativeK5CZCore W R n) = some n
  exact nativeK5CZCoreIndex_core W R n

/-- The actual selected atom is NOT any symm-iterated conservative
refl term. The two outer conservative constructors are not equated;
their internal Type-valued AX data distinguish them. -/
theorem nativeK5CZCodeIndex_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) :
    nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5CKAtomGenerator W R inner)) =
      none := by
  rfl

/-- Countably many ACTUAL original generators, each with exactly the
same 15D endpoints, are pairwise different as 16D proof certificates. -/
theorem nativeK5CZGenerator_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) :
    Function.Injective (nativeK5CZGenerator W R inner) := by
  intro n m h
  have hc := congrArg (fun gen =>
    nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) gen)) h
  rw [nativeK5CZCodeIndex_generator, nativeK5CZCodeIndex_generator] at hc
  exact Option.some.inj hc

theorem nativeK5CZGenerator_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) (n : Nat) :
    nativeK5CZGenerator W R inner n ≠
      nativeK5CKAtomGenerator W R inner := by
  intro h
  have hc := congrArg (fun gen =>
    nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) gen)) h
  rw [nativeK5CZCodeIndex_generator, nativeK5CZCodeIndex_atom] at hc
  cases hc

/-- Original proof-carrying CN alphabet indexed by natural numbers. -/
def nativeK5CZLetter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) (n : Nat) :
    NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner) :=
  ⟨nativeK5CZGenerator W R inner n,
    nativeK5CZGenerator_ne_atom W R inner n⟩

theorem nativeK5CZLetter_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) :
    Function.Injective (nativeK5CZLetter W R inner) := by
  intro n m h
  exact nativeK5CZGenerator_injective W R inner (congrArg Subtype.val h)

/-- At least countably infinitely many different ORIGINAL CN letters
live at a single fixed C60 conservative 14D fiber. This is not an
exact cardinality statement about all possible physical 16D terms. -/
theorem nativeK5CZPhysical_CNAlphabet_infinite
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) :
    Infinite (NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :=
  Infinite.of_injective (nativeK5CZLetter W R inner)
    (nativeK5CZLetter_injective W R inner)

/-- Actual strict isotropy contains a faithfully embedded FREE GROUP
on infinitely many independently certified original 16D generators.
The isomorphism is CY's proven strict one, not a numerical receiver. -/
def nativeK5CZFreeNatEmbed
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    FreeGroup Nat →*
      NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) :=
  (nativeK5CYPhysicalFreeIsotropy W R inner outer).toMonoidHom.comp
    (FreeGroup.map (nativeK5CZLetter W R inner))

theorem nativeK5CZFreeNatEmbed_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    Function.Injective (nativeK5CZFreeNatEmbed W R inner outer) :=
  (nativeK5CYPhysicalFreeIsotropy W R inner outer).injective.comp
    (FreeGroup.map_injective (nativeK5CZLetter_injective W R inner))

/-- EVERY finite rank embeds faithfully inside the same original
finite C60 geometry, with no generators beyond its native Type syntax. -/
def nativeK5CZFreeFinEmbed
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (N : Nat) :
    FreeGroup (Fin N) →*
      NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) :=
  (nativeK5CYPhysicalFreeIsotropy W R inner outer).toMonoidHom.comp
    (FreeGroup.map (fun i : Fin N => nativeK5CZLetter W R inner i.val))

theorem nativeK5CZFreeFinEmbed_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (N : Nat) :
    Function.Injective (nativeK5CZFreeFinEmbed W R inner outer N) := by
  have h : Function.Injective
      (fun i : Fin N => nativeK5CZLetter W R inner i.val) := by
    intro i j eq
    apply Fin.ext
    exact nativeK5CZLetter_injective W R inner eq
  exact (nativeK5CYPhysicalFreeIsotropy W R inner outer).injective.comp
    (FreeGroup.map_injective h)

/-- The ACTUAL strict isotropy group cannot be finite, even though
its original C60 geometry is finite: the proof-syntax rank is unbounded. -/
theorem nativeK5CZPhysical_strict_isotropy_infinite
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    Infinite (NativeC60COIsotropy
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) :=
  Infinite.of_injective
    (fun n : Nat => nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n))
    ((nativeK5CZFreeNatEmbed_injective W R inner outer).comp
      FreeGroup.of_injective)

#print axioms nativeK5CZCore
#print axioms nativeK5CZCoreIndex
#print axioms nativeK5CZCoreIndex_core
#print axioms nativeK5CZCell
#print axioms nativeK5CZCodeIndex
#print axioms nativeK5CZGenerator
#print axioms nativeK5CZCodeIndex_generator
#print axioms nativeK5CZCodeIndex_atom
#print axioms nativeK5CZGenerator_injective
#print axioms nativeK5CZGenerator_ne_atom
#print axioms nativeK5CZLetter
#print axioms nativeK5CZLetter_injective
#print axioms nativeK5CZPhysical_CNAlphabet_infinite
#print axioms nativeK5CZFreeNatEmbed
#print axioms nativeK5CZFreeNatEmbed_injective
#print axioms nativeK5CZFreeFinEmbed
#print axioms nativeK5CZFreeFinEmbed_injective
#print axioms nativeK5CZPhysical_strict_isotropy_infinite

end
end Kuu.F112.Physical
