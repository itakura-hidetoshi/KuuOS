import Kuu.F112.PolygonNativeF55P94DK5ShellingNoncommutativeGap
import Mathlib.Tactic

/-!
# F112-P94D3J-G — gauge-first, graph-independent noncommutative obstruction

Gauge transport is primary: choose an arbitrary type I of local
presentations rather than a K5 graph. Their transition words lie
in the original noncommutative free group of P/S/N source 3-cell
letters. Gauge frames act covariantly on transition words.

The resulting non-Abelian triangular transport defect is conjugated
under a frame change. Its independent integer naturality count and
complete original F55 shadow are invariant. The actual P94A typed
Peiffer boundary is equivariant under the SAME group action, so
a gauge change alone cannot remove a +1-charge obstruction.

Only AFTER these generic gauge results are established do we use the
actual outward K5 nine-face noncommutative formal shelling word as
a finite example. This is an algebraic gauge/word representation,
NOT a genuine Type-valued higher connection or a 4D filler.
The source-level F54/P92B seam and strict 3/n coherence remain
independent proof obligations. Do not infer physical gauge fields
or higher surface holonomy from an arbitrary free-word receiver.

No graph reduction of emptiness, Gray, sorry/admit, new logical
axioms or removal of the 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uI uD vD uE vE

/-- The original P/S/N free group, without abelianization, is an
algebraic receiver for a chosen gauge presentation. -/
abbrev NativeF55GaugeGroup := NativeF55P94CWord

/-- Covariant change of a based, noncommutative holonomy word.
The basepoint changes, not the underlying gauge-independent charge. -/
def nativeF55GaugeConjugate
    (g w : NativeF55GaugeGroup) : NativeF55GaugeGroup :=
  g + w - g

theorem nativeF55GaugeConjugate_zero (w : NativeF55GaugeGroup) :
    nativeF55GaugeConjugate 0 w = w := by
  simp [nativeF55GaugeConjugate]

theorem nativeF55GaugeConjugate_comp
    (g h w : NativeF55GaugeGroup) :
    nativeF55GaugeConjugate (g + h) w =
      nativeF55GaugeConjugate g (nativeF55GaugeConjugate h w) := by
  simp only [nativeF55GaugeConjugate, sub_eq_add_neg]
  group

/-- Any type of local presentations is admitted: there is no
dependence on vertices, edges or a globally preferred chart. -/
abbrev NativeF55GaugeConnection (I : Type uI) :=
  I → I → NativeF55GaugeGroup

/-- A local change of frame at both endpoints of a transition. -/
def nativeF55GaugeTransport
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (i j : I) (u : NativeF55GaugeGroup) :
    NativeF55GaugeGroup :=
  g i + u - g j

/-- Genuine noncommutative transport composition under changes
of local presentation, without dropping any intervening gauge. -/
theorem nativeF55GaugeTransport_comp
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (i j k : I)
    (u v : NativeF55GaugeGroup) :
    nativeF55GaugeTransport g i j u +
      nativeF55GaugeTransport g j k v =
    nativeF55GaugeTransport g i k (u + v) := by
  simp only [nativeF55GaugeTransport, sub_eq_add_neg]
  group

def nativeF55GaugeChangeConnection
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (A : NativeF55GaugeConnection I) :
    NativeF55GaugeConnection I :=
  fun i j => nativeF55GaugeTransport g i j (A i j)

/-- Non-Abelian Čech/triangular transport mismatch:
the two-step transport relative to the direct transition.
It is an ALGEBRAIC gauge defect, not yet a Type-valued
P92B surface/physical curvature form. -/
def nativeF55GaugeTriangleDefect
    {I : Type uI}
    (A : NativeF55GaugeConnection I)
    (i j k : I) : NativeF55GaugeGroup :=
  A i j + A j k - A i k

theorem nativeF55GaugeTriangleDefect_covariant
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (A : NativeF55GaugeConnection I)
    (i j k : I) :
    nativeF55GaugeTriangleDefect
      (nativeF55GaugeChangeConnection g A) i j k =
      nativeF55GaugeConjugate (g i)
        (nativeF55GaugeTriangleDefect A i j k) := by
  simp only [nativeF55GaugeTriangleDefect,
    nativeF55GaugeChangeConnection,
    nativeF55GaugeTransport,
    nativeF55GaugeConjugate,
    sub_eq_add_neg]
  group

/-- The P94D3H new naturality count is a GENUINE class function
on this group-word gauge receiver. It is not a gauge-fixed count. -/
theorem nativeF55GaugeNaturalityCount_invariant
    (g w : NativeF55GaugeGroup) :
    nativeK5NaturalityCount (nativeF55GaugeConjugate g w) =
      nativeK5NaturalityCount w := by
  simp only [nativeF55GaugeConjugate, map_sub, map_add]
  abel

/-- The WHOLE old signed and odd-phase F55 shadow is invariant
under the same gauge conjugation, independently of N-count. -/
theorem nativeF55GaugeFullShadow_invariant
    (g w : NativeF55GaugeGroup) :
    nativeF55P94CWordToShadow (nativeF55GaugeConjugate g w) =
      nativeF55P94CWordToShadow w := by
  simp only [nativeF55GaugeConjugate, map_sub, map_add]
  abel

theorem nativeF55GaugeTriangleDefect_NCount_invariant
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (A : NativeF55GaugeConnection I)
    (i j k : I) :
    nativeK5NaturalityCount
      (nativeF55GaugeTriangleDefect
        (nativeF55GaugeChangeConnection g A) i j k) =
    nativeK5NaturalityCount
      (nativeF55GaugeTriangleDefect A i j k) := by
  rw [nativeF55GaugeTriangleDefect_covariant]
  exact nativeF55GaugeNaturalityCount_invariant _ _

theorem nativeF55GaugeTriangleDefect_shadow_invariant
    {I : Type uI}
    (g : I → NativeF55GaugeGroup)
    (A : NativeF55GaugeConnection I)
    (i j k : I) :
    nativeF55P94CWordToShadow
      (nativeF55GaugeTriangleDefect
        (nativeF55GaugeChangeConnection g A) i j k) =
    nativeF55P94CWordToShadow
      (nativeF55GaugeTriangleDefect A i j k) := by
  rw [nativeF55GaugeTriangleDefect_covariant]
  exact nativeF55GaugeFullShadow_invariant _ _

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Existing P94D3G TYPE-valued four-cell Peiffer boundary
is equivariant under EXACTLY the same noncommutative gauge action.
This fact is already proved at the original normal-kernel level. -/
theorem nativeF55GaugePeifferBoundary_equivariant
    (g : NativeF55GaugeGroup)
    (r : NativeK5P94ATypedPeifferKernel D E) :
    nativeK5P94ATypedPeifferBoundary
      (nativeK5P94ATypedPeifferAct g r) =
    nativeF55GaugeConjugate g
      (nativeK5P94ATypedPeifferBoundary r) := by
  exact nativeK5P94ATypedPeifferBoundary_equivariant g r

/-- A +1 naturality obstruction remains outside EVERY existing
genuinely Type-generated P94A/P94C2 word kernel after ANY gauge
frame change, not just at a preferred graph-path representative. -/
theorem nativeF55GaugeCharge_one_not_mem_P94ATyped
    (g w : NativeF55GaugeGroup)
    (hw : nativeK5NaturalityCount w = 1) :
    nativeF55GaugeConjugate g w ∉
      nativeK5P94ATypedNormalClosure D E := by
  intro h
  have hh :=
    nativeK5P94ATypedNormalClosure_le_NCount_ker (D := D) (E := E) h
  change nativeK5NaturalityCount
    (nativeF55GaugeConjugate g w) = 0 at hh
  rw [nativeF55GaugeNaturalityCount_invariant, hw] at hh
  norm_num at hh

section FiveNativeStages
variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- K5 is ONLY a finite test presentation for the preceding
generic gauge theorem: all gauge frames preserve the +1
charge of the actual outward nine-face formal shelling word. -/
theorem nativeK5GaugeShelling_NCount_one
    (g : NativeF55GaugeGroup) :
    nativeK5NaturalityCount
      (nativeF55GaugeConjugate g
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5)) = 1 := by
  rw [nativeF55GaugeNaturalityCount_invariant,
    nativeK5GraphShellingWord_NCount_one]

theorem nativeK5GaugeShelling_shadow_zero
    (g : NativeF55GaugeGroup) :
    nativeF55P94CWordToShadow
      (nativeF55GaugeConjugate g
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5)) = 0 := by
  rw [nativeF55GaugeFullShadow_invariant,
    nativeK5GraphShellingWord_shadow_zero]

theorem nativeK5GaugeShelling_not_mem_P94ATyped
    (g : NativeF55GaugeGroup) :
    nativeF55GaugeConjugate g
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) ∉
        nativeK5P94ATypedNormalClosure D E := by
  exact nativeF55GaugeCharge_one_not_mem_P94ATyped
    (D := D) (E := E) g
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5)
      (nativeK5GraphShellingWord_NCount_one t1 t2 t3 t4 t5)

/-- The separately extended pentagonator normal-word kernel
contains the entire gauge orbit of its new relator. This is a
purely ALGEBRAIC normal-closure result, not a missing typed
higher-gauge coherence witness. -/
theorem nativeK5GaugePentagonatorRelator_mem
    (g : NativeF55GaugeGroup) :
    nativeF55GaugeConjugate g
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) ∈
      nativeK5PentagonatorWordNormalClosure D E
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5) := by
  have hw :=
    nativeK5PentagonatorWord_mem (D := D) (E := E)
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5)
  have hh :=
    (inferInstance :
      (nativeK5PentagonatorWordNormalClosure D E
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5)).Normal).conj_mem
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) hw g
  simpa only [nativeF55GaugeConjugate, sub_eq_add_neg] using hh

end FiveNativeStages

#print axioms nativeF55GaugeConjugate_comp
#print axioms nativeF55GaugeTransport_comp
#print axioms nativeF55GaugeTriangleDefect_covariant
#print axioms nativeF55GaugeNaturalityCount_invariant
#print axioms nativeF55GaugeFullShadow_invariant
#print axioms nativeF55GaugeTriangleDefect_NCount_invariant
#print axioms nativeF55GaugeTriangleDefect_shadow_invariant
#print axioms nativeF55GaugePeifferBoundary_equivariant
#print axioms nativeF55GaugeCharge_one_not_mem_P94ATyped
#print axioms nativeK5GaugeShelling_NCount_one
#print axioms nativeK5GaugeShelling_shadow_zero
#print axioms nativeK5GaugeShelling_not_mem_P94ATyped
#print axioms nativeK5GaugePentagonatorRelator_mem

end
end Kuu.F112.Physical
