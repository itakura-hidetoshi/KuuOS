import Kuu.F112.PolygonNativeF55P94DK5ThirteenCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112-P94D3AM — actual original source-dependent fourteen-cell coherence

The domain consists of ORIGINAL Type-valued THIRTEEN-cell evidence
between exactly equal source-typed TWELVE-cell endpoints. The specifically
conservative FOURTEEN-cell grammar preserves chosen free-group history
and integer square-exchange charge under all of its constructors.

Independently adjoin a genuine Type-valued 14-cell squareExchange
at the two original 13-cell inverse-square pasting paths; it is NOT
asserted as raw term equality or derived from the conservative grammar.

Nonexistence and no-retraction are relative to this conservative syntax
and its CHOSEN free-group history. No arbitrary high coherence, complete
old P92B descent, global strict 3/n, or (∞,3)-hyperdescent is claimed.
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

/-- The conservative 14D grammar, at exact original 12D boundaries
of two genuine original 13-cell witnesses. -/
inductive NativeK5CoreFourteenCell (p : Polygon) :
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K},
      NativeK5StructuralThirteenCell p U V →
      NativeK5StructuralThirteenCell p U V →
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (T : NativeK5StructuralThirteenCell p U V) :
      NativeK5CoreFourteenCell p T T
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p S T
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
      {U V : NativeK5StructuralTwelveCell p H K}
      {T S Z : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) (following : NativeK5CoreFourteenCell p S Z) :
      NativeK5CoreFourteenCell p T Z
  | thirteenAssoc
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
      {U V W X : NativeK5StructuralTwelveCell p H K}
      (T : NativeK5StructuralThirteenCell p U V) (S : NativeK5StructuralThirteenCell p V W)
      (Z : NativeK5StructuralThirteenCell p W X) :
      NativeK5CoreFourteenCell p (.trans (.trans T S) Z) (.trans T (.trans S Z))
  | thirteenLeftUnit
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
      (T : NativeK5StructuralThirteenCell p U V) :
      NativeK5CoreFourteenCell p (.trans (.core (.refl U)) T) T
  | thirteenRightUnit
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
      (T : NativeK5StructuralThirteenCell p U V) :
      NativeK5CoreFourteenCell p (.trans T (.core (.refl V))) T
  | thirteenInverseLeft
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
      (T : NativeK5StructuralThirteenCell p U V) :
      NativeK5CoreFourteenCell p (.trans T (.symm T)) (.core (.refl U))
  | thirteenInverseRight
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
      (T : NativeK5StructuralThirteenCell p U V) :
      NativeK5CoreFourteenCell p (.trans (.symm T) T) (.core (.refl V))
  | thirteenVerticalLeft
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralThirteenCell p V W) :
      NativeK5CoreFourteenCell p (.trans T suffix) (.trans S suffix)
  | thirteenVerticalRight
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
      {T S : NativeK5StructuralThirteenCell p V W}
      (prior : NativeK5StructuralThirteenCell p U V)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.trans prior T) (.trans prior S)
  | thirteenSymmRespect
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.symm T) (.symm S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralTwelveCell p K L) :
      NativeK5CoreFourteenCell p (.twelveVerticalLeft T suffix) (.twelveVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralTwelveCell p H K)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.twelveVerticalRight prior T) (.twelveVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.twelveSymmRespect T) (.twelveSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5CoreFourteenCell p (.elevenVerticalLeft T suffix) (.elevenVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralElevenCell p P Q)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.elevenVerticalRight prior T) (.elevenVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.elevenSymmRespect T) (.elevenSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5CoreFourteenCell p (.tenVerticalLeft T suffix) (.tenVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralTenCell p q t)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.tenVerticalRight prior T) (.tenVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.tenSymmRespect T) (.tenSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5CoreFourteenCell p (.nineVerticalLeft T suffix) (.nineVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralNineCell p e d)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.nineVerticalRight prior T) (.nineVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.nineSymmRespect T) (.nineSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5CoreFourteenCell p (.eightVerticalLeft T suffix) (.eightVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralEightCell p h k)
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.eightVerticalRight prior T) (.eightVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5CoreFourteenCell p (.eightInverseRespect T) (.eightInverseRespect S)

/-- Noncommutative history is preserved under EVERY generator of the
named conservative Type-valued fourteen-cell grammar. -/
theorem NativeK5CoreFourteenCell.historyWord_sound
    {p : Polygon}
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
    {T S : NativeK5StructuralThirteenCell p U V}
    (proof : NativeK5CoreFourteenCell p T S) :
    T.historyWord = S.historyWord := by
  induction proof with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | thirteenAssoc T S Z =>
      change (T.historyWord * S.historyWord) * Z.historyWord =
        T.historyWord * (S.historyWord * Z.historyWord)
      exact mul_assoc _ _ _
  | thirteenLeftUnit T =>
      change (1 : NativeK5ThirteenHistoryWord) * T.historyWord = T.historyWord
      exact one_mul _
  | thirteenRightUnit T =>
      change T.historyWord * (1 : NativeK5ThirteenHistoryWord) = T.historyWord
      exact mul_one _
  | thirteenInverseLeft T =>
      change T.historyWord * T.historyWord⁻¹ = (1 : NativeK5ThirteenHistoryWord)
      exact mul_inv_cancel _
  | thirteenInverseRight T =>
      change T.historyWord⁻¹ * T.historyWord = (1 : NativeK5ThirteenHistoryWord)
      exact inv_mul_cancel _
  | thirteenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : NativeK5ThirteenHistoryWord => x * suffix.historyWord) ih
  | thirteenVerticalRight prior _ ih =>
      exact congrArg (fun x : NativeK5ThirteenHistoryWord => prior.historyWord * x) ih
  | thirteenSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5ThirteenHistoryWord => x⁻¹) ih
  | twelveVerticalLeft _ suffix ih => exact ih
  | twelveVerticalRight prior _ ih => exact ih
  | twelveSymmRespect _ ih =>
      exact congrArg (fun x : NativeK5ThirteenHistoryWord =>
        nativeK5ThirteenInverseFrame * x * nativeK5ThirteenInverseFrame⁻¹) ih
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

/-- Signed 13D square count is preserved by all conservative 14D
generators at exact dependent 12D boundaries. -/
theorem NativeK5CoreFourteenCell.squareCount_sound
    {p : Polygon}
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
    {T S : NativeK5StructuralThirteenCell p U V}
    (proof : NativeK5CoreFourteenCell p T S) :
    T.squareCount = S.squareCount := by
  induction proof with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | thirteenAssoc T S Z =>
      change (T.squareCount + S.squareCount) + Z.squareCount =
        T.squareCount + (S.squareCount + Z.squareCount)
      exact add_assoc _ _ _
  | thirteenLeftUnit T =>
      change (0 : ℤ) + T.squareCount = T.squareCount
      exact zero_add _
  | thirteenRightUnit T =>
      change T.squareCount + (0 : ℤ) = T.squareCount
      exact add_zero _
  | thirteenInverseLeft T =>
      change T.squareCount + -T.squareCount = (0 : ℤ)
      exact add_neg_cancel _
  | thirteenInverseRight T =>
      change -T.squareCount + T.squareCount = (0 : ℤ)
      exact neg_add_cancel _
  | thirteenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | thirteenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | thirteenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | twelveVerticalLeft _ suffix ih => exact ih
  | twelveVerticalRight prior _ ih => exact ih
  | twelveSymmRespect _ ih => exact ih
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

/-- Independently extended, truly Type-valued original 14D syntax.
In particular, squareExchange is an ADJOINED generator, not a
proof that the original raw thirteen-cell witnesses are equal. -/
inductive NativeK5StructuralFourteenCell (p : Polygon) :
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
      {H K : NativeK5StructuralElevenCell p P Q}
      {U V : NativeK5StructuralTwelveCell p H K},
      NativeK5StructuralThirteenCell p U V →
      NativeK5StructuralThirteenCell p U V →
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5CoreFourteenCell p T S) :
      NativeK5StructuralFourteenCell p T S
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
      {U V : NativeK5StructuralTwelveCell p H K}
      (W : NativeK5StructuralThirteenCell p U V) :
      NativeK5StructuralFourteenCell p  (nativeK5ThirteenPastingLeftThenRight W) (nativeK5ThirteenPastingRightThenLeft W)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p S T
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
      {U V : NativeK5StructuralTwelveCell p H K}
      {T S Z : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) (following : NativeK5StructuralFourteenCell p S Z) :
      NativeK5StructuralFourteenCell p T Z
  | thirteenVerticalLeft
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralThirteenCell p V W) :
      NativeK5StructuralFourteenCell p (.trans T suffix) (.trans S suffix)
  | thirteenVerticalRight
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
      {T S : NativeK5StructuralThirteenCell p V W}
      (prior : NativeK5StructuralThirteenCell p U V)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.trans prior T) (.trans prior S)
  | thirteenSymmRespect
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.symm T) (.symm S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralTwelveCell p K L) :
      NativeK5StructuralFourteenCell p (.twelveVerticalLeft T suffix) (.twelveVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralTwelveCell p H K)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.twelveVerticalRight prior T) (.twelveVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.twelveSymmRespect T) (.twelveSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralElevenCell p Q R) :
      NativeK5StructuralFourteenCell p (.elevenVerticalLeft T suffix) (.elevenVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralElevenCell p P Q)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.elevenVerticalRight prior T) (.elevenVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.elevenSymmRespect T) (.elevenSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralTenCell p t j) :
      NativeK5StructuralFourteenCell p (.tenVerticalLeft T suffix) (.tenVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralTenCell p q t)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.tenVerticalRight prior T) (.tenVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.tenSymmRespect T) (.tenSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralNineCell p d j) :
      NativeK5StructuralFourteenCell p (.nineVerticalLeft T suffix) (.nineVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralNineCell p e d)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.nineVerticalRight prior T) (.nineVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.nineSymmRespect T) (.nineSymmRespect S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S)
      (suffix : NativeK5StructuralEightCell p k l) :
      NativeK5StructuralFourteenCell p (.eightVerticalLeft T suffix) (.eightVerticalLeft S suffix)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (prior : NativeK5StructuralEightCell p h k)
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.eightVerticalRight prior T) (.eightVerticalRight prior S)
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
      {T S : NativeK5StructuralThirteenCell p U V}
      (proof : NativeK5StructuralFourteenCell p T S) :
      NativeK5StructuralFourteenCell p (.eightInverseRespect T) (.eightInverseRespect S)

/-- The independently extended fourteen-cell comparison preserves
signed thirteen-cell generator count. -/
theorem NativeK5StructuralFourteenCell.squareCount_sound
    {p : Polygon}
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
    {T S : NativeK5StructuralThirteenCell p U V}
    (proof : NativeK5StructuralFourteenCell p T S) :
    T.squareCount = S.squareCount := by
  induction proof with
  | core proof => exact proof.squareCount_sound
  | squareExchange W => exact nativeK5ThirteenPasting_integerBlind W
  | symm _ ih => exact ih.symm
  | trans _ _ ih1 ih2 => exact ih1.trans ih2
  | thirteenVerticalLeft _ suffix ih =>
      exact congrArg (fun x : ℤ => x + suffix.squareCount) ih
  | thirteenVerticalRight prior _ ih =>
      exact congrArg (fun x : ℤ => prior.squareCount + x) ih
  | thirteenSymmRespect _ ih =>
      exact congrArg (fun x : ℤ => -x) ih
  | twelveVerticalLeft _ suffix ih => exact ih
  | twelveVerticalRight prior _ ih => exact ih
  | twelveSymmRespect _ ih => exact ih
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

/-- For an arbitrary original 13D term, a selected free-history
obstruction implies absence of a conservative 14D comparison,
while the independent genuine fourteen-cell generator exists. -/
theorem nativeK5ThirteenExchange_fourteenRelativeNecessity
    {p : Polygon}
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
    (W : NativeK5StructuralThirteenCell p U V)
    (hword : (nativeK5ThirteenPastingLeftThenRight W).historyWord ≠ (nativeK5ThirteenPastingRightThenLeft W).historyWord) :
    Nonempty (NativeK5StructuralFourteenCell p (nativeK5ThirteenPastingLeftThenRight W) (nativeK5ThirteenPastingRightThenLeft W)) ∧
    ¬ Nonempty (NativeK5CoreFourteenCell p (nativeK5ThirteenPastingLeftThenRight W) (nativeK5ThirteenPastingRightThenLeft W)) := by
  constructor
  · exact ⟨.squareExchange W⟩
  · rintro ⟨proof⟩
    exact hword proof.historyWord_sound

/-- The independent genuine 13D squareExchange of an ORIGINAL
12D comparison gives unconditional relative 14D necessity. -/
theorem nativeK5ThirteenSquareExchange_fourteenRelativeNecessity
    {p : Polygon}
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
    (X : NativeK5StructuralTwelveCell p H K) :
    Nonempty (NativeK5StructuralFourteenCell p
      (nativeK5ThirteenPastingLeftThenRight (NativeK5StructuralThirteenCell.squareExchange X))
      (nativeK5ThirteenPastingRightThenLeft (NativeK5StructuralThirteenCell.squareExchange X))) ∧
    ¬ Nonempty (NativeK5CoreFourteenCell p
      (nativeK5ThirteenPastingLeftThenRight (NativeK5StructuralThirteenCell.squareExchange X))
      (nativeK5ThirteenPastingRightThenLeft (NativeK5StructuralThirteenCell.squareExchange X))) :=
  nativeK5ThirteenExchange_fourteenRelativeNecessity
    (NativeK5StructuralThirteenCell.squareExchange X)
    (nativeK5ThirteenSquareExchange_pastingWord_ne X)

/-- Boundary-preserving return to the explicitly named conservative
fourteen-cell grammar is impossible at an obstructed source pair. -/
theorem nativeK5ThirteenExchange_fourteenNoCoreRetraction
    {p : Polygon}
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
    (W : NativeK5StructuralThirteenCell p U V)
    (hword : (nativeK5ThirteenPastingLeftThenRight W).historyWord ≠ (nativeK5ThirteenPastingRightThenLeft W).historyWord) :
    ¬ Nonempty
      (NativeK5StructuralFourteenCell p (nativeK5ThirteenPastingLeftThenRight W) (nativeK5ThirteenPastingRightThenLeft W) →
       NativeK5CoreFourteenCell p (nativeK5ThirteenPastingLeftThenRight W) (nativeK5ThirteenPastingRightThenLeft W)) := by
  rintro ⟨retract⟩
  obtain ⟨⟨newFourteen⟩, noCore⟩ :=
    nativeK5ThirteenExchange_fourteenRelativeNecessity W hword
  exact noCore ⟨retract newFourteen⟩

theorem nativeK5ThirteenSquareExchange_fourteenNoCoreRetraction
    {p : Polygon}
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
    (X : NativeK5StructuralTwelveCell p H K) :
    ¬ Nonempty
      (NativeK5StructuralFourteenCell p
        (nativeK5ThirteenPastingLeftThenRight (NativeK5StructuralThirteenCell.squareExchange X))
        (nativeK5ThirteenPastingRightThenLeft (NativeK5StructuralThirteenCell.squareExchange X)) →
       NativeK5CoreFourteenCell p
        (nativeK5ThirteenPastingLeftThenRight (NativeK5StructuralThirteenCell.squareExchange X))
        (nativeK5ThirteenPastingRightThenLeft (NativeK5StructuralThirteenCell.squareExchange X))) :=
  nativeK5ThirteenExchange_fourteenNoCoreRetraction
    (NativeK5StructuralThirteenCell.squareExchange X)
    (nativeK5ThirteenSquareExchange_pastingWord_ne X)

#print axioms NativeK5CoreFourteenCell
#print axioms NativeK5CoreFourteenCell.historyWord_sound
#print axioms NativeK5CoreFourteenCell.squareCount_sound
#print axioms NativeK5StructuralFourteenCell
#print axioms NativeK5StructuralFourteenCell.squareCount_sound
#print axioms nativeK5ThirteenExchange_fourteenRelativeNecessity
#print axioms nativeK5ThirteenSquareExchange_fourteenRelativeNecessity
#print axioms nativeK5ThirteenExchange_fourteenNoCoreRetraction
#print axioms nativeK5ThirteenSquareExchange_fourteenNoCoreRetraction

end
end Kuu.F112.Physical
