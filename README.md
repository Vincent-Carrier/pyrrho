# Pyrrho

Pyrrho is a REST API for generating dynamic, syntax-highlighted texts, focusing at the moment on Ancient Greek.

Annotated texts can come from different sources. At the moment, only the [AGLD Treebank format](https://perseusdl.github.io/treebank_data/) is supported, but there are plans to support other formats, such as [ConLL](https://universaldependencies.org/format.html) and dynamic input via [CLTK](https://github.com/cltk/cltk).

## Getting started

```
poetry install
poetry run python seed.py
poetry run python -m app.main
```

Then go to [/docs](http://0.0.0.0:8000/docs) or try [/corpus/ag/historiae?subdoc=1.1-1.4](http://0.0.0.0:8000/corpus/ag/historiae?subdoc=1.1-1.4)
