import Kuu.F112.PolygonNativeF55BridgeTransportPathCoherenceP76

/-!
# F112-P77 — genuine Type-valued raw vertical 4-cell certificates

P76 proves a conditional bridge-transport coherence at the
full chosen F55 shadow and at the independent P59 strict-path
normalization. However the free original F55 raw proof trees are
NOT identified merely because the two observations agree.

We now specify a FIRST genuinely proof-relevant 4-cell language
on those original raw 3-proofs: its generating constructors are
reflexivity, reversal, concatenation of 4-cells, whiskering by
arbitrary original typed F55 3-proofs on either side, and the
VERTICAL unit and associativity source comparison certificates.

These certificates are Type-valued with the exact dependent
F54 route endpoints, not equalities of numerically evaluated
shadows. A recursive soundness proof shows their normalized
P59 strict paths agree, and SEPARATELY proves the three original
selected F55 shadow coordinates agree. The chosen observations
do not define the 4-cell relation.

From actual certificates (via Nonempty only at the Prop boundary)
we construct an exact Setoid / quotient kernel on each original
F55 raw 3-Hom. The original unquotiented proof terms and
the explicit 4-cell witnesses remain accessible upstream.
There is no claim that arbitrary equal-shadow or equal-path
raw source proofs must possess a 4-cell.

The genuine north C60 disjoint-square raw generator is
distinct from its left-unit composite in the ORIGINAL syntax;
a selected nontrivial 4-cell explicitly compares the two.
This is a step toward strict vertical 3-composition, NOT proof of
horizontal 3-interchange, global strict 3/n, or hyperdescent.

No Gray, new axiom, sorry, admit, or loss of 107 public roots.
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

/-- The LEAST recursively generated Type-valued evidence for vertical
unit, associativity and two-sided composition compatibility of ACTUAL
nine-constructor original F55 source 3-proof trees. Both operands
have the very same genuinely typed F54 route endpoints. -/
inductive NativeF55RawVerticalFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v →
      Type (max (max uD uE) (max vD vE)) where
  | refl {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55RawVerticalFourCell first last raw raw
  | symm {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55RawVerticalFourCell first last f g) :
      NativeF55RawVerticalFourCell first last g f
  | trans {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (hfg : NativeF55RawVerticalFourCell first last f g)
      (hgh : NativeF55RawVerticalFourCell first last g h) :
      NativeF55RawVerticalFourCell first last f h
  | leftWhisker
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
      (h : NativeF55RawVerticalFourCell first last f g) :
      NativeF55RawVerticalFourCell first last
        (.trans prior f) (.trans prior g)
  | rightWhisker
      {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
      (h : NativeF55RawVerticalFourCell first last f g)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w) :
      NativeF55RawVerticalFourCell first last
        (.trans f suffix) (.trans g suffix)
  | leftUnit
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55RawVerticalFourCell first last
        (.trans (.ident u) raw) raw
  | rightUnit
      {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
      (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
      NativeF55RawVerticalFourCell first last
        (.trans raw (.ident v)) raw
  | assoc
      {u v w z : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
      (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p w z) :
      NativeF55RawVerticalFourCell first last
        (.trans (.trans f g) h) (.trans f (.trans g h))

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}

/-- A recursively certified genuine raw 4-cell always relates equal
STRICT P59 normal forms; path equality is a derived soundness theorem,
not the definition of a 4-cell. -/
theorem NativeF55RawVerticalFourCell.path_sound
    (h : NativeF55RawVerticalFourCell first last f g) :
    f.toNativeStrictPath = g.toNativeStrictPath := by
  induction h with
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      simpa only [
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans]
        using congrArg (fun z => prior.toNativeStrictPath.comp z) ih
  | rightWhisker h suffix ih =>
      simpa only [
        KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans]
        using congrArg (fun z => z.comp suffix.toNativeStrictPath) ih
  | leftUnit raw => exact raw.toNativeStrictPath_leftUnit
  | rightUnit raw => exact raw.toNativeStrictPath_rightUnit
  | assoc a b c => exact a.toNativeStrictPath_assoc b c

/-- Full chosen signed pentagon charge, square charge and odd phase
are preserved by every certified source vertical 4-cell. We prove
this separately from the strictly stronger typed path readout. -/
theorem NativeF55RawVerticalFourCell.shadow_sound
    (h : NativeF55RawVerticalFourCell first last f g) :
    f.nativeShadow = g.nativeShadow := by
  induction h with
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.nativeShadow + _ = prior.nativeShadow + _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ + suffix.nativeShadow = _ + suffix.nativeShadow
      rw [ih]
  | leftUnit raw =>
      change (0 : KuuNativeF55Shadow) + raw.nativeShadow =
        raw.nativeShadow
      exact zero_add _
  | rightUnit raw =>
      change raw.nativeShadow + (0 : KuuNativeF55Shadow) =
        raw.nativeShadow
      exact add_zero _
  | assoc a b c =>
      change (a.nativeShadow + b.nativeShadow) + c.nativeShadow =
        a.nativeShadow + (b.nativeShadow + c.nativeShadow)
      exact add_assoc _ _ _

/-- This genuine 4-cell relation is compatible with the earlier
P62 STRUCTURAL-UNIT path equivalence: after genuine P59 normalization
its endpoints are equal, hence P62-related. It does not identify
arbitrary P62-related raw F55 source cells in the other direction. -/
theorem NativeF55RawVerticalFourCell.toUnitPathRel
    (h : NativeF55RawVerticalFourCell first last f g) :
    NativeF55UnitPathRel first last
      f.toNativeStrictPath g.toNativeStrictPath := by
  rw [h.path_sound]
  exact .refl _

/-- The only Prop-level identification is existence of an actual
Type-valued 4-cell certificate: never equality of shadow values. -/
def nativeF55RawVerticalFourSetoid
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) where
  r := fun f g => Nonempty (NativeF55RawVerticalFourCell first last f g)
  iseqv := ⟨
    (fun raw => ⟨.refl raw⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- Only quotient the chosen independent raw vertical 4-cell source
certificates; actual original source trees are retained upstream. -/
abbrev NativeF55RawVerticalFourClasses
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :=
  _root_.Quotient (nativeF55RawVerticalFourSetoid first last u v)

/-- Canonical projection from genuine raw F55 three-proofs. -/
def nativeF55RawVerticalFourClass
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    NativeF55RawVerticalFourClasses first last u v :=
  _root_.Quotient.mk _ raw

/-- Exact kernel iff, derived from the SOURCE 4-cell Setoid. -/
theorem nativeF55RawVerticalFourClass_eq_iff
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw₁ raw₂ :
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55RawVerticalFourClass first last raw₁ =
        nativeF55RawVerticalFourClass first last raw₂ ↔
      Nonempty (NativeF55RawVerticalFourCell first last raw₁ raw₂) := by
  constructor
  · intro heq
    exact _root_.Quotient.exact heq
  · intro hw
    exact _root_.Quotient.sound hw

/-- Strict path readout is actually well-defined on the new source
4-cell quotient, proved from the 4-cell induction (not vice versa). -/
def nativeF55RawVerticalFourToPath
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last u v →
      Quiver.Path
        (⟨u⟩ : NativeF55RawRouteVertex first last)
        (⟨v⟩ : NativeF55RawRouteVertex first last) :=
  _root_.Quotient.lift
    (fun raw => raw.toNativeStrictPath)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.path_sound)

/-- The independent F55 three-coordinate observer likewise factors
through this structural quotient by the separately proved soundness. -/
def nativeF55RawVerticalFourToShadow
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last u v →
      KuuNativeF55Shadow :=
  _root_.Quotient.lift
    (fun raw => raw.nativeShadow)
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact w.shadow_sound)

/-- No choice of raw representative is needed to compute its certified
P59 free-path image: projection followed by readout is original. -/
theorem nativeF55RawVerticalFourToPath_spec
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55RawVerticalFourToPath first last u v
      (nativeF55RawVerticalFourClass first last raw) =
        raw.toNativeStrictPath := rfl

/-- Same factorization for the full signed F55 observer; this is
not a proof of converse faithfulness of either readout. -/
theorem nativeF55RawVerticalFourToShadow_spec
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55RawVerticalFourToShadow first last u v
      (nativeF55RawVerticalFourClass first last raw) =
        raw.nativeShadow := rfl

/-- Real C60 square: original F55 free source proof trees are
NOT equal, but a specified nontrivial Type-valued vertical
unit 4-cell compares them. Neither the raw square nor its
odd phase is discarded in the original presentation. -/
theorem northHexagonNativeSquare_rawDistinct_but_fourRelated :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (.ident northHexagonNativeSquareLeft)
      northHexagonNativeF55SquareCell) ≠
        northHexagonNativeF55SquareCell ∧
      Nonempty (NativeF55RawVerticalFourCell _ _
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
          (.ident northHexagonNativeSquareLeft)
          northHexagonNativeF55SquareCell)
        northHexagonNativeF55SquareCell) := by
  refine ⟨northHexagonNativeF55Square_ne_leftUnit.symm, ?_⟩
  exact ⟨.leftUnit northHexagonNativeF55SquareCell⟩

#print axioms NativeF55RawVerticalFourCell
#print axioms NativeF55RawVerticalFourCell.path_sound
#print axioms NativeF55RawVerticalFourCell.shadow_sound
#print axioms NativeF55RawVerticalFourCell.toUnitPathRel
#print axioms nativeF55RawVerticalFourSetoid
#print axioms NativeF55RawVerticalFourClasses
#print axioms nativeF55RawVerticalFourClass
#print axioms nativeF55RawVerticalFourClass_eq_iff
#print axioms nativeF55RawVerticalFourToPath
#print axioms nativeF55RawVerticalFourToShadow
#print axioms nativeF55RawVerticalFourToPath_spec
#print axioms nativeF55RawVerticalFourToShadow_spec
#print axioms northHexagonNativeSquare_rawDistinct_but_fourRelated

end
end Kuu.F112.Physical
