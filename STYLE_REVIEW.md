# Author-voice review

This records the style decisions used while revising the paper in Chris
Birkbeck's voice.

## Corpus

The corpus was assembled from the publication list on
<https://cdbirkbeck.wixsite.com/website/research>.  It contains LaTeX sources
for nine arXiv papers (2016--2026) and the author-hosted PDF
*Formalising modular forms, Eisenstein series and the statement of the
modularity conjecture*.  The inventory is in
`style-corpus/arxiv/MANIFEST.md` and
`style-corpus/author-hosted/MANIFEST.md`.

The four older solo number-theory papers were given the greatest weight.  The
2023 solo formalisation paper is useful for the order in which mathematics and
Lean code are presented, but its line-by-line tutorial register is not the
model for this paper.

## Recurring features

- Formal, explanatory prose with British spelling and first-person plural.
- A section normally opens by stating its purpose, followed by the first step.
- Definitions are motivated before they are displayed.
- Logical transitions are explicit but brief: “We begin…”, “Next we need…”,
  “Using this…”, and “It follows that…”.
- Limitations and implementation choices are stated directly, without
  promotional language.
- Standard material is compressed to a citation or short reduction; details
  are kept for the mechanism which is new.
- Notation is functional and names are economical.  A recurring construction
  may be named, but a one-use ideal or map is normally just written down.
- Lean exposition proceeds from the mathematical notion to a short
  declaration and explains only the fields needed to identify the two.

These observations have been distilled into `style-corpus/ADVICE.md`, which is
the editable guide for later Paperforge prose passes.

## Changes made

- Tightened the abstract and the opening of the introduction around the known
  result, the precise gap, and the two examples.
- Recast the AI-origin and related-work discussion in a more direct,
  source-conscious register.
- Added short purpose statements to sections that previously began abruptly.
- Replaced the old appendix of `#check`/`#print` output with five short,
  reader-facing Lean extracts:
  1. the binary rational-cover sheaf condition;
  2. sheafiness for one datum, for complete rings, and for Tate rings;
  3. restricted power series and strong noetherianity;
  4. the finite-jet rings and support subring; and
  5. the public finite-jet theorem endpoints.
- Added an explanation immediately after each extract and linked longer proofs
  to the audited AINTLIB commit.
- Rewrote Section 5 using \(T_E\) for the Tate algebra and stated the
  topologies on every Koszul term before using the word “strict”.
- Removed the coined term “graph ideal” and compressed the standard
  contractibility argument.
- Rebalanced the localisation section around the bounded-denominator chase,
  which is the part needed for the new pullback argument.
- Shortened defensive provenance prose and the field-by-field commentary in
  the Lean appendix.

The draft still says `Anonymous`; authorship metadata has not been changed.
The style corpus is evidence about structure and register, not a phrase bank.
