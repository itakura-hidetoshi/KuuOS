import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEFourObserver
import Mathlib.Tactic

/-!
F112-P94D3GK4AE — TRUE second P92B observation kernel K_AE,
canonical structural S -> K_AE comparison, and genuine quotient
projection K_AE -> former triple K_AA.

The fourth ordered moment is not an arbitrary independent numeric
variable: its AD charge/backward coordinates are PROVED equal to the
actual W/Z coordinates of the original F54 route. Thus the projection
from four values to the existing three-component observation is
verified from the complete original F54 dependent grammar, not
assumed by conflating two previously separate quotient definitions.
The existing original Q is NOT asserted to be a category.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section SourceProjectionCertificate
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n m : Nat}
variable {first last : KuuNativeF45Tree p n m ma pa mb pb}

/-- EACH actual source F54 orientation edge has original W/Z
observations (-1, 0) for forward or (-1, 1) for backward. -/
theorem KuuNativeF45Tree.RotationEdge.gk4aeADFirstPair
    (edge : KuuNativeF45Tree.RotationEdge p first last) :
    edge.gk4adValue.1 = ((-1 : Int), edge.gk4zBackwardCount) := by
  cases edge with
  | forward rot => rfl
  | backward rot => rfl

/-- Genuine finite RotationChain: AD charge is minus the number of
real physical rotation edges; AD backward count is GK4Z count. -/
theorem KuuNativeF45Tree.RotationChain.gk4aeADFirstPair
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    chain.gk4adValue.1 =
      ((-(chain.length : Int)), chain.gk4zBackwardCount) := by
  induction chain with
  | refl => rfl
  | snoc prior edge ih =>
      have he := edge.gk4aeADFirstPair
      apply Prod.ext
      · change prior.gk4adValue.1.1 + edge.gk4adValue.1.1 =
          (-(((prior.length + 1 : Nat) : Int)))
        rw [congrArg Prod.fst ih, congrArg Prod.fst he]
        push_cast
        omega
      · change prior.gk4adValue.1.2 + edge.gk4adValue.1.2 =
          prior.gk4zBackwardCount + edge.gk4zBackwardCount
        rw [congrArg Prod.snd ih, congrArg Prod.snd he]

end SourceProjectionCertificate

section FullOriginalDepthProjection
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Exact bridge between the two independently built raw observers,
checked by induction on EVERY original dependent F54 constructor. -/
theorem KuuNativeF45Tree.DepthRotationRoute.gk4aeADFirstPair
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    r.gk4adValue.1 = (r.gk4wCastCharge, r.gk4zBackwardCount) := by
  induction r with
  | chain path =>
      change path.gk4adValue.1 =
        (((0 : Int) - (path.length : Int)), path.gk4zBackwardCount)
      rw [path.gk4aeADFirstPair]
      simp
  | castDepths hn hm tree =>
      rfl
  | trans left right ihLeft ihRight =>
      apply Prod.ext
      · change left.gk4adValue.1.1 + right.gk4adValue.1.1 =
          (KuuNativeF45Tree.DepthRotationRoute.trans left right).gk4wCastCharge
        rw [congrArg Prod.fst ihLeft, congrArg Prod.fst ihRight,
          nativeGK4W_charge_trans]
      · change left.gk4adValue.1.2 + right.gk4adValue.1.2 =
          (KuuNativeF45Tree.DepthRotationRoute.trans left right).gk4zBackwardCount
        rw [congrArg Prod.snd ihLeft, congrArg Prod.snd ihRight,
          nativeGK4ZBackward_trans]
  | leftContext path later ih =>
      change path.gk4adValue.1 =
        ((KuuNativeF45Tree.DepthRotationRoute.leftContext path later).gk4wCastCharge,
         (KuuNativeF45Tree.DepthRotationRoute.leftContext path later).gk4zBackwardCount)
      rw [nativeGK4W_charge_leftContext, nativeGK4ZBackward_leftContext]
      exact ih
  | rightContext earlier path ih =>
      change path.gk4adValue.1 =
        ((KuuNativeF45Tree.DepthRotationRoute.rightContext earlier path).gk4wCastCharge,
         (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier path).gk4zBackwardCount)
      rw [nativeGK4W_charge_rightContext, nativeGK4ZBackward_rightContext]
      exact ih

end FullOriginalDepthProjection

section OriginalAndIndependentStructural
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- True projection from the quadruple original Q observer to
the preexisting triple Q observer, NOT numeric-to-Type witnesses. -/
theorem nativeGK4AEQuadP92_forget
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AEForgetValue (nativeGK4AEQuadP92 first last q) =
      nativeGK4AATripleP92 first last q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change
    ((nativeGK4GRawGrade first last raw, raw.gk4adValue.1.1),
      raw.gk4adValue.1.2) =
    ((nativeGK4GRawGrade first last raw, raw.gk4wCastCharge),
      raw.gk4zBackwardCount)
  have h := raw.gk4aeADFirstPair
  rcases Prod.mk.inj h with ⟨hcast, hback⟩
  exact Prod.ext (Prod.ext rfl hcast) hback

/-- The independently descended S observer commutes with exactly
the SAME canonical projection on genuine S route representatives. -/
theorem nativeGK4AEQuadStructural_forget
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AEForgetValue (nativeGK4AEQuadStructural first last s) =
      nativeGK4AATripleStructural first last s := by
  refine _root_.Quotient.inductionOn s ?_
  intro raw
  change
    ((nativeGK4GRawGrade first last raw, raw.gk4adValue.1.1),
      raw.gk4adValue.1.2) =
    ((nativeGK4GRawGrade first last raw, raw.gk4wCastCharge),
      raw.gk4zBackwardCount)
  have h := raw.gk4aeADFirstPair
  rcases Prod.mk.inj h with ⟨hcast, hback⟩
  exact Prod.ext (Prod.ext rfl hcast) hback

/-- True GK4T criterion for the four-component observation:
ALL fourteen original structural seams are sound. -/
theorem nativeGK4AEComparisonExists :
    NativeGK4TComparisonExists
      (nativeGK4AEQuadP92Family p D E) first last := by
  exact (nativeGK4TComparisonExists_iff_seam
    (nativeGK4AEQuadP92Family p D E) first last).mpr
      (nativeGK4AEQuadSeamInvariant first last)

/-- The actual S -> K_AE comparison between genuinely separate
original Type-valued equivalence quotients. -/
def nativeGK4AEComparison :
    NativeGK4EStructuralRouteClasses first last →
      NativeGK4SKernelClasses
        (nativeGK4AEQuadP92Family p D E) first last :=
  nativeGK4TComparison (nativeGK4AEQuadP92Family p D E)
    first last (nativeGK4AEQuadSeamInvariant first last)

theorem nativeGK4AEComparison_value
    (u : NativeGK4EStructuralRouteClasses first last) :
    (nativeGK4SKernelImageEquiv
        (nativeGK4AEQuadP92Family p D E) first last
        (nativeGK4AEComparison first last u)).val =
      nativeGK4AEQuadStructural first last u := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective first last u
  simpa only [nativeGK4AEComparison,
    nativeGK4TComparison_class, nativeGK4SKernelImageEquiv_class]
    using (nativeGK4AEQuad_commutes first last q).symm

theorem nativeGK4AEComparison_eq_iff
    (u v : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AEComparison first last u =
      nativeGK4AEComparison first last v ↔
    nativeGK4AEQuadStructural first last u =
      nativeGK4AEQuadStructural first last v := by
  constructor
  · intro h
    have hval := congrArg
      (fun z : NativeGK4SKernelClasses
          (nativeGK4AEQuadP92Family p D E) first last =>
        (nativeGK4SKernelImageEquiv
          (nativeGK4AEQuadP92Family p D E) first last z).val) h
    simpa only [nativeGK4AEComparison_value] using hval
  · intro h
    apply (nativeGK4SKernelImageEquiv
      (nativeGK4AEQuadP92Family p D E) first last).injective
    apply Subtype.ext
    simpa only [nativeGK4AEComparison_value] using h

theorem nativeGK4AEComparison_injective_iff :
    Function.Injective (nativeGK4AEComparison first last) ↔
      Function.Injective (nativeGK4AEQuadStructural first last) := by
  constructor
  · intro hinj u v h
    exact hinj ((nativeGK4AEComparison_eq_iff first last u v).mpr h)
  · intro hinj u v h
    exact hinj ((nativeGK4AEComparison_eq_iff first last u v).mp h)

theorem nativeGK4AEComparison_surjective :
    Function.Surjective (nativeGK4AEComparison first last) := by
  exact nativeGK4TComparison_surjective
    (nativeGK4AEQuadP92Family p D E) first last
    (nativeGK4AEQuadSeamInvariant first last)

/-- The original three observer and fourth ordered moment are
separately visible after genuine S descent. -/
theorem nativeGK4AEComparison_eq_iff_components
    (u v : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AEComparison first last u =
      nativeGK4AEComparison first last v ↔
    nativeGK4AATripleStructural first last u =
      nativeGK4AATripleStructural first last v ∧
    (nativeGK4ADStructuralValue first last u).2 =
      (nativeGK4ADStructuralValue first last v).2 := by
  rw [nativeGK4AEComparison_eq_iff]
  constructor
  · intro h
    exact ⟨by
        have hproj := congrArg nativeGK4AEForgetValue h
        simpa only [nativeGK4AEQuadStructural_forget] using hproj,
      congrArg (fun z : NativeGK4AEValue => z.2.2) h⟩
  · rintro ⟨htriple, hm⟩
    apply Prod.ext
    · have htr := congrArg (fun z : NativeGK4AAValue => z.1.1) htriple
      exact htr
    · apply Prod.ext
      · have hp := (nativeGK4AEQuadStructural_forget first last u).trans
          (htriple.trans (nativeGK4AEQuadStructural_forget first last v).symm)
        apply Prod.ext
        · exact congrArg (fun z : NativeGK4AAValue => z.1.2) hp
        · exact congrArg (fun z : NativeGK4AAValue => z.2) hp
      · exact hm

end OriginalAndIndependentStructural

/-- The genuine four-component ambient value category, separate
from structural S, original Q, and the attained K_AE second kernel. -/
inductive NativeGK4AEValuePoint : Type where
  | star

instance nativeGK4AEValueCategory : Category NativeGK4AEValuePoint where
  Hom _ _ := NativeGK4AEValue
  id _ := nativeGK4AEUnit
  comp u v := nativeGK4AECombine u v
  id_comp := by
    intro X Y f
    exact nativeGK4AECombine_leftUnit f
  comp_id := by
    intro X Y f
    exact nativeGK4AECombine_rightUnit f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4AECombine_assoc f g h

def nativeGK4AEValueFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤ NativeGK4AEValuePoint where
  obj _ := .star
  map := fun {X Y} f => nativeGK4AEQuadStructural X.2.2 Y.2.2 f
  map_id := by
    intro X
    exact nativeGK4AEQuadStructural_unit X.2.2
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AEQuadStructural_compose X.2.2 Y.2.2 Z.2.2 f g

def nativeGK4AEForgetMomentValueFunctor :
    NativeGK4AEValuePoint ⥤ NativeGK4AAValuePoint where
  obj _ := .star
  map := fun {X Y} f => nativeGK4AEForgetValue f
  map_id := by
    intro X
    exact nativeGK4AEForgetValue_unit
  map_comp := by
    intro X Y Z f g
    exact nativeGK4AEForgetValue_combine f g

#print axioms KuuNativeF45Tree.RotationEdge.gk4aeADFirstPair
#print axioms KuuNativeF45Tree.RotationChain.gk4aeADFirstPair
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4aeADFirstPair
#print axioms nativeGK4AEQuadP92_forget
#print axioms nativeGK4AEQuadStructural_forget
#print axioms nativeGK4AEComparisonExists
#print axioms nativeGK4AEComparison
#print axioms nativeGK4AEComparison_value
#print axioms nativeGK4AEComparison_eq_iff
#print axioms nativeGK4AEComparison_injective_iff
#print axioms nativeGK4AEComparison_surjective
#print axioms nativeGK4AEComparison_eq_iff_components
#print axioms NativeGK4AEValuePoint
#print axioms nativeGK4AEValueCategory
#print axioms nativeGK4AEValueFunctor
#print axioms nativeGK4AEForgetMomentValueFunctor

end
end Kuu.F112.Physical
