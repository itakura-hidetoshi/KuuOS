import KUOS.DependentOriginationPointwiseInverseNaturalityV4_81

namespace KUOS.DependentOriginationPointwiseInverseCoherenceV4_82

open CategoryTheory
open CategoryTheory.Functor
open KUOS.DependentOriginationPointwiseInverseNaturalityV4_81
open scoped CategoryTheory.Pseudofunctor.StrongTrans

set_option autoImplicit false

noncomputable section

/-!
# Coherent inverse strong transformations from pointwise equivalences v4.82

The input is exactly v4.81's Cat-valued strong transformation and pointwise
IsEquivalence proofs. The inverse naturality squares constructed there satisfy
all three StrongTrans coherence laws: base two-cell naturality, identity and
composition. None of those laws is an additional assumption.

The common proof is to precompose by the fully faithful comparison component,
then cancel the invertible composite of the chosen unit and mapped comparison
square. The unit equation identifies the remaining paths. For composition we
also use ordinary naturality of the inverse square along the original square.

The resulting inverse has literally the v4.81 components and naturality
isomorphisms. The chosen units assemble into an invertible modification
`identity ~= c >> inverse`; its inverse is the coherent retraction needed by
v4.80. This is a general Cat-valued theorem, not yet the KuuOS-sector
instantiation or the final mapping biequivalence.
-/

universe uB vB wB uH vH

variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {R S : Pseudofunctor B Cat.{vH, uH}}
variable (c : R ⟶ S)
variable (hc : ∀ U : B, (c.app U).toFunctor.IsEquivalence)

local notation "D" => pointwiseInverseComponent c hc
local notation "E" => pointwiseInverseUnitIso c hc
local notation "N" => pointwiseInverseNaturalityIso c hc

/-- The unit comparison equation with the inverse unit cancelled explicitly. -/
theorem pointwiseInverseNaturality_unit_app {U V : B} (p : U ⟶ V) (x : R.obj U) :
    (E V).hom.app ((R.map p).toFunctor.obj x) ≫
        (D V).map ((c.naturality p).hom.toNatTrans.app x) ≫
          (N p).hom.app ((c.app U).toFunctor.obj x) =
      (R.map p).toFunctor.map ((E U).hom.app x) := by
  exact (congrArg
    (fun m :
      (D V).obj ((c.app V).toFunctor.obj ((R.map p).toFunctor.obj x)) ⟶
        (R.map p).toFunctor.obj ((D U).obj ((c.app U).toFunctor.obj x)) =>
      (E V).hom.app ((R.map p).toFunctor.obj x) ≫ m)
    (pointwiseInverseNaturalityIso_unitCompatible c hc p x)).trans
      ((E V).hom_inv_id_app_assoc _ _)

/-- Homogeneous equality composition avoids asking the Trans typeclass to
unfold the chosen equivalence while reassociating evaluated Cat components. -/
private theorem postcomposeTriple {C : Type*} [Category C]
    {a b e f g : C} (u : a ⟶ b) (v : b ⟶ e) (n : e ⟶ f)
    (m : a ⟶ f) (h : u ≫ v ≫ n = m) (t : f ⟶ g) :
    (u ≫ v) ≫ n ≫ t = m ≫ t :=
  (Category.assoc (u ≫ v) n t).symm.trans
    ((congrArg (fun z => z ≫ t) (Category.assoc u v n)).trans
      (congrArg (fun z => z ≫ t) h))

/-! Homogeneous diagram algebra is proved once with abstract category objects.
The concrete applications below pass already established equations to these
lemmas; no simplifier must discover a functor or a category through `D`/`E`. -/

private theorem postcomposePair {C₀ : Type*} [Category C₀]
    {a b b' e f : C₀} (u : a ⟶ b) (v : b ⟶ e)
    (u' : a ⟶ b') (v' : b' ⟶ e) (h : u ≫ v = u' ≫ v') (t : e ⟶ f) :
    u ≫ v ≫ t = u' ≫ v' ≫ t :=
  (Category.assoc u v t).symm.trans
    ((congrArg (fun z => z ≫ t) h).trans (Category.assoc u' v' t))

private theorem postcomposeTripleNormalized {C₀ : Type*} [Category C₀]
    {a b e f g : C₀} (u : a ⟶ b) (v : b ⟶ e) (n : e ⟶ f)
    (m : a ⟶ f) (h : u ≫ v ≫ n = m) (t : f ⟶ g) :
    u ≫ v ≫ n ≫ t = m ≫ t :=
  (Category.assoc u v (n ≫ t)).symm.trans (postcomposeTriple u v n m h t)

private theorem mapPairCongr {C₀ C₁ : Type*} [Category C₀] [Category C₁]
    (F : C₀ ⥤ C₁) {a b b' e : C₀}
    (u : a ⟶ b) (v : b ⟶ e) (u' : a ⟶ b') (v' : b' ⟶ e)
    (h : u ≫ v = u' ≫ v') {l r : C₁} (pre : l ⟶ F.obj a) (post : F.obj e ⟶ r) :
    (pre ≫ F.map u) ≫ F.map v ≫ post =
      pre ≫ F.map u' ≫ F.map v' ≫ post := by
  simpa only [Functor.map_comp, Category.assoc] using
    congrArg (fun m : a ⟶ e => pre ≫ F.map m ≫ post) h

private theorem mapToPair {C₀ C₁ : Type*} [Category C₀] [Category C₁]
    (F : C₀ ⥤ C₁) {a b e : C₀} (u : a ⟶ b) (v : b ⟶ e)
    (m : a ⟶ e) (h : u ≫ v = m) {l : C₁} (pre : l ⟶ F.obj a) :
    pre ≫ F.map m = (pre ≫ F.map u) ≫ F.map v :=
  (congrArg (fun z => pre ≫ F.map z) h.symm).trans
    ((congrArg (fun z => pre ≫ z) (F.map_comp u v)).trans
      (Category.assoc pre (F.map u) (F.map v)).symm)

private theorem mapPairTripleCongr {C₀ C₁ : Type*} [Category C₀] [Category C₁]
    (F : C₀ ⥤ C₁) {a b e d f : C₀}
    (u : a ⟶ b) (v : b ⟶ f) (u' : a ⟶ e) (v' : e ⟶ d) (w' : d ⟶ f)
    (h : u ≫ v = u' ≫ v' ≫ w') {l r : C₁}
    (pre : l ⟶ F.obj a) (post : F.obj f ⟶ r) :
    (pre ≫ F.map u) ≫ F.map v ≫ post =
      pre ≫ F.map u' ≫ F.map v' ≫ F.map w' ≫ post := by
  simpa only [Functor.map_comp, Category.assoc] using
    congrArg (fun m : a ⟶ f => pre ≫ F.map m ≫ post) h

private theorem mapTripleEq {C₀ C₁ : Type*} [Category C₀] [Category C₁]
    (F : C₀ ⥤ C₁) {a b e f : C₀} (u : a ⟶ b) (v : b ⟶ e) (n : e ⟶ f)
    (m : a ⟶ f) (h : u ≫ v ≫ n = m) :
    F.map u ≫ F.map v ≫ F.map n = F.map m :=
  (congrArg (fun z => F.map u ≫ z) (F.map_comp v n).symm).trans
    ((F.map_comp u (v ≫ n)).symm.trans (congrArg (fun z : a ⟶ f => F.map z) h))

/-- Naturality with respect to arbitrary base two-cells, not only isomorphisms. -/
theorem pointwiseInverseNaturality_twoCell {U V : B} {p q : U ⟶ V} (alpha : p ⟶ q) :
    whiskerRight (S.map₂ alpha).toNatTrans (D V) ≫ (N q).hom =
      (N p).hom ≫ whiskerLeft (D U) (R.map₂ alpha).toNatTrans := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  apply ((whiskeringLeft (R.obj U) (S.obj U) (R.obj V)).obj
    (c.app U).toFunctor).map_injective
  apply NatTrans.ext
  funext x
  let rp := (R.map p).toFunctor
  let rq := (R.map q).toFunctor
  let a := (c.naturality p).hom.toNatTrans.app x
  let b := (c.naturality q).hom.toNatTrans.app x
  let t := (R.map₂ alpha).toNatTrans.app x
  let s := (S.map₂ alpha).toNatTrans.app ((c.app U).toFunctor.obj x)
  let z := (c.app U).toFunctor.obj x
  let k := (E V).app (rp.obj x) ≪≫
    (D V).mapIso ((Cat.Hom.toNatIso (c.naturality p)).app x)
  change (D V).map s ≫ (N q).hom.app z =
    (N p).hom.app z ≫ (R.map₂ alpha).toNatTrans.app ((D U).obj z)
  apply (Iso.cancel_iso_hom_left k _ _).1
  have hbase : (c.app V).toFunctor.map t ≫ b = a ≫ s :=
    congrArg (fun m : (R.map p ≫ c.app V) ⟶ (c.app U ≫ S.map q) =>
      m.toNatTrans.app x) (c.naturality_naturality alpha)
  have hunit : t ≫ (E V).hom.app (rq.obj x) =
      (E V).hom.app (rp.obj x) ≫ (D V).map ((c.app V).toFunctor.map t) :=
    (E V).hom.naturality t
  have h1 : k.hom ≫ (D V).map s ≫ (N q).hom.app z =
      (E V).hom.app (rp.obj x) ≫ (D V).map ((c.app V).toFunctor.map t) ≫
        (D V).map b ≫ (N q).hom.app z :=
    mapPairCongr (D V) a s ((c.app V).toFunctor.map t) b hbase.symm
      ((E V).hom.app (rp.obj x)) ((N q).hom.app z)
  have h2 : (E V).hom.app (rp.obj x) ≫ (D V).map ((c.app V).toFunctor.map t) ≫
      (D V).map b ≫ (N q).hom.app z =
        t ≫ (E V).hom.app (rq.obj x) ≫ (D V).map b ≫ (N q).hom.app z :=
    postcomposePair _ _ _ _ hunit.symm ((D V).map b ≫ (N q).hom.app z)
  have h3 : t ≫ (E V).hom.app (rq.obj x) ≫ (D V).map b ≫ (N q).hom.app z =
      t ≫ rq.map ((E U).hom.app x) :=
    congrArg (fun m => t ≫ m) (pointwiseInverseNaturality_unit_app c hc q x)
  have h4 : t ≫ rq.map ((E U).hom.app x) =
      rp.map ((E U).hom.app x) ≫ (R.map₂ alpha).toNatTrans.app ((D U).obj z) :=
    ((R.map₂ alpha).toNatTrans.naturality ((E U).hom.app x)).symm
  have h5 : k.hom ≫ (N p).hom.app z ≫ (R.map₂ alpha).toNatTrans.app ((D U).obj z) =
      rp.map ((E U).hom.app x) ≫ (R.map₂ alpha).toNatTrans.app ((D U).obj z) :=
    postcomposeTriple _ _ _ _ (pointwiseInverseNaturality_unit_app c hc p x) _
  exact h1.trans (h2.trans (h3.trans (h4.trans h5.symm)))

/-- Compatibility with base identities, as an ordinary natural-transformation equation. -/
theorem pointwiseInverseNaturality_id (U : B) :
    (N (𝟙 U)).hom ≫ whiskerLeft (D U) (R.mapId U).hom.toNatTrans =
      whiskerRight (S.mapId U).hom.toNatTrans (D U) := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  apply ((whiskeringLeft (R.obj U) (S.obj U) (R.obj U)).obj
    (c.app U).toFunctor).map_injective
  apply NatTrans.ext
  funext x
  let r := (R.map (𝟙 U)).toFunctor
  let a := (c.naturality (𝟙 U)).hom.toNatTrans.app x
  let z := (c.app U).toFunctor.obj x
  let t := (R.mapId U).hom.toNatTrans.app x
  let s := (S.mapId U).hom.toNatTrans.app z
  let k := (E U).app (r.obj x) ≪≫
    (D U).mapIso ((Cat.Hom.toNatIso (c.naturality (𝟙 U))).app x)
  change (N (𝟙 U)).hom.app z ≫ (R.mapId U).hom.toNatTrans.app ((D U).obj z) =
    (D U).map s
  apply (Iso.cancel_iso_hom_left k _ _).1
  have hbase : a ≫ s = (c.app U).toFunctor.map t := by
    have h := congrArg
      (fun m : (R.map (𝟙 U) ≫ c.app U) ⟶ (c.app U ≫ 𝟙 (S.obj U)) =>
        m.toNatTrans.app x) (c.naturality_id U)
    change a ≫ s = (c.app U).toFunctor.map t ≫ 𝟙 _ ≫ 𝟙 _ at h
    simpa only [Category.comp_id] using h
  have h1 : k.hom ≫ (N (𝟙 U)).hom.app z ≫
      (R.mapId U).hom.toNatTrans.app ((D U).obj z) =
        r.map ((E U).hom.app x) ≫ (R.mapId U).hom.toNatTrans.app ((D U).obj z) :=
    postcomposeTriple _ _ _ _ (pointwiseInverseNaturality_unit_app c hc (𝟙 U) x) _
  have h2 : r.map ((E U).hom.app x) ≫ (R.mapId U).hom.toNatTrans.app ((D U).obj z) =
      t ≫ (E U).hom.app x :=
    (R.mapId U).hom.toNatTrans.naturality ((E U).hom.app x)
  have h3 : t ≫ (E U).hom.app x =
      (E U).hom.app (r.obj x) ≫ (D U).map ((c.app U).toFunctor.map t) :=
    (E U).hom.naturality t
  have h4 : (E U).hom.app (r.obj x) ≫ (D U).map ((c.app U).toFunctor.map t) =
      k.hom ≫ (D U).map s :=
    mapToPair (D U) a s ((c.app U).toFunctor.map t) hbase ((E U).hom.app (r.obj x))
  exact h1.trans (h2.trans (h3.trans h4))

/-- Compatibility with base composition. Functor associativity is used only
inside this ordinary functor category; the native StrongTrans below retains
all bicategorical structural cells in its actual field type. -/
theorem pointwiseInverseNaturality_comp {U V T : B} (p : U ⟶ V) (q : V ⟶ T) :
    (N (p ≫ q)).hom ≫ whiskerLeft (D U) (R.mapComp p q).hom.toNatTrans =
      whiskerRight (S.mapComp p q).hom.toNatTrans (D T) ≫
        whiskerLeft (S.map p).toFunctor (N q).hom ≫
          whiskerRight (N p).hom (R.map q).toFunctor := by
  letI : (c.app U).toFunctor.IsEquivalence := hc U
  apply ((whiskeringLeft (R.obj U) (S.obj U) (R.obj T)).obj
    (c.app U).toFunctor).map_injective
  apply NatTrans.ext
  funext x
  let rp := (R.map p).toFunctor
  let rq := (R.map q).toFunctor
  let rpq := (R.map (p ≫ q)).toFunctor
  let sp := (S.map p).toFunctor
  let sq := (S.map q).toFunctor
  let a := (c.naturality p).hom.toNatTrans.app x
  let b := (c.naturality q).hom.toNatTrans.app (rp.obj x)
  let ab := (c.naturality (p ≫ q)).hom.toNatTrans.app x
  let z := (c.app U).toFunctor.obj x
  let t := (R.mapComp p q).hom.toNatTrans.app x
  let s := (S.mapComp p q).hom.toNatTrans.app z
  let k := (E T).app (rpq.obj x) ≪≫
    (D T).mapIso ((Cat.Hom.toNatIso (c.naturality (p ≫ q))).app x)
  change (N (p ≫ q)).hom.app z ≫ (R.mapComp p q).hom.toNatTrans.app ((D U).obj z) =
    (D T).map s ≫ (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z)
  apply (Iso.cancel_iso_hom_left k _ _).1
  have hbase : ab ≫ s = (c.app T).toFunctor.map t ≫ b ≫ sq.map a := by
    have h := congrArg
      (fun m : (R.map (p ≫ q) ≫ c.app T) ⟶ (c.app U ≫ (S.map p ≫ S.map q)) =>
        m.toNatTrans.app x) (c.naturality_comp p q)
    change ab ≫ s = (c.app T).toFunctor.map t ≫ 𝟙 _ ≫ b ≫ 𝟙 _ ≫ sq.map a ≫ 𝟙 _ at h
    simpa only [Category.id_comp, Category.comp_id] using h
  have hunit : t ≫ (E T).hom.app (rq.obj (rp.obj x)) =
      (E T).hom.app (rpq.obj x) ≫ (D T).map ((c.app T).toFunctor.map t) :=
    (E T).hom.naturality t
  have hsquare : (D T).map (sq.map a) ≫ (N q).hom.app (sp.obj z) =
      (N q).hom.app ((c.app V).toFunctor.obj (rp.obj x)) ≫ rq.map ((D V).map a) :=
    (N q).hom.naturality a
  have hleft : k.hom ≫ (N (p ≫ q)).hom.app z ≫
      (R.mapComp p q).hom.toNatTrans.app ((D U).obj z) =
        rpq.map ((E U).hom.app x) ≫ (R.mapComp p q).hom.toNatTrans.app ((D U).obj z) :=
    postcomposeTriple _ _ _ _ (pointwiseInverseNaturality_unit_app c hc (p ≫ q) x) _
  have hnat : rpq.map ((E U).hom.app x) ≫
      (R.mapComp p q).hom.toNatTrans.app ((D U).obj z) =
        t ≫ rq.map (rp.map ((E U).hom.app x)) :=
    (R.mapComp p q).hom.toNatTrans.naturality ((E U).hom.app x)
  have h1 : k.hom ≫ (D T).map s ≫ (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z) =
      (E T).hom.app (rpq.obj x) ≫ (D T).map ((c.app T).toFunctor.map t) ≫
        (D T).map b ≫ (D T).map (sq.map a) ≫
          (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z) :=
    mapPairTripleCongr (D T) ab s ((c.app T).toFunctor.map t) b (sq.map a) hbase
      ((E T).hom.app (rpq.obj x)) ((N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z))
  have h2 : (E T).hom.app (rpq.obj x) ≫ (D T).map ((c.app T).toFunctor.map t) ≫
      (D T).map b ≫ (D T).map (sq.map a) ≫
        (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z) =
      t ≫ (E T).hom.app (rq.obj (rp.obj x)) ≫ (D T).map b ≫
        (D T).map (sq.map a) ≫ (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z) :=
    postcomposePair _ _ _ _ hunit.symm
      ((D T).map b ≫ (D T).map (sq.map a) ≫ (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z))
  have h3 : t ≫ (E T).hom.app (rq.obj (rp.obj x)) ≫ (D T).map b ≫
      (D T).map (sq.map a) ≫ (N q).hom.app (sp.obj z) ≫ rq.map ((N p).hom.app z) =
      t ≫ (E T).hom.app (rq.obj (rp.obj x)) ≫ (D T).map b ≫
        (N q).hom.app ((c.app V).toFunctor.obj (rp.obj x)) ≫
          rq.map ((D V).map a) ≫ rq.map ((N p).hom.app z) :=
    congrArg (fun m => t ≫ (E T).hom.app (rq.obj (rp.obj x)) ≫ (D T).map b ≫ m)
      (postcomposePair _ _ _ _ hsquare (rq.map ((N p).hom.app z)))
  have h4 : t ≫ (E T).hom.app (rq.obj (rp.obj x)) ≫ (D T).map b ≫
      (N q).hom.app ((c.app V).toFunctor.obj (rp.obj x)) ≫
        rq.map ((D V).map a) ≫ rq.map ((N p).hom.app z) =
      t ≫ rq.map ((E V).hom.app (rp.obj x)) ≫
        rq.map ((D V).map a) ≫ rq.map ((N p).hom.app z) :=
    congrArg (fun m => t ≫ m)
      (postcomposeTripleNormalized _ _ _ _ (pointwiseInverseNaturality_unit_app c hc q (rp.obj x))
        (rq.map ((D V).map a) ≫ rq.map ((N p).hom.app z)))
  have h5 : t ≫ rq.map ((E V).hom.app (rp.obj x)) ≫
      rq.map ((D V).map a) ≫ rq.map ((N p).hom.app z) =
        t ≫ rq.map (rp.map ((E U).hom.app x)) :=
    congrArg (fun m => t ≫ m)
      (mapTripleEq rq _ _ _ _ (pointwiseInverseNaturality_unit_app c hc p x))
  have hright := h1.trans (h2.trans (h3.trans (h4.trans h5)))
  exact hleft.trans (hnat.trans hright.symm)

/-- All three coherence laws now assemble the actual inverse StrongTrans. -/
def pointwiseInverseStrongTrans : S ⟶ R where
  app U := (D U).toCatHom
  naturality p := Cat.Hom.isoMk (N p)
  naturality_naturality alpha := by
    apply Cat.Hom₂.ext
    exact pointwiseInverseNaturality_twoCell c hc alpha
  naturality_id U := by
    apply Cat.Hom₂.ext
    apply NatTrans.ext
    funext x
    change (N (𝟙 U)).hom.app x ≫ (R.mapId U).hom.toNatTrans.app ((D U).obj x) =
      (D U).map ((S.mapId U).hom.toNatTrans.app x) ≫ 𝟙 _ ≫ 𝟙 _
    simpa only [Category.comp_id] using NatTrans.congr_app (pointwiseInverseNaturality_id c hc U) x
  naturality_comp {U V T} p q := by
    apply Cat.Hom₂.ext
    apply NatTrans.ext
    funext x
    change (N (p ≫ q)).hom.app x ≫ (R.mapComp p q).hom.toNatTrans.app ((D U).obj x) =
      (D T).map ((S.mapComp p q).hom.toNatTrans.app x) ≫ 𝟙 _ ≫
        (N q).hom.app ((S.map p).toFunctor.obj x) ≫ 𝟙 _ ≫
          (R.map q).toFunctor.map ((N p).hom.app x) ≫ 𝟙 _
    simpa only [Category.id_comp, Category.comp_id] using
      NatTrans.congr_app (pointwiseInverseNaturality_comp c hc p q) x

@[simp] theorem pointwiseInverseStrongTrans_app (U : B) :
    (pointwiseInverseStrongTrans c hc).app U = (D U).toCatHom := rfl

@[simp] theorem pointwiseInverseStrongTrans_naturality {U V : B} (p : U ⟶ V) :
    Cat.Hom.toNatIso ((pointwiseInverseStrongTrans c hc).naturality p) = N p := rfl

/-- The chosen component units form a global invertible modification. The
reverse modification's compatibility is supplied by Mathlib's isoMk, not
assumed separately. -/
def pointwiseInverseUnitModification : 𝟙 R ≅ c ≫ pointwiseInverseStrongTrans c hc :=
  Pseudofunctor.StrongTrans.isoMk (fun U => Cat.Hom.isoMk (E U)) (by
    intro U V p
    apply Cat.Hom₂.ext
    apply NatTrans.ext
    funext x
    change (E V).hom.app ((R.map p).toFunctor.obj x) ≫
        𝟙 _ ≫ (D V).map ((c.naturality p).hom.toNatTrans.app x) ≫
          𝟙 _ ≫ (N p).hom.app ((c.app U).toFunctor.obj x) ≫ 𝟙 _ =
      (𝟙 _ ≫ 𝟙 _) ≫ (R.map p).toFunctor.map ((E U).hom.app x)
    simpa only [Category.id_comp, Category.comp_id] using
      pointwiseInverseNaturality_unit_app c hc p x)

/-- The coherent retraction is constructed from pointwise equivalence only. -/
def pointwiseInverseRetractionIso : c ≫ pointwiseInverseStrongTrans c hc ≅ 𝟙 R :=
  (pointwiseInverseUnitModification c hc).symm

@[simp] theorem pointwiseInverseUnitModification_hom_app (U : B) :
    ((pointwiseInverseUnitModification c hc).hom.as.app U).toNatTrans = (E U).hom := rfl

@[simp] theorem pointwiseInverseUnitModification_inv_app (U : B) :
    ((pointwiseInverseUnitModification c hc).inv.as.app U).toNatTrans = (E U).inv := rfl

include hc in
/-- Existence has no assumed coherent inverse or coherence fields. -/
theorem exists_pointwiseInverseRetraction :
    ∃ d : S ⟶ R, Nonempty (c ≫ d ≅ 𝟙 R) :=
  ⟨pointwiseInverseStrongTrans c hc, ⟨pointwiseInverseRetractionIso c hc⟩⟩

/-! ## Regression checks: all inputs remain pointwise, and two-cells need not be invertible. -/

example (h : ∀ U : B, (c.app U).toFunctor.IsEquivalence) : S ⟶ R :=
  pointwiseInverseStrongTrans c h

example (h : ∀ U : B, (c.app U).toFunctor.IsEquivalence) :
    ∃ d : S ⟶ R, Nonempty (c ≫ d ≅ 𝟙 R) := exists_pointwiseInverseRetraction c h

example (U : B) : (pointwiseInverseStrongTrans c hc).app U = (D U).toCatHom := rfl

example {U V : B} (p : U ⟶ V) :
    Cat.Hom.toNatIso ((pointwiseInverseStrongTrans c hc).naturality p) = N p := rfl

example {U V : B} {p q : U ⟶ V} (alpha : p ⟶ q) :
    whiskerRight (S.map₂ alpha).toNatTrans (D V) ≫ (N q).hom =
      (N p).hom ≫ whiskerLeft (D U) (R.map₂ alpha).toNatTrans :=
  pointwiseInverseNaturality_twoCell c hc alpha

example (U : B) :
    (N (𝟙 U)).hom ≫ whiskerLeft (D U) (R.mapId U).hom.toNatTrans =
      whiskerRight (S.mapId U).hom.toNatTrans (D U) :=
  pointwiseInverseNaturality_id c hc U

example {U V T : B} (p : U ⟶ V) (q : V ⟶ T) :
    (N (p ≫ q)).hom ≫ whiskerLeft (D U) (R.mapComp p q).hom.toNatTrans =
      whiskerRight (S.mapComp p q).hom.toNatTrans (D T) ≫
        whiskerLeft (S.map p).toFunctor (N q).hom ≫
          whiskerRight (N p).hom (R.map q).toFunctor :=
  pointwiseInverseNaturality_comp c hc p q

example : 𝟙 R ≅ c ≫ pointwiseInverseStrongTrans c hc :=
  pointwiseInverseUnitModification c hc

example : c ≫ pointwiseInverseStrongTrans c hc ≅ 𝟙 R :=
  pointwiseInverseRetractionIso c hc

example (U : B) :
    ((pointwiseInverseRetractionIso c hc).hom.as.app U).toNatTrans = (E U).inv := rfl

example (U : B) :
    ((pointwiseInverseRetractionIso c hc).inv.as.app U).toNatTrans = (E U).hom := rfl

example : (pointwiseInverseUnitModification c hc).hom ≫
    (pointwiseInverseUnitModification c hc).inv = 𝟙 (𝟙 R) :=
  (pointwiseInverseUnitModification c hc).hom_inv_id

example : (pointwiseInverseUnitModification c hc).inv ≫
    (pointwiseInverseUnitModification c hc).hom =
      𝟙 (c ≫ pointwiseInverseStrongTrans c hc) :=
  (pointwiseInverseUnitModification c hc).inv_hom_id

#print axioms pointwiseInverseNaturality_twoCell
#print axioms pointwiseInverseNaturality_id
#print axioms pointwiseInverseNaturality_comp
#print axioms pointwiseInverseStrongTrans
#print axioms pointwiseInverseUnitModification
#print axioms exists_pointwiseInverseRetraction

end

end KUOS.DependentOriginationPointwiseInverseCoherenceV4_82
