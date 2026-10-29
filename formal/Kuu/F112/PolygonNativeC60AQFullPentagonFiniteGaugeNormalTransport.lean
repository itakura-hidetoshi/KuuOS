import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteSignedNormalDescent
import Kuu.F112.PolygonNativeC60AQGaugePentagonDescent
import Mathlib.Tactic.Group

/-!
# F112-P94D3EZ — ordered finite signed C60 path: gauge-normal covariance

EY already showed that the exact, original, dependent four-constructor
19D path is evaluated as a finite ORDERED product of signed primitive
defects, and that this full product belongs to the minimal DT normal
closure of precisely the used original typed generators.

EZ proves, without abelianizing or deleting any primitive:
* Each DT relation normal closure is invariant under any INNER gauge
  conjugation, using DU's exact quotient-descent criterion.
* Conjugating every selected original typed primitive defect produces
  EXACTLY the SAME normal closure; the reverse inclusion is proved by
  the inverse gauge conjugation, not assumed.
* The full noncommutative ordered signed product is gauge-covariant.
* The kernel grows monotonically with the selected original typed
  generators, including left/right finite context-path extensions.
* An arbitrary endomorphism of the full group descends through the
  selected quotient IFF EACH originally selected atomic defect is
  killed in that very quotient after transport.
* Gauge-conjugated full path defects are invisible in that chosen
  quotient, while their original group values remain distinguishable
  whenever the original path defect is nonidentity.

No original geometric C60 19D filler is constructed. This is an
explicitly SELECTED relative presentation, distinct from complete
18D Type-valued evidence; do not infer full evidence preservation.
Preserve original 14D--18D evidence, DS no-go, strict Kuu, independent
Kuu as a presentation, 107 public roots, no Gray, append-only,
tighten-only, same-root, pinned Lean/mathlib. No new axiom/sorry/admit.
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

section UniversalInnerNormalTransport

variable {G : Type v} [Group G]

/-- Any inner gauge transformation preserves EVERY exact DT
normal closure: this follows from DU's relative transport criterion,
not any commutative approximation. -/
theorem nativeC60EZConjugation_stable_DT
    (R : Set (G × G)) (c : G) {x : G}
    (hx : x ∈ nativeC60DTNormalClosure R) :
    c * x * c⁻¹ ∈ nativeC60DTNormalClosure R := by
  have h := (nativeC60DUNormalKernel_preservation_iff
    R (nativeC60DUConjugation c)).mpr
      (nativeC60DUConjugation_descends R c)
  exact h x hx

/-- Noncommutative gauge conjugation does not turn a genuine original
nonidentity free word into the identity. -/
theorem nativeC60EZConjugate_ne_one
    (c x : G) (hne : x ≠ 1) :
    c * x * c⁻¹ ≠ 1 := by
  intro h
  apply hne
  calc
    x = c⁻¹ * (c * x * c⁻¹) * c := by group
    _ = 1 := by rw [h]; group

end UniversalInnerNormalTransport

section TypedFiniteGaugeNormal

variable {L : NativeC60AXLayer.{u}}
variable (T : NativeC60AXSignature L)
variable {G : Type v} [Group G] (obs : L.Total → G)

/-- A family of genuine ORIGINAL dependent generator-defects transported
by one noncommutative inner gauge element. Identity pairs are selected
explicitly, and the original primitive indices are not forgotten. -/
def nativeC60EZConjugatedSelectedPairs
    (A : Set (NativeC60EYPrimitive T)) (c : G) :
    Set (G × G) :=
  Set.image (fun a : NativeC60EYPrimitive T =>
    (c * nativeC60EYPrimitiveDefect T obs a * c⁻¹, (1 : G))) A

/-- The least normal kernel of the selected true typed atomic defects
is EXACTLY invariant under simultaneous gauge conjugation of ALL
selected relators. The reverse inclusion uses c⁻¹. -/
theorem nativeC60EZConjugatedNormal_eq
    (A : Set (NativeC60EYPrimitive T)) (c : G) :
    nativeC60DTNormalClosure
      (nativeC60EZConjugatedSelectedPairs T obs A c) =
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs A) := by
  apply le_antisymm
  · apply (nativeC60DTNormalClosure_le_iff
      (nativeC60EZConjugatedSelectedPairs T obs A c)
      (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs A))).mpr
    intro pair hp
    rcases hp with ⟨a, ha, rfl⟩
    have ha0 := nativeC60EYPrimitive_mem_normal T obs A a ha
    have hconj := nativeC60EZConjugation_stable_DT
      (nativeC60EYSelectedPairs T obs A) c ha0
    simpa using hconj
  · apply (nativeC60DTNormalClosure_le_iff
      (nativeC60EYSelectedPairs T obs A)
      (nativeC60DTNormalClosure
        (nativeC60EZConjugatedSelectedPairs T obs A c))).mpr
    intro pair hp
    rcases hp with ⟨a, ha, rfl⟩
    have hpair :
        (c * nativeC60EYPrimitiveDefect T obs a * c⁻¹, (1 : G)) ∈
          nativeC60EZConjugatedSelectedPairs T obs A c :=
      ⟨a, ha, rfl⟩
    have hc : c * nativeC60EYPrimitiveDefect T obs a * c⁻¹ ∈
        nativeC60DTNormalClosure
          (nativeC60EZConjugatedSelectedPairs T obs A c) := by
      have hmem := nativeC60DTPairDefect_mem
        (nativeC60EZConjugatedSelectedPairs T obs A c)
        (c * nativeC60EYPrimitiveDefect T obs a * c⁻¹, (1 : G)) hpair
      simpa using hmem
    have hback := nativeC60EZConjugation_stable_DT
      (nativeC60EZConjugatedSelectedPairs T obs A c) c⁻¹ hc
    have hreduce :
        c⁻¹ * (c * nativeC60EYPrimitiveDefect T obs a * c⁻¹) *
          (c⁻¹)⁻¹ = nativeC60EYPrimitiveDefect T obs a := by
      group
    simpa [hreduce] using hback

/-- The ordered finite product of ORIGINAL signed typed atomic defects
intertwines the inner gauge action. Reordering would invalidate this. -/
theorem nativeC60EZConjugation_signedList_product
    (c : G) :
    ∀ xs : List (NativeC60EYSignedPrimitive T),
      (xs.map (fun a =>
        c * nativeC60EYSignedDefect T obs a * c⁻¹)).prod =
      c * (xs.map (nativeC60EYSignedDefect T obs)).prod * c⁻¹ := by
  intro xs
  induction xs with
  | nil =>
      simp
  | cons a rest ih =>
      change
        (c * nativeC60EYSignedDefect T obs a * c⁻¹) *
          (rest.map (fun z =>
            c * nativeC60EYSignedDefect T obs z * c⁻¹)).prod =
          c * (nativeC60EYSignedDefect T obs a *
            (rest.map (nativeC60EYSignedDefect T obs)).prod) * c⁻¹
      rw [ih]
      group

/-- Original signed path order is retained when the ENTIRE defect is
conjugated, including nested inverses and noncommuting factors. -/
theorem nativeC60EZConjugation_path_product
    {x y : L.Total} (p : NativeC60AXStep T x y) (c : G) :
    ((nativeC60EYSignedAtoms T p).map (fun a =>
      c * nativeC60EYSignedDefect T obs a * c⁻¹)).prod =
      c * nativeC60EXFoldDefect T obs p * c⁻¹ := by
  calc
    _ = c * nativeC60EYOrderedDefect T obs p * c⁻¹ :=
      nativeC60EZConjugation_signedList_product T obs c _
    _ = c * nativeC60EXFoldDefect T obs p * c⁻¹ := by
      rw [nativeC60EYOrderedDefect_eq_EX T obs p]

/-- Enlarging the selected family of ORIGINAL typed generators
can only enlarge its exact minimal DT normal kernel. -/
theorem nativeC60EZNormal_mono
    {A B : Set (NativeC60EYPrimitive T)} (hAB : A ⊆ B) :
    nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs A) ≤
      nativeC60DTNormalClosure (nativeC60EYSelectedPairs T obs B) := by
  apply (nativeC60DTNormalClosure_le_iff
    (nativeC60EYSelectedPairs T obs A)
    (nativeC60DTNormalClosure
      (nativeC60EYSelectedPairs T obs B))).mpr
  intro pair hp
  rcases hp with ⟨a, ha, rfl⟩
  simpa using nativeC60EYPrimitive_mem_normal T obs B a (hAB ha)

/-- Left finite context extension includes every genuinely occurring
typed primitive of the original left subpath. -/
theorem nativeC60EZPathAtoms_trans_left
    {x y z : L.Total} (p : NativeC60AXStep T x y)
    (q : NativeC60AXStep T y z) :
    nativeC60EYPathAtoms T p ⊆
      nativeC60EYPathAtoms T (.trans p q) := by
  rintro a ⟨item, hitem, rfl⟩
  refine ⟨item, ?_, rfl⟩
  change item ∈ nativeC60EYSignedAtoms T p ++
    nativeC60EYSignedAtoms T q
  exact List.mem_append.mpr (Or.inl hitem)

/-- Right finite context extension likewise retains every actually
occurring original typed primitive of the right subpath. -/
theorem nativeC60EZPathAtoms_trans_right
    {x y z : L.Total} (p : NativeC60AXStep T x y)
    (q : NativeC60AXStep T y z) :
    nativeC60EYPathAtoms T q ⊆
      nativeC60EYPathAtoms T (.trans p q) := by
  rintro a ⟨item, hitem, rfl⟩
  refine ⟨item, ?_, rfl⟩
  change item ∈ nativeC60EYSignedAtoms T p ++
    nativeC60EYSignedAtoms T q
  exact List.mem_append.mpr (Or.inr hitem)

/-- The minimal normal kernel for a signed subpath persists under
adding arbitrary further original finite typed context on the right. -/
theorem nativeC60EZPathNormal_trans_left
    {x y z : L.Total} (p : NativeC60AXStep T x y)
    (q : NativeC60AXStep T y z) :
    nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) ≤
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs
          (nativeC60EYPathAtoms T (.trans p q))) :=
  nativeC60EZNormal_mono T obs (nativeC60EZPathAtoms_trans_left T p q)

/-- The same context monotonicity for the right original subpath. -/
theorem nativeC60EZPathNormal_trans_right
    {x y z : L.Total} (p : NativeC60AXStep T x y)
    (q : NativeC60AXStep T y z) :
    nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T q)) ≤
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs
          (nativeC60EYPathAtoms T (.trans p q))) :=
  nativeC60EZNormal_mono T obs (nativeC60EZPathAtoms_trans_right T p q)

/-- Exact DU criterion, specialized to the ORIGINAL selected typed
atomic defects: an arbitrary full-evidence endomorphism preserves
the chosen normal kernel IFF its action sends EACH selected atom
into the kernel of precisely that chosen relative quotient. -/
theorem nativeC60EZSelectedTransport_kernel_iff
    (A : Set (NativeC60EYPrimitive T)) (τ : G →* G) :
    (∀ x : G, x ∈ nativeC60DTNormalClosure
      (nativeC60EYSelectedPairs T obs A) →
        τ x ∈ nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A)) ↔
      ∀ a : NativeC60EYPrimitive T, a ∈ A →
        (QuotientGroup.mk' (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A)))
          (τ (nativeC60EYPrimitiveDefect T obs a)) = 1 := by
  refine (nativeC60DUNormalKernel_criterion
    (nativeC60EYSelectedPairs T obs A) τ).trans ?_
  constructor
  · intro hall a ha
    have hh := hall
      (nativeC60EYPrimitiveDefect T obs a, (1 : G))
      (show
        (nativeC60EYPrimitiveDefect T obs a, (1 : G)) ∈
          nativeC60EYSelectedPairs T obs A from ⟨a, ha, rfl⟩)
    simpa using hh
  · intro hall pair hp
    rcases hp with ⟨a, ha, rfl⟩
    simpa using hall a ha

/-- A full-evidence transport descends through the precisely
selected relative quotient IFF it kills exactly the selected
typed primitive defects after applying the quotient map. -/
theorem nativeC60EZSelectedTransport_factor_iff
    (A : Set (NativeC60EYPrimitive T)) (τ : G →* G) :
    (∃ induced :
        NativeC60DTQuotient (nativeC60EYSelectedPairs T obs A) →*
          NativeC60DTQuotient (nativeC60EYSelectedPairs T obs A),
      induced.comp (QuotientGroup.mk'
        (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A))) =
        (QuotientGroup.mk' (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A))).comp τ) ↔
      ∀ a : NativeC60EYPrimitive T, a ∈ A →
        (QuotientGroup.mk' (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T obs A)))
          (τ (nativeC60EYPrimitiveDefect T obs a)) = 1 := by
  exact (nativeC60DUNormalKernel_preservation_iff
    (nativeC60EYSelectedPairs T obs A) τ).symm.trans
      (nativeC60EZSelectedTransport_kernel_iff T obs A τ)

/-- In the selected path-local quotient, inner gauge transport
actually exists, unlike an arbitrary proposed contextual operation. -/
theorem nativeC60EZPathGauge_descends
    {x y : L.Total} (p : NativeC60AXStep T x y) (c : G) :
    ∃ induced :
        NativeC60DTQuotient
          (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) →*
        NativeC60DTQuotient
          (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)),
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)))) =
      (QuotientGroup.mk' (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)))).comp
          (nativeC60DUConjugation c) :=
  nativeC60DUConjugation_descends
    (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) c

/-- The gauge-transformed FULL ordered signed path defect belongs to
the SAME selected path-local normal kernel. Neither sign nor raw
dependent generator provenance is erased by this membership. -/
theorem nativeC60EZPathGauge_defect_mem
    {x y : L.Total} (p : NativeC60AXStep T x y) (c : G) :
    c * nativeC60EXFoldDefect T obs p * c⁻¹ ∈
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) :=
  nativeC60EZConjugation_stable_DT
    (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p)) c
    (nativeC60EYPath_defect_mem_exact_atoms T obs p)

/-- This selected relative quotient kills the GAUGE-TRANSFORMED
defect. It is not equality of the original Type-valued histories. -/
theorem nativeC60EZPathGauge_defect_quotient_one
    {x y : L.Total} (p : NativeC60AXStep T x y) (c : G) :
    (QuotientGroup.mk' (nativeC60DTNormalClosure
      (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p))))
      (c * nativeC60EXFoldDefect T obs p * c⁻¹) = 1 := by
  apply MonoidHom.mem_ker.mp
  rw [nativeC60DTQuotient_kernel
    (nativeC60EYSelectedPairs T obs (nativeC60EYPathAtoms T p))]
  exact nativeC60EZPathGauge_defect_mem T obs p c

end TypedFiniteGaugeNormal

#print axioms nativeC60EZConjugation_stable_DT
#print axioms nativeC60EZConjugate_ne_one
#print axioms nativeC60EZConjugatedNormal_eq
#print axioms nativeC60EZConjugation_signedList_product
#print axioms nativeC60EZConjugation_path_product
#print axioms nativeC60EZNormal_mono
#print axioms nativeC60EZPathNormal_trans_left
#print axioms nativeC60EZPathNormal_trans_right
#print axioms nativeC60EZSelectedTransport_kernel_iff
#print axioms nativeC60EZSelectedTransport_factor_iff
#print axioms nativeC60EZPathGauge_descends
#print axioms nativeC60EZPathGauge_defect_mem
#print axioms nativeC60EZPathGauge_defect_quotient_one

end
end Kuu.F112.Physical
