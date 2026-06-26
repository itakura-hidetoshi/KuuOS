# WORLD v0.59 四大相転移構造

## 対象

WORLD v0.59は、四大を物質の四分類として扱わない。

四大を、WORLDの観測可能な解析構造を読むための四つの座標として導入する。

```text
地大 = 構造安定性
水大 = 相関形成
火大 = 粗視化後の不可逆情報損失
風大 = 可逆な物理時間輸送
```

この層はread-onlyな診断層である。

WORLD状態を変更しない。

ObserveOSの観測を代行しない。

PlanOSまたはActOSへ権限を付与しない。

## 既存WORLD解析脊柱との接続

四大は新しい独立オントロジーではない。

既存のWORLD解析脊柱に対する構造化された読み方である。

```text
Araki relative entropy
→ bounded exponential arcs
→ mixed Araki Hessian
→ BKM pairing
→ vacuum quantum Fisher metric
→ completed-Hilbert excitation Gram form
→ OS reflection form
```

地大と水大は、この既存脊柱から直接定義する。

火大と風大は、物理的意味を混同しないために別の入力として保持する。

## 地大

**地大**は、基準状態からの変形に対する情報幾何学的剛性である。

有界自己共役生成子 \(h\) に対して、地大を次で定義する。

```text
Earth(h) = H_Araki(h,h)
```

v0.56では、この量はBKM pairing、量子Fisher計量、物理Hilbert励起のGram形式、OS反射形式の実部へ輸送済みである。

したがって地大は、抽象的な比喩ではなく、既存の非負二次形式を参照する。

## 水大

**水大**は、完成物理Hilbert空間上で二つの励起を結ぶ相関形式である。

対角成分を次で定義する。

```text
Water(h) = Re ⟨Ψ_h, Ψ_h⟩
```

v0.56の輸送定理により、同じ生成子について次が成立する。

```text
Earth(h) = Water(h)
```

この等式は、地大と水大が同じ概念であることを意味しない。

地大は変形コストとして読む。

水大は物理励起の相関強度として読む。

同じ二次形式に対する二つの役割である。

## 風大

**風大**は、物理Hilbert担体上の可逆な時間輸送である。

v0.59では、実時間発展を次の公理を満たす写像として受け取る。

```text
Air(0) = id
Air(s+t) = Air(s) ∘ Air(t)
⟨Air(t)ψ, Air(t)φ⟩ = ⟨ψ,φ⟩
```

この条件から、各時刻の写像は逆時間写像を持つ。

```text
Air(-t)(Air(t)ψ) = ψ
```

風大は、OS Euclidean時間の収縮ではない。

風大は、再構成後の可逆な物理時間発展に対応する。

## 火大

**火大**は、閉鎖系の基礎Hamiltonian時間発展そのものではない。

火大は、部分系への制限、条件付き期待値、環境消去、有限分解能による粗視化の後に現れる非負の情報損失である。

v0.59では、火大を次の非負診断量として受け取る。

```text
Fire(h) ≥ 0
```

この値を特定の相対エントロピー損失やDirichlet形式へ同定するには、追加の量子Markovまたは粗視化モデルが必要である。

したがってv0.59は、火大の非負性と射程境界だけを固定する。

## 四大診断テンソル

各生成子 \(h\) と時刻 \(t\) に対して、次の四成分を構成する。

```text
T_4G(i,t,h)
  = (
      Earth(h),
      Water(h),
      Fire(h),
      ||Air(t)Ψ_h - Ψ_h||²
    )
```

全成分は非負である。

地大成分と水大成分は、v0.56の物理輸送定理により厳密に一致する。

風大成分は、可逆流が対象励起をどの程度移動させたかを測る。

時刻零では風大成分は零になる。

## 相転移との関係

四大成分の単なる変化だけでは、物理的相転移を宣言しない。

相転移には、自由エネルギーの非解析性、極端状態構造の変化、HamiltonianまたはLiouvillianのギャップ閉鎖、固定点代数の変化など、別途指定された非正則性が必要である。

四大診断は、その非正則性が構造安定性、相関、不可逆性、可逆輸送のどこへ強く現れるかを整理する。

## WORLD内の位置

```text
WORLD state and reference structure
→ Araki Hessian and BKM geometry
→ physical Hilbert excitation correlation
→ four-great read-only diagnostic
→ optional ObserveOS evidence intake
```

四大診断は観測候補を整理できる。

四大診断は観測receiptを生成しない。

四大診断は検証を完了しない。

四大診断は介入を許可しない。

## 証明済み範囲

Leanが直接証明する範囲は次である。

```text
Earth(h) = Water(h)
Earth(h) ≥ 0
Water(h) ≥ 0
Fire(h) ≥ 0
AirActivity(t,h) ≥ 0
AirActivity(0,h) = 0
Air(-t)(Air(t)ψ) = ψ
Air preserves physical inner products
```

地大と水大の等式は、v0.56で証明済みのAraki Hessianから物理励起Gram形式への輸送を再利用する。

## 固定境界

```text
four-great diagnostic != ontology
four-great component != physical substance
Earth != solid matter
Water != liquid matter
Fire != temperature
Air != gaseous matter
OS Euclidean contraction != physical Fire
modular time != physical time
Fire diagnostic != basic closed-system irreversibility
phase-component change != phase transition
read-only diagnosis != observation ownership
read-only diagnosis != verification
read-only diagnosis != execution authority
```

## 次段階

次段階では、忠実正常状態を保存する量子Markov半群を導入する。

その場合、火大を非可換Dirichlet形式の正自己共役部分へ、風大を基準状態内積に関する反自己共役部分へ同定できる。

さらに、固定点代数、Araki相対エントロピー損失、Petz回復可能性へ接続する。
