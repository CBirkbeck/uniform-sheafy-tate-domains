# Paperforge and reference audit

Audit date: 1 August 2026.

## Result

The final Paperforge run completes with **0 errors and 2 warnings**.  Both
warnings are accounted for:

1. Milnor, Section 2 cannot be checked mechanically because no local copy of
   the commercial book is included.
2. The citations to Problems 24 and 28 of the online Scottish Book cannot be
   checked by Paperforge's local-PDF matcher; their statements were checked
   directly on the official page.

The plagiarism check reports no overlaps at its configured seven-word
threshold.

All locators for which an open or author-provided PDF is available pass
Paperforge's token check.  The files and download sources are recorded in
`references/PROVENANCE.md`.

## Manual mathematical spot checks

Mechanical token matching only establishes that a label occurs in a source.
The following claims were also read in context:

| Citation | What was checked |
|---|---|
| Nonarchimedean Scottish Book, Problems 24 and 28 | Problem 24 asks whether the ring map underlying a rational localisation of Tate Huber pairs is flat. Problem 28 asks for a strict regular element which becomes zero on a rational subspace. Thus the paper correctly gives a negative answer to Problem 24 and an affirmative answer to the Tate case of Problem 28. |
| Kedlaya, *Sheaves, stacks, and shtukas*, published 2019 version, Definition 1.4.5, Theorem 1.4.14, and Remark 1.4.6 | The exact base-change theorem applies to stably pseudocoherent modules. It therefore does not imply that a closed principal ideal remains injective after rational localisation. The contrary Corollary 1.4.14 in the preliminary 2017 notes was removed from the published version. |
| Hansen--Kedlaya, Remark 3.16 | It asks whether a uniform sheafy Huber ring must be stably uniform. |
| Kerz--Saito--Tamme, Lemma 3.1 | It constructs compatible rings of definition for a Milnor square using the nonarchimedean open mapping theorem. |
| Buzzard--Verberkmoes, Lemmas 2--3, Corollary 4, Theorem 7, Lemma 8, and Propositions 17--18 | Lemma 2 gives the strictness criterion; Lemma 3 and Corollary 4 relate bounded power-bounded elements to the structure presheaf; Lemma 8 and Theorem 7 show that stable uniformity is sufficient for sheafiness; Propositions 17--18 give the two standard uniformity/sheafiness pathologies described in the introduction. |
| Huber, Proposition 1.3 and Lemma 1.5 | These support the universal property and presentation-independence statements for rational localisations, including the final assertion of Lemma 8.5. |
| Huber, Theorem 2.2 and Lemmas 2.3--2.4 | These support sheafiness for strongly noetherian Tate rings and the strictness/closed-image input for finite modules. |
| Huber, Lemma 3.10; Kedlaya--Liu, Remark 2.4.7 | These give the first two assertions of Lemma 8.5: sufficiently small changes still give rational data and define the same rational subset. The canonical identification of completed rational localisations then follows from Huber, Proposition 1.3. |
| Wedhorn, Proposition and Definition 6.36; Remark 8.20; Definition 8.26; Theorem 8.28(b); Lemmas 8.31--8.34 | These support the definitions of strong noetherianity and sheafiness, the representable topological-ring formulation, and the strongly-noetherian proof route used by the formalisation. |
| Stacks Project, Tag 009O | This supports checking a sheaf on a basis. |
| Ben-Bassat--Kremnizer, Definition 5.7, Remark 5.8, and Lemmas 5.13--5.14 | These define rational localisations, prove the strict two-term resolutions for the Weierstrass and Laurent cases, and factor a general rational localisation into those cases. The paper does not use Koszul terminology or state the simultaneous multivariable result. |
| Bambozzi--Kremnizer, Notation 4.3, Definitions 4.5--4.6, Proposition 4.9, Lemma 4.11, and Corollary 4.13 | These define the relevant Koszul complex and prove strict Koszul regularity for rational localisations. This supports the exactness and strictness assertions in Lemma 5.1; the two displayed lattice estimates are derived separately by open mapping and scaling. |

## Lean proof-route audit

The prose proofs were compared with the bodies and direct dependencies of the
declarations at the two example snapshots, rather than only with their theorem
statements.  The sheaf-predicate comparison was checked separately at
`d92f96504f949ca43a27a817cb8d2f70b6486744`, and the Scottish Book
consequences at `01116aca6070283726008536cba16d165a01b505`.  The resulting
proof crosswalk is:

| Paper result | Formal proof route and disposition |
|---|---|
| Proposition 3.1 | `JetA` is a closed support subring of `JetC`; multiplicativity of the restricted Gauss norm supplies the domain and power-bounded calculation, and nonnoetherianity is proved from the `Q²` coefficient. The paper now follows this route. |
| Proposition 4.1 | `chartEquiv` first applies the quotient `A → B`, which discards the terms divisible by `Q²`, and then substitutes `W = ϖX`. An element in `Q²C` is killed in the completion by writing it as `ϖⁿXⁿ` times a bounded element. The inverse evaluates at `W/ϖ`, and the inverse identities use the decomposition into the terms of `Q`-degree at most one and the part in `Q²C`, together with polynomial density. The paper now follows this proof. |
| Lemma 5.1 | Positive-degree Koszul exactness is transported from the polynomial sequence along the flat map to the restricted Tate algebra. The degree-zero image is closed by noetherianity; higher images are closed kernels. The nonarchimedean closed-range theorem bounds the norm of a preimage by a fixed multiple of the norm of its image; this gives strictness and, after multiplication by a power of `ϖ`, the two lattice inclusions. |
| Lemma 5.2 | Choose preimages under `d₁` over `B` and `C` satisfying the norm bounds of Lemma 5.1. Their difference over `D` lies in `ker(d₁)`; choose a preimage under `d₂` with the corresponding norm bound and lift it coefficientwise to `C`. The ambient Milnor pullback then gives the element over `A`. The same inequalities prove closedness of `I_A` and strict exactness. |
| Proposition 5.3 | Lean proves algebraic exactness by correcting defects of quotient representatives through `I_C`. A quotient-norm estimate gives the left-hand topological embedding, while the norm-preserving coefficient section proves that `C_α → D_α` is open. The proof has been rewritten accordingly. |
| Theorem 6.1 | A rational cover and compatible family are pushed to `B,C,D`; sheafiness there and the localised Milnor row give separation and gluing over `A`. The subspace of tuples agreeing on pairwise intersections is closed, and the closed-range theorem gives the required topological embedding. Lean proves this concrete argument. |
| Proposition 7.1 | Over any complete ultrametric normed field `K` with an `IsFJPBase K` instance, Lean defines `ev00(f₀(W)+Qf₁(W)+Q²h)=f₀(0)` and pulls the norm valuation back along it to obtain a point of the chart. Multiplicativity of the Gauss norm gives `‖Q²a‖=‖a‖`; the resulting range factorisation is a homeomorphism, and completeness makes the range closed. The previously proved identity `canonicalMap_Qa_sq` gives `ρ(Q²)=0`. For nonflatness, Lean applies `Module.Flat.isSMulRegular_of_nonZeroDivisors`: flatness would make the image of the non-zero-divisor `Q²` act injectively on the nonzero chart, whereas that image is zero. The paper now follows this route. |
| Lemma 8.2 | Lean decomposes each finite-variable ring into the finitely many exponent-parity classes, identifies the even-exponent subring isometrically with an ordinary Tate algebra, and proves module-finiteness over it. The inclusions are the subtype inclusions in the common countable Tate algebra, hence isometric, and `exists_head_approx` gives the quantitative approximation used for density. |
| Propositions 8.3--8.4 and 8.8--8.9 | The weighted-parity development proves multiplicativity of the countable Gauss norm by choosing lexicographically maximal norm-attaining exponents, proves nonnoetherianity by direct coefficient extraction, and handles the distinguished chart by a completed quotient over \(K\langle W\rangle\) and an embedding into formal power series. The paper now uses these arguments. |
| Proposition 8.6 and Theorem 8.10 | For data in the finite-variable subring \(\mathcal A^{(N)}\), localisation is constructed by applying its quotient map to every coefficient indexed by the remaining variables and summing coefficientwise for the inverse; it does not use the Koszul complex. In the sheaf proof, the retraction \(\rho_N:\mathcal A\to\mathcal A^{(N)}\) pulls any point outside the proposed finite-variable cover back to a point outside the original cover, so the finite-variable rational subsets really do cover. Strong noetherian sheafiness then glues the coefficients, and the restriction embedding proves that they tend to zero; the closed-range theorem supplies the final topological statement. |
| Lemma 8.5 | The paper cites Huber, Lemma 3.10, and Kedlaya--Liu, Remark 2.4.7, for this standard result. Lean independently proves the quantitative norm-unit-ball specialisation used to move the rational data for a finite cover into one finite-variable strongly noetherian subring. |

## Lean crosswalk

`crosswalk/lean-decl-map.json` was curated manually after the generated
candidate incorrectly associated the sheafiness theorem with an unrelated
Witt-vector declaration.  The accepted map now covers, clause by clause:

- the Tate, uniform, power-bounded, domain, and nonnoetherian finite-jet
  endpoints;
- the bad rational chart, both continuity directions, generator formulas, and
  failure of stable uniformity;
- the nonempty point of the finite-jet chart, the isometry defined by
  multiplication by `Q²`, its vanishing on the completed chart, and the
  resulting Problem 28 and nonflatness statements;
- restricted Koszul exactness, continuity, strictness, closed images, and both
  denominator estimates;
- the ideal pullback and every topological clause of the localised Milnor row,
  including restriction compatibility; and
- the finite-rational-cover, chosen-pair all-open, completion-independent, and
  public structure-presheaf sheafiness endpoints, together with the exact
  equivalence with Mathlib's `TopCommRingCat`-valued sheaf predicate;
- the weighted-parity support definition, Tate structure, uniformity, domain,
  nonnoetherianity, and identification of the power-bounded elements;
- the finite-variable subrings, their finite-module decomposition, strong
  noetherianity, isometric transition maps, and quantitative density;
- the coefficientwise localisation equivalence, its two continuity
  directions and restriction compatibility, together with the finite-variable
  presentation and the complete two-step identification of the distinguished
  chart; and
- the weighted-parity all-pairs sheaf theorem, nonuniform domain chart, and
  failure of stable uniformity.

No doc-gen4 site exists for the audited snapshots, and the two example commits
are not currently public.  The web build therefore extracts each exact
declaration from its pinned local Git object.  Every automatic theorem badge
opens a Roe-style inline knowl and has a working standalone archival page as
its ordinary link.  The generator also covers the appendix definitions and
equivalence chain.  Its pages record the source path and commit and credit
William Coram's restricted-series code, Fabrizio Barroero's univariate
Gauss-norm code, and Bingyu Xia's power-series equivalences.

The Pages snapshot contains no orphaned xref knowls.  The build script now
clears only the generated xref-knowl directory before the PreTeXt web build,
so a withdrawn theorem or equation cannot survive as a stale standalone
page.

The claim audit confirms the precise Lean statements used in the paper.  Lean
proves the unit-ball/Gauss-norm specialisation of Lemma 5.1, exports the chart
as a bicontinuous `RingEquiv`, supplies the explicit constant-series map, and
proves sheafiness by the concrete finite-jet transfer.  For the second
example, it also proves a quantitative norm-unit-ball version of the standard
small-perturbation statement cited in the paper.

For the weighted-parity example, Lean proves uniformity, the domain and
nonnoetherianity statements, sheafiness for every ring of integral elements,
the nonuniform domain chart, and failure of stable uniformity.  The code also
supplies an isometric constant-series map from the coefficient field.

The AINTLIB audit used Lean `4.33.0-rc1` with mathlib commit
`fd1d54bcac5caba4eff2ea3421c47d907333f515`.  The 24 targeted FJP modules and
the 3,307-job umbrella build completed, no `sorry` or `admit` occurs in the FJP
tree, and the inspected headline declarations use only `propext`,
`Classical.choice`, and `Quot.sound`.

The sheaf-comparison snapshot
`d92f96504f949ca43a27a817cb8d2f70b6486744` completed its 3,006-job build.
`#print axioms` for the three comparison theorems reported only `propext`,
`Classical.choice`, and `Quot.sound`, with no `sorryAx`.  The
`overlappingInstances` warnings were the pre-existing warnings on the
neighbouring structure-sheaf declarations.

The abstract-base Scottish Book audit uses commit
`01116aca6070283726008536cba16d165a01b505`.  Its class `IsFJPBase K` consists
of a chosen element `ϖ : K`, proofs that `ϖ ≠ 0` and `‖ϖ‖ < 1`, and the ambient
complete ultrametric normed-field structure.  The Problem 24 and 28
declarations require no discreteness or noetherian-base hypothesis.  The
source files relevant here are unchanged at the current public head; the
three entry modules and the p-adic specialization compiled there.  `#print
axioms` for
`FiniteJet.finiteJet_padic_quality`,
`FiniteJet.finiteJet_problem28`,
`FiniteJet.finiteJet_not_flat_canonicalMap`,
`FiniteJet.chart_rationalOpen_nonempty`,
`FiniteJet.scottishWitness_mul_isometry`,
`ScottishBook.problem28`, and the two Problem 24 endpoints again reported only
`propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

There are explicit `IsFJPBase` instances for `F((t))` and for `ℚ_p`.  The
separate sheafy quality package `finiteJet_witnessRing_quality` assumes the
stronger class `IsFJPNoetherianBase K`; a sorry-free instance of this stronger
class is currently supplied for `F((t))`, but not for `ℚ_p`.  Neither Scottish
Book argument uses that additional assumption.

The paper deliberately links the concrete `FiniteJet.*` declarations, rather
than the generic `ScottishBook.*` wrappers.  The concrete declarations prove
all the required facts for the genuine rational datum `(W;ϖ)` on the maximal
Huber pair.  By contrast, the current type of `ScottishBook.problem28` does not
record that the chosen plus ring is a ring of integral elements, and the two
Problem 24 wrappers do not include `D.IsRational` (and likewise quantify over a
bare plus subring).  Their proofs instantiate valid concrete data, so these are
packaging omissions rather than gaps in the mathematics, but the wrappers are
not used as evidence for the paper's formalisation claim.  The concrete
Problem 24 and 28 declarations are parametrised by `IsFJPBase K`, and hence
apply in particular to `F((t))` and to the explicit mixed-characteristic base
`ℚ_p`.

The weighted-parity audit used pinned commit
`090a289211deb69117413e329325fe819aa7dbc2`.  `WP.Main` completed its
3,178-job build.  Axiom checks on the construction, uniformity, domain,
nonnoetherianity, power-bounded, sheafiness, chart, and non-stable-uniformity
endpoints again report only `propext`, `Classical.choice`, and `Quot.sound`.

## Build-level warnings

Both PDFs compile without undefined references, overfull boxes, or package
warnings.  They have only underfull-box diagnostics where page-broken code
listings leave short lines; a visual check confirms that there is no clipping.
PreTeXt itself reports deprecations for the legacy title-page shape and for
generated `<me>`/`<men>` elements; these are converter maintenance notices
rather than defects in the resulting paper.
