# KuuOS / 空OS — 既証明成果を継承する独立基礎ROADMAP

## 2026-10-17：公開root一括除外の撤回

107個の従来公開rootと元の集約importを現行パッケージへ復帰。非Grayの縁起・局所化・障害・履歴・解析・runtime接続の証明を現役として継承し、再証明・再承認を復帰条件にしません。Grayを独立Kuuの前提にしない方針は維持します。以下の過去の移行記録はこの修正に従って読みます。

## v5.292：既存設計の切替

研究順序は **空の表示と境界 → 指定された交代 → 普遍商 → 厳密な合成・交換 → 高次貼り合わせ** です。Gray/F51/F77由来の評価を空の原始定義にしません。

F94–F97等の旧Gray依存がある宣言は、元の型と仮定を保って現役成果として維持します。ただしGrayを新しい空の定義には使いません。歴史的な構成・証跡は [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に保存します。

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

**公式入口は`KuuOSFormal`一つです。** 従来の集約importと既存107公開rootを維持し、新しいKuuも同じ正本から利用します。`KuuOSStrict`・`Kuu`は内部モジュールであり、別の公開root・定理体系・権威にはしません。対象を限定したCIコンパイルは時間短縮だけの都合です。元formal tree `d72e83b11ea316730ded81cd6d73612b2ce09919`の保存版は変更しません。

通常の既存CI・登録チェック・契約は現行の`formal/`・`lakefile.toml`へ戻します。18個の記録済み形式契約は元の現行参照を維持し、自動修復権限を追加しません。従来の約120という概数ではなく、元設定の107 rootsで欠落を検出します。

依存境界は実際のimportと使用構造で確認し、`KUOS.*`を一律禁止しません。修復に伴う設定の確認は実装側の責任であり、利用者に既存証明のやり直しを求めません。

## mathlibの利用方針（2026-10-17改訂）

Grayを空の原始定義から外す方針と、mathlibを使う方針は独立です。mathlibの圏論・双圏・simplicial set・局所化・ホモトピー・代数・位相の定理を積極的に再利用します。`import Mathlib` と `import Mathlib.CategoryTheory.Quotient` など個別モジュール指定の双方を認め、前者をCIで禁止しません。ビルド効率のために個別importを選ぶことは任意であり、証明の数学的正当性や公開権威の条件としません。独立Kuuに持ち込まないものは旧Gray/F51/F77を空の成立に不可欠とする実際の依存であり、mathlibではありません。既存定理の再証明は要求せず、元のLean/mathlib固定版を維持します。

## 次の数学的義務

### 独立した高次セル

関手・自然変換の厳密2次比較を、そのまま証明関連な大域ストリクト3圏とは呼びません。空の原始境界型を使う3-cell構文、source/targetのglobularity、合成と交換を構成し、型の一致を保って厳密等式を証明することが次の義務です。交換則を未証明の公理フィールドに置くだけでは完了になりません。

### 真正な物理幾何との接続

C60の60頂点・90辺・32面の組合せ幾何を旧Grayモジュールから独立に切り出し、元のincidenceとの一致を証明します。182個という個数だけの代用品や、全サイトを二つのBoolへ縮約した関手を全原ソースの再構成とは扱いません。

### 既存の定理・runtimeの移植

既存の全rawソース結果は元の型と仮定の下で成立した証明として維持します。新旧の型を結ぶ追加命題が必要な場合は、その接続だけを証明します。既存証明そのものを未証明扱いに戻しません。旧F68の曲率やnon-liftを、新理論との比較なしに同じ量として同一視しません。runtimeの回帰テスト成功と、runtimeの新しい形式的正当化も区別します。

## 再現と統合条件

```bash
python3 scripts/run_kuu_foundation_check.py
lake build KuuOSFormal
```

ライブラリ設定`leanOptions = { warningAsError = true }`を維持します。新規コアに`sorry`・`admit`・新公理・`native_decide`を使いません。Lean v4.30.0-rc2と固定mathlib manifestを変更しません。

新規変更の動作確認と既存の証明実績を区別します。公開rootの修復を、既証明成果の再承認待ちにしません。Lean4.31 validation-only PR #1558は対象外です。

**目的は旧Grayの情報を必ず復元することではなく、空の指定関係に対して観測と高次構成がどう整合し、降下できるかを証明することです。**

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original license and attribution remain in effect.
