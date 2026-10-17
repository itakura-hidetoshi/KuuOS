# KuuOS / 空OS

## 公開証明の継承と独立基礎

**Grayを空の基礎から外すことは、従来の証明を廃止することではありません。**
2026-10-17の修正で、従来の公開root **107個すべて**と元の集約importを現行パッケージへ戻しました。既存の定理本文・名前・仮定・Lean/mathlibの固定版は変更せず、証明実績を維持します。復旧の条件として利用者に再証明・再検証を要求しません。

- `lake build` / `lake build KuuOSFormal`: 従来の公開数学・runtime接続と独立Kuuを含む標準入口。
- `lake build KuuOSStrict`: Grayに依存しない独立Kuu基礎だけの入口。
- `lake build KUOS.<既存モジュール名>`: 従来の定理を元の名前のまま利用する入口。

**公開APIの継承と、独立基礎の依存境界は別の問題です。** `KUOS.*`を名前だけで旧式・無効と判定しません。Gray固有の定理も元の仮定下での証明記録は残しますが、独立Kuuの成立条件には戻しません。

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

標準入口は独立基礎と既存の公開証明を共存させます。Lakeは従来の107 rootsに`KuuOSStrict`と`Kuu`を加えた109 rootsを公開します。元の`formal/KUOS/`は現役の定理ソースです。

`legacy/v5.291/`は元のGit tree/blobと固定設定を保存する再現用コピーです。「保存先があるから現役から除外してよい」という扱いは撤回しました。通常のCI・登録確認・既存契約は現行ソースを参照します。履歴の再現を明示した場合だけ保存版を使います。

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

公開rootの欠落とCIの保存先への誤迂回を検出する回帰確認、独立Kuuの実際の直接・間接依存確認、保存版の変更防止を行います。**mathlibは新旧すべてのLean4形式化で積極的に利用します。** `import Mathlib` と `import Mathlib.*` はどちらも許可します。個別importはビルド時間短縮のための任意の推奨にすぎず、包括importの禁止条件ではありません。Grayからの独立性は実際の依存と定義により判断し、mathlibの使用や`KUOS.*`というnamespaceだけを理由に拒否しません。

ソース`fe9d720a36025a9fc259b70bf43b9f33b45891f2`では、[独立コアCI](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/38827903551)が45件の当時のテストと644ジョブのLeanビルドに成功しています。以後の追加テスト・設定を含む統合判定は[PR #2338](https://github.com/itakura-hidetoshi/KuuOS/pull/2338)の対象headに結び付くCI結果を参照してください。過去の成功を新headの成功として扱いません。

Leanは`v4.30.0-rc2`、mathlibはコミット済みmanifestに固定します。Lean4.31検証専用PR #1558は移行対象ではなく、マージしません。

## 証明の境界

独立コアは、空の商と**厳密な二次比較計算**です。非自明な証明関連3-cellを持つ大域ストリクト3圏や任意n圏の完成を意味しません。既存定理は元の型と仮定の下で成立した成果として継承します。新しい型との同値や追加のC60接続は、それとは別の数学的命題です。接続が未完成であることを理由に、既存成果の証明実績を取り消しません。

既存runtimeの回帰検証と、その振る舞いの新基礎による数学的再証明も別です。形式化の切替だけでLLMや臨床runtimeの挙動が自動的に変わったとは主張しません。

v5.291以前のGray曲率・non-lift等は、[旧README](docs/legacy/README-v5.291.md) と [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に保存された旧理論内の結果です。

## 設計と研究順序

[現行ROADMAP](ROADMAP.md) · [独立基礎の設計](docs/superpowers/specs/2026-10-16-independent-kuu-foundation-design.md) · [実装計画](docs/superpowers/plans/2026-10-16-independent-kuu-foundation.md) · [統合記録](docs/superpowers/plans/2026-10-16-independent-kuu-foundation-integration-results.md) · [実装時の境界](AGENTS.md)

空の推論順序は、観測と推測の分離、文脈・複数表示、関係・履歴、整合性、貼り合わせまたは障害、権限境界、必要な行為、再観測です。

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff)

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
