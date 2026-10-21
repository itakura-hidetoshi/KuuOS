import Kuu.F112.PolygonNativeF55TypedUnitCongruenceP62

/-!
# F112-P63 — independent F55 left/right typed context path actions

P62 defines a proof-sensitive, vertical-composition-compatible
congruence on native F55 free paths from the structurally unit-generated
sublanguage. The next task is to construct the actual contextual
actions on *all* nine raw proof constructors, at arbitrary source depths.

Both actions below are obtained by the Mathlib free-path universal
property (Paths.lift), so their vertical unit and associativity laws
are categorical theorems, not equations postulated on raw trees.

The raw context action maps each raw generating proof to the
genuine context-wrapped raw generating proof; it does NOT erase
nontrivial pentagon/square history, identify distinct source terms
from equal charges, or replace source witnesses by shadows.

We also prove that *every* syntactically unit-only proof necessarily
has identical typed raw F54 route endpoints, and that each left/right
context preserves the unit-only test. For genuine raw identity
generators, their contextual images satisfy P62's unit congruence,
although as free paths they remain nonempty.

Full transport of P62's congruence for arbitrary normalized
structural-unit compositions and the strict horizontal
interchange/associator remain separate proof obligations.
No Gray source, new axioms, sorry or admit.
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

/-- P62 unit-only raw syntax can never connect distinct native F54
route witnesses. This is a source-level fact of the nine-constructor
dependent grammar, NOT a consequence of matching shadow values. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_endpoints
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s),
      cell.unitOnly = true → r = s
  | _, _, .ident _, _ => rfl
  | _, _, .pentagon _ _ _ _, h => by cases h
  | _, _, .disjointSquare _ _, h => by cases h
  | _, _, .symm c, h => (c.unitOnly_endpoints h).symm
  | _, _, .trans c d, h =>
      (c.unitOnly_endpoints (Bool.and_elim_left h)).trans
        (d.unitOnly_endpoints (Bool.and_elim_right h))
  | _, _, .leftContext c later, h =>
      congrArg (fun z => KuuNativeF45Tree.DepthRotationRoute.leftContext z later)
        (c.unitOnly_endpoints h)
  | _, _, .rightContext earlier c, h =>
      congrArg (fun z => KuuNativeF45Tree.DepthRotationRoute.rightContext earlier z)
        (c.unitOnly_endpoints h)
  | _, _, .precompose prior c, h =>
      congrArg (fun z => KuuNativeF45Tree.DepthRotationRoute.trans prior z)
        (c.unitOnly_endpoints h)
  | _, _, .postcompose c suffix, h =>
      congrArg (fun z => KuuNativeF45Tree.DepthRotationRoute.trans z suffix)
        (c.unitOnly_endpoints h)

/-- Native F54 left context acts on *every original raw F55 edge*,
and extends strictly to their Mathlib free paths via Paths.lift.
Nothing is identified in the proof-relevant raw source. -/
def nativeF55LeftContextPathFunctor
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    NativeF55RawPathCategory first last ⥤
      NativeF55RawPathCategory
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later) :=
  CategoryTheory.Paths.lift {
    obj := fun vertex =>
      ⟨KuuNativeF45Tree.DepthRotationRoute.leftContext vertex.route later⟩
    map := fun {_r _s} raw =>
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext raw later).toNativeRawEdge.toPath
  }

/-- Native F54 right context similarly acts on ALL source generator
cells, even when the true first/last raw Nat depths differ. -/
def nativeF55RightContextPathFunctor
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc) :
    NativeF55RawPathCategory first last ⥤
      NativeF55RawPathCategory
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last) :=
  CategoryTheory.Paths.lift {
    obj := fun vertex =>
      ⟨KuuNativeF45Tree.DepthRotationRoute.rightContext earlier vertex.route⟩
    map := fun {_r _s} raw =>
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext earlier raw).toNativeRawEdge.toPath
  }

/-- On a single original proof generator, the left contextual
free-path functor returns the SAME raw proof witness with context
attached, not an arbitrary element of its selected shadow quotient. -/
@[simp] theorem nativeF55LeftContextPathFunctor_map_raw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    (nativeF55LeftContextPathFunctor first last later).map
      raw.toNativeRawEdge.toPath =
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
      raw later).toNativeRawEdge.toPath := by
  exact CategoryTheory.Paths.lift_toPath _ raw.toNativeRawEdge

@[simp] theorem nativeF55RightContextPathFunctor_map_raw
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    (nativeF55RightContextPathFunctor earlier first last).map
      raw.toNativeRawEdge.toPath =
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
      earlier raw).toNativeRawEdge.toPath := by
  exact CategoryTheory.Paths.lift_toPath _ raw.toNativeRawEdge

/-- Both contextual actions preserve exact VERTICAL composition of
arbitrary original proof-relevant free paths. -/
theorem nativeF55LeftContextPathFunctor_map_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    {u v w : NativeF55RawRouteVertex first last}
    (f : Quiver.Path u v) (g : Quiver.Path v w) :
    (nativeF55LeftContextPathFunctor first last later).map (f.comp g) =
      ((nativeF55LeftContextPathFunctor first last later).map f).comp
        ((nativeF55LeftContextPathFunctor first last later).map g) :=
  (nativeF55LeftContextPathFunctor first last later).map_comp f g

theorem nativeF55RightContextPathFunctor_map_comp
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    {u v w : NativeF55RawRouteVertex first last}
    (f : Quiver.Path u v) (g : Quiver.Path v w) :
    (nativeF55RightContextPathFunctor earlier first last).map (f.comp g) =
      ((nativeF55RightContextPathFunctor earlier first last).map f).comp
        ((nativeF55RightContextPathFunctor earlier first last).map g) :=
  (nativeF55RightContextPathFunctor earlier first last).map_comp f g

/-- The structural-unit predicate is preserved on the WHOLE raw
nine-constructor proof tree under left context (not merely identities). -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_leftContext
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.leftContext
       raw later).unitOnly = raw.unitOnly := rfl

theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_rightContext
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.rightContext
       earlier raw).unitOnly = raw.unitOnly := rfl

/-- The contextual image of a raw identity generator has length ONE
before passing to the P62 congruence. -/
theorem nativeF55LeftContextPathFunctor_ident_length
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ((nativeF55LeftContextPathFunctor first last later).map
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
         route).toNativeRawEdge.toPath).length = 1 := by
  rw [nativeF55LeftContextPathFunctor_map_raw]
  rfl

/-- The same genuine raw-generator noncollapse holds on the right. -/
theorem nativeF55RightContextPathFunctor_ident_length
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ((nativeF55RightContextPathFunctor earlier first last).map
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
         route).toNativeRawEdge.toPath).length = 1 := by
  rw [nativeF55RightContextPathFunctor_map_raw]
  rfl

/-- Exact P62 generator compatibility for the LEFT raw identity.
The identity image is not a literal empty path; it is RELATED to one
by the physically meaningful typed structural-unit relation. -/
theorem nativeF55LeftContextPathFunctor_ident_related
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55UnitPathRel
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      ((nativeF55LeftContextPathFunctor first last later).map
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route).toNativeRawEdge.toPath)
      (Quiver.Path.nil :
        Quiver.Path
          (⟨KuuNativeF45Tree.DepthRotationRoute.leftContext route later⟩ :
            NativeF55RawRouteVertex
              (KuuNativeF45Tree.node first later)
              (KuuNativeF45Tree.node last later))
          ⟨KuuNativeF45Tree.DepthRotationRoute.leftContext route later⟩) := by
  rw [nativeF55LeftContextPathFunctor_map_raw]
  exact NativeF55UnitPathRel.structuralUnit
    (.leftContext route later) (.leftContext (.ident route) later) rfl

/-- Exact P62 generator compatibility for the RIGHT raw identity. -/
theorem nativeF55RightContextPathFunctor_ident_related
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55UnitPathRel
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      ((nativeF55RightContextPathFunctor earlier first last).map
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident route).toNativeRawEdge.toPath)
      (Quiver.Path.nil :
        Quiver.Path
          (⟨KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route⟩ :
            NativeF55RawRouteVertex
              (KuuNativeF45Tree.node earlier first)
              (KuuNativeF45Tree.node earlier last))
          ⟨KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route⟩) := by
  rw [nativeF55RightContextPathFunctor_map_raw]
  exact NativeF55UnitPathRel.structuralUnit
    (.rightContext earlier route) (.rightContext earlier (.ident route)) rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_endpoints
#print axioms nativeF55LeftContextPathFunctor
#print axioms nativeF55RightContextPathFunctor
#print axioms nativeF55LeftContextPathFunctor_map_raw
#print axioms nativeF55RightContextPathFunctor_map_raw
#print axioms nativeF55LeftContextPathFunctor_map_comp
#print axioms nativeF55RightContextPathFunctor_map_comp
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_leftContext
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly_rightContext
#print axioms nativeF55LeftContextPathFunctor_ident_length
#print axioms nativeF55RightContextPathFunctor_ident_length
#print axioms nativeF55LeftContextPathFunctor_ident_related
#print axioms nativeF55RightContextPathFunctor_ident_related

end
end Kuu.F112.Physical
