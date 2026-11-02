import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5NArbitraryTreeUnitors
import Mathlib.CategoryTheory.Whiskering
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK5O — genuine contextual whiskering and unconditional
finite typed rewrite path coherence for pointwise category equivalences.

GK5M establishes every arbitrary-subtree associator square.
GK5N establishes both unitor squares. The last two genuinely typed
GK5D constructors are whiskerRight and whiskerLeft. We prove their
whole Mathlib NatIso squares using real horizontal interchange,
GK5K/GK5L nonstrict compositor naturality and the actual child square,
without identifying distinct category presentations strictly.

Then only after all five constructors are discharged, GK5H's already
proven local-to-global theorem yields unconditional whole NatIso
and whole NatTrans path naturality.

Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Same public root107, append-only, protected #1558 remains Draft/open.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC

section FullGeneratorCoherence
variable {I : Type uI} {C D : I → Cat.{vC,uC}}
variable (e : ∀ i : I, C i ≌ D i)

/-- A genuine child basic NatIso square remains coherent upon
right-whiskering by any real finite typed subtree. This compares
three actual pastings: child square, Mathlib isoWhisker interchange,
and the GK5L left-variable nonstrict compositor square. -/
private theorem nativeGK5OWhiskerRight_of_square
    {i j k : I} {a b : NativeGK5DTypedTree C i j}
    (s : NativeGK5DTypedStep C a b)
    (c : NativeGK5DTypedTree C j k)
    (hs : NativeGK5JPathSquare e (NativeGK5DTypedPath.basic s)) :
    NativeGK5JPathSquare e
      (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.whiskerRight s c)) := by
  let Ra := nativeGK5DTreeComposite a
  let Rb := nativeGK5DTreeComposite b
  let Sc := nativeGK5DTreeComposite c
  let Tc := nativeGK5DTreeComposite (nativeGK5GChangeTree e c)
  let α := nativeGK5DStepIso (nativeGK5GChangeStep e s)
  let β := nativeGK5GChangeIso e (nativeGK5DStepIso s)
  let φa := nativeGK5GChangeTreeIso e a
  let φb := nativeGK5GChangeTreeIso e b
  let φc := nativeGK5GChangeTreeIso e c
  have hchild : α ≪≫ φb = φa ≪≫ β := by
    simpa only [NativeGK5JPathSquare, nativeGK5DPathIso,
      nativeGK5GChangePath, α, β, φa, φb] using hs
  have hinter : Functor.isoWhiskerRight β Tc ≪≫
        Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Rb) φc =
      Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc ≪≫
        Functor.isoWhiskerRight β (nativeGK5GChangeAtom e Sc) :=
    (Functor.isoWhiskerLeft_trans_isoWhiskerRight β φc).symm
  have hcomp := nativeGK5LChangeCompIso_left e (nativeGK5DStepIso s) Sc
  change
    Functor.isoWhiskerRight α Tc ≪≫
      ((Functor.isoWhiskerRight φb Tc ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Rb) φc) ≪≫
        nativeGK5GChangeCompIso e Rb Sc) =
    ((Functor.isoWhiskerRight φa Tc ≪≫
        Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫
       nativeGK5GChangeCompIso e Ra Sc) ≪≫
      nativeGK5GChangeIso e (Functor.isoWhiskerRight (nativeGK5DStepIso s) Sc)
  calc
    _ = (Functor.isoWhiskerRight (α ≪≫ φb) Tc ≪≫
           Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Rb) φc) ≪≫
          nativeGK5GChangeCompIso e Rb Sc := by
            simp only [Functor.isoWhiskerRight_trans, Iso.trans_assoc]
    _ = (Functor.isoWhiskerRight (φa ≪≫ β) Tc ≪≫
           Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Rb) φc) ≪≫
          nativeGK5GChangeCompIso e Rb Sc := by rw [hchild]
    _ = ((Functor.isoWhiskerRight φa Tc ≪≫
           Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫
          Functor.isoWhiskerRight β (nativeGK5GChangeAtom e Sc)) ≪≫
          nativeGK5GChangeCompIso e Rb Sc := by
            simp only [Functor.isoWhiskerRight_trans, Iso.trans_assoc]
            rw [hinter]
    _ = ((Functor.isoWhiskerRight φa Tc ≪≫
           Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫
           nativeGK5GChangeCompIso e Ra Sc) ≪≫
         nativeGK5GChangeIso e (Functor.isoWhiskerRight (nativeGK5DStepIso s) Sc) := by
           simpa only [Iso.trans_assoc] using
             congrArg
               (fun t => (Functor.isoWhiskerRight φa Tc ≪≫
                  Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫ t)
               hcomp

/-- A genuine child basic NatIso square remains coherent upon
left-whiskering by any real finite typed subtree. Uses the opposite
Mathlib horizontal interchange and GK5K compositor right naturality. -/
private theorem nativeGK5OWhiskerLeft_of_square
    {i j k : I}
    (a : NativeGK5DTypedTree C i j)
    {b c : NativeGK5DTypedTree C j k}
    (s : NativeGK5DTypedStep C b c)
    (hs : NativeGK5JPathSquare e (NativeGK5DTypedPath.basic s)) :
    NativeGK5JPathSquare e
      (NativeGK5DTypedPath.basic (NativeGK5DTypedStep.whiskerLeft a s)) := by
  let Ra := nativeGK5DTreeComposite a
  let Sb := nativeGK5DTreeComposite b
  let Sc := nativeGK5DTreeComposite c
  let Ta := nativeGK5DTreeComposite (nativeGK5GChangeTree e a)
  let α := nativeGK5DStepIso (nativeGK5GChangeStep e s)
  let β := nativeGK5GChangeIso e (nativeGK5DStepIso s)
  let φa := nativeGK5GChangeTreeIso e a
  let φb := nativeGK5GChangeTreeIso e b
  let φc := nativeGK5GChangeTreeIso e c
  have hchild : α ≪≫ φc = φb ≪≫ β := by
    simpa only [NativeGK5JPathSquare, nativeGK5DPathIso,
      nativeGK5GChangePath, α, β, φb, φc] using hs
  have hinter :
      Functor.isoWhiskerLeft Ta α ≪≫
        Functor.isoWhiskerRight φa (nativeGK5DTreeComposite (nativeGK5GChangeTree e c)) =
      Functor.isoWhiskerRight φa (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
        Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) α :=
    Functor.isoWhiskerLeft_trans_isoWhiskerRight φa α
  have hcomp := nativeGK5KChangeCompIso_right e Ra (nativeGK5DStepIso s)
  change
    Functor.isoWhiskerLeft Ta α ≪≫
      ((Functor.isoWhiskerRight φa
         (nativeGK5DTreeComposite (nativeGK5GChangeTree e c)) ≪≫
        Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫
        nativeGK5GChangeCompIso e Ra Sc) =
    ((Functor.isoWhiskerRight φa
         (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
        Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φb) ≪≫
        nativeGK5GChangeCompIso e Ra Sb) ≪≫
      nativeGK5GChangeIso e (Functor.isoWhiskerLeft Ra (nativeGK5DStepIso s))
  calc
    _ = ((Functor.isoWhiskerRight φa
            (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) α) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc) ≪≫
          nativeGK5GChangeCompIso e Ra Sc := by
            simpa only [Iso.trans_assoc] using
              congrArg (fun t =>
                t ≪≫ Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φc ≪≫
                  nativeGK5GChangeCompIso e Ra Sc) hinter
    _ = (Functor.isoWhiskerRight φa
            (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) (α ≪≫ φc)) ≪≫
          nativeGK5GChangeCompIso e Ra Sc := by
            simp only [Functor.isoWhiskerLeft_trans, Iso.trans_assoc]
    _ = (Functor.isoWhiskerRight φa
            (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) (φb ≪≫ β)) ≪≫
          nativeGK5GChangeCompIso e Ra Sc := by rw [hchild]
    _ = ((Functor.isoWhiskerRight φa
            (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φb) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) β) ≪≫
          nativeGK5GChangeCompIso e Ra Sc := by
            simp only [Functor.isoWhiskerLeft_trans, Iso.trans_assoc]
    _ = ((Functor.isoWhiskerRight φa
            (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
          Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φb) ≪≫
          nativeGK5GChangeCompIso e Ra Sb) ≪≫
        nativeGK5GChangeIso e (Functor.isoWhiskerLeft Ra (nativeGK5DStepIso s)) := by
          simpa only [Iso.trans_assoc] using
            congrArg
              (fun t =>
                (Functor.isoWhiskerRight φa
                   (nativeGK5DTreeComposite (nativeGK5GChangeTree e b)) ≪≫
                 Functor.isoWhiskerLeft (nativeGK5GChangeAtom e Ra) φb) ≪≫ t)
              hcomp

/-- Every *actual* GK5D associator/unitor/contextual whiskering
generator is unconditionally coherent as a whole Mathlib NatIso.
Constructor-pattern recursion retains the genuine typed endpoints. -/
theorem nativeGK5OAllBasicSteps :
    ∀ {i j : I} {a b : NativeGK5DTypedTree C i j}
        (s : NativeGK5DTypedStep C a b),
      NativeGK5JPathSquare e (NativeGK5DTypedPath.basic s)
  | _, _, _, _, .assoc a b c => nativeGK5MAssociator_subtrees e a b c
  | _, _, _, _, .leftUnit a => nativeGK5NLeftUnit_subtree e a
  | _, _, _, _, .rightUnit a => nativeGK5NRightUnit_subtree e a
  | _, _, _, _, .whiskerRight s c =>
      nativeGK5OWhiskerRight_of_square e s c (nativeGK5OAllBasicSteps s)
  | _, _, _, _, .whiskerLeft a s =>
      nativeGK5OWhiskerLeft_of_square e a s (nativeGK5OAllBasicSteps s)

/-- Discharge the GK5H exact local obstruction WITHOUT postulating
the basic-generator square as a hypothesis. -/
theorem nativeGK5OStepCompatible :
    NativeGK5HStepCompatible (C := C) (D := D) e := by
  intro i j a b s
  simpa only [NativeGK5JPathSquare, nativeGK5DPathIso,
    nativeGK5GChangePath] using (nativeGK5OAllBasicSteps e s)

/-- From real local coherence and GK5H's already proved exact gluing,
ALL genuine finite typed rewrite paths have the whole Mathlib NatIso
pseudonaturality square UNCONDITIONALLY. -/
theorem nativeGK5OAllFinitePaths :
    NativeGK5HPathCompatible (C := C) (D := D) e :=
  nativeGK5HLocalStep_implies_allPaths e (nativeGK5OStepCompatible e)

/-- Whole NatTrans hom naturality for EVERY genuine finite typed path,
with no lingering local compatibility premise. -/
theorem nativeGK5OAllFinitePaths_natTrans
    {i j : I} {a b : NativeGK5DTypedTree C i j}
    (q : NativeGK5DTypedPath C a b) :
    (nativeGK5DPathIso (nativeGK5GChangePath e q)).hom ≫
      (nativeGK5GChangeTreeIso e b).hom =
    (nativeGK5GChangeTreeIso e a).hom ≫
      (nativeGK5GChangeIso e (nativeGK5DPathIso q)).hom :=
  nativeGK5HPathNatTrans_square_of_local e (nativeGK5OStepCompatible e) q

/-- Hence the canonical GK5J endpoint obstruction is also
unconditionally discharged for ALL identical typed ordered leaves. -/
theorem nativeGK5OEndpointCompatible :
    NativeGK5JEndpointCompatible (C := C) (D := D) e :=
  (nativeGK5JEndpoints_iff_localSteps e).mpr (nativeGK5OStepCompatible e)

#print axioms nativeGK5OAllBasicSteps
#print axioms nativeGK5OStepCompatible
#print axioms nativeGK5OAllFinitePaths
#print axioms nativeGK5OAllFinitePaths_natTrans
#print axioms nativeGK5OEndpointCompatible

end FullGeneratorCoherence
end
end Kuu.F112.Physical
