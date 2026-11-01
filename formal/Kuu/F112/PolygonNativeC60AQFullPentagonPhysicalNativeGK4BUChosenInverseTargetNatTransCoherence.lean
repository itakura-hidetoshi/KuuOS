import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BTTargetInterchangeChosenInverse
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BU — target-NatTrans coherence for the ACTUAL
GK4BT natural-isomorphism comparison of the GK4BM choice inverse.

The original F45-dependent structural category S, its genuinely
attained AH image A_att, the exact kernel-compatible full
subcategory Comp_T, and the original choice inverse Q_T are
unchanged. GK4BQ supplies k_T : Q_T ≅ P_T, with P_T the GK4BP
explicit inverse. GK4BT constructs the honest target-change
NatIso Theta_R using k_U, the strict P square, and k_T.symm.

GK4BU proves compatibility under actual target natural
transformations, by pasting two genuine Mathlib interchange
squares and the GK4BP strict middle square. The equality
transported by eqToIso is accounted for, not silently discarded.
No strict target naturality of the arbitrary choice inverse is
postulated. All arrows inhabit existing Mathlib functor categories.

No unconditional S faithfulness, raw F54/F55/P92B Type-valued
higher cells, source Q category laws, all-integer-matrix reachability,
global Gray or higher hyperdescent. Strict 空 center; independent Kuu
one presentation. Append-only/tighten-only/same-root107.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV

universe uC vC

/-- Equality transport commutes with heterogeneously equal
morphisms. The two endpoint equalities are not assumed rfl. -/
private theorem nativeGK4BUEqToHom_square
    {C : Type uC} [Category.{vC} C]
    {A B A' B' : C}
    (h : A = B) (h' : A' = B')
    (f : A ⟶ A') (g : B ⟶ B')
    (hh : HEq f g) :
    f ≫ eqToHom h' = eqToHom h ≫ g := by
  cases h
  cases h'
  simpa only [eqToHom_refl, Category.comp_id, Category.id_comp] using
    (eq_of_heq hh)

section ChosenInverseTargetNatTrans
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- Interchange of the genuine target transformation with the
comparison k_U:Q_U≅P_U, as a whole Mathlib NatTrans equality. -/
theorem nativeGK4BUChosenInverse_leftInterchange
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      Functor.whiskerLeft
        (nativeGK4BNPostcompCompatible p ma mb pa pb R')
        (nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb).hom =
    Functor.whiskerLeft
        (nativeGK4BNPostcompCompatible p ma mb pa pb R)
        (nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb).hom ≫
      Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb) :=
  (Functor.whiskerLeft_comp_whiskerRight
    (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
    (nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb).hom).symm

/-- Interchange with the INVERSE of the genuine comparison k_T,
at the original compatible-source domain and attained target. -/
theorem nativeGK4BUChosenInverse_rightInterchange
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerLeft
        (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) ≫
      Functor.whiskerRight
        (nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb).inv
        (nativeGK4BNPostcompAttained p ma mb pa pb R') =
    Functor.whiskerRight
        (nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb).inv
        (nativeGK4BNPostcompAttained p ma mb pa pb R) ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) :=
  Functor.whiskerLeft_comp_whiskerRight
    (nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb).inv
    (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ)

/-- The strict GK4BP target-NatTrans square, with BOTH
definition-equality transport morphisms from GK4BT retained.
This is a real typed equation, not an informal reassociation. -/
theorem nativeGK4BUExplicitInverse_middleTransport
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb) ≫
      (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R')).hom =
    (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) := by
  simpa only [eqToIso.hom] using
    nativeGK4BUEqToHom_square
      (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R)
      (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R')
      (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb))
      (Functor.whiskerLeft
        (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ))
      (heq_of_eq
        (nativeGK4BPExplicitInverse_targetNat_square p ma mb pa pb ρ).symm)

/-- GK4BU main typed target-natural-transformation square.
Theta_R is the original GK4BT whole NatIso for the arbitrary
GK4BM choice inverse, NOT a claimed strict equality of its
two postcomposition orders. -/
theorem nativeGK4BUChosenInverse_targetNat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R').hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ) := by
  let cR := nativeGK4BNPostcompCompatible p ma mb pa pb R
  let cR' := nativeGK4BNPostcompCompatible p ma mb pa pb R'
  let aR := nativeGK4BNPostcompAttained p ma mb pa pb R
  let aR' := nativeGK4BNPostcompAttained p ma mb pa pb R'
  let qU := nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb
  let pU := nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb
  let qT := nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb
  let pT := nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb
  let kU := nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb
  let kT := nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb
  let δ := nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ
  let ε := nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ
  let eR := eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R)
  let eR' := eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R')
  let α := Functor.whiskerRight δ qU
  let β := Functor.whiskerRight δ pU
  let γ := Functor.whiskerLeft pT ε
  let ζ := Functor.whiskerLeft qT ε
  let leftK := Functor.whiskerLeft cR kU.hom
  let leftK' := Functor.whiskerLeft cR' kU.hom
  let ν := Functor.whiskerRight kT.inv aR
  let ν' := Functor.whiskerRight kT.inv aR'
  have hleft : α ≫ leftK' = leftK ≫ β :=
    nativeGK4BUChosenInverse_leftInterchange p ma mb pa pb ρ
  have hmiddle : β ≫ eR'.hom = eR.hom ≫ γ :=
    nativeGK4BUExplicitInverse_middleTransport p ma mb pa pb ρ
  have hright : γ ≫ ν' = ν ≫ ζ :=
    nativeGK4BUChosenInverse_rightInterchange p ma mb pa pb ρ
  have hpasted : α ≫ ((leftK' ≫ eR'.hom) ≫ ν') =
    ((leftK ≫ eR.hom) ≫ ν) ≫ ζ := by
    calc
      α ≫ ((leftK' ≫ eR'.hom) ≫ ν') =
        ((α ≫ leftK') ≫ eR'.hom) ≫ ν' := by simp only [Category.assoc]
      _ = ((leftK ≫ β) ≫ eR'.hom) ≫ ν' := by rw [hleft]
      _ = (leftK ≫ (β ≫ eR'.hom)) ≫ ν' := by simp only [Category.assoc]
      _ = (leftK ≫ (eR.hom ≫ γ)) ≫ ν' := by rw [hmiddle]
      _ = (leftK ≫ eR.hom) ≫ (γ ≫ ν') := by simp only [Category.assoc]
      _ = (leftK ≫ eR.hom) ≫ (ν ≫ ζ) := by rw [hright]
      _ = ((leftK ≫ eR.hom) ≫ ν) ≫ ζ := by simp only [Category.assoc]
  simpa only [nativeGK4BTChosenInverse_targetNatIso, Iso.trans_hom,
    Functor.isoWhiskerLeft_hom, Functor.isoWhiskerRight_hom,
    Iso.symm_hom] using hpasted

end ChosenInverseTargetNatTrans

#print axioms nativeGK4BUChosenInverse_leftInterchange
#print axioms nativeGK4BUChosenInverse_rightInterchange
#print axioms nativeGK4BUExplicitInverse_middleTransport
#print axioms nativeGK4BUChosenInverse_targetNat_square

end
end Kuu.F112.Physical
