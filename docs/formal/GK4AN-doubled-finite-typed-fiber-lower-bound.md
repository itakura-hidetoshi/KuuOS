# F112-P94D3GK4AN — 真正旧類 qₖ の有限下界 2k+1 と可算性

**2026-10-31 JST／Lean4定理検証済／canonical main正本。**

GK4AKが各到達旧類 `q_k` に構成した `k+1` 個の本物のF54経路類を、GK4AMの奇数半backtrack構成を全位置に移動させることで **`2k+1` 個** へ拡張した。新しい有限族は同一の元F45完全依存型自己Homに属し、同一の旧 `K_AG` 類へ忘却される。第二行列は元F55/P92B/構造seamのType値証拠を保存する既存GK4AH値であり、元の比較証拠を新造しない。

## 1．authoritative exact-source receipt

| 項目 | GitHub MCP確認 |
|---|---|
| 定理PR | [#2813](https://github.com/itakura-hidetoshi/KuuOS/pull/2813) — MERGED |
| 最終exact-source HEAD | `7b122beae70e0d069c0b922f7b429d0da1b930f8` |
| CI実checkout test-merge SHA | `3c8699e452fbf84598d7339118c02c1cddc04e53` |
| source / CI / squash 共通 Git tree | `70653a884faf43a83f9de7db846d858576b366e3` |
| 定理squash SHA、マージ直後main HEAD | `d95fdece191605e413423c6efede04ac739b611c` |
| 最終CI | [#41193236442](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41193236442) terminal SUCCESS |
| Strict Lean | **3769/3769 SUCCESS** |
| Governance | **5/5 SUCCESS** |
| 新規公理表示 | **16宣言**、標準3 `propext`、`Classical.choice`、`Quot.sound` 以内 |
| `sorryAx`、変更Lean warning/error | **0、0/0** |
| 変更ファイル | **append-only Lean 2ファイル、既存Lean変更0** |
| 固定環境 | Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6` |
| 保護 | PR #1558 Draft／OPEN／未マージ、公開root107、Gray非再導入 |

## 2．偶数族 — 既存GK4AK

真正F54の二Nat cast自己経路を `C`、LocalRotationの前後backtrackを `B` とし、`P=B^6` と置く。

```text
Even(j,d) = P^j ; C ; P^(2d) ; C ; P^j
j+d = k
0 ≤ j ≤ k
```

元四成分観測とGK4AF第一行列は `q_k` に一致し、GK4AH第二行列の線形decoder

```text
L([[a,b],[c,e]]) = 4b + 2e - 2a - c
L(Even(j,d))    = 8 - 192d
```

から `k+1` 個が相異なる。

## 3．奇数族 — GK4ANの本物のF54経路

[GK4ANShiftedOddFamily.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANShiftedOddFamily.lean) で `H=B³` を用いる。

```text
Odd(j,d) = P^j ; H ; C ; P^(2d+1) ; C ; H ; P^j
j+d+1 = k
0 ≤ j < k
```

これは既存GK4AMの真正 `V_d=H C P^(2d+1) C H` を元F54の `P^j` で前後から挟んだ**型付き自己経路**。古いフルGK4AG観測は `q_k` と一致する。GK4AFで `H=-I`、`P=I` であることも元Type値の歴史を消去する主張ではない。

新GK4AH decoderは任意の `j,d` で

```text
L(Odd(j,d)) = -88 - 192d
```

を満たす。これを用いて、同じ `q_k` の中の奇数族 `Fin k` は単射となる。旧偶数族の decoder `8-192d'` と同一なら `192(d'-d)=96` を要求するため、**偶奇族間の衝突も不可能**。各偶奇族の値は全て真正の到達第二行列であり、任意の抽象整数行列を仮定していない。

## 4．主定理と物理C60北側の無条件特殊化

[GK4ANDoubledFiniteFibers.lean](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK4ANDoubledFiniteFibers.lean) では、固定した元F54 LocalRotation証人と任意の `k:Nat` に対し、

```text
(Fin(k+1) ⊕ Fin k) ↪ Fiber(q_k)
Fin(2*k+1) ↪ Fiber(q_k)
Countable(Fiber(q_k))
```

をLean4で証明。固定mathlibの `finSumFinEquiv` で型の同型を取り、`Fin(2*k+1)` を本物の忘却ファイバーへ埋め込む。定理名は `nativeGK4AN2kPlusOneFiberEmbedding` と `nativeGK4AN_doubled_finite_countable_fiber`。真正C60北側六角形への無条件特殊化は `nativeGK4ANPhysicalNorth_doubled_finite_countable_fiber`。

| k | GK4AK下界 | GK4AN下界 |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 2 | 3 |
| 2 | 3 | 5 |
| 3 | 4 | 7 |
| 4 | 5 | 9 |

重要：ここでの数値は **各q_kで構成した相異なる点の数の下界** であって、ファイバーの全体の濃度や完全正規形ではない。異なるkの`q_k`はGK4AKにより相異なる。

## 5．CIにより修正したLean elaboration上の問題

最初のCIでは、最後の存在定理のSection変数 `rot` が定理文の型に現れておらず、自動的に一般化されずに証明内で `Unknown identifier rot` となった。同じ理由でC60特殊化の引数がずれた。既存ファイルを変更せず、GK4ANの新ファイル内で

```lean
theorem nativeGK4AN_doubled_finite_countable_fiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) (k : Nat) :
    ...
```

と本来の真正Type値仮定を明示し、**最終exact-source CI #41193236442で3769/3769 SUCCESS** と確認した。失敗した初回CIを成功証拠に用いない。

## 6．保留する研究境界／GK4AO候補

GK4ANはGK4AKの任意大有限下界を厳密に強化し、GK4ALの全ファイバー可算性、GK4AMの `∀k>0, ¬FamilyCovers(k)` と両立する。

未証明のまま保持する事項：**単一固定旧qの無限ファイバー**、`2k+1` 族が全体を尽くすこと、全整数行列の到達可能性／完全到達制約、`S→K_AI`全域忠実性／残余非忠実性、元P92B Q自体の結合律／左右単位、歴史的完全型付き同値、真正14D無条件Countable、19D filler、global strict、Gray、hyperdescent。旧値の一致は元Type値証拠ではない。

次段階では、固定qの無限性をさらに独立検討するとともに、GK4AH整数行列の行列式・合同制約など、実際に到達する値の必要条件を調べる。

© 2026 板倉英俊 / Hidetoshi Itakura。Apache-2.0。
