# Paperforge and reference audit

Audit date: 29 July 2026.

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
  public structure-presheaf sheafiness endpoints.

No doc-gen4 site exists for the audited snapshot, and the pinned AINTLIB commit
is not currently public.  The web build therefore extracts exact declaration
statements from the pinned local Git object.  Every automatic theorem badge
opens a Roe-style inline knowl and has a working standalone archival page as
its ordinary link.  The generator also covers the appendix definitions and
equivalence chain.  Its pages record the source path and commit and credit the
Coram/Xia restricted-series infrastructure.

The claim audit found three scope distinctions, now stated explicitly in the
appendix: Lean proves the unit-ball/Gauss-norm specialization of Lemma 5.1; the
chart is exported as a bicontinuous `RingEquiv`, not a bundled `K`-algebra
equivalence; and the general sheaf-transfer lemma is formalised only in its
specialized finite-jet instance.  None affects the final finite-jet endpoint.

The AINTLIB audit used Lean `4.33.0-rc1` with mathlib commit
`fd1d54bcac5caba4eff2ea3421c47d907333f515`.  The 24 targeted FJP modules and
the 3,307-job umbrella build completed, no `sorry` or `admit` occurs in the FJP
tree, and the inspected headline declarations use only `propext`,
`Classical.choice`, and `Quot.sound`.

## Build-level warnings

Both PDFs compile without undefined references, overfull boxes, or package
warnings.  They have only underfull-box diagnostics where page-broken code
listings leave short lines; a visual check confirms that there is no clipping.
PreTeXt itself reports deprecations for the legacy title-page shape and for
generated `<me>`/`<men>` elements; these are converter maintenance notices
rather than defects in the resulting paper.
