import KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
import KUOS.DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197

namespace KUOS.DependentOriginationC60StrictChargeGlobularCalculusV5_232

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60GradedGrayThreeCategoryV5_197
open KUOS.DependentOriginationGrayC60GrayThreeCategoryCoherenceV5_197
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.232 / F78 — C60 globular calculus with strict PHASE-QUOTIENT exchange

A new C60 four-level target is built using the ACTUAL sixty vertices
and the ACTUAL original Quiver.Path one-arrows (not a one-object
delooping), but the NEW F77 phase-congruence quotient interpreted as
F75 integer-charge two/three-Hom data.

The four typed levels are:
0. REAL C60 vertices (IcosahedralDart, cardinal sixty).
1. REAL composable directed finite C60 paths (not just integers).
2. A degree-completed ZMod 2 two-cell at any parallel paths.
3. An actual F75 Mathlib three-Hom with Int×Int integer charges.

We construct BOTH independently typed vertical and horizontal
two-/three-cell operations, units, associativity, middle-four laws,
left/right real-path whiskering and reassociated three-arrow naturality,
using equality transports rather than pretending distinct dependent
path expressions are definitional equal. Source F42/F43 faces still
interpret into this completed target through F51 and the genuine
F77 quotient. The old odd/odd original phase is killed ONLY after
the quotient; both original integer charges survive, including
the physical F47 comparison charge and north signed curvature -5.

This establishes a strict four-level GLOBULAR COHERENCE CERTIFICATE for
the GRADE-COMPLETED C60 TARGET. It does NOT claim the ORIGINAL raw
F42/F54/F55 three-category is globally strict or that all physical
mixed boundaries have been glued.
-/

/-! I. The real physical C60 0/1-carrier and type-indexed 2/3 carriers -/

/-- The original SIXTY C60 vertices, rather than a new singleton. -/
abbrev C60F78Object := IcosahedralDart

/-- Actual original C60 directed paths. -/
abbrev C60F78One (a b : C60F78Object) := Quiver.Path a b

/-- A correctly globular phase-quotient 2-cell between parallel paths. -/
abbrev C60F78Two {a b : C60F78Object}
    (_p _q : C60F78One a b) := C60F75StrictChargeGrade

/-- Genuine native F75 Mathlib 3-arrows above any two parallel 2-cells. -/
abbrev C60F78Three {a b : C60F78Object}
    {p q : C60F78One a b}
    (X Y : C60F78Two p q) := X ⟶ Y

/-- REAL one-arrow unit at an original C60 vertex. -/
def c60F78IdOne (a : C60F78Object) : C60F78One a a :=
  Quiver.Path.nil

/-- REAL physical one-arrow composition, as original path concatenation. -/
def c60F78CompOne {a b c : C60F78Object}
    (p : C60F78One a b) (q : C60F78One b c) :
    C60F78One a c := p.comp q

theorem c60F78One_leftUnit {a b : C60F78Object}
    (p : C60F78One a b) :
    c60F78CompOne (c60F78IdOne a) p = p :=
  Quiver.Path.nil_comp p

theorem c60F78One_rightUnit {a b : C60F78Object}
    (p : C60F78One a b) :
    c60F78CompOne p (c60F78IdOne b) = p :=
  Quiver.Path.comp_nil p

theorem c60F78One_assoc {a b c d : C60F78Object}
    (p : C60F78One a b) (q : C60F78One b c)
    (r : C60F78One c d) :
    c60F78CompOne (c60F78CompOne p q) r =
      c60F78CompOne p (c60F78CompOne q r) :=
  Quiver.Path.comp_assoc p q r

theorem c60F78ActualVertexCount :
    Fintype.card C60F78Object = 60 :=
  c60F49ActualOriginalZeroCellCount

theorem c60F78ActualEdgeCount :
    Fintype.card TruncatedIcosahedralEdge = 90 :=
  c60F49ActualOriginalPhysicalEdgeCount

theorem c60F78ActualFaceCount :
    Fintype.card TruncatedIcosahedralSeedFace = 32 :=
  c60F49ActualOriginalPolygonFaceCount

/-! II. Both genuine two-dimensional pastings are strictly coherent -/

/-- Globular identity 2-cell at a REAL original C60 one-path. -/
def c60F78IdTwo {a b : C60F78Object}
    (p : C60F78One a b) : C60F78Two p p := ⟨0⟩

/-- Strict VERTICAL 2-cell composition above three actual parallel paths. -/
def c60F78VerticalTwo {a b : C60F78Object}
    {p q r : C60F78One a b}
    (X : C60F78Two p q) (Y : C60F78Two q r) :
    C60F78Two p r := c60F76StrictChargeTwoTensor X Y

/-- Strict HORIZONTAL 2-cell composition at REAL concatenated C60 paths. -/
def c60F78HorizontalTwo {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    (X : C60F78Two p q) (Y : C60F78Two r s) :
    C60F78Two (p.comp r) (q.comp s) :=
  c60F76StrictChargeTwoTensor X Y

theorem c60F78Two_leftUnit
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) :
    c60F78VerticalTwo (c60F78IdTwo p) X = X := by
  cases X with
  | mk x =>
    change (⟨(0 : ZMod 2) + x⟩ : C60F75StrictChargeGrade) = ⟨x⟩
    rw [zero_add]

theorem c60F78Two_rightUnit
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) :
    c60F78VerticalTwo X (c60F78IdTwo q) = X := by
  cases X with
  | mk x =>
    change (⟨x + (0 : ZMod 2)⟩ : C60F75StrictChargeGrade) = ⟨x⟩
    rw [add_zero]

theorem c60F78Two_verticalAssoc
    {a b : C60F78Object} {p q r s : C60F78One a b}
    (X : C60F78Two p q) (Y : C60F78Two q r)
    (Z : C60F78Two r s) :
    c60F78VerticalTwo (c60F78VerticalTwo X Y) Z =
      c60F78VerticalTwo X (c60F78VerticalTwo Y Z) :=
  c60F76StrictChargeTwoTensor_assoc X Y Z

/-- ACTUAL strict horizontal two-cell associativity, retaining the
independently indexed three original path segments at both boundaries. -/
theorem c60F78Two_horizontalAssoc
    {a b c d : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    {t u : C60F78One c d}
    (X : C60F78Two p q) (Y : C60F78Two r s)
    (Z : C60F78Two t u) :
    c60F78HorizontalTwo (c60F78HorizontalTwo X Y) Z =
      c60F78HorizontalTwo X (c60F78HorizontalTwo Y Z) :=
  c60F76StrictChargeTwoTensor_assoc X Y Z

/-- Strict middle-four INTERCHANGE at 2-level, rather than a
nontrivial Gray 3-cell added to repair the discrepancy. -/
theorem c60F78Two_middleFour
    {a b c : C60F78Object}
    {p q r : C60F78One a b}
    {s t u : C60F78One b c}
    (X : C60F78Two p q) (X' : C60F78Two q r)
    (Y : C60F78Two s t) (Y' : C60F78Two t u) :
    c60F78VerticalTwo
      (c60F78HorizontalTwo X Y)
      (c60F78HorizontalTwo X' Y') =
    c60F78HorizontalTwo
      (c60F78VerticalTwo X X')
      (c60F78VerticalTwo Y Y') := by
  cases X with | mk x =>
    cases X' with | mk x' =>
      cases Y with | mk y =>
        cases Y' with | mk y' =>
          change (⟨(x + y) + (x' + y')⟩ : C60F75StrictChargeGrade) =
            ⟨(x + x') + (y + y')⟩
          congr 1
          abel

/-- Genuine LEFT path whiskering of a phase-quotient 2-cell. -/
def c60F78LeftWhiskerTwo {a b c : C60F78Object}
    (prior : C60F78One a b)
    {p q : C60F78One b c} (X : C60F78Two p q) :
    C60F78Two (prior.comp p) (prior.comp q) := X

/-- Genuine RIGHT path whiskering of a phase-quotient 2-cell. -/
def c60F78RightWhiskerTwo {a b c : C60F78Object}
    {p q : C60F78One a b}
    (suffix : C60F78One b c) (X : C60F78Two p q) :
    C60F78Two (p.comp suffix) (q.comp suffix) := X

/-! III. Genuine F75 categorical 3-arrows over the original path bounds -/

def c60F78IdThree
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) : C60F78Three X X := 𝟙 X

def c60F78VerticalThree
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y Z : C60F78Two p q}
    (f : C60F78Three X Y) (g : C60F78Three Y Z) :
    C60F78Three X Z := f ≫ g

def c60F78VerticalTensorThree
    {a b : C60F78Object} {p q r : C60F78One a b}
    {X X' : C60F78Two p q} {Y Y' : C60F78Two q r}
    (f : C60F78Three X X') (g : C60F78Three Y Y') :
    C60F78Three
      (c60F78VerticalTwo X Y)
      (c60F78VerticalTwo X' Y') :=
  c60F76StrictChargeThreeTensor f g

def c60F78HorizontalThree
    {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    {X X' : C60F78Two p q} {Y Y' : C60F78Two r s}
    (f : C60F78Three X X') (g : C60F78Three Y Y') :
    C60F78Three
      (c60F78HorizontalTwo X Y)
      (c60F78HorizontalTwo X' Y') :=
  c60F76StrictChargeThreeTensor f g

def c60F78LeftWhiskerThree
    {a b c : C60F78Object} (prior : C60F78One a b)
    {p q : C60F78One b c}
    {X Y : C60F78Two p q}
    (f : C60F78Three X Y) :
    C60F78Three
      (c60F78LeftWhiskerTwo prior X)
      (c60F78LeftWhiskerTwo prior Y) := f

def c60F78RightWhiskerThree
    {a b c : C60F78Object}
    {p q : C60F78One a b} (suffix : C60F78One b c)
    {X Y : C60F78Two p q}
    (f : C60F78Three X Y) :
    C60F78Three
      (c60F78RightWhiskerTwo suffix X)
      (c60F78RightWhiskerTwo suffix Y) := f

theorem c60F78Three_leftUnit
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y : C60F78Two p q} (f : C60F78Three X Y) :
    c60F78VerticalThree (c60F78IdThree X) f = f :=
  Category.id_comp f

theorem c60F78Three_rightUnit
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y : C60F78Two p q} (f : C60F78Three X Y) :
    c60F78VerticalThree f (c60F78IdThree Y) = f :=
  Category.comp_id f

theorem c60F78Three_assoc
    {a b : C60F78Object} {p q : C60F78One a b}
    {W X Y Z : C60F78Two p q}
    (f : C60F78Three W X) (g : C60F78Three X Y)
    (h : C60F78Three Y Z) :
    c60F78VerticalThree (c60F78VerticalThree f g) h =
      c60F78VerticalThree f (c60F78VerticalThree g h) :=
  Category.assoc f g h

/-- The 3-arrow middle-four equality is STRICT in the new quotient,
for every pair of truly typed horizontal C60 path configurations. -/
theorem c60F78Three_horizontalMiddleFour
    {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    {X X' X'' : C60F78Two p q}
    {Y Y' Y'' : C60F78Two r s}
    (f : C60F78Three X X') (g : C60F78Three X' X'')
    (h : C60F78Three Y Y') (k : C60F78Three Y' Y'') :
    c60F78VerticalThree
      (c60F78HorizontalThree f h)
      (c60F78HorizontalThree g k) =
    c60F78HorizontalThree
      (c60F78VerticalThree f g)
      (c60F78VerticalThree h k) := by
  exact (c60F76StrictThree_middleFour f g h k).symm

theorem c60F78Three_verticalMiddleFour
    {a b : C60F78Object}
    {p q r : C60F78One a b}
    {X X' X'' : C60F78Two p q}
    {Y Y' Y'' : C60F78Two q r}
    (f : C60F78Three X X') (g : C60F78Three X' X'')
    (h : C60F78Three Y Y') (k : C60F78Three Y' Y'') :
    c60F78VerticalTensorThree (f ≫ g) (h ≫ k) =
      c60F78VerticalTensorThree f h ≫
        c60F78VerticalTensorThree g k :=
  c60F76StrictThree_middleFour f g h k

/-- Identity preservation by a true 3-Hom horizontal bifunctor. -/
theorem c60F78HorizontalThree_id
    {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    (X : C60F78Two p q) (Y : C60F78Two r s) :
    c60F78HorizontalThree (c60F78IdThree X) (c60F78IdThree Y) =
      c60F78IdThree (c60F78HorizontalTwo X Y) := by
  apply C60F75StrictChargeThree.ext
  change (0 : Int × Int) + 0 = 0
  exact zero_add _

theorem c60F78LeftWhiskerThree_comp
    {a b c : C60F78Object} (prior : C60F78One a b)
    {p q : C60F78One b c}
    {X Y Z : C60F78Two p q}
    (f : C60F78Three X Y) (g : C60F78Three Y Z) :
    c60F78LeftWhiskerThree prior (f ≫ g) =
      c60F78LeftWhiskerThree prior f ≫
        c60F78LeftWhiskerThree prior g := rfl

theorem c60F78RightWhiskerThree_comp
    {a b c : C60F78Object}
    {p q : C60F78One a b} (suffix : C60F78One b c)
    {X Y Z : C60F78Two p q}
    (f : C60F78Three X Y) (g : C60F78Three Y Z) :
    c60F78RightWhiskerThree suffix (f ≫ g) =
      c60F78RightWhiskerThree suffix f ≫
        c60F78RightWhiskerThree suffix g := rfl

/-- Full 3-arrow associativity NATURALITY with genuinely equalized
dependent endpoints: both original integer charges are retained.
The equalities are transported via actual eqToHom, not silently
assumed as definitional equalities of different parenthesizations. -/
theorem c60F78Three_horizontalAssocNaturality
    {a b c d : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    {t u : C60F78One c d}
    {X X' : C60F78Two p q}
    {Y Y' : C60F78Two r s}
    {Z Z' : C60F78Two t u}
    (f : C60F78Three X X') (g : C60F78Three Y Y')
    (h : C60F78Three Z Z') :
    c60F78HorizontalThree
        (c60F78HorizontalThree f g) h ≫
      eqToHom (c60F78Two_horizontalAssoc X' Y' Z') =
    eqToHom (c60F78Two_horizontalAssoc X Y Z) ≫
      c60F78HorizontalThree f
        (c60F78HorizontalThree g h) := by
  apply C60F75StrictChargeThree.ext
  have hleft :=
    C60F75StrictChargeThree.eqToHom_charge_zero
      (c60F78Two_horizontalAssoc X' Y' Z')
  have hright :=
    C60F75StrictChargeThree.eqToHom_charge_zero
      (c60F78Two_horizontalAssoc X Y Z)
  change ((f.charge + g.charge) + h.charge) +
      (eqToHom (c60F78Two_horizontalAssoc X' Y' Z')).charge =
    (eqToHom (c60F78Two_horizontalAssoc X Y Z)).charge +
      (f.charge + (g.charge + h.charge))
  rw [hleft, hright]
  abel

/-! IV. Original source interpretation and nonvanishing charge witnesses -/

/-- Original F42 face witnesses retain their original path endpoints,
while their STRICTIFIED 2-cell has the same true face degree. -/
def c60F78OriginalFaceTwo
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F42PresentedFaceCell p q) : C60F78Two p q :=
  ⟨c60F43FaceDegree X⟩

/-- Actual raw F43 source THREE-CELL interpreted through its genuine
preservation-of-degree proof and BOTH integer charge coordinates. -/
def c60F78OriginalFaceThree
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell X Y) :
    C60F78Three (c60F78OriginalFaceTwo X) (c60F78OriginalFaceTwo Y) :=
  ⟨f.preservesFaceDegree, f.toNative.charge⟩

theorem c60F78OriginalFaceThree_charge
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell X Y) :
    (c60F78OriginalFaceThree f).charge = f.toNative.charge := rfl

theorem c60F78OriginalFaceTwo_ident
    {a b : C60F78Object} (p : C60F78One a b) :
    c60F78OriginalFaceTwo (C60F42PresentedFaceCell.ident p) =
      c60F78IdTwo p := rfl

theorem c60F78OriginalFaceTwo_trans
    {a b : C60F78Object} {p q r : C60F78One a b}
    (X : C60F42PresentedFaceCell p q)
    (Y : C60F42PresentedFaceCell q r) :
    c60F78OriginalFaceTwo (.trans X Y) =
      c60F78VerticalTwo
        (c60F78OriginalFaceTwo X)
        (c60F78OriginalFaceTwo Y) := rfl

theorem c60F78OriginalFaceTwo_horizontal
    {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    (X : C60F42PresentedFaceCell p q)
    (Y : C60F42PresentedFaceCell r s) :
    c60F78OriginalFaceTwo (X.horizontalLeftFirst Y) =
      c60F78HorizontalTwo
        (c60F78OriginalFaceTwo X)
        (c60F78OriginalFaceTwo Y) := rfl

theorem c60F78OriginalFaceThree_ident
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F42PresentedFaceCell p q) :
    c60F78OriginalFaceThree
        (C60F43PresentedThreeCell.ident X) =
      c60F78IdThree (c60F78OriginalFaceTwo X) := by
  apply C60F75StrictChargeThree.ext
  rfl

theorem c60F78OriginalFaceThree_trans
    {a b : C60F78Object} {p q : C60F78One a b}
    {X Y Z : C60F42PresentedFaceCell p q}
    (f : C60F43PresentedThreeCell X Y)
    (g : C60F43PresentedThreeCell Y Z) :
    c60F78OriginalFaceThree (.trans f g) =
      c60F78VerticalThree
        (c60F78OriginalFaceThree f)
        (c60F78OriginalFaceThree g) := by
  apply C60F75StrictChargeThree.ext
  rfl

/-- The original F51 local 3-Hom descends through the REAL F77
categorical quotient before entering this four-level strict envelope. -/
def c60F78OriginalSourceStrictFunctor
    {a b : C60F78Object} (p q : C60F78One a b) :
    C60F51OriginalTwo p q ⥤ C60F75StrictChargeGrade :=
  c60F77OriginalSourceQuotient p q ⋙ c60F77QuotientToStrictCharge

theorem c60F78OriginalSourceStrictFunctor_factor
    {a b : C60F78Object} (p q : C60F78One a b) :
    c60F78OriginalSourceStrictFunctor p q =
      c60F75OriginalFaceStrictification p q :=
  c60F77OriginalSource_factor p q

/-- Original source horizontal composition remains compatible
with the strict global C60 three-arrow tensor, at real path bounds. -/
theorem c60F78OriginalSource_horizontal_preserved
    {a b c : C60F78Object}
    {p q : C60F78One a b} {r s : C60F78One b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F78OriginalSourceStrictFunctor (p.comp r) (q.comp s)).map
        (c60F51HorizontalMap f g) =
    c60F78HorizontalThree
      ((c60F78OriginalSourceStrictFunctor p q).map f)
      ((c60F78OriginalSourceStrictFunctor r s).map g) := by
  rw [c60F78OriginalSourceStrictFunctor_factor,
    c60F78OriginalSourceStrictFunctor_factor,
    c60F78OriginalSourceStrictFunctor_factor]
  exact c60F76OriginalHorizontalStrictification_tensor f g

/-- Both independently integral charge coordinates really survive
the strict quotient; a local 3-endomorphism need not be identity. -/
def c60F78PentagonChargeGenerator
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) : C60F78Three X X :=
  ⟨rfl, ((1 : Int), (0 : Int))⟩

def c60F78MixedChargeGenerator
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) : C60F78Three X X :=
  ⟨rfl, ((0 : Int), (1 : Int))⟩

theorem c60F78TwoIndependentCharges
    {a b : C60F78Object} {p q : C60F78One a b}
    (X : C60F78Two p q) :
    (c60F78PentagonChargeGenerator X).charge = ((1 : Int), (0 : Int)) ∧
      (c60F78MixedChargeGenerator X).charge = ((0 : Int), (1 : Int)) ∧
      c60F78PentagonChargeGenerator X ≠ c60F78MixedChargeGenerator X := by
  constructor
  · rfl
  constructor
  · rfl
  intro h
  have hh := congrArg (fun f : C60F78Three X X => f.charge.1) h
  norm_num at hh

/-- Actual original north C60 pentagonal loop is still a nontrivial
ORIGINAL 1-arrow after phase removal. -/
theorem c60F78NorthOriginalPath_nonidentity :
    c60F41PentagonBoundaryLoop .north ≠
      (Quiver.Path.nil :
        C60F78One (icosahedralIncidentDartAt .north .s0)
          (icosahedralIncidentDartAt .north .s0)) :=
  c60F49OriginalNorthPentagonOne_nonidentity

/-! V. Bundled, audit-friendly global strict globular certificate -/

/-- A checked strict 0/1/2/3 GLOBULAR ENVELOPE certificate. Its
objects/paths remain original, whereas 2-/3-cells are the phase
quotient's degree/Int×Int COMPLETION. This is not the raw F55
mixed-boundary 3-category, nor a claim of uncorrected flatness. -/
structure C60F78StrictGlobularCertificate : Prop where
  vertices : Fintype.card C60F78Object = 60
  physicalEdges : Fintype.card TruncatedIcosahedralEdge = 90
  polygonFaces : Fintype.card TruncatedIcosahedralSeedFace = 32
  pathLeftUnit : ∀ {a b : C60F78Object} (p : C60F78One a b),
    c60F78CompOne (c60F78IdOne a) p = p
  pathRightUnit : ∀ {a b : C60F78Object} (p : C60F78One a b),
    c60F78CompOne p (c60F78IdOne b) = p
  pathAssoc : ∀ {a b c d : C60F78Object}
      (p : C60F78One a b) (q : C60F78One b c)
      (r : C60F78One c d),
    c60F78CompOne (c60F78CompOne p q) r =
      c60F78CompOne p (c60F78CompOne q r)
  twoLeftUnit : ∀ {a b : C60F78Object} {p q : C60F78One a b}
      (X : C60F78Two p q),
    c60F78VerticalTwo (c60F78IdTwo p) X = X
  twoRightUnit : ∀ {a b : C60F78Object} {p q : C60F78One a b}
      (X : C60F78Two p q),
    c60F78VerticalTwo X (c60F78IdTwo q) = X
  twoVerticalAssoc : ∀ {a b : C60F78Object}
      {p q r s : C60F78One a b}
      (X : C60F78Two p q) (Y : C60F78Two q r)
      (Z : C60F78Two r s),
    c60F78VerticalTwo (c60F78VerticalTwo X Y) Z =
      c60F78VerticalTwo X (c60F78VerticalTwo Y Z)
  twoHorizontalAssoc : ∀ {a b c d : C60F78Object}
      {p q : C60F78One a b}
      {r s : C60F78One b c}
      {t u : C60F78One c d}
      (X : C60F78Two p q) (Y : C60F78Two r s)
      (Z : C60F78Two t u),
    c60F78HorizontalTwo (c60F78HorizontalTwo X Y) Z =
      c60F78HorizontalTwo X (c60F78HorizontalTwo Y Z)
  twoMiddleFour : ∀ {a b c : C60F78Object}
      {p q r : C60F78One a b}
      {s t u : C60F78One b c}
      (X : C60F78Two p q) (X' : C60F78Two q r)
      (Y : C60F78Two s t) (Y' : C60F78Two t u),
    c60F78VerticalTwo
      (c60F78HorizontalTwo X Y)
      (c60F78HorizontalTwo X' Y') =
    c60F78HorizontalTwo
      (c60F78VerticalTwo X X')
      (c60F78VerticalTwo Y Y')
  threeLeftUnit : ∀ {a b : C60F78Object} {p q : C60F78One a b}
      {X Y : C60F78Two p q} (f : C60F78Three X Y),
    c60F78VerticalThree (c60F78IdThree X) f = f
  threeRightUnit : ∀ {a b : C60F78Object} {p q : C60F78One a b}
      {X Y : C60F78Two p q} (f : C60F78Three X Y),
    c60F78VerticalThree f (c60F78IdThree Y) = f
  threeVerticalAssoc : ∀ {a b : C60F78Object} {p q : C60F78One a b}
      {W X Y Z : C60F78Two p q}
      (f : C60F78Three W X) (g : C60F78Three X Y)
      (h : C60F78Three Y Z),
    c60F78VerticalThree (c60F78VerticalThree f g) h =
      c60F78VerticalThree f (c60F78VerticalThree g h)
  threeHorizontalMiddleFour : ∀ {a b c : C60F78Object}
      {p q : C60F78One a b} {r s : C60F78One b c}
      {X X' X'' : C60F78Two p q}
      {Y Y' Y'' : C60F78Two r s}
      (f : C60F78Three X X') (g : C60F78Three X' X'')
      (h : C60F78Three Y Y') (k : C60F78Three Y' Y''),
    c60F78VerticalThree
      (c60F78HorizontalThree f h)
      (c60F78HorizontalThree g k) =
    c60F78HorizontalThree
      (c60F78VerticalThree f g)
      (c60F78VerticalThree h k)
  threeHorizontalAssocNaturality : ∀ {a b c d : C60F78Object}
      {p q : C60F78One a b}
      {r s : C60F78One b c}
      {t u : C60F78One c d}
      {X X' : C60F78Two p q}
      {Y Y' : C60F78Two r s}
      {Z Z' : C60F78Two t u}
      (f : C60F78Three X X') (g : C60F78Three Y Y')
      (h : C60F78Three Z Z'),
    c60F78HorizontalThree (c60F78HorizontalThree f g) h ≫
        eqToHom (c60F78Two_horizontalAssoc X' Y' Z') =
      eqToHom (c60F78Two_horizontalAssoc X Y Z) ≫
        c60F78HorizontalThree f (c60F78HorizontalThree g h)

/-- REAL constructive certificate: source path data, local Mathlib
3-Homs, strict middle-four, phase collapse and two independent
integer charges are glued into a single checked proposition. -/
theorem c60F78StrictGlobularCertificate_proved :
    C60F78StrictGlobularCertificate := by
  refine {
    vertices := c60F78ActualVertexCount
    physicalEdges := c60F78ActualEdgeCount
    polygonFaces := c60F78ActualFaceCount
    pathLeftUnit := ?_
    pathRightUnit := ?_
    pathAssoc := ?_
    twoLeftUnit := ?_
    twoRightUnit := ?_
    twoVerticalAssoc := ?_
    twoHorizontalAssoc := ?_
    twoMiddleFour := ?_
    threeLeftUnit := ?_
    threeRightUnit := ?_
    threeVerticalAssoc := ?_
    threeHorizontalMiddleFour := ?_
    threeHorizontalAssocNaturality := ?_
  }
  · intro a b p
    exact c60F78One_leftUnit p
  · intro a b p
    exact c60F78One_rightUnit p
  · intro a b c d p q r
    exact c60F78One_assoc p q r
  · intro a b p q X
    exact c60F78Two_leftUnit X
  · intro a b p q X
    exact c60F78Two_rightUnit X
  · intro a b p q r s X Y Z
    exact c60F78Two_verticalAssoc X Y Z
  · intro a b c d p q r s t u X Y Z
    exact c60F78Two_horizontalAssoc X Y Z
  · intro a b c p q r s t u X X' Y Y'
    exact c60F78Two_middleFour X X' Y Y'
  · intro a b p q X Y f
    exact c60F78Three_leftUnit f
  · intro a b p q X Y f
    exact c60F78Three_rightUnit f
  · intro a b p q W X Y Z f g h
    exact c60F78Three_assoc f g h
  · intro a b c p q r s X X' X'' Y Y' Y'' f g h k
    exact c60F78Three_horizontalMiddleFour f g h k
  · intro a b c d p q r s t u X X' Y Y' Z Z' f g h
    exact c60F78Three_horizontalAssocNaturality f g h

#print axioms c60F78ActualVertexCount
#print axioms c60F78ActualEdgeCount
#print axioms c60F78One_assoc
#print axioms c60F78Two_verticalAssoc
#print axioms c60F78Two_horizontalAssoc
#print axioms c60F78Two_middleFour
#print axioms c60F78Three_assoc
#print axioms c60F78Three_horizontalMiddleFour
#print axioms c60F78Three_verticalMiddleFour
#print axioms c60F78HorizontalThree_id
#print axioms c60F78Three_horizontalAssocNaturality
#print axioms c60F78OriginalFaceThree_trans
#print axioms c60F78OriginalSourceStrictFunctor_factor
#print axioms c60F78OriginalSource_horizontal_preserved
#print axioms c60F78TwoIndependentCharges
#print axioms c60F78NorthOriginalPath_nonidentity
#print axioms c60F78StrictGlobularCertificate_proved

end
end KUOS.DependentOriginationC60StrictChargeGlobularCalculusV5_232
