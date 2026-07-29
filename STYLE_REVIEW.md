# First author-voice review

This is a first pass intended to make the paper easier to continue editing in
Chris Birkbeck's voice; it is not a wholesale rewrite.

## Corpus

The corpus was assembled from the publication list on
<https://cdbirkbeck.wixsite.com/website/research>.  It contains LaTeX sources
for nine arXiv papers (2016--2026) and the author-hosted PDF
*Formalising modular forms, Eisenstein series and the statement of the
modularity conjecture*.  The inventory is in
`style-corpus/arxiv/MANIFEST.md` and
`style-corpus/author-hosted/MANIFEST.md`.

Solo-authored papers were given the greatest weight for prose; the recent
coauthored formalisation papers were used chiefly to decide how much Lean code
belongs in a mathematical article.

## Recurring features

- Formal, explanatory prose with British spelling and first-person plural.
- A section normally opens by stating its purpose, followed by the first step.
- Definitions are motivated before they are displayed.
- Logical transitions are explicit but brief: “We begin…”, “Next we need…”,
  “Using this…”, and “It follows that…”.
- Limitations and implementation choices are stated directly, without
  promotional language.
- Formalisation exposition proceeds from the mathematical notion to a short
  Lean declaration and then explains the declaration's fields in order.

These observations have been distilled into `style-corpus/ADVICE.md`, which is
the editable guide for later Paperforge prose passes.

## Changes made in this pass

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

## Deliberate limits

The body proofs have not been globally restyled.  They should be reviewed
section by section with the author, particularly the long localisation
argument and the second, unformalised example.  The draft still says
`Anonymous`; authorship metadata was not inferred or changed.  The style
corpus is used as evidence about structure and register, not as a phrase bank.
