# Pyrrho

Pyrrho is a tool for generating dynamic, syntax-highlighted texts, focusing at the moment on Ancient Greek.

Annotated texts can come from different sources. At the moment, only the [AGLD Treebank format](https://perseusdl.github.io/treebank_data/) is supported, but there are plans to support other formats, such as [ConLL](https://universaldependencies.org/format.html) and dynamic input via [CLTK](https://github.com/cltk/cltk).

## Getting started

```
# install python dependencies
poetry install
```

Run `make app` to try the REST API, then go to `/docs` or try `/corpus/ag/nt?ref=JOHN_1`.
