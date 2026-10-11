# F59-F22: 老子・王弼・列子・周敦頤・朱子学を再読する — C60 / 空OS（v5.170）

**2026-10-12 JST · Source-grounded interpretive bridge · No theological/clinical/theorem authority**

## 0. Historical reading versus formal theorem

This note records a philosophically useful **interpretation**, not a claim
that Chinese classical authors established a modern mathematical theorem,
a unique Euclidean C60–I Ching bijection, a quantum field theory, or a
proven clinical model.

We distinguish (i) primary text, (ii) interpretive thesis, (iii) actual
Lean-verified object, and (iv) mathematics still requiring construction.
In particular, the *unverified philosophical interpretation* can be
revisited without changing the mathematical identity of the canonical
formal objects.

When discussing "列子", use the received *Liezi*, not an unsupported
attribution of every passage to the historical Lie Yukou. The received
text's date and editorial history are debated.

## 1. 老子：道・反・沖和 are processes, not a frozen root element

**Texts.** *Daodejing* (Wang Bi edition), ch. 40 and ch. 42:
- Ch. 40: the Dao's movement is described through return/reversal
  (反) and its operation through weakness/flexibility (弱).
- Ch. 42: the sequence Dao→one→two→three→myriad beings and
  yin–yang in relation, with *chongqi* (沖氣) as harmony.

Originals:
- https://zh.wikisource.org/zh-hant/道德經_(王弼本)
- https://ctext.org/dao-de-jing/zh

**KuuOS reading:** the meaningful mathematical carrier is **process,
reversal and compatible return**, not a universal permanent
"Dao = chosen north vertex" identity. The poles of the *icosahedral
seed* are centers of two of the real C60 pentagons. Their
local-real structures `κ_N`, `κ_S` are **frame choices**, never
absolute fixed North=Yang / South=Yin essences. The same local
conjugation can appear as a different manifestation under a
different chart.

**Constructive test**: the actual complex `i)-multiplication
`T(z)=i*z` intertwines `κ_N` and `κ_S` in the chosen paired
polar frame, `κ_S ∘ T = T ∘ κ_N`. The inverse map uses `-i`.
The concrete proof is a new mathematical lemma, not a proof that
Laozi intended complex numbers.

"Dao" and Buddhist *śūnyatā* ("空") may be fruitfully compared,
but are neither textual synonyms nor mathematically equal
objects by assertion.

## 1A. 王弼（226–249）：『老子注』『周易注』『周易略例』の独立した軸

**王弼は老子・列子・朱熹の脚注ではない。** 三国魏の王弼の
`老子注` と `周易略例` は、老子の「無」の理解と『周易』の
象・言・意の解釈を架橋する重要な原典である。周敦頤（宋）の
`太極圖說` および朱熹（宋）の注釈とは著者・時代・主張を
区別して扱う。

### 1A.1 原文→読み下し→現代訳：王弼『老子注』第一章

- **王弼注 原文**：`凡有皆始於無`。
- **読み下し**：凡そ有は皆、無より始まる。
- **解釈**：「有」として形をとったものの生成条件を「無」との
  関係から考える。無を空間的な虚無物質または量子真空と
  見なすものではない。
- **一次資料**：
  https://www.chineseclassic.com/LauTzu/LaoTzu_wongbee/ch01.htm

**KuuOSへの接続**：C60の北極・南極、32面、90辺、64個の
符号化像の**どれか一つを万物の固定的「本体」へ昇格させない**。
C60の実際の幾何学とLean証明は保持しつつ、より根本の
関係・生成・文脈の読取りが可能であることを意識する。
王弼の「無」と仏教の「空」は関連を探究できるが
**同一性の形式定理でも史料学的な同一命題でもない**。

### 1A.2 原文→読み下し→現代訳：『周易略例・明象』

- **王弼 原文**：`得意在忘象，得象在忘言`。
- **読み下し**：意を得るは象を忘るるに在り、象を得るは
  言を忘るるに在り。
- **現代的読解**：言を通して象を、象を通して意をつかむ。
  しかし、意味が判明した後に表現形式への固着によって
  本来の意を失わない。
- **一次資料**：
  https://zh.wikisource.org/wiki/周易略例/明象
  https://ctext.org/wiki.pl?chapter=664189&if=en

**王弼自身の重要な注意**：同篇では、象を細部まで固定
するあまり、説明の不足を埋めるために卦変や五行を
次々持ち込む解釈を戒める。したがって、
`五角形=五行`・`六角形=六氣`・`四旗=四象`・
`32面×表裏=64卦` という数的対応**だけ**を以って
王弼がそれらの同一性を保証したとは考えない。

**KuuOS旧ワークフローの継承（2025-11-13指示）**：
`卦・爻・辞 × 陰陽五行 × 曼荼羅 × 非可換解析` は
**append-only／上書き禁止**の検討対象であり、
王弼 `周易注` は乾・坤以下の64卦を略例の手順
に沿って逐次再読する。以前検討した
`象MASA → 義MASA` の粗視化 `C_WB`、
人事射影 `P_human`、卦ごとのLindblad分解、
本末テンソルは**研究案であり、Leanで既証明の定理ではない**。
符号から意味への読替えは定理と仮定を明記して行い、
従来の陰陽五行・protected-historyを消去しない。

### 1A.3 原文→読み下し→現代訳：『周易略例・明卦適變通爻』

- **王弼 原文**：`夫卦者，時也；爻者，適時之變者也`。
- **読み下し**：夫れ卦なる者は時なり。爻なる者は
  時に適うの変なり。
- **現代的読解**：卦はその時の全体的状況をまとめ、
  六つの爻は時と位置に応じた関係の変化を示す。
  卦名と吉凶を時代・文脈から切り離して
  絶対的性質に固定しない。
- **一次資料**：
  https://zh.wikisource.org/wiki/周易略例/明卦適變通爻
  https://ctext.org/wiki.pl?chapter=735882&if=en

**C60の32面表裏と64卦への正しい接続**：
`SignedFace = (TruncatedIcosahedralSeedFace × Bool)`
は32×2=64要素を持つが、これは**六爻の卦コード
`Fin 6 → Bool` との集合としての符号化候補**である。
各C60面をどの卦のどの「時」へ、各六爻を
どの局所転化・位置・人事の読みへ送るかは、
別途、完全な64件の表と文脈付き読みを構成して
証明または注記する必要がある。
**表裏の反転・陰陽共役・卦の錯綜変化が自動的に
同一の写像だと仮定しない**。

王弼の「卦=時・爻=適時之変」を使い、
最終的に`C60 signed-face chart`を
**静的な最終運命値ではなく、時・観測・三才（天・地・人）
の文脈に依存する記述**へ送り、その意味について
Leanで構成できる部分だけを形式定理とする。

### 1A.4 王弼と三才・河圖洛書・陰陽五行・歴史の整合

- `無/有`・`本/末`：表示された符号だけを「本」に
  固定せず、生成と意味の条件を重視する。
- `言/象/意`：**観測語→表現象→意味**を区別する。
  保存された証拠を捨てることではない。
- `卦/爻/時`：64卦を静的な属性ではなく
  時と関係変化の読解へ置く。
- `人事`：象数を人体・治療・運命へ直接投影せず、
  人の関係と具体的な状況を重要な解釈文脈とする。
- `河圖/洛書`：数的構造の古典的伝統と現代の
  D8不変量の証明は重要だが、数え上げの美しさが
  王弼の求めた義を自動的に決めるわけではない。
- `protected-history`：象への固着を離れることと
  履歴を消すことは違う。元のKuuOS v2.5–v3.0の
  位相射影・履歴残留・観測普遍性をそのまま保つ。

**判定規則**：王弼の文献学的解釈を前提仮定として
Leanへ密輸入しない。必ず元の原文、読み下し、解釈、
定義した現代数学、実際の形式証明という5層を区別する。
C60の象を活かしつつ、象によって意を閉ざさない。

## 2. 列子・天瑞：太易・太初・太始・太素 ≠ 四象

**Text.** *Liezi* (received version), "Tianrui" (天瑞):
- `太易`: prior to the appearing of qi.
- `太初`: onset of qi.
- `太始`: onset of form.
- `太素`: onset of substantial qualities.
- "clear/light" as heaven, "turbid/heavy" as earth, and
  "intermediate harmonizing qi" as human.

Primary witness: https://ctext.org/liezi/tian-rui/zh
Compare: https://zh.wikisource.org/zh-hant/列子/天瑞篇

**KuuOS reading:** three-power (*三才*) differentiation and
the ordering of distinct descriptions of manifestation. This
is NOT an identity of these four stages with
`太陰/少陰/少陽/太陽` (四象), and the text is NOT an
axiomatization of Fibonacci fusion or the mathlib complex field.

The original 2026-05 KuuOS `Qi v2.4` makes yin–yang the contextual
local real structure of a process: the phase reading arises only
*within* this flow. Its `Wuxing v2.5` deliberately separates
present-phase `ZMod 5` from protected Fibonacci lineage.

## 3. 周敦頤 and 朱熹: 正本の著者を分離する

The canonical line "無極而太極 ... 動極而靜 ... 一動一靜,
互為其根 ... 五行一陰陽也" belongs to **Zhou Dunyi's**
`太極圖說`, not a new original verse written by Zhu Xi.
Zhu Xi's `太極圖說解` / `太極圖解` elaborates its
`理` / `氣`, dynamic / quiescent, unity / differentiation
interpretation.

Primary texts:
- Zhou Dunyi:
  https://zh.wikisource.org/zh-hant/太極圖說
- Zhu Xi, commentary:
  https://www.shidianguji.com/book/SDZJ0476/chapter/1kbptla9d1nvp
- Zhuzi Yulei (朱子語類), vol. 98, `理一分殊`:
  https://zh.wikisource.org/zh-hant/朱子語類/098

**Text-critical point:** Zhu Xi's system cannot be reduced fairly
to static dogma: in the `理一分殊` dialogues a common order
does not erase contextual differences. His own commentary on
the `太極圖說` discusses recurrent movement and repose.
But an implementation can **misuse** any elegant system by making
one particular ordering or interpretation the irrevocable truth.

This echoes the earlier KuuOS discussion in which placing all
explanations inside one highly ordered categorical scheme risked
repeating that rigidity. The positive repair is not to discard
formal structure; it is to keep:
- stable mathematically verified compatibility laws;
- context-specific local charts, gauge transport, observer and scale;
- explicit protected history, which phase projection cannot erase;
- continual authority separation: models neither compel clinical
  decisions nor grant physical/theological truth.

**KuuOS reinterpretation of 理一分殊:** one shared formal
compatibility condition over a family of many local charts.
It is NOT the theorem `one global physically true chart`.

## 4. Correct mathematical decomposition on C60

### Existing verified authorities

- `Qi v2.3`: the Yin/Yang role belongs to a relationship, not
  a permanent object; yin containment and yang propagation.
- `Qi v2.4`: a local involutive real structure
  `κ²=id`; frame-preserving transport satisfies
  `κ_d ∘ T = T ∘ κ_c`.
- `Qi Wuxing v2.5–v3.0`: `FivePhase=ZMod 5`;
  `WuxingShift=(phase displacement,event count)`.
  One Ke event and two Sheng events project to the same phase
  but record respectively one and two events.
- `C60 v3.89–v3.90`: independent actual five-point star
  incidence and inner-pentagon recursive geometric carrier.
- `F59-F15–F17`: actual integer cellular
  `H₀=ℤ,H₁=0,H₂=ℤ`, with 60 true dart vertices,
  90 real edges, 12 pentagonal + 20 hexagonal faces.
- `F59-F21`: `Wuxing` Sheng and Ke as genuine typed quiver
  arrows. Ke diagonals are decorations, not new C60
  cellular edges.
- `F59-F22`: recover the original phase/history theory, real
  polar complex `LocalRealFrame`, four flag images, original
  five-arrow star→inner-pentagon incidence, local C60
  phase transport, and numerical Hetu/Luoshu invariants.

### Planned integration without forced identifications

**Poles:** north and south are opposite original icosahedral
pentagon centers, not sixty-dart surface vertices. Their
complex conjugations are chart-relative, and invertible
complex transport intertwines the two frames.

**四象:** each original C60 physical edge generates four real
endpoint × incident-face flags, carrying a locally chosen
two-bit reading. This does not create a C60 quadrilateral face.

**五行:** pentagonal five-phase functional differentiation
within contextual yin–yang. Positive Sheng and controlling
Ke arrows are distinct events in the protected-history
fiber even if Ke advances twice the phase.

**六氣/三陰三陽:** six climate/phase readings may decorate
each original six-edged hexagon once an explicit classical
sequence and orientation are fixed. The number six alone
does not identify climate with a polygonal face.

**三才:** heaven, earth and human are three *interpretive
roles*, not three new C60 geometric poles. Liezi's
"harmonizing qi as human" motivates a mediation condition,
not a literal center vertex absent from the actual carrier.

**十干×十二支:** the simultaneous cyclic increments have
period `lcm(10,12)=60`; any claimed association to the
sixty existing C60 dart vertices needs an explicit bijection,
chosen chart and its transport behavior (not just a count).

**六十四卦:** the original 32 polygonal faces have two
orientations/sides each, a 64-member formal signed-face
carrier. A bijection to `Bool^6` is an *additional
explicit coding theorem*, not a historical identification
of particular faces with Zhouyi hexagrams.

**河圖:** odd/even generation/completion pairs 1/6, 2/7,
3/8, 4/9, 5/10, five Wuxing relationships, 55 total.

**洛書:** the nine-palace 3×3 magic array has central 5,
pairwise opposite sum 10, row/column/diagonal sum 15,
sum 45, with D8 chart symmetry. It is a visualization
of coordinated arrangements, not a new C60 face.

**中:** compatibility of different local decompositions,
not Earth=metaphysical central substance. The whole model
is accountable to fresh source observations and formally
verified equalities without requiring no-go proofs as
a starting point for generative research.

## 5. Historical/clinical boundaries

`Laozi Dao = modern Buddhist emptiness`: **not established**.
`Liezi Four Beginnings = Four Images`: **not established**.
`Zhu Xi rational unity = unique final C60 world model`: **not established**.
`Five phases = quantum particles`: **not established**.
`Fibonacci golden ratio = clinical diagnosis/treatment threshold`:
**not established**.

The user's clinical *内経* insights are inputs to conceptual
research, NOT permission to replace evidence-based care or infer
clinical decisions from unvalidated abstract physical analogies.

By construction, the conceptual readings are **revision-friendly**,
and the actual Lean artifacts decide only exact stated
mathematical claims. This is how KuuOS retains Zhu Xi's
descriptive reach while resisting unauthorized closure.
