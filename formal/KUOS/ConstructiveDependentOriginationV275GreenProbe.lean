import KUOS.DependentOriginationOrderedSectorCorrectionV2_75

namespace KUOS.DependentOriginationOrderedSectorCorrectionV2_75

def twoSectorData : SectorOrderData (Fin 2 → Nat) 2 where
  good := fun i n x => n ≤ x i
  weaken := by
    intro i m n x hmn hgood
    exact hmn.trans hgood

def bumpSector (i : Fin 2) (x : Fin 2 → Nat) : Fin 2 → Nat :=
  fun j => if j = i then x j + 1 else x j

def twoSectorStep
    (i : Fin 2) (x y : Fin 2 → Nat) : Prop :=
  y = bumpSector i x

def twoSectorCorrector :
    OrderedSectorCorrector twoSectorData (fun _ => True) twoSectorStep 1 where
  correct := bumpSector
  step := by
    intro i x
    rfl
  invariant := by
    intro i x hx
    trivial
  gain := by
    intro i x n hxinv hgood
    change n ≤ x i at hgood
    change n + 1 ≤ bumpSector i x i
    simp [bumpSector]
    omega
  preserve_other := by
    intro i j m x hji hgood
    change m ≤ x j at hgood
    change m ≤ bumpSector i x j
    simpa [bumpSector, hji] using hgood

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
