import Kuu.F112.PolygonNativeF55RawFourHorizontalUnitObstructionP79

/-!
# F112-P80 — source-generated P62-relative Type-valued F55 unit 4-cells

P79 proves an EXACT obstruction to giving P77's original 4-cell
quotient a unital horizontal F55 operation: the real horizontal
raw identity pair has a length-TWO P59 proof path, whereas the
target strict identity has length ZERO. Existing P77 4-cells are
SOUND for P59 path EQUALITY, hence cannot compare this pair.

We now make a DISTINCT, explicitly chosen, proof-relevant
presentation. Retain every old P77 genuine Type-valued 4-cell
as a generator, and add ONLY THREE genuinely typed ORIGINAL
source comparison generators:
  - the source F55 horizontal composite of two raw identities
    versus the original raw identity at the same F54 route;
  - left F54 context of a raw unit versus the raw identity;
  - right F54 context of a raw unit versus the raw identity.
Close under actual 4-cell reflexivity, inverse, transitivity and
two-sided vertical whiskering by original F55 raw 3-proofs.

This freely generated Type-valued 4-cell syntax is NOT a theorem
that P77's old four-cells were secretly horizontal-unital, and
it is NOT an equality between original F55 raw proof histories.
The NEW generators are a visible presentation choice. Their
justification is a separate induction proving EVERY generated
4-cell is SOUND for P62's independently source-syntactic
structural-unit PATH CONGRUENCE. Separately prove full original
chosen three-coordinate F55 shadow preservation. Crucially,
do NOT claim soundness for EQUALITY of strict P59 free paths:
P79 proves such a claim would be FALSE on real C60 examples.

Construct the exact Prop boundary Setoid and quotient, an
exact if-and-only-if source witness kernel, vertically compatible
comparison, and observer factorization. Show the actual north
C60 horizontal unit pair is related in this newly chosen quotient
although it is NOT related by P77's narrower raw 4-cell quotient.
This is a strict enlargement at the source-comparison level.

Next obligations: build a vertical Category on this distinct
presentation, transport all original horizontal F55 constructors,
check interchange and higher 4-cell coherence. None of them
is asserted here. No Gray, new Lean axioms, sorry or admit,
and no discarded pre-C60 theory or legacy public roots.
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

/-- A genuinely Type-valued, freely generated SOURCE 4-cell
presentation on the original nine-constructor F55 3-proofs.
Unlike P77, its basic horizontal/context unit comparison is a
NEW SOURCE GENERATOR and is NOT proof of strict free-path equality. -/
inductive NativeF55P80UnitFourCell
    {p : Polygon} {a b : D} {x y : E} :
    ∀ {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | old
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55RawVerticalFourCell first last f g) :
      NativeF55P80UnitFourCell f g
  | refl
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55P80UnitFourCell f f
  | symm
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P80UnitFourCell f g) :
      NativeF55P80UnitFourCell g f
  | trans
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (hfg : NativeF55P80UnitFourCell f g)
      (hgh : NativeF55P80UnitFourCell g h) :
      NativeF55P80UnitFourCell f h
  | leftWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (h : NativeF55P80UnitFourCell f g) :
      NativeF55P80UnitFourCell (.trans prior f) (.trans prior g)
  | rightWhisker
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55P80UnitFourCell f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55P80UnitFourCell (.trans f suffix) (.trans g suffix)
  | horizontalUnit
      {n n' m m' k k' l l' : Nat}
      {p₀ p₁ p₂ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ : KuuNativeBlocks x y}
      {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
      {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
      {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
      {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
      (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
      (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
      NativeF55P80UnitFourCell
        ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u).horizontal
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident v))
        (.ident (nativeF55HorizontalUnitRoute u v))
  | leftContextUnit
      {n n' m m' k l : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      (u : KuuNativeF45Tree.DepthRotationRoute p first last)
      (later : KuuNativeF45Tree p k l mb pb mc pc) :
      NativeF55P80UnitFourCell
        (.leftContext (.ident u) later)
        (.ident (.leftContext u later))
  | rightContextUnit
      {k l n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p k l ma pa mb pb)
      {first : KuuNativeF45Tree p n m mb pb mc pc}
      {last : KuuNativeF45Tree p n' m' mb pb mc pc}
      (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
      NativeF55P80UnitFourCell
        (.rightContext earlier (.ident u))
        (.ident (.rightContext earlier u))

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- The correct P80 notion of soundness: EVERY chosen Type-valued
4-cell witness maps to the independently source-generated P62
structural-unit path congruence, NOT to equality of raw free paths.
The induction covers ALL eight genuinely specified constructors. -/
theorem NativeF55P80UnitFourCell.p62_sound
    (h : NativeF55P80UnitFourCell f g) :
    NativeF55UnitPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  induction h with
  | old w => exact w.toUnitPathRel
  | refl w => exact .refl _
  | symm h ih => exact .symm ih
  | trans hfg hgh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior h ih =>
      exact NativeF55UnitPathRel.prepend prior.toNativeStrictPath ih
  | rightWhisker h suffix ih =>
      exact NativeF55UnitPathRel.append suffix.toNativeStrictPath ih
  | horizontalUnit u v =>
      exact nativeF55RawFour_horizontal_identity_unitPathRelated u v
  | leftContextUnit u later =>
      exact nativeF55RawFour_leftContext_identity_unitPathRelated u later
  | rightContextUnit earlier u =>
      exact nativeF55RawFour_rightContext_identity_unitPathRelated earlier u

/-- Independently of P62, all new proof-relevant 4-cell generators
preserve the FULL original chosen F55 native shadow. This does not
define the equivalence relation by numerical equality. -/
theorem NativeF55P80UnitFourCell.shadow_sound
    (h : NativeF55P80UnitFourCell f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | old w => exact w.shadow_sound
  | refl w => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | horizontalUnit u v =>
      exact nativeF55RawFour_horizontal_identity_shadow_eq u v
  | leftContextUnit u later => rfl
  | rightContextUnit earlier u => rfl

/-- This new 4-cell relation remains a genuine VERTICAL source
congruence. Each witness is retained, not reconstructed from P62
Prop equality or a scalar grade. -/
theorem nativeF55P80UnitFour_comp_congr
    (h : NativeF55P80UnitFourCell f g)
    {w : KuuNativeF45Tree.DepthRotationRoute p first last}
    {r s : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
    (k : NativeF55P80UnitFourCell r s) :
    NativeF55P80UnitFourCell
      (.trans f r) (.trans g s) :=
  .trans (.rightWhisker h r) (.leftWhisker g k)

/-- The precise Prop boundary of this distinctly selected P80
source 4-cell presentation, generated by the exhibited witnesses. -/
def nativeF55P80UnitFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55P80UnitFourCell f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- A new, HONEST source-comparison quotient that differs from
P77; original raw F55 proof trees are never identified upstream. -/
abbrev NativeF55P80UnitFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55P80UnitFourSetoid first last u v)

def nativeF55P80UnitFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55P80UnitFourClasses first last u v :=
  _root_.Quotient.mk _ raw

/-- EXACT source witness kernel, without replacing proof existence
by numerical shadow equality or arbitrary P62 path relation. -/
theorem nativeF55P80UnitFourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P80UnitFourClass first last f =
      nativeF55P80UnitFourClass first last g ↔
      Nonempty (NativeF55P80UnitFourCell f g) := by
  constructor
  · intro eq
    exact _root_.Quotient.exact eq
  · intro hw
    exact _root_.Quotient.sound hw

/-- Every source 4-cell class equality is SOUND under P62's
independent typed unit-only path congruence; the converse is
deliberately not asserted or forced by an observer. -/
theorem nativeF55P80UnitFourClass_eq_implies_P62
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (heq : nativeF55P80UnitFourClass first last f =
      nativeF55P80UnitFourClass first last g) :
    NativeF55UnitPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  obtain ⟨w⟩ := (nativeF55P80UnitFourClass_eq_iff first last f g).mp heq
  exact w.p62_sound

/-- All chosen original signed charge and odd exchange phase
coordinates descend constructively to the new P80 4-cell quotient. -/
def nativeF55P80UnitFourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55P80UnitFourClasses first last u v →
      KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- The original selected FULL shadow is still exactly obtained
from each genuine raw source 3-proof in the new presentation. -/
theorem nativeF55P80UnitFourToShadow_spec
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55P80UnitFourToShadow first last u v
      (nativeF55P80UnitFourClass first last raw) =
        raw.nativeShadow := rfl

/-- The actually physical north C60 horizontal-unit comparison
has a NEW, EXPLICIT Type-valued witness in this P80 presentation,
not one extracted from P77 or equality of its full shadow. -/
theorem northHexagonNativeHorizontalUnit_P80_fourWitness :
    Nonempty (NativeF55P80UnitFourCell
      northHexagonNativeHorizontalRawIdentityPair
      northHexagonNativeHorizontalStrictIdentity) := by
  exact ⟨.horizontalUnit
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute⟩

/-- This new source presentation CERTIFIES equality in its new
quotient of the original physical C60 two raw horizontal units. -/
theorem northHexagonNativeHorizontalUnit_P80_class_eq :
    nativeF55P80UnitFourClass _ _
      northHexagonNativeHorizontalRawIdentityPair =
    nativeF55P80UnitFourClass _ _
      northHexagonNativeHorizontalStrictIdentity := by
  exact (nativeF55P80UnitFourClass_eq_iff _ _ _ _).2
    northHexagonNativeHorizontalUnit_P80_fourWitness

/-- Compare with the OLDER P77 source 4-cell quotient: its original
two C60 classes remain UNEQUAL. P80 is an honest distinct selected
presentation, and the old P79 obstruction is not erased historically. -/
theorem northHexagonNativeHorizontalUnit_P77_class_ne :
    nativeF55RawVerticalFourClass _ _
      northHexagonNativeHorizontalRawIdentityPair ≠
    nativeF55RawVerticalFourClass _ _
      northHexagonNativeHorizontalStrictIdentity := by
  exact nativeF55RawFour_horizontal_identity_class_ne
    northHexagonNativeLeftF54UnitRoute
    northHexagonNativeRightF54UnitRoute

#print axioms NativeF55P80UnitFourCell
#print axioms NativeF55P80UnitFourCell.p62_sound
#print axioms NativeF55P80UnitFourCell.shadow_sound
#print axioms nativeF55P80UnitFour_comp_congr
#print axioms nativeF55P80UnitFourSetoid
#print axioms NativeF55P80UnitFourClasses
#print axioms nativeF55P80UnitFourClass
#print axioms nativeF55P80UnitFourClass_eq_iff
#print axioms nativeF55P80UnitFourClass_eq_implies_P62
#print axioms nativeF55P80UnitFourToShadow
#print axioms nativeF55P80UnitFourToShadow_spec
#print axioms northHexagonNativeHorizontalUnit_P80_fourWitness
#print axioms northHexagonNativeHorizontalUnit_P80_class_eq
#print axioms northHexagonNativeHorizontalUnit_P77_class_ne

end
end Kuu.F112.Physical
