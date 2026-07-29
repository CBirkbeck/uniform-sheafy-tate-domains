# Writing advice (author-maintained)

This corpus contains Chris Birkbeck's mathematical papers.  Give the
solo-authored papers the greatest weight when deciding questions of voice; use
the coauthored formalisation papers chiefly as models for presenting Lean.

## Voice

- Use a formal but explanatory register and British spelling: *formalise*,
  *localisation*, *noetherian*, *whilst*.
- Use the first-person plural, including in a single-author paper: “we define”,
  “we show”, “our goal”.
- Prefer medium-length sentences with a clear logical spine.  A longer
  multi-clause sentence is natural when it records hypotheses or limitations,
  but follow it with a short signpost when the argument changes direction.
- State limitations candidly and specifically.  Phrases such as “we do not
  need”, “we have not proved”, “for this reason”, and “more convenient in
  practice” are preferable to promotional language.

## Mathematical exposition

- Open a section by saying what it does: “In this section we prove…”.  Then
  indicate the first step: “We begin by…”.
- Motivate a definition before displaying it.  Afterward, record conventions,
  implementation choices, or harmless differences in generality in a short
  remark.
- Make dependencies explicit with transitions such as “Before continuing…”,
  “Next we need…”, “Using this…”, and “It follows that…”.
- Attach citations to the claims they support, and give theorem, definition,
  lemma, section, or page locators whenever possible.
- In an introduction, move from background and known work to the precise gap,
  then state the goal and any limitation of the result.

## Lean in the paper

- Put the mathematical definition or theorem first.
- Display only the Lean declaration that a reader needs; link the proof and
  supporting API rather than printing a long proof term or a list of
  `#check` commands.
- After each declaration, explain its fields or conjuncts in order.  Useful
  sentence shapes are “The first field says…”, “The remaining condition
  records…”, and “Thus this is the usual mathematical definition…”.
- Explain typeclass or implementation choices only when they correspond to a
  genuine mathematical hypothesis or a deliberate difference from the printed
  statement.
- Use immutable source links pinned to a full commit.

This advice is distilled from the publication list on the author's website,
with the introductions and expository sections of the solo papers weighted
most heavily.  It is a guide for consistency, not a phrase bank: do not copy
sentences from the corpus.

Free-text guidance the generative skills read on every pass. Edit freely; examples:

- **Level of detail.** State the default: e.g. "assume a reader who knows [X]; do
  not re-derive standard facts about [Y]; always spell out [Z]-type arguments."
  Give concrete *explain / don't-explain* examples — the clearest signal there is.
- **Voice.** e.g. "first person plural, present tense, no exclamation, sparing use
  of 'clearly'."
- **Structure.** e.g. "each section opens with a one-paragraph roadmap; proofs
  end with the QED symbol, not the word."
- **Things to avoid.** e.g. specific phrasings, over-hedging, filler transitions.

This is iterative: as you correct the output, encode the correction here so it
sticks across re-runs, rather than re-explaining each time.
