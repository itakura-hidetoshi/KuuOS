import KUOS.Architecture.QiWuxingPentagonUnifiedV3_5
import KUOS.Architecture.QiWuxingGK5CGNorthP77PentagonatorChargeV4_51
import Mathlib.Tactic

/-!
Qi v4.52 — ONE canonical FivefoldIndex / FivefoldEdge for REAL
C60 physical edges, TRUE ORIGINAL F55/P77 Type-valued four-cells,
and genuine GK5X/GK5Y whole Mathlib NatIso edges.

Unlike Qi v3.5, which shared the Qi/C60/GK5 phase coordinates,
this module reads the original independent GK5CF/CG F55/P77
evidence as actual dependently typed four-proof terms. Every one of
the five old P77 edges has exactly the same source/target phase as
the selected physical C60 edge and categorical NatIso. The e04
and e43 arrows explicitly reverse old P77 cyclic 40 and 34.

Do not identify a physical Edge, a P77 four-proof, a NatIso,
a RingHom equality or an original-to-phi P94A seam.
The genuine upper three-edge vs lower two-edge P77 charge defect
remains +1 and therefore excludes the conservative source five-cell.
Numerical CRT remains separately true by Qi v4.51.

No new source five-cell or automatic pentagonator. Strict Kuu stays
central, independent Kuu is one presentation; original histories
untouched. Append-only, root107, pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
protected validation-only #1558 draft/open/unmerged.
No new axiom/sorry/admit/native_decide/Gray.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uI vC uC uD vD uE vE

section AllOriginalSources
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}

/-- Same five Qi phases select all five GENUINE ORIGINAL F55
three-proof parenthesizations; no F55 term is inferred from a number. -/
def fivefoldF55OriginalAt
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    (q : FivefoldIndex) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₄ :=
  if q = 0 then nativeGK5CFOriginalLeftLeftLeft f g h k
  else if q = 1 then nativeGK5CFOriginalLeftMiddle f g h k
  else if q = 2 then nativeGK5CFOriginalRightMiddle f g h k
  else if q = 3 then nativeGK5CFOriginalRightRight f g h k
  else nativeGK5CFOriginalMiddle f g h k

/-- ONE FivefoldEdge produces the actual endpoint-typed original
P77 four-proof. The two lower edges are ORIGINAL inversions,
not an invented 5-cell or a numerical change of direction. -/
def fivefoldF55OriginalP77Edge
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    (edge : FivefoldEdge) :
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k (fivefoldFrom edge))
      (fivefoldF55OriginalAt f g h k (fivefoldTo edge)) := by
  cases edge with
  | e01 =>
      exact nativeGK5CFP77Edge01 f g h k
  | e12 =>
      exact nativeGK5CFP77Edge12 f g h k
  | e23 =>
      exact nativeGK5CFP77Edge23 f g h k
  | e04 =>
      exact NativeF55RawVerticalFourCell.symm
        (nativeGK5CFP77Edge40 f g h k)
  | e43 =>
      exact NativeF55RawVerticalFourCell.symm
        (nativeGK5CFP77Edge34 f g h k)

/-- The exact original charge is +1 on EVERY edge in the new
directed FivefoldEdge orientation, including reverse 04 and 43. -/
theorem fivefoldF55OriginalP77Edge_assocCharge_one
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    (edge : FivefoldEdge) :
    (fivefoldF55OriginalP77Edge f g h k edge).gk5cgAssocCharge = 1 := by
  cases edge <;>
    norm_num [fivefoldF55OriginalP77Edge, fivefoldF55OriginalAt,
      fivefoldFrom, fivefoldTo,
      nativeGK5CFP77Edge01, nativeGK5CFP77Edge12,
      nativeGK5CFP77Edge23, nativeGK5CFP77Edge40,
      nativeGK5CFP77Edge34,
      NativeF55RawVerticalFourCell.gk5cgAssocCharge]

/-- Actual ORIGINAL upper three-edge pentagon constructed solely
from the shared FivefoldEdge identifiers. -/
def fivefoldF55OriginalUpper
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k 0)
      (fivefoldF55OriginalAt f g h k 3) :=
  .trans (.trans
    (fivefoldF55OriginalP77Edge f g h k .e01)
    (fivefoldF55OriginalP77Edge f g h k .e12))
    (fivefoldF55OriginalP77Edge f g h k .e23)

/-- Actual ORIGINAL lower two-edge pentagon, NOT a made-up straight edge. -/
def fivefoldF55OriginalLower
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k 0)
      (fivefoldF55OriginalAt f g h k 3) :=
  .trans (fivefoldF55OriginalP77Edge f g h k .e04)
    (fivefoldF55OriginalP77Edge f g h k .e43)

/-- The two routes have the SAME actual typed 3-cell endpoints
and DIFFERENT integer charges 3 and 2, respectively. -/
theorem fivefoldF55OriginalPentagon_charge
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    (fivefoldF55OriginalUpper f g h k).gk5cgAssocCharge = 3 ∧
    (fivefoldF55OriginalLower f g h k).gk5cgAssocCharge = 2 := by
  constructor
  · change
      (fivefoldF55OriginalP77Edge f g h k .e01).gk5cgAssocCharge +
        (fivefoldF55OriginalP77Edge f g h k .e12).gk5cgAssocCharge +
        (fivefoldF55OriginalP77Edge f g h k .e23).gk5cgAssocCharge = 3
    rw [fivefoldF55OriginalP77Edge_assocCharge_one,
      fivefoldF55OriginalP77Edge_assocCharge_one,
      fivefoldF55OriginalP77Edge_assocCharge_one]
    norm_num
  · change
      (fivefoldF55OriginalP77Edge f g h k .e04).gk5cgAssocCharge +
        (fivefoldF55OriginalP77Edge f g h k .e43).gk5cgAssocCharge = 2
    rw [fivefoldF55OriginalP77Edge_assocCharge_one,
      fivefoldF55OriginalP77Edge_assocCharge_one]
    norm_num

/-- Since each constructor of the GENUINE CONSERVATIVE 5-cell
presentation preserves signed original P77 charge, no such 5-cell
can connect the two shared-index pentagon paths. -/
theorem fivefoldF55Original_noConservativePentagonator
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldF55OriginalUpper f g h k)
      (fivefoldF55OriginalLower f g h k)) := by
  rintro ⟨w⟩
  have hcharge := w.assocCharge_sound
  obtain ⟨hu, hl⟩ := fivefoldF55OriginalPentagon_charge f g h k
  rw [hu, hl] at hcharge
  norm_num at hcharge

end AllOriginalSources

section GenuineC60PhysicalPentagon
variable (v : Vertex)
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree (.pentagon v) n m ma pa mb pb}
variable {last : KuuNativeF45Tree (.pentagon v) n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute (.pentagon v) first last}

/-- At EACH of the twelve physical pentagons, the SAME FivefoldEdge
returns both an actual incident physical C60 edge and the dependent
original F55/P77 four-proof. This is not a quotient of evidence. -/
def fivefoldOriginalPhysicalPair
    (frame : NativeC60FivePhaseGauge)
    (edge : FivefoldEdge)
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon v) r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon v) r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon v) r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon v) r₃ r₄) :
    { physical : Edge //
      edgeJoins physical
        (nativeC60GaugeDart frame v (fivefoldFrom edge))
        (nativeC60GaugeDart frame v (fivefoldTo edge)) } ×
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k (fivefoldFrom edge))
      (fivefoldF55OriginalAt f g h k (fivefoldTo edge)) :=
  ⟨⟨fivefoldPhysicalEdge frame v edge,
    fivefoldPhysicalEdge_joins frame v edge⟩,
    fivefoldF55OriginalP77Edge f g h k edge⟩

end GenuineC60PhysicalPentagon

#print axioms fivefoldF55OriginalAt
#print axioms fivefoldF55OriginalP77Edge
#print axioms fivefoldF55OriginalP77Edge_assocCharge_one
#print axioms fivefoldF55OriginalUpper
#print axioms fivefoldF55OriginalLower
#print axioms fivefoldF55OriginalPentagon_charge
#print axioms fivefoldF55Original_noConservativePentagonator
#print axioms fivefoldOriginalPhysicalPair

end
end KUOS.Architecture.WuxingPentagonUnified
