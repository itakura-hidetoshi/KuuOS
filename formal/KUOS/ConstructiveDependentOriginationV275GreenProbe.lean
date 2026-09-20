import KUOS.DependentOriginationOrderedSectorCorrectionV2_75

namespace KUOS.DependentOriginationOrderedSectorCorrectionV2_75

def twoSectorData : SectorOrderData (Fin 2 → Nat) 2 where
  good := fun i n x => n ≤ x i
  weaken := by
    intro i m n x hmn hgood
    exact hmn.trans hgood

def twoSectorStep
    (i : Fin 2) (x y : Fin 2 → Nat) : Prop :=
  y = Function.update x i (x i + 1)

def twoSectorCorrector :
    OrderedSectorCorrector twoSectorData (fun _ => True) twoSectorStep 1 where
  correct := fun i x => Function.update x i (x i + 1)
  step := by
    intro i x
    rfl
  invariant := by
    intro i x hx
    trivial
  gain := by
    intro i x n hxinv hgood
    simp [twoSectorData]
    omega
  preserve_other := by
    intro i j m x hji hgood
    simpa [twoSectorData, Function.update, hji] using hgood

def schedule01 : List (Fin 2) := [0, 1]

def zeroState : Fin 2 → Nat := fun _ => 0

example :
    ∀ i, twoSectorData.good i 1
      (twoSectorCorrector.runSchedule schedule01 zeroState) := by
  apply twoSectorCorrector.runFullCycle_order schedule01
  · decide
  · trivial
  · intro i
    fin_cases i <;> simp [schedule01]
  · intro i
    simp [twoSectorData, zeroState]

end KUOS.DependentOriginationOrderedSectorCorrectionV2_75
