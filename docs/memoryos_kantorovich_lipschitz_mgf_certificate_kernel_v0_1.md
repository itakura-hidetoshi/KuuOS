# MemoryOS v0.63 — Kantorovich duality, Lipschitz semigroup, and finite MGF certificate

MemoryOS v0.63 extends the accepted v0.62 Wasserstein–Marton certificate with an explicit finite Kantorovich dual witness, observable-side Markov semigroup contraction, and exact finite symbolic moment-generating-function ledgers.

## Three-point Kantorovich duality

For a centered signed mass difference

\[
(\delta_0,\delta_1,-\delta_0-\delta_1)
\]

on the path `early — middle — late`, the primal path distance is

\[
W_1=|\delta_0|+|\delta_0+\delta_1|.
\]

For an observable `f`, the expectation difference rewrites exactly as

\[
\delta_0(f_E-f_M)+(\delta_0+\delta_1)(f_M-f_L).
\]

Hence

\[
|\Delta_f|\le W_1\,\operatorname{Lip}(f).
\]

The Lean module provides the explicit one-Lipschitz optimizer

\[
f_E=\operatorname{sgn}(\delta_0),\qquad
f_M=0,\qquad
f_L=-\operatorname{sgn}(\delta_0+\delta_1),
\]

and proves that its dual objective equals the path Wasserstein distance. The runtime records five exact-rational witness cases, including zero, slow, fast, and mixed-sign fluxes.

## Observable Markov semigroup

For

\[
K=
\begin{pmatrix}
3/4&1/4&0\\
1/4&1/2&1/4\\
0&1/4&3/4
\end{pmatrix},
\]

v0.63 acts on observables by `Kf`. With

\[
\operatorname{Lip}(f)=\max(|f_E-f_M|,|f_M-f_L|),
\]

Lean proves

\[
\operatorname{Lip}(Kf)\le \frac34\operatorname{Lip}(f)
\]

and therefore

\[
\operatorname{Lip}(K^n f)\le
\left(\frac34\right)^n\operatorname{Lip}(f).
\]

The slow observable `(1,0,-1)` is an exact eigenmode with eigenvalue `3/4`; the fast observable `(1,-2,1)` is an exact eigenmode with eigenvalue `1/4`.

## Reference observable gaps

The certificate uses

\[
\pi=(1/3,1/3,1/3),
\]

\[
P=(29/60,1/3,11/60),\qquad
Q=(11/60,1/3,29/60).
\]

The slow observable is a one-Lipschitz optimizer for `P_n` and `Q_n`. Exact runtime records verify

\[
|\mathbb E_{P_n}f-\mathbb E_\pi f|
=W_1(P_n,\pi)=\frac3{10}\left(\frac34\right)^n,
\]

and

\[
|\mathbb E_{P_n}f-\mathbb E_{Q_n}f|
=W_1(P_n,Q_n)=\frac35\left(\frac34\right)^n.
\]

## Finite symbolic MGF ledger

For the stationary distribution, Lean proves exact finite formulas. For the slow mode scaled by `r`,

\[
M_{\mathrm{slow},r}(t)
=\frac{e^{tr}+1+e^{-tr}}3,
\qquad
\mathbb E[f^2]=\frac23r^2.
\]

For the fast mode,

\[
M_{\mathrm{fast},r}(t)
=\frac{2e^{tr}+e^{-2tr}}3,
\qquad
\mathbb E[f^2]=2r^2.
\]

The runtime stores exact rational weights and exponent coefficients for horizons `0..10`. It retains Marton influence sums and finite variance proxies from v0.62 as inputs to later concentration work. It does not claim a general path-space Gaussian theorem or an unproved exponential envelope.

## Source binding and fail-closed behavior

The runtime independently validates an accepted v0.62 certificate, its certificate digest, all v0.62 transport and Marton collection digests, exact counts, candidate IDs, PlanOS history IDs, quotient-coordinate probe IDs, and review/dissent/minority sets.

It rejects altered source records, changed dual objectives, false semigroup contraction claims, false Gaussian-theorem claims, unexpected claims, digest substitution, and any candidate selection or execution authority claim.

## Transport boundary

Eight full-rank records preserve commuting Kantorovich, Lipschitz-semigroup, and symbolic-MGF evidence. Four singular records retain atomic witnesses and terms without generating a two-dimensional target density or reconstructing lost coordinates.

MemoryOS v0.63 remains future-only, read-only, and advisory. It does not rank, prune, or select candidates; commit decisions; synthesize or activate plans; execute actions; mutate source certificates, DecisionOS, or persistent WORLD state; issue verification truth; or acquire truth authority.
