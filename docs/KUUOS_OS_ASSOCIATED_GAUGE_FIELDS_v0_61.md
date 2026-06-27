# KuuOS OS-Associated Gauge Fields v0.61

## 状態

v0.61は、ObserveOS、VerifyOS、MemoryOSを、v0.60の憲法ゲージ束に付随する三つの局所場として接続します。

この層は既存OSのcommitted stateを読取り、検証済みの状態だけをゲージ場へ射影します。

既存state、ledger、memory capsule、production runtimeは変更しません。

## 場の直和分解

12次元の有限fiberを、四つの不変部分空間へ分解します。

```text
V
=
V_constitutional
⊕ V_epistemic
⊕ V_verification
⊕ V_memory
```

座標は次のように固定します。

```text
V_constitutional:
  authority
  audit
  provenance
  rollback

V_epistemic:
  evidence_support
  uncertainty
  contradiction

V_verification:
  criterion_coverage
  verification_debt

V_memory:
  history_depth
  residue_load
  predictive_uncertainty
```

許容ゲージ変換は、憲法座標を点ごとに固定し、認識、検証、記憶の各部分空間を集合として保存します。

異なる意味チャネル間の座標交換は拒否します。

## ObserveOS場

ObserveOS場は、committed observation stateから構成します。

既存の`validate_observe_state`を通過し、`current_phase = commit`かつ`observation_recorded = true`であることを要求します。

認識チャネルには、coverage、freshness、provenance、calibration、completeness、conflictから得たsupport、uncertainty、contradictionを配置します。

ObserveOSはverification authorityを持たないため、verification debtは保持します。

## VerifyOS場

VerifyOS場は、committed verification stateから構成します。

既存の`validate_verify_state`を通過し、`current_phase = commit`かつ`verification_recorded = true`であることを要求します。

corroboration reportからevidence supportとcriterion coverageを構成し、PASSED、FAILED、INDETERMINATEのrouteをuncertaintyとcontradictionへ反映します。

この射影はverification resultをtruthへ昇格しません。

## MemoryOS場

MemoryOS場は、v0.37 predictive shielded memory capsuleから構成します。

既存の`validate_predictive_shielded_memory_capsule`を通過することを要求します。

記憶チャネルには、capsule sequence、contradiction residue、predictive uncertaintyを配置します。

semantic consolidationとprocedural reuseは候補のままであり、memory overwriteやexecution authorityを生成しません。

## 厳密なsource binding

三場を一つのbundleへ結合するとき、次を要求します。

```text
VerifyOS.source_observe_state_digest
=
ObserveOS.observe_state_digest
```

さらに、MemoryOSの少なくとも一つのmemory recordが、VerifyOSの完全な`verify_state_digest`をsource digestとして保持しなければなりません。

したがって、単に同じlineage labelを持つだけでは結合できません。

## 曲率分解

三つの有向移送について、共変残差を計算します。

```text
R_OV = U_OV Phi_Observe - Phi_Verify
R_VM = U_VM Phi_Verify - Phi_Memory
R_MO = U_MO Phi_Memory - Phi_Observe
```

各残差の対応部分空間上の二乗ノルムを、次の曲率として記録します。

```text
F_epistemic     = ||P_epistemic R_OV||^2
F_verification  = ||P_verification R_VM||^2
F_memory_return = ||P_memory R_MO||^2
```

全曲率は三者の和です。

曲率を単一スカラーへ先に潰さないため、認識上の不一致、検証上の未解決、履歴帰還のずれを区別できます。

## 記憶ホロノミー

閉路を次のように取ります。

```text
ObserveOS
→ VerifyOS
→ MemoryOS
→ ObserveOS
```

閉路移送は、MemoryOSを経由した履歴依存性を表します。

```text
H_memory
=
U_MO U_VM U_OV
```

局所ゲージ変換後はObserveOSの基点で共役変換されます。

```text
H'_memory
=
g_Observe H_memory g_Observe^-1
```

したがって、正規化traceから作るWilson型観測量はゲージ不変です。

v0.61では、Wilson観測量、ホロノミーdefect、記憶チャネル上のreturn energyをreceiptへ保存します。

## Lean形式化

Leanでは、まず共変残差について次を証明します。

```text
R(A^g, Phi^g; x, y)
=
g_y R(A, Phi; x, y)
```

各チャネル汎関数がゲージ作用に不変なら、対応する曲率も不変です。

この抽象定理から、ObserveOSからVerifyOS、VerifyOSからMemoryOS、MemoryOSからObserveOSの三曲率の同時不変性を導きます。

記憶三角ホロノミーの共役変換とclass function不変性も直接証明します。

## 実装

```text
runtime/kuuos_os_gauge_field_types_v0_61.py
runtime/kuuos_os_associated_fields_v0_61.py
runtime/kuuos_os_curvature_holonomy_v0_61.py
tests/test_kuuos_os_associated_fields_v0_61.py
tests/test_kuuos_os_curvature_holonomy_v0_61.py
scripts/check_kuuos_os_associated_gauge_fields_v0_61.py
formal/KUOS/WORLD/KuuOSOSAssociatedGaugeFieldsV0_61.lean
formal/KuuOSFormalV0_61.lean
```

## 境界

```text
projection is read-only
source validators are mandatory
source digests are preserved
cross-channel gauge transforms are forbidden
verification is not truth
memory projection does not overwrite
production mutation is not performed
```

## 非主張

v0.61は次を主張しません。

- 連続主束上の完全な微分幾何
- 接続の自律学習
- 曲率最小化によるtruth獲得
- 記憶ホロノミーによる因果性の証明
- production stateの自動変更
- Lean成功だけによる外部受理
