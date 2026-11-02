import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5YDirectPhiFiveEdgeCoherence
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5PIndexChangeNaturality
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK5Z — true dependent-index reclassification of the
GK5Y full five-edge independent direct-Phi pentagon.

Fix ANY index map f : I → J, including non-injective maps, and four
genuine J-indexed Mathlib pointwise equivalences. The actual fully
dependent fourfold category change COMMUTES with GK5F relabeling.
All five true Mathlib equivalence parenthesizations and their whole
NatIso associator edges agree under pullback of the categories.

We explicitly construct five whole direct-Phi witnesses on the
pullback typed-tree source by transporting each independently
constructed J-indexed GK5X direct Phi through the actual equality-
induced whole source NatIso. Their five genuine GK5Y edge squares
and relative edge automorphisms all remain coherent without
injection hypotheses or strictifying equivalence unit/counit.

The transported Phi is distinguished from the separately recursive
Phi of the pullback family; an equality between those two witness
constructions requires an additional genuine whole-Phi comparison.
No raw higher cells, global Gray, or unrestricted hyperdescent.

Fixed Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Canonical main, same-root107, append-only/tighten-only,
strict 空 center, independent Kuu a presentation.
Protected validation-only #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI uJ vC uC

section TypedIndexPentagon
variable {I : Type uI} {J : Type uJ}
variable (f : I → J)
variable {C D E F G : J → Cat.{vC,uC}}
variable (e : ∀ j : J, C j ≌ D j)
variable (g : ∀ j : J, D j ≌ E j)
variable (h : ∀ j : J, E j ≌ F j)
variable (k : ∀ j : J, F j ≌ G j)

/-- Strict exchange of the FOUR actual typed-tree equivalence
transports with an arbitrary non-injective index reclassification.
All original intermediate categories and unit/paste nodes survive. -/
theorem nativeGK5ZFourTree_reindex
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5FTreeReindex f G
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) =
      nativeGK5XFourTree e g h k
        (nativeGK5FTreeReindex f C t) := by
  dsimp only [nativeGK5XFourTree]
  rw [nativeGK5PChangeTree_reindex f k]
  rw [nativeGK5PChangeTree_reindex f h]
  rw [nativeGK5PChangeTree_reindex f g]
  rw [nativeGK5PChangeTree_reindex f e]

/-- Genuine whole Mathlib source functor equality between the
fourfold actual pullback change and the fourfold reindexed change. -/
theorem nativeGK5ZFourComposite_reindex
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) =
      nativeGK5DTreeComposite
        (nativeGK5XFourTree e g h k
          (nativeGK5FTreeReindex f C t)) := by
  calc
    _ = nativeGK5DTreeComposite
        (nativeGK5FTreeReindex f G
          (nativeGK5XFourTree
            (fun x : I => e (f x)) (fun x : I => g (f x))
            (fun x : I => h (f x)) (fun x : I => k (f x)) t)) :=
          (nativeGK5FTreeComposite_reindex f G _).symm
    _ = _ := congrArg nativeGK5DTreeComposite
      (nativeGK5ZFourTree_reindex f e g h k t)

/-- Whole equality-induced source NatIso, not an asserted strict
equality of independently recursive nonstrict Phi witnesses. -/
noncomputable def nativeGK5ZSourceIso
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite
        (nativeGK5XFourTree e g h k
          (nativeGK5FTreeReindex f C t)) :=
  eqToIso (nativeGK5ZFourComposite_reindex f e g h k t)

/-- All FIVE parenthesizations are genuine Mathlib Equivalence.trans
and pointwise commute with pulling back even noninjective indices. -/

theorem nativeGK5ZBracket0_reindex (i : I) :
    nativeGK5XBracket0
      (fun x : I => e (f x)) (fun x : I => g (f x))
      (fun x : I => h (f x)) (fun x : I => k (f x)) i =
    nativeGK5XBracket0 e g h k (f i) := by
  rfl

theorem nativeGK5ZBracket1_reindex (i : I) :
    nativeGK5XBracket1
      (fun x : I => e (f x)) (fun x : I => g (f x))
      (fun x : I => h (f x)) (fun x : I => k (f x)) i =
    nativeGK5XBracket1 e g h k (f i) := by
  rfl

theorem nativeGK5ZBracket2_reindex (i : I) :
    nativeGK5XBracket2
      (fun x : I => e (f x)) (fun x : I => g (f x))
      (fun x : I => h (f x)) (fun x : I => k (f x)) i =
    nativeGK5XBracket2 e g h k (f i) := by
  rfl

theorem nativeGK5ZBracket3_reindex (i : I) :
    nativeGK5XBracket3
      (fun x : I => e (f x)) (fun x : I => g (f x))
      (fun x : I => h (f x)) (fun x : I => k (f x)) i =
    nativeGK5XBracket3 e g h k (f i) := by
  rfl

theorem nativeGK5ZBracket4_reindex (i : I) :
    nativeGK5XBracket4
      (fun x : I => e (f x)) (fun x : I => g (f x))
      (fun x : I => h (f x)) (fun x : I => k (f x)) i =
    nativeGK5XBracket4 e g h k (f i) := by
  rfl

/-- The ordered dependent leaf category boundaries can be merged
by f but the original type-level source/target remains preserved. -/
theorem nativeGK5ZTreeComposite_reindex
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t) =
      nativeGK5DTreeComposite (C := fun x : I => C (f x)) t :=
  nativeGK5FTreeComposite_reindex f C t

/-- Exact whole EqToIso associator at a SAME genuine typed atom
commutes with reindexing for pentagon edge 01. No unit/counit strictness. -/
theorem nativeGK5ZEdge01_reindex
    {i j : I} (R : C (f i) ⥤ C (f j)) :
    nativeGK5XEdge01
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) R =
      nativeGK5XEdge01 e g h k R := by
  rfl

/-- Exact whole EqToIso associator at a SAME genuine typed atom
commutes with reindexing for pentagon edge 12. No unit/counit strictness. -/
theorem nativeGK5ZEdge12_reindex
    {i j : I} (R : C (f i) ⥤ C (f j)) :
    nativeGK5XEdge12
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) R =
      nativeGK5XEdge12 e g h k R := by
  rfl

/-- Exact whole EqToIso associator at a SAME genuine typed atom
commutes with reindexing for pentagon edge 23. No unit/counit strictness. -/
theorem nativeGK5ZEdge23_reindex
    {i j : I} (R : C (f i) ⥤ C (f j)) :
    nativeGK5XEdge23
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) R =
      nativeGK5XEdge23 e g h k R := by
  rfl

/-- Exact whole EqToIso associator at a SAME genuine typed atom
commutes with reindexing for pentagon edge 04. No unit/counit strictness. -/
theorem nativeGK5ZEdge04_reindex
    {i j : I} (R : C (f i) ⥤ C (f j)) :
    nativeGK5XEdge04
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) R =
      nativeGK5XEdge04 e g h k R := by
  rfl

/-- Exact whole EqToIso associator at a SAME genuine typed atom
commutes with reindexing for pentagon edge 43. No unit/counit strictness. -/
theorem nativeGK5ZEdge43_reindex
    {i j : I} (R : C (f i) ⥤ C (f j)) :
    nativeGK5XEdge43
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) R =
      nativeGK5XEdge43 e g h k R := by
  rfl

/-- The genuine original four-equivalence WHOLE pentagon is
transported to the complete dependent original index set, including
noninjective reclassification. This explicitly keeps three versus
two actual NatIso paths, not only an objectwise square. -/
theorem nativeGK5ZPullbackPentagon_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    (nativeGK5XEdge01
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) ≪≫
      nativeGK5XEdge12
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t)) ≪≫
      nativeGK5XEdge23
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) =
    nativeGK5XEdge04
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) ≪≫
      nativeGK5XEdge43
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) := by
  exact nativeGK5XPentagon_whole
    (fun x : I => e (f x)) (fun x : I => g (f x))
    (fun x : I => h (f x)) (fun x : I => k (f x))
    (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t)

/-- The same genuine pentagon as an equality of WHOLE Mathlib
NatTrans hom witnesses, not merely objectwise equality. -/
theorem nativeGK5ZPullbackPentagon_natTrans
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    ((nativeGK5XEdge01
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) ≪≫
      nativeGK5XEdge12
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t)) ≪≫
      nativeGK5XEdge23
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t)).hom =
    (nativeGK5XEdge04
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t) ≪≫
      nativeGK5XEdge43
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x))
        (nativeGK5DTreeComposite (C := fun x : I => C (f x)) t)).hom :=
  congrArg Iso.hom (nativeGK5ZPullbackPentagon_whole f e g h k t)

/-- The five GENUINE original category equivalence direct recursive
Phi witnesses are now transported through the true whole eqToIso
source comparison from GK5F relabeling. This is not a fabricated
equality with the separately constructed pullback direct Phi. -/
noncomputable def nativeGK5ZTransportedPhi0
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket0 e g h k)
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) :=
  nativeGK5ZSourceIso f e g h k t ≪≫
    nativeGK5XDirectPhi0 e g h k
      (nativeGK5FTreeReindex f C t)

noncomputable def nativeGK5ZTransportedPhi1
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket1 e g h k)
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) :=
  nativeGK5ZSourceIso f e g h k t ≪≫
    nativeGK5XDirectPhi1 e g h k
      (nativeGK5FTreeReindex f C t)

noncomputable def nativeGK5ZTransportedPhi2
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket2 e g h k)
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) :=
  nativeGK5ZSourceIso f e g h k t ≪≫
    nativeGK5XDirectPhi2 e g h k
      (nativeGK5FTreeReindex f C t)

noncomputable def nativeGK5ZTransportedPhi3
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e g h k)
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) :=
  nativeGK5ZSourceIso f e g h k t ≪≫
    nativeGK5XDirectPhi3 e g h k
      (nativeGK5FTreeReindex f C t)

noncomputable def nativeGK5ZTransportedPhi4
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5GChangeAtom (nativeGK5XBracket4 e g h k)
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) :=
  nativeGK5ZSourceIso f e g h k t ≪≫
    nativeGK5XDirectPhi4 e g h k
      (nativeGK5FTreeReindex f C t)

/- The five direct-Phi whole NatIso edge squares are obtained by
actual precomposition with the canonical source change EqToIso.
The original GK5Y edge comparisons remain the only authority. -/
/-- Whole nonstrict direct-Phi edge 01 retains its genuine
coherence after arbitrary dependent index reclassification. -/
theorem nativeGK5ZTransportedEdge01_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedPhi0 f e g h k t ≪≫
      nativeGK5XEdge01 e g h k
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
      nativeGK5ZTransportedPhi1 f e g h k t := by
  simpa only [nativeGK5ZTransportedPhi0,
    nativeGK5ZTransportedPhi1, Iso.trans_assoc] using
    congrArg
      (fun iso => nativeGK5ZSourceIso f e g h k t ≪≫ iso)
      (nativeGK5YEdge01_whole e g h k
        (nativeGK5FTreeReindex f C t))

/-- Whole nonstrict direct-Phi edge 12 retains its genuine
coherence after arbitrary dependent index reclassification. -/
theorem nativeGK5ZTransportedEdge12_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedPhi1 f e g h k t ≪≫
      nativeGK5XEdge12 e g h k
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
      nativeGK5ZTransportedPhi2 f e g h k t := by
  simpa only [nativeGK5ZTransportedPhi1,
    nativeGK5ZTransportedPhi2, Iso.trans_assoc] using
    congrArg
      (fun iso => nativeGK5ZSourceIso f e g h k t ≪≫ iso)
      (nativeGK5YEdge12_whole e g h k
        (nativeGK5FTreeReindex f C t))

/-- Whole nonstrict direct-Phi edge 23 retains its genuine
coherence after arbitrary dependent index reclassification. -/
theorem nativeGK5ZTransportedEdge23_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedPhi2 f e g h k t ≪≫
      nativeGK5XEdge23 e g h k
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
      nativeGK5ZTransportedPhi3 f e g h k t := by
  simpa only [nativeGK5ZTransportedPhi2,
    nativeGK5ZTransportedPhi3, Iso.trans_assoc] using
    congrArg
      (fun iso => nativeGK5ZSourceIso f e g h k t ≪≫ iso)
      (nativeGK5YEdge23_whole e g h k
        (nativeGK5FTreeReindex f C t))

/-- Whole nonstrict direct-Phi edge 04 retains its genuine
coherence after arbitrary dependent index reclassification. -/
theorem nativeGK5ZTransportedEdge04_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedPhi0 f e g h k t ≪≫
      nativeGK5XEdge04 e g h k
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
      nativeGK5ZTransportedPhi4 f e g h k t := by
  simpa only [nativeGK5ZTransportedPhi0,
    nativeGK5ZTransportedPhi4, Iso.trans_assoc] using
    congrArg
      (fun iso => nativeGK5ZSourceIso f e g h k t ≪≫ iso)
      (nativeGK5YEdge04_whole e g h k
        (nativeGK5FTreeReindex f C t))

/-- Whole nonstrict direct-Phi edge 43 retains its genuine
coherence after arbitrary dependent index reclassification. -/
theorem nativeGK5ZTransportedEdge43_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedPhi4 f e g h k t ≪≫
      nativeGK5XEdge43 e g h k
        (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
      nativeGK5ZTransportedPhi3 f e g h k t := by
  simpa only [nativeGK5ZTransportedPhi4,
    nativeGK5ZTransportedPhi3, Iso.trans_assoc] using
    congrArg
      (fun iso => nativeGK5ZSourceIso f e g h k t ≪≫ iso)
      (nativeGK5YEdge43_whole e g h k
        (nativeGK5FTreeReindex f C t))

/-- All five WHOLE NatIso edge comparisons after full dependent
reclassification, bundled in the actual five-vertex pentagon. -/
theorem nativeGK5ZAllFiveEdges_reindex_whole
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    (nativeGK5ZTransportedPhi0 f e g h k t ≪≫
       nativeGK5XEdge01 e g h k
         (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
     nativeGK5ZTransportedPhi1 f e g h k t) ∧
    (nativeGK5ZTransportedPhi1 f e g h k t ≪≫
       nativeGK5XEdge12 e g h k
         (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
     nativeGK5ZTransportedPhi2 f e g h k t) ∧
    (nativeGK5ZTransportedPhi2 f e g h k t ≪≫
       nativeGK5XEdge23 e g h k
         (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
     nativeGK5ZTransportedPhi3 f e g h k t) ∧
    (nativeGK5ZTransportedPhi0 f e g h k t ≪≫
       nativeGK5XEdge04 e g h k
         (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
     nativeGK5ZTransportedPhi4 f e g h k t) ∧
    (nativeGK5ZTransportedPhi4 f e g h k t ≪≫
       nativeGK5XEdge43 e g h k
         (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t)) =
     nativeGK5ZTransportedPhi3 f e g h k t) := by
  exact ⟨nativeGK5ZTransportedEdge01_whole f e g h k t,
    nativeGK5ZTransportedEdge12_whole f e g h k t,
    nativeGK5ZTransportedEdge23_whole f e g h k t,
    nativeGK5ZTransportedEdge04_whole f e g h k t,
    nativeGK5ZTransportedEdge43_whole f e g h k t⟩

/-- Actual source-valued relative direct-Phi defect for the
reindexed whole NatIso 01 edge, not a strict equivalence record. -/
noncomputable def nativeGK5ZTransportedDefect01
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
          (fun x : I => h (f x)) (fun x : I => k (f x)) t) :=
  (nativeGK5ZTransportedPhi0 f e g h k t ≪≫
    nativeGK5XEdge01 e g h k
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))) ≪≫
    (nativeGK5ZTransportedPhi1 f e g h k t).symm

/-- No obstruction appears at the 01 actual transported
direct-Phi pentagon edge for ANY possibly noninjective f. -/
theorem nativeGK5ZTransportedDefect01_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect01 f e g h k t = Iso.refl _ := by
  unfold nativeGK5ZTransportedDefect01
  rw [nativeGK5ZTransportedEdge01_whole]
  simp only [Iso.self_symm_id]

/-- Actual source-valued relative direct-Phi defect for the
reindexed whole NatIso 12 edge, not a strict equivalence record. -/
noncomputable def nativeGK5ZTransportedDefect12
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
          (fun x : I => h (f x)) (fun x : I => k (f x)) t) :=
  (nativeGK5ZTransportedPhi1 f e g h k t ≪≫
    nativeGK5XEdge12 e g h k
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))) ≪≫
    (nativeGK5ZTransportedPhi2 f e g h k t).symm

/-- No obstruction appears at the 12 actual transported
direct-Phi pentagon edge for ANY possibly noninjective f. -/
theorem nativeGK5ZTransportedDefect12_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect12 f e g h k t = Iso.refl _ := by
  unfold nativeGK5ZTransportedDefect12
  rw [nativeGK5ZTransportedEdge12_whole]
  simp only [Iso.self_symm_id]

/-- Actual source-valued relative direct-Phi defect for the
reindexed whole NatIso 23 edge, not a strict equivalence record. -/
noncomputable def nativeGK5ZTransportedDefect23
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
          (fun x : I => h (f x)) (fun x : I => k (f x)) t) :=
  (nativeGK5ZTransportedPhi2 f e g h k t ≪≫
    nativeGK5XEdge23 e g h k
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))) ≪≫
    (nativeGK5ZTransportedPhi3 f e g h k t).symm

/-- No obstruction appears at the 23 actual transported
direct-Phi pentagon edge for ANY possibly noninjective f. -/
theorem nativeGK5ZTransportedDefect23_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect23 f e g h k t = Iso.refl _ := by
  unfold nativeGK5ZTransportedDefect23
  rw [nativeGK5ZTransportedEdge23_whole]
  simp only [Iso.self_symm_id]

/-- Actual source-valued relative direct-Phi defect for the
reindexed whole NatIso 04 edge, not a strict equivalence record. -/
noncomputable def nativeGK5ZTransportedDefect04
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
          (fun x : I => h (f x)) (fun x : I => k (f x)) t) :=
  (nativeGK5ZTransportedPhi0 f e g h k t ≪≫
    nativeGK5XEdge04 e g h k
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))) ≪≫
    (nativeGK5ZTransportedPhi4 f e g h k t).symm

/-- No obstruction appears at the 04 actual transported
direct-Phi pentagon edge for ANY possibly noninjective f. -/
theorem nativeGK5ZTransportedDefect04_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect04 f e g h k t = Iso.refl _ := by
  unfold nativeGK5ZTransportedDefect04
  rw [nativeGK5ZTransportedEdge04_whole]
  simp only [Iso.self_symm_id]

/-- Actual source-valued relative direct-Phi defect for the
reindexed whole NatIso 43 edge, not a strict equivalence record. -/
noncomputable def nativeGK5ZTransportedDefect43
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
        (fun x : I => h (f x)) (fun x : I => k (f x)) t) ≅
      nativeGK5DTreeComposite (C := fun x : I => G (f x))
      (nativeGK5XFourTree
        (fun x : I => e (f x)) (fun x : I => g (f x))
          (fun x : I => h (f x)) (fun x : I => k (f x)) t) :=
  (nativeGK5ZTransportedPhi4 f e g h k t ≪≫
    nativeGK5XEdge43 e g h k
      (nativeGK5DTreeComposite (nativeGK5FTreeReindex f C t))) ≪≫
    (nativeGK5ZTransportedPhi3 f e g h k t).symm

/-- No obstruction appears at the 43 actual transported
direct-Phi pentagon edge for ANY possibly noninjective f. -/
theorem nativeGK5ZTransportedDefect43_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect43 f e g h k t = Iso.refl _ := by
  unfold nativeGK5ZTransportedDefect43
  rw [nativeGK5ZTransportedEdge43_whole]
  simp only [Iso.self_symm_id]

/-- Main: every one of the FIVE genuinely reindexed,
source-transported direct-Phi relative pentagon edge obstructions
vanishes, without any injectivity or extra coherence hypothesis. -/
theorem nativeGK5ZAllFiveDefects_reindex_refl
    {i j : I}
    (t : NativeGK5DTypedTree (fun x : I => C (f x)) i j) :
    nativeGK5ZTransportedDefect01 f e g h k t = Iso.refl _ ∧
    nativeGK5ZTransportedDefect12 f e g h k t = Iso.refl _ ∧
    nativeGK5ZTransportedDefect23 f e g h k t = Iso.refl _ ∧
    nativeGK5ZTransportedDefect04 f e g h k t = Iso.refl _ ∧
    nativeGK5ZTransportedDefect43 f e g h k t = Iso.refl _ := by
  exact ⟨nativeGK5ZTransportedDefect01_refl f e g h k t,
    nativeGK5ZTransportedDefect12_refl f e g h k t,
    nativeGK5ZTransportedDefect23_refl f e g h k t,
    nativeGK5ZTransportedDefect04_refl f e g h k t,
    nativeGK5ZTransportedDefect43_refl f e g h k t⟩

#print axioms nativeGK5ZFourTree_reindex
#print axioms nativeGK5ZFourComposite_reindex
#print axioms nativeGK5ZSourceIso
#print axioms nativeGK5ZBracket0_reindex
#print axioms nativeGK5ZBracket1_reindex
#print axioms nativeGK5ZBracket2_reindex
#print axioms nativeGK5ZBracket3_reindex
#print axioms nativeGK5ZBracket4_reindex
#print axioms nativeGK5ZEdge01_reindex
#print axioms nativeGK5ZEdge12_reindex
#print axioms nativeGK5ZEdge23_reindex
#print axioms nativeGK5ZEdge04_reindex
#print axioms nativeGK5ZEdge43_reindex
#print axioms nativeGK5ZPullbackPentagon_whole
#print axioms nativeGK5ZPullbackPentagon_natTrans
#print axioms nativeGK5ZTransportedPhi0
#print axioms nativeGK5ZTransportedPhi1
#print axioms nativeGK5ZTransportedPhi2
#print axioms nativeGK5ZTransportedPhi3
#print axioms nativeGK5ZTransportedPhi4
#print axioms nativeGK5ZTransportedEdge01_whole
#print axioms nativeGK5ZTransportedEdge12_whole
#print axioms nativeGK5ZTransportedEdge23_whole
#print axioms nativeGK5ZTransportedEdge04_whole
#print axioms nativeGK5ZTransportedEdge43_whole
#print axioms nativeGK5ZAllFiveEdges_reindex_whole
#print axioms nativeGK5ZTransportedDefect01_refl
#print axioms nativeGK5ZTransportedDefect12_refl
#print axioms nativeGK5ZTransportedDefect23_refl
#print axioms nativeGK5ZTransportedDefect04_refl
#print axioms nativeGK5ZTransportedDefect43_refl
#print axioms nativeGK5ZAllFiveDefects_reindex_refl

end TypedIndexPentagon
end
end Kuu.F112.Physical
