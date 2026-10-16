# KuuOS / 空OS

## 現行設計：空から直接構成する独立した基礎

**v5.292は既存の数学基礎の切替です。Grayの厳密化を空の定義にはしません。** 原始データは境界付きの表示グラフと、平行な表示経路の間に指定する交代関係です。型の異なる境界を同一視せず、指定関係の合成閉包・同値閉包から空の商圏を構成します。

```text
境界付き生成グラフ + 指定された表示交代
                 ↓
      空の普遍商（Kuu.Presentation）
                 ↓
  関手・自然変換の厳密な合成と交換（Kuu.Strict）
                 ↓
   文脈圏に沿う切片図式・総圏（Kuu.Incidence）
```

GrayGrade・GradedThreeCell・F51・F77・Gray位相再構成を、この列の定義・型・証明に持ち込みません。過去のGray理論との比較は別の任意研究であり、現行の空の成立条件ではありません。

## 既存実装の切替

標準入口 `formal/KuuOSFormal.lean` とLake設定を置き換えました。`lake build` は、`KuuOSFormal`・`KuuOSStrict`・`Kuu`のみを公開する現在のパッケージをビルドします。旧KUOS公開rootsは現行設定に含めません。

旧formal全体と固定設定は、元のGit tree/blobを変えずに [legacy/v5.291](legacy/v5.291/README.md) へ保存しました。旧`formal/KUOS/`は過去の参照パス向けの互換ミラーですが、現行ビルドや新しい基礎の依存先ではありません。**名称だけ空へ変更して旧Gray定義を使い続ける構成ではありません。**

既存の111件のworkflow、69件の検証スクリプト、14件のmanifest、2件のruntime接続を明示的な現行／旧パッケージ境界へ変更しています。さらにv0.86〜v0.95の読み取り専用契約10件を補い、記録済みの歴史的形式契約18件すべてに`formal_package`を指定しました。これらの指定は自動修復権限を追加しません。将来追加される現行Kuuの契約を旧系統へ自動分類しません。

## 現在のコードが扱う数学

| モジュール | 内容 |
|---|---|
| [Kuu.Presentation](formal/Kuu/Presentation.lean) | 境界付きグラフ、指定関係と最小の合成・同値閉包、正確な商射影、文脈中の交代、適合観測の一意因子化 |
| [Kuu.Strict](formal/Kuu/Strict.lean) | 実関手・自然変換の単位、結合、水平・垂直合成、middle-fourの厳密等式、比較の降下 |
| [Kuu.Incidence](formal/Kuu/Incidence.lean) | 与えられた文脈圏を保つ切片Cat値図式、Grothendieck総圏、三角形と制限の合成一致 |
| [Kuu.Checks](formal/Kuu/Checks.lean) | 指定しない異なる平行経路の非崩壊と、指定した交代が有効になる具体例 |

交代可能性は外部観測の核を原始定義とせず、指定された表示関係から生成します。観測の利用可能性は、その観測が交代関係を尊重するかによって判定します。

## 検証

```bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 固定依存のキャッシュが必要な場合
lake build KuuOSFormal
```

警告のエラー化は、Lakeライブラリの正式な設定`leanOptions = { warningAsError = true }`に固定しています。`-KleanArgs`という任意の設定キーだけに依存しません。Leanソース内の`sorry`・`admit`・新公理・`native_decide`は依存境界検査でも拒否します。

48件の回帰テスト、固定された移行範囲の残差検査、現行全モジュールの直接・間接import検査、旧formalのtree/blob保存検査を実行します。未参照の`formal/Kuu/`ファイルも検査対象です。旧rootsの再導入や包括的`import Mathlib`も失敗にします。これらを既存のPR Governance CIへ登録しています。

ソース`fe9d720a36025a9fc259b70bf43b9f33b45891f2`では、[独立コアCI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38827903551)が45件の当時のテストと644ジョブのLeanビルドに成功しています。以後の追加テスト・設定を含む統合判定は[PR #2338](https://github.com/itakura-hidetoshi/KuuOS/pull/2338)の対象headに結び付くCI結果を参照してください。過去の成功を新headの成功として扱いません。

Leanは`v4.30.0-rc2`、mathlibはコミット済みmanifestに固定します。Lean4.31検証専用PR #1558は移行対象ではなく、マージしません。

## 証明の境界

独立コアは、空の商と**厳密な二次比較計算**です。非自明な証明関連3-cellを持つ大域ストリクト3圏や任意n圏の完成を意味しません。旧F112の全rawソース定理や真正C60幾何との全接続を、新基礎で再証明済みとは扱いません。これらは旧Gray定義へ戻らず、新しい境界型と構成から証明します。

既存runtimeの回帰検証と、その振る舞いの新基礎による数学的再証明も別です。形式化の切替だけでLLMや臨床runtimeの挙動が自動的に変わったとは主張しません。

v5.291以前のGray曲率・non-lift等は、[旧README](docs/legacy/README-v5.291.md) と [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に保存された旧理論内の結果です。

## 設計と研究順序

[現行ROADMAP](ROADMAP.md) · [独立基礎の設計](docs/superpowers/specs/2026-10-16-independent-kuu-foundation-design.md) · [実装計画](docs/superpowers/plans/2026-10-16-independent-kuu-foundation.md) · [統合記録](docs/superpowers/plans/2026-10-16-independent-kuu-foundation-integration-results.md) · [実装時の境界](AGENTS.md)

空の推論順序は、観測と推測の分離、文脈・複数表示、関係・履歴、整合性、貼り合わせまたは障害、権限境界、必要な行為、再観測です。

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff)

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
