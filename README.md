# A 55-symbol definition of 2

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22089206.svg)](https://doi.org/10.5281/zenodo.22089206)

This repository records a first-order set-theoretic formula that uniquely
defines the von Neumann integer
`2 = {∅, {∅}}` in 55 symbols. Under the convention that `Rayo(n)`
allows at most `n` symbols, it proves

\[
\operatorname{Rayo}(55) \ge 3.
\]

## Formula

The canonical string is

```text
∃a(∃b(((a∈b∧(a∈x∧b∈x))∧(¬∃c(∃d((c∈d∧(d∈x∧(¬a=c)))))))))
```

It uses the grammar

```text
φ ::= u∈v | u=v | (¬φ) | (φ∧ψ) | ∃u(φ)
```

with one symbol for each variable, relation, connective, quantifier, and
parenthesis. The initially discovered display used `¬(φ)`; `formula.txt`
normalizes negation to Rayo's published `(¬φ)` convention without changing
the length.

## Verification

Run:

```console
python count.py
```

The parser recursively obtains

```text
6 atoms        × 3 = 18
5 conjunctions × 3 = 15
2 negations    × 3 =  6
4 existentials × 4 = 16
                       --
                       55
```

The full semantic proof is in [`note.pdf`](note.pdf), with reproducible source
in [`note.tex`](note.tex). The proof uses Extensionality and Foundation. It
establishes the 55-symbol upper bound on the naming length of `2`; it does not
claim that 55 is globally minimal.

## Contents

- `formula.txt` - canonical, whitespace-free formula
- `count.py` - parser, canonical serializer, and recursive symbol counter
- `note.tex` / `note.pdf` - complete proof and provenance note
- `CITATION.cff` - citation and release metadata
- `LICENSE` - MIT license

## Public baseline

As checked on 2026-08-25, the [Googology Wiki page on Rayo's
number](https://googology.fandom.com/wiki/Rayo%27s_number) listed a 56-symbol
formula for `2`. This repository improves that publicly listed construction by
one symbol. Rayo's own language and satisfaction presentation appear on the
[Big Number Duel page](https://web.mit.edu/arayo/www/bignums.html).

## Releases and Zenodo

The official GitHub--Zenodo integration is enabled for this repository. Release
[`v1.0.0`](https://github.com/fbhou/rayo-55/releases/tag/v1.0.0) is archived at
[version DOI `10.5281/zenodo.22089206`](https://doi.org/10.5281/zenodo.22089206).
The stable concept DOI for all versions is
[`10.5281/zenodo.22089205`](https://doi.org/10.5281/zenodo.22089205).

Each future GitHub release will be ingested automatically and assigned its own
version DOI. Zenodo reads the release metadata from `CITATION.cff`. See Zenodo's
guide to [archiving a GitHub release](https://help.zenodo.org/docs/github/archive-software/github-upload/).

## Provenance

GPT-5.6 Sol found the formula on 2026-08-25 in an interactive search assisted by
[OpenAI GPT-5.6 Sol](https://developers.openai.com/api/docs/models/gpt-5.6-sol).
The Git history separates the initial formula from later proof and packaging
revisions so their timestamps remain inspectable.
