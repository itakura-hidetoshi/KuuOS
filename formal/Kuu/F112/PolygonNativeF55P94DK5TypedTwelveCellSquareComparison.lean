import Kuu.F112.PolygonNativeF55P94DK5ElevenCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AI — original source-dependent Type-valued TWELVE-cell

Construct an explicit conservative TWELVE-cell grammar on original
ELEVEN-cell witnesses at their exact dependent TEN-cell boundaries:
11D associativity, units, inverses, two-sided 11D vertical congruence,
11D symmetry congruence, original 10D/9D/8D whiskering and inversion.

Every conservative 12D generator preserves the chosen universal
FREE-GROUP history of original 11D proof terms AND coarse integer
square count. The two truly typed 11D paths of the primitive
11D squareExchange have unequal free histories, hence NO filler in
the named conservative 12D presentation.

A new INDEPENDENT 12D Type-valued squareExchange is adjoined with
closure under original 11D/10D/9D/8D congruences. It gives a
filler at the exact parallel 11D boundaries, preserving the signed
integer count but not the original free-group history. This is a
RELATIVE source-presentation theorem, not a universal no-go or
arbitrary-pasting coherence.
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

inductive NativeK5CoreTwelveCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t},
      NativeK5StructuralElevenCell p P Q →
      NativeK5StructuralElevenCell p P Q →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) : NativeK5CoreTwelveCell p H H
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (R : NativeK5CoreTwelveCell p H K) : NativeK5CoreTwelveCell p K H
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K L : NativeK5StructuralElevenCell p P Q}
      (R : NativeK5CoreTwelveCell p H K) (S : NativeK5CoreTwelveCell p K L) : NativeK5CoreTwelveCell p H L
  | elevenAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R S : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) (K : NativeK5StructuralElevenCell p Q R)
      (L : NativeK5StructuralElevenCell p R S) :
      NativeK5CoreTwelveCell p (.trans (.trans H K) L) (.trans H (.trans K L))
  | elevenLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5CoreTwelveCell p (.trans (.core (.refl P)) H) H
  | elevenRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5CoreTwelveCell p (.trans H (.core (.refl Q))) H
  | elevenInverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5CoreTwelveCell p (.trans H (.symm H)) (.core (.refl P))
  | elevenInverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5CoreTwelveCell p (.trans (.symm H) H) (.core (.refl Q))
  | elevenVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5CoreTwelveCell p (.trans H suffix) (.trans K suffix)
  | elevenVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralElevenCell p P Q)
      {H K : NativeK5StructuralElevenCell p Q R}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.trans prior H) (.trans prior K)
  | elevenSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.symm H) (.symm K)
  | tenVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5CoreTwelveCell p (.tenVerticalLeft H suffix) (.tenVerticalLeft K suffix)
  | tenVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p t j}
      (prior : NativeK5StructuralTenCell p q t)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.tenVerticalRight prior H) (.tenVerticalRight prior K)
  | tenSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.tenSymmRespect H) (.tenSymmRespect K)
  | nineVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5CoreTwelveCell p (.nineVerticalLeft H suffix) (.nineVerticalLeft K suffix)
  | nineVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p d j}
      {P Q : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralNineCell p e d)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.nineVerticalRight prior H) (.nineVerticalRight prior K)
  | nineSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.nineSymmRespect H) (.nineSymmRespect K)
  | eightVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreTwelveCell p (.eightVerticalLeft H suffix) (.eightVerticalLeft K suffix)
  | eightVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p k l}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralEightCell p h k)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.eightVerticalRight prior H) (.eightVerticalRight prior K)
  | eightInverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) :
      NativeK5CoreTwelveCell p (.eightInverseRespect H) (.eightInverseRespect K)

theorem NativeK5CoreTwelveCell.historyWord_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    (R : NativeK5CoreTwelveCell p H K) :
    H.historyWord = K.historyWord := by
  induction R with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | elevenAssoc H K L =>
      change (H.historyWord * K.historyWord) * L.historyWord =
        H.historyWord * (K.historyWord * L.historyWord)
      exact mul_assoc _ _ _
  | elevenLeftUnit H =>
      change (1 : NativeK5ElevenHistoryWord) * H.historyWord = H.historyWord
      exact one_mul _
  | elevenRightUnit H =>
      change H.historyWord * (1 : NativeK5ElevenHistoryWord) = H.historyWord
      exact mul_one _
  | elevenInverseLeft H =>
      change H.historyWord * H.historyWord⁻¹ = (1 : NativeK5ElevenHistoryWord)
      exact mul_inv_cancel _
  | elevenInverseRight H =>
      change H.historyWord⁻¹ * H.historyWord = (1 : NativeK5ElevenHistoryWord)
      exact inv_mul_cancel _
  | elevenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : NativeK5ElevenHistoryWord =>
        x * suffix.historyWord) ih
  | elevenVerticalRight prior _ ih =>
      exact congrArg (fun x : NativeK5ElevenHistoryWord =>
        prior.historyWord * x) ih
  | elevenSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5ElevenHistoryWord => x⁻¹) ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5ElevenHistoryWord =>
        nativeK5ElevenInverseFrame * x * nativeK5ElevenInverseFrame⁻¹) ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

theorem NativeK5CoreTwelveCell.squareCount_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    (R : NativeK5CoreTwelveCell p H K) :
    H.squareCount = K.squareCount := by
  induction R with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | elevenAssoc H K L =>
      change (H.squareCount + K.squareCount) + L.squareCount =
        H.squareCount + (K.squareCount + L.squareCount)
      exact add_assoc _ _ _
  | elevenLeftUnit H =>
      change (0 : ℤ) + H.squareCount = H.squareCount
      exact zero_add _
  | elevenRightUnit H =>
      change H.squareCount + (0 : ℤ) = H.squareCount
      exact add_zero _
  | elevenInverseLeft H =>
      change H.squareCount + -H.squareCount = (0 : ℤ)
      exact add_neg_cancel _
  | elevenInverseRight H =>
      change -H.squareCount + H.squareCount = (0 : ℤ)
      exact neg_add_cancel _
  | elevenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | elevenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | elevenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih => exact ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- The 12D square exchange is an ADJOINED Type-valued generator,
not a definitional equality of distinct raw 11D terms. -/
inductive NativeK5StructuralTwelveCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t},
      NativeK5StructuralElevenCell p P Q →
      NativeK5StructuralElevenCell p P Q →
      Type (max (max uD uE) (max vD vE)) where
  | core
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5CoreTwelveCell p H K) : NativeK5StructuralTwelveCell p H K
  | squareExchange
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (H : NativeK5StructuralElevenCell p P Q) :
      NativeK5StructuralTwelveCell p (nativeK5ElevenPastingLeftThenRight H)
        (nativeK5ElevenPastingRightThenLeft H)
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) : NativeK5StructuralTwelveCell p K H
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K L : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) (V : NativeK5StructuralTwelveCell p K L) :
      NativeK5StructuralTwelveCell p H L
  | elevenVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5StructuralTwelveCell p (.trans H suffix) (.trans K suffix)
  | elevenVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q R : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralElevenCell p P Q)
      {H K : NativeK5StructuralElevenCell p Q R}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.trans prior H) (.trans prior K)
  | elevenSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.symm H) (.symm K)
  | tenVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5StructuralTwelveCell p (.tenVerticalLeft H suffix) (.tenVerticalLeft K suffix)
  | tenVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t j : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p t j}
      (prior : NativeK5StructuralTenCell p q t)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.tenVerticalRight prior H) (.tenVerticalRight prior K)
  | tenSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.tenSymmRespect H) (.tenSymmRespect K)
  | nineVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5StructuralTwelveCell p (.nineVerticalLeft H suffix) (.nineVerticalLeft K suffix)
  | nineVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d j : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p d j}
      {P Q : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralNineCell p e d)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.nineVerticalRight prior H) (.nineVerticalRight prior K)
  | nineSymmRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.nineSymmRespect H) (.nineSymmRespect K)
  | eightVerticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralTwelveCell p (.eightVerticalLeft H suffix) (.eightVerticalLeft K suffix)
  | eightVerticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k l : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p k l}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      (prior : NativeK5StructuralEightCell p h k)
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.eightVerticalRight prior H) (.eightVerticalRight prior K)
  | eightInverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      {u v : NativeK5StructuralSixCell p w z}
      {h k : NativeK5StructuralSevenCell p u v}
      {e d : NativeK5StructuralEightCell p h k}
      {q t : NativeK5StructuralNineCell p e d}
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralTwelveCell p (.eightInverseRespect H) (.eightInverseRespect K)

theorem NativeK5StructuralTwelveCell.squareCount_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    {P Q : NativeK5StructuralTenCell p q t}
    {H K : NativeK5StructuralElevenCell p P Q}
    (R : NativeK5StructuralTwelveCell p H K) :
    H.squareCount = K.squareCount := by
  induction R with
  | core witness => exact witness.squareCount_sound
  | squareExchange witness => exact nativeK5ElevenPasting_integerBlind witness
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | elevenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | elevenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | elevenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih => exact ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

theorem nativeK5ElevenExchange_twelveRelativeNecessity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5StructuralTenCell p q t) :
    Nonempty (NativeK5StructuralTwelveCell p (nativeK5ElevenPastingLeftThenRight (NativeK5StructuralElevenCell.squareExchange P)) (nativeK5ElevenPastingRightThenLeft (NativeK5StructuralElevenCell.squareExchange P))) ∧
    ¬ Nonempty (NativeK5CoreTwelveCell p (nativeK5ElevenPastingLeftThenRight (NativeK5StructuralElevenCell.squareExchange P)) (nativeK5ElevenPastingRightThenLeft (NativeK5StructuralElevenCell.squareExchange P))) := by
  constructor
  · exact ⟨.squareExchange (NativeK5StructuralElevenCell.squareExchange P)⟩
  · rintro ⟨R⟩
    exact nativeK5ElevenSquareExchange_pastingWord_ne P R.historyWord_sound

theorem nativeK5ElevenExchange_twelveNoCoreRetraction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    {u v : NativeK5StructuralSixCell p w z}
    {h k : NativeK5StructuralSevenCell p u v}
    {e d : NativeK5StructuralEightCell p h k}
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5StructuralTenCell p q t) :
    ¬ Nonempty
      (NativeK5StructuralTwelveCell p (nativeK5ElevenPastingLeftThenRight (NativeK5StructuralElevenCell.squareExchange P)) (nativeK5ElevenPastingRightThenLeft (NativeK5StructuralElevenCell.squareExchange P)) →
       NativeK5CoreTwelveCell p (nativeK5ElevenPastingLeftThenRight (NativeK5StructuralElevenCell.squareExchange P)) (nativeK5ElevenPastingRightThenLeft (NativeK5StructuralElevenCell.squareExchange P))) := by
  rintro ⟨retract⟩
  obtain ⟨⟨newTwelve⟩, noCore⟩ :=
    nativeK5ElevenExchange_twelveRelativeNecessity P
  exact noCore ⟨retract newTwelve⟩

#print axioms NativeK5CoreTwelveCell
#print axioms NativeK5CoreTwelveCell.historyWord_sound
#print axioms NativeK5CoreTwelveCell.squareCount_sound
#print axioms NativeK5StructuralTwelveCell
#print axioms NativeK5StructuralTwelveCell.squareCount_sound
#print axioms nativeK5ElevenExchange_twelveRelativeNecessity
#print axioms nativeK5ElevenExchange_twelveNoCoreRetraction

end
end Kuu.F112.Physical
