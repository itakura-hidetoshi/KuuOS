# KuuOS / 空OS — 独立基礎の現行ROADMAP

## v5.292：既存設計の切替

研究順序を **空の表示と境界 → 指定された交代 → 普遍商 → 厳密な合成・交換 → 高次貼り合わせ** に統一します。Gray/F51/F77由来の評価を空の原始定義にしません。現行の標準入口・公開Lake roots・説明・CI依存境界をこの順序へ変更します。

従来のF94–F97およびv5.291は、名前にKuu/Onlyを含んでいても間接的な旧Gray依存があります。その系統は独立基礎の完成ではありません。旧成果の一覧と証跡は [保存済み旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に分離し、現行の到達済み項目として混在させません。

## 現在の実装範囲

| 層 | 現在の実装 | 根拠 |
|---|---|---|
| 原始表示 | 任意の有向グラフの境界付き経路 | `Kuu.Raw` |
| 交代 | 平行経路の指定関係と合成・同値閉包 | `Kuu.Relations`, `Kuu.Replaceable`, `project_exact` |
| 普遍性 | 適合する任意観測の存在と一意性 | `observer_existsUnique` |
| 厳密な比較 | 関手・自然変換の単位・結合・middle-four等式 | `Kuu.Strict` |
| 比較の降下 | 自然変換を商上へ降下し合成・単位と一致 | `descendComparison_comp`, `descendComparison_id` |
| 文脈 | 元の文脈圏を保つ切片図式・総圏・制限 | `Kuu.Incidence` |
| 非自明性 | 指定しない並行経路は異なるまま | `quotient_not_indiscrete` |
| 依存境界 | 直接/間接の旧namespace依存を拒否 | `scripts/check_kuu_foundation.py` とPR CI |

上表はソース上の実装範囲です。対象コミットの成功はexact-head CIと`#print axioms`で別途確認します。CIで検証していないものを検証済みと呼びません。

## 今回変更する既存インターフェース

- 既存の `formal/KuuOSFormal.lean` は新コアへの入口へ置換。rootのLakeパッケージは `KuuOSFormal`, `KuuOSStrict`, `Kuu` のみを公開。
- 旧formal全体・旧Lake設定・固定manifestは `legacy/v5.291/` で別パッケージとして再現可能。元formal tree SHAは `d72e83b11ea316730ded81cd6d73612b2ce09919`。
- 旧`formal/KUOS/`は互換ミラーとしてのみ維持し、現行の定義・証明・ビルドには入れない。
- README/ROADMAPは現行設計として全面更新し、旧文書はGit blobを変えずに保存。
- 依存境界・旧snapshot保存を既存CIへ必須チェックとして追加。間接依存や未参照の現在ファイルも検査。

## 次の数学的義務

### 独立した高次セル

現在の関手・自然変換計算を、そのまま証明関連な大域ストリクト3圏と呼んではなりません。次は空の原始境界型を使った3-cell構文、source/targetのglobularity、すべての合成と交換を構成し、同一の型上で厳密等式を証明します。交換則を未証明の公理フィールドに置き換えるだけでは完了になりません。

### 真正な物理幾何との接続

元C60の60頂点・90辺・32面を新コアへ与えるには、旧Grayモジュールをimportするのではなく、必要な組合せ幾何を独立モジュールに切り出し、その元のincidenceと一致することを証明します。182個という個数だけの代用品や、全サイトを二つのBoolに縮約した関手を、全原ソースの再構成として扱いません。

### 既存の定理・runtimeの移植

旧F112の全rawソース結果を新基礎で再証明したわけではありません。各定理について新しい型・仮定・結論・依存先を追跡し、再証明できたものだけを現行側へ移します。旧F68等の曲率やnon-liftは旧理論内の独立な結果です。新理論への比較関手が未構成のまま同じ量と同一視しません。LLM/runtime/臨床等の実行挙動も独立に検証します。

## 再現とマージ条件

```bash
python3 scripts/run_kuu_foundation_check.py
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

新規コアに `sorry` / `admit` / 新公理 / `native_decide` を使わない。Lean v4.30.0-rc2とコミット済みmathlib manifestを維持する。対象headのStrict Lean・依存境界・Governance・MCP完了証跡を確認後のみマージする。Lean4.31 validation-only PR #1558は対象外。

**方針は「旧Grayの情報を必ず復元すること」ではなく、「空の指定関係に対し、どの観測と高次構成が整合して降下できるかを証明すること」です。**

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original license and attribution remain in effect.
