# Pyrrho

Pyrrho is a tool for generating dynamic, syntax-highlighted texts, focusing at the moment on Ancient Greek. You can see it in action [here](https://vcar.dev/read/xenophon/anabasis/111/).

Annotated texts can come from different sources. At the moment, only the [AGLD Treebank format](https://perseusdl.github.io/treebank_data/) and [ConLL](https://universaldependencies.org/format.html) are supported, but there are plans to support arbitrary text via [CLTK](https://github.com/cltk/cltk).

## Getting started

```
# install python dependencies, build lexicon DB
make
```

### REST API

Run `make app`, then go to `/docs` or try `/corpus/ag/nt?ref=JOHN_1`.

### CLI

```
./pyrrho ls
./pyrrho preview ag nt JOHN_1
```
