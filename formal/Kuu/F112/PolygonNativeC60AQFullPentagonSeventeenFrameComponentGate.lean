import Kuu.F112.PolygonNativeC60AQFullPentagonSeventeenExactFiberGate

/-!
# F112-P94D3FE — genuine 17D frame components and finite AQ tree fibers

The actual DR seventeen-dimensional frame is a dependent map on
original proof-carrying 16D objects and raw 16D Hom data. We expose
TWO honest sufficient hypotheses for injectivity of this frame:
injectivity on its original lower objects and injectivity on each
original dependent Hom fiber. A general C60 frame is not asserted to
satisfy these hypotheses.

The exact finite-word result of FE converts these local conditions
into injectivity on all actual 17D context objects, hence on the
NONTRIVIAL original reflexive associator 18D code family.

For each genuine finite AQ tree, equality of original transported
reflexive associator full 18D codes and membership of its original
signed two-letter defect in DV's UNQUOTIENTED kernel are each
equivalent to equality of the actual 17D context objects. This
is not a result about all arbitrary original 18D generator codes,
nor an unjustified physical 19D filler.

All original lower Type-valued witnesses, independent Kuu/strict Kuu
boundaries, 107 roots, DS no-go and no-Gray rule are retained.
No new axioms, sorry or admit. Append-only, tighten-only, same root.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section ActualFrameComponents

/-- A dependent C60 frame is injective on full proof-carrying
objects if its actual object map is injective and every onCell
map is injective on its exact original dependent Hom fiber.
This is a SUFFICIENT condition, not an assertion that every
frame is faithful. -/
theorem nativeC60FEFrame_mapTotal_injective
    {L : NativeC60AXLayer.{u}}
    (C : NativeC60BCFrame L)
    (hobj : Function.Injective C.onObj)
    (hcell : ∀ {a b : L.Obj},
      Function.Injective (fun f : L.Hom a b => C.onCell f)) :
    Function.Injective C.mapTotal := by
  intro x y h
  rcases x with ⟨⟨a, b⟩, f⟩
  rcases y with ⟨⟨a', b'⟩, g⟩
  have ha : a = a' :=
    hobj (congrArg (fun z : L.Total => z.1.1) h)
  have hb : b = b' :=
    hobj (congrArg (fun z : L.Total => z.1.2) h)
  subst a'
  subst b'
  have hfg : C.onCell f = C.onCell g :=
    eq_of_heq (Sigma.mk.inj h).2
  have hfg' : f = g := hcell hfg
  subst g
  rfl

end ActualFrameComponents

section ActualSeventeenFrameComponentGates

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Two ACTUAL DR singleton frame component injectivity conditions
suffice for injectivity of EVERY finite 17D object context.
The onCell gate is about the full raw16D typed path, not its BV
holonomy, scalar charge, parity, or a strict quotient. -/
theorem nativeC60FEAllSeventeenContexts_injective_of_frame_parts
    (hobj : ∀ side : Bool,
      Function.Injective (nativeC60DRSeventeenFrame S F side).onObj)
    (hcell : ∀ (side : Bool)
      {a b : (nativeC60DQSeventeenLayer S F).Obj},
        Function.Injective (fun p :
          (nativeC60DQSeventeenLayer S F).Hom a b =>
          (nativeC60DRSeventeenFrame S F side).onCell p)) :
    ∀ word : List Bool,
      Function.Injective (nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word) := by
  apply (nativeC60FEAllBCContexts_injective_iff_singletons
    (nativeC60DRSeventeenFrame S F)).mpr
  constructor
  · exact nativeC60FEFrame_mapTotal_injective
      (nativeC60DRSeventeenFrame S F false)
      (hobj false) (fun {a b} => hcell false (a := a) (b := b))
  · exact nativeC60FEFrame_mapTotal_injective
      (nativeC60DRSeventeenFrame S F true)
      (hobj true) (fun {a b} => hcell true (a := a) (b := b))

/-- A concrete sufficient condition for full original 18D CODE
injectivity ON THE GENUINE REFLEXIVE-ASSOCIATOR FAMILY, not a
blanket claim for arbitrary whiskered 18D generators. -/
theorem nativeC60FEAllAssocReflCodes_injective_of_frame_parts
    (hobj : ∀ side : Bool,
      Function.Injective (nativeC60DRSeventeenFrame S F side).onObj)
    (hcell : ∀ (side : Bool)
      {a b : (nativeC60DQSeventeenLayer S F).Obj},
        Function.Injective (fun p :
          (nativeC60DQSeventeenLayer S F).Hom a b =>
          (nativeC60DRSeventeenFrame S F side).onCell p)) :
    ∀ word : List Bool,
      Function.Injective
        (fun a : (nativeC60DQSeventeenLayer S F).Total =>
          nativeC60DVTransportCompleteCode S F word
            (nativeC60FDAssocReflCode S F a)) := by
  intro word
  exact (nativeC60FEAssocReflCodes_injective_iff_context
    S F word).mpr
      (nativeC60FEAllSeventeenContexts_injective_of_frame_parts
        S F hobj hcell word)

/-- Genuine physical finite AQ trees: equality of transported fully
dependent ORIGINAL 18D reflexivity associator codes is EXACTLY the
fiber equality of the ACTUAL context word (no quotient). -/
theorem nativeC60FEActualTree_assocRefl_collision_iff
    (tree : NativeK5DOContextTree)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord tree)
        (nativeC60FDAssocReflCode S F a) =
      nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord tree)
        (nativeC60FDAssocReflCode S F b) ↔
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) a =
        nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) b :=
  nativeC60FEAssocReflCode_collision_iff S F
    (nativeK5DOTreeWord tree) a b

/-- Exactly the SAME physical finite AQ tree collision is detected
by membership of an ORIGINAL signed two-letter noncommutative
difference in the true unquotiented complete DV FreeGroup kernel. -/
theorem nativeC60FEActualTree_assocRefl_kernel_iff
    (tree : NativeK5DOContextTree)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60FCCodeFiberDefect S F
        (nativeC60FDAssocReflCode S F a)
        (nativeC60FDAssocReflCode S F b) ∈
      (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord tree)).ker ↔
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) a =
        nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) b :=
  nativeC60FEAssocReflDefect_mem_kernel_iff S F
    (nativeK5DOTreeWord tree) a b

/-- Genuine chronological AQ regrouping preserves the exact
original reflexivity-associator fiber collision criterion.
No hidden identification of distinct raw higher paths. -/
theorem nativeC60FEActualTree_assocRefl_refinement
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    (nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord left)
        (nativeC60FDAssocReflCode S F a) =
      nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord left)
        (nativeC60FDAssocReflCode S F b)) ↔
    (nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord right)
        (nativeC60FDAssocReflCode S F a) =
      nativeC60DVTransportCompleteCode S F (nativeK5DOTreeWord right)
        (nativeC60FDAssocReflCode S F b)) := by
  rw [nativeK5DOTreeWord_eq_of_steps_eq hsteps]

end ActualSeventeenFrameComponentGates

#print axioms nativeC60FEFrame_mapTotal_injective
#print axioms nativeC60FEAllSeventeenContexts_injective_of_frame_parts
#print axioms nativeC60FEAllAssocReflCodes_injective_of_frame_parts
#print axioms nativeC60FEActualTree_assocRefl_collision_iff
#print axioms nativeC60FEActualTree_assocRefl_kernel_iff
#print axioms nativeC60FEActualTree_assocRefl_refinement

end
end Kuu.F112.Physical
