import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BOriginalInclusionNoFaithfulReturn

/-!
# F112-P94D3GK4C — ORIGINAL P92B cannot fill genuine F54 unit seams

P92A preserves the complete ordered zero-chain context words through
all nine original F55 constructors. P92B adds a typed associator-
naturality constructor that changes the ordered context WORDS, but
does NOT change their NUMBER. We prove that the number of true
zero-chain atoms is preserved by every original P92B constructor,
including P92B associator naturality, contexts and pre/postcomposition.

The independent original F54 StructuralSeam.leftUnit/rightUnit
constructors ADD exactly ONE genuine original zero-edge chain.
Consequently NO original P92B 3-cell can fill either typed unit seam.
This is a genuinely original Type-valued obstruction, not a shadow
or a quotient, and does not assert no-go for other presentations.

From an actual original F45 stage, we derive failure of the GK4
"every F54 seam has a P92B filler" condition, and therefore failure
of any boundary-preserving whole-presentation return. GK4B's
relative noninjectivity no-go is sharpened to existence obstruction
on every inhabited original F45 stage (NOT on an empty source type).

Lean v4.30.0-rc2; pinned mathlib, no sorry/admit/new axiom,
append-only, 107 public roots and protected validation PR untouched.
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

/-- Number of true original F54 zero-edge unit atoms, regardless of
their left/right binary context words. Not a numerical F55 shadow. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4cUnitCount
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Nat :=
  route.p92UnitContextWords.length

section CountLaws

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Vertical F54 composition concatenates all original zero-chain
atoms, including their entire provenance. -/
@[simp] theorem nativeGK4C_unitCount_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4cUnitCount =
      u.gk4cUnitCount + v.gk4cUnitCount := by
  change (u.p92UnitContextWords ++ v.p92UnitContextWords).length =
    u.p92UnitContextWords.length + v.p92UnitContextWords.length
  simp only [List.length_append]

/-- F54 left contextualization changes the zero-chain WORD, but not
the number of its original zero-chain atoms. -/
@[simp] theorem nativeGK4C_unitCount_leftContext
    {n n' m m' k l : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext u later).gk4cUnitCount =
      u.gk4cUnitCount := by
  change (u.p92UnitContextWords.map (fun word => false :: word)).length =
    u.p92UnitContextWords.length
  simp

@[simp] theorem nativeGK4C_unitCount_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier u).gk4cUnitCount =
      u.gk4cUnitCount := by
  change (u.p92UnitContextWords.map (fun word => true :: word)).length =
    u.p92UnitContextWords.length
  simp

/-- Real original F54 associator is a nonzero rotation edge, NOT a
zero-edge reflexivity chain. -/
@[simp] theorem nativeGK4C_unitCount_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {m₀ m₁' m₂' m₃' : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ m₀ q₀ m₁' q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ m₁' q₁ m₂' q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ m₂' q₂ m₃' q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4cUnitCount =
      0 := by
  rfl

/-- A genuine original F54 reflexivity chain contains one unit atom. -/
@[simp] theorem nativeGK4C_unitCount_unit
    {n m : Nat}
    (t : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute.chain
      (KuuNativeF45Tree.RotationChain.refl t)).gk4cUnitCount = 1 := by
  rfl

end CountLaws

/-- The genuine original two-axis F54 horizontal route uses the two
source histories exactly once: count is additive. -/
theorem nativeGK4C_horizontal_unitCount
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4cUnitCount =
      u.gk4cUnitCount + v.gk4cUnitCount := by
  simp only [nativeF54P90HorizontalRoute, nativeGK4C_unitCount_trans,
    nativeGK4C_unitCount_leftContext, nativeGK4C_unitCount_rightContext]

/-- P92B's NEW associator-naturality constructor is compatible with
unit-ATOM COUNT, even though P92A shows it does not preserve the entire
ordered context-word list. -/
theorem nativeGK4C_assocNaturality_unitCount
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4cUnitCount =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4cUnitCount := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute,
    nativeGK4C_unitCount_trans, nativeGK4C_unitCount_assoc,
    nativeGK4C_horizontal_unitCount]
  omega

/-- Key GK4C invariant: EVERY ORIGINAL P92B 3-cell preserves the
number of F54 zero-edge unit atoms, including all nine constructors
and the NEW triple associator-naturality generator. -/
theorem nativeGK4C_P92B_unitCount_sound
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4cUnitCount = s.gk4cUnitCount := by
  induction cell with
  | original old =>
      exact congrArg List.length old.p92UnitContextWords_sound
  | assocNaturality u v w =>
      exact nativeGK4C_assocNaturality_unitCount u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih =>
      simpa only [nativeGK4C_unitCount_leftContext] using ih
  | rightContext earlier cell ih =>
      simpa only [nativeGK4C_unitCount_rightContext] using ih
  | precompose priorRoute cell ih =>
      simpa only [nativeGK4C_unitCount_trans] using
        congrArg (fun k : Nat => priorRoute.gk4cUnitCount + k) ih
  | postcompose cell suffix ih =>
      simpa only [nativeGK4C_unitCount_trans] using
        congrArg (fun k : Nat => k + suffix.gk4cUnitCount) ih

/-- An actual F54 LEFT-UNIT structural seam has no original P92B
Type-valued filler: it changes the preserved atom count by +1. -/
theorem nativeGK4C_leftUnit_no_P92B
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P92AssocComparison p
      (.trans (.chain (.refl first)) r) r) := by
  rintro ⟨cell⟩
  have hcount := nativeGK4C_P92B_unitCount_sound cell
  have h : 1 + r.gk4cUnitCount = r.gk4cUnitCount := by
    simpa only [nativeGK4C_unitCount_trans, nativeGK4C_unitCount_unit] using hcount
  omega

/-- Same obstruction for an original F54 RIGHT-UNIT seam. -/
theorem nativeGK4C_rightUnit_no_P92B
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P92AssocComparison p
      (.trans r (.chain (.refl last))) r) := by
  rintro ⟨cell⟩
  have hcount := nativeGK4C_P92B_unitCount_sound cell
  have h : r.gk4cUnitCount + 1 = r.gk4cUnitCount := by
    simpa only [nativeGK4C_unitCount_trans, nativeGK4C_unitCount_unit] using hcount
  omega

/-- Any ACTUAL original F45 stage supplies a genuine reflexive F54
route, hence a left-unit seam which original P92B cannot realize. -/
theorem nativeGK4C_no_all_seam_P92B_of_tree
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ Nonempty (NativeGK4SeamP92Realization p D E) := by
  rintro ⟨h⟩
  let r : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  have cell : NativeF55P92AssocComparison p
      (.trans (.chain (.refl tree)) r) r :=
    h (nativeGK2PackSeam (NativeF54StructuralSeam.leftUnit r))
  exact nativeGK4C_leftUnit_no_P92B r ⟨cell⟩

/-- GK4's conditional existence gate is therefore BLOCKED on every
originally inhabited F45-stage context: no total typed P92B return. -/
theorem nativeGK4C_no_structural_P92B_return_of_tree
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {p : Polygon} {a b : D} {x y : E}
    {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ Nonempty (NativeGK4StructuralP92Return p D E) := by
  rintro ⟨ret⟩
  exact nativeGK4C_no_all_seam_P92B_of_tree tree
    ⟨nativeGK4RestrictReturnToSeams ret⟩

/-! ### ACTUAL C60 physical specialization, not a merely formal tree. -/

/-- The independent C60 north hexagon contains the genuine original
F45 native stage at sector 0. Its new structural left-unit seam is
not realizable in the original P92B presentation. -/
theorem nativeGK4C_physical_north_hexagon_no_all_seam_P92B :
    ¬ Nonempty (NativeGK4SeamP92Realization
      (.hexagon (.top 0)) Site Site) := by
  exact nativeGK4C_no_all_seam_P92B_of_tree (northHexagonNativeUnit 0)

/-- Therefore even an arbitrary boundary-preserving total
StructuralComparison-to-P92B return cannot exist on this genuine
physical C60 hexagon, independently of injectivity requirements. -/
theorem nativeGK4C_physical_north_hexagon_no_return :
    ¬ Nonempty (NativeGK4StructuralP92Return
      (.hexagon (.top 0)) Site Site) := by
  exact nativeGK4C_no_structural_P92B_return_of_tree
    (northHexagonNativeUnit 0)

#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4cUnitCount
#print axioms nativeGK4C_unitCount_trans
#print axioms nativeGK4C_unitCount_leftContext
#print axioms nativeGK4C_unitCount_rightContext
#print axioms nativeGK4C_unitCount_assoc
#print axioms nativeGK4C_unitCount_unit
#print axioms nativeGK4C_horizontal_unitCount
#print axioms nativeGK4C_assocNaturality_unitCount
#print axioms nativeGK4C_P92B_unitCount_sound
#print axioms nativeGK4C_leftUnit_no_P92B
#print axioms nativeGK4C_rightUnit_no_P92B
#print axioms nativeGK4C_no_all_seam_P92B_of_tree
#print axioms nativeGK4C_no_structural_P92B_return_of_tree
#print axioms nativeGK4C_physical_north_hexagon_no_all_seam_P92B
#print axioms nativeGK4C_physical_north_hexagon_no_return

end
end Kuu.F112.Physical
