import Kuu.F112.PolygonNativeF55P94DK5TwelveCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AK — genuine dependent THIRTEEN-cell square comparison

On ORIGINAL Type-valued 12-cell evidence at exact 11-cell boundaries,
define a conservative dependent 13-cell syntax with 12D groupoid
coherence and all original 12D/11D/10D/9D/8D congruences.
The chosen free-group 12D history and integer count are preserved by
EVERY conservative constructor. The genuine 12D inverse-square pair
has unequal free-group histories and no such conservative 13D filler.

An INDEPENDENT source-dependent Type-valued 13D squareExchange is
then adjoined. This is a presentation-relative comparison and a
specific obstruction, not universal higher coherence or an arbitrary
13D filler construction.
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

/-- Relative, conservative 13D witnesses between two ORIGINAL
source-dependent 12-cell evidence terms. -/
inductive NativeK5CoreThirteenCell (p : Polygon) :
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
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q},
      NativeK5StructuralTwelveCell p H K →
      NativeK5StructuralTwelveCell p H K →
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
      {H K : NativeK5StructuralElevenCell p P Q}
      (U : NativeK5StructuralTwelveCell p H K) :
      NativeK5CoreThirteenCell p U U
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p V U
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V W : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) (S : NativeK5CoreThirteenCell p V W) :
      NativeK5CoreThirteenCell p U W
  | twelveAssoc
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
      {H K L M : NativeK5StructuralElevenCell p P Q}
      (U : NativeK5StructuralTwelveCell p H K) (V : NativeK5StructuralTwelveCell p K L)
      (W : NativeK5StructuralTwelveCell p L M) :
      NativeK5CoreThirteenCell p (.trans (.trans U V) W) (.trans U (.trans V W))
  | twelveLeftUnit
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
      (U : NativeK5StructuralTwelveCell p H K) :
      NativeK5CoreThirteenCell p (.trans (.core (.refl H)) U) U
  | twelveRightUnit
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
      (U : NativeK5StructuralTwelveCell p H K) :
      NativeK5CoreThirteenCell p (.trans U (.core (.refl K))) U
  | twelveInverseLeft
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
      (U : NativeK5StructuralTwelveCell p H K) :
      NativeK5CoreThirteenCell p (.trans U (.symm U)) (.core (.refl H))
  | twelveInverseRight
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
      (U : NativeK5StructuralTwelveCell p H K) :
      NativeK5CoreThirteenCell p (.trans (.symm U) U) (.core (.refl K))
  | twelveVerticalLeft
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V)
      (suffix : NativeK5StructuralTwelveCell p K L) :
      NativeK5CoreThirteenCell p (.trans U suffix) (.trans V suffix)
  | twelveVerticalRight
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
      {U V : NativeK5StructuralTwelveCell p K L}
      (prior : NativeK5StructuralTwelveCell p H K)
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.trans prior U) (.trans prior V)
  | twelveSymmRespect
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.symm U) (.symm V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5CoreThirteenCell p (.elevenVerticalLeft U suffix) (.elevenVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p Q R}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralElevenCell p P Q)
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.elevenVerticalRight prior U) (.elevenVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.elevenSymmRespect U) (.elevenSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5CoreThirteenCell p (.tenVerticalLeft U suffix) (.tenVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralTenCell p q t)
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.tenVerticalRight prior U) (.tenVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.tenSymmRespect U) (.tenSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5CoreThirteenCell p (.nineVerticalLeft U suffix) (.nineVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralNineCell p e d)
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.nineVerticalRight prior U) (.nineVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.nineSymmRespect U) (.nineSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreThirteenCell p (.eightVerticalLeft U suffix) (.eightVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralEightCell p h k)
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.eightVerticalRight prior U) (.eightVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5CoreThirteenCell p U V) :
      NativeK5CoreThirteenCell p (.eightInverseRespect U) (.eightInverseRespect V)

/-- Every conservative 13D constructor conserves the selected
noncommutative universal free-group history of original 12D terms. -/
theorem NativeK5CoreThirteenCell.historyWord_sound
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
    {U V : NativeK5StructuralTwelveCell p H K}
    (R : NativeK5CoreThirteenCell p U V) :
    U.historyWord = V.historyWord := by
  induction R with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | twelveAssoc U V W =>
      change (U.historyWord * V.historyWord) * W.historyWord =
        U.historyWord * (V.historyWord * W.historyWord)
      exact mul_assoc _ _ _
  | twelveLeftUnit U =>
      change (1 : NativeK5TwelveHistoryWord) * U.historyWord = U.historyWord
      exact one_mul _
  | twelveRightUnit U =>
      change U.historyWord * (1 : NativeK5TwelveHistoryWord) = U.historyWord
      exact mul_one _
  | twelveInverseLeft U =>
      change U.historyWord * U.historyWord⁻¹ = (1 : NativeK5TwelveHistoryWord)
      exact mul_inv_cancel _
  | twelveInverseRight U =>
      change U.historyWord⁻¹ * U.historyWord = (1 : NativeK5TwelveHistoryWord)
      exact inv_mul_cancel _
  | twelveVerticalLeft _ suffix ih =>
      exact congrArg (fun x : NativeK5TwelveHistoryWord => x * suffix.historyWord) ih
  | twelveVerticalRight prior _ ih =>
      exact congrArg (fun x : NativeK5TwelveHistoryWord => prior.historyWord * x) ih
  | twelveSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5TwelveHistoryWord => x⁻¹) ih
  | elevenVerticalLeft _ suffix ih => exact ih
  | elevenVerticalRight prior _ ih => exact ih
  | elevenSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5TwelveHistoryWord =>
        nativeK5TwelveInverseFrame * x * nativeK5TwelveInverseFrame⁻¹) ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih => exact ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- Every conservative 13D constructor preserves signed count. -/
theorem NativeK5CoreThirteenCell.squareCount_sound
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
    {U V : NativeK5StructuralTwelveCell p H K}
    (R : NativeK5CoreThirteenCell p U V) :
    U.squareCount = V.squareCount := by
  induction R with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | twelveAssoc U V W =>
      change (U.squareCount + V.squareCount) + W.squareCount =
        U.squareCount + (V.squareCount + W.squareCount)
      exact add_assoc _ _ _
  | twelveLeftUnit U =>
      change (0 : ℤ) + U.squareCount = U.squareCount
      exact zero_add _
  | twelveRightUnit U =>
      change U.squareCount + (0 : ℤ) = U.squareCount
      exact add_zero _
  | twelveInverseLeft U =>
      change U.squareCount + -U.squareCount = (0 : ℤ)
      exact add_neg_cancel _
  | twelveInverseRight U =>
      change -U.squareCount + U.squareCount = (0 : ℤ)
      exact neg_add_cancel _
  | twelveVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | twelveVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | twelveSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | elevenVerticalLeft _ suffix ih => exact ih
  | elevenVerticalRight prior _ ih => exact ih
  | elevenSymmRespect _ ih => exact ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih => exact ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih

/-- An independent Type-valued 13D squareExchange generator
compares the two ORIGINAL dependent 12-cell paths. -/
inductive NativeK5StructuralThirteenCell (p : Polygon) :
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
      {P Q : NativeK5StructuralTenCell p q t}
      {H K : NativeK5StructuralElevenCell p P Q},
      NativeK5StructuralTwelveCell p H K →
      NativeK5StructuralTwelveCell p H K →
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (T : NativeK5CoreThirteenCell p U V) :
      NativeK5StructuralThirteenCell p U V
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
      {H K : NativeK5StructuralElevenCell p P Q}
      (W : NativeK5StructuralTwelveCell p H K) :
      NativeK5StructuralThirteenCell p (nativeK5TwelvePastingLeftThenRight W) (nativeK5TwelvePastingRightThenLeft W)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p V U
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V W : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) (S : NativeK5StructuralThirteenCell p V W) :
      NativeK5StructuralThirteenCell p U W
  | twelveVerticalLeft
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V)
      (suffix : NativeK5StructuralTwelveCell p K L) :
      NativeK5StructuralThirteenCell p (.trans U suffix) (.trans V suffix)
  | twelveVerticalRight
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
      {U V : NativeK5StructuralTwelveCell p K L}
      (prior : NativeK5StructuralTwelveCell p H K)
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.trans prior U) (.trans prior V)
  | twelveSymmRespect
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.symm U) (.symm V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5StructuralThirteenCell p (.elevenVerticalLeft U suffix) (.elevenVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p Q R}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralElevenCell p P Q)
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.elevenVerticalRight prior U) (.elevenVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.elevenSymmRespect U) (.elevenSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5StructuralThirteenCell p (.tenVerticalLeft U suffix) (.tenVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralTenCell p q t)
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.tenVerticalRight prior U) (.tenVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.tenSymmRespect U) (.tenSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5StructuralThirteenCell p (.nineVerticalLeft U suffix) (.nineVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralNineCell p e d)
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.nineVerticalRight prior U) (.nineVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.nineSymmRespect U) (.nineSymmRespect V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralThirteenCell p (.eightVerticalLeft U suffix) (.eightVerticalLeft V suffix)
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K}
      (prior : NativeK5StructuralEightCell p h k)
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.eightVerticalRight prior U) (.eightVerticalRight prior V)
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (R : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralThirteenCell p (.eightInverseRespect U) (.eightInverseRespect V)

/-- Newly adjoined 13D equality preserves the signed integer
12D count even where chosen free history does NOT descend. -/
theorem NativeK5StructuralThirteenCell.squareCount_sound
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
    {U V : NativeK5StructuralTwelveCell p H K}
    (R : NativeK5StructuralThirteenCell p U V) :
    U.squareCount = V.squareCount := by
  induction R with
  | core witness => exact witness.squareCount_sound
  | squareExchange witness => exact nativeK5TwelvePasting_integerBlind witness
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | twelveVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | twelveVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | twelveSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | elevenVerticalLeft _ suffix ih => exact ih
  | elevenVerticalRight prior _ ih => exact ih
  | elevenSymmRespect _ ih => exact ih
  | tenVerticalLeft _ suffix ih => exact ih
  | tenVerticalRight prior _ ih => exact ih
  | tenSymmRespect _ ih => exact ih
  | nineVerticalLeft _ suffix ih => exact ih
  | nineVerticalRight prior _ ih => exact ih
  | nineSymmRespect _ ih => exact ih
  | eightVerticalLeft _ suffix ih => exact ih
  | eightVerticalRight prior _ ih => exact ih
  | eightInverseRespect _ ih => exact ih


/-- For an arbitrary original 12D witness, the new independent 13D
square always compares its two pastings. An obstruction to a
conservative filler additionally needs unequal selected histories. -/
theorem nativeK5TwelveExchange_thirteenRelativeNecessity
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
    (W : NativeK5StructuralTwelveCell p H K)
    (hword : (nativeK5TwelvePastingLeftThenRight W).historyWord ≠
      (nativeK5TwelvePastingRightThenLeft W).historyWord) :
    Nonempty (NativeK5StructuralThirteenCell p
      (nativeK5TwelvePastingLeftThenRight W) (nativeK5TwelvePastingRightThenLeft W)) ∧
    ¬ Nonempty (NativeK5CoreThirteenCell p
      (nativeK5TwelvePastingLeftThenRight W) (nativeK5TwelvePastingRightThenLeft W)) := by
  constructor
  · exact ⟨.squareExchange W⟩
  · rintro ⟨proof⟩
    exact hword proof.historyWord_sound

/-- Fully unconditional result on the original independent 12D
squareExchange generator, certified by an existing S₃ witness. -/
theorem nativeK5TwelveSquareExchange_thirteenRelativeNecessity
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
    (X : NativeK5StructuralElevenCell p P Q) :
    Nonempty (NativeK5StructuralThirteenCell p
      (nativeK5TwelvePastingLeftThenRight (NativeK5StructuralTwelveCell.squareExchange X))
      (nativeK5TwelvePastingRightThenLeft (NativeK5StructuralTwelveCell.squareExchange X))) ∧
    ¬ Nonempty (NativeK5CoreThirteenCell p
      (nativeK5TwelvePastingLeftThenRight (NativeK5StructuralTwelveCell.squareExchange X))
      (nativeK5TwelvePastingRightThenLeft (NativeK5StructuralTwelveCell.squareExchange X))) :=
  nativeK5TwelveExchange_thirteenRelativeNecessity
    (NativeK5StructuralTwelveCell.squareExchange X)
    (nativeK5TwelveSquareExchange_pastingWord_ne X)

/-- Boundary-preserving retraction of the independent 13D comparison
onto the named conservative grammar is impossible at this exact pair. -/
theorem nativeK5TwelveExchange_thirteenNoCoreRetraction
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
    (W : NativeK5StructuralTwelveCell p H K)
    (hword : (nativeK5TwelvePastingLeftThenRight W).historyWord ≠
      (nativeK5TwelvePastingRightThenLeft W).historyWord) :
    ¬ Nonempty
      (NativeK5StructuralThirteenCell p
        (nativeK5TwelvePastingLeftThenRight W) (nativeK5TwelvePastingRightThenLeft W) →
       NativeK5CoreThirteenCell p
        (nativeK5TwelvePastingLeftThenRight W) (nativeK5TwelvePastingRightThenLeft W)) := by
  rintro ⟨retract⟩
  obtain ⟨⟨newThirteen⟩, noCore⟩ :=
    nativeK5TwelveExchange_thirteenRelativeNecessity W hword
  exact noCore ⟨retract newThirteen⟩

theorem nativeK5TwelveSquareExchange_thirteenNoCoreRetraction
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
    (X : NativeK5StructuralElevenCell p P Q) :
    ¬ Nonempty
      (NativeK5StructuralThirteenCell p
        (nativeK5TwelvePastingLeftThenRight (NativeK5StructuralTwelveCell.squareExchange X))
        (nativeK5TwelvePastingRightThenLeft (NativeK5StructuralTwelveCell.squareExchange X)) →
       NativeK5CoreThirteenCell p
        (nativeK5TwelvePastingLeftThenRight (NativeK5StructuralTwelveCell.squareExchange X))
        (nativeK5TwelvePastingRightThenLeft (NativeK5StructuralTwelveCell.squareExchange X))) :=
  nativeK5TwelveExchange_thirteenNoCoreRetraction
    (NativeK5StructuralTwelveCell.squareExchange X)
    (nativeK5TwelveSquareExchange_pastingWord_ne X)

#print axioms NativeK5CoreThirteenCell
#print axioms NativeK5CoreThirteenCell.historyWord_sound
#print axioms NativeK5CoreThirteenCell.squareCount_sound
#print axioms NativeK5StructuralThirteenCell
#print axioms NativeK5StructuralThirteenCell.squareCount_sound
#print axioms nativeK5TwelveExchange_thirteenRelativeNecessity
#print axioms nativeK5TwelveExchange_thirteenNoCoreRetraction
#print axioms nativeK5TwelveSquareExchange_thirteenRelativeNecessity
#print axioms nativeK5TwelveSquareExchange_thirteenNoCoreRetraction

end
end Kuu.F112.Physical
