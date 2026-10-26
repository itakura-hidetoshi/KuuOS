import Kuu.F112.PolygonNativeC60BridgedHigherWhiskering

/-!
# F112-P94D3BT — strict bridge-choice reflection and exact BH replacement

BS builds a genuinely two-input, but bridge-dependent, raw sixteen-
dimensional comparison: for full dependent comparison cells q : a => b
and r : c => d, any bridge k : a => c yields q^{-1}; k; r : b => d.

BT strengthens BS's SUFFICIENT bridge-choice replacement criterion
to a NECESSARY-AND-SUFFICIENT theorem, for EVERY SELECTED strict
Kuu parallel relation, not just the no-extra-relations presentation.

The selected strict Kuu inverse laws prove that conjugation by the
actual q and r is an EQUIVALENCE between the FULL source and target
strict hom sets. Therefore two different raw bridges have the same
strict-glued output IF AND ONLY IF their strict arrows are equal,
IF AND ONLY IF the two raw bridges belong to the selected compositional
Kuu replacement closure. The reverse direction is genuine cancellation
by strictly invertible original proof images, not Peiffer/observer
cancellation and not raw16D term cancellation.

This is the exact BH-style compatibility criterion for BR/BS's
partial bridge-dependent presentation. All lower original 15D/14D
dependent endpoints remain typed. The result does not construct a
global two-variable BB object operation; BG and BI unconditional
middle-four for a genuinely nondegenerate total whiskering remain open.

The genuine C60 AU naturality boundary specializes the theorem at an
actual pair of distinct original physical 15D sources, in the already
DECLARED BC context-closed Kuu higher comparison presentation.
No new axioms, sorry, admit, Gray, or 107-root changes.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Core theorem: conjugation by the TWO actual dependent raw 16D
comparisons becomes a bijection of complete selected strict hom sets.
The strict inverse laws are proven in AZ; no quotient by observation. -/
def nativeC60BTBridgeHomEquiv {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T)
    (q r : (nativeC60AXNext L T).Total) :
    ((nativeC60AZStrictProject T R).obj ⟨q.1.1⟩ ⟶
        (nativeC60AZStrictProject T R).obj ⟨r.1.1⟩) ≃
      ((nativeC60AZStrictProject T R).obj ⟨q.1.2⟩ ⟶
        (nativeC60AZStrictProject T R).obj ⟨r.1.2⟩) where
  toFun k :=
    nativeC60AZStrictStep T R (.symm q.2) ≫ k ≫
      nativeC60AZStrictStep T R r.2
  invFun t :=
    nativeC60AZStrictStep T R q.2 ≫ t ≫
      nativeC60AZStrictStep T R (.symm r.2)
  left_inv := by
    intro k
    change nativeC60AZStrictStep T R q.2 ≫
      (nativeC60AZStrictStep T R (.symm q.2) ≫ k ≫
        nativeC60AZStrictStep T R r.2) ≫
          nativeC60AZStrictStep T R (.symm r.2) = k
    simp only [Category.assoc, nativeC60AZStrictStep_inv_left,
      Category.id_comp, Category.comp_id]
    rw [← Category.assoc, nativeC60AZStrictStep_inv_left T R q.2,
      Category.id_comp]
  right_inv := by
    intro t
    change nativeC60AZStrictStep T R (.symm q.2) ≫
      (nativeC60AZStrictStep T R q.2 ≫ t ≫
        nativeC60AZStrictStep T R (.symm r.2)) ≫
          nativeC60AZStrictStep T R r.2 = t
    simp only [Category.assoc, nativeC60AZStrictStep_inv_right,
      Category.id_comp, Category.comp_id]
    rw [← Category.assoc, nativeC60AZStrictStep_inv_right T R q.2,
      Category.id_comp]

/-- The genuinely two-input BS bridge operation interpreted as a
COMPLETE selected strict arrow, without choosing raw representatives
of an already strict hom. -/
def nativeC60BTStrictGluing {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T)
    (q r : (nativeC60AXNext L T).Total)
    (bridge : NativeC60AXStep T q.1.1 r.1.1) :
    (nativeC60AZStrictProject T R).obj ⟨q.1.2⟩ ⟶
      (nativeC60AZStrictProject T R).obj ⟨r.1.2⟩ :=
  nativeC60BTBridgeHomEquiv T R q r
    (nativeC60AZStrictStep T R bridge)

/-- The strict map really IS the BS raw higher pasting, rather than
an independently imposed or observed horizontal operation. -/
theorem nativeC60BTStrictGluing_spec {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T)
    (q r : (nativeC60AXNext L T).Total)
    (bridge : NativeC60AXStep T q.1.1 r.1.1) :
    nativeC60BTStrictGluing T R q r bridge =
      nativeC60AZStrictStep T R
        (.trans (.trans (.symm q.2) bridge) r.2) := by
  change nativeC60AZStrictStep T R (.symm q.2) ≫
      nativeC60AZStrictStep T R bridge ≫
      nativeC60AZStrictStep T R r.2 =
    nativeC60AZStrictStep T R (.trans (.trans (.symm q.2) bridge) r.2)
  simp only [nativeC60AZStrictStep_comp, Category.assoc]

/-- Exact REFLECTION of bridge equality: strict-glued comparison
equality is equivalent to selected strict Kuu bridge equality.
BS previously proved only the forward propagation direction. -/
theorem nativeC60BTStrictGluing_eq_iff {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T)
    (q r : (nativeC60AXNext L T).Total)
    (bridge bridge' : NativeC60AXStep T q.1.1 r.1.1) :
    nativeC60BTStrictGluing T R q r bridge =
        nativeC60BTStrictGluing T R q r bridge' ↔
      nativeC60AZStrictStep T R bridge =
        nativeC60AZStrictStep T R bridge' := by
  constructor
  · intro h
    exact (nativeC60BTBridgeHomEquiv T R q r).injective h
  · intro h
    exact congrArg (nativeC60BTBridgeHomEquiv T R q r) h

/-- COMPLETE necessary-and-sufficient BH-like criterion relative to
the ACTUALLY SELECTED compositional strict Kuu replacement relation.
No identification of raw free sixteen-dimensional terms is asserted. -/
theorem nativeC60BTStrictGluing_eq_iff_replaceable
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L) (R : NativeC60AZParallelRelation T)
    (q r : (nativeC60AXNext L T).Total)
    (bridge bridge' : NativeC60AXStep T q.1.1 r.1.1) :
    nativeC60BTStrictGluing T R q r bridge =
        nativeC60BTStrictGluing T R q r bridge' ↔
      Kuu.Replaceable (nativeC60AZStrictRelations T R)
        (nativeC60AZRawArrow T bridge)
        (nativeC60AZRawArrow T bridge') :=
  (nativeC60BTStrictGluing_eq_iff T R q r bridge bridge').trans
    (nativeC60AZStrictStep_exact T R bridge bridge')

/-- For the BS raw-gluing term, exact reflectivity holds in ANY
selected strict quotient of the BC context-closed signature, not only
the no-extra-relations choice used by BG/BH/BI. -/
theorem nativeC60BTRawGluing_strict_eq_iff_replaceable
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (q r : NativeC60BGRawArrowBundle S F)
    (bridge bridge' : NativeC60AXStep (nativeC60BCClosedSignature S F)
        q.1.1 r.1.1) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BSGluedStep S F ⟨q, r, bridge⟩) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BSGluedStep S F ⟨q, r, bridge'⟩) ↔
      Kuu.Replaceable
        (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F) R)
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) bridge)
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) bridge') := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
      (.trans (.trans (.symm q.2) bridge) r.2) =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
      (.trans (.trans (.symm q.2) bridge') r.2) ↔ _
  rw [← nativeC60BTStrictGluing_spec (nativeC60BCClosedSignature S F) R
      q r bridge,
    ← nativeC60BTStrictGluing_spec (nativeC60BCClosedSignature S F) R
      q r bridge']
  exact nativeC60BTStrictGluing_eq_iff_replaceable
    (nativeC60BCClosedSignature S F) R q r bridge bridge'

/-- The no-extra-relations specialization ties BS's partial gluing
directly to the SAME strict replacement closure used by BH.
All four original dependent endpoints remain unchanged. -/
theorem nativeC60BTNoRelations_bridge_choice_exact
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F)
    (bridge bridge' : NativeC60AXStep (nativeC60BCClosedSignature S F)
        q.1.1 r.1.1) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BSGluedStep S F ⟨q, r, bridge⟩) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BSGluedStep S F ⟨q, r, bridge'⟩) ↔
      Kuu.Replaceable
        (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)))
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) bridge)
        (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) bridge') :=
  nativeC60BTRawGluing_strict_eq_iff_replaceable
    S F (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    q r bridge bridge'

section OriginalC60

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

/-- ACTUAL C60 AU source/target original 15D witnesses (BS's
nonidentical pair). All new strict 16D classes are measured on their
already-declared typed comparison, never on a scalar proxy. -/
def nativeK5BTPhysicalNaturalityBridgeEquiv
    (W : NativeK5StructuralThirteenCell p U V) :
    ((nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BSNaturalityFirst W).1.1⟩ ⟶
      (nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BSNaturalitySecond W).1.1⟩) ≃
    ((nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BSNaturalityFirst W).1.2⟩ ⟶
      (nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BSNaturalitySecond W).1.2⟩) :=
  nativeC60BTBridgeHomEquiv
    (nativeK5BCSignature W) (nativeC60AZNoRelations (nativeK5BCSignature W))
    (nativeK5BSNaturalityFirst W) (nativeK5BSNaturalitySecond W)

/-- Same exact replacement reflection for TWO actual distinct
physical AU 15D proof objects with matching original 14D boundaries.
The named sixteen-dimensional bridge is independently supplied
in the already-explicit BC presentation (not newly fabricated). -/
theorem nativeK5BTPhysicalNaturality_choice_exact
    (W : NativeK5StructuralThirteenCell p U V)
    (bridge bridge' : NativeC60AXStep (nativeK5BCSignature W)
      (nativeK5BSNaturalityFirst W).1.1
      (nativeK5BSNaturalitySecond W).1.1) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeC60BSGluedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          ⟨nativeK5BSNaturalityFirst W, nativeK5BSNaturalitySecond W,
            bridge⟩) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeC60BSGluedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          ⟨nativeK5BSNaturalityFirst W, nativeK5BSNaturalitySecond W,
            bridge'⟩) ↔
      Kuu.Replaceable
        (nativeC60AZStrictRelations (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W)))
        (nativeC60AZRawArrow (nativeK5BCSignature W) bridge)
        (nativeC60AZRawArrow (nativeK5BCSignature W) bridge') :=
  nativeC60BTNoRelations_bridge_choice_exact
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5BSNaturalityFirst W) (nativeK5BSNaturalitySecond W)
    bridge bridge'

end OriginalC60

#print axioms nativeC60BTBridgeHomEquiv
#print axioms nativeC60BTStrictGluing
#print axioms nativeC60BTStrictGluing_spec
#print axioms nativeC60BTStrictGluing_eq_iff
#print axioms nativeC60BTStrictGluing_eq_iff_replaceable
#print axioms nativeC60BTRawGluing_strict_eq_iff_replaceable
#print axioms nativeC60BTNoRelations_bridge_choice_exact
#print axioms nativeK5BTPhysicalNaturalityBridgeEquiv
#print axioms nativeK5BTPhysicalNaturality_choice_exact

end
end Kuu.F112.Physical
