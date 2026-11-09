# Qi v5.59 — 任意自然数次数の反転祖先鎖と条件付き残余障害のLean4形式証明記録

正式記録日：2026-11-09 JST

## 1. Canonical正本と分離した検証

- Repository: `itakura-hidetoshi/KuuOS`、canonical branch: `main`。
- 継承元Qi v5.58正式HEAD: `af120df4322d6729548fc6427a9dddc106ab5ed6`、tree: `fe253b310d522523a3317c24663f7389cb8409ac`。
- [定理PR #3407](https://github.com/itakura-hidetoshi/KuuOS/pull/3407) **MERGED**。新規Leanモジュール `formal/KUOS/Architecture/QiWuxingGK5CHP77AncestorTowerConditionalShiftV5_59.lean`、324行、既存Leanへの削除・変更なし。
- [定理認証済みソース](https://github.com/itakura-hidetoshi/KuuOS/blob/059c378cb5deec5433e6fadb789ae876992d6e31/formal/KUOS/Architecture/QiWuxingGK5CHP77AncestorTowerConditionalShiftV5_59.lean)、HEAD `059c378cb5deec5433e6fadb789ae876992d6e31`、squash `658f8c31e9f482d50c0c5cccb4d90aabc84d5a46`、source/test-merge/squash共通tree `f10629e75995342bf13b6f9b370fbdd6cfbcbbb7`。
- [定理exact-source CI #42578124663](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42578124663) **completed SUCCESS**。Scoped Strict Lean **9,111/9,111**、Governance **5/5**、変更Lean error/warning **0/0**、正しいsource SHAを指すexact-head受領書 **2件SUCCESS**。
- [公開import PR #3408](https://github.com/itakura-hidetoshi/KuuOS/pull/3408) **MERGED**。source `91bb6346a646eb2122a0cf309815b8cde37d7ffe`、squash `075ed0952e5473dbb2807aa710b56f873a613c42`。source/test-merge/squash共通tree `ec523ea49c114e808cc9b3e42ff0b522f9da5849`。変更は `KuuOSFormal.lean` のimport **+1/-0** のみ。
- [公開exact-source CI #42578981707](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42578981707) **completed SUCCESS**。全公開集約 `KuuOSFormal` **10,372/10,372**、Governance **30/30**、新規15宣言の同じ公理結果、sorryAxなし、変更Lean error/warning **0/0**、exact-head受領書 **2件SUCCESS**。他の9 workflowは8件SUCCESS・1件SKIPPED。
- 文書専用PRのsource・検証・統合結果は当該PR自身のGitHub受領書で確定する。未確定の未来のsquash SHAやCI結果を本文で先取りしない。

## 2. 数学的定義：自然数次数の反転祖先鎖

真正の `SelectedContextualEighteen` 証拠Mを元16D fiber・真正17D二端点に保持して、`selectedAncestorTowerByProof` を**Mそのものに対する構造再帰**で構成し、`selectedAncestorTowerCount l r n M` を定義する。

```text
C₀(M) = 1                    -- 形式的seed。反転回数ではない
Cₙ₊₁(inherited old18) = 0
Cₙ₊₁(strict J) = 0
Cₙ₊₁(reverse M) = Cₙ₊₁(M) + Cₙ(M)
Cₙ₊₁(chain M L) = Cₙ₊₁(M) + Cₙ₊₁(L)
```

二つの元whiskering構成子について、元のType値の内部を消去したり同一視したりせず、証拠Mを構造的にたどる。**それぞれが内部のframed／16D文脈を変えうる**ので、再帰関数の文脈添字を外側に固定しない。C₀の定数性は独立の帰納証明で確定した。

`selectedAncestorTower_preservesOld` と `selectedAncestorTower_preservesNew` は、任意の `n : Nat` について、それぞれ元selected19の5構成子と独立したv5.50新比較7構成子でCₙが保存されることを形式証明する。新比較 `rawReverse` では同次数の比較帰納法仮定と、ひとつ低い次数の帰納法仮定を組み合わせる。

`selectedAncestorTowerOnOldQuotient` と `selectedAncestorTowerOnNewQuotient` で各次数を双方の商へ**別々に**降下し、`selectedAncestorTower_factorsOld` で元商から新商への射影との因子化を証明する。

## 3. 真正N→N証拠対における条件付き昇次数

既存の固定された真正17D端点Nと、その同じfiberに属する実在する18D値A,Bを入力として受け取る。

```text
L(A,B) = chain (reverse A) B
R(A,B) = chain A (reverse B)
```

任意の `n : Nat` について、

- `Cₙ(A)=Cₙ(B)` なら `Cₙ₊₁(L)=Cₙ₊₁(R)`。
- `Cₙ(A)≠Cₙ(B)` なら `Cₙ₊₁(L)≠Cₙ₊₁(R)`。
- `∀ k<n, Cₖ(A)=Cₖ(B)` なら `∀ k≤n, Cₖ(L)=Cₖ(R)`。
- `Cₙ(A)≠Cₙ(B)` なら、二点を結ぶ真正 `SelectedRawCongruentNineteen` 比較の `Nonempty` は否定される。

最後の結合結果が `selectedAncestorShift_residualGate`。局所的な観測一致を商クラス全体の同一性へ無条件に昇格しないための、**供給証拠対に条件付けた**一般次数の非比較定理である。すべての次数でそのような証拠対が実在する、という命題ではない。

## 4. 初回CIの不合格・全文照合・修正

初回HEAD `8adaae3103f3a00343ff75e27d7abf2fc87fc526` の [CI #42577509613](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/42577509613) は **FAILURE**。329行・16宣言の初稿で、再帰補助関数の `prev` を固定された16D文脈内の17D二端点にしか多相化していなかった。元v5.37 `SelectedContextualEighteen.whiskerRight` の内部証拠は異なるframed／16D文脈を取るため、再帰先Mへの適用が型不一致となった。これが後続の定義展開不成立と `rfl`・`congrArg` エラーへ波及し、未認証ソースには派生的 `sorryAx` が現れた。この初稿は認証も統合もしていない。

変更Lean全文、元v5.37のinductive構成子全文、元selected19、新v5.50比較7構成子、前段v5.58の証明と固定Leanのログを照合した。Lean公式[Structural Recursion](https://lean-lang.org/doc/reference/latest/Definitions/Recursive-Definitions/)も参照したが、公式最新文書は固定pinによる型検査の代替としない。

修正後HEAD `059c378cb5deec5433e6fadb789ae876992d6e31` は、`prev` を渡す固定文脈の計数stepではなく、真正元18D証拠そのものを構造帰納し、型付き各文脈に多相的な `Nat → Nat` を返す実装に変更した。次数0の定数性も別の帰納定理として保持。元証拠の構成子、仮定、比較のgenerator、fiberや端点、計算上限4,000,000 heartbeats、Lean/mathlib pinは変更していない。認証済み新規モジュールは324行・15宣言となった。

## 5. 新規15宣言の実公理監査

| 宣言（接頭辞 `selected`） | `#print axioms` 実結果 |
| --- | --- |
| `AncestorTowerByProof` | なし |
| `AncestorTowerCount` | なし |
| `AncestorTower_zero` | なし |
| `AncestorTower_preservesOld` | なし |
| `AncestorTower_preservesNew` | なし |
| `AncestorTowerOnOldQuotient` | なし |
| `AncestorTowerOnNewQuotient` | なし |
| `AncestorTower_factorsOld` | `Quot.sound` |
| `AncestorShiftLeft` | なし |
| `AncestorShiftRight` | なし |
| `AncestorShift_equalNext` | `propext, Quot.sound` |
| `AncestorShift_unequalNext` | `propext, Quot.sound` |
| `AncestorShift_prefixCompatible` | `propext, Quot.sound` |
| `AncestorShift_noNewComparison` | `propext, Quot.sound` |
| `AncestorShift_residualGate` | `propext, Quot.sound` |

厳密に全15宣言を確認済み。**公理不要9宣言、標準公理のみ6宣言、新規sorryAxなし、変更Lean error/warning 0/0**。公理監査は新規宣言に対するもので、過去の全宣言が一律に同じ公理集合という主張ではない。

## 6. 既証明障害とNO_DATA、次段

**既証明障害を保持**：Qi v5.51の真正旧18D証拠がある場合の旧LeftNestedCountと元19D正規代表の非降下定理は、本研究で解除されない。元I6全成分を新商の商不変量へ勝手に昇格しない。

**NO_DATA**：今回の自然数次数塔 `C₅` とv5.58までの個別定義された反転祖先五重鎖数との**形式的な同一性証明**、具体的な八変量共同観測の反例、すべての有限塔観測に対する実在証拠対の構成とその全次数反例、任意異端点fiberの非空性、異fiberへのwhiskering比較、20D gluing、独立WORLDやC60の数学的同一視、制度的実行権限。特に条件付きの `∀ n` を無条件の `∀ n, ∃ witness` へ置換しない。

**次段Qi v5.60候補**：個別に認証済みのC₁〜C₅と新towerの同値を真正raw証拠の全構成子で形式証明し、v5.58の具体的C₅差4対6を条件付き塔へ安全に接続する。その後に反転位置交換の反復列が任意の有限prefixに対する真正反例を与えるかを別途検証する。未認証を認証済みとはしない。

元Type値、公開root107、Lean `v4.30.0-rc2`、mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`、保護PR #1558 Draft/OPEN/未マージを維持。append-only／tighten-only／overwrite-forbidden／same-root。

空OS（KuuOS）、空OSライト、陰陽五行テンソル、周易テンソル、曼荼羅テンソルの著作権は板倉英俊（Hidetoshi Itakura）に帰属する。
