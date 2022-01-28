# Phrase Tokenizer
[![pytest](https://github.com/ffreemt/phrase-tokenizer/actions/workflows/on-push.yml/badge.svg)](https://github.com/ffreemt/phrase-tokenizer/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://www.python.org/downloads/)[![Codacy Badge](https://app.codacy.com/project/badge/Grade/d7e1c1f44dbb423099a929aadd7db2fd)](https://www.codacy.com/gh/ffreemt/phrase-tokenizer/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ffreemt/phrase-tokenizer&amp;utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![PyPI version](https://badge.fury.io/py/phrase-tokenizer.svg)](https://badge.fury.io/py/phrase-tokenizer)

Tokenize an English sentence to phrases via benepar.

## Installation

```bash
pip install phrase-tokenizer
# pip install phrase-tokenizer -U to update
# or to install the latest from github:
# pip git+https://github.com/ffreemt/phrase-tokenizer.git
```

Or clone the repo `https://github.com/ffreemt/phrase-tokenizer.git`:

```bash
git clone https://github.com/ffreemt/phrase-tokenizer.git
cd phrase-tokenizer
pip install logzero benepar tensorflow
```
Or use `poetry`, e.g.
```bash
git clone https://github.com/ffreemt/phrase-tokenizer.git
cd phrase-tokenizer
poetry install
```

## Usage

```python
from phrase_tokenizer import phrase_tok

res = phrase_tok("Short cuts make long delays.")
print(res)
# ['Short cuts', 'make long delays']

# verbose=True turns on verbose to see the tokenizing process
res = phrase_tok("Short cuts make long delays", verbose=True)
# ',..Short.cuts,.make..long.delays..'
```

Consult the source code for details.

## For Developers

```bash
git clone https://github.com/ffreemt/phrase-tokenizer.git
cd phrase-tokenizer
pip install -r requirements-dev.txt
```

In `ipython`, ``plot_tree`` is able to draw a nice tree to aid the development, e.g.,

```python
from phrase_tokenizer.phrase_tok import plot_tree

plot_tree("Short cuts make long delays.")
```
![img](https://github.com/ffreemt/phrase-tokenizer/blob/master/img/short_cuts.png?raw=true)


