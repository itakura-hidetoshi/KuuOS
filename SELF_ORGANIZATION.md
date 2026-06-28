# KuuOS Self-Organization

KuuOSの自己改良における主経路は、v0.78から次の閉ループです。

```text
観測
→ 構造診断
→ 有限候補生成
→ isolated shadow比較
→ 暫定採用
→ 再観測
→ 保持またはsourceへrollback
```

この主経路は外部承認を要求しません。

候補の採用条件は、人の許可ではなく、保護座標の保存、有限候補性、全shadow contextでの非悪化、少なくとも一contextでの改善、再観測での非悪化です。

複数cycleは有限supervisorが接続します。

supervisorは、改善後stateを次cycleのsourceへ渡し、次のいずれかで停止します。

```text
NO_CHANGE
再観測rollback
最大cycle数
```

無制限な探索、無限実行、authority拡張、外部host stateの隠れた書換えは行いません。

実装と形式化は次を参照します。

```text
docs/KUUOS_SELF_ORGANIZING_IMPROVEMENT_LOOP_v0_78.md
runtime/kuuos_self_organization_types_v0_78.py
runtime/kuuos_self_organization_cycle_v0_78.py
runtime/kuuos_self_organization_supervisor_v0_78.py
formal/KUOS/WORLD/KuuOSSelfOrganizingImprovementLoopV0_78.lean
formal/KUOS/WORLD/KuuOSBoundedSelfOrganizationSupervisorV0_78.lean
```

v0.63、v0.69、v0.74の外部review系列は履歴的・別用途の経路として残りますが、v0.78の主経路には含まれません。
