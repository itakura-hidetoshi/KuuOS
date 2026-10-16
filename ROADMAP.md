# KuuOS / 空OS — 独立基礎の現行ROADMAP

## v5.292：既存設計の切替

研究順序は **空の表示と境界 → 指定された交代 → 普遍商 → 厳密な合成・交換 → 高次貼り合わせ** です。Gray/F51/F77由来の評価を空の原始定義にしません。

F94–F97およびv5.291は、名称にKuu/Onlyを含んでいても間接的な旧Gray依存があります。その系統を独立基礎の完成とは扱いません。旧成果と証跡は [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に分離します。

## 独立した実装範囲

| 層 | 実装 | 根拠 |
|---|---|---|
| 原始表示 | 有向グラフの境界付き経路 | `Kuu.Raw` |
| 交代 | 平行経路の指定関係と合成・同値閉包 | `Kuu.Relations`, `Kuu.Replaceable`, `project_exact` |
| 普遍性 | 適合観測の存在と一意性 | `observer_existsUnique` |
| 厳密な比較 | 関手・自然変換の単位・結合・middle-four | `Kuu.Strict` |
| 比較の降下 | 単位・合成と整合する自然変換の降下 | `descendComparison_comp`, `descendComparison_id` |
| 文脈 | 与えられた文脈圏上の切片図式・総圏・制限 | `Kuu.Incidence` |
| 非自明性 | 指定しない平行経路の非崩壊 | `quotient_not_indiscrete` |

ソース`fe9d720a36025a9fc259b70bf43b9f33b45891f2`の独立CIは644ジョブ成功、21件の`#print axioms`にsorryAxなしです。後続headの検証をこの結果で代用しません。

## 既存インターフェースと検証の切替

標準入口とLake公開rootsは`KuuOSFormal`, `KuuOSStrict`, `Kuu`だけです。旧formal全体と固定設定は`legacy/v5.291/`に保存し、元formal tree SHA `d72e83b11ea316730ded81cd6d73612b2ce09919`を維持します。旧`formal/KUOS/`は互換ミラーであり、現行基礎の依存先ではありません。

既存の111workflow、69検証スクリプト、14manifest、2runtimeファイルの接続を切り替え、固定196ファイルの移行範囲に対して残差を検査します。その後、v0.86〜v0.95の読み取り専用形式契約10件のパッケージ指定も補い、記録済み18契約の指定漏れを別の回帰テストで拒否します。パッケージ指定は自動修復への参加や権限の拡大ではありません。

48件の独立基礎・パッケージ境界・移行・契約指定・コンパイラ設定の回帰テストを実行します。旧定理の検査を削除したり、現行入口へ旧importを戻したりしてCIを成功させません。警告のエラー化は`lakefile.toml`の実コンパイラ設定で保証します。

## 次の数学的義務

### 独立した高次セル

関手・自然変換の厳密2次比較を、そのまま証明関連な大域ストリクト3圏とは呼びません。空の原始境界型を使う3-cell構文、source/targetのglobularity、合成と交換を構成し、型の一致を保って厳密等式を証明することが次の義務です。交換則を未証明の公理フィールドに置くだけでは完了になりません。

### 真正な物理幾何との接続

C60の60頂点・90辺・32面の組合せ幾何を旧Grayモジュールから独立に切り出し、元のincidenceとの一致を証明します。182個という個数だけの代用品や、全サイトを二つのBoolへ縮約した関手を全原ソースの再構成とは扱いません。

### 既存の定理・runtimeの移植

旧F112の全rawソース結果を再証明済みとはしません。各定理の新しい型・仮定・結論を追跡し、再証明したものだけを現行側へ移します。旧F68の曲率やnon-liftを、新理論との比較なしに同じ量として同一視しません。runtimeの回帰テスト成功と、runtimeの新しい形式的正当化も区別します。

## 再現と統合条件

```bash
python3 scripts/run_kuu_foundation_check.py
lake build KuuOSFormal
```

ライブラリ設定`leanOptions = { warningAsError = true }`を維持します。新規コアに`sorry`・`admit`・新公理・`native_decide`を使いません。Lean v4.30.0-rc2と固定mathlib manifestを変更しません。

[PR #2338](https://github.com/itakura-hidetoshi/KuuOS/pull/2338)のexact-head Lean、静的検査、runtime、選択された回帰検査、required gate、必要なMCP証跡の成功が統合条件です。Lean4.31 validation-only PR #1558は対象外です。

**目的は旧Grayの情報を必ず復元することではなく、空の指定関係に対して観測と高次構成がどう整合し、降下できるかを証明することです。**

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original license and attribution remain in effect.
