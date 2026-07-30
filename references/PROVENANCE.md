# Reference corpus provenance

The files under `references/pdfs/` are used only for Paperforge's mechanical
locator checks. They were downloaded on 29 July 2026 from the following open
or author-provided sources.

| Local file | Source | Access note |
|---|---|---|
| `Bambozzi-Kremnizer-Sheafyness-Spectra-Banach-Rings.pdf` | <https://arxiv.org/pdf/2009.13926> | arXiv author manuscript |
| `Ben-Bassat-Kremnizer-Non-Archimedean-Relative-Algebraic-Geometry.pdf` | <https://www.numdam.org/item/10.5802/afst.1526.pdf> | Publisher archive (Numdam/CEDRAM), CC BY 4.0 |
| `Buzzard-Verberkmoes-Stably-Uniform-Affinoids-Sheafy.pdf` | <https://arxiv.org/pdf/1404.7020> | arXiv author manuscript |
| `Hansen-Kedlaya-Sheafiness-Criteria-Huber-Rings.pdf` | <https://kskedlaya.org/papers/criteria.pdf> | author manuscript |
| `Huber-Generalization-Formal-Schemes-Rigid-Analytic-Varieties.pdf` | <https://math.stanford.edu/~conrad/Perfseminar/refs/Huberformalrigid.pdf> | seminar reference copy |
| `Kedlaya-Sheaves-Stacks-Shtukas-AWS.pdf` | <https://swc-math.github.io/aws/2017/2017KedlayaNotes.pdf> | official AWS notes |
| `Kerz-Saito-Tamme-K-Theory-Non-Archimedean-Rings-II.pdf` | <https://arxiv.org/pdf/2103.06711> | arXiv author manuscript |
| `de-Moura-Ullrich-Lean-4.pdf` | <https://lean-lang.org/papers/lean4.pdf> | Official Lean project copy of the CADE-28 paper |
| `Mathlib-Community-Lean-Mathematical-Library.pdf` | <https://arxiv.org/pdf/1910.09336> | arXiv author manuscript of the CPP 2020 paper |
| `Mihara-Tate-Acyclicity-Uniformity-Berkovich-Adic-Spectra.pdf` | <https://arxiv.org/pdf/1403.7856> | arXiv author manuscript |
| `Stacks-Project-Authors-Stacks-Project.pdf` | <https://stacks.math.columbia.edu/download/book.pdf> | official open-source book build |
| `Temkin-Non-Archimedean-Pinchings.pdf` | <https://arxiv.org/pdf/2105.13692> | arXiv author manuscript |
| `Wedhorn-Adic-Spaces.pdf` | <https://arxiv.org/pdf/1910.05934> | arXiv author manuscript |

## Locator map for the added mathematical sources

The following are the locators relevant to the claims in the paper, rather
than merely places where the cited numerals happen to occur.

| Source | Relevant locators |
|---|---|
| Wedhorn, *Adic Spaces* | Proposition and Definition 6.36 (strongly noetherian Tate rings, p. 54); Remark 8.20 (the topological-ring sheaf condition, p. 80); Definition 8.26 (sheafy and stably sheafy f-adic rings, p. 81); Theorem 8.28(b) (strongly noetherian Tate rings, p. 81); Lemma 8.31, Corollary 8.32, Lemma 8.33, and Lemma 8.34 (the proof route through flatness and rational-cover acyclicity, pp. 82--84). |
| Huber, *A generalization of formal schemes and rigid analytic varieties* | Theorem 2.2 (the structure presheaf is a sheaf of complete topological rings, with rational acyclicity); Lemma 2.3 (finite-module maps are strict, and submodules are closed in the complete case); Lemma 2.4 (open mapping and strictness over a complete noetherian Tate ring). |
| Ben-Bassat--Kremnizer, *Non-Archimedean analytic geometry as relative algebraic geometry* | Definition 5.7 and Remark 5.8 (rational localizations, printed pp. 80--81); Lemmas 5.13 and 5.14 (strict two-term resolutions for the one-variable Weierstrass and Laurent cases, followed by factorization of a general rational localization, printed pp. 82--84). The paper does not use Koszul terminology or state strictness for the simultaneous multivariable complex. |
| Bambozzi--Kremnizer, *On the sheafyness property of spectra of Banach rings* | Definitions 4.5--4.6 and Proposition 4.9 (Koszul regularity and the Weierstrass/Laurent cases); in the final journal version, Lemma 4.11 and Corollary 4.13 (factorization and strict Koszul regularity of rational localizations). The local arXiv manuscript numbers the last two results Lemma 4.10 and Corollary 4.11. |

The Lean 4 and mathlib papers are software citations, not sources for a
mathematical lemma in the argument. The exact versions actually checked are
recorded below.

## Formalisation and code provenance

| Component | Exact source | Use and attribution |
|---|---|---|
| AINTLIB formalisation | `CBirkbeck/AINTLIB`, finite-jet commit `b007a4f3d4226f00a684b402715aa542e2f0bcdc` and weighted-parity commit `090a289211deb69117413e329325fe819aa7dbc2`, project `projects/AdicSpaces` | These are the immutable Git objects against which the paper's declaration crosswalk and axiom audit were run. The Paperforge site exposes the audited declarations from both commits directly. |
| Lean 4 | Toolchain `leanprover/lean4:v4.33.0-rc1`; tag commit `62eed1db4d67327ec8120be05f1a1b0847d74561` | Recorded by AINTLIB's root `lean-toolchain`. Upstream tag: <https://github.com/leanprover/lean4/releases/tag/v4.33.0-rc1>. Cite de Moura--Ullrich for the system. |
| mathlib4 | Commit `fd1d54bcac5caba4eff2ea3421c47d907333f515` | Recorded by AINTLIB's root `lake-manifest.json`; exact tree: <https://github.com/leanprover-community/mathlib4/tree/fd1d54bcac5caba4eff2ea3421c47d907333f515>. Cite the mathlib Community paper for the library, while retaining this commit for reproducibility. |
| William Coram restricted-power-series code | Upstream repository <https://github.com/WilliamCoram/PhD>, snapshot `e8fcf8fbff848a95475ab62ae2568cbb73961de8` (the last upstream commit before the 4 July 2026 vendoring), principally `PhD/PR'd/MvRestricted.lean`, `PhD/ToPR/MvGaussNorm.lean`, `PhD/ToPR/MvRestricted.lean`, `PhD/ToPR/GaussNorm.lean`, and `PhD/ToPR/RestrictedIso.lean` | Adapted in AINTLIB as `Vendored/CoramMvRestricted.lean`, `CoramMvGaussNorm.lean`, `CoramMvRestrictedNorm.lean`, `CoramRestrictedNorm.lean`, and `CoramRestrictedIso.lean`. The initial AINTLIB vendor commits are respectively `a6a128d567f26345d6653b9a8f275e024302a47c`, `5e4a87228793251a06a33966a446d7f46072fb1b`, `2322d3c045b68c3d42c4460d461ee31bcd9dd5fb`, `0cf1371881f2b1a0b90e0013fbf1d657ec17e406`, and `8cdb21d5dbce2ab6c19ce015d33103c93dd460f2`. Copyright William Coram; the upstream `LICENSE` and the vendored file headers specify Apache 2.0. |
| Bingyu Xia power-series equivalences | `WilliamCoram/PhD` at the same upstream snapshot, `PhD/Bryce/Basic.lean` and `PhD/Bryce/Equiv.lean` | Combined and adapted in AINTLIB as `Vendored/XiaMvPowerSeriesEquiv.lean`, introduced by AINTLIB commit `a522ed904b5d238fefcec87a1592498533e828dc`. The vendored header attributes Bingyu Xia and specifies Apache 2.0. |

The code-provenance rows above are in the actual dependency closure of the
finite-jet construction. In the audited snapshot,
`FJP/RestrictedLaurent.lean` imports `CoramRestrictedNorm` and
`CoramRestrictedIso`; those files transitively import the other Coram files
and `XiaMvPowerSeriesEquiv`. The AINTLIB copies at the audited commit, not the
pre-adaptation upstream files, are therefore the canonical sources for
reproducing the checked build.

No local PDF is supplied for Milnor. Its locator remains a manual verification
item. The Scottish Book citation points to a live web page and carries no
theorem locator for Paperforge to check.

Mechanical token matching is only the first stage of the reference audit. A
successful Paperforge check means that the cited number occurs in the matched
source; it does not by itself establish that the source supports the claim.
