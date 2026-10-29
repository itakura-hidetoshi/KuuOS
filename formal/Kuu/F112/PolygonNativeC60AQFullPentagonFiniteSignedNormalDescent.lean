import Kuu.F112.PolygonNativeC60AQFullPentagonNineteenOrderedFactor
import Kuu.F112.PolygonNativeC60PentagonNormalClosureDescent

/-!
# F112-P94D3EY — finite ordered signed 19D defects and exact normal descent

Flatten the ACTUAL dependent four-constructor NativeC60AXStep syntax into a
finite ordered list of original typed generators with an occurrence sign.
Reversal reverses the entire list AND inverts each signed occurrence.
No generator is replaced by a scalar/graph edge, and no commutation is used.

The noncommutative product of these signed defects equals EX's exact group
fold and its original H(source)⁻¹ * H(target) endpoint ratio. For ANY
selected set of original typed atoms, coverage of a path's actual signed
occurrences implies that the whole path defect belongs to the DT minimal
normal closure of the selected atomic defects. A receiver factors through
that explicit relative quotient iff it kills every selected atomic defect.

This is an algebraic, selected relative presentation: never equality of
distinct original complete 18D Type-valued witnesses. No actual geometric
19D filler is constructed. Keep strict Kuu, independent Kuu presentation,
DS complete-evidence no-go, all 14D--18D evidence, 107 public roots,
no Gray, pinned Lean/mathlib, append-only and same-root.
No new axioms, sorry, admit, or arbitrary abelianization.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w

section SignedFullPathNormalClosure

variable {L : NativeC60AXLayer.{u}}
variable (T : NativeC60AXSignature L)

/-- A primitive of the ORIGINAL dependent signature, retaining both
boundaries and its original generator, rather than only its shadow. -/
structure NativeC60EYPrimitive where
  source : L.Total
  target : L.Total
  generator : T.Gen source target

/-- An occurrence of a real primitive with its signed orientation. -/
structure NativeC60EYSignedPrimitive where
  primitive : NativeC60EYPrimitive T
  backwards : Bool

/-- Inversion changes only the occurrence orientation, never the
underlying original dependent generator or its evidence boundaries. -/
def nativeC60EYFlip (a : NativeC60EYSignedPrimitive T) :
    NativeC60EYSignedPrimitive T :=
  ⟨a.primitive, !a.backwards⟩

/-- Flatten the original Type-valued signed/composite path into its
finite sequence of genuine typed signed primitive occurrences.
The inverse case MUST reverse order in a noncommutative group. -/
def nativeC60EYSignedAtoms {x y : L.Total}
    (p : NativeC60AXStep T x y) : List (NativeC60EYSignedPrimitive T) :=
  p.fold
    (fun {a b} (g : T.Gen a b) =>
      [⟨⟨a, b, g⟩, false⟩])
    (fun _ => [])
    (fun xs => xs.reverse.map (nativeC60EYFlip T))
    (fun xs ys => xs ++ ys)

section GroupValued

variable {G : Type v} [Group G] (obs : L.Total → G)

/-- Complete noncommutative defect of an ORIGINAL typed primitive. -/
def nativeC60EYPrimitiveDefect (a : NativeC60EYPrimitive T) : G :=
  (obs a.source)⁻¹ * obs a.target

/-- The sign applies to the whole noncommutative atomic ratio. -/
def nativeC60EYSignedDefect (a : NativeC60EYSignedPrimitive T) : G :=
  if a.backwards then
    (nativeC60EYPrimitiveDefect T obs a.primitive)⁻¹
  else nativeC60EYPrimitiveDefect T obs a.primitive

theorem nativeC60EYSignedDefect_flip
    (a : NativeC60EYSignedPrimitive T) :
    nativeC60EYSignedDefect T obs (nativeC60EYFlip T a) =
      (nativeC60EYSignedDefect T obs a)⁻¹ := by
  cases a with
  | mk atom backwards =>
      cases backwards <;>
        simp [nativeC60EYFlip, nativeC60EYSignedDefect]

/-- Ordered finite product of every signed genuine primitive of the
given original Type-valued path. No abelianization or sorting. -/
def nativeC60EYOrderedDefect {x y : L.Total}
    (p : NativeC60AXStep T x y) : G :=
  ((nativeC60EYSignedAtoms T p).map
    (nativeC60EYSignedDefect T obs)).prod

/-- Fundamental group identity for the FULL reversed signed word. -/
theorem nativeC60EYReverseFlipProduct
    (xs : List (NativeC60EYSignedPrimitive T)) :
    (((xs.reverse.map (nativeC60EYFlip T)).map
      (nativeC60EYSignedDefect T obs)).prod) =
      ((xs.map (nativeC60EYSignedDefect T obs)).prod)⁻¹ := by
  induction xs with
  | nil => simp
  | cons atom rest ih =>
      calc
        ((((atom :: rest).reverse.map (nativeC60EYFlip T)).map
          (nativeC60EYSignedDefect T obs)).prod) =
            (((rest.reverse.map (nativeC60EYFlip T)).map
              (nativeC60EYSignedDefect T obs)).prod) *
              nativeC60EYSignedDefect T obs
                (nativeC60EYFlip T atom) := by
                  simp [List.map_append, List.prod_append]
        _ = ((rest.map (nativeC60EYSignedDefect T obs)).prod)⁻¹ *
              (nativeC60EYSignedDefect T obs atom)⁻¹ := by
                rw [ih, nativeC60EYSignedDefect_flip]
        _ = (((atom :: rest).map
              (nativeC60EYSignedDefect T obs)).prod)⁻¹ := by
                simp [mul_inv_rev]

/-- Every four-constructor original typed path is EXACTLY the ordered
product of its finite signed primitive occurrences, as evaluated by EX.
Importantly, a nested symm reverses ORDER, not only individual signs. -/
theorem nativeC60EYOrderedDefect_eq_EX :
    ∀ {x y : L.Total} (p : NativeC60AXStep T x y),
      nativeC60EYOrderedDefect T obs p =
        nativeC60EXFoldDefect T obs p := by
  intro x y p
  induction p with
  | atom g =>
      simp [nativeC60EYOrderedDefect, nativeC60EYSignedAtoms,
        nativeC60EYSignedDefect, nativeC60EYPrimitiveDefect,
        nativeC60EXFoldDefect]
  | refl a =>
      simp [nativeC60EYOrderedDefect, nativeC60EYSignedAtoms,
        nativeC60EXFoldDefect]
  | symm p ih =>
      change (((nativeC60EYSignedAtoms T p).reverse.map
        (nativeC60EYFlip T)).map
          (nativeC60EYSignedDefect T obs)).prod =
          (nativeC60EXFoldDefect T obs p)⁻¹
      rw [nativeC60EYReverseFlipProduct T obs]
      simpa only [nativeC60EYOrderedDefect] using
        congrArg (fun t : G => t⁻¹) ih
  | trans p q ihp ihq =>
      change (((nativeC60EYSignedAtoms T p ++
        nativeC60EYSignedAtoms T q).map
          (nativeC60EYSignedDefect T obs)).prod) =
        nativeC60EXFoldDefect T obs p *
          nativeC60EXFoldDefect T obs q
      rw [List.map_append, List.prod_append]
      simpa only [nativeC60EYOrderedDefect] using
        congrArg₂ (fun a b : G => a * b) ihp ihq

/-- The finite signed product telescopes, without any commutativity
hypothesis, to the ORIGINAL group-observer endpoint ratio. -/
theorem nativeC60EYOrderedDefect_eq_endpoints
    {x y : L.Total} (p : NativeC60AXStep T x y) :
    nativeC60EYOrderedDefect T obs p = (obs x)⁻¹ * obs y := by
  rw [nativeC60EYOrderedDefect_eq_EX T obs p]
  exact nativeC60EXFoldDefect_eq_endpoints T obs p

/-- The pairs (atomic_defect, 1) for precisely a SELECTED family of
original typed generators. DT's quotient is genuinely a NEW relative
presentation, not a faithful equality of original 18D evidence. -/
def nativeC60EYSelectedPairs (A : Set (NativeC60EYPrimitive T)) :
    Set (G × G) :=
  Set.image
    (fun a : NativeC60EYPrimitive T =>
      (nativeC60EYPrimitiveDefect T obs a, (1 : G))) A

/-- A selected primitive's exact GROUP defect lies in the DT least
normal closure of selected (defect, 1) relations. -/
theorem nativeC60EYPrimitive_mem_normal
    (A : Set (NativeC60EYPrimitive T))
    (a : NativeC60EYPrimitive T) (ha : a ∈ A) :
    nativeC60EYPrimitiveDefect T obs a ∈
      nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A) := by
  have hp : (nativeC60EYPrimitiveDefect T obs a, (1 : G)) ∈
      nativeC60EYSelectedPairs T obs A := ⟨a, ha, rfl⟩
  have hh := nativeC60DTPairDefect_mem
    (nativeC60EYSelectedPairs T obs A)
    (nativeC60EYPrimitiveDefect T obs a, (1 : G)) hp
  simpa using hh

/-- Either occurrence orientation lies in the very SAME minimal
normal subgroup; no equality of signed Type-valued paths is assumed. -/
theorem nativeC60EYSigned_mem_normal
    (A : Set (NativeC60EYPrimitive T))
    (a : NativeC60EYSignedPrimitive T) (ha : a.primitive ∈ A) :
    nativeC60EYSignedDefect T obs a ∈
      nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A) := by
  cases h : a.backwards with
  | false =>
      simpa [nativeC60EYSignedDefect, h] using
        (nativeC60EYPrimitive_mem_normal T obs A a.primitive ha)
  | true =>
      simpa [nativeC60EYSignedDefect, h] using
        ((nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A)).inv_mem
          (nativeC60EYPrimitive_mem_normal T obs A a.primitive ha))

/-- Finite induction on the ordered signed list; arbitrary
noncommutative multiplication is retained in original order. -/
theorem nativeC60EYSignedList_mem_normal
    (A : Set (NativeC60EYPrimitive T)) :
    ∀ xs : List (NativeC60EYSignedPrimitive T),
      (∀ a, a ∈ xs → a.primitive ∈ A) →
      (xs.map (nativeC60EYSignedDefect T obs)).prod ∈
        nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A) := by
  intro xs
  induction xs with
  | nil =>
      intro _
      simpa using (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs A)).one_mem
  | cons atom rest ih =>
      intro hall
      have ha : atom.primitive ∈ A :=
        hall atom (by simp)
      have hrest : ∀ z, z ∈ rest → z.primitive ∈ A := by
        intro z hz
        exact hall z (by simp [hz])
      change nativeC60EYSignedDefect T obs atom *
          (rest.map (nativeC60EYSignedDefect T obs)).prod ∈
        nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A)
      exact (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs A)).mul_mem
          (nativeC60EYSigned_mem_normal T obs A atom ha)
          (ih hrest)

/-- All signed atoms of p are drawn from the selected original
typed primitive set A, with actual provenance retained. -/
def nativeC60EYPathCovered
    (A : Set (NativeC60EYPrimitive T))
    {x y : L.Total} (p : NativeC60AXStep T x y) : Prop :=
  ∀ a, a ∈ nativeC60EYSignedAtoms T p → a.primitive ∈ A

/-- The full signed path defect belongs to the chosen DT normal
closure whenever every actually used ORIGINAL primitive is selected. -/
theorem nativeC60EYPath_defect_mem_normal
    (A : Set (NativeC60EYPrimitive T))
    {x y : L.Total} (p : NativeC60AXStep T x y)
    (hcover : nativeC60EYPathCovered T A p) :
    nativeC60EXFoldDefect T obs p ∈
      nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A) := by
  rw [← nativeC60EYOrderedDefect_eq_EX T obs p]
  exact nativeC60EYSignedList_mem_normal T obs A
    (nativeC60EYSignedAtoms T p) hcover

/-- The selected generators may be JUST those that actually occur
in the given finite Type-valued path; no unrelated ambient atoms. -/
def nativeC60EYPathAtoms {x y : L.Total}
    (p : NativeC60AXStep T x y) :
    Set (NativeC60EYPrimitive T) :=
  {a | ∃ z, z ∈ nativeC60EYSignedAtoms T p ∧ z.primitive = a}

theorem nativeC60EYPathAtoms_cover
    {x y : L.Total} (p : NativeC60AXStep T x y) :
    nativeC60EYPathCovered T (nativeC60EYPathAtoms T p) p := by
  intro z hz
  exact ⟨z, hz, rfl⟩

/-- The whole ordered defect belongs to the smallest normal kernel
generated ONLY by the path's genuinely occurring typed primitives. -/
theorem nativeC60EYPath_defect_mem_exact_atoms
    {x y : L.Total} (p : NativeC60AXStep T x y) :
    nativeC60EXFoldDefect T obs p ∈
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) :=
  nativeC60EYPath_defect_mem_normal T obs
    (nativeC60EYPathAtoms T p) p
    (nativeC60EYPathAtoms_cover T p)

/-- EXACT DT DESCENT CRITERION for the selected typed generators.
A group receiver factors through the explicit relative quotient
precisely if every selected primitive defect becomes 1 under it. -/
theorem nativeC60EYReceiver_factor_iff
    (A : Set (NativeC60EYPrimitive T))
    {H : Type w} [Group H] (ρ : G →* H) :
    (∃ induced : NativeC60DTQuotient
          (nativeC60EYSelectedPairs T obs A) →* H,
       induced.comp (QuotientGroup.mk'
          (nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A))) =
         ρ) ↔
      ∀ a : NativeC60EYPrimitive T, a ∈ A →
        ρ (nativeC60EYPrimitiveDefect T obs a) = 1 := by
  refine (nativeC60DTQuotient_factor_iff
    (nativeC60EYSelectedPairs T obs A) ρ).trans ?_
  constructor
  · intro hall a ha
    have hh := hall
      (nativeC60EYPrimitiveDefect T obs a, (1 : G))
      (show (nativeC60EYPrimitiveDefect T obs a, (1 : G)) ∈
        nativeC60EYSelectedPairs T obs A from ⟨a, ha, rfl⟩)
    simpa using hh
  · intro h pair hp
    rcases hp with ⟨a, ha, rfl⟩
    simpa using h a ha

/-- A selected-atom-preserving receiver necessarily kills every
full path defect covered by those atoms. This does NOT prove the
original group-valued path defect is the identity. -/
theorem nativeC60EYReceiver_path_defect_one
    (A : Set (NativeC60EYPrimitive T))
    {H : Type w} [Group H] (ρ : G →* H)
    (hρ : ∀ a : NativeC60EYPrimitive T, a ∈ A →
      ρ (nativeC60EYPrimitiveDefect T obs a) = 1)
    {x y : L.Total} (p : NativeC60AXStep T x y)
    (hcover : nativeC60EYPathCovered T A p) :
    ρ (nativeC60EXFoldDefect T obs p) = 1 := by
  have hk : nativeC60DTNormalClosure
      (nativeC60EYSelectedPairs T obs A) ≤ ρ.ker := by
    apply (nativeC60DTNormalClosure_ker_iff
      (nativeC60EYSelectedPairs T obs A) ρ).mpr
    intro pair hp
    rcases hp with ⟨a, ha, rfl⟩
    simpa using hρ a ha
  exact MonoidHom.mem_ker.mp
    (hk (nativeC60EYPath_defect_mem_normal T obs A p hcover))

end GroupValued
end SignedFullPathNormalClosure

#print axioms NativeC60EYPrimitive
#print axioms NativeC60EYSignedPrimitive
#print axioms nativeC60EYSignedAtoms
#print axioms nativeC60EYSignedDefect_flip
#print axioms nativeC60EYReverseFlipProduct
#print axioms nativeC60EYOrderedDefect_eq_EX
#print axioms nativeC60EYOrderedDefect_eq_endpoints
#print axioms nativeC60EYPrimitive_mem_normal
#print axioms nativeC60EYPath_defect_mem_exact_atoms
#print axioms nativeC60EYReceiver_factor_iff
#print axioms nativeC60EYReceiver_path_defect_one

end
end Kuu.F112.Physical
