# Paperforge and reference audit

Audit date: 29 July 2026.

## Result

The final Paperforge run completes with **0 errors and 7 warnings**.  The
warnings are all accounted for:

1. Two occurrences of Milnor, Section 2 cannot be checked mechanically because
   no local copy of the commercial book is included.
2. BGR, Corollaries 7.3.2/10 and 7.3.2/6 cannot be checked mechanically for the
   same reason.
3. The plagiarism scan reports three inherited, generic overlaps: an eight-word
   phrase about rational localisation of a reduced affinoid algebra, an
   eight-word proof-direction phrase, and a seven-word phrase defining a sheaf
   of complete topological rings.  None is new text introduced in this pass.

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
| Stacks Project, Tags 00MB and 009O | These support completion flatness and checking a sheaf on a basis. |
| Kedlaya, AWS Remark 1.2.16 | This is the reduced-affinoid rational-localisation statement used in the second example. |
| Conrad, Proposition 15.1.1 | Its proof invokes the two BGR corollaries cited in the paper. |
| Bambozzi--Kremnizer, Section 4 | This develops rational localisations through Koszul complexes, as stated in the related-work discussion. |

## Lean crosswalk

`crosswalk/lean-decl-map.json` was curated manually after the generated
candidate incorrectly associated the sheafiness theorem with an unrelated
Witt-vector declaration.  The accepted map now covers:

- the uniform-domain and non-noetherian finite-jet endpoints;
- the bad rational chart and failure of stable uniformity;
- restricted Koszul exactness, strictness, and closed-image estimates;
- exactness of the localised Milnor row; and
- the final rational-cover and all-open sheafiness endpoints.

No doc-gen4 site exists for the audited snapshot yet, so the web build makes
the automatic theorem badges inert rather than emitting links to missing
documentation pages.  The appendix supplies pinned source-file links instead.

The AINTLIB audit used Lean `4.33.0-rc1` with mathlib commit
`fd1d54bcac5caba4eff2ea3421c47d907333f515`.  The 24 targeted FJP modules and
the 3,307-job umbrella build completed, no `sorry` or `admit` occurs in the FJP
tree, and the inspected headline declarations use only `propext`,
`Classical.choice`, and `Quot.sound`.

## Build-level warnings

Both final PDFs compile without undefined references, overfull boxes, or
LaTeX/package warnings.  PreTeXt itself reports deprecations for the legacy
title-page shape and for generated `<me>`/`<men>` elements; these are converter
maintenance notices rather than defects in the resulting paper.
