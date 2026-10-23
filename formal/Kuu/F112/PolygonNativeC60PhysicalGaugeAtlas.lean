import Kuu.F112.PolygonRawLoop
import Mathlib.Tactic

/-!
# F112 — native C60 physical gauge atlas, not a graph substitute for coherence

The genuine C60 physical geometry (60 dart vertices, 90 physical edges,
32 original faces, 360 incidence flags) is retained EXACTLY.  The
forward mathematical interpretation is a *gauge field* on the actual
182-site incidence source, not a graph equality or a fabricated edge.

A local gauge potential is a function on the actual sites.  Its
coboundary shifts the additive incidence connection.  Raw F69
proof-relevant zigzags retain every original forward/reverse leg;
gauge holonomy telescopes under a local frame change.

The curvature comparing a REAL physical two-step flag with its
different actual diagonal, and the raw 10/12-leg boundaries of all
32 original faces, are gauge-invariant.  The raw words are NOT thereby
identified, and their curvature is NOT asserted to vanish.

No old KUOS/Gray imports, no graph-derived higher filler, no sorry,
admit, added logical axiom or removal of existing source theorems.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u
variable {A : Type u} [AddCommGroup A]

/-- A gauge field on the ACTUAL physical incidence order.  A
vertex-to-face diagonal and a vertex-to-edge-to-face composite
are different source paths; no graph representation identifies them. -/
abbrev NativeC60IncidenceGaugeField (A : Type u) :=
  (s t : Site) → s ≤ t → A

/-- A local gauge/choice of presentation at every genuine C60 site. -/
abbrev NativeC60LocalGauge (A : Type u) := Site → A

/-- A pure change of local frame: the exact additive coboundary. -/
def nativeC60GaugeCoboundary (phi : NativeC60LocalGauge A) :
    NativeC60IncidenceGaugeField A :=
  fun s t _ => phi t - phi s

/-- The connection's physical site incidence is not changed. -/
def nativeC60GaugeTransform
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A) :
    NativeC60IncidenceGaugeField A :=
  fun s t h => field s t h + nativeC60GaugeCoboundary phi s t h

theorem nativeC60GaugeTransform_zero
    (field : NativeC60IncidenceGaugeField A) :
    nativeC60GaugeTransform field (fun _ => 0) = field := by
  funext s t h
  simp [nativeC60GaugeTransform, nativeC60GaugeCoboundary]

/-- Two successive changes of charts compose as an additive gauge.
This is a genuine group action, not a graph-path identification. -/
theorem nativeC60GaugeTransform_comp
    (field : NativeC60IncidenceGaugeField A)
    (phi psi : NativeC60LocalGauge A) :
    nativeC60GaugeTransform (nativeC60GaugeTransform field phi) psi =
      nativeC60GaugeTransform field (fun s => phi s + psi s) := by
  funext s t h
  dsimp [nativeC60GaugeTransform, nativeC60GaugeCoboundary]
  abel

/-- Integral of an arbitrary ORIGINAL, proof-relevant C60 raw zigzag.
Reverse legs are signed but never erased from the source syntax. -/
def nativeC60GaugeIntegral
    (field : NativeC60IncidenceGaugeField A) {s t : Site} :
    Zigzag s t → A
  | .nil _ => 0
  | .forward h rest =>
      field _ _ h + nativeC60GaugeIntegral field rest
  | .backward h rest =>
      -(field _ _ h) + nativeC60GaugeIntegral field rest

/-- Gauge integration preserves typed ORIGINAL path concatenation. -/
theorem nativeC60GaugeIntegral_append
    (field : NativeC60IncidenceGaugeField A)
    {s t u : Site} (p : Zigzag s t) (q : Zigzag t u) :
    nativeC60GaugeIntegral field (append p q) =
      nativeC60GaugeIntegral field p + nativeC60GaugeIntegral field q := by
  induction p with
  | nil _ =>
      simp [append, nativeC60GaugeIntegral]
  | forward h rest ih =>
      simp only [append, nativeC60GaugeIntegral]
      rw [ih]
      abel
  | backward h rest ih =>
      simp only [append, nativeC60GaugeIntegral]
      rw [ih]
      abel

/-- Exact gauge covariance along EVERY actual raw F69 zigzag:
the only correction is the terminal minus initial frame potential.
This follows by proof-relevant induction over all forward/reverse legs. -/
theorem nativeC60GaugeIntegral_transform
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    {s t : Site} (path : Zigzag s t) :
    nativeC60GaugeIntegral (nativeC60GaugeTransform field phi) path =
      nativeC60GaugeIntegral field path + (phi t - phi s) := by
  induction path with
  | nil _ =>
      simp [nativeC60GaugeIntegral]
  | forward h rest ih =>
      simp only [nativeC60GaugeIntegral]
      rw [ih]
      dsimp [nativeC60GaugeTransform, nativeC60GaugeCoboundary]
      abel
  | backward h rest ih =>
      simp only [nativeC60GaugeIntegral]
      rw [ih]
      dsimp [nativeC60GaugeTransform, nativeC60GaugeCoboundary]
      abel

/-- A genuine closed C60 raw path has gauge-invariant holonomy,
even if its source proof-term is nontrivially different from nil. -/
theorem nativeC60GaugeIntegral_closed_invariant
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    {s : Site} (path : Zigzag s s) :
    nativeC60GaugeIntegral (nativeC60GaugeTransform field phi) path =
      nativeC60GaugeIntegral field path := by
  rw [nativeC60GaugeIntegral_transform]
  simp

/-- Original 360 physical dart-edge-face flags: their two-step
and one-step incidences are distinct raw witnesses.  The
curvature is the difference of their actual gauge-integrated routes. -/
def nativeC60FlagGaugeCurvature
    (field : NativeC60IncidenceGaugeField A)
    (e : Edge) (endpoint faceSide : Bool) : A :=
  nativeC60GaugeIntegral field (flagRawTwoStep e endpoint faceSide) -
    nativeC60GaugeIntegral field (flagRawDiagonal e endpoint faceSide)

/-- The genuine C60 two-step-versus-diagonal curvature survives
EVERY change of local gauge, without equating the raw paths. -/
theorem nativeC60FlagGaugeCurvature_invariant
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (e : Edge) (endpoint faceSide : Bool) :
    nativeC60FlagGaugeCurvature
        (nativeC60GaugeTransform field phi) e endpoint faceSide =
      nativeC60FlagGaugeCurvature field e endpoint faceSide := by
  unfold nativeC60FlagGaugeCurvature
  rw [nativeC60GaugeIntegral_transform,
    nativeC60GaugeIntegral_transform]
  abel

/-- Every REAL C60 polygon is represented by the original typed
10/12-leg F69 loop, never a new square or abstract graph face. -/
def nativeC60FaceGaugeCurvature
    (field : NativeC60IncidenceGaugeField A)
    (p : Polygon) : A :=
  nativeC60GaugeIntegral field (polygonRawLoop p)

theorem nativeC60FaceGaugeCurvature_invariant
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (p : Polygon) :
    nativeC60FaceGaugeCurvature
        (nativeC60GaugeTransform field phi) p =
      nativeC60FaceGaugeCurvature field p :=
  nativeC60GaugeIntegral_closed_invariant field phi (polygonRawLoop p)

/-- Nonzero genuine physical curvature is NOT removable by
changing representation.  In particular, a gauge is not a
license to declare arbitrary nonflat C60 boundary data flat. -/
theorem nativeC60FaceGaugeCurvature_no_flat_gauge
    (field : NativeC60IncidenceGaugeField A)
    (p : Polygon)
    (hcurv : nativeC60FaceGaugeCurvature field p ≠ 0)
    (phi : NativeC60LocalGauge A) :
    nativeC60FaceGaugeCurvature
      (nativeC60GaugeTransform field phi) p ≠ 0 := by
  rw [nativeC60FaceGaugeCurvature_invariant]
  exact hcurv

/-- Independent of original graph presentations, the
gauge orbit is the exact equivalence on genuinely typed
physical incidence fields, generated by real local chart changes. -/
def nativeC60GaugeEquivalent
    (field next : NativeC60IncidenceGaugeField A) : Prop :=
  ∃ phi : NativeC60LocalGauge A,
    next = nativeC60GaugeTransform field phi

theorem nativeC60GaugeEquivalent_refl
    (field : NativeC60IncidenceGaugeField A) :
    nativeC60GaugeEquivalent field field := by
  refine ⟨fun _ => 0, ?_⟩
  exact (nativeC60GaugeTransform_zero field).symm

theorem nativeC60GaugeEquivalent_symm
    {field next : NativeC60IncidenceGaugeField A}
    (h : nativeC60GaugeEquivalent field next) :
    nativeC60GaugeEquivalent next field := by
  rcases h with ⟨phi, rfl⟩
  refine ⟨fun s => -phi s, ?_⟩
  funext s t hst
  dsimp [nativeC60GaugeTransform, nativeC60GaugeCoboundary]
  abel

theorem nativeC60GaugeEquivalent_trans
    {field next last : NativeC60IncidenceGaugeField A}
    (hfn : nativeC60GaugeEquivalent field next)
    (hnl : nativeC60GaugeEquivalent next last) :
    nativeC60GaugeEquivalent field last := by
  rcases hfn with ⟨phi, rfl⟩
  rcases hnl with ⟨psi, rfl⟩
  refine ⟨fun s => phi s + psi s, ?_⟩
  exact (nativeC60GaugeTransform_comp field phi psi).symm

/-- Genuine gauge classes, not graph-connected-component classes. -/
def nativeC60GaugeSetoid : Setoid (NativeC60IncidenceGaugeField A) where
  r := nativeC60GaugeEquivalent
  iseqv := ⟨nativeC60GaugeEquivalent_refl,
    fun _ _ => nativeC60GaugeEquivalent_symm,
    fun _ _ _ => nativeC60GaugeEquivalent_trans⟩

abbrev NativeC60GaugeClasses (A : Type u) [AddCommGroup A] :=
  Quotient (nativeC60GaugeSetoid (A := A))

/-- The curvature of EACH genuine original polygon descends to
gauge classes: original C60 nonflat holonomy is retained. -/
def nativeC60GaugeClassFaceCurvature (p : Polygon) :
    NativeC60GaugeClasses A → A :=
  Quotient.lift
    (fun field => nativeC60FaceGaugeCurvature field p)
    (by
      intro field next h
      rcases h with ⟨phi, rfl⟩
      exact (nativeC60FaceGaugeCurvature_invariant field phi p).symm)

/-- The independent original face readout is invariant under
any presentation-equivalent gauge field representative. -/
theorem nativeC60GaugeClassFaceCurvature_spec
    (field : NativeC60IncidenceGaugeField A)
    (p : Polygon) :
    nativeC60GaugeClassFaceCurvature p
      (Quotient.mk (nativeC60GaugeSetoid (A := A)) field) =
        nativeC60FaceGaugeCurvature field p := rfl

#print axioms nativeC60GaugeTransform_comp
#print axioms nativeC60GaugeIntegral_append
#print axioms nativeC60GaugeIntegral_transform
#print axioms nativeC60GaugeIntegral_closed_invariant
#print axioms nativeC60FlagGaugeCurvature_invariant
#print axioms nativeC60FaceGaugeCurvature_invariant
#print axioms nativeC60FaceGaugeCurvature_no_flat_gauge
#print axioms nativeC60GaugeEquivalent_refl
#print axioms nativeC60GaugeEquivalent_symm
#print axioms nativeC60GaugeEquivalent_trans
#print axioms nativeC60GaugeClassFaceCurvature
#print axioms nativeC60GaugeClassFaceCurvature_spec

end
end Kuu.F112.Physical
