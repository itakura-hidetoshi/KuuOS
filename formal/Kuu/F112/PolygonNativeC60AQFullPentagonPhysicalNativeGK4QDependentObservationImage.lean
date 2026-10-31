import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4PCompositionalObserverKernel
import Mathlib.Tactic

/-!
# F112-P94D3GK4Q — genuinely typed observation images

Each hom is the ACTUAL image of an observer on the existing original P92B
witness-existence quotient. No replacement raw route space or lost dependent
F45 endpoints. Under the three GK4P genuine-route observation laws, actual
P92B composition and P93 context maps act on these typed image subtypes.
Prove factorization through the observable image, unique induced operations,
and conditional associativity ONLY for the observable image when its VALUE
operation is associative. Never transfer associativity or units backwards
to the original P92B quotient. Boolean and Option Nat are genuine instances;
the finer Option Nat still cannot descend along structural unit seams.
No sorry/admit/axiom or Gray. Same-root append-only; public roots 107.
Lean 4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

/-- Actual image at a FIXED fully dependent original F45 boundary,
rather than all of B or an invented replacement for P92B classes. -/
abbrev NativeGK4QImage
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  { value : B // ∃ q : NativeF55P92AssocRouteClasses first last,
      observe first last q = value }

/-- Canonical projection from the actual P92B quotient onto its image. -/
def nativeGK4QOfClass
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (q : NativeF55P92AssocRouteClasses first last) :
    NativeGK4QImage observe first last :=
  ⟨observe first last q, ⟨q, rfl⟩⟩

/-- No extra image point is invented: every one has a genuine P92B witness. -/
theorem nativeGK4QOfClass_surjective
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Surjective (nativeGK4QOfClass observe first last) := by
  intro z
  obtain ⟨q, hq⟩ := z.property
  refine ⟨q, ?_⟩
  apply Subtype.ext
  exact hq

/-- GK4P's RAW composition law extends to actual quotient classes. -/
theorem nativeGK4Q_map_compose
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    observe t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) =
      combine (observe t₁ t₂ u) (observe t₂ t₃ v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro r
  refine _root_.Quotient.inductionOn v ?_
  intro s
  simpa only [nativeGK4H_p92Compose_class] using (laws.map_trans r s)

/-- Genuine P93 quotient whiskering is measured by the declared left action. -/
theorem nativeGK4Q_map_leftContext
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (q : NativeF55P92AssocRouteClasses first last) :
    observe (.node first later) (.node last later)
      (nativeF55P93LeftContextClass later q) =
      leftAction later (observe first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro r
  change nativeGK4ORead observe (.leftContext r later) =
    leftAction later (nativeGK4ORead observe r)
  exact laws.map_leftContext r later

/-- Genuine P93 quotient whiskering is measured by the declared right action. -/
theorem nativeGK4Q_map_rightContext
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (q : NativeF55P92AssocRouteClasses first last) :
    observe (.node earlier first) (.node earlier last)
      (nativeF55P93RightContextClass earlier q) =
      rightAction earlier (observe first last q) := by
  refine _root_.Quotient.inductionOn q ?_
  intro r
  change nativeGK4ORead observe (.rightContext earlier r) =
    rightAction earlier (nativeGK4ORead observe r)
  exact laws.map_rightContext earlier r

/-- TRUE image closure under the prescribed observation-value product. -/
def nativeGK4QImageCompose
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (u : NativeGK4QImage observe t₁ t₂)
    (v : NativeGK4QImage observe t₂ t₃) :
    NativeGK4QImage observe t₁ t₃ :=
  ⟨combine u.val v.val, by
    obtain ⟨r, hr⟩ := u.property
    obtain ⟨s, hs⟩ := v.property
    refine ⟨nativeGK4H_p92Compose t₁ t₂ t₃ r s, ?_⟩
    calc
      observe t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ r s) =
          combine (observe t₁ t₂ r) (observe t₂ t₃ s) :=
        nativeGK4Q_map_compose observe combine leftAction rightAction laws t₁ t₂ t₃ r s
      _ = combine u.val v.val := congrArg₂ combine hr hs⟩

/-- The image operation is a STRICT observable factor of actual P92B composition. -/
theorem nativeGK4QImageCompose_ofClass
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₂ t₃
        (nativeGK4QOfClass observe t₁ t₂ u)
        (nativeGK4QOfClass observe t₂ t₃ v) =
      nativeGK4QOfClass observe t₁ t₃ (nativeGK4H_p92Compose t₁ t₂ t₃ u v) := by
  apply Subtype.ext
  exact (nativeGK4Q_map_compose observe combine leftAction rightAction laws t₁ t₂ t₃ u v).symm

/-- Uniqueness: no competing operation on the image can commute with
projection from ALL actual source P92B classes. -/
theorem nativeGK4QImageCompose_unique
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (f : NativeGK4QImage observe t₁ t₂ → NativeGK4QImage observe t₂ t₃ →
      NativeGK4QImage observe t₁ t₃)
    (hf : ∀ (u : NativeF55P92AssocRouteClasses t₁ t₂)
        (v : NativeF55P92AssocRouteClasses t₂ t₃),
        f (nativeGK4QOfClass observe t₁ t₂ u)
          (nativeGK4QOfClass observe t₂ t₃ v) =
        nativeGK4QOfClass observe t₁ t₃
          (nativeGK4H_p92Compose t₁ t₂ t₃ u v)) :
    ∀ u v, f u v =
      nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₂ t₃ u v := by
  intro u v
  obtain ⟨r, rfl⟩ := nativeGK4QOfClass_surjective observe t₁ t₂ u
  obtain ⟨s, rfl⟩ := nativeGK4QOfClass_surjective observe t₂ t₃ v
  rw [hf r s, nativeGK4QImageCompose_ofClass]

/-- On the image, associativity follows from VALUE associativity, without
asserting the missing original P92B three-route associativity. -/
theorem nativeGK4QImageCompose_assoc
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    (assoc : ∀ x y z : B, combine (combine x y) z = combine x (combine y z))
    {a b : D} {x y : E} {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
    (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)
    (u : NativeGK4QImage observe t₁ t₂)
    (v : NativeGK4QImage observe t₂ t₃)
    (w : NativeGK4QImage observe t₃ t₄) :
    nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₃ t₄
        (nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₂ t₃ u v) w =
      nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₂ t₄
        u (nativeGK4QImageCompose observe combine leftAction rightAction laws t₂ t₃ t₄ v w) := by
  apply Subtype.ext
  exact assoc u.val v.val w.val

/-- Actual P93 left whiskering closes on the image; all endpoints persist. -/
def nativeGK4QImageLeftContext
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (u : NativeGK4QImage observe first last) :
    NativeGK4QImage observe (.node first later) (.node last later) :=
  ⟨leftAction later u.val, by
    obtain ⟨q, hq⟩ := u.property
    refine ⟨nativeF55P93LeftContextClass later q, ?_⟩
    calc
      observe (.node first later) (.node last later)
          (nativeF55P93LeftContextClass later q) =
        leftAction later (observe first last q) :=
        nativeGK4Q_map_leftContext observe combine leftAction rightAction laws first last later q
      _ = leftAction later u.val := congrArg (leftAction later) hq⟩

/-- The left image action is a strict factor of ACTUAL P93 whiskering. -/
theorem nativeGK4QImageLeftContext_ofClass
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4QImageLeftContext observe combine leftAction rightAction laws first last later
        (nativeGK4QOfClass observe first last q) =
      nativeGK4QOfClass observe (.node first later) (.node last later)
        (nativeF55P93LeftContextClass later q) := by
  apply Subtype.ext
  exact (nativeGK4Q_map_leftContext observe combine leftAction rightAction laws first last later q).symm

/-- Actual P93 right whiskering closes on the image. -/
def nativeGK4QImageRightContext
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (u : NativeGK4QImage observe first last) :
    NativeGK4QImage observe (.node earlier first) (.node earlier last) :=
  ⟨rightAction earlier u.val, by
    obtain ⟨q, hq⟩ := u.property
    refine ⟨nativeF55P93RightContextClass earlier q, ?_⟩
    calc
      observe (.node earlier first) (.node earlier last)
          (nativeF55P93RightContextClass earlier q) =
        rightAction earlier (observe first last q) :=
        nativeGK4Q_map_rightContext observe combine leftAction rightAction laws earlier first last q
      _ = rightAction earlier u.val := congrArg (rightAction earlier) hq⟩

/-- The right image action is a strict factor of actual P93 whiskering. -/
theorem nativeGK4QImageRightContext_ofClass
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4QImageRightContext observe combine leftAction rightAction laws earlier first last
        (nativeGK4QOfClass observe first last q) =
      nativeGK4QOfClass observe (.node earlier first) (.node earlier last)
        (nativeF55P93RightContextClass earlier q) := by
  apply Subtype.ext
  exact (nativeGK4Q_map_rightContext observe combine leftAction rightAction laws earlier first last q).symm

/-- Uniqueness of induced left context from the surjective P92B projection. -/
theorem nativeGK4QImageLeftContext_unique
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (f : NativeGK4QImage observe first last →
      NativeGK4QImage observe (.node first later) (.node last later))
    (hf : ∀ q : NativeF55P92AssocRouteClasses first last,
      f (nativeGK4QOfClass observe first last q) =
        nativeGK4QOfClass observe (.node first later) (.node last later)
          (nativeF55P93LeftContextClass later q)) :
    ∀ z, f z =
      nativeGK4QImageLeftContext observe combine leftAction rightAction laws first last later z := by
  intro z
  obtain ⟨q, rfl⟩ := nativeGK4QOfClass_surjective observe first last z
  rw [hf q, nativeGK4QImageLeftContext_ofClass]

/-- Uniqueness of induced right context from the actual P92B projection. -/
theorem nativeGK4QImageRightContext_unique
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] {B : Type uB}
    (observe : NativeGK4OObserverFamily p D E B)
    (combine : B → B → B)
    (leftAction rightAction : NativeGK4PContextAction p D E B)
    (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b} {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (f : NativeGK4QImage observe first last →
      NativeGK4QImage observe (.node earlier first) (.node earlier last))
    (hf : ∀ q : NativeF55P92AssocRouteClasses first last,
      f (nativeGK4QOfClass observe first last q) =
        nativeGK4QOfClass observe (.node earlier first) (.node earlier last)
          (nativeF55P93RightContextClass earlier q)) :
    ∀ z, f z =
      nativeGK4QImageRightContext observe combine leftAction rightAction laws earlier first last z := by
  intro z
  obtain ⟨q, rfl⟩ := nativeGK4QOfClass_surjective observe first last z
  rw [hf q, nativeGK4QImageRightContext_ofClass]

/-- For the genuine GK4K image, some 0 is absent at every typed boundary.
This is stronger than treating the entire Option Nat codomain as an image. -/
theorem nativeGK4QOptionImage_no_zero
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (z : NativeGK4QImage (nativeGK4OOptionFamily p D E) first last) :
    z.val ≠ some 0 := by
  obtain ⟨q, hq⟩ := z.property
  intro hz
  exact nativeGK4KP92Option_no_zero first last q (hq.trans hz)

/- The generic no-zero theorem specializes to the genuine physical C60 north
triple by using nativeGK4FPhysicalNorthTriple as both endpoints. -/

#print axioms NativeGK4QImage
#print axioms nativeGK4QOfClass
#print axioms nativeGK4QOfClass_surjective
#print axioms nativeGK4Q_map_compose
#print axioms nativeGK4Q_map_leftContext
#print axioms nativeGK4Q_map_rightContext
#print axioms nativeGK4QImageCompose
#print axioms nativeGK4QImageCompose_ofClass
#print axioms nativeGK4QImageCompose_unique
#print axioms nativeGK4QImageCompose_assoc
#print axioms nativeGK4QImageLeftContext
#print axioms nativeGK4QImageLeftContext_ofClass
#print axioms nativeGK4QImageRightContext
#print axioms nativeGK4QImageRightContext_ofClass
#print axioms nativeGK4QImageLeftContext_unique
#print axioms nativeGK4QImageRightContext_unique
#print axioms nativeGK4QOptionImage_no_zero

end
end Kuu.F112.Physical
