filks
=====

Generates silly poems based off of mad-libbed, serious poems,
a tagged text corpus, and a pronunciation dictionary.


Requirements
============

1. Python 3.3+

Installation
============

To install:

```
pip install filks
filk install
```

The ``filk install`` step is not *strictly* necessary if you plan to
use strictly a library and corpus you already have installed; however
in most cases this will be most convenient.  This step downloads
the ``nltk`` library texts to your machine.

Usage
=====

To generate a terrible poem:

```
filk format
```

See ``filk format -h`` for options.

Development
===========

To build the dev environment:

```
make venv
. venv/bin/activate
python main.py
```

LICENSING
=========

All original source code in this repo,
including all *.py and configuration files,
is released under the MIT license included.

However, this library relies on corpuses from `nltk`
which may have a variety of free-ish licenses.

