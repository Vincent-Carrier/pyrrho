py = poetry run python
lexicons = data/ag/lsj.db

.PHONY: default app clean

default: $(lexicons)
	$(py) -m cli.main $(args)


app: $(lexicons)
	$(py) -m app.main

clean:
	rm -f $(lexicons)

$(lexicons):
	$(py) -m core.seed

