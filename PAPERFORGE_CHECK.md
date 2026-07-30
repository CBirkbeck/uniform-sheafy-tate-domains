# Paperforge and reference audit

Audit date: 30 July 2026.

## Result

The final Paperforge run completes with **0 errors and 7 warnings**.  The
warnings are all accounted for:

1. Milnor, Section 2 cannot be checked mechanically because no local copy of
   the commercial book is included.
2. BGR, Corollaries 7.3.2/10 and 7.3.2/6 cannot be checked mechanically for the
   same reason.
3. The plagiarism scan reports four inherited matches involving three generic
   phrases: a proof-direction phrase, a statement that a construction is
   independent of a choice, and the definition of a sheaf of complete
   topological rings.  None is new text introduced in this pass.

All locators for which an open or author-provided PDF is available pass
Paperforge's token check.  The files and download sources are recorded in
`references/PROVENANCE.md`.

## Manual mathematical spot checks

Mechanical token matching only establishes that a label occurs in a source.
The following claims were also read in context:

| Citation | What was checked |
|---|---|
| Hansen--Kedlaya, Remark 3.16 | It asks whether a uniform sheafy Huber ring must be stably uniform. |
| Kerz--Saito--Tamme, Lemma 3.1 | It constructs compatible rings of definition for a Milnor square using the nonarchimedean open mapping theorem. |
| Buzzard--Verberkmoes, Lemma 2 and Propositions 17--18 | These supply the strictness criterion and the two standard uniformity/sheafiness pathologies described in the introduction. |
| Huber, Proposition 1.3 and Lemma 1.5 | These support the universal property and presentation-independence statements for rational localisations. |
| Huber, Theorem 2.2 and Lemmas 2.3--2.4 | These support sheafiness for strongly noetherian Tate rings and the strictness/closed-image input for finite modules. |
| Wedhorn, Proposition and Definition 6.36; Remark 8.20; Definition 8.26; Theorem 8.28(b); Lemmas 8.31--8.34 | These support the definitions of strong noetherianity and sheafiness, the representable topological-ring formulation, and the strongly-noetherian proof route used by the formalisation. |
| Stacks Project, Tag 009O | This supports checking a sheaf on a basis. |
| Kedlaya, AWS Remark 1.2.16 | This is the reduced-affinoid rational-localisation statement used in the second example. |
| Conrad, Proposition 15.1.1 | Its proof invokes the two BGR corollaries cited in the paper. |
| Ben-Bassat--Kremnizer, Definition 5.7, Remark 5.8, and Lemmas 5.13--5.14 | These give the earlier strict graph-complex framework. |
| Bambozzi--Kremnizer, Definitions 4.5--4.6, Proposition 4.9, Lemma 4.11, and Corollary 4.13 | These prove strict Koszul regularity for rational localisations. Consequently Lemma 5.1 is presented as a lattice-sensitive restatement, not as a new result. |

## Lean crosswalk

`crosswalk/lean-decl-map.json` was curated manually after the generated
candidate incorrectly associated the sheafiness theorem with an unrelated
Witt-vector declaration.  The accepted map now covers, clause by clause:

- the Tate, uniform, power-bounded, domain, and nonnoetherian finite-jet
  endpoints;
- the bad rational chart, both continuity directions, generator formulas, and
  failure of stable uniformity;
- restricted Koszul exactness, continuity, strictness, closed images, and both
  denominator estimates;
- the ideal pullback and every topological clause of the localised Milnor row,
  including restriction compatibility; and
- the finite-rational-cover, chosen-pair all-open, completion-independent, and
  public structure-presheaf sheafiness endpoints;
- the weighted-parity support definition, Tate structure, uniformity, domain,
  nonnoetherianity, and identification of the power-bounded elements;
- the weighted-parity all-pairs sheaf theorem, nonuniform domain chart, and
  failure of stable uniformity.

No doc-gen4 site exists for either audited snapshot, and neither AINTLIB
commit is currently public.  The web build therefore extracts each exact
declaration from its pinned local Git object.  Every automatic theorem badge
opens a Roe-style inline knowl and has a working standalone archival page as
its ordinary link.  The generator also covers the appendix definitions and
equivalence chain.  Its pages record the source path and commit and credit the
Coram/Xia restricted-series infrastructure.

The claim audit found three scope distinctions, now stated explicitly in the
appendix: Lean proves the unit-ball/Gauss-norm specialization of Lemma 5.1; the
chart is exported as a bicontinuous `RingEquiv`, not a bundled `K`-algebra
equivalence; and the general sheaf-transfer lemma is formalised only in its
specialized finite-jet instance.  None affects the final finite-jet endpoint.

For the weighted-parity example, the audit separates the completed statements
from the remaining reducedness argument.  Lean proves sheafiness for every
ring of integral elements, proves that the distinguished chart is a
nonuniform domain, and deduces failure of stable uniformity.  The current
finite-chain reducedness declarations depend on `sorryAx` and have therefore
not been given completion badges.  The code also supplies an isometric
constant-series map from the coefficient field, although it is not bundled as
an `Algebra K` instance.  Sheafiness of shifted-weight models and the
bicontinuous Tate-extension equivalences are present, but the transported
strong-sheafiness statement is not packaged as a single theorem and is not
claimed in the paper.

The AINTLIB audit used Lean `4.33.0-rc1` with mathlib commit
`fd1d54bcac5caba4eff2ea3421c47d907333f515`.  The 24 targeted FJP modules and
the 3,307-job umbrella build completed, no `sorry` or `admit` occurs in the FJP
tree, and the inspected headline declarations use only `propext`,
`Classical.choice`, and `Quot.sound`.

The weighted-parity audit used work-in-progress snapshot
`090a289211deb69117413e329325fe819aa7dbc2`.  `WP.Main` completed its
3,178-job build.  Axiom checks on the construction, uniformity, domain,
nonnoetherianity, power-bounded, sheafiness, chart, and non-stable-uniformity
endpoints again report only `propext`, `Classical.choice`, and `Quot.sound`.
Both finite-chain reducedness endpoints report `sorryAx`; the three remaining
source gaps are in `WP/HeadReduced.lean`.

## Build-level warnings

Both PDFs compile without undefined references, overfull boxes, or package
warnings.  They have only underfull-box diagnostics where page-broken code
listings leave short lines; a visual check confirms that there is no clipping.
PreTeXt itself reports deprecations for the legacy title-page shape and for
generated `<me>`/`<men>` elements; these are converter maintenance notices
rather than defects in the resulting paper.
