import Kuu.F112.PolygonNativeC60FiniteStrictBoundaryTransport

/-!
# F112-P94D3BB — typed horizontal candidates and the exact Peiffer obstruction

BA supplied a surjection from actual dependent AX comparison syntax onto each
strict Kuu hom-set. BB uses those representatives to study HORIZONTAL
composition across adjacent dimensions, not another vertical composition law.

A horizontal operation on the actual C60-dependent cells must supply typed
left and right whiskerings. We do not fabricate such an operation from the
existence of finite strict categories. Given candidate whiskerings, we prove:
* their two possible horizontal pastings have genuine dependent boundaries;
* separate congruence is sufficient to descend both pastings to strict homs;
* strict interchange is EQUIVALENT to their exact selected-replacement Peiffer
  equality, not to equality of their numerical shadows;
* a distinguishing noncommutative strict holonomy obstructs interchange;
* compatibility with the NEXT declared signature is an additional obligation.

These are conditional cross-level theorems; they do not construct original
C60 geometric 16-cells, assert global strict 3/n-categories, or introduce Gray.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Actual dependent horizontal candidates. Neither field is inferred from a
stagewise strict category. All four corners and each intermediate boundary are
indexed by the original proof-relevant C60 layer. -/
structure NativeC60BBWhiskering {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) where
  obj : L.Total → L.Total → L.Total
  left : ∀ (a : L.Total) {x y : L.Total},
    NativeC60AXStep S x y → NativeC60AXStep S (obj a x) (obj a y)
  right : ∀ {x y : L.Total},
    NativeC60AXStep S x y → ∀ (a : L.Total),
      NativeC60AXStep S (obj x a) (obj y a)

/-- First whisker the left comparison on the right, then the right comparison
on the left. The intermediate object is exactly H.obj b c. -/
def nativeC60BBHorizontalRL {L : NativeC60AXLayer.{u}}
    {S : NativeC60AXSignature L} (H : NativeC60BBWhiskering S)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d) :
    NativeC60AXStep S (H.obj a c) (H.obj b d) :=
  .trans (H.right f c) (H.left b g)

/-- The other genuine typed square, with intermediate object H.obj a d. -/
def nativeC60BBHorizontalLR {L : NativeC60AXLayer.{u}}
    {S : NativeC60AXSignature L} (H : NativeC60BBWhiskering S)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d) :
    NativeC60AXStep S (H.obj a c) (H.obj b d) :=
  .trans (H.left a g) (H.right f d)

/-- The two pastings really have the same original lower boundary. -/
theorem nativeC60BBHorizontal_boundary {L : NativeC60AXLayer.{u}}
    {S : NativeC60AXSignature L} (H : NativeC60BBWhiskering S)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d) :
    (H.obj a c).1 = (H.obj b d).1 :=
  (nativeC60BBHorizontalRL H f g).boundary

/-- The two *different* compatibility obligations on whiskering. This is an
explicit hypothesis, not a consequence of vertical strictification. -/
structure NativeC60BBWhiskeringCongruent {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S) : Prop where
  left : ∀ (a : L.Total) {x y : L.Total}
    (f g : NativeC60AXStep S x y),
    nativeC60AZStrictStep S R f = nativeC60AZStrictStep S R g →
      nativeC60AZStrictStep S R (H.left a f) =
        nativeC60AZStrictStep S R (H.left a g)
  right : ∀ {x y : L.Total} (f g : NativeC60AXStep S x y)
    (a : L.Total),
    nativeC60AZStrictStep S R f = nativeC60AZStrictStep S R g →
      nativeC60AZStrictStep S R (H.right f a) =
        nativeC60AZStrictStep S R (H.right g a)

/-- Congruence of the first square, with *both* independent comparison
representatives varying. No identification of raw higher cells is made. -/
theorem nativeC60BBHorizontalRL_congr {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f f' : NativeC60AXStep S a b) (g g' : NativeC60AXStep S c d)
    (hf : nativeC60AZStrictStep S R f = nativeC60AZStrictStep S R f')
    (hg : nativeC60AZStrictStep S R g = nativeC60AZStrictStep S R g') :
    nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f g) =
      nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f' g') := by
  calc
    _ = nativeC60AZStrictStep S R (H.right f c) ≫
          nativeC60AZStrictStep S R (H.left b g) :=
      nativeC60AZStrictStep_comp S R _ _
    _ = nativeC60AZStrictStep S R (H.right f' c) ≫
          nativeC60AZStrictStep S R (H.left b g') := by
      rw [hc.right f f' c hf, hc.left b g g' hg]
    _ = _ := (nativeC60AZStrictStep_comp S R _ _).symm

theorem nativeC60BBHorizontalLR_congr {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f f' : NativeC60AXStep S a b) (g g' : NativeC60AXStep S c d)
    (hf : nativeC60AZStrictStep S R f = nativeC60AZStrictStep S R f')
    (hg : nativeC60AZStrictStep S R g = nativeC60AZStrictStep S R g') :
    nativeC60AZStrictStep S R (nativeC60BBHorizontalLR H f g) =
      nativeC60AZStrictStep S R (nativeC60BBHorizontalLR H f' g') := by
  calc
    _ = nativeC60AZStrictStep S R (H.left a g) ≫
          nativeC60AZStrictStep S R (H.right f d) :=
      nativeC60AZStrictStep_comp S R _ _
    _ = nativeC60AZStrictStep S R (H.left a g') ≫
          nativeC60AZStrictStep S R (H.right f' d) := by
      rw [hc.left a g g' hg, hc.right f f' d hf]
    _ = _ := (nativeC60AZStrictStep_comp S R _ _).symm

/-- Strict horizontal operation assembled using BA's proved representative
surjectivity. Its value is independent of representatives by hc. -/
def nativeC60BBStrictHorizontalRL {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (_hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f : (nativeC60AZStrictProject S R).obj ⟨a⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨b⟩)
    (g : (nativeC60AZStrictProject S R).obj ⟨c⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨d⟩) :
    (nativeC60AZStrictProject S R).obj ⟨H.obj a c⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨H.obj b d⟩ :=
  nativeC60AZStrictStep S R
    (nativeC60BBHorizontalRL H
      (Classical.choose (nativeC60BAStep_surjective S R a b f))
      (Classical.choose (nativeC60BAStep_surjective S R c d g)))

def nativeC60BBStrictHorizontalLR {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (_hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f : (nativeC60AZStrictProject S R).obj ⟨a⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨b⟩)
    (g : (nativeC60AZStrictProject S R).obj ⟨c⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨d⟩) :
    (nativeC60AZStrictProject S R).obj ⟨H.obj a c⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨H.obj b d⟩ :=
  nativeC60AZStrictStep S R
    (nativeC60BBHorizontalLR H
      (Classical.choose (nativeC60BAStep_surjective S R a b f))
      (Classical.choose (nativeC60BAStep_surjective S R c d g)))

theorem nativeC60BBStrictHorizontalRL_raw {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d) :
    nativeC60BBStrictHorizontalRL S R H hc
      (nativeC60AZStrictStep S R f) (nativeC60AZStrictStep S R g) =
        nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f g) := by
  unfold nativeC60BBStrictHorizontalRL
  refine nativeC60BBHorizontalRL_congr S R H hc _ f _ g ?_ ?_
  · exact Classical.choose_spec (nativeC60BAStep_surjective S R a b
      (nativeC60AZStrictStep S R f))
  · exact Classical.choose_spec (nativeC60BAStep_surjective S R c d
      (nativeC60AZStrictStep S R g))

theorem nativeC60BBStrictHorizontalLR_raw {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d) :
    nativeC60BBStrictHorizontalLR S R H hc
      (nativeC60AZStrictStep S R f) (nativeC60AZStrictStep S R g) =
        nativeC60AZStrictStep S R (nativeC60BBHorizontalLR H f g) := by
  unfold nativeC60BBStrictHorizontalLR
  refine nativeC60BBHorizontalLR_congr S R H hc _ f _ g ?_ ?_
  · exact Classical.choose_spec (nativeC60BAStep_surjective S R a b
      (nativeC60AZStrictStep S R f))
  · exact Classical.choose_spec (nativeC60BAStep_surjective S R c d
      (nativeC60AZStrictStep S R g))

/-- The precise still-unproved middle-four obstruction, formulated inside
Kuu's selected strict replacement quotient rather than in an observer kernel. -/
def NativeC60BBPeifferSound {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S) : Prop :=
  ∀ {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d),
    nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f g) =
      nativeC60AZStrictStep S R (nativeC60BBHorizontalLR H f g)

/-- Strict Peiffer equality is EXACTLY membership in Kuu's compositional
replacement closure. Equality of Peiffer numerical evaluations is weaker. -/
theorem nativeC60BBPeiffer_iff_replaceable {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S) :
    NativeC60BBPeifferSound S R H ↔
      ∀ {a b c d : L.Total}
        (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d),
        Kuu.Replaceable (nativeC60AZStrictRelations S R)
          (nativeC60AZRawArrow S (nativeC60BBHorizontalRL H f g))
          (nativeC60AZRawArrow S (nativeC60BBHorizontalLR H f g)) := by
  constructor
  · intro hp a b c d f g
    exact (nativeC60AZStrictStep_exact S R _ _).mp (hp f g)
  · intro hp a b c d f g
    exact (nativeC60AZStrictStep_exact S R _ _).mpr (hp f g)

/-- An actual all-hom-set strict interchange holds if and only if the
raw typed Peiffer square becomes a selected Kuu replacement. -/
theorem nativeC60BBStrictInterchange_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H) :
    (∀ {a b c d : L.Total}
      (f : (nativeC60AZStrictProject S R).obj ⟨a⟩ ⟶
        (nativeC60AZStrictProject S R).obj ⟨b⟩)
      (g : (nativeC60AZStrictProject S R).obj ⟨c⟩ ⟶
        (nativeC60AZStrictProject S R).obj ⟨d⟩),
      nativeC60BBStrictHorizontalRL S R H hc f g =
        nativeC60BBStrictHorizontalLR S R H hc f g) ↔
      NativeC60BBPeifferSound S R H := by
  constructor
  · intro hi a b c d f g
    simpa only [nativeC60BBStrictHorizontalRL_raw,
      nativeC60BBStrictHorizontalLR_raw] using
        (hi (nativeC60AZStrictStep S R f) (nativeC60AZStrictStep S R g))
  · intro hp a b c d f g
    unfold nativeC60BBStrictHorizontalRL nativeC60BBStrictHorizontalLR
    exact hp _ _

/-- Separate functoriality of both whiskering directions. Even when the two
directions descend, these unit/composition laws do NOT hold automatically. -/
structure NativeC60BBWhiskeringFunctorial {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S) : Prop where
  left_refl : ∀ (a x : L.Total),
    nativeC60AZStrictStep S R (H.left a (.refl x)) =
      𝟙 ((nativeC60AZStrictProject S R).obj ⟨H.obj a x⟩)
  right_refl : ∀ (x a : L.Total),
    nativeC60AZStrictStep S R (H.right (.refl x) a) =
      𝟙 ((nativeC60AZStrictProject S R).obj ⟨H.obj x a⟩)
  left_trans : ∀ (a : L.Total) {x y z : L.Total}
    (f : NativeC60AXStep S x y) (g : NativeC60AXStep S y z),
    nativeC60AZStrictStep S R (H.left a (.trans f g)) =
      nativeC60AZStrictStep S R (H.left a f) ≫
        nativeC60AZStrictStep S R (H.left a g)
  right_trans : ∀ {x y z : L.Total}
    (f : NativeC60AXStep S x y) (g : NativeC60AXStep S y z)
    (a : L.Total),
    nativeC60AZStrictStep S R (H.right (.trans f g) a) =
      nativeC60AZStrictStep S R (H.right f a) ≫
        nativeC60AZStrictStep S R (H.right g a)

/-- Proper middle-four: interchange of horizontal with vertical composites.
The proof genuinely uses both whiskering functorialities AND the Peiffer square.
It does not promote unproved raw equality to strict equality. -/
theorem nativeC60BBHorizontal_middleFour {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hf : NativeC60BBWhiskeringFunctorial S R H)
    (hp : NativeC60BBPeifferSound S R H)
    {a b e c d k : L.Total}
    (f : NativeC60AXStep S a b) (f' : NativeC60AXStep S b e)
    (g : NativeC60AXStep S c d) (g' : NativeC60AXStep S d k) :
    nativeC60AZStrictStep S R
        (nativeC60BBHorizontalRL H (.trans f f') (.trans g g')) =
      nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f g) ≫
        nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f' g') := by
  have hpe :
      nativeC60AZStrictStep S R (H.right f' c) ≫
          nativeC60AZStrictStep S R (H.left e g) =
        nativeC60AZStrictStep S R (H.left b g) ≫
          nativeC60AZStrictStep S R (H.right f' d) := by
    simpa only [nativeC60BBHorizontalRL, nativeC60BBHorizontalLR,
      nativeC60AZStrictStep_comp] using hp f' g
  calc
    nativeC60AZStrictStep S R
        (nativeC60BBHorizontalRL H (.trans f f') (.trans g g')) =
      (nativeC60AZStrictStep S R (H.right f c) ≫
        nativeC60AZStrictStep S R (H.right f' c)) ≫
      (nativeC60AZStrictStep S R (H.left e g) ≫
        nativeC60AZStrictStep S R (H.left e g')) := by
          rw [nativeC60AZStrictStep_comp, hf.right_trans f f' c,
            hf.left_trans e g g']
    _ = nativeC60AZStrictStep S R (H.right f c) ≫
        ((nativeC60AZStrictStep S R (H.right f' c) ≫
            nativeC60AZStrictStep S R (H.left e g)) ≫
          nativeC60AZStrictStep S R (H.left e g')) := by
          simp only [Category.assoc]
    _ = nativeC60AZStrictStep S R (H.right f c) ≫
        ((nativeC60AZStrictStep S R (H.left b g) ≫
            nativeC60AZStrictStep S R (H.right f' d)) ≫
          nativeC60AZStrictStep S R (H.left e g')) := by
          rw [hpe]
    _ = (nativeC60AZStrictStep S R (H.right f c) ≫
            nativeC60AZStrictStep S R (H.left b g)) ≫
          (nativeC60AZStrictStep S R (H.right f' d) ≫
            nativeC60AZStrictStep S R (H.left e g')) := by
          simp only [Category.assoc]
    _ = nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f g) ≫
          nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f' g') := by
          simp only [nativeC60BBHorizontalRL, nativeC60AZStrictStep_comp]

/-- The horizontal strict arrow preserves the pair of identities when
both actual whiskerings preserve identities. -/
theorem nativeC60BBStrictHorizontal_id {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    (hf : NativeC60BBWhiskeringFunctorial S R H)
    (a c : L.Total) :
    nativeC60BBStrictHorizontalRL S R H hc
        (𝟙 ((nativeC60AZStrictProject S R).obj ⟨a⟩))
        (𝟙 ((nativeC60AZStrictProject S R).obj ⟨c⟩)) =
      𝟙 ((nativeC60AZStrictProject S R).obj ⟨H.obj a c⟩) := by
  have hu :
      nativeC60AZStrictStep S R
        (nativeC60BBHorizontalRL H (.refl a) (.refl c)) =
        𝟙 ((nativeC60AZStrictProject S R).obj ⟨H.obj a c⟩) := by
    change nativeC60AZStrictStep S R
      (.trans (H.right (.refl a) c) (H.left a (.refl c))) = _
    rw [nativeC60AZStrictStep_comp, hf.right_refl, hf.left_refl, Category.id_comp]
  calc
    nativeC60BBStrictHorizontalRL S R H hc
        (𝟙 ((nativeC60AZStrictProject S R).obj ⟨a⟩))
        (𝟙 ((nativeC60AZStrictProject S R).obj ⟨c⟩)) =
      nativeC60BBStrictHorizontalRL S R H hc
        (nativeC60AZStrictStep S R (.refl a))
        (nativeC60AZStrictStep S R (.refl c)) := by
          rw [nativeC60AZStrictStep_refl, nativeC60AZStrictStep_refl]
    _ = nativeC60AZStrictStep S R
        (nativeC60BBHorizontalRL H (.refl a) (.refl c)) :=
          nativeC60BBStrictHorizontalRL_raw S R H hc _ _
    _ = _ := hu

/-- Genuine all-hom-set middle-four interchange, not merely equality of
the two uncomposed Peiffer paths. BA representatives remove arbitrary
choices; the interchange equation is proved after strict realization. -/
theorem nativeC60BBStrictHorizontal_comp {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S R H)
    (hf : NativeC60BBWhiskeringFunctorial S R H)
    (hp : NativeC60BBPeifferSound S R H)
    {a b e c d k : L.Total}
    (f : (nativeC60AZStrictProject S R).obj ⟨a⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨b⟩)
    (f' : (nativeC60AZStrictProject S R).obj ⟨b⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨e⟩)
    (g : (nativeC60AZStrictProject S R).obj ⟨c⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨d⟩)
    (g' : (nativeC60AZStrictProject S R).obj ⟨d⟩ ⟶
      (nativeC60AZStrictProject S R).obj ⟨k⟩) :
    nativeC60BBStrictHorizontalRL S R H hc (f ≫ f') (g ≫ g') =
      nativeC60BBStrictHorizontalRL S R H hc f g ≫
        nativeC60BBStrictHorizontalRL S R H hc f' g' := by
  obtain ⟨f₀, rfl⟩ := nativeC60BAStep_surjective S R a b f
  obtain ⟨f₁, rfl⟩ := nativeC60BAStep_surjective S R b e f'
  obtain ⟨g₀, rfl⟩ := nativeC60BAStep_surjective S R c d g
  obtain ⟨g₁, rfl⟩ := nativeC60BAStep_surjective S R d k g'
  calc
    nativeC60BBStrictHorizontalRL S R H hc
        (nativeC60AZStrictStep S R f₀ ≫ nativeC60AZStrictStep S R f₁)
        (nativeC60AZStrictStep S R g₀ ≫ nativeC60AZStrictStep S R g₁) =
      nativeC60BBStrictHorizontalRL S R H hc
        (nativeC60AZStrictStep S R (.trans f₀ f₁))
        (nativeC60AZStrictStep S R (.trans g₀ g₁)) := by
          rw [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_comp]
    _ = nativeC60AZStrictStep S R
        (nativeC60BBHorizontalRL H (.trans f₀ f₁) (.trans g₀ g₁)) :=
          nativeC60BBStrictHorizontalRL_raw S R H hc _ _
    _ = nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f₀ g₀) ≫
          nativeC60AZStrictStep S R (nativeC60BBHorizontalRL H f₁ g₁) :=
          nativeC60BBHorizontal_middleFour S R H hf hp f₀ f₁ g₀ g₁
    _ = nativeC60BBStrictHorizontalRL S R H hc
          (nativeC60AZStrictStep S R f₀) (nativeC60AZStrictStep S R g₀) ≫
        nativeC60BBStrictHorizontalRL S R H hc
          (nativeC60AZStrictStep S R f₁) (nativeC60AZStrictStep S R g₁) := by
          rw [nativeC60BBStrictHorizontalRL_raw, nativeC60BBStrictHorizontalRL_raw]

/-- A noncommutative receiver can witness failure, but it never DEFINES
the strict quotient or its selected replacement relation. -/
theorem nativeC60BBPeiffer_holonomy_obstruction
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (R : NativeC60AZParallelRelation S)
    (H : NativeC60BBWhiskering S)
    {G : Type v} [Group G]
    (weight : ∀ {x y}, S.Gen x y → G)
    (hw : NativeC60AZWeightsRespect S R weight)
    {a b c d : L.Total}
    (f : NativeC60AXStep S a b) (g : NativeC60AXStep S c d)
    (hne : nativeC60AZHolonomy S weight (nativeC60BBHorizontalRL H f g) ≠
      nativeC60AZHolonomy S weight (nativeC60BBHorizontalLR H f g)) :
    ¬ NativeC60BBPeifferSound S R H := by
  intro hp
  have heq := hp f g
  have hm := congrArg
    (fun k : (nativeC60AZStrictProject S R).obj ⟨H.obj a c⟩ ⟶
        (nativeC60AZStrictProject S R).obj ⟨H.obj b d⟩ =>
      (nativeC60AZStrictHolonomy S R weight hw).map k) heq
  simp only [nativeC60AZStrictHolonomy_arrow] at hm
  exact hne (congrArg MulOpposite.unop hm)

/-- Relates congruence of the constructed lower strict quotient to an
ACTUAL generator of the independently specified upper AX signature. -/
theorem nativeC60BBUpperGenerator_left {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S (nativeC60AZHigherRelations S T) H)
    {x y : L.Total} (f g : NativeC60AXStep S x y)
    (e : T.Gen ⟨(x, y), f⟩ ⟨(x, y), g⟩) (a : L.Total) :
    nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) (H.left a f) =
      nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) (H.left a g) :=
  hc.left a f g (nativeC60AZStrictStep_declared S
    (nativeC60AZHigherRelations S T) ⟨e⟩)

theorem nativeC60BBUpperGenerator_right {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L)
    (T : NativeC60AXSignature (nativeC60AXNext L S))
    (H : NativeC60BBWhiskering S)
    (hc : NativeC60BBWhiskeringCongruent S (nativeC60AZHigherRelations S T) H)
    {x y : L.Total} (f g : NativeC60AXStep S x y)
    (e : T.Gen ⟨(x, y), f⟩ ⟨(x, y), g⟩) (a : L.Total) :
    nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) (H.right f a) =
      nativeC60AZStrictStep S (nativeC60AZHigherRelations S T) (H.right g a) :=
  hc.right f g a (nativeC60AZStrictStep_declared S
    (nativeC60AZHigherRelations S T) ⟨e⟩)

section PhysicalC60

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

/-- Genuine original C60 data and its AS nonabelian Peiffer receiver.
The inequality is an explicit remaining physical obligation, NOT guessed
from the nontriviality of one group element. -/
theorem nativeK5BBPhysicalPeiffer_obstruction
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5AXKuuSignature W))
    {a b c d : (nativeK5AXBaseLayer W).Total}
    (f : NativeC60AXStep (nativeK5AXKuuSignature W) a b)
    (g : NativeC60AXStep (nativeK5AXKuuSignature W) c d)
    (hne :
      nativeC60AZHolonomy (nativeK5AXKuuSignature W)
        (nativeC60AZConstantWeight (nativeK5AXKuuSignature W)
          (nativeK5ASPhysicalDefect W [])) (nativeC60BBHorizontalRL Hh f g) ≠
      nativeC60AZHolonomy (nativeK5AXKuuSignature W)
        (nativeC60AZConstantWeight (nativeK5AXKuuSignature W)
          (nativeK5ASPhysicalDefect W [])) (nativeC60BBHorizontalLR Hh f g)) :
    ¬ NativeC60BBPeifferSound (nativeK5AXKuuSignature W)
        (nativeC60AZNoRelations (nativeK5AXKuuSignature W)) Hh := by
  exact nativeC60BBPeiffer_holonomy_obstruction
    (nativeK5AXKuuSignature W)
    (nativeC60AZNoRelations (nativeK5AXKuuSignature W)) Hh
    (nativeC60AZConstantWeight (nativeK5AXKuuSignature W)
      (nativeK5ASPhysicalDefect W []))
    (by intro x y f g h; exact h.elim) f g hne

end PhysicalC60

#print axioms NativeC60BBWhiskering
#print axioms nativeC60BBHorizontalRL
#print axioms nativeC60BBHorizontalLR
#print axioms nativeC60BBHorizontal_boundary
#print axioms NativeC60BBWhiskeringCongruent
#print axioms nativeC60BBHorizontalRL_congr
#print axioms nativeC60BBHorizontalLR_congr
#print axioms nativeC60BBStrictHorizontalRL
#print axioms nativeC60BBStrictHorizontalLR
#print axioms nativeC60BBStrictHorizontalRL_raw
#print axioms nativeC60BBStrictHorizontalLR_raw
#print axioms NativeC60BBPeifferSound
#print axioms nativeC60BBPeiffer_iff_replaceable
#print axioms nativeC60BBStrictInterchange_iff
#print axioms NativeC60BBWhiskeringFunctorial
#print axioms nativeC60BBHorizontal_middleFour
#print axioms nativeC60BBStrictHorizontal_id
#print axioms nativeC60BBStrictHorizontal_comp
#print axioms nativeC60BBPeiffer_holonomy_obstruction
#print axioms nativeC60BBUpperGenerator_left
#print axioms nativeC60BBUpperGenerator_right
#print axioms nativeK5BBPhysicalPeiffer_obstruction

end
end Kuu.F112.Physical
